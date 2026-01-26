import torch
import torch.nn as nn
from torch import Tensor
import torch.nn.functional as F
from torch.nn.modules.normalization import LayerNorm
from torch.nn.modules.transformer import TransformerEncoder, TransformerEncoderLayer, TransformerDecoder
from typing import Optional, Union, Callable
from .attention import AttentionLayer, ProbAttention
from .decoder import DecoderLayer, PBEEDecoder
from .encoder import Encoder, EncoderLayer, ConvLayer, EncoderStack, PBEEncoder
from .utils import get_sequence_list


class FeatureIsolatedTransformer(nn.Transformer):
    def __init__(self, d_model_list: list, nhead_list: list, num_encoder_layers: int, num_decoder_layers: int,
                 dim_feedforward: int = 2048, dropout: float = 0.1,
                 activation: Union[str, Callable[[Tensor], Tensor]] = F.relu, output_attention: str = True,
                 inner_classifiers_config: list = None, patience: int = 1, use_pyramid_encoder: bool = False,
                 distil: bool = False, projections_config: list = None,
                 IA_encoder: bool = False, IA_decoder: bool = False, device=None, use_cross_attn = False):

        super(FeatureIsolatedTransformer, self).__init__(sum(d_model_list), nhead_list[-1], num_encoder_layers,
                                                         num_decoder_layers, dim_feedforward, dropout, activation)
        del self.encoder
        self.use_cross_attn = use_cross_attn
        self.l2body_attn = None
        self.r2l_attn = None
        self.body_to_hand_proj = None

        if self.use_cross_attn:
            self.l2body_attn = nn.MultiheadAttention(d_model_list[0], num_heads=1, batch_first=True)
            self.r2l_attn = nn.MultiheadAttention(d_model_list[1], num_heads=1, batch_first=True)
            self.body_to_hand_proj = nn.Linear(120, 63)


        self.d_model = sum(d_model_list)
        self.d_ff = dim_feedforward
        self.dropout = dropout
        self.num_encoder_layers = num_encoder_layers
        self.num_decoder_layers = num_decoder_layers
        self.device = device
        self.use_pyramid_encoder = use_pyramid_encoder
        self.use_IA_encoder = IA_encoder
        self.use_IA_decoder = IA_decoder
        self.inner_classifiers_config = inner_classifiers_config
        self.projections_config = projections_config
        self.patience = patience
        self.distil = distil
        self.activation = activation
        self.output_attention = output_attention
        self.l_hand_encoder = self.get_custom_encoder(d_model_list[0], nhead_list[0])
        self.r_hand_encoder = self.get_custom_encoder(d_model_list[1], nhead_list[1])
        self.body_encoder = self.get_custom_encoder(d_model_list[2], nhead_list[2])
        self.decoder = self.get_custom_decoder(nhead_list[-1])
        self._reset_parameters()

    def get_custom_encoder(self, f_d_model: int, nhead: int):
        Attn = ProbAttention

        if self.use_pyramid_encoder:
            # print("Pyramid encoder")
            # print(f'self.distl {self.distil}')
            e_layers = get_sequence_list(self.num_encoder_layers)
            inp_lens = list(range(len(e_layers)))
            encoders = [
                Encoder(
                    [
                        EncoderLayer(
                            AttentionLayer(
                                Attn(output_attention=self.output_attention),
                                f_d_model, nhead, mix=False),
                            f_d_model,
                            self.d_ff,
                            dropout=self.dropout,
                            activation=self.activation
                        ) for _ in range(el)
                    ],
                    [
                        ConvLayer(
                            f_d_model, self.device
                        ) for _ in range(self.num_encoder_layers - 1)
                    ] if self.distil else None,
                    norm_layer=torch.nn.LayerNorm(f_d_model)
                ) for el in e_layers]

            encoder = EncoderStack(encoders, inp_lens)
        else:
            encoder_layer = TransformerEncoderLayer(f_d_model, nhead, self.d_ff, self.dropout, self.activation)
            # Replace the default self-attention module with the custom one
            encoder_layer.self_attn = AttentionLayer(
                Attn(output_attention=self.output_attention),
                f_d_model, nhead, mix=False
            )
            encoder_norm = LayerNorm(f_d_model)

            if self.use_IA_encoder:
                # print("Encoder with input adaptive")
                self.inner_classifiers_config[0] = f_d_model
                encoder = PBEEncoder(
                    encoder_layer, self.num_encoder_layers, norm=encoder_norm,
                    inner_classifiers_config=self.inner_classifiers_config,
                    projections_config=self.projections_config,
                    patience=self.patience
                )
            else:
                # print("Normal encoder")
                encoder = TransformerEncoder(encoder_layer, self.num_encoder_layers, norm=encoder_norm)

        return encoder

    def get_custom_decoder(self, nhead):
        decoder_layer = DecoderLayer(self.d_model, nhead, self.d_ff)
        decoder_norm = LayerNorm(self.d_model)
        if self.use_IA_decoder:
            # print("Decoder with with input adaptive")
            return PBEEDecoder(
                decoder_layer, self.num_decoder_layers, norm=decoder_norm,
                inner_classifiers_config=self.inner_classifiers_config, patient=self.patience
            )
        else:
            # print("Normal decoder")
            return TransformerDecoder(
                decoder_layer, self.num_decoder_layers, norm=decoder_norm)

    def checker(self, full_src, tgt, is_batched):
        if not self.batch_first and full_src.size(1) != tgt.size(1) and is_batched:
            raise RuntimeError("the batch number of src and tgt must be equal")
        elif self.batch_first and full_src.size(0) != tgt.size(0) and is_batched:
            raise RuntimeError("the batch number of src and tgt must be equal")
        if full_src.size(-1) != self.d_model or tgt.size(-1) != self.d_model:
            print(self.d_model)
            print(full_src.size())
            print(tgt.size())
            raise RuntimeError("the feature number of src and tgt must be equal to d_model")

    def forward(self, src: list, tgt: Tensor, src_mask: Optional[Tensor] = None, tgt_mask: Optional[Tensor] = None,
                memory_mask: Optional[Tensor] = None, src_key_padding_mask: Optional[Tensor] = None,
                tgt_key_padding_mask: Optional[Tensor] = None, memory_key_padding_mask: Optional[Tensor] = None,
                src_is_causal: Optional[bool] = None, tgt_is_causal: Optional[bool] = None,
                memory_is_causal: bool = False, training: bool = True) -> Tensor:

        full_src = torch.cat(src, dim=-1)
        self.checker(full_src, tgt, full_src.dim() == 3)

        # code for concurrency is removed...
        if self.use_IA_encoder:
            l_hand_memory = self.l_hand_encoder(src[0], mask=src_mask, src_key_padding_mask=src_key_padding_mask,
                                                training=training)
            r_hand_memory = self.r_hand_encoder(src[1], mask=src_mask, src_key_padding_mask=src_key_padding_mask,
                                                training=training)
            body_memory = self.body_encoder(src[2], mask=src_mask, src_key_padding_mask=src_key_padding_mask,
                                            training=training)
        else:
            l_hand_memory = self.l_hand_encoder(src[0], mask=src_mask, src_key_padding_mask=src_key_padding_mask)
            r_hand_memory = self.r_hand_encoder(src[1], mask=src_mask, src_key_padding_mask=src_key_padding_mask)
            body_memory = self.body_encoder(src[2], mask=src_mask, src_key_padding_mask=src_key_padding_mask)

        if self.use_cross_attn:
            # Example: Parallel Body -> Hands
            body_memory_proj_l = self.body_to_hand_proj(body_memory) # Assuming proj adapts to l_hand dim
            body_memory_proj_r = self.body_to_hand_proj(body_memory) # Assuming proj adapts to r_hand dim (or use separate projections)

            l_crossed, _ = self.l2body_attn(l_hand_memory, body_memory_proj_l, body_memory_proj_l)
            r_crossed_body, _ = self.r2l_attn(r_hand_memory, body_memory_proj_r, body_memory_proj_r) # Reusing r2l_attn layer name, but logic is Body->RHand

            # Combine Body attention results (example: simple addition)
            l_hand_memory = l_crossed + l_hand_memory
            r_hand_memory_temp = r_crossed_body + r_hand_memory # Temporary variable

            # Optional: Hand-to-Hand attention
            r_crossed_l, _ = self.r2l_attn(r_hand_memory_temp, l_hand_memory, l_hand_memory)
            r_hand_memory = r_crossed_l + r_hand_memory_temp # Final r_hand memory
         
        full_memory = torch.cat((l_hand_memory, r_hand_memory, body_memory), -1)

        if self.use_IA_decoder:
            output = self.decoder(tgt, full_memory, tgt_mask=tgt_mask, memory_mask=memory_mask,
                                  tgt_key_padding_mask=tgt_key_padding_mask,
                                  memory_key_padding_mask=memory_key_padding_mask, training=training)
        else:
            output = self.decoder(tgt, full_memory, tgt_mask=tgt_mask, memory_mask=memory_mask,
                                  tgt_key_padding_mask=tgt_key_padding_mask,
                                  memory_key_padding_mask=memory_key_padding_mask)

        return output

class CustomLearnedAbsolutePE(nn.Module):
    """
    Implements a Learned Absolute Positional Encoding with a specific,
    non-standard initialization method preserved from the original SiFormer.

    The positional encodings are stored as a learnable nn.Parameter and
    added to the input sequence embeddings. Includes optional dropout.
    """
    def __init__(self, d_model: int, max_len: int = 30, dropout: float = 0.1):
        """
        Args:
            d_model (int): The feature dimension of the embeddings.
            max_len (int): The maximum sequence length anticipated.
            dropout (float): Dropout probability applied after adding PE. Defaults to 0.1.
        """
        super().__init__()
        self.d_model = d_model
        self.max_len = max_len
        self.dropout = nn.Dropout(p=dropout)

        # Initialize the positional encoding table using the specific, vectorized method
        initial_pe_value = self._initialize_encoding_table_vectorized(d_model, max_len)

        # Create the learnable parameter
        # Shape: [max_len, 1, d_model] for broadcasting with [seq_len, batch_size, d_model] input
        self.pos_embedding = nn.Parameter(initial_pe_value, requires_grad=True)

        # Buffer for position indices (optional, but good practice if needed elsewhere)
        # Not strictly needed for this implementation as we slice the embedding directly.
        # self.register_buffer('positions', torch.arange(max_len).unsqueeze(1))

    @staticmethod
    def _initialize_encoding_table_vectorized(d_model: int, seq_len: int) -> torch.Tensor:
        """
        Replicates the original SiFormer get_encoding_table initialization logic
        using efficient, vectorized PyTorch operations.

        Initializes a tensor where all features j >= 0 for a given position i
        are copies of the initial random value generated for feature j=0 at position i.
        This specific initialization is preserved for consistency with the original model.

        Args:
            d_model (int): The feature dimension.
            seq_len (int): The maximum sequence length.

        Returns:
            torch.Tensor: Initialized positional encoding tensor of shape [seq_len, 1, d_model].
        """
        # Ensure reproducibility if the original relied on this seed
        torch.manual_seed(42)

        # 1. Generate random values for the *first* feature dimension for all positions
        # Shape: [seq_len, 1]
        first_feature_values = torch.rand(seq_len, 1)

        # 2. Expand (repeat without copying memory) these values across the d_model dimension
        # Shape: [seq_len, d_model]
        # Note: expand() is memory efficient. If requires_grad=True later, gradients
        # will flow back correctly to the original 'first_feature_values' if it were part of the graph.
        # Here, it's just initialization data, so expand is fine.
        frame_pos = first_feature_values.repeat(1, d_model)

        # 3. Add the singleton dimension for broadcasting (like the original unsqueeze(1))
        # Shape becomes [seq_len, 1, d_model]
        frame_pos = frame_pos.unsqueeze(1)

        return frame_pos

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Adds the learned positional encoding to the input tensor, followed by dropout.

        Args:
            x (torch.Tensor): Input tensor of shape [seq_len, batch_size, d_model].
                           Assumes input is already on the correct device.

        Returns:
            torch.Tensor: Output tensor with positional encodings added and dropout applied,
                          same shape as input [seq_len, batch_size, d_model].
        """
        seq_len = x.size(0)

        # Check if input sequence length exceeds the max_len this PE was initialized for
        if seq_len > self.max_len:
            # Option 1: Raise error (safer)
            raise ValueError(
                f"Input sequence length ({seq_len}) exceeds the maximum length "
                f"({self.max_len}) supported by this positional encoding layer."
            )
            # Option 2: Allow truncation (might hide errors)
            # seq_len = self.max_len
            # x = x[:seq_len]

        # Slice the positional embedding tensor to match the input sequence length
        # self.pos_embedding shape: [max_len, 1, d_model]
        # Sliced pe shape: [seq_len, 1, d_model]
        # Ensures gradients flow back to the *sliced part* of the nn.Parameter
        pe = self.pos_embedding[:seq_len] # Equivalent to [:seq_len, :, :] due to shape

        # Add positional encoding to the input tensor.
        # Broadcasting handles the batch dimension:
        # [seq_len, batch_size, d_model] + [seq_len, 1, d_model] -> [seq_len, batch_size, d_model]
        x = x + pe

        # Apply dropout
        return self.dropout(x)


class SiFormerMobile(nn.Module):
    """
    Implementation of the SPOTER (Sign POse-based TransformER) architecture for sign language recognition from sequence
    of skeletal data.
    """

    def __init__(
        self,
        num_classes,
        num_hid=246,
        num_enc_layers=3,
        num_dec_layers=2,
        patience=1,
        seq_len=5,
        device=None,
        IA_encoder=True,
        IA_decoder=False,
        cross_attn=False,
        use_pyramid_encoder=False,
        dropout=0.1,
    ):
        super(SiFormerMobile, self).__init__()
        # print("Feature isolated transformer")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.seq_len = seq_len

        # self.l_hand_embedding = nn.Parameter(self.get_encoding_table(d_model=63))
        # self.r_hand_embedding = nn.Parameter(self.get_encoding_table(d_model=63))
        # self.body_embedding = nn.Parameter(self.get_encoding_table(d_model=120))

        self.l_hand_embedding = CustomLearnedAbsolutePE(d_model=63, max_len=seq_len, dropout=dropout)
        self.r_hand_embedding = CustomLearnedAbsolutePE(d_model=63, max_len=seq_len, dropout=dropout)
        self.body_embedding = CustomLearnedAbsolutePE(d_model=120, max_len=seq_len, dropout=dropout)

        self.class_query = nn.Parameter(torch.rand(1, 1, num_hid))
        self.transformer = FeatureIsolatedTransformer(
            [21 * 3, 21 * 3, 40 * 3],
            [3, 3, 2, 2],
            num_encoder_layers=num_enc_layers,
            num_decoder_layers=num_dec_layers,
            IA_encoder=IA_encoder,
            IA_decoder=IA_decoder,
            inner_classifiers_config=[num_hid, num_classes],
            projections_config=[seq_len, 1],
            device=device,
            patience=patience,
            use_pyramid_encoder=use_pyramid_encoder,
            distil=False,
            use_cross_attn=cross_attn,
            dropout=dropout,
        )
        self.projection = nn.Linear(num_hid, num_classes)

    def pad_or_truncate_sequence(self, x, target_len):
        """
        x: Tensor of shape [seq_len, batch_size, features]
        target_len: int, desired sequence length

        Returns:
            Tensor of shape [target_len, batch_size, features]
        """
        seq_len = x.size(0)

        if seq_len < target_len:
            pad_size = target_len - seq_len
            padding = torch.zeros(pad_size, x.size(1), x.size(2), device=x.device, dtype=x.dtype)
            x = torch.cat([x, padding], dim=0)
        elif seq_len > target_len:
            x = x[:target_len]

        return x

    def forward(self, X, training=False):
        X = X.permute(1, 0, 2)  # (246, 16, 30)
        target_seq_len = self.seq_len
        # Input shape: (82, 3, batch_size, seq_len) -> Reshape to separate landmarks
        X = X.view(82, 3, X.shape[1], X.shape[2])
        # Reorder to (batch_size, seq_len, 82, 3)
        X = X.permute(2, 3, 0, 1)

        # Split into body parts: each shape (batch_size, seq_len, n_landmarks, 3)
        l_hand = X[:, :, :21, :]  # Left hand: 21 landmarks
        r_hand = X[:, :, 21:42, :]  # Right hand: 21 landmarks
        body = X[:, :, 42:, :]  # Body: 40 landmarks
        batch_size = l_hand.size(0)

        # Flatten landmarks and coordinates: (batch_size, seq_len, n_landmarks * 3)
        new_l_hand = l_hand.view(l_hand.size(0), l_hand.size(1), l_hand.size(2) * l_hand.size(3))  # Shape: (B, T, 63)
        new_r_hand = r_hand.view(r_hand.size(0), r_hand.size(1), r_hand.size(2) * r_hand.size(3))  # Shape: (B, T, 63)
        body = body.view(body.size(0), body.size(1), body.size(2) * body.size(3))  # Shape: (B, T, 120)

        # Permute to (seq_len, batch_size, feature_size)
        new_l_hand = new_l_hand.permute(1, 0, 2).type(dtype=torch.float32)  # Shape: (T, B, 63)
        new_r_hand = new_r_hand.permute(1, 0, 2).type(dtype=torch.float32)  # Shape: (T, B, 63)
        new_body = body.permute(1, 0, 2).type(dtype=torch.float32)  # Shape: (T, B, 120)

        # Pad or truncate sequences to target length
        new_l_hand = self.pad_or_truncate_sequence(new_l_hand, target_seq_len)
        new_r_hand = self.pad_or_truncate_sequence(new_r_hand, target_seq_len)
        new_body = self.pad_or_truncate_sequence(new_body, target_seq_len)

        # Add positional embeddings (Learned PE):
        # l_hand_in = new_l_hand.to(self.device) + self.l_hand_embedding[:new_l_hand.size(0), :, :]
        # r_hand_in = new_r_hand.to(self.device) + self.r_hand_embedding[:new_r_hand.size(0), :, :]
        # body_in = new_body.to(self.device) + self.body_embedding[:new_body.size(0), :, :]

        l_hand_in = self.l_hand_embedding(new_l_hand.to(self.device))
        r_hand_in = self.r_hand_embedding(new_r_hand.to(self.device))
        body_in = self.body_embedding(new_body.to(self.device))

        transformer_output = self.transformer(
            [l_hand_in, r_hand_in, body_in], self.class_query.repeat(1, batch_size, 1), training=training
        ).transpose(0, 1)

        # Final projection to class probabilities: (batch_size, num_classes)
        out = self.projection(transformer_output).squeeze()
        return out

    @staticmethod
    def get_encoding_table(d_model=108, seq_len=5):
        torch.manual_seed(42)
        tensor_shape = (seq_len, d_model)
        frame_pos = torch.rand(tensor_shape)
        for i in range(tensor_shape[0]):
            for j in range(1, tensor_shape[1]):
                frame_pos[i, j] = frame_pos[i, j - 1]
        frame_pos = frame_pos.unsqueeze(1)  # (seq_len, 1, feature_size): (seq_len, 1, d_model)
        return frame_pos