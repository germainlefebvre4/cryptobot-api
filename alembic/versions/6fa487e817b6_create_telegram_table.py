"""Create telegram table

Revision ID: 6fa487e817b6
Revises: 573bb86269e5
Create Date: 2021-08-01 15:42:04.630517

"""
from alembic import op
from sqlalchemy import (
    Boolean, Column, ForeignKey, Integer, Float, String, DateTime, Date, Time)
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6fa487e817b6'
down_revision = '573bb86269e5'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'telegrams',
        Column('id', Integer, primary_key=True, index=True),

        Column('client_id', String, unique=True),
        Column('token', String),
        
        Column('created_on', DateTime),
        Column('updated_on', DateTime),
        Column(
            'user_id', Integer,
            ForeignKey(
                'users.id', name='fk_telegram_user_id',
                ondelete='CASCADE'),
            nullable=False)
    )

    op.add_column(
        'cryptobots',
        Column(
            'telegram_id', Integer,
            ForeignKey(
                'telegrams.id', name='fk_cryptobot_telegram_id',
                ondelete='CASCADE'),
            nullable=False)
        # )
    )

    op.drop_column('cryptobots', 'telegram_client_id')
    op.drop_column('cryptobots', 'telegram_token')



def downgrade():
    op.drop_constraint(
        "fk_cryptobot_telegram_id", "cryptobots", type_="foreignkey")
    op.drop_constraint(
        "fk_telegram_user_id", "telegrams", type_="foreignkey")
    op.drop_table("telegrams")
