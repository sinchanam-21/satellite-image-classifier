import torch
import torch.nn as nn
import torch.nn.functional as F

class SatelliteCNN(nn.Module):
    def __init__(self, num_classes=4):
        super(SatelliteCNN, self).__init__()
        # Input size: 3 x 64 x 64 (standard for this dataset)
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        
        # After 3 poolings (64->32->16->8)
        self.fc1 = nn.Linear(128 * 8 * 8, 512)
        self.fc2 = nn.Linear(512, num_classes)
        self.dropout = nn.Dropout(0.25)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = self.pool(F.relu(self.conv3(x)))
        
        x = x.view(-1, 128 * 8 * 8)
        x = self.dropout(x)
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        return x

if __name__ == "__main__":
    model = SatelliteCNN()
    print(model)
    test_input = torch.randn(1, 3, 64, 64)
    output = model(test_input)
    print(f"Output shape: {output.shape}")
