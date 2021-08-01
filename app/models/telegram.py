from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Telegram(Base):
    __tablename__ = "telegrams"

    id = Column(Integer, primary_key=True, index=True)
    
    client_id = Column(String, unique=True, index=True, nullable=False)
    token = Column(String, index=True, nullable=False)

    created_on = Column(DateTime)
    updated_on = Column(DateTime)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete='CASCADE'),
        nullable=True)
    user = relationship("User", foreign_keys=[user_id])

    cryptobots = relationship("Cryptobot", back_populates='telegram')
