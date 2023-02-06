import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


def test_user_model_str_method(user, user_no_name):
    assert str(user) == f'{user.first_name} {user.last_name}', (
        'User model __str__() method output is incorrect for user with non '
        'empty first_name and last_name fields'
    )
    assert str(user_no_name) == f'{user_no_name.username}', (
        'User model __str__() method output is incorrect for user with empty '
        'first_name and last_name fields'
    )


@pytest.mark.parametrize("field_name, result",
                         (["email", True], ["username", True]))
def test_fields_unique_attribute(field_name, result):
    assert User._meta.get_field(field_name).unique == result, (
        f"User.{field_name} field should be defined as `unique={result}`"
    )


@pytest.mark.parametrize('field_attr, result',
                         [['verbose_name', 'Телеграм id'], ['unique', True],
                          ['blank', True], ['null', True]])
def test_tg_id_field(field_attr, result):
    field = 'tg_id'
    assert getattr(User._meta.get_field(field), field_attr) == result, (
        f'User.{field} field should be defined as {field_attr}={repr(result)}'
    )


def test_user_model_login_field():
    username_field = 'username'
    assert User.USERNAME_FIELD == username_field, (
        'User.USERNAME_FIELD should be defined as '
        f'USERNAME_FIELD = {username_field}'
    )
