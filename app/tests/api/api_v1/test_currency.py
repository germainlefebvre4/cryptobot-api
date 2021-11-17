from datetime import date, datetime
from dateutil.relativedelta import relativedelta

# from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.utils import random_lower_string, random_weekdays
from app.tests.utils.user import create_random_user
from app.tests.utils.currency import get_random_exchange_currency


def test_create_currency(
    client: TestClient, normal_user_token_headers: dict,
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    user_id = r.json()["id"]

    base_currency, quote_currency = get_random_exchange_currency()
    data = {
        "base_currency": base_currency,
        "quote_currency": quote_currency,
    }

    response = client.post(
        f"{settings.API_V1_STR}/margin/currencies/?" + \
        f"&user_id={user_id}",
        headers=normal_user_token_headers,
        json=data,
    )
    content = response.json()

    assert response.status_code == 200
    assert "id" in content
    assert content["base_currency"] == base_currency
    assert content["quote_currency"] == quote_currency


def test_read_currencies_by_user(
    client: TestClient, normal_user_token_headers: dict,
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    user_id = r.json()["id"]
    
    response = client.get(
        f"{settings.API_V1_STR}/margin/currencies/?" + \
        f"&user_id={user_id}",
        headers=normal_user_token_headers,
    )
    content = response.json()

    assert response.status_code == 200
    assert isinstance(content, list)


def test_read_currency_by_id_by_user(
    client: TestClient, normal_user_token_headers: dict,
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    user_id = r.json()["id"]

    base_currency, quote_currency = get_random_exchange_currency()
    data = {
        "base_currency": base_currency,
        "quote_currency": quote_currency,
    }

    response = client.post(
        f"{settings.API_V1_STR}/margin/currencies/?" + \
        f"&user_id={user_id}",
        headers=normal_user_token_headers,
        json=data,
    )
    content = response.json()
    assert response.status_code == 200

    currency_id = content['id']


    response = client.get(
        f"{settings.API_V1_STR}/margin/currencies/{currency_id}?" + \
        f"&user_id={user_id}",
        headers=normal_user_token_headers,
    )
    content = response.json()

    assert response.status_code == 200
    assert "id" in content
    assert content["base_currency"] == base_currency
    assert content["quote_currency"] == quote_currency
