# Deployment Guide: Hugging Face Spaces

To deploy **SatelliteEye** to Hugging Face, follow these simple steps:

### 1. Create a Space
- Go to [Hugging Face Spaces](https://huggingface.co/spaces).
- Click **Create new Space**.
- **Name**: `satellite-image-classifier` (or your choice).
- **SDK**: Select **Docker** (Best for custom Flask setups).
  - *Alternatively*, select **Static** if you only want the UI, but for AI features use **Docker** or **Streamlit**.
  - **For this Flux setup, we will use a Dockerfile.**

### 2. Prepare the Files
You need to upload these files to your Space:
- `requirements.txt`
- `app_huggingface.py` (rename it to `app.py` on HF or adjust Dockerfile)
- `src/` (the entire folder)
- `static/` (the entire folder)
- `templates/` (the entire folder)
- `models/best_model.pth`
- `Dockerfile` (see below)

### 3. Dockerfile
Create a file named `Dockerfile` in the root of your Hugging Face Space repository with this content:

```dockerfile
FROM python:3.10

# Set up user
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

# Copy requirements and install
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy project files
COPY --chown=user . .

# Run the app
CMD ["python", "app_huggingface.py"]
```

### 4. Push to Hugging Face
Use the Hugging Face web interface to upload these files or use Git:
```bash
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
git add .
git commit -m "Initial deployment"
git push hf main
```

### 5. Your App is Live!
Hugging Face will automatically build and deploy your app. You can share the public URL with others.
