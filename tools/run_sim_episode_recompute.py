#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
D1 Phase 2：单 episode A3 重算，产出与 sim_runner 同构的 replay_output.jsonl。
baseline：A3(default weights)；candidate：A3(patched weights) + Presence-Only 对齐。
供 run_sim_suite --mode recompute 调用；不进入 simulation/，可导入 a3。
"""
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

REPLAY_FILENAME = "replay_output.jsonl"
FROZEN_STREAM_FILENAME = "frozen_risk_stream.jsonl"
OBS_V1 = "OBS_V1"


def _load_json(path: str) -> Optional[Dict[str, Any]]:
    if not path or not os.path.isfile(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return None


def _load_jsonl(path: str) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    if not path or not os.path.isfile(path):
        return out
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out


def run_episode_recompute(
    base_dir: str,
    version_tag: str,
    episode_rel_path: str,
    patch_path: str,
    out_dir: str,
    bundle_episode_id: Optional[str] = None,
    baseline_bundle_path: Optional[str] = None,
) -> str:
    """
    用 A3 Headless 重算 decision，写出 replay_output.jsonl。
    接口与 sim_runner.run_episode 对齐；baseline 时 baseline_bundle_path 为空。
    返回 bundle 目录路径。
    """
    # 从项目根运行：ROOT 在 path；从 tools 运行需能解析 a3_headless_adapter
    _tools = ROOT / "tools"
    if str(_tools) not in sys.path:
        sys.path.insert(0, str(_tools))
    from a3_headless_adapter import A3HeadlessAdapter
    from simulation.logic.presence_contract import build_presence_map, is_weights_only_patch

    base_dir = base_dir.rstrip("/")
    out_dir = out_dir.rstrip("/")
    episode_dir = os.path.join(base_dir, episode_rel_path.strip("/"))
    records_path = os.path.join(episode_dir, "records.jsonl")
    meta_path = os.path.join(episode_dir, "meta.json")

    records = _load_jsonl(records_path)
    obs_v1 = [r for r in records if (r.get("record_type") or "").strip() == OBS_V1]
    meta = _load_json(meta_path) or {}
    episode_id = meta.get("episode_id") or os.path.basename(episode_dir.rstrip("/"))
    bundle_id = bundle_episode_id if bundle_episode_id is not None else episode_id

    patch_config: Dict[str, Any] = {}
    if patch_path and os.path.isfile(patch_path):
        patch_config = _load_json(patch_path) or {}
    patch_id = "baseline" if not patch_config else (Path(patch_path).stem or "baseline")
    bundle_name = f"{bundle_id}_{patch_id}"
    bundle_dir = os.path.join(out_dir, bundle_name)
    os.makedirs(bundle_dir, exist_ok=True)

    is_baseline = not baseline_bundle_path or not baseline_bundle_path.strip()
    presence_map: Dict[str, Dict[int, bool]] = {"has_decision": {}, "has_lookahead": {}}
    baseline_replay_path = ""
    if not is_baseline and baseline_bundle_path:
        baseline_replay_path = os.path.join(baseline_bundle_path.rstrip("/"), REPLAY_FILENAME)
        if os.path.isfile(baseline_replay_path):
            presence_map = build_presence_map(baseline_replay_path)
        baseline_replay_path = os.path.abspath(baseline_replay_path) if baseline_replay_path else ""

    adapter = A3HeadlessAdapter(base_config={}, patch_config=patch_config)
    adapter.reset()

    replay_lines: List[Dict[str, Any]] = []
    for r in obs_v1:
        seq = r.get("seq", len(replay_lines))
        ts = r.get("ts", 0.0)
        out = adapter.tick(r, virtual_ts=ts)
        decision: Dict[str, Any] = {
            "safety_level": out.get("safety_level"),
            "control_mode": out.get("control_mode"),
            "pal_lookahead_m": out.get("pal_lookahead_m"),
        }

        forced_lookahead_presence = False
        if not is_baseline and presence_map["has_decision"]:
            hd = presence_map["has_decision"].get(seq)
            hl = presence_map["has_lookahead"].get(seq, False)
            if hd is not None:
                if not hd:
                    decision = {}
                else:
                    if not hl:
                        decision.pop("pal_lookahead_m", None)
                    else:
                        if "pal_lookahead_m" not in decision:
                            decision["pal_lookahead_m"] = None
                            forced_lookahead_presence = True
                rec_out = {
                    "seq": seq,
                    "ts": ts,
                    "decision": decision,
                    "explain_placeholder": False,
                    "replay_meta": {
                        "weights_only_contract_applied": is_weights_only_patch(patch_config),
                        "frozen_stream_path": baseline_replay_path,
                        "forced_decision_presence": False,
                        "forced_lookahead_presence": forced_lookahead_presence,
                        "missing_frozen": False,
                    },
                }
            else:
                rec_out = {"seq": seq, "ts": ts, "decision": decision, "explain_placeholder": False}
        else:
            rec_out = {"seq": seq, "ts": ts, "decision": decision, "explain_placeholder": False}

        replay_lines.append(rec_out)

    replay_path = os.path.join(bundle_dir, REPLAY_FILENAME)
    with open(replay_path, "w", encoding="utf-8") as f:
        for rec in replay_lines:
            out_rec = {"seq": rec["seq"], "ts": rec["ts"], "decision": rec["decision"], "explain_placeholder": rec.get("explain_placeholder", False)}
            if "replay_meta" in rec:
                out_rec["replay_meta"] = rec["replay_meta"]
            f.write(json.dumps(out_rec, ensure_ascii=False) + "\n")

    if is_baseline:
        from simulation.logic.risk_freeze_cache import build_frozen_stream_from_baseline
        build_frozen_stream_from_baseline(replay_path, os.path.join(bundle_dir, FROZEN_STREAM_FILENAME))

    run_meta = {
        "episode_id": episode_id,
        "patch_id": patch_id,
        "engine_version": "recompute_v1",
        "record_count": len(replay_lines),
        "config_applied": patch_config,
        "weights_only_contract_applied": not is_baseline and is_weights_only_patch(patch_config),
        "frozen_stream_path": baseline_replay_path if not is_baseline else None,
        "recompute": True,
    }
    with open(os.path.join(bundle_dir, "run_meta.json"), "w", encoding="utf-8") as f:
        json.dump(run_meta, f, ensure_ascii=False, indent=2)

    return bundle_dir


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="D1 Phase 2: Run one episode with A3 recompute")
    p.add_argument("--base-dir", default="library_store")
    p.add_argument("--version-tag", default="v1.1")
    p.add_argument("--episode", required=True, help="e.g. v1.1/golden/slice_XXX")
    p.add_argument("--patch", default="")
    p.add_argument("--out-dir", default="outputs")
    p.add_argument("--baseline-bundle", default="", help="Candidate run: path to baseline bundle dir")
    args = p.parse_args()
    out_version = os.path.join(args.out_dir.rstrip("/"), args.version_tag, "simulations")
    bundle = run_episode_recompute(
        args.base_dir,
        args.version_tag,
        args.episode,
        args.patch or os.path.join(ROOT, "patches", "empty_patch.json"),
        out_version,
        baseline_bundle_path=args.baseline_bundle or None,
    )
    print(bundle)
