from datetime import date, datetime
from dateutil.relativedelta import relativedelta

# from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.utils import random_lower_string, random_weekdays
from app.tests.utils.user import create_random_user
from app.tests.utils.binance_account import create_random_binance_account


def test_create_binance_account_by_admin(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    data = {
        "binance_api_key": random_lower_string(),
        "binance_api_secret": random_lower_string(),
    }

    response = client.post(
        f"{settings.API_V1_STR}/binance/accounts/",
        headers=superuser_token_headers,
        json=data)
    content = response.json()

    assert response.status_code == 200
    assert "id" in content
    assert content["binance_api_url"] == "https://api.binance.com"
    assert content["binance_api_key"] == data["binance_api_key"]
    assert content["binance_api_secret"] == data["binance_api_secret"]


def test_create_binance_account_by_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    user_id = r.json()["id"]
    user_firstname = r.json()["firstname"]
    user_email = r.json()["email"]
    
    data = {
        "binance_api_key": random_lower_string(),
        "binance_api_secret": random_lower_string(),
    }

    response = client.post(
        f"{settings.API_V1_STR}/binance/accounts/",
        headers=normal_user_token_headers,
        json=data)
    content = response.json()

    assert response.status_code == 200
    assert "id" in content
    assert content["binance_api_url"] == "https://api.binance.com"
    assert content["binance_api_key"] == data["binance_api_key"]
    assert content["binance_api_secret"] == data["binance_api_secret"]


def test_read_binance_account_by_admin(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    user = create_random_user(db)
    binance_account = create_random_binance_account(db, user_id=user.id)

    response = client.get(
        f"{settings.API_V1_STR}/binance/accounts/{binance_account.id}",
        headers=superuser_token_headers,
    )
    content = response.json()

    assert response.status_code == 200
    assert "id" in content
    assert content["binance_api_url"] == binance_account.binance_api_url
    assert content["binance_api_key"] == binance_account.binance_api_key
    assert content["binance_api_secret"] == binance_account.binance_api_secret


def test_read_binance_account_by_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    user_id = r.json()["id"]
    
    binance_account = create_random_binance_account(db, user_id=user_id)
    
    response = client.get(
        f"{settings.API_V1_STR}/binance/accounts/{binance_account.id}",
        headers=normal_user_token_headers,
    )
    content = response.json()

    assert response.status_code == 200
    assert "id" in content
    assert content["binance_api_url"] == binance_account.binance_api_url
    assert content["binance_api_key"] == binance_account.binance_api_key
    assert content["binance_api_secret"] == binance_account.binance_api_secret


def test_read_binance_account_by_another_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    binance_account = create_random_binance_account(db)
    response = client.get(
        f"{settings.API_V1_STR}/binance/accounts/{binance_account.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400


def test_update_binance_account_by_admin(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    user = create_random_user(db)
    binance_account = create_random_binance_account(db, user_id=user.id)

    data = {
        "binance_api_key": random_lower_string(),
        "binance_api_secret": random_lower_string(),
    }

    response = client.put(
        f"{settings.API_V1_STR}/binance/accounts/{binance_account.id}",
        headers=superuser_token_headers,
        json=data
    )
    content = response.json()

    assert response.status_code == 200
    assert "id" in content
    assert content["binance_api_url"] == "https://api.binance.com"
    assert content["binance_api_key"] == data["binance_api_key"]
    assert content["binance_api_secret"] == data["binance_api_secret"]


def test_update_binance_account_by_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    user_id = r.json()["id"]

    binance_account = create_random_binance_account(db, user_id=user_id)

    data = {
        "binance_api_key": random_lower_string(),
        "binance_api_secret": random_lower_string(),
    }

    response = client.put(
        f"{settings.API_V1_STR}/binance/accounts/{binance_account.id}",
        headers=normal_user_token_headers,
        json=data
    )
    content = response.json()

    assert response.status_code == 200
    assert "id" in content
    assert content["binance_api_url"] == "https://api.binance.com"
    assert content["binance_api_key"] == data["binance_api_key"]
    assert content["binance_api_secret"] == data["binance_api_secret"]


def test_update_binance_account_by_another_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    binance_account = create_random_binance_account(db)

    data = {
        "binance_api_key": random_lower_string(),
        "binance_api_secret": random_lower_string(),
    }

    response = client.put(
        f"{settings.API_V1_STR}/binance/accounts/{binance_account.id}",
        headers=normal_user_token_headers,
        json=data
    )
    
    assert response.status_code == 400


def test_delete_binance_account_by_admin(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    user = create_random_user(db)
    binance_account = create_random_binance_account(db, user_id=user.id)

    response = client.delete(
        f"{settings.API_V1_STR}/binance/accounts/{binance_account.id}",
        headers=superuser_token_headers,
    )
    content = response.json()

    assert response.status_code == 200
    assert "id" in content
    assert content["binance_api_url"] == binance_account.binance_api_url
    assert content["binance_api_key"] == binance_account.binance_api_key
    assert content["binance_api_secret"] == binance_account.binance_api_secret


def test_delete_binance_account_by_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/users/me",
        headers=normal_user_token_headers)
    user_id = r.json()["id"]
    
    binance_account = create_random_binance_account(db, user_id=user_id)

    response = client.delete(
        f"{settings.API_V1_STR}/binance/accounts/{binance_account.id}",
        headers=normal_user_token_headers)
    content = response.json()

    assert response.status_code == 200
    assert "id" in content
    assert content["binance_api_url"] == binance_account.binance_api_url
    assert content["binance_api_key"] == binance_account.binance_api_key
    assert content["binance_api_secret"] == binance_account.binance_api_secret


def test_delete_binance_account_by_another_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    binance_account = create_random_binance_account(db)
    response = client.delete(
        f"{settings.API_V1_STR}/binance/accounts/{binance_account.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
