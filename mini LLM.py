import torch
import torch.nn as nn

class MiniLLM(nn.Module):
    def __init__(self, vocab_size, embed_size):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_size)
        self.transformer = nn.Transformer(
            d_model=embed_size,
            nhead=4,
            num_encoder_layers=2
        )
        self.fc = nn.Linear(embed_size, vocab_size)

    def forward(self, x):
        x = self.embedding(x)
        x = self.transformer(x, x)
        return self.fc(x)

model = MiniLLM(vocab_size=10000, embed_size=128)