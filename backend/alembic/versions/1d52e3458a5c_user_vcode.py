"""user_vcode

Revision ID: 1d52e3458a5c
Revises: 55bcb87abbaf
Create Date: 2024-11-01 13:22:52.326393

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '1d52e3458a5c'
down_revision: Union[str, None] = '55bcb87abbaf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('vcode', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'vcode')
    # ### end Alembic commands ###
