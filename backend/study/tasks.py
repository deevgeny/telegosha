import requests
from celery import shared_task


@shared_task
def send_telegram_message(tg_id, tg_api_token, message):
    url = (f'https://api.telegram.org/bot{tg_api_token}/'
           f'sendMessage?chat_id={tg_id}&text={message}')
    requests.get(url)
