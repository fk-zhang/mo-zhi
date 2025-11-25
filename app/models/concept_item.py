from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Text, Enum as SAEnum, ForeignKey

from ..core.session import Base
from .enums import Quality
from .quality import QualityDef


class ConceptItem(Base):
    __tablename__ = "concept_items"
    __table_args__ = {"comment": "概念/物品档案：定义、规则、效果、限制"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    book_id: Mapped[int] = mapped_column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False, comment="所属书籍ID")
    name: Mapped[str] = mapped_column(String(128), nullable=False, index=True, comment="名称")
    kind: Mapped[str] = mapped_column(String(32), nullable=False, comment="类别（概念/物品/功法/神器/技能等）")
    quality: Mapped[Quality | None] = mapped_column(SAEnum(Quality, native_enum=True), nullable=True, comment="系统预设品质（凡/优/稀/史诗/传说/神话等）")
    quality_def_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("quality_defs.id", ondelete="SET NULL"), nullable=True, comment="用户自定义品质ID（若设置则优先于系统预设品质）")
    definition: Mapped[str | None] = mapped_column(Text, nullable=True, comment="定义/描述")
    rules: Mapped[str | None] = mapped_column(Text, nullable=True, comment="规则/原理")
    effects: Mapped[str | None] = mapped_column(Text, nullable=True, comment="效果/用途")
    limitations: Mapped[str | None] = mapped_column(Text, nullable=True, comment="限制条件")
