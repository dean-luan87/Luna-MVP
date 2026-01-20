# vision_pipeline/b2/v03/gate_runtime.py
"""
B2 Gate Runtime State (v0.4.1)
极薄层：Gate 只影响 B，不影响 C

Patch 5: Gate 只影响 B，不影响 C（边界锁）
"""

from enum import Enum


class BGateState(Enum):
    """
    B Gate 状态（只影响 B 的运行，不影响 C）
    
    - ACTIVE: B 可以产生判断
    - READ_ONLY: B 只观察，不产生新判断
    - SUSPENDED: B 完全不说话
    """
    ACTIVE = "active"
    READ_ONLY = "read_only"
    SUSPENDED = "suspended"


def get_gate_state_from_mode(gate_mode_value: str) -> BGateState:
    """
    从 Gate Mode 转换为 BGateState
    
    :param gate_mode_value: Gate mode 值（如 "ACTIVE", "READ_ONLY", "SUSPENDED"）
    :return: BGateState
    """
    gate_mode_upper = gate_mode_value.upper()
    
    if gate_mode_upper == "ACTIVE":
        return BGateState.ACTIVE
    elif gate_mode_upper in ("READ_ONLY", "READONLY"):
        return BGateState.READ_ONLY
    else:
        return BGateState.SUSPENDED
