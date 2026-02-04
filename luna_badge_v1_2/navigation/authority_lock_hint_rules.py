"""
Authority Lock Hint Rules (v1.4.8 Step 7)

提示策略配置

关键原则：
- GPS 的 hint 永远更谨慎
- 禁止 hardcode 在逻辑中
- 所有阈值可配置
"""

from typing import Dict, Any, Optional


# Hint 规则表
HINT_RULES: Dict[str, Dict[str, Any]] = {
    "VISUAL": {
        "min_lock_progress": 0.3,      # 最小锁定进度（30%）
        "default_severity": "LOW",     # 默认严重程度
        "hint_delay_s": 0.5,           # Hint 延迟时间（秒）
    },
    "MAP_VISION": {
        "min_lock_progress": 0.4,      # 最小锁定进度（40%）
        "default_severity": "LOW",
        "hint_delay_s": 0.5,
    },
    "GPS": {
        "min_lock_progress": 0.6,      # GPS 的 hint 更谨慎（60%）
        "default_severity": "MEDIUM",  # GPS 使用 MEDIUM severity
        "hint_delay_s": 0.8,           # GPS 延迟更长
    }
}


def get_hint_rule(authority: str) -> Dict[str, Any]:
    """
    获取 Hint 规则
    
    Args:
        authority: 目标主权（"VISUAL" / "MAP_VISION" / "GPS"）
        
    Returns:
        Hint 规则字典
    """
    return HINT_RULES.get(authority, {
        "min_lock_progress": 0.3,
        "default_severity": "LOW",
        "hint_delay_s": 0.5,
    })


def calculate_eta_s(lock_start_ts: float, lock_s: float, now_ts: float) -> Optional[float]:
    """
    计算 ETA（预计完成接管时间）
    
    公式：eta_s = max(0, lock_s - (now_ts - lock_start_ts))
    
    禁止复杂，不用预测，不用 ML，不用 fancy。
    
    Args:
        lock_start_ts: LOCKING 状态开始时间
        lock_s: 锁定时间要求（秒）
        now_ts: 当前时间戳
        
    Returns:
        ETA（秒），如果已超时则返回 None
    """
    elapsed = now_ts - lock_start_ts
    eta = lock_s - elapsed
    
    if eta < 0:
        return None  # 已超时
    
    return max(0.0, eta)






