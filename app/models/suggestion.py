from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Text, UniqueConstraint, ForeignKey

from ..core.session import Base


class CommonSuggestion(Base):
    __tablename__ = "common_suggestions"
    __table_args__ = (
        # 全局同类型同名唯一
        UniqueConstraint("type", "name", name="uq_suggestion_type_name"),
        {"comment": "常见名录（全局）：功法名称/技能/职业/称号 等推荐词库，供用户选用或参考"},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="主键ID")

    type: Mapped[str] = mapped_column(String(32), nullable=False, comment="类型（skill/technique/martial_art/profession/title/weapon/treasure 等）")
    name: Mapped[str] = mapped_column(String(128), nullable=False, index=True, comment="名称")
    alias: Mapped[str | None] = mapped_column(String(256), nullable=True, comment="别名/同义名（逗号或JSON）")
    description: Mapped[str | None] = mapped_column(Text, nullable=True, comment="简介/设定说明/来源典故")
    tags: Mapped[str | None] = mapped_column(String(256), nullable=True, comment="标签（逗号或JSON）")
    examples: Mapped[str | None] = mapped_column(Text, nullable=True, comment="示例用法/招式名/派生词等")
    language: Mapped[str | None] = mapped_column(String(16), nullable=True, comment="语言/本地化标识，如 zh/en/jp")
    popularity: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="热度/权重，用于排序")
