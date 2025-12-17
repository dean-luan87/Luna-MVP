"""
Expression Params (C-2.3)

表达参数（不是语言）

ExpressionParams（不是语言）：
- action: str
- distance_value: float
- distance_unit: str      # "meters" | "steps" | "seconds"
- direction_reference: str # "egocentric" | "absolute"
- lateral_hint: bool
- urgency_level: int      # 1-5
- contract_id: str        # C-4 治理字段（可选）
- scene: str              # C-4 治理字段（可选）
- urgency: str            # C-4 治理字段（可选，"low" / "normal" / "high"）
- duplicate_key: str      # C-4 治理字段（可选，用于防重复）
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ExpressionParams:
    """
    ExpressionParams 数据类
    
    表达参数（不是语言）：
    - action: 动作类型
    - distance_value: 距离数值
    - distance_unit: 距离单位（"meters" | "steps" | "seconds"）
    - direction_reference: 方向参考系（"egocentric" | "absolute"）
    - lateral_hint: 是否有横向提示
    - urgency_level: 紧急程度（1-5）
    - contract_id: 表达意图来源（C-4 治理字段，可选）
    - scene: 场景标签（C-4 治理字段，可选）
    - urgency: 紧急程度文本（C-4 治理字段，可选，"low" / "normal" / "high"）
    - duplicate_key: 防重复键（C-4 治理字段，可选，用于防重复播报）
    """
    action: str
    distance_value: float
    distance_unit: str      # "meters" | "steps" | "seconds"
    direction_reference: str # "egocentric" | "absolute"
    lateral_hint: bool
    urgency_level: int      # 1-5
    contract_id: Optional[str] = None     # C-4 治理字段
    scene: Optional[str] = None           # C-4 治理字段
    urgency: Optional[str] = None         # C-4 治理字段
    duplicate_key: Optional[str] = None   # C-4 治理字段
