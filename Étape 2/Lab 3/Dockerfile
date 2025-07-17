# Dockerfile pour application FastAPI Lab 2
FROM python:3.11-slim


WORKDIR /app
# Installation des dépendances & copy requirements
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
# Commande pour run l'application 
CMD ["uvicorn", "production.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
