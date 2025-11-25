from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey, CheckConstraint, Enum as SAEnum
from enum import Enum

from ..core.session import Base


class TimelineEvent(Base):
    __tablename__ = "timeline_events"
    __table_args__ = {"comment": "时间线/历史事件：时间、地点、经过、影响"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    book_id: Mapped[int] = mapped_column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False, comment="所属书籍ID")
    title: Mapped[str] = mapped_column(String(128), nullable=False, index=True, comment="事件标题")
    time: Mapped[str | None] = mapped_column(String(64), nullable=True, comment="事件时间（可为纪元/年/月/日/序号等文本）")
    location_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("locations.id", ondelete="SET NULL"), nullable=True, comment="地点ID")
    description: Mapped[str | None] = mapped_column(Text, nullable=True, comment="事件经过/描述")
    impact: Mapped[str | None] = mapped_column(Text, nullable=True, comment="对世界/势力/人物的影响")


class EventParticipant(Base):
    __tablename__ = "event_participants"
    __table_args__ = {"comment": "事件参与人物关联"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    book_id: Mapped[int] = mapped_column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False, comment="所属书籍ID")
    event_id: Mapped[int] = mapped_column(Integer, ForeignKey("timeline_events.id", ondelete="CASCADE"), nullable=False, comment="事件ID")
    character_id: Mapped[int] = mapped_column(Integer, ForeignKey("characters.id", ondelete="CASCADE"), nullable=False, comment="人物ID")


class AcquisitionKind(str, Enum):
    """获取物类型：统一抽象功法/技能/灵宠/天材地宝/道具等"""

    SKILL = "skill"              # 功法/技能（建议以 ConceptItem.kind='skill' 表示）
    TECHNIQUE = "technique"      # 秘术/术法/神通（亦可用 ConceptItem）
    BEAST = "beast"              # 灵宠/契约兽（BeastPet）
    TREASURE = "treasure"        # 神器/法器/道具（ConceptItem.kind='treasure'）
    MATERIAL = "material"        # 天材地宝/材料（ConceptItem.kind='material'）
    OTHER = "other"              # 其它自定义


class EventAcquisition(Base):
    __tablename__ = "event_acquisitions"
    __table_args__ = (
        CheckConstraint(
            "(concept_item_id IS NOT NULL) + (beast_pet_id IS NOT NULL) + (custom_name IS NOT NULL) = 1",
            name="ck_event_acq_one_target",
        ),
        {"comment": "事件获取记录：某人物在某事件中获得功法/技能/灵宠/天材地宝等"},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    book_id: Mapped[int] = mapped_column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False, comment="所属书籍ID")
    event_id: Mapped[int] = mapped_column(Integer, ForeignKey("timeline_events.id", ondelete="CASCADE"), nullable=False, comment="事件ID")
    character_id: Mapped[int] = mapped_column(Integer, ForeignKey("characters.id", ondelete="CASCADE"), nullable=False, comment="获得者人物ID")

    kind: Mapped[AcquisitionKind] = mapped_column(SAEnum(AcquisitionKind, native_enum=True), nullable=False, comment="获取类型")

    # 目标引用三选一：概念/物品，或灵宠，或自定义名称
    concept_item_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("concept_items.id", ondelete="SET NULL"), nullable=True, comment="关联概念/物品ID（功法/法器/材料等）")
    beast_pet_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("beast_pets.id", ondelete="SET NULL"), nullable=True, comment="关联灵宠ID")
    custom_name: Mapped[str | None] = mapped_column(String(128), nullable=True, comment="自定义名称（无建档时使用）")

    quantity: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="数量（材料/道具时可用）")
    notes: Mapped[str | None] = mapped_column(Text, nullable=True, comment="备注/获取方式/限制条件等")
