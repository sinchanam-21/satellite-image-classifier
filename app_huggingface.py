import os
import sys
import torch
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename

# Add src to path for Hugging Face environment
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from predict import Predictor

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Production model path
MODEL_PATH = "models/best_model.pth"
predictor = None

def get_predictor():
    global predictor
    if predictor is None:
        if os.path.exists(MODEL_PATH):
            predictor = Predictor(MODEL_PATH)
        else:
            print(f"Error: Model not found at {MODEL_PATH}")
            return None
    return predictor

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        p = get_predictor()
        if p is None:
            return jsonify({"error": "Model not found. Please ensure the model file is uploaded."}), 500
        
        try:
            result = p.predict(filepath)
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            if os.path.exists(filepath):
                os.remove(filepath)

if __name__ == '__main__':
    # Hugging Face Spaces usually uses port 7860
    app.run(host='0.0.0.0', port=7860)
