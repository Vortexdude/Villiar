"""Create admin user

Revision ID: 34ec6eb7567d
Revises: 8ee7e990a280
Create Date: 2024-06-25 18:09:41.211558

"""
from typing import Sequence, Union
from uuid import uuid4
from alembic import op, context
import sqlalchemy as sa
from datetime import datetime, UTC
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash
from Viliar.src.views.auth.models import UserModel, Role


# revision identifiers, used by Alembic.
revision: str = '34ec6eb7567d'
down_revision: Union[str, None] = '8ee7e990a280'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

config = context.get_context().config
admin_password = config.get_main_option('admin_pass')
guest_password = config.get_main_option('guest_pass')


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
    password=generate_password_hash(admin_password),
    active=True,
    created_datatime=now_in_utc(),
    last_login=now_in_utc()

)
guest_user = dict(
    id=str(uuid4()),
    email="nitin@gmail.com",
    username="nnamdev",
    fullname="Nitin Namdev",
    password=generate_password_hash(guest_password),
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

    session = Session(bind=connection)
    admin_user_id = session.query(UserModel).filter_by(username=admin_user['username']).first().id
    guest_user_id = session.query(UserModel).filter_by(username=guest_user['username']).first().id
    admin_role_id = session.query(Role).filter_by(name=admin_role['name']).first().id
    guest_role_id = session.query(Role).filter_by(name=guest_role['name']).first().id

    op.bulk_insert(
        role_associations_table,
        [
            {'user_id': admin_user_id, 'role_id': admin_role_id},
            {'user_id': guest_user_id, 'role_id': guest_role_id}
        ]
    )


def downgrade() -> None:
    # Delete initial data from users
    op.execute("DELETE FROM users WHERE email IN ('admin@viliar.com', 'nitin@gmail.com')")

    # Delete initial data from roles
    op.execute("DELETE FROM roles WHERE name IN ('admin', 'guest')")

    op.execute("DELETE FROM roles WHERE name IN ('admin', 'user')")

