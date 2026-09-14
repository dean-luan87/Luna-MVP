from __future__ import annotations

from .levels import AdviceLevel
from .frequency import FrequencyPolicy


DEFAULT_POLICIES = {
    AdviceLevel.EMERGENCY: FrequencyPolicy(
        cooldown_s=0.0, quota_per_min=999
    ),
    AdviceLevel.NORMAL: FrequencyPolicy(
        cooldown_s=10.0, quota_per_min=3
    ),
}
