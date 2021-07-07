from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import random
import json

from sqlalchemy.orm import Session

from app import crud, models
from app.schemas.cryptobot import CryptobotCreate
from app.tests.utils.utils import (
    random_int_range, random_float_range, random_lower_string,
    random_time_range, random_weekdays)

from app.tests.utils.user import create_random_user


def create_random_cryptobot(
        db: Session,
        user_id: int = None,
        ) -> models.Cryptobot:
    if not user_id:
        user = create_random_user(db)
        user_id = user.id
    
    binance_api_url = "https://api.binance.com"
    binance_api_key = "xxxxxxxxxxxxxxxxxxx"
    binance_api_secret = "xxxxxxxxxxxxxxxxxxx"
    binance_config_base_currency = "BTC"
    binance_config_quote_currency = "EUR"
    binance_config_granularity = "15m"
    binance_config_live = False
    binance_config_verbose = True
    binance_config_graphs = False
    binance_config_buymaxsize = 0.0004
    logger_filelog = True
    logger_logfile = "pycryptobot.log"
    logger_fileloglevel = "DEBUG"
    logger_consolelog = True
    logger_consoleloglevel = "INFO"
    telegram_client_id = "xxxxxx"
    telegram_token = "xxxxxx"

    cryptobot_in = CryptobotCreate(
        binance_api_url=binance_api_url, binance_api_key=binance_api_key,
        binance_api_secret=binance_api_secret, binance_config_base_currency=binance_config_base_currency,
        binance_config_quote_currency=binance_config_quote_currency,
        binance_config_granularity=binance_config_granularity, binance_config_live=binance_config_live,
        binance_config_verbose=binance_config_verbose, binance_config_graphs=binance_config_graphs,
        binance_config_buymaxsize=binance_config_buymaxsize, logger_filelog=logger_filelog,
        logger_logfile=logger_logfile, logger_fileloglevel=logger_fileloglevel,
        logger_consolelog=logger_consolelog, logger_consoleloglevel=logger_consoleloglevel,
        telegram_client_id=telegram_client_id, telegram_token=telegram_token)
    
    return crud.cryptobot.create_with_owner(
        db=db, obj_in=cryptobot_in, user_id=user_id)
