import pytest
from django.contrib.auth import get_user_model
from django.db import models

from users.models import SchoolGroup

User = get_user_model()


@pytest.mark.parametrize('field_attr, value',
                         [['verbose_name', 'Учитель'],
                          ['on_delete', models.SET_NULL],
                          ['help_text', 'Учитель группы'],
                          ['_related_name', 'school_groups'],
                          ['_limit_choices_to', {'role': User.TEACHER}],
                          ['null', True], ['blank', True]])
def test_teacher_field(field_attr, value):
    field = 'teacher'
    if field_attr == 'on_delete':
        assert getattr(SchoolGroup._meta.get_field(field).remote_field,
                       field_attr) == value, (
            f'SchoolGroup.{field} field should be defined as '
            f'{field_attr}={repr(value)}'
        )
        return
    assert getattr(SchoolGroup._meta.get_field(field), field_attr) == value, (
        f'SchoolGroup.{field} field should be defined as '
        f'{field_attr}={repr(value)}'
    )


@pytest.mark.parametrize('field_attr, result',
                         [['verbose_name', 'Класс'],
                          ['help_text', 'Класс группы'],
                          ['max_length', 3]])
def test_grade_field(field_attr, result):
    field = 'grade'
    assert getattr(SchoolGroup._meta.get_field(field), field_attr) == result, (
        f'SchoolGroup.{field} field should be defined as '
        f'{field_attr}={repr(result)}'
    )


@pytest.mark.parametrize('field_attr, result',
                         [['verbose_name', 'Название'],
                          ['help_text', 'Название группы'],
                          ['max_length', 32]])
def test_name_field(field_attr, result):
    field = 'name'
    assert getattr(SchoolGroup._meta.get_field(field), field_attr) == result, (
        f'SchoolGroup.{field} field should be defined as '
        f'{field_attr}={repr(result)}'
    )


@pytest.mark.parametrize('class_attr, value',
                         [['verbose_name', 'Школьная группа'],
                          ['verbose_name_plural', 'Школьные группы']])
def test_model_meta_class(class_attr, value):
    assert getattr(SchoolGroup._meta, class_attr) == value, (
        'Task model Meta class should be defined as '
        f'{class_attr}={repr(value)}'
    )


def test_user_model_str_method(school_group):
    result = f'{school_group.grade} - {school_group.name}'
    assert str(school_group) == result, (
        'SchoolGroup model __str__() method output is incorrect'
    )
