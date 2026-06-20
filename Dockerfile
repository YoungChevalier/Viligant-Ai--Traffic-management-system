# Use a slim Python 3.11 image to minimize attack surface and size
FROM python:3.11-slim as base

# Set environment variables for clean Python execution
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Install system dependencies (OpenCV requires libgl1 and libglib2.0)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install shared dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy shared libraries (Queue contracts, schemas, CV utils)
COPY libs /app/libs

# Define ARG to target a specific service
ARG SERVICE_NAME
ENV SERVICE_NAME=${SERVICE_NAME}

# Copy the specific service code
COPY services/${SERVICE_NAME} /app/services/${SERVICE_NAME}

# Expose standard FastAPI port
EXPOSE 8000

# Container Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/openapi.json || exit 1

# Startup command dynamically routes to the target service
CMD uvicorn services.${SERVICE_NAME}.app.main:app --host 0.0.0.0 --port 8000
