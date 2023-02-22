import logging
import os

from django.contrib.auth import get_user_model
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from kombu.exceptions import OperationalError

from .models import Task, Topic
from .tasks import send_telegram_message

User = get_user_model()

TASK_SEQUENCE = {
    Task.INTRO: Task.LEARN,
    Task.LEARN: Task.TEST,
    Task.TEST: Task.SPELL,
    Task.SPELL: Task.INTRO
}

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
logger.addHandler(handler)


@receiver(post_save, sender=Task)
def send_messages(sender, instance, created, **kwargs):
    tg_id = instance.user.tg_id
    if created and tg_id:
        message = ('Привет!\n\nПоявилось новое задание: '
                   f'{instance.get_category_display().lower()} '
                   f'на тему {instance.topic.name.lower()}.\n'
                   'Найти его можно в меню > задания или с помощью команды '
                   '/tasks.')
        try:
            send_telegram_message.delay(tg_id, os.environ.get('TG_API_TOKEN'),
                                        message)
        except OperationalError as exc:
            logger.error('Sending task raised: %r' % exc)


@receiver(post_save, sender=Task)
def create_next_task(sender, instance, **kwargs):
    """Create next task when user completed current one."""
    if not instance.active and instance.passed:
        Task.objects.get_or_create(topic=instance.topic,
                                   user=instance.user,
                                   category=TASK_SEQUENCE[instance.category])


@receiver(m2m_changed, sender=Topic.school_groups.through)
def create_topic_tasks(sender, instance, action, pk_set, **kwargs):
    """Create first tasks for new topic.

    Create first topic task for every school_group user when new
    topic is created or group is added to Topic.school_groups.
    """
    if action == 'post_add':
        users = User.objects.filter(school_group__id__in=pk_set)
        tasks = [Task(topic=instance,
                      user=user,
                      category=Task.INTRO) for user in users]
        Task.objects.bulk_create(tasks, ignore_conflicts=True)
        message = ('Привет!\n\nПоявилась новая тема для изучения: '
                   f'{instance.name.lower()}.\nЗадания можно найти в '
                   'меню > задания или с помощью команды /tasks.')
        args = [(user.tg_id,
                 os.environ.get('TG_API_TOKEN'),
                 message) for user in users]
        try:
            logger.info(args)
            send_telegram_message.starmap(args).delay()
        except OperationalError as exc:
            logger.error('Sending task raised: %r' % exc)
