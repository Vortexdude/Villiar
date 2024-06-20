"""add last_login to users and update paths length in roles

Revision ID: 80bf904c8cc4
Revises: aec3bc17266b
Create Date: 2024-06-18 17:02:37.898905

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '80bf904c8cc4'
down_revision: Union[str, None] = 'aec3bc17266b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('last_login', sa.DateTime(), nullable=True))
    op.alter_column('roles', 'paths',
                    existing_type=sa.VARCHAR(length=50),
                    type_=sa.String(length=100),
                    existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
                    sa.Column('id', sa.VARCHAR(), autoincrement=False, nullable=False),
                    sa.Column('name', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
                    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.Column('paths', sa.VARCHAR(length=500), autoincrement=False, nullable=True),
                    sa.PrimaryKeyConstraint('id', name='roles_pkey')
                    )
    op.create_table('users',
                    sa.Column('id', sa.VARCHAR(), autoincrement=False, nullable=False),
                    sa.Column('username', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
                    sa.Column('fullname', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=False),
                    sa.Column('password', sa.VARCHAR(), autoincrement=False, nullable=False),
                    sa.Column('active', sa.BOOLEAN(), autoincrement=False, nullable=False),
                    sa.Column('created_datatime', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
                    sa.PrimaryKeyConstraint('id', name='users_pkey')
                    )
    # ### end Alembic commands ###
