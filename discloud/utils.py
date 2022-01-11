from __future__ import annotations
import datetime

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import Client

__all__ = ("MISSING",
           "TimePeriod",
           "FutureDate",
           "date_now",
           "MemoryInfo")


class Missing:
    def __eq__(self, other):
        return False

    def __bool__(self):
        return False

    def __repr__(self):
        return "..."


MISSING = Missing()


def date_now() -> datetime.datetime:
    return datetime.datetime.now(tz=datetime.timezone.utc)


class TimePeriod:
    __slots__ = (
        "days",
        "hours",
        "minutes",
        "seconds",
        "_left",
        "_client",
        "_language"
    )

    def __init__(self, client: Client, data: dict) -> None:
        self._client = client
        self._language: str = client.language
        left: dict = data['lastDataLeft']
        self._left = left
        self.days: int | None = left.get('days', 0)
        self.hours: int | None = left.get('hours', 0)
        self.minutes: int | None = left.get('minutes', 0)
        self.seconds: int | None = left.get('seconds', 0)

    def __str__(self) -> str:
        return self.format_string()

    def __repr__(self) -> str:
        return "<TimePeriod days=%s hours=%s minutes=%s seconds=%s>"

    def total_seconds(self) -> int:
        return self.days * 86400 + self.hours * 3600 + self.minutes * 60 + self.seconds

    @staticmethod
    def _converter_pt(secs: int) -> str:
        info = {
            "dia": 86400,
            "hora": 3600,
            "minuto": 60,
            "segundo": 1
        }
        result = []
        for unit, deli in info.items():
            if secs >= deli:
                amt, secs = divmod(secs, deli)
                add_s = "s" if amt > 1 else ""
                result.append(f"{amt} {unit}{add_s}")
        return ', '.join(result)

    @staticmethod
    def _converter_en(secs: int) -> str:
        info = {
            "day": 86400,
            "hour": 3600,
            "minute": 60,
            "second": 1
        }
        result = []
        for unit, deli in info.items():
            if secs >= deli:
                amt, secs = divmod(secs, deli)
                add_s = "s" if amt > 1 else ""
                result.append(f"{amt} {unit}{add_s}")
        return ', '.join(result)

    def format_string(self) -> str:
        left: int = self.total_seconds()
        conv = self._converter_en if self._client.language == "en" else self._converter_pt
        return conv(left)

    @classmethod
    def from_text(cls, client: Client, text: str) -> TimePeriod:
        if "about" in text:  # about an hour/about a minute
            unit = text.split()[2]
            amt = 1
        else:  # everything else: x days, x hours, x minutes
            amt, unit = text.split()
            amt = 1 if not amt.isdigit() else amt
        unit = unit+"s" if not unit.endswith("s") else unit
        return cls(client, {"lastDataLeft": {unit: int(amt)}})


class FutureDate:
    def __init__(self, date: datetime.datetime, tz: datetime.tzinfo = None) -> None:
        self.date = date
        self.tz = tz

    def __repr__(self) -> datetime.datetime:
        return self.date

    def __str__(self) -> str:
        return self.date.strftime("%d-%m-%Y %H:%M:%S")

    @classmethod
    def from_string(cls, text: str) -> FutureDate:  # todo: refactor this function
        d: datetime = datetime.datetime.strptime(text[:19], "%Y-%m-%DT%H:%M:%S")
        d.replace(tzinfo=None).astimezone(datetime.timezone.utc)
        return cls(d)

    @classmethod
    def from_dict(cls, data: dict, tz: datetime.tzinfo = None) -> FutureDate:
        tz = tz if tz else datetime.timezone.utc
        end_time = date_now() + datetime.timedelta(**data)
        return cls(end_time, tz)

    def to_tz(self, tz: datetime.tzinfo = None) -> FutureDate:
        self.date.replace(tzinfo=self.tz).astimezone(tz)
        return self


class StatInfo:  # possible future stats add
    ...


class MemoryInfo(StatInfo):
    def __init__(self, info: str) -> None:
        self._info = info

    def __str__(self) -> str:
        return self._info

    @property
    def using(self):
        return self._info.split("/")[0]

    @property
    def available(self):
        return self._info.split("/")[1]
