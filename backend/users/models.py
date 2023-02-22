from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Custom user model."""

    TEACHER = 'teacher'
    PUPIL = 'pupil'
    ROLE_CHOICES = [(TEACHER, 'Учитель'),
                    (PUPIL, 'Ученик')]

    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    email = models.EmailField(_("email address"), unique=True, blank=True,
                              null=True)
    tg_id = models.PositiveBigIntegerField(
        verbose_name='Телеграм id',
        unique=True,
        blank=True,
        null=True
    )
    role = models.CharField(
        max_length=7,
        verbose_name='Роль',
        help_text='Выберите роль',
        blank=True,
        default='',
        choices=ROLE_CHOICES
    )
    school_group = models.ForeignKey(
        'SchoolGroup',
        on_delete=models.SET_NULL,
        related_name='users',
        verbose_name='Школьная группа',
        help_text='Выберите школьную группу',
        null=True,
        blank=True
    )

    def __str__(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        return f'{self.username}'


class SchoolGroup(models.Model):
    """School group model."""
    teacher = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        related_name='school_groups',
        verbose_name='Учитель',
        help_text='Учитель группы',
        null=True,
        blank=True,
        limit_choices_to={'role': User.TEACHER}
    )
    grade = models.CharField(
        max_length=3,
        verbose_name='Класс',
        help_text='Класс группы'
    )
    name = models.CharField(
        max_length=32,
        verbose_name='Название',
        help_text='Название группы'
    )

    class Meta:
        verbose_name = 'Школьная группа'
        verbose_name_plural = 'Школьные группы'

    def __str__(self):
        return f'{self.grade} - {self.name}'
