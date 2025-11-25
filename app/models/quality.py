from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Text, ForeignKey, UniqueConstraint

from ..core.session import Base


class QualityDef(Base):
    __tablename__ = "quality_defs"
    __table_args__ = (
        UniqueConstraint("user_id", "book_id", "code", name="uq_quality_user_book_code"),
        UniqueConstraint("user_id", "book_id", "name", name="uq_quality_user_book_name"),
        {"comment": "用户在书籍维度的自定义品质定义：名称/代码/排序/颜色/描述"},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, comment="用户ID")
    book_id: Mapped[int] = mapped_column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False, comment="所属书籍ID")

    code: Mapped[str] = mapped_column(String(64), nullable=False, comment="品质代码（英文/唯一）")
    name: Mapped[str] = mapped_column(String(64), nullable=False, comment="品质名称（展示）")
    rank: Mapped[int] = mapped_column(Integer, nullable=False, comment="品质排序/等级（值越大代表等级越高）")
    color: Mapped[str | None] = mapped_column(String(32), nullable=True, comment="颜色（可用十六进制/预设名）")
    description: Mapped[str | None] = mapped_column(Text, nullable=True, comment="说明/备注")
