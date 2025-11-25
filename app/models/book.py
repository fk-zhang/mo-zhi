from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Text, UniqueConstraint, ForeignKey

from ..core.session import Base


class Book(Base):
    __tablename__ = "books"
    __table_args__ = (
        UniqueConstraint("user_id", "slug", name="uq_book_user_slug"),
        UniqueConstraint("user_id", "name", name="uq_book_user_name"),
        {"comment": "书籍/项目：用于区分不同世界设定"},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, comment="创建者用户ID")

    name: Mapped[str] = mapped_column(String(128), nullable=False, comment="书名/项目名")
    slug: Mapped[str] = mapped_column(String(128), nullable=False, comment="唯一短标识（用于URL/区分）")
    subtitle: Mapped[str | None] = mapped_column(String(256), nullable=True, comment="副标题/系列名")
    protagonist_name: Mapped[str | None] = mapped_column(String(128), nullable=True, comment="主角名称（可为空）")
    description: Mapped[str | None] = mapped_column(Text, nullable=True, comment="世界观/书籍简介")
    cover_url: Mapped[str | None] = mapped_column(String(256), nullable=True, comment="封面地址（可选）")
    status: Mapped[str | None] = mapped_column(String(32), nullable=True, comment="状态（连载/完结/大纲中 等）")
    tags: Mapped[str | None] = mapped_column(String(256), nullable=True, comment="标签（逗号/JSON均可）")
