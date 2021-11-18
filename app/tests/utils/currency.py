from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import random
import json

from sqlalchemy.orm import Session

from app import crud, models
from app.schemas.currency import Currency, CurrencyCreate
from app.tests.utils.utils import (
    random_int_range, random_float_range, random_lower_string,
    random_time_range, random_weekdays)

# from app.tests.utils.user import create_random_user_id


def get_random_exchange_currency():
    base_currencies = ["AVAX", "DOGE", "ETH", "SHIB", "XTZ"]
    quote_currencies = ["BTC", "BUSD", "USDT", "DAI"]

    return random.choice(base_currencies), random.choice(quote_currencies)
