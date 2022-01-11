PT_ERRORS = {
    "Invalid token": "Token da API inválido",
    "Something went wrong, try again later": "Algo deu errado tente de novo mais tarde",
    "File not found": "Arquivo não encontrado",
    "You don't have this bot": "Você não possui este bot"
}


class DisCloudException(Exception):
    pass


class RequestError(DisCloudException):
    def __init__(self, msg, lang):
        if lang == "pt":
            msg = PT_ERRORS.get(msg, msg)
        super().__init__(msg)


class InvalidToken(RequestError):
    pass


class FileNotFound(RequestError):
    pass


class BotNotFound(RequestError):
    pass


class InternalError(RequestError):
    pass


class InvalidArgument(DisCloudException):
    pass


ERRORS = {
    "Invalid token": InvalidToken,
    "Something went wrong, try again later": InternalError,
    "File not found": FileNotFound,
    "You don't have this bot": BotNotFound
}
