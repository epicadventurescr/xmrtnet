FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (if any needed for pyscopg2 or others)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

COPY . .

# Environment variables
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

# Run with Gunicorn matches src.main:app
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 src.main:app
