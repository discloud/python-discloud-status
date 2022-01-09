from __future__ import annotations

import aiohttp
from typing import Any, TYPE_CHECKING
from .errors import ERRORS, RequestError
from .discloud import BaseModel, Action

if TYPE_CHECKING:
    from .client import Client
    from .discloud import File


class Route:
    BASE: str = "https://discloud.app/status"

    def __init__(self, method: str, endpoint: str, **params):
        self.method = method
        self.endpoint = endpoint
        url = self.BASE + endpoint
        if params:
            url = url.format(**params)
        self.url: str = url


class RequestManager(BaseModel):
    def __init__(self, client: Client) -> None:
        super().__init__(client)
        self.api_token: str = client.api_token
        self.__session = aiohttp.ClientSession
        # self.cache: dict = {}

    async def request(self, route: Route, **kwargs) -> Any:
        method: str = route.method
        url: str = route.url
        headers: dict = {"api-token": self.api_token}
        if "file" in kwargs:
            file = kwargs.pop("file")
            form = aiohttp.FormData()
            form.add_field("file", file.fp, filename=file.filename)
            kwargs['data'] = form
        async with self.__session() as ses:
            async with ses.request(method, url, headers=headers, **kwargs) as response:
                code = response.status
                data: dict = await response.json()
                msg: str = data.get('message')
                if code == 200:
                    if method == "GET":
                        return data
                    return Action(data)
                else:
                    err: RequestError.__class__ = ERRORS.get(msg, Exception)
                    if err is not Exception:
                        raise err(msg, self._client.language)
                    else:  # avoid issues
                        raise err

    async def fetch_bot(self, bot_id: int) -> dict:
        return await self.request(Route("GET", "/bot/{bot_id}", bot_id=bot_id))

    async def fetch_user(self) -> dict:
        return await self.request(Route("GET", "/user"))

    async def restart(self, bot_id: int) -> Action:
        return await self.request(Route("POST", "/bot/{bot_id}/restart", bot_id=bot_id))

    async def fetch_logs(self, bot_id: int) -> dict:
        return await self.request(Route("GET", "/bot/{bot_id}/logs", bot_id=bot_id))

    async def commit(self, bot_id: int, file: File, restart: bool = False) -> Action:
        restart = "?restart=true" if restart else "?restart=false"
        return await self.request(Route("POST", "/bot/{bot_id}/commit"+restart, bot_id=bot_id), file=file)




