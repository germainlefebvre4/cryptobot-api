from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.security.api_key import APIKey

from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings

router = APIRouter()



@router.get("/{user_id}", response_model=schemas.User)
def read_user_by_id_with_apikey(
    user_id: int,
    api_key: APIKey = Depends(deps.get_api_key),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = crud.user.get(db, id=user_id)
    return user
