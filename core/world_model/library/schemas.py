# -*- coding: utf-8 -*-
"""
v1.8.5: Library Schemas（图书馆模式定义）

职责：
- 定义知识条目的类型和生命周期状态
- 定义模式版本号（用于可追责、可回归）
"""

# 模式版本号
SCHEMA_VERSION = "1.0"

# 知识条目类型
ITEM_FACT = "FACT"
ITEM_RULE = "RULE"
ITEM_POI_INFO = "POI_INFO"
ITEM_SAFETY_NOTE = "SAFETY_NOTE"

# 生命周期状态
LIFE_ACTIVE = "ACTIVE"
LIFE_PASSIVE = "PASSIVE"
LIFE_DEPRECATED = "DEPRECATED"


