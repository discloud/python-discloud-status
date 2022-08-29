from .http import RequestManager
from .utils import MISSING
from .errors import InvalidArgument
from .discloud import Action, Application, AppMod, Backup, File, Logs, Response, User
from .discloud_typing import *

from typing import List, Literal


class Client:
    def __init__(self, api_token: str, language=MISSING, **kwargs) -> None:
        self.api_token = api_token
        self.language: str = "en-US" if language is MISSING else language
        self.http = RequestManager(self, **kwargs)

    async def set_language(self, language: str) -> Action:
        available_options = ["pt-BR", "en-US"]
        if language not in available_options:
            raise InvalidArgument(f"'language' must be one of following: {', '.join(available_options)}")
        response: Response = await self.http.set_locale(language)
        self.language = language
        return Action(response)

    async def delete_app(self, app_id: str) -> Action:
        response: Response = await self.http.delete_app(app_id)
        return Action(response)

    async def upload_app(self, file: File) -> Action:
        if not isinstance(file, File):
            raise InvalidArgument('File must be an instance of File')
        response: Response = await self.http.upload_app(file)
        return Action(response)

    async def user_info(self) -> User:
        response: Response = await self.http.fetch_user()
        data: UserPayload = response.data
        user_data: UserData = data['user']
        return User(self, user_data)

    async def app_info(self, target: str | Literal["all"]) -> Application | List[Application]:
        response: Response = await self.http.fetch_app(target)
        data: AppsPayload = response.data
        apps = data['apps']
        if isinstance(apps, list):
            apps: List[AppData]
            return [Application(self, app_data) for app_data in apps]
        apps: AppData
        return Application(self, apps)

    async def restart(self, target: str | Literal["all"]) -> Action:
        response = await self.http.restart(target)
        return Action(response)

    async def start(self, target: str | Literal["all"]) -> Action:
        response = await self.http.start(target)
        return Action(response)

    async def stop(self, target: str | Literal["all"]) -> Action:
        response = await self.http.stop(target)
        return Action(response)

    async def logs(self, target: str | Literal["all"]) -> Logs | List[Logs]:
        response: Response = await self.http.fetch_logs(target)
        data: LogsPayload = response.data
        logs = data['apps']
        if isinstance(logs, list):
            logs: List[LogsData]
            return [Logs(logs_data) for logs_data in logs]
        logs: LogsData
        return Logs(logs)

    async def commit(self, app_id: str, file: File) -> Action:
        if not isinstance(file, File):
            raise InvalidArgument('File must be an instance of File')
        response: Response = await self.http.commit_app(app_id, file)
        return Action(response)

    async def ram(self, app_id: str, new_ram: int) -> Action:
        response: Response = await self.http.change_app_ram(app_id, new_ram)
        return Action(response)

    async def backup(self, target: str | Literal["all"]) -> Backup | List[Backup]:
        response: Response = await self.http.backup(target)
        data: BackupPayload = response.data
        backups = data['backups']
        if isinstance(backups, list):
            backups: List[BackupData]
            return [Backup(backup_data) for backup_data in backups]
        backups: BackupData
        return Backup(backups)


mod_perms = ["start_app", "stop_app", "restart_app", "logs_app", "commit_app", "edit_ram", "backup_app", "status_app"]


class ModManager:
    def __init__(self, client: Client, app_id: str):
        self.client: Client = client
        self.http: RequestManager = client.http
        self.app_id = app_id

    async def get_mods(self) -> AppMod | List[AppMod]:
        response: Response = await self.http.get_mods_for_app(self.app_id)
        data: ModsPayload = response.data
        mods = data['team']
        if isinstance(mods, list):
            mods: List[ModData]
            return [AppMod(mod_data) for mod_data in mods]
        mods: ModData
        return AppMod(mods)

    async def add_mod(self, mod_id: str, perms: List[str]) -> Action: # keep an eye
        if not isinstance(perms, list):
            raise InvalidArgument('"new_perms" must be a list of perms')
        if not perms:
            raise InvalidArgument("you must give a list of new perms")
        response: Response = await self.http.add_mod_for_app(self.app_id, mod_id, perms)
        return Action(response)

    async def delete_mod(self, mod_id: str) -> Action:
        response: Response = await self.http.remove_mod_for_app(self.app_id, mod_id)
        return Action(response)

    async def edit_mod_perms(self, mod_id: str, new_perms: List[str]) -> Action:
        if not isinstance(new_perms, list):
            raise InvalidArgument('"new_perms" must be a list of perms')
        if not new_perms:
            raise InvalidArgument("you must give a list of new perms")
        final = []
        for perm in new_perms:
            if perm not in mod_perms:
                final.append(perm)
        if final:
            raise InvalidArgument(f"Invalid perms were found: {', '.join(final)}. "
                                  f"Available perms: {', '.join(mod_perms)}.")
        response: Response = await self.http.edit_mod_perms_for_app(self.app_id, mod_id, new_perms)
        return Action(response)

    async def start(self) -> Action:
        response: Response = await self.http.mod_start_app(self.app_id)
        return Action(response)

    async def stop(self) -> Action:
        response: Response = await self.http.mod_stop_app(self.app_id)
        return Action(response)

    async def restart(self) -> Action:
        response: Response = await self.http.mod_restart_app(self.app_id)
        return Action(response)

    async def backup(self) -> Backup | List[Backup]:
        response: Response = await self.http.mod_backup_app(self.app_id)
        data: BackupPayload = response.data
        backups = data['backups']
        if isinstance(backups, list):
            backups: List[BackupData]
            return [Backup(backup_data) for backup_data in backups]
        backups: BackupData
        return Backup(backups)

    async def commit(self, file: File) -> Action:
        response: Response = await self.http.mod_commit_app(self.app_id, file)
        return Action(response)

    async def logs(self) -> Logs | List[Logs]:
        response: Response = await self.http.mod_app_logs(self.app_id)
        data: LogsPayload = response.data
        logs = data['apps']
        if isinstance(logs, list):
            logs: List[LogsData]
            return [Logs(logs_data) for logs_data in logs]
        logs: LogsData
        return Logs(logs)

    async def change_ram(self, new_ram: int) -> Action:
        response: Response = await self.http.mod_change_app_ram(self.app_id, new_ram)
        return Action(response)

    async def status(self) -> Application | List[Application]:
        response: Response = await self.http.mod_app_status(self.app_id)
        data: AppsPayload = response.data
        apps = data['apps']
        if isinstance(apps, list):
            apps: List[AppData]
            return [Application(self.client, app_data) for app_data in apps]
        apps: AppData
        return Application(self.client, apps)
