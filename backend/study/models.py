from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

from users.models import SchoolGroup

User = get_user_model()


class Word(models.Model):
    """Word model."""
    origin = models.CharField(
        verbose_name='Слово',
        max_length=32,
        help_text='Слово на иностранном языке'
    )
    translation = models.CharField(
        verbose_name='Перевод',
        max_length=32,
        help_text='Значение на родном языке'
    )
    sound = models.FileField(
        verbose_name='Голос',
        help_text=('Файл добавлять не надо '
                   '(он будет сгенерирован автоматически)'),
        upload_to=settings.SOUND_PATH,
        blank=True,
    )

    class Meta:
        verbose_name = 'слово'
        verbose_name_plural = 'слова'
        ordering = ['origin']

    def __str__(self):
        return f'{self.origin} - {self.translation}'


class Topic(models.Model):
    """Topic model."""
    name = models.CharField(
        verbose_name='Название',
        max_length=32,
        help_text='Укажите тему (категорию) слов',
        unique=True
    )
    description = models.CharField(
        verbose_name='Описание',
        max_length=128,
        help_text='Краткое описание темы',
        blank=True
    )
    school_groups = models.ManyToManyField(
        SchoolGroup,
        related_name='topics',
        verbose_name='Группы',
        help_text='Выбрать группы'
    )
    words = models.ManyToManyField(
        Word,
        related_name='topics',
        verbose_name='Слова',
        help_text='Выбрать минимум три слова'
    )

    class Meta:
        verbose_name = 'тема'
        verbose_name_plural = 'темы'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'description'],
                name='Тема с таким названием и описанием уже существует'
            )
        ]

    def __str__(self):
        return self.name


class Task(models.Model):
    """Task model."""

    INTRO = 'intro'
    LEARN = 'learn'
    TEST = 'test'
    SPELL = 'spell'
    CATEGORY_CHOICES = [(INTRO, 'Знакомство'),
                        (LEARN, 'Запоминание'),
                        (TEST, 'Тест'),
                        (SPELL, 'Правописание')]
    topic = models.ForeignKey(
        Topic,
        verbose_name='Тема',
        on_delete=models.PROTECT,
        help_text='Выберите тему задачи',
        related_name='tasks'
    )
    category = models.CharField(
        verbose_name='Категория',
        max_length=8,
        help_text='Категория задания',
        choices=CATEGORY_CHOICES,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Ученик',
        help_text='Выбрать ученика, чтобы назначить ему задание',
        related_name='tasks'
    )
    correct = models.PositiveSmallIntegerField(
        verbose_name='Верно',
        default=0,
    )
    incorrect = models.PositiveSmallIntegerField(
        verbose_name='Неверно',
        default=0,
    )
    attempts = models.PositiveSmallIntegerField(
        verbose_name='Попытки',
        default=0,
    )
    active = models.BooleanField(
        verbose_name='Активное',
        default=True,
    )
    passed = models.BooleanField(
        verbose_name='Пройдено',
        default=False,
    )

    class Meta:
        verbose_name = 'задание'
        verbose_name_plural = 'задания'
        ordering = ['topic__id', 'id']
        constraints = [
            models.UniqueConstraint(
                fields=['topic', 'category', 'user'],
                name='Такое задание у пользователя уже существует'
            ),
        ]

    def __str__(self):
        return f'{self.get_category_display()} - {self.topic}'

    def save(self, *args, **kwargs):
        """Update attempts, passed and active fields."""
        if self.id and (self.correct or self.incorrect):
            self.attempts += 1
        if self.incorrect == 0 and self.correct > 0:
            self.passed = True
            self.active = False
        super(Task, self).save(*args, **kwargs)
