from .db_instance import db
import arrow


class CRUDMix(object):
    @classmethod
    def create(cls, **kwargs):
        commit = kwargs.get("commit", True)
        instance = cls(**kwargs)
        return instance.save(commit)

    def update(self, commit=True, **kwargs):
        kwargs.pop("id", None)
        kwargs.pop("deleted", None)
        kwargs.pop("modified", None)
        kwargs.pop("created", None)

        for attr, value in kwargs.items():
            setattr(self, attr, value)

        setattr(self, "modified", arrow.now())
        return commit and self.save() or self

    def save(self, commit=True):
        setattr(self, "modified", arrow.now())
        db.session.add(self)

        if commit:
            self.commit()
        return self

    @staticmethod
    def commit():
        try:
            db.session.commit()
        except Exception as e:
            raise e
