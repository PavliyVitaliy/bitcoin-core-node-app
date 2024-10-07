"""create transaction table

Revision ID: 3d39faa3010d
Revises: 
Create Date: 2024-10-07 12:14:53.528830

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3d39faa3010d"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "transactions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("tx_id", sa.String(), nullable=False),
        sa.Column("input_address", sa.String(), nullable=False),
        sa.Column("output_address", sa.String(), nullable=False),
        sa.Column("amount", sa.Numeric(), nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
        sa.Column("vouts", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_transactions")),
        sa.UniqueConstraint("id", name=op.f("uq_transactions_id")),
        sa.UniqueConstraint("tx_id", name=op.f("uq_transactions_tx_id")),
    )


def downgrade() -> None:
    op.drop_table("transactions")
