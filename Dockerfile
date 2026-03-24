# Use Python 3.11 slim image as base
FROM python:3.11-slim

WORKDIR /app

# Install CJK fonts for Chinese/Japanese/Korean text rendering
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    fonts-noto-cjk \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY main.py .

# Create image cache directory with write permissions
RUN mkdir -p /app/generated_images && \
    chmod 777 /app/generated_images

# Expose API port
EXPOSE 3000

# Start FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]
