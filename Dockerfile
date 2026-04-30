FROM python:3.11-slim

WORKDIR /app

# Install minimal dependencies
RUN pip install flask gunicorn requests

COPY . .

# Environment variables
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 3600 worker:app