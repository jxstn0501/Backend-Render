# Basis: kleines Python-Image
FROM python:3.12-slim

# Arbeitsverzeichnis im Container
WORKDIR /app

# System-Pakete (optional: falls Pillow, numpy etc. nötig wären)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Dependencies installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Projektcode kopieren
COPY . .

# Port für Fly.io
EXPOSE 8080

# Start Befehl (gunicorn für Production)
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]