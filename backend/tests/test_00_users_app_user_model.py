from itertools import zip_longest

import pytest
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


@pytest.mark.parametrize('_class, constant',
                         zip_longest([], ['TEACHER', 'PUPIL', 'ROLE_CHOICES'],
                                     fillvalue=User))
def test_model_constants(_class, constant):
    assert hasattr(_class, constant), f'Missing {_class}.{constant} constant'


@pytest.mark.parametrize('constant, value',
                         [[User.TEACHER, 'teacher'],
                          [User.PUPIL, 'pupil'],
                          [User.ROLE_CHOICES, [(User.TEACHER, 'Учитель'),
                                               (User.PUPIL, 'Ученик')]]])
def test_model_constants_values(constant, value):
    assert constant == value, f'Incorrect {constant} value'


def test_user_model_str_method(user, user_no_name):
    assert str(user) == f'{user.first_name} {user.last_name}', (
        'User model __str__() method output is incorrect for user with non '
        'empty first_name and last_name fields'
    )
    assert str(user_no_name) == f'{user_no_name.username}', (
        'User model __str__() method output is incorrect for user with empty '
        'first_name and last_name fields'
    )


@pytest.mark.parametrize('field_name, result',
                         [["username", True]])
def test_builin_fields_unique_attribute(field_name, result):
    assert User._meta.get_field(field_name).unique == result, (
        f"User.{field_name} field should be defined as `unique={result}`"
    )


def test_email_field():
    assert User._meta.get_field('email').blank, (
        'User.email field should be defined as `blank=True`'
    )


@pytest.mark.parametrize('field_attr, result',
                         [['verbose_name', 'Телеграм id'], ['unique', True],
                          ['blank', True], ['null', True]])
def test_tg_id_field(field_attr, result):
    field = 'tg_id'
    assert getattr(User._meta.get_field(field), field_attr) == result, (
        f'User.{field} field should be defined as {field_attr}={repr(result)}'
    )


@pytest.mark.parametrize('field_attr, value',
                         [['verbose_name', 'Роль'],
                          ['max_length', 7],
                          ['help_text', 'Выберите роль'],
                          ['blank', True],
                          ['default', ''],
                          ['choices', [(User.TEACHER, 'Учитель'),
                                       (User.PUPIL, 'Ученик')]]])
def test_role_field(field_attr, value):
    field = 'role'
    assert getattr(User._meta.get_field(field), field_attr) == value, (
        f'User.{field} field should be defined as {field_attr}={repr(value)}'
    )


@pytest.mark.parametrize('field_attr, value',
                         [['verbose_name', 'Школьная группа'],
                          ['on_delete', models.SET_NULL],
                          ['help_text', 'Выберите школьную группу'],
                          ['_related_name', 'users'],
                          ['null', True], ['blank', True]])
def test_school_group_field(field_attr, value):
    field = 'school_group'
    if field_attr == 'on_delete':
        assert getattr(
            User._meta.get_field(field).remote_field, field_attr) == value, (
                f'User.{field} field should be defined as '
                f'{field_attr}={repr(value)}'
        )
        return
    assert getattr(User._meta.get_field(field), field_attr) == value, (
        f'User.{field} field should be defined as {field_attr}={repr(value)}'
    )


def test_user_model_login_field():
    username_field = 'username'
    assert User.USERNAME_FIELD == username_field, (
        'User.USERNAME_FIELD should be defined as '
        f'USERNAME_FIELD = {username_field}'
    )
