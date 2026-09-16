# ============================================
# Barfußschuh AI Agents - Production Dockerfile
# ============================================

# Basis-Image: Python 3.12 slim (minimal, sicher)
FROM python:3.12-slim

# Metadaten für das Image
LABEL maintainer="dein.name@example.com"
LABEL description="Multi-Agent E-Commerce System für Barfußschuhe"
LABEL version="1.0.0"

# Umgebungsvariablen für Python (verhindert .pyc Dateien und Buffering)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# System-Abhängigkeiten installieren (minimal halten)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

# Arbeitsverzeichnis setzen
WORKDIR /app

# ZUERST requirements.txt kopieren (Docker Cache Optimierung!)
# Das verhindert, dass bei jeder Code-Änderung alle Pakete neu installiert werden
COPY requirements.txt .

# Python-Abhängigkeiten installieren
RUN pip install --no-cache-dir -r requirements.txt

# Restlichen Code kopieren
COPY . .

# Nicht-Root User erstellen (Security Best Practice)
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser

# Streamlit Port freigeben
EXPOSE 8501

# Healthcheck (prüft, ob Streamlit läuft)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Startbefehl: Streamlit UI
CMD ["streamlit", "run", "src/ui/app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true", \
     "--server.enableCORS=false", \
     "--server.enableXsrfProtection=false"]
