# -*- coding: utf-8 -*-
"""
v1.8.5: Library（图书馆模块）

职责：
- LibraryRegistry：事实慢确认与知识唤醒系统
- 承接候选池 → L1/L2 知识条目
- 按 Scene / Map / Task 上下文唤醒知识（只供参考，不裁决）
"""

from .library_registry import LibraryRegistry, LibraryHint
from .schemas import (
    SCHEMA_VERSION,
    ITEM_FACT,
    ITEM_RULE,
    ITEM_POI_INFO,
    ITEM_SAFETY_NOTE,
    LIFE_ACTIVE,
    LIFE_PASSIVE,
    LIFE_DEPRECATED,
)

__all__ = [
    "LibraryRegistry",
    "LibraryHint",
    "SCHEMA_VERSION",
    "ITEM_FACT",
    "ITEM_RULE",
    "ITEM_POI_INFO",
    "ITEM_SAFETY_NOTE",
    "LIFE_ACTIVE",
    "LIFE_PASSIVE",
    "LIFE_DEPRECATED",
]


