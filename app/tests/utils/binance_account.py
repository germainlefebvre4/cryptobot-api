from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import random
import json

from sqlalchemy.orm import Session

from app import crud, models
from app.schemas.binance_account import BinanceAccountCreate
from app.tests.utils.utils import (
    random_int_range, random_float_range, random_lower_string,
    random_time_range, random_weekdays)

from app.tests.utils.user import create_random_user


def create_random_binance_account(
        db: Session,
        user_id: int = None,
        ) -> models.BinanceAccount:
    if not user_id:
        user = create_random_user(db)
        user_id = user.id
    
    binance_api_key = random_lower_string()
    binance_api_secret = random_lower_string()

    binance_account_in = BinanceAccountCreate(
        binance_api_key=binance_api_key, binance_api_secret=binance_api_secret)
    
    return crud.binance_account.create_with_owner(
        db=db, obj_in=binance_account_in, user_id=user_id)
