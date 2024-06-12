"""Create users, roles, policies tables and association tables

Revision ID: 514833f6866d
Revises: 
Create Date: 2024-06-12 22:36:47.686492

"""
from typing import Sequence, Union
from uuid import uuid4
from alembic import op
import sqlalchemy as sa
from datetime import datetime, UTC

# revision identifiers, used by Alembic.
revision: str = '514833f6866d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
schema = 'public'


def upgrade() -> None:
    surrogate_pk = sa.Column('id', sa.String, primary_key=True, default=lambda: str(uuid4()))
    op.create_table(
        'users',
        surrogate_pk,
        sa.Column('username', sa.String, nullable=False),
        sa.Column('date_created', sa.DateTime(timezone=True), nullable=False, default=datetime.now(UTC),
                  onupdate=datetime.now(UTC)),
        sa.Column('active', sa.Boolean, nullable=False, default=True),
        schema=schema
    )
    op.create_table(
        'roles',
        surrogate_pk,
        sa.Column('name', sa.String, unique=True),
        schema='public'
    )

    op.create_table(
        'policies',
        surrogate_pk,
        sa.Column('name', sa.String, unique=True),
        sa.Column('description', sa.String),
        schema='public'
    )

    op.create_table(
        'user_roles',
        sa.Column('user_id', sa.String, sa.ForeignKey('public.users.id'), primary_key=True),
        sa.Column('role_id', sa.String, sa.ForeignKey('public.roles.id'), primary_key=True),
        schema='public'
    )

    op.create_table(
        'role_policies',
        sa.Column('role_id', sa.String, sa.ForeignKey('public.roles.id'), primary_key=True),
        sa.Column('policy_id', sa.String, sa.ForeignKey('public.policies.id'), primary_key=True),
        schema='public'
    )


def downgrade() -> None:
    # Drop association tables first
    op.drop_table('role_policies', schema='public')
    op.drop_table('user_roles', schema='public')

    # Drop main tables
    op.drop_table('policies', schema='public')
    op.drop_table('roles', schema='public')
    op.drop_table('users', schema='public')
