import requests
from numpy import average

from app.core.config import settings

from app.schemas import (
    Cryptobot,
    CryptobotStatus, CryptobotLogs, CryptobotVersion,
    CryptobotMargin, CryptobotMarginTradeLast,
)

from binance.client import Client


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

    bot_logs = r.json()["logs"].replace('\n', '<br>').replace(' ', '&nbsp;')

    return CryptobotLogs(logs=bot_logs)


def get_bot_version(bot_name: str):
    r = requests.get(
        f"{settings.CONTROLLER_URL}/bot/{bot_name}/version",
        headers = {}
    )

    return CryptobotVersion(version=r.json()["version"])


def get_bot_margin_trades_current_last(base_currency: str, quote_currency: str, user_id: int):
    r = requests.get(
        f"{settings.MARGIN_URL}/margin/currencies/{base_currency}/{quote_currency}/trades/current/last" + \
            f"?user_id={user_id}",
        headers = {}
    )

    return r.json()


def get_bot_margin_trades_current_run(base_currency: str, quote_currency: str, user_id: int):
    r = requests.get(
        f"{settings.MARGIN_URL}/margin/currencies/{base_currency}/{quote_currency}/trades/current/run" + \
            f"?user_id={user_id}",
        headers = {}
    )

    return r.json()
