#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 2 Recompute Mode 验收。
Case 1: baseline vs empty_patch，mode=recompute → decision 完全一致（parity）。
Case 2: 小幅 weights 调整 → decision 有差异，guarded_ratio/early_gain 有变化。
"""
import json
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def _fake_episode(ep_dir: Path, n: int = 4, obs_variant: str = "default") -> None:
    """obs_variant: default | high_risk 用于 Case 2 触发权重差异。"""
    ep_dir.mkdir(parents=True, exist_ok=True)
    (ep_dir / "meta.json").write_text(
        json.dumps({"episode_id": "RECOMPUTE_FAKE", "created_at": "2026-02-13T00:00:00Z"}, ensure_ascii=False),
        encoding="utf-8",
    )
    with (ep_dir / "records.jsonl").open("w", encoding="utf-8") as f:
        for i in range(n):
            if obs_variant == "high_risk" and i % 2 == 1:
                obs = {"complexity": 0.85, "path": 0.2, "vc": 0.7, "frame_quality": "GOOD"}
            else:
                obs = {"complexity": 0.3, "path": 0.0, "vc": 0.9, "frame_quality": "GOOD"}
            rec = {"record_type": "OBS_V1", "seq": i, "ts": float(i), "obs": obs}
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def _load_replay_decisions(bundle_path: str) -> list:
    path = os.path.join(bundle_path.rstrip("/"), "replay_output.jsonl")
    out = []
    if not os.path.isfile(path):
        return out
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            rec = json.loads(line)
            out.append(rec.get("decision") or {})
    return out


def test_case1_baseline_vs_empty_patch_parity() -> None:
    """mode=recompute 下 baseline 与 empty_patch decision 完全一致。"""
    from simulation.sim_runner import run_episode

    with tempfile.TemporaryDirectory(prefix="recompute_") as tmp:
        base_dir = os.path.join(tmp, "base")
        out_dir = os.path.join(tmp, "out", "simulations")
        os.makedirs(out_dir, exist_ok=True)
        ep_rel = "v1.1/episodes/recompute/EP"
        ep_dir = Path(base_dir) / ep_rel
        _fake_episode(ep_dir)

        empty_patch = Path(tmp) / "empty.json"
        empty_patch.write_text("{}", encoding="utf-8")

        baseline_bundle = run_episode(base_dir, "v1.1", ep_rel, "", out_dir, bundle_episode_id="EP", mode="recompute")
        empty_bundle = run_episode(
            base_dir, "v1.1", ep_rel, str(empty_patch), out_dir,
            bundle_episode_id="EP", baseline_bundle_path=baseline_bundle, mode="recompute",
        )

        base_dec = _load_replay_decisions(baseline_bundle)
        empty_dec = _load_replay_decisions(empty_bundle)
        assert len(base_dec) == len(empty_dec) == 4, (len(base_dec), len(empty_dec))
        for i, (b, e) in enumerate(zip(base_dec, empty_dec)):
            assert b.get("safety_level") == e.get("safety_level"), f"帧{i} safety_level 一致"
            assert b.get("control_mode") == e.get("control_mode"), f"帧{i} control_mode 一致"
            assert b.get("pal_lookahead_m") == e.get("pal_lookahead_m"), f"帧{i} pal_lookahead_m 一致"


def test_case2_weights_change_affects_decision() -> None:
    """小幅 weights 调整后 decision 或 scorecard 有变化（用 high_risk obs + 极端权重触发）。"""
    from simulation.logic.scorer import score
    from simulation.sim_runner import run_episode

    with tempfile.TemporaryDirectory(prefix="recompute2_") as tmp:
        base_dir = os.path.join(tmp, "base")
        out_dir = os.path.join(tmp, "out", "simulations")
        os.makedirs(out_dir, exist_ok=True)
        ep_rel = "v1.1/episodes/recompute/EP2"
        ep_dir = Path(base_dir) / ep_rel
        _fake_episode(ep_dir, n=6, obs_variant="high_risk")

        # 极端权重：candidate 把 risk_density 提到 1.0，更容易触发 CAUTION/GUARDED，与 baseline 默认 0.3 产生差异
        weight_patch = Path(tmp) / "w.json"
        weight_patch.write_text(json.dumps({"weights.risk_density": 1.0}), encoding="utf-8")

        baseline_bundle = run_episode(base_dir, "v1.1", ep_rel, "", out_dir, bundle_episode_id="EP2", mode="recompute")
        candidate_bundle = run_episode(
            base_dir, "v1.1", ep_rel, str(weight_patch), out_dir,
            bundle_episode_id="EP2", baseline_bundle_path=baseline_bundle, mode="recompute",
        )

        base_dec = _load_replay_decisions(baseline_bundle)
        cand_dec = _load_replay_decisions(candidate_bundle)
        assert len(base_dec) == len(cand_dec)

        sc = score(baseline_bundle, candidate_bundle)
        gr_delta = (sc.get("efficiency") or {}).get("guarded_ratio_delta")
        early_gain = sc.get("early_conservative_action_gain")

        # 要么 decision 内容有差异，要么 scorecard 指标有变化
        decisions_differ = any(
            b.get("safety_level") != c.get("safety_level") or b.get("control_mode") != c.get("control_mode")
            for b, c in zip(base_dec, cand_dec)
        )
        metrics_differ = (gr_delta is not None and gr_delta != 0) or (early_gain is not None and early_gain != 0)
        assert decisions_differ or metrics_differ, (
            "weights 调整应带来 decision 或 guarded_ratio/early_gain 变化 "
            f"(gr_delta={gr_delta}, early_gain={early_gain}, decisions_differ={decisions_differ})"
        )


def main() -> int:
    test_case1_baseline_vs_empty_patch_parity()
    test_case2_weights_change_affects_decision()
    print("test_recompute_mode: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
