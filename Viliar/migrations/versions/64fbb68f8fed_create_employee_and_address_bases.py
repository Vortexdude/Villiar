"""create employee and address bases

Revision ID: 64fbb68f8fed
Revises: 34ec6eb7567d
Create Date: 2024-06-26 19:23:39.056965

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '64fbb68f8fed'
down_revision: Union[str, None] = '34ec6eb7567d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create designations table
    op.create_table(
        'designations',
        sa.Column('id', sa.String, primary_key=True),
        sa.Column('title', sa.String(length=100), nullable=True, unique=True),
    )

    # Create addresses table
    op.create_table(
        'addresses',
        sa.Column('id', sa.String, primary_key=True),
        sa.Column('street', sa.String(length=100), nullable=True),
        sa.Column('city', sa.String(length=50), nullable=True),
        sa.Column('state', sa.String(length=30), nullable=True),
        sa.Column('zip_code', sa.String(length=10), nullable=True),
    )

    # Create employees table
    op.create_table(
        'employees',
        sa.Column('id', sa.String, primary_key=True),
        sa.Column('name', sa.String(length=50), nullable=False, unique=True),
        sa.Column('salary', sa.Integer, nullable=False),
        sa.Column('joining_date', sa.DateTime, nullable=False, default=sa.func.now()),
        sa.Column('total_experience', sa.Integer, nullable=False),
        sa.Column('designation_id', sa.String, sa.ForeignKey('designations.id'), nullable=False),
        sa.Column('address_id', sa.String, sa.ForeignKey('addresses.id'), nullable=False),
    )


def downgrade() -> None:
    pass
