import datetime

from .mixing import CRUDMix
from .db_instance import db
from sqlalchemy import DateTime, Boolean, Integer, Column
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Model(CRUDMix, db.Model):
    __abstract__ = True


class SurrogatePK(Base):

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    deleted = db.Column(db.Boolean, nullable=False)
    modified = db.Column(db.DateTime(timezone=True))
    created = db.Column(db.DateTime(timezone=True))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.deleted = kwargs.get("deleted", False)
        self.modified = kwargs.get("modified", datetime.datetime.now())
        self.created = kwargs.get("created", datetime.datetime.now())

    @classmethod
    def get_by_id(cls, id):
        if any((isinstance(id, str) and id.isdigit(), isinstance(id, (int, float))),):
            with db.session.no_autoflush:
                return cls.query.get_or_404(int(id))

    @classmethod
    def delete_by_ids(cls, ids, commit=True):
        kw = [{"id": id, "deleted": True} for id in ids]
        db.session.bulk_update_mappings(cls, kw)
        if commit:
            db.session.commit()

    @classmethod
    def delete_by_id(cls, id, commit=True):
        item = cls.get_by_id(id)
        item.delete(commit)

    @classmethod
    def update_by_id(cls, id, schema, instance, commit=True):
        item = cls.get_by_id(id)
        item.update_by_ma(schema, instance, commit=commit)
        return item
