from http import HTTPStatus

import pytest

STATS_URL = '/api/v1/progress/'


def test_user_stats_url_exists(api_client, user):
    url = f'{STATS_URL}{user.tg_id}/'
    response = api_client.get(url)
    assert response.status_code != HTTPStatus.NOT_FOUND, (
        f'URL {url} with user tasks not found'
    )


def test_user_stats_url_404(api_client, user):
    url = f'{STATS_URL}{user.tg_id + 1}/'
    response = api_client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND, (
        f'URL {url} with not existing telegram id should return HTTP 404'
    )


def test_user_stats_response_fields_count(api_client, user):
    count = 4
    url = f'{STATS_URL}{user.tg_id}/'
    response = api_client.get(url)
    assert len(response.json()) == count, (
        f'Incorrect number of fields in response from {url}'
    )


@pytest.mark.parametrize('field',
                         ['topics', 'words', 'total_tasks', 'passed_tasks'])
def test_user_stats_response_fields_names(api_client, user, field):
    response = api_client.get(f'{STATS_URL}{user.tg_id}/')
    assert field in response.json(), (
        f'Field `{field}` is missing in response'
    )


@pytest.mark.django_db
def test_user_stats_response_data_with_0_passed_tasks(api_client, user,
                                                      two_tasks_with_words):
    data = {'topics': 1, 'words': 0, 'total_tasks': 2, 'passed_tasks': 0}
    response = api_client.get(f'{STATS_URL}{user.tg_id}/')
    assert response.json() == data, (
        'Incorrect response value for the user who has not completed any '
        'task yet'
    )


@pytest.mark.django_db
def test_user_stats_response_data_with_1_passed_tasks(api_client, user,
                                                      two_tasks_with_words,
                                                      one_task_passed):
    data = {'topics': 1, 'words': 5, 'total_tasks': 2, 'passed_tasks': 1}
    response = api_client.get(f'{STATS_URL}{user.tg_id}/')
    assert response.json() == data, (
        'Incorrect response value for the user who has passed one task'
    )


@pytest.mark.django_db
def test_user_stats_response_data_with_2_passed_tasks(api_client, user,
                                                      two_tasks_with_words,
                                                      two_tasks_passed):
    data = {'topics': 1, 'words': 5, 'total_tasks': 2, 'passed_tasks': 2}
    response = api_client.get(f'{STATS_URL}{user.tg_id}/')
    assert response.json() == data, (
        'Incorrect response value for the user who has passed two tasks'
    )
