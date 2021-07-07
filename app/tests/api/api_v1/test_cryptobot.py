from datetime import date, datetime
from dateutil.relativedelta import relativedelta

# from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.utils import random_lower_string, random_weekdays
from app.tests.utils.user import create_random_user
from app.tests.utils.cryptobot import create_random_cryptobot


def test_create_cryptobot_by_admin(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    data = {
        "binance_api_url": "https://api.binance.com",
        "binance_api_key": "xxxxxxxxxxxxxxxxxxx",
        "binance_api_secret": "xxxxxxxxxxxxxxxxxxx",
        "binance_config_base_currency": "BTC",
        "binance_config_quote_currency": "EUR",
        "binance_config_granularity": "15m",
        "binance_config_live": False,
        "binance_config_verbose": True,
        "binance_config_graphs": False,
        "binance_config_buymaxsize": 0.0004,
        "logger_filelog": True,
        "logger_logfile": "pycryptobot.log",
        "logger_fileloglevel": "DEBUG",
        "logger_consolelog": True,
        "logger_consoleloglevel": "INFO",
        "telegram_client_id": "xxxxxx",
        "telegram_token": "xxxxxx",
    }

    response = client.post(
        f"{settings.API_V1_STR}/cryptobots/",
        headers=superuser_token_headers,
        json=data)
    content = response.json()

    assert response.status_code == 200
    assert "id" in content
    assert content["user_id"] == 1
    assert isinstance(content["user"], dict)
    assert content["user"]["id"] == 1
    assert content["user"]["firstname"] == settings.USER_ADMIN_FIRSTNAME
    assert content["user"]["email"] == settings.USER_ADMIN_EMAIL
    assert content["binance_api_url"] == data["binance_api_url"]
    assert content["binance_api_key"] == data["binance_api_key"]
    assert content["binance_api_secret"] == data["binance_api_secret"]
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
    assert content["telegram_client_id"] == data["telegram_client_id"]
    assert content["telegram_token"] == data["telegram_token"]


def test_create_cryptobot_by_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    user_id = r.json()["id"]
    user_firstname = r.json()["firstname"]
    user_email = r.json()["email"]
    
    data = {
        "binance_api_url": "https://api.binance.com",
        "binance_api_key": "xxxxxxxxxxxxxxxxxxx",
        "binance_api_secret": "xxxxxxxxxxxxxxxxxxx",
        "binance_config_base_currency": "BTC",
        "binance_config_quote_currency": "EUR",
        "binance_config_granularity": "15m",
        "binance_config_live": False,
        "binance_config_verbose": True,
        "binance_config_graphs": False,
        "binance_config_buymaxsize": 0.0004,
        "logger_filelog": True,
        "logger_logfile": "pycryptobot.log",
        "logger_fileloglevel": "DEBUG",
        "logger_consolelog": True,
        "logger_consoleloglevel": "INFO",
        "telegram_client_id": "xxxxxx",
        "telegram_token": "xxxxxx",
    }

    response = client.post(
        f"{settings.API_V1_STR}/cryptobots/",
        headers=normal_user_token_headers,
        json=data)
    content = response.json()

    assert response.status_code == 200
    assert "id" in content
    assert content["user_id"] == user_id
    assert isinstance(content["user"], dict)
    assert content["user"]["id"] == user_id
    assert content["user"]["firstname"] == user_firstname
    assert content["user"]["email"] == user_email
    assert content["binance_api_url"] == data["binance_api_url"]
    assert content["binance_api_key"] == data["binance_api_key"]
    assert content["binance_api_secret"] == data["binance_api_secret"]
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
    assert content["telegram_client_id"] == data["telegram_client_id"]
    assert content["telegram_token"] == data["telegram_token"]


def test_read_cryptobot_by_admin(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    user = create_random_user(db)
    cryptobot = create_random_cryptobot(db, user_id=user.id)

    response = client.get(
        f"{settings.API_V1_STR}/cryptobots/{cryptobot.id}",
        headers=superuser_token_headers,
    )
    content = response.json()

    assert response.status_code == 200
    assert "id" in content
    assert "user_id" in content
    assert content["user"]["id"] == user.id
    assert content["user"]["firstname"] == user.firstname
    assert content["user"]["email"] == user.email
    assert content["binance_api_url"] == cryptobot.binance_api_url
    assert content["binance_api_key"] == cryptobot.binance_api_key
    assert content["binance_api_secret"] == cryptobot.binance_api_secret
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
    assert content["telegram_client_id"] == cryptobot.telegram_client_id
    assert content["telegram_token"] == cryptobot.telegram_token


def test_read_cryptobot_by_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    user_id = r.json()["id"]
    
    cryptobot = create_random_cryptobot(db, user_id=user_id)
    
    response = client.get(
        f"{settings.API_V1_STR}/cryptobots/{cryptobot.id}",
        headers=normal_user_token_headers,
    )
    content = response.json()

    assert response.status_code == 200
    assert "id" in content
    # assert "user_id" in content
    # assert content["user"]["id"] == user.id
    # assert content["user"]["firstname"] == user.firstname
    # assert content["user"]["email"] == user.email
    assert content["binance_api_url"] == cryptobot.binance_api_url
    assert content["binance_api_key"] == cryptobot.binance_api_key
    assert content["binance_api_secret"] == cryptobot.binance_api_secret
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
    assert content["telegram_client_id"] == cryptobot.telegram_client_id
    assert content["telegram_token"] == cryptobot.telegram_token


def test_read_cryptobot_by_another_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    cryptobot = create_random_cryptobot(db)
    response = client.get(
        f"{settings.API_V1_STR}/cryptobots/{cryptobot.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400


def test_update_cryptobot_by_admin(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    user = create_random_user(db)
    cryptobot = create_random_cryptobot(db, user_id=user.id)

    data = {
        "binance_api_url": "https://api.binance.com",
        "binance_api_key": "xxxxxxxxxxxxxxxxxxx",
        "binance_api_secret": "xxxxxxxxxxxxxxxxxxx",
        "binance_config_base_currency": "BTC",
        "binance_config_quote_currency": "EUR",
        "binance_config_granularity": "15m",
        "binance_config_live": False,
        "binance_config_verbose": True,
        "binance_config_graphs": False,
        "binance_config_buymaxsize": 0.0004,
        "logger_filelog": True,
        "logger_logfile": "pycryptobot.log",
        "logger_fileloglevel": "DEBUG",
        "logger_consolelog": True,
        "logger_consoleloglevel": "INFO",
        "telegram_client_id": "xxxxxx",
        "telegram_token": "xxxxxx",
    }

    response = client.put(
        f"{settings.API_V1_STR}/cryptobots/{cryptobot.id}",
        headers=superuser_token_headers,
        json=data
    )
    content = response.json()

    assert response.status_code == 200
    assert "id" in content
    # assert content["user_id"] == user_id
    # assert isinstance(content["user"], dict)
    # assert content["user"]["id"] == user_id
    # assert content["user"]["firstname"] == user_firstname
    # assert content["user"]["email"] == user_email
    assert content["binance_api_url"] == data["binance_api_url"]
    assert content["binance_api_key"] == data["binance_api_key"]
    assert content["binance_api_secret"] == data["binance_api_secret"]
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
    assert content["telegram_client_id"] == data["telegram_client_id"]
    assert content["telegram_token"] == data["telegram_token"]


def test_update_cryptobot_by_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    user_id = r.json()["id"]

    cryptobot = create_random_cryptobot(db, user_id=user_id)

    data = {
        "binance_api_url": "https://api.binance.com",
        "binance_api_key": "xxxxxxxxxxxxxxxxxxx",
        "binance_api_secret": "xxxxxxxxxxxxxxxxxxx",
        "binance_config_base_currency": "BTC",
        "binance_config_quote_currency": "EUR",
        "binance_config_granularity": "15m",
        "binance_config_live": False,
        "binance_config_verbose": True,
        "binance_config_graphs": False,
        "binance_config_buymaxsize": 0.0004,
        "logger_filelog": True,
        "logger_logfile": "pycryptobot.log",
        "logger_fileloglevel": "DEBUG",
        "logger_consolelog": True,
        "logger_consoleloglevel": "INFO",
        "telegram_client_id": "xxxxxx",
        "telegram_token": "xxxxxx",
    }

    response = client.put(
        f"{settings.API_V1_STR}/cryptobots/{cryptobot.id}",
        headers=normal_user_token_headers,
        json=data
    )
    content = response.json()

    assert response.status_code == 200
    assert "id" in content
    # assert content["user_id"] == user_id
    # assert isinstance(content["user"], dict)
    # assert content["user"]["id"] == user_id
    # assert content["user"]["firstname"] == user_firstname
    # assert content["user"]["email"] == user_email
    assert content["binance_api_url"] == data["binance_api_url"]
    assert content["binance_api_key"] == data["binance_api_key"]
    assert content["binance_api_secret"] == data["binance_api_secret"]
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
    assert content["telegram_client_id"] == data["telegram_client_id"]
    assert content["telegram_token"] == data["telegram_token"]


def test_update_cryptobot_by_another_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    cryptobot = create_random_cryptobot(db)

    data = {
        "binance_api_url": "https://api.binance.com",
        "binance_api_key": "xxxxxxxxxxxxxxxxxxx",
        "binance_api_secret": "xxxxxxxxxxxxxxxxxxx",
        "binance_config_base_currency": "BTC",
        "binance_config_quote_currency": "EUR",
        "binance_config_granularity": "15m",
        "binance_config_live": False,
        "binance_config_verbose": True,
        "binance_config_graphs": False,
        "binance_config_buymaxsize": 0.0004,
        "logger_filelog": True,
        "logger_logfile": "pycryptobot.log",
        "logger_fileloglevel": "DEBUG",
        "logger_consolelog": True,
        "logger_consoleloglevel": "INFO",
        "telegram_client_id": "xxxxxx",
        "telegram_token": "xxxxxx",
    }

    response = client.put(
        f"{settings.API_V1_STR}/cryptobots/{cryptobot.id}",
        headers=normal_user_token_headers,
        json=data
    )
    
    assert response.status_code == 400


def test_delete_cryptobot_by_admin(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    user = create_random_user(db)
    cryptobot = create_random_cryptobot(db, user_id=user.id)

    response = client.delete(
        f"{settings.API_V1_STR}/cryptobots/{cryptobot.id}",
        headers=superuser_token_headers,
    )
    content = response.json()

    assert response.status_code == 200
    assert "id" in content
    # assert "user_id" in content
    # assert content["user"]["id"] == user.id
    # assert content["user"]["firstname"] == user.firstname
    # assert content["user"]["email"] == user.email
    assert content["binance_api_url"] == cryptobot.binance_api_url
    assert content["binance_api_key"] == cryptobot.binance_api_key
    assert content["binance_api_secret"] == cryptobot.binance_api_secret
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
    assert content["telegram_client_id"] == cryptobot.telegram_client_id
    assert content["telegram_token"] == cryptobot.telegram_token


def test_delete_cryptobot_by_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/users/me",
        headers=normal_user_token_headers)
    user_id = r.json()["id"]
    
    cryptobot = create_random_cryptobot(db, user_id=user_id)

    response = client.delete(
        f"{settings.API_V1_STR}/cryptobots/{cryptobot.id}",
        headers=normal_user_token_headers)
    content = response.json()

    assert response.status_code == 200
    assert "id" in content
    # assert "user_id" in content
    # assert content["user"]["id"] == user.id
    # assert content["user"]["firstname"] == user.firstname
    # assert content["user"]["email"] == user.email
    assert content["binance_api_url"] == cryptobot.binance_api_url
    assert content["binance_api_key"] == cryptobot.binance_api_key
    assert content["binance_api_secret"] == cryptobot.binance_api_secret
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
    assert content["telegram_client_id"] == cryptobot.telegram_client_id
    assert content["telegram_token"] == cryptobot.telegram_token


def test_delete_cryptobot_by_another_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    cryptobot = create_random_cryptobot(db)
    response = client.delete(
        f"{settings.API_V1_STR}/cryptobots/{cryptobot.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
