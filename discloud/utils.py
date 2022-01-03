from __future__ import annotations
import datetime


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


def date_now() -> datetime.datetime:
    return datetime.datetime.now(tz=datetime.timezone.utc)


class TimePeriod:
    def __init__(self, data: dict) -> None:
        self.language: str = data['lang']
        left: dict = data['lastDataLeft']
        self.left = left
        self.days: int = left.get('days')
        self.hours: int = left.get('hours')
        self.minutes: int = left.get('minutes')
        self.seconds: int = left.get('seconds')

    def __str__(self) -> str:
        return self.format_string()

    def __repr__(self) -> str:
        return "<TimePeriod days=%s hours=%s minutes=%s seconds=%s>"

    def format_string(self):
        data = self.left
        if self.language == "pt":
            return "{days} dias, {hours} horas, {minutes} minutos e {seconds} segundos".format(**data)
        return "{days} days, {hours} hours, {minutes} minutes and {seconds} seconds".format(**data)


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
