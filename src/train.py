import torch
import torch.nn as nn
import torch.optim as optim
import os
from model import SatelliteCNN
from data_loader import get_data_loaders

def train_model():
    print("Initializing training process...")
    # Config
    DATA_DIR = r"c:\satellite-image-classifier\data"
    MODEL_SAVE_PATH = r"c:\satellite-image-classifier\models\best_model.pth"
    BATCH_SIZE = 32
    EPOCHS = 10
    LEARNING_RATE = 0.001

    print(f"Loading data from {DATA_DIR}...")

    if not os.path.exists(r"c:\satellite-image-classifier\models"):
        os.makedirs(r"c:\satellite-image-classifier\models")

    # Device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # Load data
    train_loader, val_loader, classes = get_data_loaders(DATA_DIR, BATCH_SIZE)
    print(f"Classes: {classes}")

    # Init model, loss, optimizer
    model = SatelliteCNN(num_classes=len(classes)).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

    best_val_acc = 0.0

    # Training loop
    for epoch in range(EPOCHS):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0

        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()

        train_acc = 100 * correct / total
        
        # Validation
        model.eval()
        val_correct = 0
        val_total = 0
        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs)
                _, predicted = outputs.max(1)
                val_total += labels.size(0)
                val_correct += predicted.eq(labels).sum().item()

        val_acc = 100 * val_correct / val_total
        print(f"Epoch {epoch+1}/{EPOCHS} - Loss: {running_loss/len(train_loader):.4f}, Train Acc: {train_acc:.2f}%, Val Acc: {val_acc:.2f}%")

        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save({
                'model_state_dict': model.state_dict(),
                'classes': classes
            }, MODEL_SAVE_PATH)
            print(f"--- Model saved with accuracy: {val_acc:.2f}% ---")

if __name__ == "__main__":
    train_model()
