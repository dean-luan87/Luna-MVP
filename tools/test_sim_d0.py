#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 3.3-D0 最小测试：假 episode + 空 patch 跑 sim_runner，断言 replay_output.jsonl、scorecard.json 存在且 gate PASS。
"""
import json
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def _generate_fake_episodes(out_dir: str, version: str = "v1.1", count: int = 3) -> str:
    """内联生成假 episode，不依赖外部脚本。返回 episode 相对路径前缀。"""
    date = "20260209"
    session = "fake-session-d0"
    base = Path(out_dir) / version / "episodes" / date / session
    for i in range(1, count + 1):
        eid = f"FAKE_{i}"
        ep_dir = base / eid
        ep_dir.mkdir(parents=True, exist_ok=True)
        meta = {
            "version_tag": version,
            "session_id": session,
            "episode_id": eid,
            "trigger_type": "FAKE",
            "trigger_ts": 1.0,
            "trigger_seq": 0,
            "record_count": 4,
            "created_at": "2026-02-09T12:00:00Z",
        }
        (ep_dir / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
        records = []
        for j in range(4):
            records.append({
                "record_type": "OBS_V1",
                "ts": float(j + 1),
                "seq": j,
                "sampled": True,
                "obs": {"motion": 0.0, "path": 0.0, "branch": 0.0, "roi": 0},
                "decision": {"safety_level": "SAFE", "control_mode": "ASSISTED"},
            })
        with (ep_dir / "records.jsonl").open("w", encoding="utf-8") as f:
            for r in records:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return f"{version}/episodes/{date}/{session}/FAKE_1"


def main():
    from simulation.logic.gate import is_gate_passed
    from simulation.logic.scorer import score
    from simulation.sim_runner import run_episode

    with tempfile.TemporaryDirectory(prefix="sim_d0_") as tmp:
        base_dir = os.path.join(tmp, "library_store")
        out_dir = os.path.join(tmp, "outputs", "v1.1", "simulations")
        os.makedirs(out_dir, exist_ok=True)
        episode_rel = _generate_fake_episodes(base_dir, count=3)
        empty_patch = os.path.join(tmp, "empty_patch.json")
        with open(empty_patch, "w", encoding="utf-8") as f:
            json.dump({}, f)
        bundle = run_episode(
            base_dir=base_dir,
            version_tag="v1.1",
            episode_rel_path=episode_rel,
            patch_path=empty_patch,
            out_dir=out_dir,
        )
        replay_path = os.path.join(bundle, "replay_output.jsonl")
        meta_path = os.path.join(bundle, "run_meta.json")
        assert os.path.isfile(replay_path), "replay_output.jsonl should exist"
        assert os.path.isfile(meta_path), "run_meta.json should exist"
        baseline_bundle = run_episode(
            base_dir=base_dir,
            version_tag="v1.1",
            episode_rel_path=episode_rel,
            patch_path="",
            out_dir=out_dir,
        )
        scorecard = score(baseline_path=baseline_bundle, candidate_path=bundle)
        scorecard_path = os.path.join(bundle, "scorecard.json")
        with open(scorecard_path, "w", encoding="utf-8") as f:
            json.dump(scorecard, f, ensure_ascii=False, indent=2)
        assert os.path.isfile(scorecard_path), "scorecard.json should exist"
        passed, reasons = is_gate_passed(scorecard)
        assert passed, f"gate should PASS: {reasons}"
    print("test_sim_d0: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
