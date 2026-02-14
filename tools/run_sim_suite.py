#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
D2.2: 多 episode 汇总 gate，按 Golden tag 分桶一票否决。
支持 --golden（从 library_store/v1.1/golden 读）或 --episodes-index。
任一 bucket 内有一 episode FAIL → overall FAIL；bucket 缺失仅标记 MISSING_COVERAGE。
"""
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from simulation.logic.gate import is_gate_passed
from simulation.logic.scorer import score
from simulation.sim_runner import run_episode
from tools.audit_exit_latency import run_audit

REQUIRED_TAG_BUCKETS = ["low_light", "cross_traffic", "dynamic_object", "crowded", "reflection", "narrow_passage"]


def main():
    import argparse
    p = argparse.ArgumentParser(description="Run sim suite with tag buckets")
    p.add_argument("--base-dir", default="library_store")
    p.add_argument("--version-tag", default="v1.1")
    p.add_argument("--patch", required=True, help="param_patch.json path")
    p.add_argument("--out-dir", default="outputs")
    p.add_argument("--sim-dir", default="", help="Override simulations dir (e.g. for D1 per-candidate isolation)")
    p.add_argument("--golden", action="store_true", help="Use golden dir for episodes and tags")
    p.add_argument("--golden-stress", action="store_true", help="Use golden_stress dir (calibration stress suite)")
    p.add_argument("--golden-stress-v2", action="store_true", help="Use golden_stress_v2 (B2 continuous near-threshold)")
    p.add_argument("--episodes-index", default="", help="Path to episodes_index.jsonl (relative to base-dir/version)")
    p.add_argument("--mode", choices=["replay", "recompute"], default="replay", help="replay=record; recompute=A3 headless (baseline and candidate)")
    args = p.parse_args()
    base_dir = args.base_dir.rstrip("/")
    version = args.version_tag
    out_version = os.path.join(args.out_dir.rstrip("/"), version)
    sim_dir = args.sim_dir.rstrip("/") if args.sim_dir else os.path.join(out_version, "simulations")
    os.makedirs(sim_dir, exist_ok=True)

    episode_dir_name = "golden_stress_v2" if args.golden_stress_v2 else ("golden_stress" if args.golden_stress else "golden")
    if args.golden or args.golden_stress or args.golden_stress_v2:
        golden_dir = os.path.join(base_dir, version, episode_dir_name)
        if not os.path.isdir(golden_dir):
            print("ERROR: dir not found:", golden_dir, file=sys.stderr)
            return 2
        episode_paths_and_tags = []
        for ep_id in sorted(os.listdir(golden_dir)):
            ep_dir = os.path.join(golden_dir, ep_id)
            if not os.path.isdir(ep_dir):
                continue
            meta_path = os.path.join(ep_dir, "meta.json")
            if not os.path.isfile(meta_path):
                continue
            try:
                meta = json.load(open(meta_path, "r", encoding="utf-8"))
            except Exception:
                continue
            rel = meta.get("source_episode_path") or meta.get("golden_episode_path") or f"{version}/{episode_dir_name}/{ep_id}"
            tags = meta.get("tags") or meta.get("golden_tags") or []
            episode_paths_and_tags.append((rel, ep_id, tags))
    else:
        idx_path = os.path.join(base_dir, args.episodes_index or f"{version}/episodes_index.jsonl")
        if not os.path.isfile(idx_path):
            print("ERROR: episodes index not found:", idx_path, file=sys.stderr)
            return 2
        episode_paths_and_tags = []
        with open(idx_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                rel = row.get("path") or ""
                ep_id = row.get("episode_id") or Path(rel).name if rel else ""
                tags = row.get("tags") or []
                episode_paths_and_tags.append((rel, ep_id, tags))

    results_by_episode = {}
    episode_paths = {}  # ep_id -> {scorecard_path, gate_result_path} 绝对路径，供 suite_report 证据链
    for rel, ep_id, tags in episode_paths_and_tags:
        if not rel:
            continue
        try:
            # baseline 与 candidate 均用同一 mode（replay 或 recompute），保证同源
            baseline_bundle = run_episode(base_dir, version, rel, "", sim_dir, bundle_episode_id=ep_id, mode=args.mode)
            candidate_bundle = run_episode(
                base_dir, version, rel, args.patch, sim_dir,
                bundle_episode_id=ep_id,
                baseline_bundle_path=baseline_bundle,
                mode=args.mode,
            )
            sc = score(baseline_bundle, candidate_bundle)
            sc["episode_id"] = ep_id
            sc["episode_path"] = rel
            baseline_replay_path = Path(baseline_bundle) / "replay_output.jsonl"
            candidate_replay_path = Path(candidate_bundle) / "replay_output.jsonl"
            exit_audit_path_abs: Optional[str] = None
            if baseline_replay_path.is_file() and candidate_replay_path.is_file():
                exit_audit_json = Path(candidate_bundle) / "exit_audit_report.json"
                report = run_audit(
                    str(baseline_replay_path.resolve()),
                    str(candidate_replay_path.resolve()),
                    out_path=str(exit_audit_json.resolve()),
                    top_k=10,
                )
                exit_audit_path_abs = str(exit_audit_json.resolve())
                sc["guardian_discipline"] = report["summary"]
            results_by_episode[ep_id] = sc
            sp = os.path.join(candidate_bundle, "scorecard.json")
            with open(sp, "w", encoding="utf-8") as f:
                json.dump(sc, f, ensure_ascii=False, indent=2)
            passed, reasons = is_gate_passed(sc)
            gate_payload = {"passed": passed, "reasons": reasons}
            if passed and (sc.get("lookahead_forced_ratio") or 0) > 0:
                gate_payload["warnings"] = [f"WARN: lookahead_forced_ratio={sc.get('lookahead_forced_ratio')} (C 层关注)"]
            gp = os.path.join(candidate_bundle, "gate_result.json")
            with open(gp, "w", encoding="utf-8") as f:
                json.dump(gate_payload, f, ensure_ascii=False, indent=2)
            episode_paths[ep_id] = {
                "scorecard_path": str(Path(sp).resolve()),
                "gate_result_path": str(Path(gp).resolve()),
                "candidate_bundle": candidate_bundle,
                "baseline_replay_path": str(baseline_replay_path.resolve()) if baseline_replay_path.is_file() else None,
                "candidate_replay_path": str(candidate_replay_path.resolve()) if candidate_replay_path.is_file() else None,
                "exit_audit_path": exit_audit_path_abs,
            }
        except Exception as e:
            results_by_episode[ep_id] = {"episode_id": ep_id, "error": str(e), "regression_count": 1}
            episode_paths[ep_id] = {}
    golden_tags_by_episode = {ep_id: tags for _, ep_id, tags in episode_paths_and_tags}

    bucket = {}
    for eid, tags in golden_tags_by_episode.items():
        sc = results_by_episode.get(eid)
        if sc is None:
            continue
        for t in tags:
            bucket.setdefault(t, []).append(sc)

    overall_fail_reasons = []
    missing_buckets = []
    for t in REQUIRED_TAG_BUCKETS:
        if t not in bucket or len(bucket[t]) == 0:
            missing_buckets.append(t)
            continue
        for sc in bucket[t]:
            ok, reasons = is_gate_passed(sc)
            if not ok:
                overall_fail_reasons.append(f"BUCKET_FAIL:{t}:{sc.get('episode_id', '?')}:{reasons}")
                break

    print("--- Per-episode ---")
    for eid, sc in results_by_episode.items():
        ok, reasons = is_gate_passed(sc)
        print(eid, "PASS" if ok else "FAIL", reasons if reasons else "")
    print("--- Buckets ---")
    for t in REQUIRED_TAG_BUCKETS:
        n = len(bucket.get(t, []))
        status = "MISSING" if n == 0 else ("FAIL" if any(not is_gate_passed(sc)[0] for sc in bucket[t]) else "PASS")
        print(f"  {t}: {n} episodes, {status}")
    if missing_buckets:
        print("MISSING_COVERAGE:", ",".join(missing_buckets))
    print("--- Overall ---")
    suite_id = Path(args.patch).stem + "_" + datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    suite_dir = os.path.join(out_version, "sim_suites", suite_id)
    os.makedirs(suite_dir, exist_ok=True)
    n_ep = len(results_by_episode)
    weighted_available = sum(1 for sc in results_by_episode.values() if (sc.get("early") or {}).get("weighted_early_gain_available") is True)
    weighted_early_gain_available_ratio = round(weighted_available / max(1, n_ep), 4)
    per_episode = {}
    for eid, sc in results_by_episode.items():
        ok, reasons = is_gate_passed(sc)
        paths = episode_paths.get(eid, {})
        tags = golden_tags_by_episode.get(eid, [])
        # D1 weights-only contract 审计字段（从 candidate run_meta 读）
        candidate_bundle = (episode_paths.get(eid) or {}).get("candidate_bundle")
        run_meta_path = Path(candidate_bundle) / "run_meta.json" if candidate_bundle else None
        woc_applied = False
        frozen_stream_path: Optional[str] = None
        if run_meta_path and run_meta_path.is_file():
            try:
                run_meta = json.loads(run_meta_path.read_text(encoding="utf-8"))
                woc_applied = run_meta.get("weights_only_contract_applied", False)
                frozen_stream_path = run_meta.get("frozen_stream_path")
            except Exception:
                pass
        per_episode[eid] = {
            "episode_id": eid,
            "golden_id": eid,
            "scorecard_path": paths.get("scorecard_path"),
            "gate_result_path": paths.get("gate_result_path"),
            "baseline_replay_path": paths.get("baseline_replay_path"),
            "candidate_replay_path": paths.get("candidate_replay_path"),
            "exit_audit_path": paths.get("exit_audit_path"),
            "guardian_discipline": sc.get("guardian_discipline"),
            "passed": ok,
            "reasons": reasons,
            "tags": tags,
            "weights_only_contract_applied": woc_applied,
            "frozen_stream_path": frozen_stream_path,
        }
    suite_report = {
        "suite_id": suite_id,
        "patch": args.patch,
        "per_episode": per_episode,
        "per_bucket": {t: {"count": len(bucket.get(t, [])), "passed": not (t in bucket and any(not is_gate_passed(sc)[0] for sc in bucket[t]))} for t in REQUIRED_TAG_BUCKETS},
        "overall": len(overall_fail_reasons) == 0,
        "overall_fail_reasons": overall_fail_reasons,
        "missing_buckets": missing_buckets,
        "weighted_early_gain_available_ratio": weighted_early_gain_available_ratio,
    }
    suite_report_path = os.path.join(suite_dir, "suite_report.json")
    with open(suite_report_path, "w", encoding="utf-8") as f:
        json.dump(suite_report, f, ensure_ascii=False, indent=2)
    print("suite_report:", suite_report_path)

    if overall_fail_reasons:
        for r in overall_fail_reasons:
            print(r)
        print("OVERALL: FAIL")
        return 2
    print("OVERALL: PASS", "(missing buckets marked above)" if missing_buckets else "")
    return 0


if __name__ == "__main__":
    sys.exit(main())
