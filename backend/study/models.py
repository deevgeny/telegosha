from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


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

    class Meta:
        verbose_name = 'слово'
        verbose_name_plural = 'слова'
        ordering = ['origin']

    def __str__(self):
        return f'{self.origin} - {self.translation}'


class Exercise(models.Model):
    """Exercise model."""

    QUIZ = 'quiz'
    SPELLING = 'spelling'
    CATEGORY_CHOICES = [(QUIZ, 'Тест'),
                        (SPELLING, 'Правописание')]
    category = models.CharField(
        verbose_name='Категория',
        max_length=8,
        help_text='Категория упражнения',
        choices=CATEGORY_CHOICES,
    )
    topic = models.CharField(
        verbose_name='Тема',
        max_length=150,
        help_text='Тема упражнения'
    )
    description = models.CharField(
        verbose_name='Описание',
        max_length=150,
        help_text='Описание задания, не более 150 символов.',
        blank=True
    )
    words = models.ManyToManyField(
        Word,
        verbose_name='Слова',
        help_text='Добавить слова',
        related_name='exercises',
    )
    users = models.ManyToManyField(
        User,
        verbose_name='Ученики',
        help_text='Выбрать учеников, чтобы назначить им упражнение',
        related_name='exercises',
        through='Task'
    )

    class Meta:
        verbose_name = 'упражнение'
        verbose_name_plural = 'упражнения'

    def __str__(self):
        return f'{self.get_category_display()} - {self.topic}'


class Task(models.Model):
    """Task model."""
    exercise = models.ForeignKey(
        Exercise,
        verbose_name='Упражнение',
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    user = models.ForeignKey(
        User,
        verbose_name='Ученик',
        on_delete=models.CASCADE,
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
    passed = models.BooleanField(
        verbose_name='Пройдено',
        default=False,
    )

    class Meta:
        verbose_name = 'задание'
        verbose_name_plural = 'задания'

    def __str__(self):
        return f'{self.exercise} {self.user}'

    def save(self, *args, **kwargs):
        """Update passed field."""
        if self.incorrect == 0 and self.correct > 0:
            self.passed = True
        super(Task, self).save(*args, **kwargs)
