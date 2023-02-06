import pytest
from django.db import models

from study.models import Result


@pytest.mark.parametrize('class_attr, value',
                         [['verbose_name', 'результат'],
                          ['verbose_name_plural', 'результаты']])
def test_model_meta_class(class_attr, value):
    assert getattr(Result._meta, class_attr) == value, (
        'Result model Meta class should be defined as '
        f'{class_attr}={repr(value)}'
    )


def test_model_meta_class_constraints():
    n_of_constraints = 1
    fields = ('task', 'user')
    name = 'Пользователю можно назначить только одно задание'
    assert len(Result._meta.constraints) == n_of_constraints, (
        f'Result model should have {n_of_constraints} constraint(s) in Meta '
        'class'
    )
    assert isinstance(Result._meta.constraints[0], models.UniqueConstraint), (
        'Incorrect constraint in Result model Meta class'
    )
    assert Result._meta.constraints[0].fields == fields, (
        'Incorrect fields in Meta class constraints'
    )
    assert Result._meta.constraints[0].name == name, (
        'Incorrect error message in Meta class constraint'
    )


def test_model_str_method(task, user):
    # Result is through model for task with 'user task' unique constraints
    # Created automatically when create task and assign it to user
    result = Result.objects.get(user=user)
    assert str(result) == f'{result.task} {result.user}', (
        'Result __str__() method should return `self.task self.user`'
    )


def test_model_save_method(task, user):
    result = Result.objects.get(user=user)
    assert not result.passed, ('Newly created result should have passed=False')
    result.correct = 10
    result.save()
    assert result.passed, (
        'Result with correct > 0 and incorrect == 0 should set passed = True '
        'when models save() method is called.'
    )


@pytest.mark.parametrize('field_attr, value',
                         [['verbose_name', 'Задание'],
                          ['on_delete', models.CASCADE],
                          ['_related_name', 'results']])
def test_task_field(field_attr, value):
    field = 'task'
    if field_attr == 'on_delete':
        assert getattr(
            Result._meta.get_field(field).remote_field, field_attr) == value, (
                f'Result.{field} field should be defined as '
                f'{field_attr}={repr(value)}'
        )
        return
    assert getattr(Result._meta.get_field(field), field_attr) == value, (
        f'Result.{field} field should be defined as {field_attr}={repr(value)}'
    )


@pytest.mark.parametrize('field_attr, value',
                         [['verbose_name', 'Ученик'],
                          ['on_delete', models.CASCADE],
                          ['_related_name', 'results']])
def test_user_field(field_attr, value):
    field = 'user'
    if field_attr == 'on_delete':
        assert (getattr(Result._meta.get_field(field).remote_field, field_attr)
                == value), (f'Result.{field} field should be defined as '
                            f'{field_attr}={repr(value)}')
        return
    assert getattr(Result._meta.get_field(field), field_attr) == value, (
        f'Result.{field} field should be defined as {field_attr}={repr(value)}'
    )


@pytest.mark.parametrize('field_attr, value',
                         [['verbose_name', 'Верно'],
                          ['default', 0]])
def test_correct_field(field_attr, value):
    field = 'correct'
    assert getattr(Result._meta.get_field(field), field_attr) == value, (
        f'Result.{field} field should be defined as {field_attr}={repr(value)}'
    )


@pytest.mark.parametrize('field_attr, value',
                         [['verbose_name', 'Неверно'],
                          ['default', 0]])
def test_incorrect_field(field_attr, value):
    field = 'incorrect'
    assert getattr(Result._meta.get_field(field), field_attr) == value, (
        f'Result.{field} field should be defined as {field_attr}={repr(value)}'
    )


@pytest.mark.parametrize('field_attr, value',
                         [['verbose_name', 'Пройдено'],
                          ['default', False]])
def test_passed_field(field_attr, value):
    field = 'passed'
    assert getattr(Result._meta.get_field(field), field_attr) == value, (
        f'Result.{field} field should be defined as {field_attr}={repr(value)}'
    )
