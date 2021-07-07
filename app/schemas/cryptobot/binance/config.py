from typing import Optional
from enum import Enum, IntEnum

from pydantic import BaseModel


class BinanceConfigBase(BaseModel):
    base_currency: str
    quote_currency: str
    granularity: str = "15m"
    live: bool = False # enum(0, 1) = 0
    verbose : bool = True # enum(0, 1) = 1
    graphs: bool = False # enum(0, 1) = 0
    buymaxsize: float


class BinanceConfigCreate(BinanceConfigBase):
    base_currency: str
    quote_currency: str
    granularity: str = "15m"
    live: bool = False # enum(0, 1) = 0
    verbose : bool = True # enum(0, 1) = 1
    graphs: bool = False # enum(0, 1) = 0
    buymaxsize: float


class BinanceConfig(BinanceConfigBase):
    pass
