from __future__ import annotations

import aiohttp
import time
from typing import Any, TYPE_CHECKING
from .errors import ERRORS, RequestError
from .discloud import BaseModel, Action, File

if TYPE_CHECKING:
    from .client import Client


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
        self.rate_limit_reset: None | float = None
        self.check_timer: bool = False
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
        if self.check_timer:
            if time.time() < self.rate_limit_reset:
                raise RequestError("Ratelimit still on cooldown", self._client.language)
            else:
                self.check_timer = False
        async with self.__session() as ses:
            async with ses.request(method, url, headers=headers, **kwargs) as response:
                code = response.status
                data: dict = await response.json()
                msg: str = data.get('message')
                r_headers = response.headers
                ratelimit_rem = int(r_headers['x-ratelimit-remaining'])
                #print(f"Request restante", ratelimit_rem)
                #ratelimit_reset = r_headers['x-ratelimit-reset']
                #print(f"Timestamp reset {ratelimit_reset}", f"Timestamp now {int(time.time())}")
                #print("Diff", int(ratelimit_reset)-int(time.time()))
                if ratelimit_rem == 9:
                    self.rate_limit_reset = time.time() + 130
                if ratelimit_rem == 0:
                    self.check_timer = True
                if code == 200:
                    if method == "GET":
                        return data
                    return Action(data)
                else:
                    err: RequestError.__class__ = ERRORS.get(msg, Exception)
                    if err is not Exception:
                        raise err(msg, self._client.language)
                    else:  # avoid issues
                        raise err(data)

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


