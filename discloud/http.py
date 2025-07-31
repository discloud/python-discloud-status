from __future__ import annotations

import aiohttp
from typing import TYPE_CHECKING, Any
from .errors import InvalidArgument, InvalidToken, RequestError
from .discloud import File, Response
from .discloud_typing import *

if TYPE_CHECKING:
    from .client import Client


class Route:
    VERSION: int
    # BASE_V1: str = "https://discloud.app/status"
    BASE_V2: str = "https://api.discloud.app/v2"

    ENDPOINTS = {
        #   1: {
        #        "INFO": "/user",
        #        "BOT_COMMIT": "/bot/{target}/commit",
        #        "BOT_INFO": "/bot/{target}",
        #        "BOT_LOGS": "/bot/{target}/logs",
        #        "BOT_RESTART": "/bot/{target}/restart{restart}"
        #   },
        2: {
            "SET_LOCALE": {"METHOD": "PUT", "PATH": "/locale/{locale}"},
            "GET_USER_INFO": {"METHOD": "GET", "PATH": "/user"},
            "GET_APP_INFO": {"METHOD": "GET", "PATH": "/app/{app_id}"},
            "UPLOAD": {"METHOD": "POST", "PATH": "/upload"},
            "GET_STATUS": {"METHOD": "GET", "PATH": "/app/{target}/status"},
            "GET_LOGS": {"METHOD": "GET", "PATH": "/app/{target}/logs"},
            "START": {"METHOD": "PUT", "PATH": "/app/{target}/start"},
            "RESTART": {"METHOD": "PUT", "PATH": "/app/{target}/restart"},
            "STOP": {"METHOD": "PUT", "PATH": "/app/{target}/stop"},
            "COMMIT": {"METHOD": "PUT", "PATH": "/app/{app_id}/commit"},
            "DELETE": {"METHOD": "DELETE", "PATH": "/app/{app_id}/delete"},
            "RAM": {"METHOD": "PUT", "PATH": "/app/{app_id}/ram"},
            "BACKUP": {"METHOD": "GET", "PATH": "/app/{target}/backup"},
            # mod management
            "ADD_MOD": {"METHOD": "POST", "PATH": "/app/{app_id}/team"},
            "REMOVE_MOD": {"METHOD": "DELETE", "PATH": "/app/{app_id}/team/{mod_id}"},
            "EDIT_MOD": {"METHOD": "PUT", "PATH": "/app/{app_id}/team"},
            "GET_MODS": {"METHOD": "GET", "PATH": "/app/{app_id}/team"},
            # mod stuff
            "MOD_START_APP": {"METHOD": "PUT", "PATH": "/team/{app_id}/start"},
            "MOD_RESTART_APP": {"METHOD": "PUT", "PATH": "/team/{app_id}/restart"},
            "MOD_STOP_APP": {"METHOD": "PUT", "PATH": "/team/{app_id}/stop"},
            "MOD_BACKUP_APP": {"METHOD": "GET", "PATH": "/team/{app_id}/backup"},
            "MOD_COMMIT_APP": {"METHOD": "PUT", "PATH": "/team/{app_id}/commit"},
            # NA
            "MOD_APP_LOGS": {"METHOD": "GET", "PATH": "/team/{app_id}/logs"},
            "MOD_CHANGE_RAM": {"METHOD": "PUT", "PATH": "/team/{app_id}/ram"},
            "MOD_APP_STATUS": {"METHOD": "GET", "PATH": "/team/{app_id}/status"},
        }
    }

    def __init__(self, version: int, endpoint: str, **params):
        if version != 2:
            raise InvalidArgument("Invalid version selected, available options: (2,)")
        api: Dict[str, Dict[str, str]] = self.ENDPOINTS[version]  # type: ignore
        route: Dict[str, str] = api[endpoint]
        self.method: str = route.get("METHOD", "")
        self.endpoint: str = route.get("PATH", "")
        url: str = getattr(self, f"BASE_V{version}") + self.endpoint
        if params:
            url = url.format(**params)
        self.url = url


class RequestManager:
    def __init__(self, client: Client, **kwargs) -> None:
        self.api_token: str = client.api_token
        self.__session = aiohttp.ClientSession
        self.version: int = 2  # kwargs.get("version", 2)
        self.debug: bool = kwargs.get("debug", False)
        self.rate_limit_remaining: int = 1

    async def request(self, route: Route, **kwargs) -> Any:
        method: str = route.method
        url: str = route.url
        headers: dict = {"api-token": self.api_token}
        if method == "PUT":
            kwargs["skip_auto_headers"] = {"Content-Type"}
        if "file" in kwargs:
            file = kwargs.pop("file")
            form = aiohttp.FormData()
            form.add_field("file", file.bytes, filename=file.filename)
            kwargs["data"] = form
            try:
                del kwargs["skip_auto_headers"]
            except KeyError:
                pass
        if "json" in kwargs:
            headers["Content-Type"] = "application/json"
        if self.rate_limit_remaining == 0:
            raise RequestError("Ratelimit still on cooldown")
        async with self.__session() as ses:
            async with ses.request(method, url, headers=headers, **kwargs) as response:
                code: int = response.status
                if code == 200:
                    data = await response.json()
                    r_headers = response.headers
                    if self.debug:
                        print(data)
                    remain = int(r_headers["ratelimit-remaining"])
                    self.rate_limit_remaining = remain  # todo improve?
                    return data
                else:
                    if code == 401:
                        raise InvalidToken(
                            "An invalid token was provided"
                        )  # todo translate
                    d: dict = await response.json()
                    msg: str = d.get("message", None)
                    raise RequestError(
                        f"""An error ocurred during {method} request to {url}\nERROR: {msg}"""
                    )

    async def set_locale(self, lang: str) -> Response:
        route = Route(self.version, "SET_LOCALE", locale=lang)
        result = await self.request(route)
        response = Response("set_locale", result)
        return response

    async def commit_app(self, app_id: str, file: File) -> Response:
        route = Route(self.version, "COMMIT", app_id=app_id)
        result = await self.request(route, file=file)
        response = Response("commit", result)
        return response

    async def delete_app(self, app_id: str) -> Response:
        route = Route(self.version, "DELETE", app_id=app_id)
        result = await self.request(route)
        response = Response("delete", result)
        return response
    
    async def fetch_app(self, target: str) -> Response:
        route = Route(self.version, "GET_APP_INFO", app_id=target)
        result = await self.request(route)
        response = Response("status", result)
        return response

    async def fetch_app_status(self, target: str) -> Response:
        route = Route(self.version, "GET_STATUS", target=target)
        result = await self.request(route)
        response = Response("status", result)
        return response

    async def fetch_logs(self, target: str) -> Response:
        route = Route(self.version, "GET_LOGS", target=target)
        result = await self.request(route)
        response = Response("logs", result)
        return response

    async def fetch_user(self) -> Response:
        route = Route(self.version, "GET_USER_INFO")
        result = await self.request(route)
        response = Response("userinfo", result)
        return response

    async def start(self, target: str) -> Response:
        route = Route(self.version, "START", target=target)
        result = await self.request(route)
        response = Response("start", result)
        return response

    async def stop(self, target: str) -> Response:
        route = Route(self.version, "STOP", target=target)
        result = await self.request(route)
        response = Response("stop", result)
        return response

    async def restart(self, target: str) -> Response:
        route = Route(self.version, "RESTART", target=target)
        result: RawResponseData = await self.request(route)
        response = Response("restart", result)
        return response

    async def upload_app(self, file: File) -> Response:
        route = Route(self.version, "UPLOAD")
        result: RawResponseData = await self.request(route, file=file)
        response: Response = Response("upload", result)
        return response

    async def change_app_ram(self, app_id: str, new_ram: int) -> Response:
        route = Route(self.version, "RAM", app_id=app_id)
        result: RawResponseData = await self.request(route, json={"ramMB": new_ram})
        response: Response = Response("ram", result)
        return response

    async def backup(self, target: str) -> Response:
        route = Route(self.version, "BACKUP", target=target)
        result: BackupPayload = await self.request(route)
        response: Response = Response("backup", result)
        return response

    # mod stuff
    async def get_mods_for_app(self, app_id: str) -> Response:
        route = Route(self.version, "GET_MODS", app_id=app_id)
        result = await self.request(route)
        response: Response = Response("get_mods", result)
        return response

    async def add_mod_for_app(
        self, app_id: str, mod_id: str, perms: List[str]
    ) -> Response:
        route = Route(self.version, "ADD_MOD", app_id=app_id)
        payload = {"modID": mod_id, "perms": perms}
        result = await self.request(route, json=payload)
        response = Response("add_mod", result)
        return response

    async def remove_mod_for_app(self, app_id: str, mod_id: str) -> Response:
        route = Route(self.version, "REMOVE_MOD", app_id=app_id, mod_id=mod_id)
        result = await self.request(route)
        response = Response("remove_mod", result)
        return response

    async def edit_mod_perms_for_app(
        self, app_id: str, mod_id: str, perms: List[str]
    ) -> Response:
        route = Route(self.version, "EDIT_MOD", app_id=app_id)
        payload = {"modID": mod_id, "perms": perms}
        result = await self.request(route, json=payload)
        response = Response("edit_mod", result)
        return response

    async def mod_start_app(self, app_id: str) -> Response:
        route = Route(self.version, "MOD_START_APP", app_id=app_id)
        result = await self.request(route)
        response = Response("mod_start", result)
        return response

    async def mod_stop_app(self, app_id: str) -> Response:
        route = Route(self.version, "MOD_STOP_APP", app_id=app_id)
        result = await self.request(route)
        response = Response("mod_stop", result)
        return response

    async def mod_restart_app(self, app_id: str) -> Response:
        route = Route(self.version, "MOD_RESTART_APP", app_id=app_id)
        result = await self.request(route)
        response = Response("mod_restart", result)
        return response

    async def mod_backup_app(self, app_id: str) -> Response:
        route = Route(self.version, "MOD_BACKUP_APP", app_id=app_id)
        result = await self.request(route)
        response = Response("mod_backup", result)
        return response

    async def mod_commit_app(self, app_id: str, file: File) -> Response:
        route = Route(self.version, "MOD_COMMIT_APP", app_id=app_id)
        result = await self.request(route, file=file)
        response = Response("mod_commit", result)
        return response

    async def mod_app_logs(self, app_id: str) -> Response:
        route = Route(self.version, "MOD_APP_LOGS", app_id=app_id)
        result = await self.request(route)
        response = Response("mod_logs", result)
        return response

    async def mod_change_app_ram(self, app_id: str, new_ram=int) -> Response:
        route = Route(self.version, "MOD_CHANGE_RAM", app_id=app_id)
        result = await self.request(route, json={"ramMB": new_ram})
        response = Response("mod_ram", result)
        return response

    async def mod_app_status(self, app_id: str) -> Response:
        route = Route(self.version, "MOD_APP_STATUS", app_id=app_id)
        result = await self.request(route)
        response = Response("mod_status", result)
        return response
