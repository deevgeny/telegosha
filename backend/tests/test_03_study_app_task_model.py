from itertools import zip_longest

import pytest
from django.db import models

from study.models import Result, Task


@pytest.mark.parametrize('_class, constant',
                         zip_longest([], ['QUIZ', 'SPELLING'], fillvalue=Task))
def test_model_constants(_class, constant):
    assert hasattr(_class, constant), f'Missing {_class}.{constant} constant'


@pytest.mark.parametrize('constant, value',
                         [[Task.QUIZ, 'quiz'],
                          [Task.SPELLING, 'spelling']])
def test_model_constants_values(constant, value):
    assert constant == value, f'Incorrect {constant} value'


@pytest.mark.parametrize('class_attr, value',
                         [['verbose_name', 'задание'],
                          ['verbose_name_plural', 'задания']])
def test_model_meta_class(class_attr, value):
    assert getattr(Task._meta, class_attr) == value, (
        'Task model Meta class should be defined as '
        f'{class_attr}={repr(value)}'
    )


def test_model_str_method(task):
    assert str(task) == f'{task.get_category_display()} - {task.topic}', (
        'Task __str__() method should return `self.get_category_display() - '
        'self.topic`'
    )


@pytest.mark.parametrize('field_attr, value',
                         [['verbose_name', 'Тема'],
                          ['on_delete', models.PROTECT],
                          ['help_text', 'Выберите тему задачи'],
                          ['_related_name', 'tasks']])
def test_topic_field(field_attr, value):
    field = 'topic'
    if field_attr == 'on_delete':
        assert getattr(
            Task._meta.get_field(field).remote_field, field_attr) == value, (
                f'Task.{field} field should be defined as '
                f'{field_attr}={repr(value)}'
        )
        return
    assert getattr(Task._meta.get_field(field), field_attr) == value, (
        f'Task.{field} field should be defined as {field_attr}={repr(value)}'
    )


@pytest.mark.parametrize('field_attr, value',
                         [['verbose_name', 'Категория'],
                          ['max_length', 8],
                          ['help_text', 'Категория задания'],
                          ['choices', [(Task.QUIZ, 'Тест'),
                                       (Task.SPELLING, 'Правописание')]]])
def test_category_field(field_attr, value):
    field = 'category'
    assert getattr(Task._meta.get_field(field), field_attr) == value, (
        f'Task.{field} field should be defined as {field_attr}={repr(value)}'
    )


@pytest.mark.parametrize('field_attr, value',
                         [['verbose_name', 'Ученики'],
                          ['help_text',
                           'Выбрать учеников, чтобы назначить им задачу'],
                          ['_related_name', 'tasks'],
                          ['through', Result]])
def test_users_field(field_attr, value):
    field = 'users'
    if field_attr == 'through':
        assert (getattr(Task._meta.get_field(field).remote_field, field_attr)
                == value), (f'Task.{field} field should be defined as '
                            f'{field_attr}={repr(value)}')
        return
    assert getattr(Task._meta.get_field(field), field_attr) == value, (
        f'Task.{field} field should be defined as {field_attr}={repr(value)}'
    )
