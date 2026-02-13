FROM python:3.10

# Set up user for security
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

# Install dependencies
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of the application
COPY --chown=user . .

# Expose port (HF Spaces defaults to 7860)
EXPOSE 7860

# Launch the app
CMD ["python", "app_huggingface.py"]
