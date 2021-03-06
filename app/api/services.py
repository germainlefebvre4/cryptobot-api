import requests
from app import schemas
from numpy import average

from fastapi import HTTPException

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
    try:
        r = requests.get(
            f"{settings.CONTROLLER_URL}/operator/bot/{bot_name}",
            headers = {}
        )
    except:
        raise HTTPException(status_code=404, detail="An error occured on retrieving bot informations")


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
    try:
        r = requests.get(
            f"{settings.CONTROLLER_URL}/bot/{bot_name}/status",
            headers = {}
        )
    except:
        raise HTTPException(status_code=404, detail="An error occured on retrieving bot status")


    return CryptobotStatus(status=r.json()["status"])


def get_bot_logs(bot_name: str):
    try:
        r = requests.get(
            f"{settings.CONTROLLER_URL}/bot/{bot_name}/logs",
            headers = {}
        )
    except:
        raise HTTPException(status_code=404, detail="An error occured on retrieving bot logs")


    bot_logs = r.json()["logs"].replace('\n', '<br>').replace(' ', '&nbsp;')

    return CryptobotLogs(logs=bot_logs)


def get_bot_version(bot_name: str):
    try:
        r = requests.get(
            f"{settings.CONTROLLER_URL}/bot/{bot_name}/version",
            headers = {}
        )
    except:
        raise HTTPException(status_code=404, detail="An error occured on retrieving bot version")


    return CryptobotVersion(version=r.json()["version"])


def get_bot_margin_trades_current_last(base_currency: str, quote_currency: str, user_id: int):
    try:
        r = requests.get(
            f"{settings.MARGIN_URL}/trades/currencies/{base_currency}/{quote_currency}/current/last" + \
                f"?user_id={user_id}",
            headers = {}
        )
    except:
        raise HTTPException(status_code=404, detail="An error occured on retrieving last trade margin")


    return r.json()


def get_bot_margin_trades_current_run(base_currency: str, quote_currency: str, user_id: int):
    try:
        r = requests.get(
            f"{settings.MARGIN_URL}/trades/currencies/{base_currency}/{quote_currency}/current/run" + \
                f"?user_id={user_id}",
            headers = {}
        )
    except:
        raise HTTPException(status_code=404, detail="An error occured on retrieving current run margin")


    return r.json()


def get_currencies(user_id: int, skip: int, limit: int):
    try:
        r = requests.get(
            f"{settings.MARGIN_URL}/currencies/?" + \
                f"&skip={skip}" + \
                f"&limit={limit}" + \
                f"&user_id={user_id}",
            headers = {}
        )
    except:
        raise HTTPException(status_code=404, detail="An error occured on retrieving margin currencies")


    return r.json()


def create_currency(user_id: int, currency_in: schemas.CurrencyCreate):
    try:
        r = requests.post(
            f"{settings.MARGIN_URL}/currencies/?" + \
            f"&user_id={user_id}",
            headers = {},
            json = dict(currency_in),
        )
    except:
        raise HTTPException(status_code=404, detail="An error occured on creating margin currency")


    if r.status_code == 200:
        return r.json()
    else:
        raise HTTPException(status_code=r.status_code, detail="En error occured")


def get_currency_by_id(user_id: int, currency_id: int):
    try:
        r = requests.get(
            f"{settings.MARGIN_URL}/currencies/{currency_id}?" + \
            f"&user_id={user_id}",
            headers = {}
        )
    except:
        raise HTTPException(status_code=404, detail="An error occured on retrieving currency by id")

    if r.status_code == 200:
        return r.json()
    elif r.status_code == 404:
        return None
    else:
        raise HTTPException(status_code=404, detail="Currency not found")


def delete_currency_by_id(user_id: int, currency_id: int):
    r = requests.delete(
        f"{settings.MARGIN_URL}/currencies/{currency_id}?" + \
        f"&user_id={user_id}",
        headers = {}
    )

    if r.status_code == 200:
        return r.json()
    else:
        raise HTTPException(status_code=r.status_code, detail="En error occured")


def get_currencies_margin_trades(user_id: int, skip: int, limit: int):
    try:
        r = requests.get(
            f"{settings.MARGIN_URL}/margin/trades" + \
            f"?user_id={user_id}",
            headers = {}
        )
    except:
        raise HTTPException(status_code=404, detail="An error occured on retrieving currencies margin trades")


    return r.json()


def get_last_user_trade(base_currency: str, quote_currency: str, user_id: int):
    try:
        r = requests.get(
            f"{settings.BINANCE_URL}/trades/{base_currency}/{quote_currency}/last" + \
                "?user_id=" + str(user_id),
        )
    except:
        return None
        raise HTTPException(status_code=404, detail="An error occured on retrieving last trades")

    if r.status_code == 200:
        return r.json()
    else:
        return None
        raise Exception(f"Error getting current price for {base_currency}/{quote_currency}")


def get_last_user_trade_event(base_currency: str, quote_currency: str, user_id: int):
    res = get_last_user_trade(base_currency, quote_currency, user_id)
    if res:
        if res["isBuyer"]:
            return "BUY"
        else:
            return "SELL"
