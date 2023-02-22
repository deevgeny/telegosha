from collections import Counter
from http import HTTPStatus

import pytest

from study.models import Task

TASK_URL = '/api/v1/tasks/'


def test_tasks_url_exists(api_client, user):
    url = f'{TASK_URL}{user.tg_id}/'
    response = api_client.get(url)
    assert response.status_code != HTTPStatus.NOT_FOUND, (
        f'URL {url} with user tasks not found'
    )


def test_empty_tasks_list(api_client, user):
    url = f'{TASK_URL}{user.tg_id}/'
    response = api_client.get(url)
    assert response.status_code == HTTPStatus.OK, (
        f'URL {url} should return HTTP 200'
    )
    assert response.json() == [], (
        f'URL {url} should return empty list for a user who has no tasks'
    )


def test_non_empty_tasks_response(api_client, intro_task):
    url = f'{TASK_URL}{intro_task.user.tg_id}/'
    response = api_client.get(url)
    assert response.status_code == HTTPStatus.OK, (
        f'URL {url} should return HTTP 200'
    )
    assert len(response.json()) == 1, (
        f'URL {url} should return tasks list for a user who has tasks'
    )


@pytest.mark.parametrize('field',
                         ['id', 'topic', 'category', 'data'])
def test_task_response_fields(api_client, intro_task, field):
    url = f'{TASK_URL}{intro_task.user.tg_id}/'
    response = api_client.get(url)
    assert response.status_code == HTTPStatus.OK, (
        f'URL {url} should return HTTP 200'
    )
    assert field in response.json()[0], (
        f'Field {field} is missing in response json data'
    )


@pytest.mark.parametrize('field, value',
                         [['category', 'intro'],
                          ['data', [['five', 'пять'], ['four', 'четыре'],
                                    ['one', 'один'], ['three', 'три'],
                                    ['two', 'два']]],
                          ['id', 1],
                          ['topic', 'topic']])
def test_intro_task_response_fields_values(api_client, intro_task, field,
                                           value):
    url = f'{TASK_URL}{intro_task.user.tg_id}/'
    response = api_client.get(url)
    assert response.status_code == HTTPStatus.OK, (
        f'URL {url} should return HTTP 200'
    )
    assert response.json()[0][field] == value, (
        f'Field {field} value is incorrect in response json data'
    )


@pytest.mark.parametrize('field, value',
                         [['category', 'learn'],
                          ['id', 1],
                          ['topic', 'topic']])
def test_learn_task_response_fields_values(api_client, learn_task, field,
                                           value):
    url = f'{TASK_URL}{learn_task.user.tg_id}/'
    response = api_client.get(url)
    assert response.status_code == HTTPStatus.OK, (
        f'URL {url} should return HTTP 200'
    )
    assert response.json()[0][field] == value, (
        f'Field {field} value is incorrect in response json data'
    )


def test_learn_task_buttons_response_data_field(api_client, learn_task):
    """Test for special data field with telegram buttons."""
    data_keys = ['buttons', 'word', 'origin']
    url = f'{TASK_URL}{learn_task.user.tg_id}/'
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


@pytest.mark.parametrize('field, value',
                         [['category', 'test'],
                          ['id', 1],
                          ['topic', 'topic']])
def test_test_task_response_fields_values(api_client, test_task, field, value):
    url = f'{TASK_URL}{test_task.user.tg_id}/'
    response = api_client.get(url)
    assert response.status_code == HTTPStatus.OK, (
        f'URL {url} should return HTTP 200'
    )
    assert response.json()[0][field] == value, (
        f'Field {field} value is incorrect in response json data'
    )


def test_test_task_buttons_response_data_field(api_client, test_task):
    """Test for special data field with telegram buttons."""
    data_keys = ['buttons', 'word', 'origin']
    url = f'{TASK_URL}{test_task.user.tg_id}/'
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


@pytest.mark.parametrize('field, value',
                         [['category', 'spell'],
                          ['id', 1],
                          ['topic', 'topic']])
def test_spell_task_response_fields_values(api_client, spell_task, field,
                                           value):
    url = f'{TASK_URL}{spell_task.user.tg_id}/'
    response = api_client.get(url)
    assert response.status_code == HTTPStatus.OK, (
        f'URL {url} should return HTTP 200'
    )
    assert response.json()[0][field] == value, (
        f'Field {field} value is incorrect in response json data'
    )


def test_spell_response_data_field(api_client, spell_task):
    """Test for special data field with telegram questions."""
    data_keys = ['word', 'spelling']
    url = f'{TASK_URL}{spell_task.user.tg_id}/'
    data = api_client.get(url).json()[0]['data']
    assert len(data) == 5, (
        'Incorrect number of items in data field'
    )
    for key in data_keys:
        assert key in data[0], (
            f'Missing key {key} in data item'
        )


def test_intro_task_update_with_incorrect_answers(api_client, intro_task):
    # Check database record before runnnig the test
    obj = intro_task
    assert obj.correct == 0, (
        'Incorrect newly created task with field `correct` not equal to 0'
    )
    assert obj.incorrect == 0, (
        'Incorrect newly created task with field `incorrect` not equal to 0'
    )
    assert obj.attempts == 0, (
        'Incorrect newly created task with field `attempts` not equal to 0'
    )
    assert not obj.passed, (
        'Incorrect newly created task with field `passed` not equal to False'
    )
    # Make patch request with data
    url = f'{TASK_URL}{intro_task.user.tg_id}/{intro_task.id}/'
    data = {'incorrect': 5, 'correct': 0}
    response = api_client.patch(url, data=data, format='json')
    # Run tests
    assert response.status_code == HTTPStatus.OK, (
        'Incorrect status code for successful task result update'
    )
    assert response.json() == data, (
        'Incorrect response json data for successful task result update'
    )
    task = Task.objects.get(id=obj.id)
    assert task.correct == data['correct'], (
        'Task result was not updated in database correctly with mistake '
        'in `correct` field'
    )
    assert task.incorrect == data['incorrect'], (
        'Task result was not updated in database correctly with mistake '
        'in `incorrect` field'
    )
    assert task.attempts == 1, (
        'Task result was not updated in database correctly with mistake '
        'in `attempts` field'
    )
    assert not task.passed, (
        'Task result was not updated in database correctly with mistake '
        'in `passed` field'
    )


def test_intro_task_update_with_correct_answers(api_client, intro_task):
    # Check database record before runnnig the test
    obj = intro_task
    assert obj.correct == 0, (
        'Incorrect newly created task with field `correct` not equal to 0'
    )
    assert obj.incorrect == 0, (
        'Incorrect newly created task with field `incorrect` not equal to 0'
    )
    assert obj.attempts == 0, (
        'Incorrect newly created task with field `attempts` not equal to 0'
    )
    assert not obj.passed, (
        'Incorrect newly created task with field `passed` not equal to False'
    )
    # Make patch request with data
    url = f'{TASK_URL}{intro_task.user.tg_id}/{intro_task.id}/'
    data = {'incorrect': 0, 'correct': 5}
    response = api_client.patch(url, data=data, format='json')
    # Run tests
    assert response.status_code == HTTPStatus.OK, (
        'Incorrect status code for successful task result update'
    )
    assert response.json() == data, (
        'Incorrect response json data for successful task result update'
    )
    task = Task.objects.get(id=obj.id)
    assert task.correct == data['correct'], (
        'Task result was not updated in database correctly with mistake '
        'in `correct` field'
    )
    assert task.incorrect == data['incorrect'], (
        'Task result was not updated in database correctly with mistake '
        'in `incorrect` field'
    )
    assert task.attempts == 1, (
        'Task result was not updated in database correctly with mistake '
        'in `attempts` field'
    )
    assert task.passed, (
        'Task result was not updated in database correctly with mistake '
        'in `passed` field'
    )
    assert Task.objects.filter(user=obj.user, category='learn').exists(), (
        'After successfully completing current task, next task was not '
        'created in database'
    )
