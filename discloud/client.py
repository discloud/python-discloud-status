from .http import RequestManager
from .utils import MISSING
from .errors import InvalidArgument
from .discloud import User, Bot, File, Action, Logs


class Client:
    def __init__(self, api_token: str, language: str = MISSING) -> None:
        self.api_token = api_token
        if language not in ["en", "pt"]:
            raise InvalidArgument("Input a valid value")  # todo: change error
        self.language: str = "en" if language is MISSING else language
        self.__requester = RequestManager(self)

    async def fetch_user_info(self) -> User:
        data: dict = await self.__requester.fetch_user()
        return User(self, data)

    async def fetch_bot(self, bot_id: int) -> Bot:
        data: dict = await self.__requester.fetch_bot(bot_id)
        return Bot(self, data)

    async def restart_bot(self, bot_id: int) -> Action:
        response: Action = await self.__requester.restart(bot_id)
        return response

    async def fetch_logs(self, bot_id: int) -> Logs:
        data: dict = await self.__requester.fetch_logs(bot_id)
        return Logs(data)

    async def commit(self, bot_id: int, file: File, restart: bool = False) -> Action:
        response: Action = await self.__requester.commit(bot_id, file, restart=restart)
        return response
