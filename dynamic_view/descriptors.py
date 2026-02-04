from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass(frozen=True)
class EntityDescriptor:
    """
    A11-lite：识别侧输出的“身份锚点”
    - kind: person/cat/vehicle/traffic_light/...（业务层定义）
    - signature: 可选；未来接 embedding/re-id/hash
    - attributes: 可选；颜色/背包/花纹等（用于筛选与解释，不用于硬判定）
    - confidence: 识别可信度（A11-lite 不使用，仅保留）
    """
    kind: str
    signature: Optional[str] = None
    attributes: Optional[Dict[str, Any]] = None
    confidence: float = 1.0
