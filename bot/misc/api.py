"""
External API service connection module.
"""
import logging
from dataclasses import dataclass
from http import HTTPStatus
from os import environ
from typing import ClassVar, Optional, Union

import aiohttp
from aiohttp.client_exceptions import ClientConnectionError

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)


@dataclass
class BaseApi():
    """Base class for API service."""
    url: str
    access_token: Optional[str] = None


@dataclass
class DjangoApiV1(BaseApi):
    """Django API representation."""

    NOT_FOUND: ClassVar[dict] = {'detail': 'not_found'}
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
                    return {'detail': 'server_error'}
            except ClientConnectionError:
                logger.error('Connection error to %s' % url)
                return {'detail': 'connection_error'}

    async def update_user_task_results(self, user_tg_id: int, exercise_id: int,
                                       incorrect: int,
                                       correct: int) -> Union[dict, list,
                                                              None]:
        """Update user task results."""
        url = f'{self.url}results/{user_tg_id}/{exercise_id}/'
        data = {'correct': correct, 'incorrect': incorrect}
        async with aiohttp.ClientSession() as session:
            try:
                async with session.patch(url, json=data) as resp:
                    if resp.status == HTTPStatus.OK:
                        return None
                    if resp.status == HTTPStatus.NOT_FOUND:
                        return self.NOT_FOUND
            except ClientConnectionError:
                logger.error('Connection error to %s' % url)
                return None

    async def get_user_progress(self, user_tg_id: int) -> Optional[dict]:
        """Get user progress data."""
        url = f'{self.url}progress/{user_tg_id}/'
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as resp:
                    if resp.status == HTTPStatus.OK:
                        return await resp.json()
                    if resp.status == HTTPStatus.NOT_FOUND:
                        return self.NOT_FOUND
                    return None
            except ClientConnectionError:
                logger.error('Connection error to %s' % url)
                return {'detail': 'connection_error'}


backend_api = DjangoApiV1()
