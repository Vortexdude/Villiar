"""Insert admin and normal roles with policies

Revision ID: bb8538362e8e
Revises: 514833f6866d
Create Date: 2024-06-12 22:41:59.153015

"""
from typing import Sequence, Union
from datetime import datetime, UTC
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from uuid import uuid4

# revision identifiers, used by Alembic.
revision: str = 'bb8538362e8e'
down_revision: Union[str, None] = '514833f6866d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def now_in_utc():
    return datetime.now(UTC)


def upgrade():
    # Define tables as per previous migration
    users_table = table('users',
                        column('id', sa.String),
                        column('username', sa.String),
                        column('date_created', sa.DateTime(timezone=True)),
                        column('active', sa.Boolean)
                        )

    roles_table = table('roles',
                        column('id', sa.String),
                        column('name', sa.String)
                        )

    policies_table = table('policies',
                           column('id', sa.String),
                           column('name', sa.String),
                           column('description', sa.String)
                           )

    user_roles_table = table('user_roles',
                             column('user_id', sa.String),
                             column('role_id', sa.String)
                             )

    role_policies_table = table('role_policies',
                                column('role_id', sa.String),
                                column('policy_id', sa.String)
                                )

    # Generate UUIDs for new entries
    admin_user_id = str(uuid4())
    guest_user_id = str(uuid4())
    admin_role_id = str(uuid4())
    guest_role_id = str(uuid4())
    admin_policy_id = str(uuid4())
    guest_policy_id = str(uuid4())

    # Insert admin and normal user
    op.bulk_insert(users_table, [
        {'id': admin_user_id, 'username': 'dudeperfect', 'date_created': now_in_utc(), 'active': True},
        {'id': guest_user_id, 'username': 'dperfectdude', 'date_created': now_in_utc(), 'active': True}
    ])

    # Insert roles
    op.bulk_insert(roles_table, [
        {'id': admin_role_id, 'name': 'admin'},
        {'id': guest_role_id, 'name': 'guest'}
    ])

    # Insert policies
    op.bulk_insert(policies_table, [
        {'id': admin_policy_id, 'name': 'admin_resources', 'description': 'Policy for admin accounts'},
        {'id': guest_policy_id, 'name': 'guest_resources', 'description': 'Policy for guest account'}
    ])

    # Associate admin and normal user with their roles
    op.bulk_insert(user_roles_table, [
        {'user_id': admin_user_id, 'role_id': admin_role_id},
        {'user_id': guest_user_id, 'role_id': guest_role_id}
    ])

    # Associate roles with policies
    op.bulk_insert(role_policies_table, [
        {'role_id': admin_role_id, 'policy_id': admin_policy_id},
        {'role_id': admin_role_id, 'policy_id': guest_policy_id},
        {'role_id': guest_role_id, 'policy_id': admin_policy_id},
        {'role_id': guest_role_id, 'policy_id': guest_policy_id}
    ])


def downgrade():
    # Define tables for deletion as per upgrade
    user_roles_table = table('user_roles',
                             column('user_id', sa.String),
                             column('role_id', sa.String)
                             )

    role_policies_table = table('role_policies',
                                column('role_id', sa.String),
                                column('policy_id', sa.String)
                                )

    users_table = table('users',
                        column('id', sa.String),
                        column('username', sa.String)
                        )

    roles_table = table('roles',
                        column('id', sa.String),
                        column('name', sa.String)
                        )

    policies_table = table('policies',
                           column('id', sa.String),
                           column('name', sa.String)
                           )

    # Generate UUIDs for new entries
    admin_user_id = str(uuid4())
    guest_user_id = str(uuid4())
    admin_role_id = str(uuid4())
    guest_role_id = str(uuid4())
    guest_policy_id = str(uuid4())
    admin_policy_id = str(uuid4())

    # Delete role-policies associations
    op.execute(role_policies_table.delete().where(
        (role_policies_table.c.role_id == admin_role_id) & (role_policies_table.c.policy_id == admin_policy_id)
    ))
    op.execute(role_policies_table.delete().where(
        (role_policies_table.c.role_id == admin_role_id) & (role_policies_table.c.policy_id == guest_policy_id)
    ))
    op.execute(role_policies_table.delete().where(
        (role_policies_table.c.role_id == guest_role_id) & (role_policies_table.c.policy_id == admin_policy_id)
    ))
    op.execute(role_policies_table.delete().where(
        (role_policies_table.c.role_id == guest_role_id) & (role_policies_table.c.policy_id == guest_policy_id)
    ))

    # Delete user-roles associations
    op.execute(user_roles_table.delete().where(
        (user_roles_table.c.user_id == admin_user_id) & (user_roles_table.c.role_id == admin_role_id)
    ))
    op.execute(user_roles_table.delete().where(
        (user_roles_table.c.user_id == guest_user_id) & (user_roles_table.c.role_id == guest_role_id)
    ))

    # Delete policies
    op.execute(policies_table.delete().where(
        policies_table.c.id.in_([admin_policy_id, guest_policy_id])
    ))

    # Delete roles
    op.execute(roles_table.delete().where(
        roles_table.c.id.in_([admin_role_id, guest_role_id])
    ))

    # Delete users
    op.execute(users_table.delete().where(
        users_table.c.id.in_([admin_user_id, guest_user_id])
    ))
