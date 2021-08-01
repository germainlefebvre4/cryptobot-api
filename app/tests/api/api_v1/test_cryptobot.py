from datetime import date, datetime
from dateutil.relativedelta import relativedelta

# from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.utils import random_lower_string, random_weekdays
from app.tests.utils.user import create_random_user
from app.tests.utils.cryptobot import create_random_cryptobot
from app.tests.utils.binance_account import create_random_binance_account
from app.tests.utils.telegram import create_random_telegram

from app.tests.mock import mock_output


def test_create_cryptobot_by_admin(
    client: TestClient, monkeypatch, superuser_token_headers: dict, db: Session
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/users/me",
        headers=superuser_token_headers)
    user_id = r.json()["id"]

    binance_account = create_random_binance_account(db, user_id=user_id)
    telegram = create_random_telegram(db, user_id=user_id)

    data = {
        "binance_config_base_currency": "BTC",
        "binance_config_quote_currency": "EUR",
        "binance_config_granularity": "15m",
        "binance_config_live": False,
        "binance_config_verbose": True,
        "binance_config_graphs": False,
        "binance_config_buymaxsize": 0.0004,
        "binance_config_sellupperpcnt": -10,
        "binance_config_selllowerpcnt": 10,
        "logger_filelog": True,
        "logger_logfile": "pycryptobot.log",
        "logger_fileloglevel": "DEBUG",
        "logger_consolelog": True,
        "logger_consoleloglevel": "INFO",
    }

    monkeypatch.setattr("app.api.services.create_operator_bot", mock_output({"msg": "ok"}))
    response = client.post(
        f"{settings.API_V1_STR}/cryptobots/" + \
            f"?binance_account_id={binance_account.id}" + \
            f"&telegram_id={telegram.id}",
        headers=superuser_token_headers,
        json=data)
    content = response.json()

    assert response.status_code == 200
    assert "id" in content
    assert isinstance(content["binance_account"], dict)
    assert content["binance_account"]["binance_api_url"] == "https://api.binance.com"
    assert content["binance_account"]["binance_api_key"] == binance_account.binance_api_key
    assert content["binance_account"]["binance_api_secret"] == binance_account.binance_api_secret
    assert content["telegram"]["client_id"] == telegram.client_id
    assert content["telegram"]["token"] == telegram.token
    assert content["binance_config_base_currency"] == data["binance_config_base_currency"]
    assert content["binance_config_quote_currency"] == data["binance_config_quote_currency"]
    assert content["binance_config_granularity"] == data["binance_config_granularity"]
    assert content["binance_config_live"] == data["binance_config_live"]
    assert content["binance_config_verbose"] == data["binance_config_verbose"]
    assert content["binance_config_graphs"] == data["binance_config_graphs"]
    assert content["binance_config_buymaxsize"] == data["binance_config_buymaxsize"]
    assert content["logger_filelog"] == data["logger_filelog"]
    assert content["logger_logfile"] == data["logger_logfile"]
    assert content["logger_fileloglevel"] == data["logger_fileloglevel"]
    assert content["logger_consolelog"] == data["logger_consolelog"]
    assert content["logger_consoleloglevel"] == data["logger_consoleloglevel"]


def test_create_cryptobot_by_user(
    client: TestClient, monkeypatch, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/users/me",
        headers=normal_user_token_headers)
    user_id = r.json()["id"]

    binance_account = create_random_binance_account(db, user_id=user_id)
    telegram = create_random_telegram(db, user_id=user_id)
    
    data = {
        "binance_config_base_currency": "BTC",
        "binance_config_quote_currency": "EUR",
        "binance_config_granularity": "15m",
        "binance_config_live": False,
        "binance_config_verbose": True,
        "binance_config_graphs": False,
        "binance_config_buymaxsize": 0.0004,
        "binance_config_sellupperpcnt": -10,
        "binance_config_selllowerpcnt": 10,
        "logger_filelog": True,
        "logger_logfile": "pycryptobot.log",
        "logger_fileloglevel": "DEBUG",
        "logger_consolelog": True,
        "logger_consoleloglevel": "INFO",
    }

    monkeypatch.setattr("app.api.services.create_operator_bot", mock_output({"msg": "ok"}))
    response = client.post(
        f"{settings.API_V1_STR}/cryptobots/" + \
            f"?binance_account_id={binance_account.id}" + \
            f"&telegram_id={telegram.id}",
        headers=normal_user_token_headers,
        json=data)
    content = response.json()

    assert response.status_code == 200
    assert "id" in content
    assert content["binance_account"]["binance_api_url"] == binance_account.binance_api_url
    assert content["binance_account"]["binance_api_key"] == binance_account.binance_api_key
    assert content["binance_account"]["binance_api_secret"] == binance_account.binance_api_secret
    assert content["telegram"]["client_id"] == telegram.client_id
    assert content["telegram"]["token"] == telegram.token
    assert content["binance_config_base_currency"] == data["binance_config_base_currency"]
    assert content["binance_config_quote_currency"] == data["binance_config_quote_currency"]
    assert content["binance_config_granularity"] == data["binance_config_granularity"]
    assert content["binance_config_live"] == data["binance_config_live"]
    assert content["binance_config_verbose"] == data["binance_config_verbose"]
    assert content["binance_config_graphs"] == data["binance_config_graphs"]
    assert content["binance_config_buymaxsize"] == data["binance_config_buymaxsize"]
    assert content["logger_filelog"] == data["logger_filelog"]
    assert content["logger_logfile"] == data["logger_logfile"]
    assert content["logger_fileloglevel"] == data["logger_fileloglevel"]
    assert content["logger_consolelog"] == data["logger_consolelog"]
    assert content["logger_consoleloglevel"] == data["logger_consoleloglevel"]


def test_read_cryptobot_by_admin(
    client: TestClient, monkeypatch, superuser_token_headers: dict, db: Session
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/users/me",
        headers=superuser_token_headers)
    user_id = r.json()["id"]

    binance_account = create_random_binance_account(db, user_id=user_id)
    telegram = create_random_telegram(db, user_id=user_id)
    cryptobot = create_random_cryptobot(db, user_id=user_id, binance_account_id=binance_account.id, telegram_id=telegram.id)

    monkeypatch.setattr("app.api.services.get_operator_bot", mock_output({"msg": "ok"}))
    response = client.get(
        f"{settings.API_V1_STR}/cryptobots/{cryptobot.id}",
        headers=superuser_token_headers,
    )
    content = response.json()

    assert response.status_code == 200
    assert "id" in content
    assert content["binance_account"]["binance_api_url"] == binance_account.binance_api_url
    assert content["binance_account"]["binance_api_key"] == binance_account.binance_api_key
    assert content["binance_account"]["binance_api_secret"] == binance_account.binance_api_secret
    assert content["telegram"]["client_id"] == telegram.client_id
    assert content["telegram"]["token"] == telegram.token
    assert content["binance_config_base_currency"] == cryptobot.binance_config_base_currency
    assert content["binance_config_quote_currency"] == cryptobot.binance_config_quote_currency
    assert content["binance_config_granularity"] == cryptobot.binance_config_granularity
    assert content["binance_config_live"] == cryptobot.binance_config_live
    assert content["binance_config_verbose"] == cryptobot.binance_config_verbose
    assert content["binance_config_graphs"] == cryptobot.binance_config_graphs
    assert content["binance_config_buymaxsize"] == cryptobot.binance_config_buymaxsize
    assert content["logger_filelog"] == cryptobot.logger_filelog
    assert content["logger_logfile"] == cryptobot.logger_logfile
    assert content["logger_fileloglevel"] == cryptobot.logger_fileloglevel
    assert content["logger_consolelog"] == cryptobot.logger_consolelog
    assert content["logger_consoleloglevel"] == cryptobot.logger_consoleloglevel


def test_read_cryptobot_by_user(
    client: TestClient, monkeypatch, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/users/me",
        headers=normal_user_token_headers)
    user_id = r.json()["id"]

    binance_account = create_random_binance_account(db, user_id=user_id)
    telegram = create_random_telegram(db, user_id=user_id)
    cryptobot = create_random_cryptobot(db, user_id=user_id, binance_account_id=binance_account.id, telegram_id=telegram.id)
    
    monkeypatch.setattr("app.api.services.get_operator_bot", mock_output({"msg": "ok"}))
    response = client.get(
        f"{settings.API_V1_STR}/cryptobots/{cryptobot.id}",
        headers=normal_user_token_headers,
    )
    content = response.json()

    assert response.status_code == 200
    assert "id" in content
    assert content["binance_account"]["binance_api_url"] == binance_account.binance_api_url
    assert content["binance_account"]["binance_api_key"] == binance_account.binance_api_key
    assert content["binance_account"]["binance_api_secret"] == binance_account.binance_api_secret
    assert content["telegram"]["client_id"] == telegram.client_id
    assert content["telegram"]["token"] == telegram.token
    assert content["binance_config_base_currency"] == cryptobot.binance_config_base_currency
    assert content["binance_config_quote_currency"] == cryptobot.binance_config_quote_currency
    assert content["binance_config_granularity"] == cryptobot.binance_config_granularity
    assert content["binance_config_live"] == cryptobot.binance_config_live
    assert content["binance_config_verbose"] == cryptobot.binance_config_verbose
    assert content["binance_config_graphs"] == cryptobot.binance_config_graphs
    assert content["binance_config_buymaxsize"] == cryptobot.binance_config_buymaxsize
    assert content["logger_filelog"] == cryptobot.logger_filelog
    assert content["logger_logfile"] == cryptobot.logger_logfile
    assert content["logger_fileloglevel"] == cryptobot.logger_fileloglevel
    assert content["logger_consolelog"] == cryptobot.logger_consolelog
    assert content["logger_consoleloglevel"] == cryptobot.logger_consoleloglevel


def test_read_cryptobot_by_another_user(
    client: TestClient, monkeypatch, normal_user_token_headers: dict, db: Session
) -> None:
    user = create_random_user(db)
    binance_account = create_random_binance_account(db, user_id=user.id)
    telegram = create_random_telegram(db, user_id=user.id)
    cryptobot = create_random_cryptobot(db, user_id=user.id, binance_account_id=binance_account.id, telegram_id=telegram.id)

    monkeypatch.setattr("app.api.services.get_operator_bot", mock_output({"msg": "ok"}))
    response = client.get(
        f"{settings.API_V1_STR}/cryptobots/{cryptobot.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400


def test_update_cryptobot_by_admin(
    client: TestClient, monkeypatch, superuser_token_headers: dict, db: Session
) -> None:
    user = create_random_user(db)
    binance_account = create_random_binance_account(db, user_id=user.id)
    telegram = create_random_telegram(db, user_id=user.id)
    cryptobot = create_random_cryptobot(db, user_id=user.id, binance_account_id=binance_account.id, telegram_id=telegram.id)

    data = {
        "binance_config_base_currency": "BTC",
        "binance_config_quote_currency": "EUR",
        "binance_config_granularity": "15m",
        "binance_config_live": False,
        "binance_config_verbose": True,
        "binance_config_graphs": False,
        "binance_config_buymaxsize": 0.0004,
        "binance_config_sellupperpcnt": -10,
        "binance_config_selllowerpcnt": 10,
        "logger_filelog": True,
        "logger_logfile": "pycryptobot.log",
        "logger_fileloglevel": "DEBUG",
        "logger_consolelog": True,
        "logger_consoleloglevel": "INFO",
    }

    monkeypatch.setattr("app.api.services.update_operator_bot", mock_output({"msg": "ok"}))
    response = client.put(
        f"{settings.API_V1_STR}/cryptobots/{cryptobot.id}",
        headers=superuser_token_headers,
        json=data
    )
    content = response.json()

    assert response.status_code == 200
    assert "id" in content
    assert content["binance_account"]["binance_api_url"] == binance_account.binance_api_url
    assert content["binance_account"]["binance_api_key"] == binance_account.binance_api_key
    assert content["binance_account"]["binance_api_secret"] == binance_account.binance_api_secret
    assert content["telegram"]["client_id"] == telegram.client_id
    assert content["telegram"]["token"] == telegram.token
    assert content["binance_config_base_currency"] == data["binance_config_base_currency"]
    assert content["binance_config_quote_currency"] == data["binance_config_quote_currency"]
    assert content["binance_config_granularity"] == data["binance_config_granularity"]
    assert content["binance_config_live"] == data["binance_config_live"]
    assert content["binance_config_verbose"] == data["binance_config_verbose"]
    assert content["binance_config_graphs"] == data["binance_config_graphs"]
    assert content["binance_config_buymaxsize"] == data["binance_config_buymaxsize"]
    assert content["logger_filelog"] == data["logger_filelog"]
    assert content["logger_logfile"] == data["logger_logfile"]
    assert content["logger_fileloglevel"] == data["logger_fileloglevel"]
    assert content["logger_consolelog"] == data["logger_consolelog"]
    assert content["logger_consoleloglevel"] == data["logger_consoleloglevel"]


def test_update_cryptobot_by_user(
    client: TestClient, monkeypatch, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/users/me",
        headers=normal_user_token_headers)
    user_id = r.json()["id"]

    binance_account = create_random_binance_account(db, user_id=user_id)
    telegram = create_random_telegram(db, user_id=user_id)
    cryptobot = create_random_cryptobot(db, user_id=user_id, binance_account_id=binance_account.id, telegram_id=telegram.id)

    data = {
        "binance_config_base_currency": "BTC",
        "binance_config_quote_currency": "EUR",
        "binance_config_granularity": "15m",
        "binance_config_live": False,
        "binance_config_verbose": True,
        "binance_config_graphs": False,
        "binance_config_buymaxsize": 0.0004,
        "binance_config_sellupperpcnt": -10,
        "binance_config_selllowerpcnt": 10,
        "logger_filelog": True,
        "logger_logfile": "pycryptobot.log",
        "logger_fileloglevel": "DEBUG",
        "logger_consolelog": True,
        "logger_consoleloglevel": "INFO",
    }

    monkeypatch.setattr("app.api.services.update_operator_bot", mock_output({"msg": "ok"}))
    response = client.put(
        f"{settings.API_V1_STR}/cryptobots/{cryptobot.id}",
        headers=normal_user_token_headers,
        json=data
    )
    content = response.json()

    assert response.status_code == 200
    assert "id" in content
    assert content["binance_account"]["binance_api_url"] == binance_account.binance_api_url
    assert content["binance_account"]["binance_api_key"] == binance_account.binance_api_key
    assert content["binance_account"]["binance_api_secret"] == binance_account.binance_api_secret
    assert content["telegram"]["client_id"] == telegram.client_id
    assert content["telegram"]["token"] == telegram.token
    assert content["binance_config_base_currency"] == data["binance_config_base_currency"]
    assert content["binance_config_quote_currency"] == data["binance_config_quote_currency"]
    assert content["binance_config_granularity"] == data["binance_config_granularity"]
    assert content["binance_config_live"] == data["binance_config_live"]
    assert content["binance_config_verbose"] == data["binance_config_verbose"]
    assert content["binance_config_graphs"] == data["binance_config_graphs"]
    assert content["binance_config_buymaxsize"] == data["binance_config_buymaxsize"]
    assert content["logger_filelog"] == data["logger_filelog"]
    assert content["logger_logfile"] == data["logger_logfile"]
    assert content["logger_fileloglevel"] == data["logger_fileloglevel"]
    assert content["logger_consolelog"] == data["logger_consolelog"]
    assert content["logger_consoleloglevel"] == data["logger_consoleloglevel"]


def test_update_cryptobot_by_another_user(
    client: TestClient, monkeypatch, normal_user_token_headers: dict, db: Session
) -> None:
    user = create_random_user(db)
    binance_account = create_random_binance_account(db, user_id=user.id)
    telegram = create_random_telegram(db, user_id=user.id)
    cryptobot = create_random_cryptobot(db, user_id=user.id, binance_account_id=binance_account.id, telegram_id=telegram.id)

    data = {
        "binance_config_base_currency": "BTC",
        "binance_config_quote_currency": "EUR",
        "binance_config_granularity": "15m",
        "binance_config_live": False,
        "binance_config_verbose": True,
        "binance_config_graphs": False,
        "binance_config_buymaxsize": 0.0004,
        "binance_config_sellupperpcnt": -10,
        "binance_config_selllowerpcnt": 10,
        "logger_filelog": True,
        "logger_logfile": "pycryptobot.log",
        "logger_fileloglevel": "DEBUG",
        "logger_consolelog": True,
        "logger_consoleloglevel": "INFO",
    }

    monkeypatch.setattr("app.api.services.update_operator_bot", mock_output({"msg": "ok"}))
    response = client.put(
        f"{settings.API_V1_STR}/cryptobots/{cryptobot.id}",
        headers=normal_user_token_headers,
        json=data
    )
    
    assert response.status_code == 400


def test_delete_cryptobot_by_admin(
    client: TestClient, monkeypatch, superuser_token_headers: dict, db: Session
) -> None:
    user = create_random_user(db)
    binance_account = create_random_binance_account(db, user_id=user.id)
    telegram = create_random_telegram(db, user_id=user.id)
    cryptobot = create_random_cryptobot(db, user_id=user.id, binance_account_id=binance_account.id, telegram_id=telegram.id)

    monkeypatch.setattr("app.api.services.delete_operator_bot", mock_output({"msg": "ok"}))
    response = client.delete(
        f"{settings.API_V1_STR}/cryptobots/{cryptobot.id}",
        headers=superuser_token_headers,
    )
    content = response.json()

    assert response.status_code == 200
    assert "id" in content
    assert content["binance_config_base_currency"] == cryptobot.binance_config_base_currency
    assert content["binance_config_quote_currency"] == cryptobot.binance_config_quote_currency
    assert content["binance_config_granularity"] == cryptobot.binance_config_granularity
    assert content["binance_config_live"] == cryptobot.binance_config_live
    assert content["binance_config_verbose"] == cryptobot.binance_config_verbose
    assert content["binance_config_graphs"] == cryptobot.binance_config_graphs
    assert content["binance_config_buymaxsize"] == cryptobot.binance_config_buymaxsize
    assert content["logger_filelog"] == cryptobot.logger_filelog
    assert content["logger_logfile"] == cryptobot.logger_logfile
    assert content["logger_fileloglevel"] == cryptobot.logger_fileloglevel
    assert content["logger_consolelog"] == cryptobot.logger_consolelog
    assert content["logger_consoleloglevel"] == cryptobot.logger_consoleloglevel


def test_delete_cryptobot_by_user(
    client: TestClient, monkeypatch, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/users/me",
        headers=normal_user_token_headers)
    user_id = r.json()["id"]
    
    binance_account = create_random_binance_account(db, user_id=user_id)
    telegram = create_random_telegram(db, user_id=user_id)
    cryptobot = create_random_cryptobot(db, user_id=user_id, binance_account_id=binance_account.id, telegram_id=telegram.id)

    monkeypatch.setattr("app.api.services.delete_operator_bot", mock_output({"msg": "ok"}))
    response = client.delete(
        f"{settings.API_V1_STR}/cryptobots/{cryptobot.id}",
        headers=normal_user_token_headers)
    content = response.json()

    assert response.status_code == 200
    assert "id" in content
    assert content["binance_config_base_currency"] == cryptobot.binance_config_base_currency
    assert content["binance_config_quote_currency"] == cryptobot.binance_config_quote_currency
    assert content["binance_config_granularity"] == cryptobot.binance_config_granularity
    assert content["binance_config_live"] == cryptobot.binance_config_live
    assert content["binance_config_verbose"] == cryptobot.binance_config_verbose
    assert content["binance_config_graphs"] == cryptobot.binance_config_graphs
    assert content["binance_config_buymaxsize"] == cryptobot.binance_config_buymaxsize
    assert content["logger_filelog"] == cryptobot.logger_filelog
    assert content["logger_logfile"] == cryptobot.logger_logfile
    assert content["logger_fileloglevel"] == cryptobot.logger_fileloglevel
    assert content["logger_consolelog"] == cryptobot.logger_consolelog
    assert content["logger_consoleloglevel"] == cryptobot.logger_consoleloglevel


def test_delete_cryptobot_by_another_user(
    client: TestClient, monkeypatch, normal_user_token_headers: dict, db: Session
) -> None:
    user = create_random_user(db)
    binance_account = create_random_binance_account(db, user_id=user.id)
    telegram = create_random_telegram(db, user_id=user.id)
    cryptobot = create_random_cryptobot(db, user_id=user.id, binance_account_id=binance_account.id, telegram_id=telegram.id)
    
    monkeypatch.setattr("app.api.services.delete_operator_bot", mock_output({"msg": "ok"}))
    response = client.delete(
        f"{settings.API_V1_STR}/cryptobots/{cryptobot.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
