from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Text, ForeignKey, Boolean, UniqueConstraint, Enum as SAEnum
from enum import Enum

from ..core.session import Base


class LocationLevel(str, Enum):
    """地理层级枚举（网文常见层级）

    典型父子层级示例：
    GALAXY(星系) > PLANET(星球) > CONTINENT(大陆) > DOMAIN(域) > STATE(州) > PREFECTURE(郡) > CITY(城) > TOWN(镇) > VILLAGE(村)
    实际可按世界观自由组合。
    """

    GALAXY = "galaxy"          # 星系
    PLANET = "planet"          # 星球
    CONTINENT = "continent"    # 大陆
    DOMAIN = "domain"          # 域/界域/大域
    STATE = "state"            # 州/省级
    PREFECTURE = "prefecture"  # 郡/府/道
    CITY = "city"              # 城
    TOWN = "town"              # 镇
    VILLAGE = "village"        # 村


class Location(Base):
    __tablename__ = "locations"
    __table_args__ = (
        UniqueConstraint("book_id", "name", "level", "parent_id", name="uq_location_book_name_level_parent"),
        {"comment": "地点档案（网文地理层级）：星系/星球/大陆/域/州/城/镇/村 等，支持父子层级"},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    book_id: Mapped[int] = mapped_column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False, comment="所属书籍ID")
    name: Mapped[str] = mapped_column(String(128), nullable=False, index=True, comment="地点名称")
    level: Mapped[LocationLevel] = mapped_column(
        SAEnum(LocationLevel, native_enum=True),
        nullable=False,
        comment="地理层级（使用枚举：galaxy/planet/continent/domain/state/prefecture/city/town/village）",
    )
    level_desc: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="层级自定义描述（如本世界观对该层级的别称/定义说明）",
    )
    parent_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("locations.id", ondelete="SET NULL"),
        nullable=True,
        comment="父级地点ID（如 城 的父级为 州/域；大陆 的父级为 星球）",
    )
    territory: Mapped[str | None] = mapped_column(String(256), nullable=True, comment="范围/辖域 描述")
    culture: Mapped[str | None] = mapped_column(Text, nullable=True, comment="文化习俗/风土人情")
    path: Mapped[str | None] = mapped_column(Text, nullable=True, comment="层级路径（可选，如 galaxy/planet/continent/domain/city）")


class Organization(Base):
    __tablename__ = "organizations"
    __table_args__ = {"comment": "王朝/组织/宗门/势力档案：结构、成员、建筑等"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    book_id: Mapped[int] = mapped_column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False, comment="所属书籍ID")
    name: Mapped[str] = mapped_column(String(128), nullable=False, index=True, comment="组织名称")
    type: Mapped[str | None] = mapped_column(String(64), nullable=True, comment="组织类型（王朝/宗门/家族/国家机关/商会/教派等）")
    description: Mapped[str | None] = mapped_column(Text, nullable=True, comment="组织/势力简介与设定描述")
    location_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("locations.id", ondelete="SET NULL"), nullable=True, comment="所在地点ID")
    influence_area: Mapped[str | None] = mapped_column(Text, nullable=True, comment="势力范围描述")
    culture_customs: Mapped[str | None] = mapped_column(Text, nullable=True, comment="文化习俗")
    political_structure: Mapped[str | None] = mapped_column(Text, nullable=True, comment="政治/组织结构")
    core_members: Mapped[str | None] = mapped_column(Text, nullable=True, comment="核心成员（可列表/JSON）")
    important_buildings: Mapped[str | None] = mapped_column(Text, nullable=True, comment="重要建筑（可列表/JSON）")
    established_time: Mapped[str | None] = mapped_column(String(64), nullable=True, comment="成立时间（纪元/年份等）")


class CharacterOrganizationMembership(Base):
    __tablename__ = "character_org_memberships"
    __table_args__ = (
        UniqueConstraint("book_id", "character_id", "organization_id", name="uq_character_org_book"),
        {"comment": "人物-组织/宗门 关联：职位/身份、是否间谍、任职时间等"},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    book_id: Mapped[int] = mapped_column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False, comment="所属书籍ID")
    character_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("characters.id", ondelete="CASCADE"),
        nullable=False,
        comment="人物ID",
    )
    organization_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        comment="组织ID",
    )
    role_title: Mapped[str | None] = mapped_column(String(128), nullable=True, comment="在组织/宗门中的职位/身份")
    is_spy: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, comment="是否为间谍/潜伏身份")
    start_time: Mapped[str | None] = mapped_column(String(64), nullable=True, comment="任职开始时间（文本表示）")
    end_time: Mapped[str | None] = mapped_column(String(64), nullable=True, comment="任职结束时间（文本表示）")
    notes: Mapped[str | None] = mapped_column(Text, nullable=True, comment="备注")


class OrganizationHierarchy(Base):
    __tablename__ = "organization_hierarchies"
    __table_args__ = (
        UniqueConstraint("book_id", "parent_org_id", "child_org_id", name="uq_org_hierarchy_book"),
        {"comment": "组织/宗门/国家 之间的隶属关系；国家视为一种组织/势力"},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    book_id: Mapped[int] = mapped_column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False, comment="所属书籍ID")
    parent_org_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        comment="上级组织ID（可为国家/宗门/势力等）",
    )
    child_org_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        comment="下属组织ID（可为国家/宗门/势力等）",
    )
    relation_type: Mapped[str | None] = mapped_column(String(64), nullable=True, comment="隶属关系类型（直属/盟友/附庸/托管等）")
    notes: Mapped[str | None] = mapped_column(Text, nullable=True, comment="备注")
