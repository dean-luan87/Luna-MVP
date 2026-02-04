"""
World Fact (v1.4.8 Step 11)

系统对世界的客观描述（与产品、语言、表达方式无关）
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class WorldFact:
    """
    系统对世界的客观描述（与产品、语言、表达方式无关）
    """
    fact_type: str                  # e.g. "LANDMARK_DETECTED", "PATH_BLOCKED"
    ts: float                       # 时间戳
    scene: str                      # "indoor" / "outdoor" / "mixed"
    
    spatial_ref: Dict[str, Any]     # 距离、方向、相对位置（抽象）
    confidence: float               # 置信度 0~1
    
    source: str                     # "LOCAL_MAP" / "GPS" / "VISION" / "FUSION"
    raw_ref_id: str                 # 回溯到原始系统的ID
