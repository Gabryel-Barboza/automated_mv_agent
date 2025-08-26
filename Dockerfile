FROM python:3.12.11-alpine

COPY backend /app

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app/src


CMD ["fastapi", "run", "main.py"]
