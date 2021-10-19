from datetime import datetime
import json

from typing import List, Dict, Union, Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.binance_account import BinanceAccount
from app.models.user import User
from app.schemas.binance_account import BinanceAccountCreate, BinanceAccountUpdate


class CRUDBinanceAccount(CRUDBase[BinanceAccount, BinanceAccountCreate, BinanceAccountUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: BinanceAccountCreate, user_id: int,
    ) -> BinanceAccount:
        obj_in_data = jsonable_encoder(obj_in)
        created_on = datetime.now()
        db_obj = self.model(**obj_in_data, user_id=user_id,
            created_on=created_on)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[BinanceAccount]:
        return (
            db.query(self.model)
            .order_by(BinanceAccount.icreated_on.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_by_user(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[BinanceAccount]:
        return (
            db.query(self.model)
            .join(BinanceAccount.user)
            .filter(BinanceAccount.user_id == user_id)
            .order_by(BinanceAccount.created_on.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update(
        self,
        db: Session,
        *,
        db_obj: BinanceAccount,
        obj_in: Union[BinanceAccountUpdate, Dict[str, Any]]
    ) -> BinanceAccount:
        obj_data = jsonable_encoder(db_obj)
        updated_on = datetime.now()
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        update_data = {**update_data, **dict(updated_on=updated_on)}
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

binance_account = CRUDBinanceAccount(BinanceAccount)
