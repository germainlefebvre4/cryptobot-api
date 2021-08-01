from datetime import date, datetime
from dateutil.relativedelta import relativedelta

# from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.utils import random_lower_string, random_weekdays
from app.tests.utils.user import create_random_user
from app.tests.utils.telegram import create_random_telegram


def test_create_telegram_by_admin(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    data = {
        "client_id": random_lower_string(),
        "token": random_lower_string(),
    }

    response = client.post(
        f"{settings.API_V1_STR}/telegram/",
        headers=superuser_token_headers,
        json=data)
    content = response.json()

    assert response.status_code == 200
    assert "id" in content
    assert content["client_id"] == data["client_id"]
    assert content["token"] == data["token"]


def test_create_telegram_by_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    user_id = r.json()["id"]
    user_firstname = r.json()["firstname"]
    user_email = r.json()["email"]
    
    data = {
        "client_id": random_lower_string(),
        "token": random_lower_string(),
    }

    response = client.post(
        f"{settings.API_V1_STR}/telegram/",
        headers=normal_user_token_headers,
        json=data)
    content = response.json()

    assert response.status_code == 200
    assert "id" in content
    assert content["client_id"] == data["client_id"]
    assert content["token"] == data["token"]


def test_read_telegram_by_admin(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    user = create_random_user(db)
    telegram = create_random_telegram(db, user_id=user.id)

    response = client.get(
        f"{settings.API_V1_STR}/telegram/{telegram.id}",
        headers=superuser_token_headers,
    )
    content = response.json()

    assert response.status_code == 200
    assert "id" in content
    assert content["client_id"] == telegram.client_id
    assert content["token"] == telegram.token


def test_read_telegram_by_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    user_id = r.json()["id"]
    
    telegram = create_random_telegram(db, user_id=user_id)
    
    response = client.get(
        f"{settings.API_V1_STR}/telegram/{telegram.id}",
        headers=normal_user_token_headers,
    )
    content = response.json()

    assert response.status_code == 200
    assert "id" in content
    assert content["client_id"] == telegram.client_id
    assert content["token"] == telegram.token


def test_read_telegram_by_another_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    telegram = create_random_telegram(db)
    response = client.get(
        f"{settings.API_V1_STR}/telegram/{telegram.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400


def test_update_telegram_by_admin(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    user = create_random_user(db)
    telegram = create_random_telegram(db, user_id=user.id)

    data = {
        "client_id": random_lower_string(),
        "token": random_lower_string(),
    }

    response = client.put(
        f"{settings.API_V1_STR}/telegram/{telegram.id}",
        headers=superuser_token_headers,
        json=data
    )
    content = response.json()

    assert response.status_code == 200
    assert "id" in content
    assert content["client_id"] == data["client_id"]
    assert content["token"] == data["token"]


def test_update_telegram_by_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    user_id = r.json()["id"]

    telegram = create_random_telegram(db, user_id=user_id)

    data = {
        "client_id": random_lower_string(),
        "token": random_lower_string(),
    }

    response = client.put(
        f"{settings.API_V1_STR}/telegram/{telegram.id}",
        headers=normal_user_token_headers,
        json=data
    )
    content = response.json()

    assert response.status_code == 200
    assert "id" in content
    assert content["client_id"] == data["client_id"]
    assert content["token"] == data["token"]


def test_update_telegram_by_another_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    telegram = create_random_telegram(db)

    data = {
        "client_id": random_lower_string(),
        "token": random_lower_string(),
    }

    response = client.put(
        f"{settings.API_V1_STR}/telegram/{telegram.id}",
        headers=normal_user_token_headers,
        json=data
    )
    
    assert response.status_code == 400


def test_delete_telegram_by_admin(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    user = create_random_user(db)
    telegram = create_random_telegram(db, user_id=user.id)

    response = client.delete(
        f"{settings.API_V1_STR}/telegram/{telegram.id}",
        headers=superuser_token_headers,
    )
    content = response.json()

    assert response.status_code == 200
    assert "id" in content
    assert content["client_id"] == telegram.client_id
    assert content["token"] == telegram.token


def test_delete_telegram_by_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/users/me",
        headers=normal_user_token_headers)
    user_id = r.json()["id"]
    
    telegram = create_random_telegram(db, user_id=user_id)

    response = client.delete(
        f"{settings.API_V1_STR}/telegram/{telegram.id}",
        headers=normal_user_token_headers)
    content = response.json()

    assert response.status_code == 200
    assert "id" in content
    assert content["client_id"] == telegram.client_id
    assert content["token"] == telegram.token


def test_delete_telegram_by_another_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    telegram = create_random_telegram(db)
    response = client.delete(
        f"{settings.API_V1_STR}/telegram/{telegram.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
