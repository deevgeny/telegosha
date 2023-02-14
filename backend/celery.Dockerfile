FROM python:3.10.6-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --upgrade pip --no-cache-dir --root-user-action=ignore

COPY . .

CMD ["celery", "-A", "config", "worker", "-l", "INFO"]