#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
D2.2 作弊注入测试：
1) candidate 把部分 decision 字段置空 → COVERAGE_FAIL
2) candidate 在低风险帧提前 GUARDED → VOLATILITY fail
3) 恶意测试：candidate 保留 decision 但 safety_level 全写 SAFE（baseline 有 CAUTION）→ Gate 当前会 PASS，暴露“风险降级”语义漏洞，供 D1 前决策是否需 D2.3 封堵。
"""
import json
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from simulation.logic.gate import is_gate_passed
from simulation.logic.scorer import score


def _write_replay(path: str, records: list) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def test_coverage_fail_on_null_decision():
    """作弊 1：candidate 部分帧 decision 字段置空（缺 safety_level）→ 应触发 COVERAGE_FAIL；保留 control_mode 避免 volatility 先触发。"""
    baseline_records = [
        {"seq": i, "ts": float(i + 1), "decision": {"safety_level": "SAFE", "control_mode": "ASSISTED", "pal_lookahead_m": 2.0}, "explain_placeholder": True}
        for i in range(4)
    ]
    candidate_records = [
        {"seq": 0, "ts": 1.0, "decision": {"safety_level": "SAFE", "control_mode": "ASSISTED", "pal_lookahead_m": 2.0}, "explain_placeholder": True},
        {"seq": 1, "ts": 2.0, "decision": {"control_mode": "ASSISTED"}, "explain_placeholder": True},
        {"seq": 2, "ts": 3.0, "decision": {"control_mode": "ASSISTED"}, "explain_placeholder": True},
        {"seq": 3, "ts": 4.0, "decision": {"safety_level": "SAFE", "control_mode": "ASSISTED", "pal_lookahead_m": 2.0}, "explain_placeholder": True},
    ]
    with tempfile.TemporaryDirectory(prefix="ag_") as d:
        b_dir = os.path.join(d, "baseline")
        c_dir = os.path.join(d, "candidate")
        _write_replay(os.path.join(b_dir, "replay_output.jsonl"), baseline_records)
        _write_replay(os.path.join(c_dir, "replay_output.jsonl"), candidate_records)
        sc = score(b_dir, c_dir)
        passed, reasons = is_gate_passed(sc)
    assert not passed, f"expected FAIL for nulled decision, got PASS"
    assert any("COVERAGE" in r for r in reasons), f"expected COVERAGE_FAIL in reasons: {reasons}"
    assert sc.get("decision_coverage_delta", 0) < -0.02 or sc.get("lookahead_coverage_delta", 0) < -0.02, \
        f"expected coverage delta < -0.02, got decision={sc.get('decision_coverage_delta')}, lookahead={sc.get('lookahead_coverage_delta')}"
    print("PASS: cheat 1 (null decision) → COVERAGE_FAIL")


def test_low_risk_only_guarded():
    """作弊 2：candidate 仅在低风险帧（如第 0 帧）提前 GUARDED，高风险帧不提前。early_gain 仍会高；weighted 落地后应为 0。"""
    baseline_records = [
        {"seq": i, "ts": float(i + 1), "decision": {"safety_level": "SAFE", "control_mode": "ASSISTED", "pal_lookahead_m": 2.0}, "explain_placeholder": True}
        for i in range(4)
    ]
    candidate_records = [json.loads(json.dumps(r)) for r in baseline_records]
    candidate_records[0]["decision"]["control_mode"] = "GUARDED"
    for i in range(1, 4):
        pass
    with tempfile.TemporaryDirectory(prefix="ag_") as d:
        b_dir = os.path.join(d, "baseline")
        c_dir = os.path.join(d, "candidate")
        _write_replay(os.path.join(b_dir, "replay_output.jsonl"), baseline_records)
        _write_replay(os.path.join(c_dir, "replay_output.jsonl"), candidate_records)
        sc = score(b_dir, c_dir)
        passed, reasons = is_gate_passed(sc)
    assert sc.get("early_conservative_action_gain", -1) == 1.0, f"unweighted early_gain should be 1.0, got {sc.get('early_conservative_action_gain')}"
    assert sc.get("decision_coverage_delta", 0) >= -0.02, "no coverage loss for this cheat (same structure)"
    assert sc.get("lookahead_coverage_delta", 0) >= -0.02, "no lookahead coverage loss"
    assert not passed, f"expected FAIL (volatility), got PASS"
    assert any("VOLATILITY" in r for r in reasons), f"expected VOLATILITY fail: {reasons}"
    print("PASS: cheat 2 (low-risk only GUARDED) → early_gain=1.0, VOLATILITY fail; weighted gain would be 0 when implemented")


def test_safety_level_downgrade_passes():
    """
    恶意测试 3：candidate 保留 decision 字段，但把 safety_level 全部强制写 SAFE（baseline 有 CAUTION）。
    当前 Gate 会 PASS（regression=0 因 SAFE 不比 CAUTION 更危险），但这是实质性安全退化。
    本测试不断言 FAIL，而是断言 PASS，用于暴露“safety_level 是风险判断结果还是参数可塑输出”的语义漏洞；
    D1 启动前应做“恶意参数空间攻击测试”，据此决定是否引入 D2.3。
    """
    baseline_records = [
        {"seq": 0, "ts": 1.0, "decision": {"safety_level": "CAUTION", "control_mode": "GUARDED", "pal_lookahead_m": 1.5}, "explain_placeholder": True},
        {"seq": 1, "ts": 2.0, "decision": {"safety_level": "CAUTION", "control_mode": "GUARDED", "pal_lookahead_m": 1.5}, "explain_placeholder": True},
    ]
    candidate_records = [json.loads(json.dumps(r)) for r in baseline_records]
    for r in candidate_records:
        (r.setdefault("decision", {}))["safety_level"] = "SAFE"
    with tempfile.TemporaryDirectory(prefix="ag_") as d:
        b_dir = os.path.join(d, "baseline")
        c_dir = os.path.join(d, "candidate")
        _write_replay(os.path.join(b_dir, "replay_output.jsonl"), baseline_records)
        _write_replay(os.path.join(c_dir, "replay_output.jsonl"), candidate_records)
        sc = score(b_dir, c_dir)
        passed, reasons = is_gate_passed(sc)
    assert passed, f"Semantic vulnerability test: expected current Gate to PASS (safety_level downgrade not blocked); got FAIL: {reasons}"
    assert sc.get("regression_count", 1) == 0, "regression_count should be 0 when candidate is SAFE vs baseline CAUTION"
    print("PASS: cheat 3 (safety_level downgrade) → Gate PASS (known semantic gap; see D2.2 audit)")


def main():
    test_coverage_fail_on_null_decision()
    test_low_risk_only_guarded()
    test_safety_level_downgrade_passes()
    print("test_anti_gaming_d22: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
