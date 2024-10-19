"""audiofilepath

Revision ID: 6f6255f305b6
Revises: 0ef660ba61f9
Create Date: 2024-10-19 18:21:26.680946

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6f6255f305b6'
down_revision: Union[str, None] = '0ef660ba61f9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('lessons', sa.Column('audio_file_path', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('lessons', 'audio_file_path')
    # ### end Alembic commands ###
