import time

from advice_budget.frequency_engine import FrequencyEngine
from advice_budget.levels import AdviceLevel
from advice_budget.frequency import FrequencyPolicy


def test_normal_cooldown_blocks():
    eng = FrequencyEngine(
        {
            AdviceLevel.NORMAL: FrequencyPolicy(cooldown_s=10, quota_per_min=3),
            AdviceLevel.EMERGENCY: FrequencyPolicy(0, 999),
        }
    )
    now = time.time()
    assert eng.can_emit("path_hint", "pal", AdviceLevel.NORMAL, now)
    eng.mark_emitted("path_hint", "pal", AdviceLevel.NORMAL, now)
    assert not eng.can_emit("path_hint", "pal", AdviceLevel.NORMAL, now + 5)


def test_emergency_always_allowed():
    eng = FrequencyEngine(
        {
            AdviceLevel.NORMAL: FrequencyPolicy(10, 3),
            AdviceLevel.EMERGENCY: FrequencyPolicy(0, 999),
        }
    )
    now = time.time()
    assert eng.can_emit("traffic_alert", "pal", AdviceLevel.EMERGENCY, now)
