from dataclasses import dataclass
from typing import Dict, Any


@dataclass(frozen=True)
class ChangeDemand:
    """
    系统当前需要判断的“变化类型”。
    注意：这是需求，不是观察指令。
    """

    demand_type: str
    priority: int
    constraints: Dict[str, Any]
    source: str  # "task" | "c"
