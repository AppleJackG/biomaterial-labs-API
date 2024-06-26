"""change summary table

Revision ID: 7a55d98a76f2
Revises: dda4002b9f73
Create Date: 2024-04-05 13:52:24.271056

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7a55d98a76f2'
down_revision: Union[str, None] = 'dda4002b9f73'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('summary_table', sa.Column('styrol_polymerization_bulk', sa.String(), nullable=True))
    op.drop_column('summary_table', 'styrol_polymerization_bulk_status')
    op.drop_column('summary_table', 'styrol_polymerization_bulk_mark')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('summary_table', sa.Column('styrol_polymerization_bulk_mark', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.add_column('summary_table', sa.Column('styrol_polymerization_bulk_status', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.drop_column('summary_table', 'styrol_polymerization_bulk')
    # ### end Alembic commands ###
