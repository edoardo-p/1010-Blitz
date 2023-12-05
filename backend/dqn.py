import torch
import torch.nn as nn


class DQNNet(nn.Module):
    def __init__(self, num_actions: int):
        super().__init__()

        self.grid_conv = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, stride=1, padding=1),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Flatten(),
        )

        self.embedding = nn.Sequential(
            nn.Embedding(19, 4),
            nn.Linear(4, 64),
            nn.ReLU(),
        )

        self.fc = nn.Sequential(
            nn.Linear(64 * 2 * 2 + 64, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, num_actions),
            nn.Sigmoid(),
        )

    def forward(self, grid: torch.Tensor, piece_idx: torch.Tensor) -> torch.Tensor:
        grid_vector = self.grid_conv(grid)
        piece_vector = self.embedding(piece_idx)
        x = torch.cat((grid_vector, piece_vector), dim=-1)
        return self.fc(x)
