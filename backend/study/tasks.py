import pyttsx3
import requests
from celery import chain, shared_task

from .models import Word


@shared_task
def send_telegram_message(tg_id, tg_api_token, message):
    url = (f'https://api.telegram.org/bot{tg_api_token}/'
           f'sendMessage?chat_id={tg_id}&text={message}')
    requests.get(url)


@shared_task
def generate_sound_file(word, abs_path):
    engine = pyttsx3.init()
    engine.setProperty('voice', 'english')
    engine.setProperty('rate', 120)
    engine.save_to_file(word, abs_path)
    engine.runAndWait()


@shared_task
def add_sound_file_to_database(_, id, rel_path):
    obj = Word.objects.get(id=id)
    obj.sound = rel_path
    obj.save()


def generate_sound_chain(word, abs_path, id, rel_path):
    chain(generate_sound_file.s(word, abs_path),
          add_sound_file_to_database.s(id, rel_path))()
