import requests

from app.core.config import settings


def create_operator_bot(data: dict):
    r = requests.post(
        f"{settings.CONTROLLER_URL}/operator/bot/",
        json = data,
        headers = {}
    )

    return r.json()


def get_operator_bot(bot_name: str):
    r = requests.get(
        f"{settings.CONTROLLER_URL}/operator/bot/{bot_name}",
        headers = {}
    )

    return r.json()


def update_operator_bot(bot_name: str, data: dict):
    r = requests.put(
        f"{settings.CONTROLLER_URL}/operator/bot/{bot_name}",
        json = data,
        headers = {}
    )

    return r.json()


def delete_operator_bot(bot_name: str):
    r = requests.delete(
        f"{settings.CONTROLLER_URL}/operator/bot/{bot_name}",
        headers = {}
    )

    return r.json()