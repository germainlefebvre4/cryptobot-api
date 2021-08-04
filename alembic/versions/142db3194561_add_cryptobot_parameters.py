"""Add cryptobot parameters

Revision ID: 142db3194561
Revises: 6fa487e817b6
Create Date: 2021-08-03 17:38:40.011443

"""
from alembic import op
from sqlalchemy import (
    Boolean, Column, ForeignKey, Integer, Float, String, DateTime, Date, Time)
import sqlalchemy as sa
from sqlalchemy import orm

from app.models import Cryptobot

# revision identifiers, used by Alembic.
revision = '142db3194561'
down_revision = '6fa487e817b6'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    op.add_column('cryptobots', Column('binance_config_disablebullonly', Boolean, default=False))
    op.add_column('cryptobots', Column('binance_config_disablebuynearhigh', Boolean, default=False))
    op.add_column('cryptobots', Column('binance_config_disablebuymacd', Boolean, default=False))
    op.add_column('cryptobots', Column('binance_config_disablebuyema', Boolean, default=False))
    op.add_column('cryptobots', Column('binance_config_disablebuyobv', Boolean, default=False))
    op.add_column('cryptobots', Column('binance_config_disablebuyelderray', Boolean, default=False))
    op.add_column('cryptobots', Column('binance_config_disablefailsafefibonaccilow', Boolean, default=False))
    op.add_column('cryptobots', Column('binance_config_disablefailsafelowerpcnt', Boolean, default=False))
    op.add_column('cryptobots', Column('binance_config_disableprofitbankupperpcnt', Boolean, default=False))
    op.add_column('cryptobots', Column('binance_config_disableprofitbankfibonaccihigh', Boolean, default=False))
    op.add_column('cryptobots', Column('binance_config_disableprofitbankreversal', Boolean, default=False))

    for cryptobot in session.query(Cryptobot):
        cryptobot.binance_config_disablebullonly = False
        cryptobot.binance_config_disablebullonly = False
        cryptobot.binance_config_disablebuynearhigh = False
        cryptobot.binance_config_disablebuymacd = False
        cryptobot.binance_config_disablebuyema = False
        cryptobot.binance_config_disablebuyobv = False
        cryptobot.binance_config_disablebuyelderray = False
        cryptobot.binance_config_disablefailsafefibonaccilow = False
        cryptobot.binance_config_disablefailsafelowerpcnt = False
        cryptobot.binance_config_disableprofitbankupperpcnt = False
        cryptobot.binance_config_disableprofitbankfibonaccihigh = False
        cryptobot.binance_config_disableprofitbankreversal = False

    session.commit()


def downgrade():
    op.drop_column('cryptobots', 'binance_config_disablebullonly')
    op.drop_column('cryptobots', 'binance_config_disablebuynearhigh')
    op.drop_column('cryptobots', 'binance_config_disablebuymacd')
    op.drop_column('cryptobots', 'binance_config_disablebuyema')
    op.drop_column('cryptobots', 'binance_config_disablebuyobv')
    op.drop_column('cryptobots', 'binance_config_disablebuyelderray')
    op.drop_column('cryptobots', 'binance_config_disablefailsafefibonaccilow')
    op.drop_column('cryptobots', 'binance_config_disablefailsafelowerpcnt')
    op.drop_column('cryptobots', 'binance_config_disableprofitbankupperpcnt')
    op.drop_column('cryptobots', 'binance_config_disableprofitbankfibonaccihigh')
    op.drop_column('cryptobots', 'binance_config_disableprofitbankreversal')

