# -*- coding: utf-8 -*-
"""
v1.8.5: Relocalization Gate（重定位闸门）

职责：
- 统一重定位闸门（全局护栏）
- 防止在视觉失衡/漂移状态下污染系统

规则（写死）：
- 如果 drift_suspected=True 或 relocalizing=True，返回 False
- 返回 False 时：
  - SceneRegistry：冻结 current_scene，不切
  - MemoryRegistry：禁止写入
  - CandidatePool：禁止升级
  - Library：不消费

这是防错位污染的核心机制。
"""

from core.world_model.common.types import PositionState


def check_relocalization_gate(position_state: PositionState) -> bool:
    """
    统一重定位闸门（全局护栏）
    
    规则：
    - 如果 drift_suspected=True 或 relocalizing=True，返回 False
    - 否则返回 True
    
    返回 False 时：
    - SceneRegistry：冻结 current_scene，不切
    - MemoryRegistry：禁止写入
    - CandidatePool：禁止升级
    - Library：不消费
    
    Args:
        position_state: 位置状态
    
    Returns:
        bool: True 表示可以通过闸门，False 表示需要冻结
    """
    # 如果位置不稳定，直接返回 False
    if not position_state.stable:
        return False
    
    # 如果检测到漂移或正在重定位，返回 False
    if position_state.drift_suspected or position_state.relocalizing:
        return False
    
    return True


