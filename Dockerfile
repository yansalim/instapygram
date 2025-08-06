# Use a slim Python image for reduced footprint
FROM python:3.11-slim

# Prevent Python from writing pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    TZ=America/Sao_Paulo

# Install system dependencies; ffmpeg is required for video uploads via instagrapi
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    ffmpeg \
    tzdata \
 && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements first to leverage Docker layer caching
COPY requirements.txt ./

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port on which the Flask app listens
EXPOSE 5000

# Default command: run under Gunicorn with multiple workers/threads
CMD ["gunicorn", "run:app", "--bind", "0.0.0.0:5000", "--workers", "2", "--threads", "4", "--timeout", "120"]