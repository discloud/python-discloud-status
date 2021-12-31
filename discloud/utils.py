from __future__ import annotations
import datetime
from datetime import datetime
# from dateutil


class Missing:
    def __eq__(self, other):
        return False

    def __bool__(self):
        return False

    def __repr__(self):
        return "..."


class DisCloudException(Exception):
    pass


class InvalidArgument(DisCloudException):
    pass


MISSING = Missing()

EN_TEXTS = (

    (86400, "day"),
    (3600, "hour"),
    (60, "minute"),
    (1, "second")
)

PT_TEXTS = (
    (86400, "dia"),
    (3600, "hora"),
    (60, "minuto"),
    (1, "segundo")
)


class TimePeriod:
    def __init__(self, time: dict, language: str = MISSING):  # todo
        self.language = "en" if language is MISSING else language
        self.time = time

    def __str__(self):  # todo
        return self.format_string()

    def format_string(self):
        texts = EN_TEXTS if self.language == "en" else PT_TEXTS
        t = self.time
        total = t['days']*86400 + t['hours']*3600 + t['minutes']*60 + t['seconds']
        result = []
        for amt, unit in texts:
            if total > amt:
                result.append()
        return ', '.join(result)


class FutureDate:
    def __init__(self, date: datetime) -> None:
        self.date = date

    def __repr__(self) -> datetime:
        return self.date

    def __str__(self) -> datetime:
        return self.date

    @classmethod
    async def from_string(cls, text: str) -> FutureDate:
        d: datetime = datetime.datetime.strptime(text[:19], "%Y-%M-%DT%H:%M%S")
        d.replace(tzinfo=None).astimezone(datetime.timezone.utc)
        return cls(d)
