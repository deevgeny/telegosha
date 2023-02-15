"""
External API service connection module.
"""
import logging
from dataclasses import dataclass
from http import HTTPStatus
from os import environ
from typing import ClassVar, Union

import aiohttp
from aiohttp.client_exceptions import ClientConnectionError

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)


@dataclass
class BackendApiV1():
    """Backend v1 API class."""

    NOT_FOUND: ClassVar[dict] = {'detail': 'not_found'}
    SERVER_ERROR: ClassVar[dict] = {'detail': 'server_error'}
    CONNECTION_ERROR: ClassVar[dict] = {'detail': 'connection_error'}
    url: str = environ.get('BACKEND_URL', 'http://127.0.0.1:8000/api/v1/')

    async def get_user_tasks(self, user_tg_id: int) -> dict:
        """Return user assigned tasks."""
        url = f'{self.url}tasks/{user_tg_id}/'
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as resp:
                    if resp.status == HTTPStatus.OK:
                        return await resp.json()
                    if resp.status == HTTPStatus.NOT_FOUND:
                        return self.NOT_FOUND
                    logger.error(
                        'Response status %s to url %s' % (resp.status, url)
                    )
                    return self.SERVER_ERROR
            except ClientConnectionError:
                logger.error('Connection error to %s' % url)
                return self.CONNECTION_ERROR

    async def update_user_task_results(self, user_tg_id: int, exercise_id: int,
                                       incorrect: int,
                                       correct: int) -> Union[dict, list]:
        """Update user task results."""
        url = f'{self.url}results/{user_tg_id}/{exercise_id}/'
        data = {'correct': correct, 'incorrect': incorrect}
        async with aiohttp.ClientSession() as session:
            try:
                async with session.patch(url, json=data) as resp:
                    if resp.status == HTTPStatus.OK:
                        return await resp.json()
                    if resp.status == HTTPStatus.NOT_FOUND:
                        return self.NOT_FOUND
            except ClientConnectionError:
                logger.error('Connection error to %s' % url)
                return self.CONNECTION_ERROR

    async def get_user_progress(self, user_tg_id: int) -> dict:
        """Get user progress data."""
        url = f'{self.url}progress/{user_tg_id}/'
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as resp:
                    if resp.status == HTTPStatus.OK:
                        return await resp.json()
                    if resp.status == HTTPStatus.NOT_FOUND:
                        return self.NOT_FOUND
                    return self.SERVER_ERROR
            except ClientConnectionError:
                logger.error('Connection error to %s' % url)
                return self.CONNECTION_ERROR


backend_api = BackendApiV1()
