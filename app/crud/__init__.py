from .crud_user import user
from .crud_cryptobot import cryptobot
from .crud_binance_account import binance_account
from .crud_telegram import telegram

# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from app.models.item import Item
# from app.schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
