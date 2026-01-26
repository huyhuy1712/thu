import torch
from torch import nn, Tensor
import torch.nn.functional as F

class ConvLayer(nn.Module):
    def __init__(self, c_in, device =None):
        super(ConvLayer, self).__init__()
        padding = 1
        self.devive  =device
        self.downConv = nn.Conv1d(in_channels=c_in,
                                  out_channels=c_in, 
                                  padding=padding,
                                  kernel_size=3,
                                  padding_mode="circular")
        self.norm = nn.BatchNorm1d(c_in)
        self.activation = nn.ELU()
        self.maxPool = nn.MaxPool1d(kernel_size=52, stride=1, padding=0)  # distil 1/4
    
    def forward(self, x):
        x = x.permute(1,2,0)
        x = self.downConv(x)
        x = self.norm(x)
        x = self.activation(x)
        x = self.maxPool(x)
        x = x.permute(2, 0, 1)
        return x
    
class EncoderLayer(nn.Module):
    def __init__(self, attn, d_model, d_ff, dropout=0.1, activation = "relu"):
        super(EncoderLayer, self).__init__()
        self.d_ff = d_ff if d_ff != None else d_model*4
        self.attn = attn
        self.conv1 = nn.Conv1d(in_channels=d_model, out_channels=d_ff, kernel_size=1)
        self.conv2 = nn.Conv1d(in_channels=d_ff, out_channels=d_model, kernel_size=1)
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(dropout)
        self.activation = F.relu if activation == "relu" else F.gelu

    def forward(self, x, attn_mask = None):
        new_x = self.attn(
            x, x, x, attn_mask
        )
        x = self.activation(self.norm1(x + self.dropout(new_x)))
        y  = self.dropout(self.conv1(x.transpose(-1, 1)))
        y = self.dropout(self.conv2(y).transpose(-1, 1))
        return self.norm2(x+y)
    
class Encoder(nn.Module):
    def __init__(self, enc_layers, conv_layers=None, norm_layer=None):
        super(Encoder, self).__init__()
        self.enc_layers = nn.ModuleList(enc_layers)
        self.conv_layers = nn.ModuleList(conv_layers) if conv_layers is not None else None
        self.norm = norm_layer

    def forward(self, x, mask=None, src_key_padding_mask=None):
        # x: [L, B, D/F]
        if self.conv_layers is not None:
            for attn_layer, conv_layer in zip(self.enc_layers, self.conv_layers):
                x = attn_layer(x, attn_mask=mask)
                x = conv_layer(x)
            x = self.enc_layers[-1](x, attn_mask=mask)
        else:
            for attn_layer in self.enc_layers:
                x = attn_layer(x, attn_mask=mask)

        if self.norm is not None:
            x = self.norm(x)
        # x: [L//2, B, D/F]
        return x
    
class PBEEncoder(nn.TransformerEncoder):
    __constants__ = ['norm']
     
    def __init__(self, encoder_layer, num_layers, norm=None, enable_nested_tensor=False,
                 patience=1, inner_classifiers_config=None, projections_config=None):
        super(PBEEncoder, self).__init__(encoder_layer, num_layers, norm, enable_nested_tensor)
        self.patience = patience
        self.inner_classifiers = nn.ModuleList(
            [nn.Linear(inner_classifiers_config[0], inner_classifiers_config[1])
             for _ in range(num_layers)]
        )
        self.projections = nn.ModuleList(
            [nn.Linear(projections_config[0], projections_config[1])
             for _ in range(num_layers)]
        )
        
    def forward(self, src: Tensor, mask, src_key_padding_mask,
                training: bool = True):
        output = src
        # Check if model can use Nested Tensor Mode
        convert_to_nested = False
        first_layer = self.layers[0]
        if isinstance(first_layer, torch.nn.TransformerEncoderLayer):
            if (not first_layer.norm_first and not first_layer.training and
                    first_layer.self_attn.batch_first and
                    first_layer.self_attn._qkv_same_embed_dim and first_layer.activation_relu_or_gelu and
                    first_layer.norm1.eps == first_layer.norm2.eps and
                    src.dim() == 3 and self.enable_nested_tensor):
                if src_key_padding_mask is not None and not output.is_nested and mask is None:
                    tensor_args = (
                        src,
                        first_layer.self_attn.in_proj_weight,
                        first_layer.self_attn.in_proj_bias,
                        first_layer.self_attn.out_proj.weight,
                        first_layer.self_attn.out_proj.bias,
                        first_layer.norm1.weight,
                        first_layer.norm1.bias,
                        first_layer.norm2.weight,
                        first_layer.norm2.bias,
                        first_layer.linear1.weight,
                        first_layer.linear1.bias,
                        first_layer.linear2.weight,
                        first_layer.linear2.bias,
                    )
                    if not torch.overrides.has_torch_function(tensor_args):
                        if not torch.is_grad_enabled() or all([not x.requires_grad for x in tensor_args]):
                            if output.is_cuda or 'cpu' in str(output.device):
                                convert_to_nested = True
                                output = torch._nested_tensor_from_mask(output, src_key_padding_mask.logical_not())
        
        # Main Code
        if training or self.patience == 0:
            for i, mod in enumerate(self.layers):
                if convert_to_nested:
                    output = mod(output, src_mask=mask)
                else:
                    output = mod(output, src_mask=mask, src_key_padding_mask=src_key_padding_mask)  # [L, B, F/D]
                # mod_output = output
                # classifier_out = self.inner_classifiers[i](mod_output).squeeze().unsqueeze(0)  # [B, L, C]
                # _ = self.projections[i](classifier_out.permute(0, 2, 1)).squeeze(-1)  # [1, 100]
        else:
            patient_counter = 0
            patient_result = None
            calculated_layer_num = 0
            for i, mod in enumerate(self.layers):
                calculated_layer_num += 1
                if convert_to_nested:
                    output = mod(output, src_mask=mask)
                else:
                    output = mod(output, src_mask=mask, src_key_padding_mask=src_key_padding_mask)
                mod_output = output
                if self.norm is not None:
                    mod_output = self.norm(mod_output)  # [L, B, D/F]
                classifier_out = self.inner_classifiers[i](mod_output).squeeze().unsqueeze(0)  # [B, L, C]
                projection_out = self.projections[i](classifier_out.permute(0, 2, 1)).squeeze(-1)  # [1, 100]
                labels = projection_out.detach().argmax(dim=1)  # [1]
                if patient_result is not None:
                    patient_labels = patient_result.detach().argmax(dim=1)
                if (patient_result is not None) and torch.all(labels.eq(patient_labels)):
                    patient_counter += 1
                else:
                    patient_counter = 0
                patient_result = projection_out
                if patient_counter == self.patience:
                    break
            # print(f"calculated_enc_layer_num: {calculated_layer_num}")

        if convert_to_nested:
            output = output.to_padded_tensor(0.)

        if self.norm is not None:
            output = self.norm(output)

        return output
    
class EncoderStack(nn.Module):
    def __init__(self, encoders, inp_lens):
        super(EncoderStack, self).__init__()
        self.encoders = nn.ModuleList(encoders)
        self.inp_lens = inp_lens

    def forward(self, x, mask=None, src_key_padding_mask=None, training=True):
        # x: [L, B, F/D] -> [L', B, F/D]
        x_stack = []
        for i_len, encoder in zip(self.inp_lens, self.encoders):  # inp_lens: 0, 1, 2
            inp_len = x.shape[0] // (2 ** i_len)
            x_s = encoder(x[-inp_len:, :, :])
            x_stack.append(x_s)
        x_stack = torch.cat(x_stack, 0)
        return x_stack
