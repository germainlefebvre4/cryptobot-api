from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import json
import math

from typing import Any, List, Optional, Dict

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Cryptobot])
def read_cryptobots(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve cryptobots.
    """
    if crud.user.is_superuser(current_user):
        cryptobots = crud.cryptobot.get_multi(db, skip=skip, limit=limit)
    else:
        cryptobots = crud.cryptobot.get_multi_by_user(
            db=db, user_id=current_user.id, skip=skip, limit=limit
        )
    # for cryptobot in cryptobots:
    #     tmp = json.loads(cryptobot["weekdays"])
    #     cryptobot["weekdays"] = tmp
    return cryptobots


@router.post("/", response_model=schemas.Cryptobot)
def create_cryptobot(
    *,
    db: Session = Depends(deps.get_db),
    cryptobot_in: schemas.CryptobotCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new cryptobot.
    """
    if crud.user.get(db, id=current_user.id) or crud.user.get(db, id=current_user.id):
        pass
    else:
        raise HTTPException(status_code=400, detail="User not found")
    cryptobot = crud.cryptobot.create_with_owner(
        db=db, obj_in=cryptobot_in, user_id=current_user.id)
    return cryptobot


@router.put("/{id}", response_model=schemas.Cryptobot)
def update_cryptobot(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    cryptobot_in: schemas.CryptobotUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an cryptobot.
    """
    cryptobot = crud.cryptobot.get(db=db, id=id)
    if not cryptobot:
        raise HTTPException(status_code=404, detail="Cryptobot not found")
    if (not crud.user.is_superuser(current_user) and
            (cryptobot.user_id != current_user.id)):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    cryptobot = crud.cryptobot.update(db=db, db_obj=cryptobot, obj_in=cryptobot_in)
    return cryptobot


@router.get("/{id}", response_model=schemas.Cryptobot)
def read_cryptobot(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get cryptobot by ID.
    """
    cryptobot = crud.cryptobot.get(db=db, id=id)
    if not cryptobot:
        raise HTTPException(status_code=404, detail="Cryptobot not found")
    if (not crud.user.is_superuser(current_user) and
            (cryptobot.user_id != current_user.id)):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return cryptobot


@router.delete("/{id}", response_model=schemas.CryptobotDelete)
def delete_cryptobot(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an cryptobot.
    """
    cryptobot = crud.cryptobot.get(db=db, id=id)
    if not cryptobot:
        raise HTTPException(status_code=404, detail="Cryptobot not found")
    if (not crud.user.is_superuser(current_user) and
            (cryptobot.user_id != current_user.id)):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    cryptobot = crud.cryptobot.remove(db=db, id=id)
    return cryptobot
