from fastapi import APIRouter

from app.api.api_v1.endpoints import (
    cryptobots,login, users, utils)

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(cryptobots.router, prefix="/cryptobots", tags=["cryptobots"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
