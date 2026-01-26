import torch
import torch.nn as nn
import torch.nn.functional as F

import numpy as np

from math import sqrt

class ProbMask():
    def __init__(self, B, H, L,  index, scores, device="cpu"):
        _mask = torch.ones(L, scores.shape[-1],dtype=torch.bool).to(device).triu(1)
        _mask_exp = _mask.unsqueeze(0).unsqueeze(0).expand(B, H, L, scores.shape[-1])
        indicator = _mask_exp[torch.arange(B)[:, None, None],
                    torch.arange(H)[None, :, None],
                    index, :].to(device)
        self._mask = indicator.view(scores.shape).to(device)

    @property
    def mask(self):
        return

class ProbAttention(nn.Module):
    def __init__(self, mask_flag=False, factor=5, scale=None, 
                 attention_dropout=0.1, output_attention=True):
        super(ProbAttention, self).__init__()
        self.factor = factor
        self.scale = scale
        self.mask_flag = mask_flag
        self.output_attention = output_attention
        self.dropout = nn.Dropout(attention_dropout)
        
    def _prob_QK(self, Q, K, sample_k, n_top):
        B, H, L_K, E  = K.shape
        _, _, L_Q, _  = Q.shape
         # calculate the sampled Q_K
        K_expand = K.unsqueeze(-3).expand(B, H, L_Q, L_K, E)
        sample_index = np.random.randint(low=0, high=L_K, size=(L_Q, sample_k))
        K_sample = K_expand[:, :, torch.arange(L_Q).unsqueeze(1), sample_index, :]
        Q_K_sample = torch.matmul(Q.unsqueeze(-2), K_sample.transpose(-2, -1)).squeeze(-2)
        
        # find the Top_k query with sparisty measurement
        M = Q_K_sample.max(-1).values - torch.div(Q_K_sample.sum(-1), L_K)
        M_top = M.topk(n_top, sorted=False)[1]
        
        # Caculate Q reduced
        Q_reduce = Q[torch.arange(B)[:, None, None],
                   torch.arange(H)[None, :, None],
                   M_top, :]
        Q_K = torch.matmul(Q_reduce, K.transpose(-2, -1))
        
        return Q_K, M_top
    
    def _get_initial_context(self, V, L_Q):
        B, H, L_V, D = V.shape
        if not self.mask_flag:
            # V_sum = V.sum(dim=-2)
            V_sum = V.mean(dim=-2)
            contex = V_sum.unsqueeze(-2).expand(B, H, L_Q, V_sum.shape[-1]).clone()
        else:  # use mask
            assert (L_Q == L_V)  # requires that L_Q == L_V, i.e. for self-attention only
            contex = V.cumsum(dim=-2)
        return contex
    
    def _update_context(self, context_in, V, scores, index, L_Q, attn_mask):
        B, H, L_V, D = V.shape

        if self.mask_flag:
            attn_mask = ProbMask(B, H, L_Q, index, scores, device=V.device)
            scores.masked_fill_(attn_mask.mask, -np.inf)

        attn = torch.softmax(scores, dim=-1)  # nn.Softmax(dim=-1)(scores)

        context_in[torch.arange(B)[:, None, None],
        torch.arange(H)[None, :, None],
        index, :] = torch.matmul(attn, V).type_as(context_in)
        if self.output_attention:
            attns = (torch.ones([B, H, L_V, L_V]) / L_V).type_as(attn).to(attn.device)
            attns[torch.arange(B)[:, None, None], torch.arange(H)[None, :, None], index, :] = attn
            return (context_in, attns)
        else:
            return (context_in, None)
        
    def forward(self, queries, keys, values, attn_mask):
        B, L_Q, H, D = queries.shape
        _, L_K, _, _ = keys.shape
        
        queries = queries.transpose(2, 1)
        keys = keys.transpose(2, 1)
        values = values.transpose(2, 1)
        
        U_part = self.factor * np.ceil(np.log(L_K)).astype('int').item()  # c*ln(L_k)
        u = self.factor * np.ceil(np.log(L_Q)).astype('int').item()  # c*ln(L_q)
        
        U_part = min(U_part, L_K)
        u = min(u, L_Q)
        
        scores_top, index = self._prob_QK(queries, keys, U_part, u)
        
        scale = self.scale if self.scale!=None else 1. / sqrt(D)

        if scale is not None:
            scores_top = scores_top * scale
        
        context = self._get_initial_context(values, L_Q)
        
        context, attn = self._update_context(context, values, 
                                             scores_top, index, L_Q, attn_mask)
        
        return context.transpose(2, 1).contiguous(), attn
    
class AttentionLayer(nn.Module):
    def __init__(self, attn, d_model, n_heads, d_keys=None, d_values=None, mix= None):
        super(AttentionLayer, self).__init__()
        
        d_keys = d_keys if d_keys!=None else (d_model // n_heads)
        d_values = d_values if d_values!=None else (d_model // n_heads)
        
        self.inner_attn = attn
        self.query_projection = nn.Linear(d_model, d_keys * n_heads)
        self.key_projection = nn.Linear(d_model, d_keys * n_heads)
        self.value_projection = nn.Linear(d_model, d_values * n_heads)
        self.out_projection = nn.Linear(d_values * n_heads, d_model)
        self.num_heads = n_heads
        self.mix = mix
        self.batch_first = None
        self._qkv_same_embed_dim = True
        self.attention_scores = None
        
    def forward(self, queries, keys, values, attn_mask, 
                key_padding_mask=None, need_weights=False, is_causal=None):
        
        queries = queries.permute(1, 0, 2).type(dtype=torch.float32)
        keys = keys.permute(1, 0, 2).type(dtype=torch.float32)
        values = values.permute(1, 0, 2).type(dtype=torch.float32)
        
        B, L, _ = queries.shape
        _, S, _ = keys.shape
        H = self.num_heads
        
        queries = self.query_projection(queries).view(B, L, H, -1)
        keys = self.key_projection(keys).view(B, L, H, -1)
        values = self.value_projection(values).view(B, L, H, -1)

        out, self.attention_scores = self.inner_attn(
            queries,
            keys,
            values,
            attn_mask
        ) 
        if self.mix:
            out = out.transpose(2, 1).contiguous()
        out = out.view(B, L, -1)

        out = self.out_projection(out)
        out = out.permute(1, 0, 2).type(dtype=torch.float32)

        # print(f"out from prob_spare attention: {out.shape}")
        return out