from enum import Enum


class Quality(str, Enum):
    """品质枚举（通用于功法/技能/物品/灵宠/材料等）

    可根据世界观进行扩展或映射：
    COMMON(凡) < UNCOMMON(优) < RARE(稀) < EPIC(史诗) < LEGENDARY(传说) < MYTHIC(神话)
    """

    COMMON = "common"          # 凡/普通
    UNCOMMON = "uncommon"      # 优/优秀
    RARE = "rare"              # 稀有
    EPIC = "epic"              # 史诗
    LEGENDARY = "legendary"    # 传说
    MYTHIC = "mythic"          # 神话/至宝
