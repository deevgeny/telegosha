from http import HTTPStatus

import pytest

from study.models import Result

RESULT_URL = '/api/v1/results/'


def test_user_results_url_exists(api_client, user):
    url = f'{RESULT_URL}{user.tg_id}/'
    response = api_client.get(url)
    assert response.status_code != HTTPStatus.NOT_FOUND, (
        f'URL {url} with user results not found'
    )


def test_user_empty_results_list(api_client, user):
    url = f'{RESULT_URL}{user.tg_id}/'
    response = api_client.get(url)
    assert response.status_code == HTTPStatus.OK, (
        f'URL {url} should return HTTP 200'
    )
    assert response.json() == [], (
        f'URL {url} should return empty list for a user who have no results'
    )


def test_user_non_empty_results_response(api_client, user, task):
    url = f'{RESULT_URL}{user.tg_id}/'
    response = api_client.get(url)
    assert response.status_code == HTTPStatus.OK, (
        f'URL {url} should return HTTP 200'
    )
    assert len(response.json()) == 1, (
        f'URL {url} should return results list for a user who has results'
    )


def test_user_empty_results_response(api_client, user):
    url = f'{RESULT_URL}{user.tg_id}/'
    response = api_client.get(url)
    assert response.status_code == HTTPStatus.OK, (
        f'URL {url} should return HTTP 200'
    )
    assert len(response.json()) == 0, (
        f'URL {url} should return empty list for a user who has no results'
    )


def test_other_user_empty_results_response(api_client, user, user_1, task):
    url = f'{RESULT_URL}{user_1.tg_id}/'
    response = api_client.get(url)
    assert response.status_code == HTTPStatus.OK, (
        f'URL {url} should return HTTP 200'
    )
    assert len(response.json()) == 0, (
        f'URL {url} should return empty list for a user who has no results'
    )


@pytest.mark.parametrize('field',
                         ['topic', 'category', 'passed'])
def test_user_result_response_fields(api_client, user, task, field):
    url = f'{RESULT_URL}{user.tg_id}/'
    response = api_client.get(url)
    assert response.status_code == HTTPStatus.OK, (
        f'URL {url} should return HTTP 200'
    )
    assert field in response.json()[0], (
        f'Field {field} is missing in response json data'
    )


@pytest.mark.parametrize('field, value',
                         [['topic', 'topic'],
                          ['category', 'Тест'],
                          ['passed', False]])
def test_user_result_response_fields_values(api_client, user, task, field,
                                            value):
    url = f'{RESULT_URL}{user.tg_id}/'
    response = api_client.get(url)
    assert response.status_code == HTTPStatus.OK, (
        f'URL {url} should return HTTP 200'
    )
    assert response.json()[0][field] == value, (
        f'Field {field} value is incorrect in response json data'
    )


@pytest.mark.django_db
def test_user_successful_result_update(api_client, user, task, words):
    # Check database record before runnnig the test
    result = Result.objects.get(user=user, task=task)
    assert result.correct == 0, (
        'Incorrect database result record before running the test with field '
        '`correct` not equal to 0'
    )
    assert result.incorrect == 0, (
        'Incorrect database result record before running the test with field '
        '`incorrect` not equal to 0'
    )
    assert not result.passed, (
        'Incorrect database result record before running the test with field '
        '`passed` not equal to False'
    )
    # Make patch request with data
    url = f'{RESULT_URL}{user.tg_id}/{task.id}/'
    data = {'incorrect': 0, 'correct': 5}
    response = api_client.patch(url, data=data, format='json')
    # Run tests
    assert response.status_code == HTTPStatus.OK, (
        'Incorrect status code for successful user result update'
    )
    assert response.json() == data, (
        'Incorrect response json data for successful user result update'
    )
    result = Result.objects.get(user=user, task=task)
    assert result.correct == data['correct'], (
        'User task result was not updated in database correctly with mistake '
        'in `correct` field'
    )
    assert result.incorrect == data['incorrect'], (
        'User task result was not updated in database correctly with mistake '
        'in `incorrect` field'
    )
    assert result.passed, (
        'User task result was not updated in database correctly with mistake '
        'in `passed` field'
    )


@pytest.mark.django_db
def test_user_unsuccessful_result_update(api_client, user, task, words):
    # Check database record before runnnig the test
    result = Result.objects.get(user=user, task=task)
    assert result.correct == 0, (
        'Incorrect database result record before running the test with field '
        '`correct` not equal to 0'
    )
    assert result.incorrect == 0, (
        'Incorrect database result record before running the test with field '
        '`incorrect` not equal to 0'
    )
    assert not result.passed, (
        'Incorrect database result record before running the test with field '
        '`passed` not equal to False'
    )
    # Make patch request with data
    url = f'{RESULT_URL}{user.tg_id}/{task.id}/'
    data = {'incorrect': 1, 'correct': 4}
    response = api_client.patch(url, data=data, format='json')
    # Run tests
    assert response.status_code == HTTPStatus.OK, (
        'Incorrect status code for successuf user result update'
    )
    assert response.json() == data, (
        'Incorrect response json data for successful user result update'
    )
    result = Result.objects.get(user=user, task=task)
    assert result.correct == data['correct'], (
        'User task result was not updated in database correctly with mistake '
        'in `correct` field'
    )
    assert result.incorrect == data['incorrect'], (
        'User task result was not updated in database correctly with mistake '
        'in `incorrect` field'
    )
    assert not result.passed, (
        'User task result was not updated in database correctly with mistake '
        'in `passed` field'
    )
