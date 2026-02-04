"""
Calibration Hint (v1.4.8 Step 10)

定义"校准 / 学习提示"的最小数据结构（内部使用）。

重要禁令：
- Step 10 不得参与任何实时决策
- 不允许修改 Step 1–9 的任何已有代码
- Hint 不自动生效、不回写参数
- 不涉及任何语言表达 / TTS / UI
- description 为工程解释，不是表达层文本
"""

from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import List, Tuple


@dataclass
class CalibrationHint:
    """
    校准 / 学习提示（内部使用）
    
    注意：
    - description 为工程解释，不是表达层文本
    - 不允许直接生成任何"播报语句"
    """
    hint_type: str                  # e.g. "LANDMARK_UNSTABLE"
    authority: str                  # "MAP_VISION" / "VISUAL" / "GPS"
    
    confidence_drop: float          # 0.0 ~ 1.0
    related_map_ids: List[str]
    related_landmark_ids: List[str]
    
    time_range: Tuple[float, float]  # (start_ts, end_ts)
    description: str                 # 内部说明，不给用户
    
    def to_dict(self) -> dict:
        """转换为字典（用于序列化）"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> "CalibrationHint":
        """从字典创建（用于反序列化）"""
        return cls(**data)


# Hint 类型常量
HINT_TYPE_LANDMARK_UNSTABLE = "LANDMARK_UNSTABLE"
HINT_TYPE_AUTHORITY_FLIP_FREQUENT = "AUTHORITY_FLIP_FREQUENT"
HINT_TYPE_MAP_CONFIDENCE_OVERRATED = "MAP_CONFIDENCE_OVERRATED"
HINT_TYPE_GPS_ONLY_ZONE_DETECTED = "GPS_ONLY_ZONE_DETECTED"






