FROM python:3.10.6-slim

WORKDIR /app

RUN apt-get update && apt-get install -y espeak ffmpeg

COPY requirements.txt .

RUN pip install -r requirements.txt --upgrade pip --no-cache-dir --root-user-action=ignore

COPY . .

CMD ["celery", "-A", "config", "worker", "-l", "INFO"]