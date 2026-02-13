# SatelliteEye - Advanced Satellite Image Classifier

A premium, end-to-end deep learning system designed to classify satellite imagery with high precision.

![Thumbnail](https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?q=80&w=1000&auto=format&fit=crop)

## 🚀 Features
- **High Precision CNN**: Custom-built Convolutional Neural Network optimized for terrain classification.
- **Real-time Inference**: Ultra-fast prediction pipeline using PyTorch.
- **Glassmorphism UI**: A stunning, modern web interface with HSL-based dynamic styling and smooth animations.
- **Drag & Drop**: Seamless image uploading for instant analysis.
- **Probability Breakdown**: Detailed class-wise distribution for informed decision making.

## 🛠️ Technology Stack
- **AI Core**: PyTorch, Torchvision
- **Data**: NumPy, Pillow
- **API**: Flask
- **Aesthetics**: Vanilla CSS (Custom Design System), FontAwesome, Google Fonts

## 📂 Project Structure
- `src/`: Core logic (Model, Data Loading, Training)
- `static/`: Frontend assets (Premium CSS, JS)
- `templates/`: HTML structures
- `models/`: Saved model weights
- `data/`: Satellite imagery dataset

## 🚦 Getting Started

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Train the Model**:
   ```bash
   python src/train.py
   ```

3. **Launch the Application**:
   ```bash
   python app.py
   ```
   *Then visit `http://localhost:5000` in your browser.*

## 🛰️ Categories
The system currently classifies four distinct terrain types:
- ☁️ **Cloudy**: High-altitude cloud cover assessment.
- 🏜️ **Desert**: Arid regions and sand dunes.
- 🌳 **Green Area**: Forestation and vegetation density.
- 🌊 **Water**: Ocean, lakes, and river systems.

---
Designed with ❤️ by Antigravity
