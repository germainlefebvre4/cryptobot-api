from typing import Optional
from datetime import date, datetime

from pydantic import BaseModel
from app.schemas.user import User
from app.schemas.binance_account import BinanceAccount


class CryptobotBase(BaseModel):
    # customer: str
    binance_config_base_currency: str
    binance_config_quote_currency: str
    binance_config_granularity: str = "15m"
    binance_config_live: bool = False
    binance_config_verbose : bool = True
    binance_config_graphs: bool = False
    binance_config_buymaxsize: float
    binance_config_sellupperpcnt: float
    binance_config_selllowerpcnt: float
    logger_filelog: bool = False
    logger_logfile: str = "pycryptobot.log"
    logger_fileloglevel: str = "INFO"
    logger_consolelog: bool = True
    logger_consoleloglevel: str
    telegram_client_id: str
    telegram_token: str


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
    logger_filelog: bool = False
    logger_logfile: str = "pycryptobot.log"
    logger_fileloglevel: str = "INFO"
    logger_consolelog: bool = True
    logger_consoleloglevel: str
    telegram_client_id: str
    telegram_token: str


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

    created_on: Optional[datetime]
    updated_on: Optional[datetime]

    class Config:
        orm_mode = True


class Cryptobot(CryptobotInDBBase):
    pass


class CryptobotInDB(CryptobotInDBBase):
    pass
