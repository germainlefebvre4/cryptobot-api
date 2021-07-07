"""First revision

Revision ID: f71ee231a6dc
Revises: 6e523d653806
Create Date: 2020-11-09 12:15:11.582850

"""
from alembic import op
from sqlalchemy import (
    Boolean, Column, ForeignKey, Integer, Float, String, DateTime, Date, Time)
from sqlalchemy.dialects.postgresql import JSON

# revision identifiers, used by Alembic.
revision = 'f71ee231a6dc'
down_revision = '6e523d653806'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        Column('id', Integer, primary_key=True, index=True),
        Column('email', String, unique=True, index=True),
        Column('firstname', String, index=True),
        Column('hashed_password', String),
        Column('is_active', Boolean, default=True),
        Column('is_user', Boolean, default=True),
        Column('is_superuser', Boolean, default=False),
    )
    op.create_index(
      op.f("ix_user_email"), "users", ["email"], unique=False)
    op.create_index(
      op.f("ix_user_firstname"), "users", ["firstname"], unique=False)

    op.create_table(
        'cryptobots',
        Column('id', Integer, primary_key=True, index=True),
        
        Column('binance_api_url', String),
        Column('binance_api_key', String),
        Column('binance_api_secret', String),
        Column('binance_config_base_currency', String),
        Column('binance_config_quote_currency', String),
        Column('binance_config_granularity', String),
        Column('binance_config_live', Boolean),
        Column('binance_config_verbose', Boolean),
        Column('binance_config_graphs', Boolean),
        Column('binance_config_buymaxsize', Float),
        Column('logger_filelog', Boolean),
        Column('logger_logfile', String),
        Column('logger_fileloglevel', String),
        Column('logger_consolelog', Boolean),
        Column('logger_consoleloglevel', String),
        Column('telegram_client_id', String),
        Column('telegram_token', String),

        Column('created_on', DateTime),
        Column('updated_on', DateTime),
        Column(
            'user_id', Integer,
            ForeignKey(
                'users.id', name='fk_cryptobot_user_id',
                ondelete='CASCADE'),
            nullable=False)
    )

def downgrade():
    op.drop_index("ix_user_firstname", table_name="users")
    op.drop_index("ix_user_email", table_name="users")
    op.drop_constraint(
        "fk_cryptobot_user_id", "cryptobots", type_="foreignkey")
    op.drop_table("cryptobots")
    op.drop_table("users")
