from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Topic(models.Model):
    """Topic model."""
    name = models.CharField(
        verbose_name='Тема',
        max_length=150,
        help_text='Укажите тему (категорию) слов',
        unique=True
    )

    class Meta:
        verbose_name = 'тема'
        verbose_name_plural = 'темы'

    def __str__(self):
        return self.name


class Word(models.Model):
    """Vocabulary model."""
    origin = models.CharField(
        verbose_name='Слово',
        max_length=30,
        help_text='Слово на иностранном языке'
    )
    translation = models.CharField(
        verbose_name='Перевод',
        max_length=30,
        help_text='Значение на родном языке'
    )
    topic = models.ForeignKey(
        Topic,
        verbose_name='Тема',
        on_delete=models.PROTECT,
        help_text='Выберите тематику слова',
        related_name='words'
    )

    class Meta:
        verbose_name = 'слово'
        verbose_name_plural = 'слова'
        ordering = ['origin']

    def __str__(self):
        return f'{self.origin} - {self.translation}'


class Task(models.Model):
    """Task model."""

    QUIZ = 'quiz'
    SPELLING = 'spelling'
    CATEGORY_CHOICES = [(QUIZ, 'Тест'),
                        (SPELLING, 'Правописание')]
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
    users = models.ManyToManyField(
        User,
        verbose_name='Ученики',
        help_text='Выбрать учеников, чтобы назначить им задачу',
        related_name='tasks',
        through='Result'
    )

    class Meta:
        verbose_name = 'задание'
        verbose_name_plural = 'задания'

    def __str__(self):
        return f'{self.get_category_display()} - {self.topic}'


class Result(models.Model):
    """Result model."""
    task = models.ForeignKey(
        Task,
        verbose_name='Задание',
        on_delete=models.CASCADE,
        related_name='results'
    )
    user = models.ForeignKey(
        User,
        verbose_name='Ученик',
        on_delete=models.CASCADE,
        related_name='results'
    )
    correct = models.PositiveSmallIntegerField(
        verbose_name='Верно',
        default=0,
    )
    incorrect = models.PositiveSmallIntegerField(
        verbose_name='Неверно',
        default=0,
    )
    passed = models.BooleanField(
        verbose_name='Пройдено',
        default=False,
    )

    class Meta:
        verbose_name = 'результат'
        verbose_name_plural = 'результаты'
        constraints = [
            models.UniqueConstraint(
                fields=['task', 'user'],
                name='Пользователю можно назначить только одно задание'
            )
        ]

    def __str__(self):
        return f'{self.task} {self.user}'

    def save(self, *args, **kwargs):
        """Update passed field."""
        if self.incorrect == 0 and self.correct > 0:
            self.passed = True
        super(Result, self).save(*args, **kwargs)
