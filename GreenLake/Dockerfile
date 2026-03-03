# GreenLake Flask app for Fly.io
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Fly.io expects the app to listen on PORT (default 8080)
ENV PORT=8080
EXPOSE 8080

CMD ["gunicorn", "-c", "gunicorn.conf.py", "-b", "0.0.0.0:8080", "main:app"]
