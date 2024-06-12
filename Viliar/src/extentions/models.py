from . sqla import HelperMethods, Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Boolean

class UserModel(HelperMethods, Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, )