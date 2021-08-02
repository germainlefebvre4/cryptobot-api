from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import random
import json

from sqlalchemy.orm import Session

from app import crud
from app.schemas.telegram import TelegramCreate, TelegramUpdate
from app.tests.utils.utils import (
    random_int_range, random_float_range,
    random_lower_string)

from app.tests.utils.user import create_random_user


def test_create_telegram(db: Session) -> None:
    user = create_random_user(db)

    client_id = random_lower_string()
    token = random_lower_string()

    telegram_in = TelegramCreate(
        client_id=client_id, token=token,
    )
    
    telegram = crud.telegram.create_with_owner(
        db=db, obj_in=telegram_in, user_id=user.id)

    assert telegram.user_id == user.id
    assert telegram.user.id == user.id
    assert telegram.user.firstname == user.firstname
    assert telegram.user.email == user.email
    assert telegram.client_id == client_id
    assert telegram.token == token
    assert isinstance(telegram.created_on, datetime)
    assert telegram.updated_on == None


def test_get_telegram(db: Session) -> None:
    user = create_random_user(db)

    client_id = random_lower_string()
    token = random_lower_string()

    telegram_in = TelegramCreate(
        client_id=client_id, token=token,
    )
    
    telegram = crud.telegram.create_with_owner(
        db=db, obj_in=telegram_in, user_id=user.id)
    stored_telegrams = crud.telegram.get(db=db, id=telegram.id)

    assert stored_telegrams
    assert telegram.id == stored_telegrams.id
    assert telegram.user_id == stored_telegrams.user_id
    assert telegram.user.id == stored_telegrams.user.id
    assert telegram.user.firstname == stored_telegrams.user.firstname
    assert telegram.user.email == stored_telegrams.user.email
    assert telegram.client_id == stored_telegrams.client_id
    assert telegram.token == stored_telegrams.token
    assert isinstance(stored_telegrams.created_on, datetime)
    assert stored_telegrams.updated_on == None


def test_get_telegrams_with_user(db: Session) -> None:
    user = create_random_user(db)

    client_id = random_lower_string()
    token = random_lower_string()

    telegram_in = TelegramCreate(
        client_id=client_id, token=token,
    )

    stored_telegrams_before = crud.telegram.get_multi_by_user(db=db, user_id=user.id)
    telegram = crud.telegram.create_with_owner(
        db=db, obj_in=telegram_in, user_id=user.id)
        
    stored_telegrams = crud.telegram.get_multi_by_user(db=db, user_id=user.id)

    assert isinstance(stored_telegrams, list)
    assert stored_telegrams
    assert len(stored_telegrams) == len(stored_telegrams_before) + 1


def test_update_telegram(db: Session) -> None:
    user = create_random_user(db)

    client_id = random_lower_string()
    token = random_lower_string()

    telegram_in = TelegramCreate(
        client_id=client_id, token=token)

    telegram = crud.telegram.create_with_owner(
        db=db, obj_in=telegram_in, user_id=user.id)
        
    telegram_update = TelegramUpdate(
        client_id=client_id, token=token,
    )

    telegram2 = crud.telegram.update(db=db, db_obj=telegram, obj_in=telegram_update)

    assert telegram.id == telegram2.id
    assert telegram.user_id == telegram2.user_id
    assert telegram.user.id == telegram2.user.id
    assert telegram.user.firstname == telegram2.user.firstname
    assert telegram.user.email == telegram2.user.email
    assert telegram.client_id == telegram2.client_id
    assert telegram.token == telegram2.token
    assert isinstance(telegram2.created_on, datetime)
    assert isinstance(telegram2.updated_on, datetime)


def test_delete_telegram(db: Session) -> None:
    user = create_random_user(db)

    client_id = random_lower_string()
    token = random_lower_string()

    telegram_in = TelegramCreate(
        client_id=client_id, token=token,
    )

    telegram = crud.telegram.create_with_owner(
        db=db, obj_in=telegram_in, user_id=user.id)

    telegram2 = crud.telegram.remove(db=db, id=telegram.id)

    telegram3 = crud.telegram.get(db=db, id=telegram.id)
    
    assert telegram3 is None
    assert telegram.id == telegram.id
    assert telegram2.user_id == telegram.user_id
    assert telegram2.user.id == telegram.user.id
    assert telegram2.user.firstname == telegram.user.firstname
    assert telegram2.user.email == telegram.user.email
    assert telegram2.client_id == telegram.client_id
    assert telegram2.token == telegram.token
    assert isinstance(telegram2.created_on, datetime)
