from typing import Any

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
# from app.core.config import settings

router = APIRouter()


@router.get("/users/_count", status_code=status.HTTP_200_OK, response_model=schemas.MetricUserCount)
def get_users_count(
    db: Session = Depends(deps.get_db),
    # current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve users count.
    """
    threshold = 5
    
    count = crud.user.count(db)
    status = "ok" if count < threshold else "error"
    
    metric = schemas.MetricUserCount(
        count=count,
        status=status,
    )
    return metric

