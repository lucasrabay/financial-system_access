import torch.nn as nn

class PowerfulOrdinalNN(nn.Module):
    def __init__(self, in_features: int = 154, hidden1: int = 128, hidden2: int = 64, out_features: int = 2):
        super().__init__()
        self.fc1      = nn.Linear(in_features, hidden1)
        self.bn1      = nn.BatchNorm1d(hidden1)
        self.relu1    = nn.ReLU()
        self.dropout1 = nn.Dropout(0.4)
        self.fc2      = nn.Linear(hidden1, hidden2)
        self.bn2      = nn.BatchNorm1d(hidden2)
        self.relu2    = nn.ReLU()
        self.dropout2 = nn.Dropout(0.4)
        self.fc3      = nn.Linear(hidden2, out_features)

    def forward(self, x):
        x = self.fc1(x)
        x = self.bn1(x)
        x = self.relu1(x)
        x = self.dropout1(x)
        x = self.fc2(x)
        x = self.bn2(x)
        x = self.relu2(x)
        x = self.dropout2(x)
        x = self.fc3(x)
        return x
