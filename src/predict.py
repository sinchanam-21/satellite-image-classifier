import torch
from torchvision import transforms
from PIL import Image
from model import SatelliteCNN
import os

class Predictor:
    def __init__(self, model_path):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Load checkpoint
        checkpoint = torch.load(model_path, map_location=self.device)
        self.classes = checkpoint['classes']
        
        # Init model
        self.model = SatelliteCNN(num_classes=len(self.classes))
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.model.to(self.device)
        self.model.eval()

        self.transform = transforms.Compose([
            transforms.Resize((64, 64)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

    def predict(self, image_path):
        image = Image.open(image_path).convert('RGB')
        image = self.transform(image).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            outputs = self.model(image)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            confidence, predicted = torch.max(probabilities, 1)
            
        return {
            "class": self.classes[predicted.item()],
            "confidence": confidence.item(),
            "probabilities": {self.classes[i]: probabilities[0][i].item() for i in range(len(self.classes))}
        }

if __name__ == "__main__":
    # Test prediction if model exists
    model_path = r"c:\satellite-image-classifier\models\best_model.pth"
    if os.path.exists(model_path):
        predictor = Predictor(model_path)
        # You'd need an image to test here
        print("Predictor initialized successfully.")
    else:
        print("Model file not found. Please train the model first.")
