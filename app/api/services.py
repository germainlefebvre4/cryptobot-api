import requests

from app.core.config import settings

from app.schemas import CryptobotStatus, CryptobotLogs, CryptobotVersion, CryptobotMargin, Cryptobot

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

def get_bot_margin(bot_name: str, currency_pair: str, cryptobot: Cryptobot):
    # Connect Binance API
    client = Client(cryptobot.binance_account.binance_api_key, cryptobot.binance_account.binance_api_secret)

    # # Get recent trades
    last_trade = client.get_my_trades(
        symbol=currency_pair,
        limit=1,
    )
    # del last_trade[-1]
    if len(last_trade) > 0:
        if last_trade[0]['isBuyer']:
            # Get last buy price in quote currency
            last_trade_quote_price = float(last_trade[0]['price'])
            # Get current price in quote currency
            current_quote_price = float(client.get_symbol_ticker(symbol=currency_pair)['price'])
            # Get current margin in quote currency
            quote_margin = '{:.4f}'.format((current_quote_price - last_trade_quote_price) / last_trade_quote_price)

            return CryptobotMargin(margin=quote_margin)

    return CryptobotMargin()
