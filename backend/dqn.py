import torch
import torch.nn as nn


class DQNNet(nn.Module):
    def __init__(self, num_actions: int, num_pieces: int):
        super().__init__()

        self.grid_conv = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, stride=1, padding=1),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Flatten(),
        )

        self.embedding = nn.Sequential(
            nn.Embedding(num_pieces, 4),
            nn.ReLU(),
        )

        self.fc = nn.Sequential(
            nn.Linear(64 * 2 * 2 + 4, 256),
            nn.ReLU(),
            nn.Linear(256, 256),
            nn.ReLU(),
            nn.Linear(256, num_actions),
            nn.Sigmoid(),
        )

    def forward(self, grid: torch.Tensor, piece_idx: torch.Tensor) -> torch.Tensor:
        grid_vector = self.grid_conv(grid)
        piece_vector = self.embedding(piece_idx)
        x = torch.cat((grid_vector, piece_vector), dim=-1)
        return self.fc(x)
