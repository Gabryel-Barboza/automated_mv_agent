FROM python:3.12.11-alpine

COPY client /app

WORKDIR /app

CMD ["python", "-u", "src/main.py"]