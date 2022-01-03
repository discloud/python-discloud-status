from __future__ import annotations
import enum

from .utils import TimePeriod, FutureDate


PT_TRANSLATIONS = {
    "Free": "Grátis",
    "Platinum": "Platina",
    "Diamond": "Diamante",
    "Sapphire": "Safíra"
}


class PlanType(enum.Enum):
    Free = 0
    Carbon = 3
    Gold = 1
    Platinum = 2
    Diamond = 4
    # Ruby = 5 todo: v2 release
    Sapphire = 6
    # Krypton = 7 todo: v2 release


class Plan:
    def __init__(self, data: dict) -> None:
        self.type: PlanType = PlanType[data['plan']]
        self.lifetime = data.get('planDataEnd') == "Lifetime"
        self.language: str = data['lang']
        if self.lifetime:
            self.expires_in = "never"
            if self.language == "pt":
                self.expires_in = "nunca"
            self.expire_date = None

        else:
            self.expire_date: FutureDate = FutureDate.from_dict(data['lastDataLeft'])
            self.expires_in: TimePeriod = TimePeriod(data)

    def __str__(self) -> str:  # todo
        if self.language == "pt":
            return PT_TRANSLATIONS.get(self.type.name, self.type.name)
        return self.type.name

    def __repr__(self) -> str:
        return "<Plan type=%s>" % self.type


class DisCloudUser:
    def __init__(self, data: dict) -> None:
        self.id = int(data['userID'])
        self.plan = Plan(data)

