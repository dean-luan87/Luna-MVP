#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
D2.3 单测：伪造小 replay，不依赖 runtime。
1) 失败用例：baseline CAUTION/ASSISTED/2.0，candidate SAFE/ASSISTED/2.0 → degradation_rate>0，Gate 必须 FAIL（PERCEPTION_FAIL）。
2) 通过用例：candidate 同样 SAFE 但 GUARDED 或 lookahead 缩短≥10% → degradation_rate=0，不因 D2.3 FAIL。
"""
import json
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def _write_replay(dir_path: str, records: list) -> None:
    os.makedirs(dir_path, exist_ok=True)
    path = os.path.join(dir_path, "replay_output.jsonl")
    with open(path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def main() -> int:
    from simulation.logic.gate import is_gate_passed
    from simulation.logic.scorer import score

    with tempfile.TemporaryDirectory(prefix="perception_d23_") as tmp:
        base = os.path.join(tmp, "baseline")
        cand = os.path.join(tmp, "candidate")
        # 两帧：ref CAUTION
        base_records = [
            {"seq": 0, "ts": 0.0, "decision": {"safety_level": "CAUTION", "control_mode": "ASSISTED", "pal_lookahead_m": 2.0}},
            {"seq": 1, "ts": 1.0, "decision": {"safety_level": "CAUTION", "control_mode": "ASSISTED", "pal_lookahead_m": 2.0}},
        ]
        _write_replay(base, base_records)

        # --- 失败用例：candidate 判成 SAFE，无缓解 ---
        cand_fail = [
            {"seq": 0, "ts": 0.0, "decision": {"safety_level": "SAFE", "control_mode": "ASSISTED", "pal_lookahead_m": 2.0}},
            {"seq": 1, "ts": 1.0, "decision": {"safety_level": "SAFE", "control_mode": "ASSISTED", "pal_lookahead_m": 2.0}},
        ]
        _write_replay(cand, cand_fail)
        sc_fail = score(baseline_path=base, candidate_path=cand)
        assert (sc_fail.get("perception") or {}).get("degradation_rate", 0) > 0, "degradation_rate should > 0"
        passed_fail, reasons_fail = is_gate_passed(sc_fail)
        assert not passed_fail, f"Gate must FAIL: {reasons_fail}"
        assert any("PERCEPTION_FAIL" in r for r in reasons_fail), f"PERCEPTION_FAIL expected in {reasons_fail}"

        # --- 通过用例 1：candidate SAFE 但 GUARDED → 缓解 ---
        cand_guarded = [
            {"seq": 0, "ts": 0.0, "decision": {"safety_level": "SAFE", "control_mode": "GUARDED", "pal_lookahead_m": 2.0}},
            {"seq": 1, "ts": 1.0, "decision": {"safety_level": "SAFE", "control_mode": "GUARDED", "pal_lookahead_m": 2.0}},
        ]
        _write_replay(cand, cand_guarded)
        sc_guard = score(baseline_path=base, candidate_path=cand)
        assert (sc_guard.get("perception") or {}).get("degradation_rate", 0) == 0, "degradation_rate should be 0 (mitigation by GUARDED)"
        passed_guard, reasons_guard = is_gate_passed(sc_guard)
        assert "PERCEPTION_FAIL" not in " ".join(reasons_guard), f"D2.3 should not fail: {reasons_guard}"

        # --- 通过用例 2：candidate SAFE，lookahead 缩短≥10% (1.6 <= 2.0*0.9) → 缓解 ---
        cand_lookahead = [
            {"seq": 0, "ts": 0.0, "decision": {"safety_level": "SAFE", "control_mode": "ASSISTED", "pal_lookahead_m": 1.6}},
            {"seq": 1, "ts": 1.0, "decision": {"safety_level": "SAFE", "control_mode": "ASSISTED", "pal_lookahead_m": 1.6}},
        ]
        _write_replay(cand, cand_lookahead)
        sc_la = score(baseline_path=base, candidate_path=cand)
        assert (sc_la.get("perception") or {}).get("degradation_rate", 0) == 0, "degradation_rate should be 0 (mitigation by lookahead)"
        passed_la, reasons_la = is_gate_passed(sc_la)
        assert "PERCEPTION_FAIL" not in " ".join(reasons_la), f"D2.3 should not fail: {reasons_la}"

    print("test_perception_gate_d23: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
