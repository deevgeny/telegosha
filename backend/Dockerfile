FROM python:3.10.6-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir --upgrade pip --root-user-action=ignore

COPY . .

CMD ["gunicorn", "config.wsgi:application", "--bind", "0:8000" ]