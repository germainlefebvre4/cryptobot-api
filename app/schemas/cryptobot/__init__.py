from typing import Optional
from datetime import date, datetime

from pydantic import BaseModel
from app.schemas.user import User
from app.schemas.cryptobot.binance import Binance
from app.schemas.cryptobot.logger import Logger
from app.schemas.cryptobot.telegram import Telegram


class CryptobotBase(BaseModel):
    binance_api_url: str = "https://api.binance.com"
    binance_api_key: str
    binance_api_secret: str
    binance_config_base_currency: str
    binance_config_quote_currency: str
    binance_config_granularity: str = "15m"
    binance_config_live: bool = False # enum(0, 1) = 0
    binance_config_verbose : bool = True # enum(0, 1) = 1
    binance_config_graphs: bool = False # enum(0, 1) = 0
    binance_config_buymaxsize: float
    logger_filelog: bool = False
    logger_logfile: str = "pycryptobot.log"
    logger_fileloglevel: str # enum("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"),
    logger_consolelog: bool = True
    logger_consoleloglevel: str # enum("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
    telegram_client_id: str
    telegram_token: str


class CryptobotCreate(CryptobotBase):
    binance_api_url: str = "https://api.binance.com"
    binance_api_key: str
    binance_api_secret: str
    binance_config_base_currency: str
    binance_config_quote_currency: str
    binance_config_granularity: str = "15m"
    binance_config_live: bool = False
    binance_config_verbose : bool = True
    binance_config_graphs: bool = False
    binance_config_buymaxsize: float
    logger_filelog: bool = False
    logger_logfile: str = "pycryptobot.log"
    logger_fileloglevel: str
    logger_consolelog: bool = True
    logger_consoleloglevel: str
    telegram_client_id: str
    telegram_token: str


class CryptobotUpdate(CryptobotBase):
    binance_api_url: str = "https://api.binance.com"
    binance_api_key: str
    binance_api_secret: str
    binance_config_base_currency: str
    binance_config_quote_currency: str
    binance_config_granularity: str = "15m"
    binance_config_live: bool = False
    binance_config_verbose : bool = True
    binance_config_graphs: bool = False
    binance_config_buymaxsize: float
    logger_filelog: bool = False
    logger_logfile: str = "pycryptobot.log"
    logger_fileloglevel: str
    logger_consolelog: bool = True
    logger_consoleloglevel: str
    telegram_client_id: str
    telegram_token: str


class CryptobotDelete(CryptobotBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class CryptobotInDBBase(CryptobotBase):
    id: int
    user_id: int
    user: User
    
    binance_api_url: str = "https://api.binance.com"
    binance_api_key: str
    binance_api_secret: str
    binance_config_base_currency: str
    binance_config_quote_currency: str
    binance_config_granularity: str = "15m"
    binance_config_live: bool = False
    binance_config_verbose : bool = True
    binance_config_graphs: bool = False
    binance_config_buymaxsize: float
    logger_filelog: bool = False
    logger_logfile: str = "pycryptobot.log"
    logger_fileloglevel: str
    logger_consolelog: bool = True
    logger_consoleloglevel: str
    telegram_client_id: str
    telegram_token: str
    
    created_on: Optional[datetime]
    updated_on: Optional[datetime]

    class Config:
        orm_mode = True


class Cryptobot(CryptobotInDBBase):
    pass


class CryptobotInDB(CryptobotInDBBase):
    pass
