from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Text, ForeignKey

from ..core.session import Base


class Character(Base):
    __tablename__ = "characters"
    __table_args__ = {"comment": "人物档案：基础信息、外貌、性格、背景、技能等"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    book_id: Mapped[int] = mapped_column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False, comment="所属书籍ID")
    name: Mapped[str] = mapped_column(String(64), nullable=False, index=True, comment="姓名")
    alias: Mapped[str | None] = mapped_column(String(128), nullable=True, comment="别名")
    gender: Mapped[str | None] = mapped_column(String(16), nullable=True, comment="性别")
    age: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="年龄")
    title: Mapped[str | None] = mapped_column(String(128), nullable=True, comment="身份/称号")
    appearance: Mapped[str | None] = mapped_column(Text, nullable=True, comment="外貌特征")
    personality: Mapped[str | None] = mapped_column(Text, nullable=True, comment="性格特点")
    background: Mapped[str | None] = mapped_column(Text, nullable=True, comment="背景故事")
    skills: Mapped[str | None] = mapped_column(Text, nullable=True, comment="技能/能力（可用JSON或换行分隔）")


class CharacterRelationship(Base):
    __tablename__ = "character_relationships"
    __table_args__ = {"comment": "人物-人物关系：如亲属/朋友/师徒/敌对等"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    book_id: Mapped[int] = mapped_column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False, comment="所属书籍ID")
    source_id: Mapped[int] = mapped_column(Integer, ForeignKey("characters.id", ondelete="CASCADE"), nullable=False, comment="源人物ID")
    target_id: Mapped[int] = mapped_column(Integer, ForeignKey("characters.id", ondelete="CASCADE"), nullable=False, comment="目标人物ID")
    relation_type: Mapped[str | None] = mapped_column(String(64), nullable=True, comment="关系类型（亲属/朋友/师徒/敌对等）")
    notes: Mapped[str | None] = mapped_column(Text, nullable=True, comment="关系备注")
