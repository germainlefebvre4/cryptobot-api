from typing import Optional

from pydantic import BaseModel
from app.schemas.cryptobot.binance.config import BinanceConfig

class BinanceBase(BaseModel):
    api_url: str = "https://api.binance.com"
    api_key: str
    api_secret: str
    config: BinanceConfig


class BinanceCreate(BinanceBase):
    api_url: str = "https://api.binance.com"
    api_key: str
    api_secret: str
    config: BinanceConfig


class Binance(BinanceBase):
    pass
