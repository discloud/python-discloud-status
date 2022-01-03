import aiohttp
from typing import Any
from .utils import InvalidArgument


class Route:
    BASE = "https://discloud.app/status"

    def __init__(self, method: str, endpoint: str, **params):
        self.method = method
        self.endpoint = endpoint
        url = self.BASE + endpoint
        if params:
            url.format_map(params)
        self.url: str = url


class RequestManager:
    def __init__(self, api_token: str) -> None:
        self.api_token = api_token
        self.__session = aiohttp.ClientSession()
        self.cache: dict = {}

    async def request(self, route: Route) -> Any:
        method: str = route.method
        url: str = route.url
        headers: dict = {"api-token": self.api_token}
        async with self.__session as ses:
            async with ses.request(method, url, headers=headers) as response:
                return await response.json()

    async def fetch_bot(self, bot_id: int):  # todo: typehint
        return await self.request(Route("GET", "/bot/{bot_id}", bot_id=bot_id))

    async def fetch_user(self):  # todo: typehint
        return await self.request(Route("GET", "/user"))

    async def restart(self, bot_id: int):  # todo: typehint
        return await self.request(Route("POST", "/bot/{bot_id}/restart", bot_id=bot_id))

    async def fetch_logs(self, bot_id: int):  # todo: typehint
        ...




