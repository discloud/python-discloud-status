from __future__ import annotations
import datetime
import dateutil.parser
import requests
from typing import List, Tuple
from libretranslatepy import LibreTranslateAPI


__all__ = (
    "MISSING",
    "TimePeriod",
    "check_perms",
    "Date",
    "date_now",
    "MemoryInfo",
    "NetworkInfo",
    "mod_perms",
    "translate",
)


mod_perms = [
    "start_app",
    "stop_app",
    "restart_app",
    "logs_app",
    "commit_app",
    "edit_ram",
    "backup_app",
    "status_app",
]


def check_perms(perms) -> Tuple[List[str], List[str]]:
    invalid = []
    for perm in perms:
        if perm not in mod_perms:
            perms.remove(perm)
            invalid.append(perm)
    return perms, invalid

class Translate:
    def get_fast_translator_provider(self) -> dict:
        providers = []
        translators_url = [
            "https://translate.argosopentech.com",
            "https://libretranslate.de",
            "https://lt.vern.cc"
        ]

        for translator_url in translators_url:
            try:
                request = requests.get(translator_url, timeout=1.2)
            except Exception:
                continue

            if request.status_code == 200:
                providers.append({
                    'url': request.url,
                    'time': request.elapsed.total_seconds()
                })

        return min(providers, key=lambda provider: provider['time']) if len(providers) >= 1 else {}
    
    def translate(self, string: str, target: str, source: str = None) -> str:
        provider = self.get_fast_translator_provider()

        if not provider or string == target:
            return string
        
        translator = LibreTranslateAPI(provider['url'])

        for language in translator.languages():
            if language['code'] == target:
                break
            else:
                return string

        if source is None:
            source = translator.detect(string)[0]['language']

            if target == source:
                return string

        return translator.translate(string, source, target)

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
    __slots__ = ("days", "hours", "minutes", "seconds", "left", "_client", "_language")

    def __init__(self, language, left) -> None:
        self._language: str = language
        self.days: int = left.get("days", 0)
        self.hours: int = left.get("hours", 0)
        self.minutes: int = left.get("minutes", 0)
        self.seconds: int = left.get("seconds", 0)

    # def __str__(self) -> str:
    #     return self.format_string()

    def __repr__(self) -> str:
        return "<TimePeriod days=%s hours=%s minutes=%s seconds=%s>"

    @staticmethod
    def _converter_pt(secs: int) -> str:
        info = {"dia": 86400, "hora": 3600, "minuto": 60, "segundo": 1}
        result = []
        for unit, deli in info.items():
            if secs >= deli:
                amt, secs = divmod(secs, deli)
                add_s = "s" if amt > 1 else ""
                result.append(f"{amt} {unit}{add_s}")
        return ", ".join(result)

    @staticmethod
    def calculate_time(total_secs: float) -> dict:
        info = {"days": 86400, "hours": 3600, "minutes": 60, "seconds": 1}
        result = {}
        for unit, deli in info.items():
            result[unit] = 0
            if total_secs >= deli:
                amt, total_secs = divmod(total_secs, deli)
                result[unit] = int(amt)
        return result

    # def format_string(self) -> str:
    #     info = {
    #         "day": self.days,
    #         "hour": self.hours,
    #         "minute": self.minutes,
    #         "second": self.seconds,
    #     }
    #     result = []
    #     is_pt = self._language == "pt-BR"
    #     for k, v in info.items():
    #         if v:
    #             s = f"{v} {translate(k, is_pt)}"
    #             if v > 1:
    #                 s += "s"
    #             result.append(s)
    #     return ", ".join(result)

    @classmethod
    def after_date(cls, lang: str, date: Date) -> TimePeriod:
        difference = date_now() - date.date
        seconds = difference.total_seconds()
        time_data = cls.calculate_time(seconds)
        return cls(lang, time_data)

    @classmethod
    def until_date(cls, lang: str, date: Date) -> TimePeriod:
        difference = date.date - date_now()
        seconds = difference.total_seconds()
        time_data = cls.calculate_time(seconds)
        return cls(lang, time_data)


class Date:
    def __init__(self, date: datetime.datetime, tz: datetime.tzinfo = None) -> None:
        self.date = date
        self.tz = tz

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return self.date.strftime("%d-%m-%Y %H:%M:%S")

    @classmethod
    def from_string(cls, date_str: str) -> Date:  # todo: refactor this function
        d: datetime.datetime = dateutil.parser.isoparse(date_str)
        return cls(d, datetime.timezone.utc)

    @classmethod
    def from_dict(cls, data: dict, tz: datetime.tzinfo = None) -> Date:
        tz = tz if tz else datetime.timezone.utc
        end_time = date_now() + datetime.timedelta(**data)
        return cls(end_time, tz)

    def to_tz(self, tz: datetime.tzinfo = None) -> Date:
        self.date.replace(tzinfo=self.tz).astimezone(tz)
        return self


class StatInfo:  # possible future stats add
    pass


class NetworkInfo(StatInfo):
    def __init__(self, info: dict):
        self._info = info

    @property
    def download(self) -> str:
        return self._info.get("down", None)

    @property
    def upload(self) -> str:
        return self._info.get("up", None)


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
