from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class BinanceAccount(Base):
    __tablename__ = "binance_accounts"

    id = Column(Integer, primary_key=True, index=True)
    binance_api_key = Column(String, unique=True, index=True, nullable=False)
    binance_api_secret = Column(String, index=True, nullable=False)

    created_on = Column(DateTime)
    updated_on = Column(DateTime)

    # user_id = Column(
    #     Integer,
    #     ForeignKey("users.id", ondelete='CASCADE'),
    #     nullable=False)
    # user = relationship("User", foreign_keys=[user_id])

    # cryptobots = relationship("Cryptobot", back_populates='binance_account')


    # cryptobots = relationship(
    #     'cryptobots',
    #     primaryjoin="BinanceAccount.id == Cryptobot.binance_account_id")

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete='CASCADE'),
        nullable=True)
    user = relationship("User", foreign_keys=[user_id])

    cryptobots = relationship("Cryptobot", back_populates='binance_account')
