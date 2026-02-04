from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

from map_d0.packages import LocalPackageState


@dataclass(frozen=True)
class CacheDecision:
    city_id: str
    layer: str
    action: str
    reason: str


class CachePolicy:
    """
    缓存策略：
    - 按城市管理
    - L1 优先级 > L2
    - 最近使用优先
    """

    def __init__(self, max_cities: int = 5):
        self.max_cities = max_cities

    def decide(self, local_states: Dict[str, Dict[str, LocalPackageState]]) -> List[CacheDecision]:
        """
        输入：所有城市/层的本地状态
        输出：缓存决策（不执行）
        """
        city_last_used: List[Tuple[str, float]] = []
        for city_id, layers in local_states.items():
            last = max((st.last_used_ts for st in layers.values()), default=0.0)
            city_last_used.append((city_id, last))

        city_last_used.sort(key=lambda x: x[1], reverse=True)

        decisions: List[CacheDecision] = []
        for idx, (city_id, _) in enumerate(city_last_used):
            if idx < self.max_cities:
                decisions.append(CacheDecision(city_id, "*", "keep", "within_limit"))
                continue

            layers = local_states.get(city_id, {})
            for layer, st in layers.items():
                if layer == "L2":
                    decisions.append(CacheDecision(city_id, layer, "evict", "city_over_limit"))
                else:
                    decisions.append(CacheDecision(city_id, layer, "defer", "keep_L1_as_anchor"))

        return decisions
