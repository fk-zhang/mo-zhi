from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Text, ForeignKey, Enum as SAEnum, UniqueConstraint

from ..core.session import Base
from .enums import Quality
from .quality import QualityDef


class BeastType(Base):
    __tablename__ = "beast_types"
    __table_args__ = (
        UniqueConstraint("book_id", "name", name="uq_beast_type_book_name"),
        {"comment": "灵兽/神兽 类型定义：生活习性、弱点、能力等"},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    book_id: Mapped[int] = mapped_column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False, comment="所属书籍ID")
    name: Mapped[str] = mapped_column(String(128), nullable=False, comment="类型名称（如青鸾、地火蜥等）")
    classification: Mapped[str | None] = mapped_column(String(64), nullable=True, comment="分类/属性（如飞禽/鳞甲/元素/圣兽/神兽等）")
    habitat: Mapped[str | None] = mapped_column(Text, nullable=True, comment="栖息地/分布区域")
    habits: Mapped[str | None] = mapped_column(Text, nullable=True, comment="生活习性/作息/群居或独居")
    diet: Mapped[str | None] = mapped_column(Text, nullable=True, comment="食性/偏好")
    temperament: Mapped[str | None] = mapped_column(Text, nullable=True, comment="性情（温顺/暴烈/狡黠等）")
    weaknesses: Mapped[str | None] = mapped_column(Text, nullable=True, comment="弱点/克制方式")
    abilities: Mapped[str | None] = mapped_column(Text, nullable=True, comment="典型能力/天赋（可列表/JSON）")
    element_affinity: Mapped[str | None] = mapped_column(String(64), nullable=True, comment="元素/属性亲和（火/雷/风/木/金等）")
    typical_realm: Mapped[str | None] = mapped_column(String(64), nullable=True, comment="常见境界范围")
    lifecycle: Mapped[str | None] = mapped_column(Text, nullable=True, comment="生命周期/成长阶段（幼生/成体/王者等）")
    rarity: Mapped[str | None] = mapped_column(String(32), nullable=True, comment="稀有度（可与品质协同或自定义）")
    description: Mapped[str | None] = mapped_column(Text, nullable=True, comment="类型简介/设定说明")


class BeastPet(Base):
    __tablename__ = "beast_pets"
    __table_args__ = {"comment": "灵兽/宠物档案：名称、境界、能力、所属人物"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    book_id: Mapped[int] = mapped_column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False, comment="所属书籍ID")
    name: Mapped[str] = mapped_column(String(128), nullable=False, index=True, comment="宠物名称")
    type_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("beast_types.id", ondelete="SET NULL"), nullable=True, comment="灵兽类型ID")
    realm: Mapped[str | None] = mapped_column(String(64), nullable=True, comment="境界/实力等级")
    quality: Mapped[Quality | None] = mapped_column(SAEnum(Quality, native_enum=True), nullable=True, comment="品质（凡/优/稀/史诗/传说/神话等）")
    quality_def_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("quality_defs.id", ondelete="SET NULL"), nullable=True, comment="用户自定义品质ID（若设置则优先于系统预设品质）")
    abilities: Mapped[str | None] = mapped_column(Text, nullable=True, comment="能力描述（可列表/JSON）")
    owner_character_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("characters.id", ondelete="SET NULL"), nullable=True, comment="所属人物ID")
