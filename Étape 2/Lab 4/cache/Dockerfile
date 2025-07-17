FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main_avec_metriques.py .
COPY cache_manager.py .
COPY prototype ./prototype

ENV PYTHONPATH=/app

CMD ["python", "main_avec_metriques.py"]