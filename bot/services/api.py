"""
External API service connection module.
"""
import asyncio
import logging
from dataclasses import dataclass
from http import HTTPStatus
from typing import Optional

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

    url: str = "http://127.0.0.1:8000/api/v1/"

    async def get_user_tasks(self, user_tg_id: int) -> dict:
        """Return user assigned tasks."""
        url = f'{self.url}tasks/{user_tg_id}/'
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as resp:
                    if resp.status != HTTPStatus.OK:
                        return []
                    return await resp.json()
            except ClientConnectionError:
                logger.error('Connection error')
                return []

    async def update_user_task_results(self, user_tg_id: int, exercise_id: int,
                                       correct: int, incorrect: int) -> None:
        """Update user task results."""
        url = f'{self.url}tasks/{user_tg_id}/{exercise_id}/'
        data = {'correct': correct, 'incorrect': incorrect}
        async with aiohttp.ClientSession() as session:
            try:
                async with session.patch(url, json=data) as resp:
                    if resp.status == HTTPStatus.OK:
                        return
                    return
            except ClientConnectionError:
                logger.error('Connection error')
                return


backend_api = DjangoApiV1()


async def main():
    mock_api = DjangoApiV1()
    tasks = await mock_api.get_user_tasks(5874231148)
    print(tasks)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
