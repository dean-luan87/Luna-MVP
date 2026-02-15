#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Weight-Only Replay Contract 验收：weights-only patch 与 baseline 同构，Gate 不因 coverage/结构误杀。
断言：decision/lookahead presence 与 baseline 逐帧一致，无 COVERAGE_FAIL_LOOKAHEAD_LOSS，
scorecard 中 lookahead_forced_ratio >= 0 可读。
执行包 C1：混合 presence（帧 0/1 有 decision+lookahead，帧 2 有 decision 无 lookahead，帧 3 无 decision）。
"""
import json
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def _fake_episode_with_decision_and_lookahead(ep_dir: Path, n_frames: int = 4) -> None:
    ep_dir.mkdir(parents=True, exist_ok=True)
    (ep_dir / "meta.json").write_text(
        json.dumps({"episode_id": "FAKE_WOC", "created_at": "2026-02-09T12:00:00Z"}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    records = []
    for j in range(n_frames):
        records.append({
            "record_type": "OBS_V1",
            "ts": float(j),
            "seq": j,
            "obs": {},
            "decision": {"safety_level": "SAFE", "control_mode": "ASSISTED", "pal_lookahead_m": 2.0},
        })
    with (ep_dir / "records.jsonl").open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def _baseline_bundle_with_mixed_presence(bundle_dir: Path) -> None:
    """手写 baseline replay + frozen stream：帧 0/1 有 decision+lookahead，帧 2 有 decision 无 lookahead，帧 3 无 decision。"""
    bundle_dir.mkdir(parents=True, exist_ok=True)
    replay_lines = [
        {"seq": 0, "ts": 0.0, "decision": {"control_mode": "ASSISTED", "safety_level": "SAFE", "pal_lookahead_m": 2.0}},
        {"seq": 1, "ts": 1.0, "decision": {"control_mode": "GUARDED", "safety_level": "CAUTION", "pal_lookahead_m": 1.5}},
        {"seq": 2, "ts": 2.0, "decision": {"control_mode": "ASSISTED", "safety_level": "SAFE"}},
        {"seq": 3, "ts": 3.0, "decision": {}},
    ]
    with (bundle_dir / "replay_output.jsonl").open("w", encoding="utf-8") as f:
        for rec in replay_lines:
            f.write(json.dumps({"seq": rec["seq"], "ts": rec["ts"], "decision": rec["decision"], "explain_placeholder": True}, ensure_ascii=False) + "\n")
    frozen_lines = [
        {"seq": 0, "has_decision": True, "has_lookahead": True, "control_mode": "ASSISTED", "safety_level": "SAFE", "pal_lookahead_m": 2.0},
        {"seq": 1, "has_decision": True, "has_lookahead": True, "control_mode": "GUARDED", "safety_level": "CAUTION", "pal_lookahead_m": 1.5},
        {"seq": 2, "has_decision": True, "has_lookahead": False, "control_mode": "ASSISTED", "safety_level": "SAFE", "pal_lookahead_m": None},
        {"seq": 3, "has_decision": False, "has_lookahead": False, "control_mode": None, "safety_level": None, "pal_lookahead_m": None},
    ]
    with (bundle_dir / "frozen_risk_stream.jsonl").open("w", encoding="utf-8") as f:
        for obj in frozen_lines:
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def _decision_present(rec: dict) -> bool:
    """与 presence_contract 一致：有 decision 对象（键存在且非 None）。"""
    return rec.get("decision") is not None


def _lookahead_present(rec: dict) -> bool:
    """与 presence_contract 一致：decision 中存在 pal_lookahead_m 字段。"""
    return "pal_lookahead_m" in (rec.get("decision") or {})


def _test_mixed_presence(tmp: str) -> None:
    """C1：混合 presence — 手写 baseline bundle，跑 candidate，断言逐帧一致 + 无 COVERAGE_FAIL_LOOKAHEAD + lookahead_forced_ratio 可读。"""
    from simulation.logic.gate import is_gate_passed
    from simulation.logic.risk_freeze_cache import load_frozen_stream
    from simulation.logic.scorer import score
    from simulation.sim_runner import run_episode

    base_dir = os.path.join(tmp, "base")
    out_dir = os.path.join(tmp, "out", "simulations")
    os.makedirs(out_dir, exist_ok=True)
    ep_rel = "v1.1/episodes/20260209/woc/MIXED_WOC"
    ep_dir = Path(base_dir) / ep_rel
    _fake_episode_with_decision_and_lookahead(ep_dir, n_frames=4)

    baseline_bundle_dir = Path(out_dir) / "MIXED_WOC_baseline"
    _baseline_bundle_with_mixed_presence(baseline_bundle_dir)
    frozen = load_frozen_stream(str(baseline_bundle_dir / "frozen_risk_stream.jsonl"))
    assert len(frozen) == 4, f"frozen 应有 4 帧: {list(frozen.keys())}"

    weight_patch = Path(tmp) / "weights_only_mixed.json"
    weight_patch.write_text(json.dumps({"weights.risk_density": 0.5}, indent=2), encoding="utf-8")

    candidate_bundle = run_episode(
        base_dir, "v1.1", ep_rel, str(weight_patch), out_dir,
        bundle_episode_id="MIXED_WOC",
        baseline_bundle_path=str(baseline_bundle_dir),
    )
    baseline_replay_path = baseline_bundle_dir / "replay_output.jsonl"
    candidate_replay_path = Path(candidate_bundle) / "replay_output.jsonl"
    assert baseline_replay_path.exists() and candidate_replay_path.exists()

    def load_replay(p: Path) -> list:
        out = []
        with p.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    out.append(json.loads(line))
        return out

    base_recs = load_replay(baseline_replay_path)
    cand_recs = load_replay(candidate_replay_path)
    assert len(base_recs) == len(cand_recs) == 4

    for i, (br, cr) in enumerate(zip(base_recs, cand_recs)):
        b_dec = _decision_present(br)
        c_dec = _decision_present(cr)
        assert c_dec == b_dec, f"帧 {i} decision presence 应一致: baseline={b_dec} candidate={c_dec}"
        b_la = _lookahead_present(br)
        c_la = _lookahead_present(cr)
        assert c_la == b_la, f"帧 {i} lookahead presence 应一致: baseline={b_la} candidate={c_la}"

    sc = score(str(baseline_bundle_dir), candidate_bundle)
    passed, reasons = is_gate_passed(sc)
    reason_str = " ".join(reasons)
    assert "COVERAGE_FAIL_LOOKAHEAD" not in reason_str, f"不应因 lookahead coverage FAIL: {reasons}"

    lf_ratio = sc.get("lookahead_forced_ratio")
    assert lf_ratio is not None and lf_ratio >= 0, f"lookahead_forced_ratio 应可读且 >= 0: {lf_ratio}"
    eff = sc.get("efficiency") or {}
    assert "lookahead_forced_ratio" in eff and eff["lookahead_forced_ratio"] >= 0


def main() -> int:
    from simulation.logic.gate import is_gate_passed
    from simulation.logic.risk_freeze_cache import is_weights_only_patch
    from simulation.logic.scorer import score
    from simulation.sim_runner import run_episode

    with tempfile.TemporaryDirectory(prefix="woc_") as tmp:
        base_dir = os.path.join(tmp, "base")
        out_dir = os.path.join(tmp, "out", "simulations")
        os.makedirs(out_dir, exist_ok=True)
        ep_rel = "v1.1/episodes/20260209/woc/FAKE_WOC"
        ep_dir = Path(base_dir) / ep_rel
        _fake_episode_with_decision_and_lookahead(ep_dir)
        weight_patch = Path(tmp) / "weights_only.json"
        weight_patch.write_text(json.dumps({"weights.risk_density": 0.5}, indent=2), encoding="utf-8")
        assert is_weights_only_patch(json.loads(weight_patch.read_text())), "patch 应为 weights-only"

        baseline_bundle = run_episode(base_dir, "v1.1", ep_rel, "", out_dir, bundle_episode_id="FAKE_WOC")
        candidate_bundle = run_episode(
            base_dir, "v1.1", ep_rel, str(weight_patch), out_dir,
            bundle_episode_id="FAKE_WOC",
            baseline_bundle_path=baseline_bundle,
        )
        sc = score(baseline_bundle, candidate_bundle)
        passed, reasons = is_gate_passed(sc)
        assert sc.get("decision_coverage_delta", 1) == 0, f"decision_coverage_delta 应为 0: {sc.get('decision_coverage_delta')}"
        assert sc.get("lookahead_coverage_delta", 1) == 0, f"lookahead_coverage_delta 应为 0: {sc.get('lookahead_coverage_delta')}"
        reason_str = " ".join(reasons)
        assert "COVERAGE_FAIL_LOOKAHEAD" not in reason_str, f"不应因 lookahead coverage FAIL: {reasons}"
        assert "COVERAGE_FAIL_DECISION" not in reason_str, f"不应因 decision coverage FAIL: {reasons}"
        # Presence-Only 不注入数值，gate 可能因 perception/efficiency 等 FAIL，仅要求不被 coverage 误杀
        gr_delta = (sc.get("efficiency") or {}).get("guarded_ratio_delta")
        assert gr_delta != 1.0 or passed, f"guarded_ratio_delta 不应为 1.0 导致误杀（或 gate 应通过）: {reasons}"

        # C1 混合 presence
        _test_mixed_presence(tmp)

    print("test_weights_only_contract: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
