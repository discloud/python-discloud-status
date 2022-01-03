from .manager import RequestManager, Route
from .utils import MISSING, InvalidArgument
from .discloud import DisCloudUser


class UserClient:
    def __init__(self, api_token: str, language: str = MISSING) -> None:
        self.api_token = api_token
        if language not in ["en", "pt"]:
            raise InvalidArgument("Input a valid value")  # todo: change error
        self.language = "en" if language is MISSING else language
        self.__requester = RequestManager(api_token)

    async def fetch_user_info(self) -> DisCloudUser:
        data = await self.__requester.fetch_user()
        data['lang'] = self.language
        # print(data) debugging purposes
        return DisCloudUser(data)

    async def fetch_bot(self, bot_id: int):  # todo: typehint
        ...
