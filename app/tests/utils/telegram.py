from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import random
import json

from sqlalchemy.orm import Session

from app import crud, models
from app.schemas.telegram import TelegramCreate
from app.tests.utils.utils import (
    random_int_range, random_float_range, random_lower_string,
    random_time_range, random_weekdays)

from app.tests.utils.user import create_random_user


def create_random_telegram(
        db: Session,
        user_id: int = None,
        ) -> models.Telegram:
    if not user_id:
        user = create_random_user(db)
        user_id = user.id
    
    client_id = random_lower_string()
    token = random_lower_string()

    telegram_in = TelegramCreate(
        client_id=client_id, token=token)
    
    return crud.telegram.create_with_owner(
        db=db, obj_in=telegram_in, user_id=user_id)
