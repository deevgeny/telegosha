import os

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Result
from .tasks import send_telegram_message


@receiver(post_save, sender=Result)
def send_messages(sender, instance, created, **kwargs):
    tg_id = instance.user.tg_id
    if created and tg_id:
        message = ('Привет!\n\nПоявилось новое задание: '
                   f'{instance.task.get_category_display().lower()} '
                   f'на тему {instance.task.topic.name.lower()}.\n'
                   'Найти его можно в меню > задания или с помощью команды '
                   '/tasks.')
        send_telegram_message.delay(tg_id, os.environ.get('TG_API_TOKEN'),
                                    message)
