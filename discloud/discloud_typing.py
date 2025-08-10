from __future__ import annotations

from typing import Dict, List, Literal, Optional, TypedDict, Union


class RawResponseData(TypedDict):
    message: Optional[str]
    status: Literal["ok", "error"]
    statusCode: Optional[int]

class AppInfo(TypedDict):
    id: str
    avatarURL: str
    name: str
    type: int
    online: bool
    ram_killed: bool
    main_file: str
    lang: str
    mods: List[any]
    autoDeployGit: str
    autoRestart: bool

class AppStatus(TypedDict):
    id: str
    container: str
    cpu: str
    memory: str
    ssd: str
    netIO: Dict[str, str]
    last_restart: str
    startedAt: str


class BackupData(TypedDict):
    id: str
    url: str


class LogsData(TypedDict):
    id: str
    terminal: Dict[str, str]


class ModData(TypedDict):
    modID: str
    perms: List[str]


class UserData(TypedDict):
    userID: str
    totalRamMb: int
    ramUsedMb: int
    apps: List[str]
    plan: str
    lastDataLeft: Dict[str, int]
    planDataEnd: str
    locale: str
    subdomains: Optional[List[str]]
    customdomains: Optional[List[str]]


class ResponsePayload(RawResponseData):
    user: Optional[UserData]
    apps: Optional[
        Union[Union[List[AppStatus], AppStatus], Union[List[LogsData], LogsData]]
    ]


class AppsPayload(RawResponseData):
    apps: Union[List[AppStatus], AppStatus]


class AppModPayload(RawResponseData):
    app: Dict[str, Union[str, List[str]]]


class BackupPayload(RawResponseData):
    backups: Union[List[BackupData], BackupData]


class LocaleUpdatePayload(RawResponseData):
    locale: str


class LogsPayload(RawResponseData):
    apps: Union[List[LogsData], LogsData]


class ModsPayload(RawResponseData):
    team: Union[List[ModData], ModData]


class UserPayload(RawResponseData):
    user: UserData
