import requests

from app.core.config import settings

from app.schemas import CryptobotStatus, CryptobotLogs


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


def get_bot_status(bot_name: str):
    r = requests.get(
        f"{settings.CONTROLLER_URL}/bot/{bot_name}/status",
        headers = {}
    )

    return CryptobotStatus(status=r.json()["status"])


def get_bot_logs(bot_name: str):
    r = requests.get(
        f"{settings.CONTROLLER_URL}/bot/{bot_name}/logs",
        headers = {}
    )

    return CryptobotLogs(logs=r.json()["logs"])
