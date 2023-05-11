from __future__ import annotations
import enum
import io
from typing import TYPE_CHECKING, Any, List, Optional

from .utils import TimePeriod, Date, MemoryInfo, NetworkInfo, translate as t
from .discloud_typing import *

if TYPE_CHECKING:
    from .client import Client


class ActionType(enum.Enum):
    set_locale = LocaleUpdatePayload
    upload = RawResponseData
    userinfo = UserPayload
    status = AppsPayload
    logs = LogsPayload
    start = RawResponseData
    restart = RawResponseData
    stop = RawResponseData
    commit = RawResponseData
    remove = RawResponseData
    ram = RawResponseData
    backup = BackupPayload
    get_mods = ModsPayload
    add_mod = AppModPayload
    remove_mod = RawResponseData
    edit_mod = AppModPayload
    mod_start = RawResponseData
    mod_restart = RawResponseData
    mod_stop = RawResponseData
    mod_logs = LogsPayload
    mod_backup = BackupPayload
    mod_ram = RawResponseData
    mod_commit = RawResponseData
    mod_status = AppsPayload


class Response:
    def __init__(self, action: str, data: Any) -> None:
        self.type = ActionType[action]
        self.data = data
        self.message: Optional[str] = data.get("message")
        self.status: str = data["status"]

    def __str__(self) -> str:
        return self.message if self.message else "No message"


class Action:
    def __init__(self, response: Response):
        self.status, self.message = response.status, response.message

    def __repr__(self) -> str:
        return '<Message="%s" status="%s">' % (self.message, self.status)

    def __str__(self) -> str:
        return f"""STATUS: {self.status}\nMESSAGE: {self.message}"""


class File:
    def __init__(self, fp: str | io.BufferedReader) -> None:
        if isinstance(fp, str) and not fp.endswith(".zip"):
            raise ValueError("File must be .zip")  # todo: add custom error translations
        self.bytes = fp
        self.filename = "file"
        if isinstance(fp, str):
            self.bytes = open(fp, "rb")
            self.filename = fp
         


class PlanType(enum.Enum):
    Free = 0
    Carbon = 1
    Gold = 2
    Platinum = 3
    Diamond = 4
    Krypton = 5
    Sapphire = 6
    Safira = 6  # Translation
    Ruby = 7


# Returns
class Backup:
    """
    .class backup
    ------------
    """

    def __init__(self, data: BackupData) -> None:
        self.url = data["url"]

    def __str__(self) -> str:
        return self.url


class Logs:
    def __init__(self, data: LogsData) -> None:
        terminal = data["terminal"]
        self.full = terminal["big"]
        self.small = terminal["small"]
        self.url = terminal["url"]

    def __str__(self) -> str:
        return self.full


# Internal Objects
class Plan:
    def __init__(self, data: UserData) -> None:
        plan_type: PlanType = PlanType[data["plan"]]
        self.type: PlanType = plan_type
        end_date = data.get("planDataEnd")
        self.language = data["locale"]
        is_pt = self.language == "pt-BR"
        self.lifetime: bool = end_date == "Lifetime"
        if end_date != "Subscription":
            self.expire_date = (
                None if self.lifetime or not end_date else Date.from_string(end_date)
            )
            self.expires_in = (
                t("never", is_pt)
                if not self.expire_date
                else TimePeriod.until_date(self.language, self.expire_date)
            )
        else:
            self.expire_date = t(end_date, is_pt)
            self.expires_in = t(end_date, is_pt)

    def __str__(self) -> str:
        return t(self.type.name, self.language == "pt-BR")

    def __repr__(self) -> str:
        return "<Plan type=%s>" % self.type


class ApplicationModerator:
    def __init__(self, data: ModData):
        self.id: int = int(data["modID"])
        self.perms: List[str] = data["perms"]


AppMod = ApplicationModerator


class User:
    def __init__(self, client: Client, data: UserData) -> None:
        self._client = client
        self.id: int = int(data["userID"])
        self.total_ram: int = data["totalRamMb"]
        self.using_ram: int = data["ramUsedMb"]
        self.apps: List[str]
        self.plan: Plan = Plan(data)
        self.locale: str = data["locale"]

    def _build_user_apps(self, app):
        ...


class BaseApplication:  # todo
    pass


class PartialApplication(BaseApplication):
    def __init__(self, client: Client, app_id: str):
        self._client = client
        self.id = app_id

    # async def get_info(self) -> Application:
    #    bot = await self._client.app_info(self.id)
    #    return bot


class Application(PartialApplication):
    __slots__ = ("id", "status", "cpu", "memory", "start_date", "online_since")

    def __init__(self, client: Client, data: AppData) -> None:
        self.status: str = data["container"]
        self.cpu: str = data["cpu"]
        self.memory: MemoryInfo = MemoryInfo(data["memory"])
        is_online = self.status == "Online"
        is_pt = client.language == "pt-BR"
        self.start_date = (
            Date.from_string(data["startedAt"])
            if is_online
            else t("Not available", is_pt)
        )
        self.online_since = (
            TimePeriod.after_date(client.language, self.start_date)
            if is_online
            else t("Offline", is_pt)
        )
        self.net_info = NetworkInfo(data["netIO"])
        self.ssd = data["ssd"]
        super().__init__(client, data["id"])

    # async def get_info(self):
    #    raise NotImplementedError

    # async def restart(self):
    #    return await self._client.restart(self.id)

    # async def fetch_logs(self) -> Logs:
    #    return await self._client.logs(self.id)

    # async def commit(self, file: File):
    #    return await self._client.commit(self.id, file)
