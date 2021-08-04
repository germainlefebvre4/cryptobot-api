from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import random
import json

from sqlalchemy.orm import Session

from app import crud
from app.schemas.cryptobot import CryptobotCreate, CryptobotUpdate
from app.schemas.binance_account import BinanceAccount
from app.schemas.telegram import Telegram
from app.tests.utils.utils import (
    random_int_range, random_float_range,
    random_lower_string)

from app.tests.utils.user import create_random_user
from app.tests.utils.binance_account import create_random_binance_account
from app.tests.utils.telegram import create_random_telegram


def test_create_cryptobot(db: Session) -> None:
    user = create_random_user(db)
    binance_account = create_random_binance_account(db, user_id=user.id)
    telegram = create_random_telegram(db, user_id=user.id)

    binance_config_base_currency = "BTC"
    binance_config_quote_currency = "EUR"
    binance_config_granularity = "15m"
    binance_config_live = False
    binance_config_verbose = True
    binance_config_graphs = False
    binance_config_buymaxsize = 0.0004
    binance_config_sellupperpcnt = 10
    binance_config_selllowerpcnt = -10
    binance_config_disablebullonly = False
    binance_config_disablebuynearhigh = False
    binance_config_disablebuymacd = False
    binance_config_disablebuyema = False
    binance_config_disablebuyobv = False
    binance_config_disablebuyelderray = False
    binance_config_disablefailsafefibonaccilow = False
    binance_config_disablefailsafelowerpcnt = False
    binance_config_disableprofitbankupperpcnt = False
    binance_config_disableprofitbankfibonaccihigh = False
    binance_config_disableprofitbankreversal = False
    logger_filelog = True
    logger_logfile = "pycryptobot.log"
    logger_fileloglevel = "DEBUG"
    logger_consolelog = True
    logger_consoleloglevel = "INFO"

    cryptobot_in = CryptobotCreate(
        binance_config_base_currency=binance_config_base_currency,
        binance_config_quote_currency=binance_config_quote_currency,
        binance_config_granularity=binance_config_granularity,
        binance_config_live=binance_config_live,
        binance_config_verbose=binance_config_verbose,
        binance_config_graphs=binance_config_graphs,
        binance_config_buymaxsize=binance_config_buymaxsize,
        binance_config_sellupperpcnt=binance_config_sellupperpcnt,
        binance_config_selllowerpcnt=binance_config_selllowerpcnt,
        binance_config_disablebullonly=binance_config_disablebullonly,
        binance_config_disablebuynearhigh=binance_config_disablebuynearhigh,
        binance_config_disablebuymacd=binance_config_disablebuymacd,
        binance_config_disablebuyema=binance_config_disablebuyema,
        binance_config_disablebuyobv=binance_config_disablebuyobv,
        binance_config_disablebuyelderray=binance_config_disablebuyelderray,
        binance_config_disablefailsafefibonaccilow=binance_config_disablefailsafefibonaccilow,
        binance_config_disablefailsafelowerpcnt=binance_config_disablefailsafelowerpcnt,
        binance_config_disableprofitbankupperpcnt=binance_config_disableprofitbankupperpcnt,
        binance_config_disableprofitbankfibonaccihigh=binance_config_disableprofitbankfibonaccihigh,
        binance_config_disableprofitbankreversal=binance_config_disableprofitbankreversal,
        logger_filelog=logger_filelog, logger_logfile=logger_logfile, logger_fileloglevel=logger_fileloglevel,
        logger_consolelog=logger_consolelog, logger_consoleloglevel=logger_consoleloglevel,
    )
    
    cryptobot = crud.cryptobot.create_with_owner(
        db=db, obj_in=cryptobot_in, user_id=user.id, binance_account_id=binance_account.id, telegram_id=telegram.id)

    assert cryptobot.user_id == user.id
    assert cryptobot.user.id == user.id
    assert cryptobot.user.firstname == user.firstname
    assert cryptobot.user.email == user.email
    assert cryptobot.binance_config_base_currency == binance_config_base_currency
    assert cryptobot.binance_config_quote_currency == binance_config_quote_currency
    assert cryptobot.binance_config_granularity == binance_config_granularity
    assert cryptobot.binance_config_live == binance_config_live
    assert cryptobot.binance_config_verbose == binance_config_verbose
    assert cryptobot.binance_config_graphs == binance_config_graphs
    assert cryptobot.binance_config_buymaxsize == binance_config_buymaxsize
    assert cryptobot.binance_config_sellupperpcnt == binance_config_sellupperpcnt
    assert cryptobot.binance_config_selllowerpcnt == binance_config_selllowerpcnt
    assert cryptobot.binance_config_disablebullonly == binance_config_disablebullonly
    assert cryptobot.binance_config_disablebuynearhigh == binance_config_disablebuynearhigh
    assert cryptobot.binance_config_disablebuymacd == binance_config_disablebuymacd
    assert cryptobot.binance_config_disablebuyema == binance_config_disablebuyema
    assert cryptobot.binance_config_disablebuyobv == binance_config_disablebuyobv
    assert cryptobot.binance_config_disablebuyelderray == binance_config_disablebuyelderray
    assert cryptobot.binance_config_disablefailsafefibonaccilow == binance_config_disablefailsafefibonaccilow
    assert cryptobot.binance_config_disablefailsafelowerpcnt == binance_config_disablefailsafelowerpcnt
    assert cryptobot.binance_config_disableprofitbankupperpcnt == binance_config_disableprofitbankupperpcnt
    assert cryptobot.binance_config_disableprofitbankfibonaccihigh == binance_config_disableprofitbankfibonaccihigh
    assert cryptobot.binance_config_disableprofitbankreversal == binance_config_disableprofitbankreversal
    assert cryptobot.logger_filelog == logger_filelog
    assert cryptobot.logger_logfile == logger_logfile
    assert cryptobot.logger_fileloglevel == logger_fileloglevel
    assert cryptobot.logger_consolelog == logger_consolelog
    assert cryptobot.logger_consoleloglevel == logger_consoleloglevel
    assert isinstance(cryptobot.created_on, datetime)
    assert cryptobot.updated_on == None


def test_get_cryptobot(db: Session) -> None:
    user = create_random_user(db)
    binance_account = create_random_binance_account(db, user_id=user.id)
    telegram = create_random_telegram(db, user_id=user.id)

    binance_config_base_currency = "BTC"
    binance_config_quote_currency = "EUR"
    binance_config_granularity = "15m"
    binance_config_live = False
    binance_config_verbose = True
    binance_config_graphs = False
    binance_config_buymaxsize = 0.0004
    binance_config_sellupperpcnt = 10
    binance_config_selllowerpcnt = -10
    binance_config_disablebullonly = False
    binance_config_disablebuynearhigh = False
    binance_config_disablebuymacd = False
    binance_config_disablebuyema = False
    binance_config_disablebuyobv = False
    binance_config_disablebuyelderray = False
    binance_config_disablefailsafefibonaccilow = False
    binance_config_disablefailsafelowerpcnt = False
    binance_config_disableprofitbankupperpcnt = False
    binance_config_disableprofitbankfibonaccihigh = False
    binance_config_disableprofitbankreversal = False
    logger_filelog = True
    logger_logfile = "pycryptobot.log"
    logger_fileloglevel = "DEBUG"
    logger_consolelog = True
    logger_consoleloglevel = "INFO"

    cryptobot_in = CryptobotCreate(
        binance_config_base_currency=binance_config_base_currency,
        binance_config_quote_currency=binance_config_quote_currency,
        binance_config_granularity=binance_config_granularity,
        binance_config_live=binance_config_live,
        binance_config_verbose=binance_config_verbose,
        binance_config_graphs=binance_config_graphs,
        binance_config_buymaxsize=binance_config_buymaxsize,
        binance_config_sellupperpcnt=binance_config_sellupperpcnt,
        binance_config_selllowerpcnt=binance_config_selllowerpcnt,
        binance_config_disablebullonly=binance_config_disablebullonly,
        binance_config_disablebuynearhigh=binance_config_disablebuynearhigh,
        binance_config_disablebuymacd=binance_config_disablebuymacd,
        binance_config_disablebuyema=binance_config_disablebuyema,
        binance_config_disablebuyobv=binance_config_disablebuyobv,
        binance_config_disablebuyelderray=binance_config_disablebuyelderray,
        binance_config_disablefailsafefibonaccilow=binance_config_disablefailsafefibonaccilow,
        binance_config_disablefailsafelowerpcnt=binance_config_disablefailsafelowerpcnt,
        binance_config_disableprofitbankupperpcnt=binance_config_disableprofitbankupperpcnt,
        binance_config_disableprofitbankfibonaccihigh=binance_config_disableprofitbankfibonaccihigh,
        binance_config_disableprofitbankreversal=binance_config_disableprofitbankreversal,
        logger_filelog=logger_filelog, logger_logfile=logger_logfile, logger_fileloglevel=logger_fileloglevel,
        logger_consolelog=logger_consolelog, logger_consoleloglevel=logger_consoleloglevel,
    )
    
    cryptobot = crud.cryptobot.create_with_owner(
        db=db, obj_in=cryptobot_in, user_id=user.id, binance_account_id=binance_account.id, telegram_id=telegram.id)
    stored_cryptobots = crud.cryptobot.get(db=db, id=cryptobot.id)

    assert stored_cryptobots
    assert cryptobot.id == stored_cryptobots.id
    assert cryptobot.user_id == stored_cryptobots.user_id
    assert cryptobot.user.id == stored_cryptobots.user.id
    assert cryptobot.user.firstname == stored_cryptobots.user.firstname
    assert cryptobot.user.email == stored_cryptobots.user.email
    assert cryptobot.binance_config_base_currency == stored_cryptobots.binance_config_base_currency
    assert cryptobot.binance_config_quote_currency == stored_cryptobots.binance_config_quote_currency
    assert cryptobot.binance_config_granularity == stored_cryptobots.binance_config_granularity
    assert cryptobot.binance_config_live == stored_cryptobots.binance_config_live
    assert cryptobot.binance_config_verbose == stored_cryptobots.binance_config_verbose
    assert cryptobot.binance_config_graphs == stored_cryptobots.binance_config_graphs
    assert cryptobot.binance_config_buymaxsize == stored_cryptobots.binance_config_buymaxsize
    assert cryptobot.binance_config_sellupperpcnt == binance_config_sellupperpcnt
    assert cryptobot.binance_config_selllowerpcnt == binance_config_selllowerpcnt
    assert cryptobot.binance_config_disablebullonly == stored_cryptobots.binance_config_disablebullonly
    assert cryptobot.binance_config_disablebuynearhigh == stored_cryptobots.binance_config_disablebuynearhigh
    assert cryptobot.binance_config_disablebuymacd == stored_cryptobots.binance_config_disablebuymacd
    assert cryptobot.binance_config_disablebuyema == stored_cryptobots.binance_config_disablebuyema
    assert cryptobot.binance_config_disablebuyobv == stored_cryptobots.binance_config_disablebuyobv
    assert cryptobot.binance_config_disablebuyelderray == stored_cryptobots.binance_config_disablebuyelderray
    assert cryptobot.binance_config_disablefailsafefibonaccilow == stored_cryptobots.binance_config_disablefailsafefibonaccilow
    assert cryptobot.binance_config_disablefailsafelowerpcnt == stored_cryptobots.binance_config_disablefailsafelowerpcnt
    assert cryptobot.binance_config_disableprofitbankupperpcnt == stored_cryptobots.binance_config_disableprofitbankupperpcnt
    assert cryptobot.binance_config_disableprofitbankfibonaccihigh == stored_cryptobots.binance_config_disableprofitbankfibonaccihigh
    assert cryptobot.binance_config_disableprofitbankreversal == stored_cryptobots.binance_config_disableprofitbankreversal
    assert cryptobot.logger_filelog == stored_cryptobots.logger_filelog
    assert cryptobot.logger_logfile == stored_cryptobots.logger_logfile
    assert cryptobot.logger_fileloglevel == stored_cryptobots.logger_fileloglevel
    assert cryptobot.logger_consolelog == stored_cryptobots.logger_consolelog
    assert cryptobot.logger_consoleloglevel == stored_cryptobots.logger_consoleloglevel
    assert isinstance(stored_cryptobots.created_on, datetime)
    assert stored_cryptobots.updated_on == None


def test_get_cryptobots_with_user(db: Session) -> None:
    user = create_random_user(db)
    binance_account = create_random_binance_account(db, user_id=user.id)
    telegram = create_random_telegram(db, user_id=user.id)

    binance_config_base_currency = "BTC"
    binance_config_quote_currency = "EUR"
    binance_config_granularity = "15m"
    binance_config_live = False
    binance_config_verbose = True
    binance_config_graphs = False
    binance_config_buymaxsize = 0.0004
    binance_config_sellupperpcnt = 10
    binance_config_selllowerpcnt = -10
    binance_config_disablebullonly = False
    binance_config_disablebuynearhigh = False
    binance_config_disablebuymacd = False
    binance_config_disablebuyema = False
    binance_config_disablebuyobv = False
    binance_config_disablebuyelderray = False
    binance_config_disablefailsafefibonaccilow = False
    binance_config_disablefailsafelowerpcnt = False
    binance_config_disableprofitbankupperpcnt = False
    binance_config_disableprofitbankfibonaccihigh = False
    binance_config_disableprofitbankreversal = False
    logger_filelog = True
    logger_logfile = "pycryptobot.log"
    logger_fileloglevel = "DEBUG"
    logger_consolelog = True
    logger_consoleloglevel = "INFO"

    cryptobot_in = CryptobotCreate(
        binance_config_base_currency=binance_config_base_currency,
        binance_config_quote_currency=binance_config_quote_currency,
        binance_config_granularity=binance_config_granularity,
        binance_config_live=binance_config_live,
        binance_config_verbose=binance_config_verbose,
        binance_config_graphs=binance_config_graphs,
        binance_config_buymaxsize=binance_config_buymaxsize,
        binance_config_sellupperpcnt=binance_config_sellupperpcnt,
        binance_config_selllowerpcnt=binance_config_selllowerpcnt,
        binance_config_disablebullonly=binance_config_disablebullonly,
        binance_config_disablebuynearhigh=binance_config_disablebuynearhigh,
        binance_config_disablebuymacd=binance_config_disablebuymacd,
        binance_config_disablebuyema=binance_config_disablebuyema,
        binance_config_disablebuyobv=binance_config_disablebuyobv,
        binance_config_disablebuyelderray=binance_config_disablebuyelderray,
        binance_config_disablefailsafefibonaccilow=binance_config_disablefailsafefibonaccilow,
        binance_config_disablefailsafelowerpcnt=binance_config_disablefailsafelowerpcnt,
        binance_config_disableprofitbankupperpcnt=binance_config_disableprofitbankupperpcnt,
        binance_config_disableprofitbankfibonaccihigh=binance_config_disableprofitbankfibonaccihigh,
        binance_config_disableprofitbankreversal=binance_config_disableprofitbankreversal,
        logger_filelog=logger_filelog, logger_logfile=logger_logfile, logger_fileloglevel=logger_fileloglevel,
        logger_consolelog=logger_consolelog, logger_consoleloglevel=logger_consoleloglevel,
    )

    stored_cryptobots_before = crud.cryptobot.get_multi_by_user(db=db, user_id=user.id)
    cryptobot = crud.cryptobot.create_with_owner(
        db=db, obj_in=cryptobot_in, user_id=user.id, binance_account_id=binance_account.id, telegram_id=telegram.id)
        
    stored_cryptobots = crud.cryptobot.get_multi_by_user(db=db, user_id=user.id)

    assert isinstance(stored_cryptobots, list)
    assert stored_cryptobots
    assert len(stored_cryptobots) == len(stored_cryptobots_before) + 1


def test_update_cryptobot(db: Session) -> None:
    user = create_random_user(db)
    binance_account = create_random_binance_account(db, user_id=user.id)
    telegram = create_random_telegram(db, user_id=user.id)

    binance_config_base_currency = "BTC"
    binance_config_quote_currency = "EUR"
    binance_config_granularity = "15m"
    binance_config_live = False
    binance_config_verbose = True
    binance_config_graphs = False
    binance_config_buymaxsize = 0.0004
    binance_config_sellupperpcnt = 10
    binance_config_selllowerpcnt = -10
    binance_config_disablebullonly = False
    binance_config_disablebuynearhigh = False
    binance_config_disablebuymacd = False
    binance_config_disablebuyema = False
    binance_config_disablebuyobv = False
    binance_config_disablebuyelderray = False
    binance_config_disablefailsafefibonaccilow = False
    binance_config_disablefailsafelowerpcnt = False
    binance_config_disableprofitbankupperpcnt = False
    binance_config_disableprofitbankfibonaccihigh = False
    binance_config_disableprofitbankreversal = False
    logger_filelog = True
    logger_logfile = "pycryptobot.log"
    logger_fileloglevel = "DEBUG"
    logger_consolelog = True
    logger_consoleloglevel = "INFO"

    cryptobot_in = CryptobotCreate(
        binance_config_base_currency=binance_config_base_currency,
        binance_config_quote_currency=binance_config_quote_currency,
        binance_config_granularity=binance_config_granularity,
        binance_config_live=binance_config_live,
        binance_config_verbose=binance_config_verbose,
        binance_config_graphs=binance_config_graphs,
        binance_config_buymaxsize=binance_config_buymaxsize,
        binance_config_sellupperpcnt=binance_config_sellupperpcnt,
        binance_config_selllowerpcnt=binance_config_selllowerpcnt,
        binance_config_disablebullonly=binance_config_disablebullonly,
        binance_config_disablebuynearhigh=binance_config_disablebuynearhigh,
        binance_config_disablebuymacd=binance_config_disablebuymacd,
        binance_config_disablebuyema=binance_config_disablebuyema,
        binance_config_disablebuyobv=binance_config_disablebuyobv,
        binance_config_disablebuyelderray=binance_config_disablebuyelderray,
        binance_config_disablefailsafefibonaccilow=binance_config_disablefailsafefibonaccilow,
        binance_config_disablefailsafelowerpcnt=binance_config_disablefailsafelowerpcnt,
        binance_config_disableprofitbankupperpcnt=binance_config_disableprofitbankupperpcnt,
        binance_config_disableprofitbankfibonaccihigh=binance_config_disableprofitbankfibonaccihigh,
        binance_config_disableprofitbankreversal=binance_config_disableprofitbankreversal,
        logger_filelog=logger_filelog, logger_logfile=logger_logfile, logger_fileloglevel=logger_fileloglevel,
        logger_consolelog=logger_consolelog, logger_consoleloglevel=logger_consoleloglevel,
    )

    cryptobot = crud.cryptobot.create_with_owner(
        db=db, obj_in=cryptobot_in, user_id=user.id, binance_account_id=binance_account.id, telegram_id=telegram.id)
        
    cryptobot_update = CryptobotUpdate(
        binance_config_base_currency=binance_config_base_currency, binance_config_quote_currency=binance_config_quote_currency,
        binance_config_granularity=binance_config_granularity, binance_config_live=binance_config_live,
        binance_config_verbose=binance_config_verbose, binance_config_graphs=binance_config_graphs,
        binance_config_buymaxsize=binance_config_buymaxsize,
        binance_config_sellupperpcnt=binance_config_sellupperpcnt, binance_config_selllowerpcnt=binance_config_selllowerpcnt,
        logger_filelog=logger_filelog, logger_logfile=logger_logfile, logger_fileloglevel=logger_fileloglevel,
        logger_consolelog=logger_consolelog, logger_consoleloglevel=logger_consoleloglevel,
    )

    cryptobot2 = crud.cryptobot.update(db=db, db_obj=cryptobot, obj_in=cryptobot_update)

    assert cryptobot.id == cryptobot2.id
    assert cryptobot.user_id == cryptobot2.user_id
    assert cryptobot.user.id == cryptobot2.user.id
    assert cryptobot.user.firstname == cryptobot2.user.firstname
    assert cryptobot.user.email == cryptobot2.user.email
    assert cryptobot.binance_config_base_currency == cryptobot2.binance_config_base_currency
    assert cryptobot.binance_config_quote_currency == cryptobot2.binance_config_quote_currency
    assert cryptobot.binance_config_granularity == cryptobot2.binance_config_granularity
    assert cryptobot.binance_config_live == cryptobot2.binance_config_live
    assert cryptobot.binance_config_verbose == cryptobot2.binance_config_verbose
    assert cryptobot.binance_config_graphs == cryptobot2.binance_config_graphs
    assert cryptobot.binance_config_buymaxsize == cryptobot2.binance_config_buymaxsize
    assert cryptobot.binance_config_sellupperpcnt == cryptobot2.binance_config_sellupperpcnt
    assert cryptobot.binance_config_selllowerpcnt == cryptobot2.binance_config_selllowerpcnt
    assert cryptobot.binance_config_disablebullonly == cryptobot2.binance_config_disablebullonly
    assert cryptobot.binance_config_disablebuynearhigh == cryptobot2.binance_config_disablebuynearhigh
    assert cryptobot.binance_config_disablebuymacd == cryptobot2.binance_config_disablebuymacd
    assert cryptobot.binance_config_disablebuyema == cryptobot2.binance_config_disablebuyema
    assert cryptobot.binance_config_disablebuyobv == cryptobot2.binance_config_disablebuyobv
    assert cryptobot.binance_config_disablebuyelderray == cryptobot2.binance_config_disablebuyelderray
    assert cryptobot.binance_config_disablefailsafefibonaccilow == cryptobot2.binance_config_disablefailsafefibonaccilow
    assert cryptobot.binance_config_disablefailsafelowerpcnt == cryptobot2.binance_config_disablefailsafelowerpcnt
    assert cryptobot.binance_config_disableprofitbankupperpcnt == cryptobot2.binance_config_disableprofitbankupperpcnt
    assert cryptobot.binance_config_disableprofitbankfibonaccihigh == cryptobot2.binance_config_disableprofitbankfibonaccihigh
    assert cryptobot.binance_config_disableprofitbankreversal == cryptobot2.binance_config_disableprofitbankreversal
    assert cryptobot.logger_filelog == cryptobot2.logger_filelog
    assert cryptobot.logger_logfile == cryptobot2.logger_logfile
    assert cryptobot.logger_fileloglevel == cryptobot2.logger_fileloglevel
    assert cryptobot.logger_consolelog == cryptobot2.logger_consolelog
    assert cryptobot.logger_consoleloglevel == cryptobot2.logger_consoleloglevel
    assert isinstance(cryptobot2.created_on, datetime)
    assert isinstance(cryptobot2.updated_on, datetime)


def test_delete_cryptobot(db: Session) -> None:
    user = create_random_user(db)
    binance_account = create_random_binance_account(db, user_id=user.id)
    telegram = create_random_telegram(db, user_id=user.id)

    binance_config_base_currency = "BTC"
    binance_config_quote_currency = "EUR"
    binance_config_granularity = "15m"
    binance_config_live = False
    binance_config_verbose = True
    binance_config_graphs = False
    binance_config_buymaxsize = 0.0004
    binance_config_sellupperpcnt = 10
    binance_config_selllowerpcnt = -10
    binance_config_disablebullonly = False
    binance_config_disablebuynearhigh = False
    binance_config_disablebuymacd = False
    binance_config_disablebuyema = False
    binance_config_disablebuyobv = False
    binance_config_disablebuyelderray = False
    binance_config_disablefailsafefibonaccilow = False
    binance_config_disablefailsafelowerpcnt = False
    binance_config_disableprofitbankupperpcnt = False
    binance_config_disableprofitbankfibonaccihigh = False
    binance_config_disableprofitbankreversal = False
    logger_filelog = True
    logger_logfile = "pycryptobot.log"
    logger_fileloglevel = "DEBUG"
    logger_consolelog = True
    logger_consoleloglevel = "INFO"

    cryptobot_in = CryptobotCreate(
        binance_config_base_currency=binance_config_base_currency,
        binance_config_quote_currency=binance_config_quote_currency,
        binance_config_granularity=binance_config_granularity,
        binance_config_live=binance_config_live,
        binance_config_verbose=binance_config_verbose,
        binance_config_graphs=binance_config_graphs,
        binance_config_buymaxsize=binance_config_buymaxsize,
        binance_config_sellupperpcnt=binance_config_sellupperpcnt,
        binance_config_selllowerpcnt=binance_config_selllowerpcnt,
        binance_config_disablebullonly=binance_config_disablebullonly,
        binance_config_disablebuynearhigh=binance_config_disablebuynearhigh,
        binance_config_disablebuymacd=binance_config_disablebuymacd,
        binance_config_disablebuyema=binance_config_disablebuyema,
        binance_config_disablebuyobv=binance_config_disablebuyobv,
        binance_config_disablebuyelderray=binance_config_disablebuyelderray,
        binance_config_disablefailsafefibonaccilow=binance_config_disablefailsafefibonaccilow,
        binance_config_disablefailsafelowerpcnt=binance_config_disablefailsafelowerpcnt,
        binance_config_disableprofitbankupperpcnt=binance_config_disableprofitbankupperpcnt,
        binance_config_disableprofitbankfibonaccihigh=binance_config_disableprofitbankfibonaccihigh,
        binance_config_disableprofitbankreversal=binance_config_disableprofitbankreversal,
        logger_filelog=logger_filelog, logger_logfile=logger_logfile, logger_fileloglevel=logger_fileloglevel,
        logger_consolelog=logger_consolelog, logger_consoleloglevel=logger_consoleloglevel,
    )

    cryptobot = crud.cryptobot.create_with_owner(
        db=db, obj_in=cryptobot_in, user_id=user.id, binance_account_id=binance_account.id, telegram_id=telegram.id)

    cryptobot2 = crud.cryptobot.remove(db=db, id=cryptobot.id)

    cryptobot3 = crud.cryptobot.get(db=db, id=cryptobot.id)
    
    assert cryptobot3 is None
    assert cryptobot.id == cryptobot.id
    assert cryptobot2.user_id == cryptobot.user_id
    assert cryptobot2.user.id == cryptobot.user.id
    assert cryptobot2.user.firstname == cryptobot.user.firstname
    assert cryptobot2.user.email == cryptobot.user.email
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
    assert isinstance(cryptobot2.created_on, datetime)
