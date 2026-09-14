import time

from advice_budget.arbiter import AdviceArbiter
from advice_budget.types import AdviceCandidate
from advice_budget.levels import AdviceLevel
from advice_budget.frequency_engine import FrequencyEngine
from advice_budget.frequency import FrequencyPolicy


def test_emergency_wins():
    freq = FrequencyEngine(
        {
            AdviceLevel.NORMAL: FrequencyPolicy(10, 1),
            AdviceLevel.EMERGENCY: FrequencyPolicy(0, 999),
        }
    )
    arb = AdviceArbiter(freq)
    cands = [
        AdviceCandidate("c1", "pal", AdviceLevel.NORMAL.value, "path_hint", 0.9, {}),
        AdviceCandidate("c2", "roi", AdviceLevel.EMERGENCY.value, "traffic_alert", 0.5, {}),
    ]
    chosen = arb.arbitrate(cands, now=time.time())
    assert chosen is not None
    assert chosen.level == AdviceLevel.EMERGENCY.value


def test_frequency_blocks_normal():
    freq = FrequencyEngine(
        {
            AdviceLevel.NORMAL: FrequencyPolicy(10, 1),
            AdviceLevel.EMERGENCY: FrequencyPolicy(0, 999),
        }
    )
    arb = AdviceArbiter(freq)
    now = time.time()
    cand = AdviceCandidate("c1", "pal", AdviceLevel.NORMAL.value, "path_hint", 0.9, {})
    chosen = arb.arbitrate([cand], now=now)
    assert chosen is not None
    arb.mark_emitted(chosen, now=now)
    blocked = arb.arbitrate([cand], now=now + 2)
    assert blocked is None
