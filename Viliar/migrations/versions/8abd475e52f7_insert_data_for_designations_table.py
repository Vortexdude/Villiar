"""insert data for designations table

Revision ID: 8abd475e52f7
Revises: 64fbb68f8fed
Create Date: 2024-06-26 21:37:59.502458

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from uuid import uuid4

# revision identifiers, used by Alembic.
revision: str = '8abd475e52f7'
down_revision: Union[str, None] = '64fbb68f8fed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


designation_table = sa.table(
    "designations",
    sa.column('id', sa.String),
    sa.column('title', sa.String)
)


def _uid() -> str:
    return str(uuid4()).split("-")[-1]


designations = [
    {"id": _uid(), "title": "Junior Software Engineer"},
    {"id": _uid(), "title": "Staff Software Engineer"},
    {"id": _uid(), "title": "Senior Software Engineer"},
    {"id": _uid(), "title": "Associate Software Engineer"},
    {"id": _uid(), "title": "Software Engineer"},
    {"id": _uid(), "title": "Devops Engineer"},
    {"id": _uid(), "title": "SRE Engineer"},
    {"id": _uid(), "title": "Java Developer"},
    {"id": _uid(), "title": "Python Developer"},
    {"id": _uid(), "title": "Dotnet Developer"},
    {"id": _uid(), "title": "Automation Engineer"},
    {"id": _uid(), "title": "Project Manager"},
    {"id": _uid(), "title": "Software Tester"},
    {"id": _uid(), "title": "QA Tester"},
    {"id": _uid(), "title": "Automation QA Engineer"},
]


def upgrade() -> None:
    op.bulk_insert(
        designation_table,
        designations
    )


def downgrade() -> None:
    pass
