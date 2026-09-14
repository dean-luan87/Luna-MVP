# -*- coding: utf-8 -*-
"""
v1.8.5 Phase C 包 B: World Write Gates（全局写入闸门）

职责：
- 统一 Gate 规则（写死，覆盖三库）
- 防止在定位/视觉失衡时写入错误信息

设计原则：
- 当定位/视觉失衡时，系统宁可"慢"和"冻结"，也绝不"错写"
- 统一 Gate 规则，确保 SceneRegistry / MemoryRegistry / CandidatePool / LibraryRegistry 一致执行
"""

from core.world_model.common.types import PositionState


def should_freeze_world_writes(position_state: PositionState) -> bool:
    """
    统一 Gate 规则（写死，覆盖三库）
    
    规则：
    - 如果位置不稳定（stable=False）
    - 或者检测到漂移（drift_suspected=True）
    - 或者正在重定位（relocalizing=True）
    - 则返回 True（需要冻结写入）
    
    具体约束（强制一致）：
    - SceneRegistry: freeze → 不切 Scene
    - MemoryRegistry: forbid writes → 不写体验、不发候选
    - FactCandidatePool: forbid promote → 不升级、不消费
    - LibraryRegistry: forbid consume → 不 consume/promote
    
    注意：可以允许"衰减/rollback"继续运行（不写新事实，只让旧事实退潮）。
    
    Args:
        position_state: 位置状态
    
    Returns:
        bool: True 表示需要冻结写入，False 表示允许写入
    """
    return (
        (not position_state.stable)
        or position_state.drift_suspected
        or position_state.relocalizing
    )


