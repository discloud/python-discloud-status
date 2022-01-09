from __future__ import annotations
import enum
import io
from typing import TYPE_CHECKING

from .utils import TimePeriod, FutureDate, MemoryInfo

if TYPE_CHECKING:
    from .client import Client

PT_TRANSLATIONS = {
    "Free": "Grátis",
    "Platinum": "Platina",
    "Diamond": "Diamante",
    "Sapphire": "Safíra"
}


class Action:
    def __init__(self, data: dict) -> None:  # todo: translate messages
        self.message: str = data['message']
        self.status: bool = data['status']

    def __repr__(self) -> str:
        return "<Message=\"%s\" status=%s>" % (self.message, self.status)

    def __str__(self) -> str:
        return self.message


class File:
    def __init__(self, fp: str | io.IOBase) -> None:
        if not fp.endswith(".zip"):
            raise ValueError("File must be .zip")   # todo: add custom error translations
        self.fp = open(fp, "rb")
        self.filename: str = self.fp.name


class PlanType(enum.Enum):
    Free = 0
    Carbon = 3
    Gold = 1
    Platinum = 2
    Diamond = 4
    # ... = 5 todo: v2 release
    Sapphire = 6
    # ... = 7 todo: v2 release


class Logs:
    def __init__(self, data: dict) -> None:
        self.url = data['link']
        self.logs = self.text = data['logs']

    def __str__(self) -> str:
        return self.logs


class BaseModel:
    __slots__ = (
        '_client'
    )

    def __init__(self, client: Client):
        self._client = client


class Plan(BaseModel):
    def __init__(self, client: Client, data: dict) -> None:
        super().__init__(client)
        self.type: PlanType = PlanType[data['plan']]
        self.lifetime: bool = data.get('planDataEnd') == "Lifetime"
        self.language: str = client.language
        if self.lifetime:
            self.expires_in: str = "never"
            if self.language == "pt":
                self.expires_in: str = "nunca"
            self.expire_date = None

        else:
            self.expire_date: FutureDate = FutureDate.from_dict(data['lastDataLeft'])
            self.expires_in: TimePeriod = TimePeriod(self._client, data)

    def __str__(self) -> str:
        if self.language == "pt":
            return PT_TRANSLATIONS.get(self.type.name, self.type.name)
        return self.type.name

    def __repr__(self) -> str:
        return "<Plan type=%s>" % self.type


class User(BaseModel):
    __slots__ = ("id",
                 "plan")

    def __init__(self, client: Client, data: dict) -> None:
        super().__init__(client)
        self.id: int = int(data['userID'])
        self.plan: Plan = Plan(client, data)


class BaseApplication(BaseModel):  # todo: v2 future site applications
    async def restart(self):
        raise NotImplementedError


class Site(BaseApplication):  # todo: v2 discloud
    async def restart(self):
        ...


class Bot(BaseApplication):
    __slots__ = ("id",
                 "status",
                 "cpu",
                 "memory",
                 "last_restart")

    def __init__(self, client: Client, data: dict) -> None:
        super().__init__(client)
        self.id: int = int(data['bot_id'])
        self.status: str = data['container']
        self.cpu: str = data['cpu']
        self.memory: MemoryInfo = MemoryInfo(data['memory'])
        self.last_restart: TimePeriod = TimePeriod.from_text(client, data['last_restart'])
        # self.language = "Python"
        # self.lang_version = "3.10.1"

    async def restart(self) -> Action:
        return await self._client.restart_bot(self.id)

    async def fetch_logs(self) -> Logs:
        return await self._client.fetch_logs(self.id)

    async def commit(self, file: File, restart: bool = False) -> Action:
        return await self._client.commit(self.id, file, restart=restart)
