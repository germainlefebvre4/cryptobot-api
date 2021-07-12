from sqlalchemy import Column, ForeignKey, Integer, Float, Date, DateTime, String, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Cryptobot(Base):
    __tablename__ = "cryptobots"

    id = Column(Integer, primary_key=True, index=True)
    customer = Column(String)
    binance_api_url = Column(String, default="https://api.binance.com")
    binance_api_key = Column(String, nullable=False)
    binance_api_secret = Column(String, nullable=False)
    binance_config_base_currency = Column(String, nullable=False)
    binance_config_quote_currency = Column(String, nullable=False)
    binance_config_granularity = Column(String, default="15m")
    binance_config_live = Column(Boolean, default=False)
    binance_config_verbose = Column(Boolean, default=True)
    binance_config_graphs = Column(Boolean, default=False)
    binance_config_buymaxsize = Column(Float, nullable=False)
    binance_config_sellupperpcnt = Column(Float, nullable=False)
    binance_config_selllowerpcnt = Column(Float, nullable=False)
    logger_filelog = Column(Boolean, default=False)
    logger_logfile = Column(String, default="pycryptobot.log")
    logger_fileloglevel = Column(String, default="INFO")
    logger_consolelog = Column(Boolean, default=True)
    logger_consoleloglevel = Column(String, default="INFO")
    telegram_client_id = Column(String, nullable=False)
    telegram_token = Column(String, nullable=False)
    
    created_on = Column(DateTime)
    updated_on = Column(DateTime)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete='CASCADE'),
        nullable=False)

    user = relationship("User", foreign_keys=[user_id])
