from itertools import zip_longest

import pytest
from django.db import models

from study.models import Task


@pytest.mark.parametrize('_class, constant',
                         zip_longest([], ['INTRO', 'LEARN', 'TEST', 'SPELL'],
                                     fillvalue=Task))
def test_model_constants(_class, constant):
    assert hasattr(_class, constant), f'Missing {_class}.{constant} constant'


@pytest.mark.parametrize(
    'constant, value',
    [[Task.INTRO, 'intro'], [Task.LEARN, 'learn'], [Task.TEST, 'test'],
     [Task.SPELL, 'spell'],
     [Task.CATEGORY_CHOICES, [(Task.INTRO, 'Знакомство'),
                              (Task.LEARN, 'Запоминание'),
                              (Task.TEST, 'Тест'),
                              (Task.SPELL, 'Правописание')]]]
)
def test_model_constants_values(constant, value):
    assert constant == value, f'Incorrect {constant} value'


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
                          ['choices', [(Task.INTRO, 'Знакомство'),
                                       (Task.LEARN, 'Запоминание'),
                                       (Task.TEST, 'Тест'),
                                       (Task.SPELL, 'Правописание')]]])
def test_category_field(field_attr, value):
    field = 'category'
    assert getattr(Task._meta.get_field(field), field_attr) == value, (
        f'Task.{field} field should be defined as {field_attr}={repr(value)}'
    )


@pytest.mark.parametrize('field_attr, value',
                         [['verbose_name', 'Ученик'],
                          ['on_delete', models.CASCADE],
                          ['help_text',
                           'Выбрать ученика, чтобы назначить ему задание'],
                          ['_related_name', 'tasks']])
def test_user_field(field_attr, value):
    field = 'user'
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
                         [['verbose_name', 'Верно'],
                          ['default', 0]])
def test_correct_field(field_attr, value):
    field = 'correct'
    assert getattr(Task._meta.get_field(field), field_attr) == value, (
        f'Task.{field} field should be defined as {field_attr}={repr(value)}'
    )


@pytest.mark.parametrize('field_attr, value',
                         [['verbose_name', 'Неверно'],
                          ['default', 0]])
def test_incorrect_field(field_attr, value):
    field = 'incorrect'
    assert getattr(Task._meta.get_field(field), field_attr) == value, (
        f'Task.{field} field should be defined as {field_attr}={repr(value)}'
    )


@pytest.mark.parametrize('field_attr, value',
                         [['verbose_name', 'Попытки'],
                          ['default', 0]])
def test_attempts_field(field_attr, value):
    field = 'attempts'
    assert getattr(Task._meta.get_field(field), field_attr) == value, (
        f'Task.{field} field should be defined as {field_attr}={repr(value)}'
    )


@pytest.mark.parametrize('field_attr, value',
                         [['verbose_name', 'Активное'],
                          ['default', True]])
def test_active_field(field_attr, value):
    field = 'active'
    assert getattr(Task._meta.get_field(field), field_attr) == value, (
        f'Task.{field} field should be defined as {field_attr}={repr(value)}'
    )


@pytest.mark.parametrize('field_attr, value',
                         [['verbose_name', 'Пройдено'],
                          ['default', False]])
def test_passed_field(field_attr, value):
    field = 'passed'
    assert getattr(Task._meta.get_field(field), field_attr) == value, (
        f'Task.{field} field should be defined as {field_attr}={repr(value)}'
    )


@pytest.mark.parametrize('class_attr, value',
                         [['verbose_name', 'задание'],
                          ['verbose_name_plural', 'задания'],
                          ['ordering', ['topic__id', 'id']]])
def test_model_meta_class(class_attr, value):
    assert getattr(Task._meta, class_attr) == value, (
        'Task model Meta class should be defined as '
        f'{class_attr}={repr(value)}'
    )


def test_model_meta_class_constraints():
    n_of_constraints = 1
    fields = ('topic', 'category', 'user')
    name = 'Такое задание у пользователя уже существует'
    assert len(Task._meta.constraints) == n_of_constraints, (
        f'Task model should have {n_of_constraints} constraint(s) in Meta '
        'class'
    )
    assert isinstance(Task._meta.constraints[0], models.UniqueConstraint), (
        'Incorrect constraint type in Task model Meta class'
    )
    assert Task._meta.constraints[0].fields == fields, (
        'Incorrect fields in Meta class constraint'
    )
    assert Task._meta.constraints[0].name == name, (
        'Incorrect error message in Meta class constraint'
    )


# Celery
def test_model_str_method(intro_task):
    obj = intro_task
    assert str(obj) == f'{obj.get_category_display()} - {obj.topic}', (
        'Task __str__() method should return `self.get_category_display() - '
        'self.topic`'
    )


def test_model_save_method_for_passed_and_active_fields(intro_task):
    obj = intro_task
    assert not obj.passed, ('Newly created task should have passed=False')
    assert obj.active, ('Newly created task should have active=True')
    obj.correct = 10
    obj.save()
    assert obj.passed, (
        'Task with correct > 0 and incorrect == 0 should set passed = True '
        'when models save() method is called.'
    )
    assert not obj.active, (
        'Task with correct > 0 and incorrect == 0 should set active = False '
        'when models save() method is called.'
    )


def test_model_save_method_for_attempts_field(intro_task):
    obj = intro_task
    assert obj.attempts == 0, ('Newly created task should have attempts=0')
    obj.incorrect = 1
    obj.save()
    assert obj.attempts == 1, (
        'Task with incorrect > 0 should increase attempts field by 1 '
        'every time when models save() method is called.'
    )
    obj.incorrect = 1
    obj.correct = 1
    obj.save()
    assert obj.attempts == 2, (
        'Task with correct > 0 should increase attempts field by 1 '
        'every time when models save() method is called.'
    )
