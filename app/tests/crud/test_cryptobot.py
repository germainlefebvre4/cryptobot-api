from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import random
import json

from sqlalchemy.orm import Session

from app import crud
from app.schemas.cryptobot import CryptobotCreate, CryptobotUpdate
from app.schemas.cryptobot import binance, logger, telegram
from app.tests.utils.utils import (
    random_int_range, random_float_range,
    random_lower_string)

from app.tests.utils.user import create_random_user


def test_create_cryptobot(db: Session) -> None:
    user = create_random_user(db)

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
    
    cryptobot = crud.cryptobot.create_with_owner(
        db=db, obj_in=cryptobot_in, user_id=user.id)

    assert cryptobot.user_id == user.id
    assert cryptobot.user.id == user.id
    assert cryptobot.user.firstname == user.firstname
    assert cryptobot.user.email == user.email
    assert cryptobot.binance_api_url == binance_api_url
    assert cryptobot.binance_api_key == binance_api_key
    assert cryptobot.binance_api_secret == binance_api_secret
    assert cryptobot.binance_config_base_currency == binance_config_base_currency
    assert cryptobot.binance_config_quote_currency == binance_config_quote_currency
    assert cryptobot.binance_config_granularity == binance_config_granularity
    assert cryptobot.binance_config_live == binance_config_live
    assert cryptobot.binance_config_verbose == binance_config_verbose
    assert cryptobot.binance_config_graphs == binance_config_graphs
    assert cryptobot.binance_config_buymaxsize == binance_config_buymaxsize
    assert cryptobot.logger_filelog == logger_filelog
    assert cryptobot.logger_logfile == logger_logfile
    assert cryptobot.logger_fileloglevel == logger_fileloglevel
    assert cryptobot.logger_consolelog == logger_consolelog
    assert cryptobot.logger_consoleloglevel == logger_consoleloglevel
    assert cryptobot.telegram_client_id == telegram_client_id
    assert cryptobot.telegram_token == telegram_token
    assert isinstance(cryptobot.created_on, datetime)
    assert cryptobot.updated_on == None


def test_get_cryptobot(db: Session) -> None:
    user = create_random_user(db)

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
    
    cryptobot = crud.cryptobot.create_with_owner(
        db=db, obj_in=cryptobot_in, user_id=user.id)
    stored_cryptobots = crud.cryptobot.get(db=db, id=cryptobot.id)

    assert stored_cryptobots
    assert cryptobot.id == stored_cryptobots.id
    assert cryptobot.user_id == stored_cryptobots.user_id
    assert cryptobot.user.id == stored_cryptobots.user.id
    assert cryptobot.user.firstname == stored_cryptobots.user.firstname
    assert cryptobot.user.email == stored_cryptobots.user.email
    assert cryptobot.binance_api_url == stored_cryptobots.binance_api_url
    assert cryptobot.binance_api_key == stored_cryptobots.binance_api_key
    assert cryptobot.binance_api_secret == stored_cryptobots.binance_api_secret
    assert cryptobot.binance_config_base_currency == stored_cryptobots.binance_config_base_currency
    assert cryptobot.binance_config_quote_currency == stored_cryptobots.binance_config_quote_currency
    assert cryptobot.binance_config_granularity == stored_cryptobots.binance_config_granularity
    assert cryptobot.binance_config_live == stored_cryptobots.binance_config_live
    assert cryptobot.binance_config_verbose == stored_cryptobots.binance_config_verbose
    assert cryptobot.binance_config_graphs == stored_cryptobots.binance_config_graphs
    assert cryptobot.binance_config_buymaxsize == stored_cryptobots.binance_config_buymaxsize
    assert cryptobot.logger_filelog == stored_cryptobots.logger_filelog
    assert cryptobot.logger_logfile == stored_cryptobots.logger_logfile
    assert cryptobot.logger_fileloglevel == stored_cryptobots.logger_fileloglevel
    assert cryptobot.logger_consolelog == stored_cryptobots.logger_consolelog
    assert cryptobot.logger_consoleloglevel == stored_cryptobots.logger_consoleloglevel
    assert cryptobot.telegram_client_id == stored_cryptobots.telegram_client_id
    assert cryptobot.telegram_token == stored_cryptobots.telegram_token
    assert isinstance(stored_cryptobots.created_on, datetime)
    assert stored_cryptobots.updated_on == None


def test_get_cryptobots_with_user(db: Session) -> None:
    user = create_random_user(db)

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

    stored_cryptobots_before = crud.cryptobot.get_multi_by_user(db=db, user_id=user.id)
    cryptobot = crud.cryptobot.create_with_owner(
        db=db, obj_in=cryptobot_in, user_id=user.id)
        
    stored_cryptobots = crud.cryptobot.get_multi_by_user(db=db, user_id=user.id)

    assert isinstance(stored_cryptobots, list)
    assert stored_cryptobots
    assert len(stored_cryptobots) == len(stored_cryptobots_before) + 1


def test_update_cryptobot(db: Session) -> None:
    user = create_random_user(db)

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

    cryptobot = crud.cryptobot.create_with_owner(
        db=db, obj_in=cryptobot_in, user_id=user.id)
        
    cryptobot_update = CryptobotUpdate(
        binance_api_url=binance_api_url, binance_api_key=binance_api_key,
        binance_api_secret=binance_api_secret, binance_config_base_currency=binance_config_base_currency,
        binance_config_quote_currency=binance_config_quote_currency,
        binance_config_granularity=binance_config_granularity, binance_config_live=binance_config_live,
        binance_config_verbose=binance_config_verbose, binance_config_graphs=binance_config_graphs,
        binance_config_buymaxsize=binance_config_buymaxsize, logger_filelog=logger_filelog,
        logger_logfile=logger_logfile, logger_fileloglevel=logger_fileloglevel,
        logger_consolelog=logger_consolelog, logger_consoleloglevel=logger_consoleloglevel,
        telegram_client_id=telegram_client_id, telegram_token=telegram_token)

    cryptobot2 = crud.cryptobot.update(db=db, db_obj=cryptobot, obj_in=cryptobot_update)

    assert cryptobot.id == cryptobot2.id
    assert cryptobot.user_id == cryptobot2.user_id
    assert cryptobot.user.id == cryptobot2.user.id
    assert cryptobot.user.firstname == cryptobot2.user.firstname
    assert cryptobot.user.email == cryptobot2.user.email
    assert cryptobot.binance_api_url == cryptobot2.binance_api_url
    assert cryptobot.binance_api_key == cryptobot2.binance_api_key
    assert cryptobot.binance_api_secret == cryptobot2.binance_api_secret
    assert cryptobot.binance_config_base_currency == cryptobot2.binance_config_base_currency
    assert cryptobot.binance_config_quote_currency == cryptobot2.binance_config_quote_currency
    assert cryptobot.binance_config_granularity == cryptobot2.binance_config_granularity
    assert cryptobot.binance_config_live == cryptobot2.binance_config_live
    assert cryptobot.binance_config_verbose == cryptobot2.binance_config_verbose
    assert cryptobot.binance_config_graphs == cryptobot2.binance_config_graphs
    assert cryptobot.binance_config_buymaxsize == cryptobot2.binance_config_buymaxsize
    assert cryptobot.logger_filelog == cryptobot2.logger_filelog
    assert cryptobot.logger_logfile == cryptobot2.logger_logfile
    assert cryptobot.logger_fileloglevel == cryptobot2.logger_fileloglevel
    assert cryptobot.logger_consolelog == cryptobot2.logger_consolelog
    assert cryptobot.logger_consoleloglevel == cryptobot2.logger_consoleloglevel
    assert cryptobot.telegram_client_id == cryptobot2.telegram_client_id
    assert cryptobot.telegram_token == cryptobot2.telegram_token
    assert isinstance(cryptobot2.created_on, datetime)
    assert isinstance(cryptobot2.updated_on, datetime)


def test_delete_cryptobot(db: Session) -> None:
    user = create_random_user(db)

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

    cryptobot = crud.cryptobot.create_with_owner(
        db=db, obj_in=cryptobot_in, user_id=user.id)

    cryptobot2 = crud.cryptobot.remove(db=db, id=cryptobot.id)

    cryptobot3 = crud.cryptobot.get(db=db, id=cryptobot.id)
    
    assert cryptobot3 is None
    assert cryptobot.id == cryptobot.id
    assert cryptobot2.user_id == cryptobot.user_id
    assert cryptobot2.user.id == cryptobot.user.id
    assert cryptobot2.user.firstname == cryptobot.user.firstname
    assert cryptobot2.user.email == cryptobot.user.email
    assert cryptobot2.binance_api_url == cryptobot.binance_api_url
    assert cryptobot2.binance_api_key == cryptobot.binance_api_key
    assert cryptobot2.binance_api_secret == cryptobot.binance_api_secret
    assert cryptobot2.binance_config_base_currency == cryptobot.binance_config_base_currency
    assert cryptobot2.binance_config_quote_currency == cryptobot.binance_config_quote_currency
    assert cryptobot2.binance_config_granularity == cryptobot.binance_config_granularity
    assert cryptobot2.binance_config_live == cryptobot.binance_config_live
    assert cryptobot2.binance_config_verbose == cryptobot.binance_config_verbose
    assert cryptobot2.binance_config_graphs == cryptobot.binance_config_graphs
    assert cryptobot2.binance_config_buymaxsize == cryptobot.binance_config_buymaxsize
    assert cryptobot2.logger_filelog == cryptobot.logger_filelog
    assert cryptobot2.logger_logfile == cryptobot.logger_logfile
    assert cryptobot2.logger_fileloglevel == cryptobot.logger_fileloglevel
    assert cryptobot2.logger_consolelog == cryptobot.logger_consolelog
    assert cryptobot2.logger_consoleloglevel == cryptobot.logger_consoleloglevel
    assert cryptobot2.telegram_client_id == cryptobot.telegram_client_id
    assert cryptobot2.telegram_token == cryptobot.telegram_token
    assert isinstance(cryptobot2.created_on, datetime)
