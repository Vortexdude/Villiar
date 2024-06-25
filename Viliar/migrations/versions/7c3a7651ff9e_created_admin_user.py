"""created admin user

Revision ID: 7c3a7651ff9e
Revises: c52ed9b1bb31
Create Date: 2024-06-24 23:15:19.123265

"""
from typing import Sequence, Union
from uuid import uuid4
from alembic import op
import sqlalchemy as sa
from datetime import datetime, UTC

# revision identifiers, used by Alembic.
revision: str = '7c3a7651ff9e'
down_revision: Union[str, None] = 'c52ed9b1bb31'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def now_in_utc() -> datetime:
    """Current time in UTC"""
    return datetime.now(tz=UTC)

# ------- define all the tables - - - - - -


roles_table = sa.table(
    "roles",
    sa.column('id', sa.String),
    sa.column('name', sa.String),
    sa.column('description', sa.String),
    sa.column('paths', sa.String)
)

users_table = sa.table(
    "users",
    sa.column("id", sa.String),
    sa.column('username', sa.String),
    sa.column('fullname', sa.String),
    sa.column('email', sa.String),
    sa.column('password', sa.String),
    sa.column('active', sa.Boolean),
    sa.column('created_datatime', sa.DateTime),
    sa.column('last_login', sa.DateTime)
)

role_associations_table = sa.table(
    'role_associations',
    sa.column('user_id', sa.String),
    sa.column('role_id', sa.String)

)

# ------- Define the users - - - - - -


admin_user = dict(
    id=str(uuid4()),
    email="admin@viliar.com",
    username="Admin",
    fullname="Viliar Dev",
    password="moyom#234",
    active=True,
    created_datatime=now_in_utc(),
    last_login=now_in_utc()

)
guest_user = dict(
    id=str(uuid4()),
    email="nitin@gmail.com",
    username="nnamdev",
    fullname="Nitin Namdev",
    password="string",
    active=True,
    created_datatime=now_in_utc(),
    last_login=now_in_utc()
)

admin_role = dict(
    id=str(uuid4()),
    name='admin',
    description='Administrator role',
    paths='/admin/*',
)

guest_role = dict(
    id=str(uuid4()),
    name='guest',
    description='Guest role',
    paths='/users/*',
)


def upgrade() -> None:
    op.bulk_insert(roles_table, [guest_role, admin_role])
    op.bulk_insert(users_table, [admin_user, guest_user])
    connection = op.get_bind()
    admin_user_id = connection.execute(sa.select([users_table.c.id]).where(users_table.c.username == 'admin')).fetchone()[0]
    user_user_id = connection.execute(sa.select([users_table.c.id]).where(users_table.c.username == 'guest')).fetchone()[0]

    admin_role_id = connection.execute(sa.select([roles_table.c.id]).where(roles_table.c.name == 'admin')).fetchone()[0]
    user_role_id = connection.execute(sa.select([roles_table.c.id]).where(roles_table.c.name == 'guest')).fetchone()[0]
    op.bulk_insert(
            role_associations_table,
            [
                {'user_id': admin_user_id, 'role_id': admin_role_id},
                {'user_id': user_user_id, 'role_id': user_role_id}
            ]
        )


def downgrade() -> None:
    # Delete initial data from users
    op.execute("DELETE FROM users WHERE email IN ('admin@viliar.com', 'nitin@gmail.com')")

    # Delete initial data from roles
    op.execute("DELETE FROM roles WHERE name IN ('admin', 'guest')")

    op.execute("DELETE FROM roles WHERE name IN ('admin', 'user')")
