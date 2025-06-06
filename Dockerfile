FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install pytest
CMD [ "python", "app/main.py" ]