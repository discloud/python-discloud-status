class DisCloudException(Exception):
    pass


class RequestError(DisCloudException):
    pass


class InvalidToken(RequestError):
    pass


class InternalError(RequestError):
    pass


class RateLimit(RequestError):
    pass


class InvalidArgument(DisCloudException):
    pass


