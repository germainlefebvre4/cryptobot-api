from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.config import settings
# from app.db import base
from app.tests.utils.binance_account import create_random_binance_account
from app.tests.utils.telegram import create_random_telegram
from app.tests.utils.cryptobot import create_random_cryptobot

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    user_admin = crud.user.get_by_email(db, email=settings.USER_ADMIN_EMAIL)
    if not user_admin:
        user_in = schemas.UserCreate(
            email=settings.USER_ADMIN_EMAIL,
            firstname=settings.USER_ADMIN_FIRSTNAME,
            password=settings.USER_ADMIN_PASSWORD,
            is_superuser=True,
        )
        user_admin = crud.user.create(db, obj_in=user_in)

    user_test = crud.user.get_by_email(db, email=settings.USER_TEST_EMAIL)
    if not user_test:
        user_in = schemas.UserCreate(
            email=settings.USER_TEST_EMAIL,
            firstname=settings.USER_TEST_FIRSTNAME,
            password=settings.USER_TEST_PASSWORD,
            is_superuser=False,
        )
        user_test = crud.user.create(db, obj_in=user_in)
    
    binance_account_user_test = create_random_binance_account(db, user_id=user_test.id)
    telegram_user_test = create_random_telegram(db, user_id=user_test.id)
    cryptobot_user_test = create_random_cryptobot(db, user_id=user_test.id, binance_account_id=binance_account_user_test.id, telegram_id=telegram_user_test.id)

