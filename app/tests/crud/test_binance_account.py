from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import random
import json

from sqlalchemy.orm import Session

from app import crud
from app.schemas.binance_account import BinanceAccountCreate, BinanceAccountUpdate
from app.tests.utils.utils import (
    random_int_range, random_float_range,
    random_lower_string)

from app.tests.utils.user import create_random_user


def test_create_binance_account(db: Session) -> None:
    user = create_random_user(db)

    binance_api_key = random_lower_string()
    binance_api_secret = random_lower_string()

    binance_account_in = BinanceAccountCreate(
        binance_api_key=binance_api_key, binance_api_secret=binance_api_secret,
    )
    
    binance_account = crud.binance_account.create_with_owner(
        db=db, obj_in=binance_account_in, user_id=user.id)

    assert binance_account.user_id == user.id
    assert binance_account.user.id == user.id
    assert binance_account.user.firstname == user.firstname
    assert binance_account.user.email == user.email
    assert binance_account.binance_api_key == binance_api_key
    assert binance_account.binance_api_secret == binance_api_secret
    assert isinstance(binance_account.created_on, datetime)
    assert binance_account.updated_on == None


def test_get_binance_account(db: Session) -> None:
    user = create_random_user(db)

    binance_api_key = random_lower_string()
    binance_api_secret = random_lower_string()

    binance_account_in = BinanceAccountCreate(
        binance_api_key=binance_api_key, binance_api_secret=binance_api_secret,
    )
    
    binance_account = crud.binance_account.create_with_owner(
        db=db, obj_in=binance_account_in, user_id=user.id)
    stored_binance_accounts = crud.binance_account.get(db=db, id=binance_account.id)

    assert stored_binance_accounts
    assert binance_account.id == stored_binance_accounts.id
    assert binance_account.user_id == stored_binance_accounts.user_id
    assert binance_account.user.id == stored_binance_accounts.user.id
    assert binance_account.user.firstname == stored_binance_accounts.user.firstname
    assert binance_account.user.email == stored_binance_accounts.user.email
    assert binance_account.binance_api_key == stored_binance_accounts.binance_api_key
    assert binance_account.binance_api_secret == stored_binance_accounts.binance_api_secret
    assert isinstance(stored_binance_accounts.created_on, datetime)
    assert stored_binance_accounts.updated_on == None


def test_get_binance_accounts_with_user(db: Session) -> None:
    user = create_random_user(db)

    binance_api_key = random_lower_string()
    binance_api_secret = random_lower_string()

    binance_account_in = BinanceAccountCreate(
        binance_api_key=binance_api_key, binance_api_secret=binance_api_secret,
    )

    stored_binance_accounts_before = crud.binance_account.get_multi_by_user(db=db, user_id=user.id)
    binance_account = crud.binance_account.create_with_owner(
        db=db, obj_in=binance_account_in, user_id=user.id)
        
    stored_binance_accounts = crud.binance_account.get_multi_by_user(db=db, user_id=user.id)

    assert isinstance(stored_binance_accounts, list)
    assert stored_binance_accounts
    assert len(stored_binance_accounts) == len(stored_binance_accounts_before) + 1


def test_update_binance_account(db: Session) -> None:
    user = create_random_user(db)

    binance_api_key = random_lower_string()
    binance_api_secret = random_lower_string()

    binance_account_in = BinanceAccountCreate(
        binance_api_key=binance_api_key, binance_api_secret=binance_api_secret)

    binance_account = crud.binance_account.create_with_owner(
        db=db, obj_in=binance_account_in, user_id=user.id)
        
    binance_account_update = BinanceAccountUpdate(
        binance_api_key=binance_api_key, binance_api_secret=binance_api_secret,
    )

    binance_account2 = crud.binance_account.update(db=db, db_obj=binance_account, obj_in=binance_account_update)

    assert binance_account.id == binance_account2.id
    assert binance_account.user_id == binance_account2.user_id
    assert binance_account.user.id == binance_account2.user.id
    assert binance_account.user.firstname == binance_account2.user.firstname
    assert binance_account.user.email == binance_account2.user.email
    assert binance_account.binance_api_key == binance_account2.binance_api_key
    assert binance_account.binance_api_secret == binance_account2.binance_api_secret
    assert isinstance(binance_account2.created_on, datetime)
    assert isinstance(binance_account2.updated_on, datetime)


def test_delete_binance_account(db: Session) -> None:
    user = create_random_user(db)

    binance_api_key = random_lower_string()
    binance_api_secret = random_lower_string()

    binance_account_in = BinanceAccountCreate(
        binance_api_key=binance_api_key, binance_api_secret=binance_api_secret,
    )

    binance_account = crud.binance_account.create_with_owner(
        db=db, obj_in=binance_account_in, user_id=user.id)

    binance_account2 = crud.binance_account.remove(db=db, id=binance_account.id)

    binance_account3 = crud.binance_account.get(db=db, id=binance_account.id)
    
    assert binance_account3 is None
    assert binance_account.id == binance_account.id
    assert binance_account2.user_id == binance_account.user_id
    assert binance_account2.user.id == binance_account.user.id
    assert binance_account2.user.firstname == binance_account.user.firstname
    assert binance_account2.user.email == binance_account.user.email
    assert binance_account2.binance_api_key == binance_account.binance_api_key
    assert binance_account2.binance_api_secret == binance_account.binance_api_secret
    assert isinstance(binance_account2.created_on, datetime)
