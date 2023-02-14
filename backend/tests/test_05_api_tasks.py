from collections import Counter
from http import HTTPStatus

import pytest

TASK_URL = '/api/v1/tasks/'


def test_user_tasks_url_exists(api_client, user):
    url = f'{TASK_URL}{user.tg_id}/'
    response = api_client.get(url)
    assert response.status_code != HTTPStatus.NOT_FOUND, (
        f'URL {url} with user tasks not found'
    )


def test_user_empty_tasks_list(api_client, user):
    url = f'{TASK_URL}{user.tg_id}/'
    response = api_client.get(url)
    assert response.status_code == HTTPStatus.OK, (
        f'URL {url} should return HTTP 200'
    )
    assert response.json() == [], (
        f'URL {url} should return empty list for a user who has no tasks'
    )


def test_user_non_empty_tasks_response(api_client, user, task):
    url = f'{TASK_URL}{user.tg_id}/'
    response = api_client.get(url)
    assert response.status_code == HTTPStatus.OK, (
        f'URL {url} should return HTTP 200'
    )
    assert len(response.json()) == 1, (
        f'URL {url} should return tasks list for a user who has tasks'
    )


@pytest.mark.parametrize('field',
                         ['id', 'topic', 'category', 'data'])
def test_user_task_response_fields(api_client, user, task, field):
    url = f'{TASK_URL}{user.tg_id}/'
    response = api_client.get(url)
    assert response.status_code == HTTPStatus.OK, (
        f'URL {url} should return HTTP 200'
    )
    assert field in response.json()[0], (
        f'Field {field} is missing in response json data'
    )


@pytest.mark.parametrize('field, value',
                         [['category', 'quiz'],
                          ['data', []],
                          ['id', 1],
                          ['topic', 'topic']])
def test_user_task_response_fields_values(api_client, user, task, field,
                                          value):
    url = f'{TASK_URL}{user.tg_id}/'
    response = api_client.get(url)
    assert response.status_code == HTTPStatus.OK, (
        f'URL {url} should return HTTP 200'
    )
    assert response.json()[0][field] == value, (
        f'Field {field} value is incorrect in response json data'
    )


def test_user_task_response_data_field(api_client, user, task, words):
    """Test for special data field with telegram buttons."""
    data_keys = ['buttons', 'word']
    url = f'{TASK_URL}{user.tg_id}/'
    data = api_client.get(url).json()[0]['data']
    assert len(data) == 5, (
        'Incorrect number of items in data field'
    )
    for key in data_keys:
        assert key in data[0], (
            f'Missing key {key} in data item'
        )
    # Check buttons are unique
    for item in data:
        buttons = {}
        for button in item['buttons']:
            buttons.update(button)
            counter = Counter(list(buttons.values()))
        assert len(buttons) == 3, (
            'Response data should have 3 buttons'
        )
        assert len(set(list(buttons))) == 3, (
            'Buttons in data are not unique'
        )
        assert counter['correct'] == 1, (
            'Buttons should only have one correct answer'
        )
        assert counter['incorrect'] == 2, (
            'Buttons should have 2 incorrect answers'
        )
