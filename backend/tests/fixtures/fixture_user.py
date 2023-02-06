import pytest


@pytest.fixture
def user_no_name(django_user_model):
    return django_user_model.objects.create(
        username='user_no_name', email='user_no_name@fake.com', tg_id=1234
    )


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create(
        username='user', email='user@fake.com', first_name='Firstname',
        last_name='Lastname', tg_id=12345
    )


@pytest.fixture
def user_1(django_user_model):
    return django_user_model.objects.create(
        username='user1', email='user1@fake.com', first_name='Firstname',
        last_name='Lastname', tg_id=123456
    )


@pytest.fixture
def user_client(user, client):
    client.force_login(user)
    return client


@pytest.fixture
def user_1_client(user_1, client):
    client.force_login(user_1)
    return client
