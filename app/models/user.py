from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String

from ..core.session import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
