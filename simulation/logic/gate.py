# -*- coding: utf-8 -*-
"""
Phase 3.3-D0/B1/D2.1/D2.2/D2.3: Gate Policy — 发布门禁。
判定顺序（价值观表达，不可合并、不可颠倒）：
1. Safety（regression + danger_delta）
2. Coverage（沉默作弊优先于行为表现）
3. Stability（volatility）
4. Efficiency（guarded_ratio / lookahead_drop）
5. Perception（D2.3 语义守恒：风险判成 SAFE 须有缓解代理）
6. EarlyGain（方向性约束）
"""
from typing import Any, Dict, List, Tuple

VOLATILITY_MAX = 0.2
MAX_GUARDED_RATIO_DELTA = 0.30
MAX_LOOKAHEAD_DROP_RATIO = 0.15
MAX_COVERAGE_LOSS = 0.02
# D2.3: 感知退化率零容忍
MAX_PERCEPTION_DEGRADATION_RATE = 0.0

# Guardian Discipline Phase 1（冻结）
EXIT_LATENCY_P95_LIMIT = 6
EXIT_LATENCY_MAX_LIMIT = 12
HYSTERESIS_EFFICIENCY_MIN = 0.90
BASELINE_NO_ENTRY_MAX = 0  # 第一版仅 WARN，不 FAIL


def is_gate_passed(scorecard: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    1. Safety: regression_count > 0 → FAIL
    2. Safety: danger_delta > 0 → FAIL
    3. Coverage: decision_coverage_delta < -0.02 → FAIL
    4. Coverage: lookahead_coverage_delta < -0.02 → FAIL
    5. Stability: volatility_index > 0.2 → FAIL
    6. Efficiency: guarded_ratio_delta > 0.30 → FAIL
    7. Efficiency: lookahead_drop_ratio > 0.15 → FAIL
    8. EarlyGain: early_conservative_action_gain < 0 → FAIL
    否则 PASS。
    """
    reasons: List[str] = []
    regression_count = scorecard.get("regression_count", 0)
    if regression_count > 0:
        reasons.append(f"REGRESSION({regression_count})")
        return False, reasons

    danger_delta = scorecard.get("danger_delta", 1)
    if danger_delta > 0:
        reasons.append(f"DANGER_DELTA({danger_delta})")
        return False, reasons

    decision_coverage_delta = scorecard.get("decision_coverage_delta", 0)
    if decision_coverage_delta < -MAX_COVERAGE_LOSS:
        reasons.append(f"COVERAGE_FAIL_DECISION_LOSS: Decision coverage delta = {decision_coverage_delta:.3f} (max loss {MAX_COVERAGE_LOSS:.3f})")
        return False, reasons

    lookahead_coverage_delta = scorecard.get("lookahead_coverage_delta", 0)
    if lookahead_coverage_delta < -MAX_COVERAGE_LOSS:
        reasons.append(f"COVERAGE_FAIL_LOOKAHEAD_LOSS: Lookahead coverage delta = {lookahead_coverage_delta:.3f} (max loss {MAX_COVERAGE_LOSS:.3f})")
        return False, reasons

    volatility_index = scorecard.get("volatility_index", 1.0)
    if volatility_index > VOLATILITY_MAX:
        reasons.append(f"VOLATILITY({volatility_index:.3f})")
        return False, reasons

    efficiency = scorecard.get("efficiency") or {}
    guarded_ratio_delta = efficiency.get("guarded_ratio_delta", 0)
    if guarded_ratio_delta > MAX_GUARDED_RATIO_DELTA:
        reasons.append(f"EFF_GUARDED_RATIO_DELTA({guarded_ratio_delta:.3f})")
        return False, reasons

    lookahead_drop_ratio = efficiency.get("lookahead_drop_ratio", 0)
    if lookahead_drop_ratio > MAX_LOOKAHEAD_DROP_RATIO:
        reasons.append(f"EFF_LOOKAHEAD_DROP({lookahead_drop_ratio:.3f})")
        return False, reasons

    # D2.3 Perception: 语义守恒，一票否决
    perception = scorecard.get("perception") or {}
    degradation_rate = perception.get("degradation_rate", 0.0)
    if degradation_rate > MAX_PERCEPTION_DEGRADATION_RATE:
        examples = perception.get("degradation_examples", [])[:5]
        reasons.append(
            f"PERCEPTION_FAIL: degradation_rate={degradation_rate:.4f} (max {MAX_PERCEPTION_DEGRADATION_RATE:.3f}), examples={examples}"
        )
        return False, reasons

    early_gain = scorecard.get("early_conservative_action_gain", -1.0)
    if early_gain < 0:
        reasons.append(f"EARLY_GAIN_NEG({early_gain:.3f})")
        return False, reasons

    # Guardian Discipline Phase 1：退出纪律红线（来源 per_episode guardian_discipline summary）
    gd = scorecard.get("guardian_discipline")
    if isinstance(gd, dict):
        p95 = gd.get("exit_latency_p95")
        max_lat = gd.get("exit_latency_max")
        eff = gd.get("hysteresis_efficiency")
        if p95 is not None and p95 > EXIT_LATENCY_P95_LIMIT:
            reasons.append(f"GUARDIAN_DISCIPLINE_VIOLATION: exit_latency_p95={p95} > {EXIT_LATENCY_P95_LIMIT}")
            return False, reasons
        if max_lat is not None and max_lat > EXIT_LATENCY_MAX_LIMIT:
            reasons.append(f"GUARDIAN_DISCIPLINE_VIOLATION: exit_latency_max={max_lat} > {EXIT_LATENCY_MAX_LIMIT}")
            return False, reasons
        if eff is not None and eff < HYSTERESIS_EFFICIENCY_MIN:
            reasons.append(f"GUARDIAN_DISCIPLINE_VIOLATION: hysteresis_efficiency={eff} < {HYSTERESIS_EFFICIENCY_MIN}")
            return False, reasons
        no_entry = gd.get("baseline_no_entry_count", 0)
        if no_entry is not None and no_entry > 0:
            reasons.append("WARN_BASELINE_NO_ENTRY_EVENTS")

    # D1 Presence-Only：仅追加 warnings，不改变通过条件
    coverage = scorecard.get("coverage") or {}
    eff = scorecard.get("efficiency") or {}
    decision_valid_ratio = scorecard.get("decision_valid_ratio") or coverage.get("decision_valid_ratio")
    dr_baseline = coverage.get("decision_coverage_ratio_baseline")
    if decision_valid_ratio is not None and dr_baseline is not None and decision_valid_ratio < dr_baseline - 0.02:
        reasons.append("WARN_DECISION_VALIDITY_DROP")

    lookahead_value_valid_ratio = scorecard.get("lookahead_value_valid_ratio") or coverage.get("lookahead_value_valid_ratio")
    if lookahead_value_valid_ratio is not None and lookahead_value_valid_ratio < 0.8:
        reasons.append("WARN_LOOKAHEAD_VALUE_MISSING")

    lookahead_presence_forced_ratio = scorecard.get("lookahead_presence_forced_ratio") or coverage.get("lookahead_presence_forced_ratio")
    if lookahead_presence_forced_ratio is not None and lookahead_presence_forced_ratio > 0.5:
        reasons.append("WARN_LOOKAHEAD_PRESENCE_FORCED_HIGH")

    lf_ratio = eff.get("lookahead_forced_ratio", 0.0) or scorecard.get("lookahead_forced_ratio", 0.0)
    if lf_ratio > 0.0:
        reasons.append(f"WARN: lookahead_forced_ratio={lf_ratio:.2f} (weights-only contract applied)")

    return True, reasons
