

from typing import List, Tuple, Dict, Any
import torch
import torch.nn as nn
import torch.nn.functional as F

class GRU4Rec(nn.Module):
    """
    Simple GRU-based next-item prediction model.
    Input: sequence of item indices (batch_size, seq_len)
    Output: logits over item vocabulary (batch_size, vocab_size)
    """
    def __init__(self, vocab_size: int, embed_dim: int = 128, hidden_dim: int = 128, n_layers: int = 1, dropout: float = 0.2):
        super().__init__()
        self.vocab_size = vocab_size
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.gru = nn.GRU(embed_dim, hidden_dim, num_layers=n_layers, batch_first=True, dropout=dropout)
        self.fc = nn.Linear(hidden_dim, vocab_size)

    def forward(self, input_seq: torch.LongTensor) -> torch.Tensor:
        """
        input_seq: (batch, seq_len)
        returns logits for next item: (batch, vocab_size)
        """
        emb = self.embedding(input_seq)  # (batch, seq_len, embed_dim)
        _, h = self.gru(emb)  # h: (n_layers, batch, hidden_dim)
        h = h[-1]  # last layer (batch, hidden_dim)
        logits = self.fc(h)  # (batch, vocab_size)
        return logits

class SimpleSASRec(nn.Module):
    """
    Very simplified transformer-style model for session sequences.
    Not a drop-in full SASRec. Use this as a starting point.
    """
    def __init__(self, vocab_size: int, embed_dim: int = 128, n_heads: int = 4, num_layers: int = 2, dropout: float = 0.1):
        super().__init__()
        self.vocab_size = vocab_size
        self.item_emb = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        encoder_layer = nn.TransformerEncoderLayer(d_model=embed_dim, nhead=n_heads, dropout=dropout)
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        self.fc = nn.Linear(embed_dim, vocab_size)

    def forward(self, input_seq: torch.LongTensor) -> torch.Tensor:
        """
        input_seq: (batch, seq_len)
        transformer expects (seq_len, batch, embed)
        """
        emb = self.item_emb(input_seq)  # (batch, seq_len, embed)
        emb = emb.permute(1,0,2)  # (seq_len, batch, embed)
        out = self.transformer(emb)  # (seq_len, batch, embed)
        # use last position
        last = out[-1]  # (batch, embed)
        logits = self.fc(last)  # (batch, vocab_size)
        return logits

# Utility for negative sampling and dataset
class SequenceDataset(torch.utils.data.Dataset):
    """
    Prepare sequences for training session models.
    Each example is (sequence_tensor, target_item)
    Sequences are padded to max_len.
    """
    def __init__(self, sessions: List[List[int]], max_len: int = 50, pad_idx: int = 0):
        self.sessions = sessions
        self.max_len = max_len
        self.pad_idx = pad_idx

    def __len__(self):
        return len(self.sessions)

    def __getitem__(self, idx):
        seq = self.sessions[idx]
        # input is all but last item, target is last item
        input_seq = seq[:-1][-self.max_len:]
        target = seq[-1]
        # pad on left
        pad_len = self.max_len - len(input_seq)
        if pad_len > 0:
            input_seq = [self.pad_idx] * pad_len + input_seq
        return torch.LongTensor(input_seq), torch.LongTensor([target]).squeeze(0)
