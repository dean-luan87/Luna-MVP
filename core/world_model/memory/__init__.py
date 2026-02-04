# -*- coding: utf-8 -*-
"""
v1.8.5: Memory（记忆模块）

职责：
- MemoryRegistry：记忆注册表（入口整流器）
- FactCandidatePool：事实候选池（承接 Memory → 候选事实）
- 管理体验记忆与事实候选的分流演化
"""

from .candidate_pool import FactCandidatePool, FactCandidate, STATUS_PENDING, STATUS_PROMOTABLE, STATUS_REJECTED, STATUS_CONSUMED
from .memory_registry import MemoryRegistry, ExperienceMemory

__all__ = [
    "MemoryRegistry",
    "ExperienceMemory",
    "FactCandidatePool",
    "FactCandidate",
    "STATUS_PENDING",
    "STATUS_PROMOTABLE",
    "STATUS_REJECTED",
    "STATUS_CONSUMED",
]

