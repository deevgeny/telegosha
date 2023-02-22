from http import HTTPStatus

import pytest

STATS_URL = '/api/v1/progress/'


def test_user_progress_url_exists(api_client, user):
    url = f'{STATS_URL}{user.tg_id}/'
    response = api_client.get(url)
    assert response.status_code != HTTPStatus.NOT_FOUND, (
        f'URL {url} with user tasks not found'
    )


def test_user_progress_url_404(api_client, user):
    url = f'{STATS_URL}{user.tg_id + 1}/'
    response = api_client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND, (
        f'URL {url} with not existing telegram id should return HTTP 404'
    )


def test_user_progress_response_fields_count(api_client, user):
    count = 4
    url = f'{STATS_URL}{user.tg_id}/'
    response = api_client.get(url)
    assert len(response.json()) == count, (
        f'Incorrect number of fields in response from {url}'
    )


@pytest.mark.parametrize('field',
                         ['topics', 'words', 'total_tasks', 'passed_tasks'])
def test_user_progress_response_fields_names(api_client, user, field):
    response = api_client.get(f'{STATS_URL}{user.tg_id}/')
    assert field in response.json(), (
        f'Field `{field}` is missing in response'
    )


@pytest.mark.django_db
def test_user_progress_response_data_with_no_tasks(api_client, user):
    data = {'topics': 0, 'words': 0, 'total_tasks': 0, 'passed_tasks': 0}
    response = api_client.get(f'{STATS_URL}{user.tg_id}/')
    assert response.json() == data, (
        'Incorrect response value for the user with no tasks assigned'
    )


@pytest.mark.django_db
def test_user_progress_response_data_with_1_new_task(api_client, intro_task):
    data = {'topics': 1, 'words': 0, 'total_tasks': 1, 'passed_tasks': 0}
    response = api_client.get(f'{STATS_URL}{intro_task.user.tg_id}/')
    assert response.json() == data, (
        'Incorrect response value for the user who has not passed one task'
    )


@pytest.mark.django_db
def test_user_progress_response_data_with_1_passed_task(api_client,
                                                        intro_task):
    obj = intro_task
    obj.correct = 5
    obj.save()
    data = {'topics': 1, 'words': 5, 'total_tasks': 2, 'passed_tasks': 1}
    response = api_client.get(f'{STATS_URL}{intro_task.user.tg_id}/')
    assert response.json() == data, (
        'Incorrect response value for the user who has passed one task'
    )
