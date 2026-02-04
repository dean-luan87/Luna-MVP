from typing import List

from .contract import ObservationPolicy


def merge_policies(policies: List[ObservationPolicy]) -> ObservationPolicy:
    return ObservationPolicy(
        max_invisible_time=max(p.max_invisible_time for p in policies),
        priority=max(p.priority for p in policies),
        recovery_grace_time=max(p.recovery_grace_time for p in policies),
    )
