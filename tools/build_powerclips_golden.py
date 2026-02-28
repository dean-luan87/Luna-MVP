#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 2 High-Stress Injection：从 stress_v2 源构建「高能 Golden Suite」。
只选能跨阈值片段（high_risk_frames > 0），按 risk_used_max 降序取 TopK，保证 early_gain 有物理意义。
不修改 A3 引擎、阈值、Gate；仅构建评测集与 meta。
"""
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from simulation.sim_runner import run_episode


def _replay_risk_stats(replay_path: Path) -> Tuple[float, int, set]:
    """从 replay_output.jsonl 统计 risk_used_max, high_risk_frames, thresholds_seen。"""
    risk_max = 0.0
    high_risk_count = 0
    thresholds_seen: set = set()
    for line in replay_path.read_text(encoding="utf-8").strip().splitlines():
        if not line:
            continue
        r = json.loads(line)
        v = r.get("risk_used_for_decision")
        if isinstance(v, (int, float)):
            risk_max = max(risk_max, float(v))
        if r.get("high_risk") is True:
            high_risk_count += 1
        t = r.get("threshold_safe_to_caution")
        if isinstance(t, (int, float)):
            thresholds_seen.add(t)
    return risk_max, high_risk_count, thresholds_seen


def main() -> int:
    import argparse
    p = argparse.ArgumentParser(description="Build golden_stress_v2_powerclips from stress_v2 episodes (high-risk only)")
    p.add_argument("--stress-dir", default="library_store/v1.1/episodes/20260213/stress_v2_a3_trace",
                   help="Dir containing episode subdirs with records.jsonl")
    p.add_argument("--out-suite", default="library_store/v1.1/golden_stress_v2_powerclips",
                   help="Output suite dir (will contain episode subdirs + meta.json each)")
    p.add_argument("--top-k", type=int, default=24, help="Max episodes to keep (by risk_used_max desc)")
    p.add_argument("--base-patch", default="patches/physics/stress_v2_phys_v1.json",
                   help="Physics patch for recompute (must include smoothing.* for real risk)")
    p.add_argument("--base-dir", default="library_store",
                   help="Base dir under ROOT (with version-tag)")
    p.add_argument("--version-tag", default="v1.1", help="Version segment")
    args = p.parse_args()

    stress_dir = ROOT / args.stress_dir.strip().strip("/")
    out_suite = ROOT / args.out_suite.strip().strip("/")
    base_dir_str = str(ROOT / args.base_dir.strip().strip("/"))  # run_episode: base_dir 不含 version
    version = args.version_tag
    base_with_version = ROOT / args.base_dir.strip().strip("/") / args.version_tag

    # episode_rel_path = version / (stress_dir 相对 base_with_version) / ep_id，与 run_sim_suite 一致
    try:
        rel_suffix = str(stress_dir.resolve().relative_to(base_with_version.resolve())).replace("\\", "/")
    except ValueError:
        rel_suffix = stress_dir.name
    rel_prefix = f"{version}/{rel_suffix}"

    base_patch_path = ROOT / args.base_patch.strip()
    if not base_patch_path.is_file():
        print("ERROR: base-patch not found:", base_patch_path, file=sys.stderr)
        return 2
    patch_stem = base_patch_path.stem or "baseline"

    if not stress_dir.is_dir():
        print("ERROR: stress-dir not found:", stress_dir, file=sys.stderr)
        return 2

    episode_ids = []
    for d in sorted(stress_dir.iterdir()):
        if not d.is_dir():
            continue
        if (d / "records.jsonl").is_file():
            episode_ids.append(d.name)

    if not episode_ids:
        print("ERROR: no episode subdirs with records.jsonl in", stress_dir, file=sys.stderr)
        return 2

    print("[powerclips] scanning", len(episode_ids), "episodes with base_patch", str(base_patch_path))
    tmp = Path(tempfile.mkdtemp(prefix="powerclips_"))
    try:
        stats: List[Tuple[str, float, int, set, Path, Path]] = []  # ep_id, risk_max, hr_count, ths, replay_path, records_dir
        for ep_id in episode_ids:
            rel = f"{rel_prefix}/{ep_id}"
            try:
                bundle_dir = run_episode(
                    base_dir_str,
                    version,
                    rel,
                    str(base_patch_path),
                    str(tmp),
                    bundle_episode_id=ep_id,
                    baseline_bundle_path=None,
                    mode="recompute",
                )
            except Exception as e:
                print("[powerclips] skip", ep_id, "run_episode failed:", e, file=sys.stderr)
                continue
            replay_path = Path(bundle_dir) / "replay_output.jsonl"
            if not replay_path.is_file():
                print("[powerclips] skip", ep_id, "no replay_output.jsonl", file=sys.stderr)
                continue
            risk_max, high_risk_count, ths = _replay_risk_stats(replay_path)
            if high_risk_count <= 0:
                continue
            records_dir = stress_dir / ep_id
            stats.append((ep_id, risk_max, high_risk_count, ths, replay_path, records_dir))

        # 按 risk_used_max 降序，再按 high_risk_frames 降序，取 TopK
        stats.sort(key=lambda x: (-x[1], -x[2]))
        selected = stats[: args.top_k]
        if not selected:
            print("ERROR: no episodes with high_risk_frames > 0; cannot build powerclips suite", file=sys.stderr)
            return 2

        out_suite.mkdir(parents=True, exist_ok=True)
        source_tag = "stress_v2_sweep_debug"
        for ep_id, risk_max, high_risk_count, ths, replay_path, records_dir in selected:
            ep_out = out_suite / ep_id
            ep_out.mkdir(parents=True, exist_ok=True)
            # 复制 records.jsonl
            shutil.copy2(records_dir / "records.jsonl", ep_out / "records.jsonl")
            if (records_dir / "meta.json").is_file():
                shutil.copy2(records_dir / "meta.json", ep_out / "meta_source.json")
            # 复制 replay（recompute 产出）
            shutil.copy2(replay_path, ep_out / "replay_output.jsonl")
            meta = {
                "powerclip": True,
                "source": source_tag,
                "risk_used_max": risk_max,
                "high_risk_frames": high_risk_count,
                "thresholds_seen": list(ths),
                "version": "powerclips_v1",
            }
            (ep_out / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
            print("[powerclips]", ep_id, "risk_used_max=%.4f" % risk_max, "high_risk_frames=%d" % high_risk_count)

        print("[powerclips] wrote", len(selected), "episodes to", out_suite)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    return 0


if __name__ == "__main__":
    sys.exit(main())
