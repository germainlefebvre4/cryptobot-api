from typing import Optional
from datetime import date, datetime

from pydantic import BaseModel
from app.schemas.user import User
from app.schemas.binance_account import BinanceAccount
from app.schemas.telegram import Telegram

class CryptobotBase(BaseModel):
    binance_config_base_currency: str
    binance_config_quote_currency: str
    binance_config_granularity: str = "15m"
    binance_config_live: bool = False
    binance_config_verbose : bool = True
    binance_config_graphs: bool = False
    binance_config_buymaxsize: float
    binance_config_sellupperpcnt: float
    binance_config_selllowerpcnt: float
    binance_config_disablebullonly: bool = False
    binance_config_disablebuynearhigh: bool = False
    binance_config_disablebuymacd: bool = False
    binance_config_disablebuyema: bool = False
    binance_config_disablebuyobv: bool = False
    binance_config_disablebuyelderray: bool = False
    binance_config_disablefailsafefibonaccilow: bool = False
    binance_config_disablefailsafelowerpcnt: bool = False
    binance_config_disableprofitbankupperpcnt: bool = False
    binance_config_disableprofitbankfibonaccihigh: bool = False
    binance_config_disableprofitbankreversal: bool = False
    logger_filelog: bool = False
    logger_logfile: str = "pycryptobot.log"
    logger_fileloglevel: str = "INFO"
    logger_consolelog: bool = True
    logger_consoleloglevel: str


class CryptobotCreate(CryptobotBase):
    pass


class CryptobotUpdate(BaseModel):
    binance_config_granularity: str = "15m"
    binance_config_live: bool = False
    binance_config_verbose : bool = True
    binance_config_graphs: bool = False
    binance_config_buymaxsize: float
    binance_config_sellupperpcnt: float
    binance_config_selllowerpcnt: float
    binance_config_disablebullonly: bool = False
    binance_config_disablebuynearhigh: bool = False
    binance_config_disablebuymacd: bool = False
    binance_config_disablebuyema: bool = False
    binance_config_disablebuyobv: bool = False
    binance_config_disablebuyelderray: bool = False
    binance_config_disablefailsafefibonaccilow: bool = False
    binance_config_disablefailsafelowerpcnt: bool = False
    binance_config_disableprofitbankupperpcnt: bool = False
    binance_config_disableprofitbankfibonaccihigh: bool = False
    binance_config_disableprofitbankreversal: bool = False
    logger_filelog: bool = False
    logger_logfile: str = "pycryptobot.log"
    logger_fileloglevel: str = "INFO"
    logger_consolelog: bool = True
    logger_consoleloglevel: str


class CryptobotDelete(CryptobotBase):
    id: int
    user_id: int
    binance_account_id: int

    class Config:
        orm_mode = True


class CryptobotInDBBase(CryptobotBase):
    id: int
    user_id: int
    user: User
    binance_account_id: int
    binance_account: BinanceAccount
    telegram_id: Optional[int]
    telegram: Optional[Telegram]

    created_on: Optional[datetime]
    updated_on: Optional[datetime]

    class Config:
        orm_mode = True


class Cryptobot(CryptobotInDBBase):
    pass


class CryptobotInDB(CryptobotInDBBase):
    pass


class CryptobotStatus(BaseModel):
    status: str


class CryptobotLogs(BaseModel):
    logs: str


class CryptobotVersion(BaseModel):
    version: str


class CryptobotMargin(BaseModel):
    value: Optional[float]
    unit: Optional[str]

class CryptobotMarginOverall(CryptobotMargin):
    pass

class CryptobotMarginLastTrade(BaseModel):
    base_currency: Optional[CryptobotMargin]
    quote_currency: Optional[CryptobotMargin]
    percent: Optional[float]

