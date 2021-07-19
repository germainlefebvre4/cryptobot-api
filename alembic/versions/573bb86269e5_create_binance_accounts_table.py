"""Create binance_accounts table

Revision ID: 573bb86269e5
Revises: f71ee231a6dc
Create Date: 2021-07-17 06:37:19.252974

"""
from alembic import op
from sqlalchemy import (
    Boolean, Column, ForeignKey, Integer, Float, String, DateTime, Date, Time)
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '573bb86269e5'
down_revision = 'f71ee231a6dc'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'binance_accounts',
        Column('id', Integer, primary_key=True, index=True),

        Column('binance_api_url', String, nullable=False),
        Column('binance_api_key', String, unique=True),
        Column('binance_api_secret', String),
        
        Column('created_on', DateTime),
        Column('updated_on', DateTime),
        Column(
            'user_id', Integer,
            ForeignKey(
                'users.id', name='fk_binance_account_user_id',
                ondelete='CASCADE'),
            nullable=False)
    )

    op.add_column(
        'cryptobots',
        Column(
            'binance_account_id', Integer,
            ForeignKey(
                'binance_accounts.id', name='fk_cryptobot_binance_account_id',
                ondelete='CASCADE'),
            nullable=False)
    )

    op.drop_column('cryptobots', 'binance_api_key')
    op.drop_column('cryptobots', 'binance_api_secret')



def downgrade():
    op.drop_constraint(
        "fk_cryptobot_binance_account_id", "cryptobots", type_="foreignkey")
    op.drop_constraint(
        "fk_binance_account_user_id", "binance_accounts", type_="foreignkey")
    op.drop_table("binance_accounts")
