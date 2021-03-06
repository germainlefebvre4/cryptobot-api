from sqlalchemy import Column, ForeignKey, Integer, Float, Date, DateTime, String, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Cryptobot(Base):
    __tablename__ = "cryptobots"

    id = Column(Integer, primary_key=True, index=True)
    binance_config_base_currency = Column(String, nullable=False)
    binance_config_quote_currency = Column(String, nullable=False)
    binance_config_granularity = Column(String, default="15m")
    binance_config_live = Column(Boolean, default=False)
    binance_config_verbose = Column(Boolean, default=True)
    binance_config_graphs = Column(Boolean, default=False)
    binance_config_buymaxsize = Column(Float, nullable=False)
    binance_config_sellupperpcnt = Column(Float, nullable=False)
    binance_config_selllowerpcnt = Column(Float, nullable=False)
    binance_config_disablebullonly = Column(Boolean, default=False)
    binance_config_disablebuynearhigh = Column(Boolean, default=False)
    binance_config_disablebuymacd = Column(Boolean, default=False)
    binance_config_disablebuyema = Column(Boolean, default=False)
    binance_config_disablebuyobv = Column(Boolean, default=False)
    binance_config_disablebuyelderray = Column(Boolean, default=False)
    binance_config_disablefailsafefibonaccilow = Column(Boolean, default=False)
    binance_config_disablefailsafelowerpcnt = Column(Boolean, default=False)
    binance_config_disableprofitbankupperpcnt = Column(Boolean, default=False)
    binance_config_disableprofitbankfibonaccihigh = Column(Boolean, default=False)
    binance_config_disableprofitbankreversal = Column(Boolean, default=False)
    logger_filelog = Column(Boolean, default=False)
    logger_logfile = Column(String, default="pycryptobot.log")
    logger_fileloglevel = Column(String, default="INFO")
    logger_consolelog = Column(Boolean, default=True)
    logger_consoleloglevel = Column(String, default="INFO")
    
    created_on = Column(DateTime)
    updated_on = Column(DateTime)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete='CASCADE'),
        nullable=False)
    binance_account_id = Column(
        Integer,
        ForeignKey("binance_accounts.id", ondelete='CASCADE'),
        nullable=False)
    telegram_id = Column(
        Integer,
        ForeignKey("telegrams.id", ondelete='CASCADE'),
        nullable=True)

    user = relationship("User", foreign_keys=[user_id])
    binance_account = relationship("BinanceAccount", foreign_keys=[binance_account_id])
    telegram = relationship("Telegram", foreign_keys=[telegram_id])