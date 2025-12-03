# Official lightweight Python 3.12 image
FROM python:3.12-slim AS base

# Prevent stdout/stderr buffering
ENV PYTHONBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PIP_NO_CACHE_DIR=1

# Set working directory
WORKDIR /app

# Install dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt
COPY requirements.txt .

# Install Python dependenncies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy app code and any data
COPY . .

# Make intrypoint executable
RUN chmod +x /app/entrypoint.sh

# Expose FastAPI port
EXPOSE 8000

# Start via entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]