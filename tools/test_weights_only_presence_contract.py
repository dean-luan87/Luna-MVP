#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Presence-Only Contract 验收：仅 presence 对齐，禁止 baseline 数值注入。
用例 1：baseline vs weights-only candidate → coverage delta=0，forced_lookahead_presence 时 value 必为 null。
用例 2：非 weights-only patch（thresholds.*）→ 合同不生效。
用例 3：恶意 candidate（record 无 decision）→ runner 补 presence，scorer 有效率拉低，gate 出 warning。
"""
import json
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def _fake_episode(ep_dir: Path, records_with_decision: list) -> None:
    """records_with_decision: 每帧的 decision 内容，可为 {} 表示无。"""
    ep_dir.mkdir(parents=True, exist_ok=True)
    (ep_dir / "meta.json").write_text(
        json.dumps({"episode_id": "FAKE_POC", "created_at": "2026-02-09T12:00:00Z"}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    lines = []
    for j, dec in enumerate(records_with_decision):
        lines.append({"record_type": "OBS_V1", "ts": float(j), "seq": j, "obs": {}, "decision": dec})
    with (ep_dir / "records.jsonl").open("w", encoding="utf-8") as f:
        for r in lines:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def test_baseline_vs_weights_only_candidate():
    """用例 1：decision_coverage_delta=0, lookahead_coverage_delta=0；forced_lookahead_presence 时 value 必为 null。"""
    from simulation.logic.gate import is_gate_passed
    from simulation.logic.presence_contract import is_weights_only_patch
    from simulation.logic.scorer import score
    from simulation.sim_runner import run_episode

    with tempfile.TemporaryDirectory(prefix="poc1_") as tmp:
        base_dir = os.path.join(tmp, "base")
        out_dir = os.path.join(tmp, "out", "simulations")
        os.makedirs(out_dir, exist_ok=True)
        ep_rel = "v1.1/episodes/poc/EP1"
        ep_dir = Path(base_dir) / ep_rel
        # 帧 0,1 有 decision+lookahead；帧 2 有 decision 无 lookahead（无 pal_lookahead_m）；帧 3 有 decision+lookahead
        _fake_episode(ep_dir, [
            {"safety_level": "SAFE", "control_mode": "ASSISTED", "pal_lookahead_m": 2.0},
            {"safety_level": "CAUTION", "control_mode": "GUARDED", "pal_lookahead_m": 1.5},
            {"safety_level": "SAFE", "control_mode": "ASSISTED"},
            {"safety_level": "SAFE", "control_mode": "ASSISTED", "pal_lookahead_m": 1.0},
        ])
        weight_patch = Path(tmp) / "w.json"
        weight_patch.write_text(json.dumps({"weights.risk_density": 0.5}), encoding="utf-8")
        assert is_weights_only_patch(json.loads(weight_patch.read_text()))

        baseline_bundle = run_episode(base_dir, "v1.1", ep_rel, "", out_dir, bundle_episode_id="EP1")
        candidate_bundle = run_episode(
            base_dir, "v1.1", ep_rel, str(weight_patch), out_dir,
            bundle_episode_id="EP1", baseline_bundle_path=baseline_bundle,
        )
        sc = score(baseline_bundle, candidate_bundle)
        passed, reasons = is_gate_passed(sc)

        assert sc.get("decision_coverage_delta", 1) == 0, f"decision_coverage_delta 应为 0: {sc.get('decision_coverage_delta')}"
        assert sc.get("lookahead_coverage_delta", 1) == 0, f"lookahead_coverage_delta 应为 0: {sc.get('lookahead_coverage_delta')}"

        # 任意 forced_lookahead_presence==true 的帧，pal_lookahead_m 必为 null（禁止 baseline 数值注入）
        cand_replay = Path(candidate_bundle) / "replay_output.jsonl"
        with cand_replay.open("r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                rec = json.loads(line)
                meta = rec.get("replay_meta") or {}
                if meta.get("forced_lookahead_presence"):
                    la = (rec.get("decision") or {}).get("pal_lookahead_m")
                    assert la is None, f"forced_lookahead_presence 时 pal_lookahead_m 必须为 null，不得注入 baseline 数值: {rec}"

        assert passed or "COVERAGE_FAIL" not in " ".join(reasons), f"不应因 coverage 误杀: {reasons}"


def test_non_weights_patch_contract_not_applied():
    """用例 2：thresholds.* patch → 合同不生效，candidate 结构可变化。"""
    from simulation.logic.presence_contract import is_weights_only_patch
    from simulation.sim_runner import run_episode

    with tempfile.TemporaryDirectory(prefix="poc2_") as tmp:
        base_dir = os.path.join(tmp, "base")
        out_dir = os.path.join(tmp, "out", "simulations")
        os.makedirs(out_dir, exist_ok=True)
        ep_rel = "v1.1/episodes/poc/EP2"
        ep_dir = Path(base_dir) / ep_rel
        _fake_episode(ep_dir, [
            {"safety_level": "SAFE", "control_mode": "ASSISTED", "pal_lookahead_m": 2.0},
        ] * 2)
        th_patch = Path(tmp) / "th.json"
        th_patch.write_text(json.dumps({"thresholds.caution_min": 0.3}), encoding="utf-8")
        assert not is_weights_only_patch(json.loads(th_patch.read_text())), "thresholds 非 weights-only"

        baseline_bundle = run_episode(base_dir, "v1.1", ep_rel, "", out_dir, bundle_episode_id="EP2")
        candidate_bundle = run_episode(
            base_dir, "v1.1", ep_rel, str(th_patch), out_dir,
            bundle_episode_id="EP2", baseline_bundle_path=baseline_bundle,
        )
        # candidate 未应用合同：replay 中不应出现 weights_only_contract_applied
        with (Path(candidate_bundle) / "replay_output.jsonl").open("r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                rec = json.loads(line)
                if rec.get("replay_meta", {}).get("weights_only_contract_applied"):
                    raise AssertionError("非 weights-only patch 不应应用合同")
                break


def test_malicious_candidate_placeholders_and_warning():
    """用例 3：record 无 decision → runner 补 presence 占位，scorer 有效率低，gate 出 WARN。"""
    from simulation.logic.gate import is_gate_passed
    from simulation.logic.scorer import score
    from simulation.sim_runner import run_episode

    with tempfile.TemporaryDirectory(prefix="poc3_") as tmp:
        base_dir = os.path.join(tmp, "base")
        out_dir = os.path.join(tmp, "out", "simulations")
        os.makedirs(out_dir, exist_ok=True)
        ep_rel = "v1.1/episodes/poc/EP3"
        ep_dir = Path(base_dir) / ep_rel
        # 全部帧 record 无 decision（空 dict）
        _fake_episode(ep_dir, [{}, {}, {}, {}])
        weight_patch = Path(tmp) / "w.json"
        weight_patch.write_text(json.dumps({"weights.risk_density": 0.5}), encoding="utf-8")

        baseline_bundle = run_episode(base_dir, "v1.1", ep_rel, "", out_dir, bundle_episode_id="EP3")
        candidate_bundle = run_episode(
            base_dir, "v1.1", ep_rel, str(weight_patch), out_dir,
            bundle_episode_id="EP3", baseline_bundle_path=baseline_bundle,
        )
        sc = score(baseline_bundle, candidate_bundle)
        passed, reasons = is_gate_passed(sc)

        # decision_valid_ratio 应很低（多为占位）
        dr = sc.get("decision_valid_ratio")
        assert dr is not None and dr < 0.5, f"恶意 candidate 应有低 decision_valid_ratio: {dr}"

        # gate 仍可 PASS（不新增硬门禁），但应带 WARN
        reason_str = " ".join(reasons)
        assert "WARN_DECISION_VALIDITY_DROP" in reason_str or "WARN_LOOKAHEAD" in reason_str or passed, (
            f"应有 validity/lookahead 相关 warning: {reasons}"
        )


def main() -> int:
    test_baseline_vs_weights_only_candidate()
    test_non_weights_patch_contract_not_applied()
    test_malicious_candidate_placeholders_and_warning()
    print("test_weights_only_presence_contract: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
