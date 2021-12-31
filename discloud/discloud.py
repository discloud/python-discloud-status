from __future__ import annotations
import enum
from .client import UserClient


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
    def __init__(self, client: UserClient, data: dict) -> None:
        self.client = client
        self.type: PlanType = PlanType[data['plan']]
        self.expires_in = ...  # todo
        self.expire_date = ...  # todo

    def __str__(self) -> str:  # todo
        if self.client.language == "pt":
            return PT_TRANSLATIONS.get(self.type.name, self.type.name)
        return self.type.name

    def __repr__(self) -> str:
        return "<Plan type=%s>" % self.type


class DisCloudUser:
    def __init__(self, client, data: dict) -> None:
        self.client = client
        self.id = int(data['userID'])
        self.plan = Plan(client, data['plan'])

