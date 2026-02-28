#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
D0.1 第四步：从长 episode 自动切出“策略变化瞬间”±window_s 窗口，写入 golden 目录并产出 golden_candidates.jsonl。
触发器：safety_level 变化、control_mode 切换、pal 连续下降、complexity 上升（若有）。
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

OBS_V1 = "OBS_V1"
WINDOW_S = 2.0
TRIGGERS = ("safety_level_change", "control_mode_switch", "negative_pal_trend", "complexity_rise")
GOLDEN_TAGS = frozenset({"low_light", "cross_traffic", "dynamic_object", "crowded", "reflection", "narrow_passage"})


def _load_jsonl(path: Path) -> list[dict]:
    out: list[dict] = []
    if not path.is_file():
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


def _get_ts(r: dict) -> float:
    return float(r.get("ts") or 0.0)


def _decision(r: dict) -> dict:
    return r.get("decision") or {}


def _obs(r: dict) -> dict:
    return r.get("obs") or {}


def detect_triggers(records: list[dict]) -> list[tuple[int, str, float]]:
    """返回 [(record_index, trigger_type, ts_anchor), ...]。"""
    obs_v1 = [r for r in records if (r.get("record_type") or "").strip() == OBS_V1]
    out: list[tuple[int, str, float]] = []
    prev_safety = None
    prev_control = None
    prev_pal: float | None = None
    pal_drop_count = 0
    prev_comp: float | None = None

    for i, r in enumerate(obs_v1):
        d = _decision(r)
        ts = _get_ts(r)
        safety = (d.get("safety_level") or "").strip().upper() or None
        control = (d.get("control_mode") or "").strip().upper() or None
        pal_raw = d.get("pal_lookahead_m")
        pal = float(pal_raw) if pal_raw is not None else None
        comp_raw = _obs(r).get("complexity")
        comp = float(comp_raw) if comp_raw is not None else None

        if safety and safety != prev_safety and prev_safety is not None:
            if {safety, prev_safety} & {"SAFE", "CAUTION"}:
                out.append((i, "safety_level_change", ts))
        prev_safety = safety or prev_safety

        if control and control != prev_control and prev_control is not None:
            if {control, prev_control} & {"ASSISTED", "GUARDED"}:
                out.append((i, "control_mode_switch", ts))
        prev_control = control or prev_control

        if pal is not None and prev_pal is not None and pal < prev_pal:
            pal_drop_count += 1
            if pal_drop_count >= 2:
                out.append((i, "negative_pal_trend", ts))
                pal_drop_count = 0
        else:
            pal_drop_count = 0
        prev_pal = pal if pal is not None else prev_pal

        if comp is not None and prev_comp is not None and comp > prev_comp and comp - prev_comp > 0.05:
            out.append((i, "complexity_rise", ts))
        prev_comp = comp if comp is not None else prev_comp

    return out


def slice_records(records: list[dict], anchor_ts: float, window_s: float) -> list[dict]:
    obs_v1 = [r for r in records if (r.get("record_type") or "").strip() == OBS_V1]
    lo = anchor_ts - window_s
    hi = anchor_ts + window_s
    return [r for r in obs_v1 if lo <= _get_ts(r) <= hi]


def main() -> int:
    import argparse
    from datetime import datetime, timezone

    p = argparse.ArgumentParser(description="Slice episode to golden candidates (±window around triggers)")
    p.add_argument("--base-dir", default=os.path.join(ROOT, "library_store"))
    p.add_argument("--version-tag", default="v1.1")
    p.add_argument("--episode", required=True, help="Episode path relative to base_dir")
    p.add_argument("--out-dir", default=os.path.join(ROOT, "outputs"))
    p.add_argument("--window-s", type=float, default=WINDOW_S)
    p.add_argument("--write-golden", action="store_true", help="Write each slice to library_store/version/golden/")
    p.add_argument("--max-slices", type=int, default=20, help="Max number of slices to emit (by trigger order)")
    p.add_argument("--tag", default="dynamic_object", choices=list(GOLDEN_TAGS), help="Tag for written golden slices")
    p.add_argument("--tag-cross-traffic", type=int, default=2, help="Tag first N slices as cross_traffic (for D0.1 ≥2 条)")
    args = p.parse_args()

    base_dir = Path(args.base_dir)
    episode_dir = base_dir / args.episode.strip("/")
    records_path = episode_dir / "records.jsonl"
    if not records_path.is_file():
        print("ERROR: records not found:", records_path, file=sys.stderr)
        return 2

    records = _load_jsonl(records_path)
    triggers = detect_triggers(records)
    if not triggers:
        print("WARNING: no triggers found in episode")
    # 去重：相邻同 ts 的只保留一个
    seen_ts: set[float] = set()
    unique: list[tuple[int, str, float]] = []
    for idx, tt, ts in triggers:
        key = round(ts, 2)
        if key not in seen_ts:
            seen_ts.add(key)
            unique.append((idx, tt, ts))
    triggers = unique[: args.max_slices]

    out_version = Path(args.out_dir.rstrip("/")) / args.version_tag
    out_version.mkdir(parents=True, exist_ok=True)
    candidates_path = out_version / "golden_candidates.jsonl"
    candidates: list[dict] = []

    golden_root = base_dir / args.version_tag / "golden"
    if args.write_golden:
        golden_root.mkdir(parents=True, exist_ok=True)

    n_cross = max(0, args.tag_cross_traffic)
    for k, (idx, trigger_type, anchor_ts) in enumerate(triggers):
        slice_recs = slice_records(records, anchor_ts, args.window_s)
        if not slice_recs:
            continue
        golden_id = f"slice_{Path(args.episode).name}_{trigger_type}_{k}_{int(anchor_ts)}"
        tags = ["cross_traffic"] if k < n_cross else [args.tag]
        entry = {
            "golden_id": golden_id,
            "source_episode": args.episode.strip("/"),
            "trigger": trigger_type,
            "ts_anchor": anchor_ts,
            "record_count": len(slice_recs),
            "tags": tags,
        }
        if args.write_golden:
            dest_dir = golden_root / golden_id
            dest_dir.mkdir(parents=True, exist_ok=True)
            with open(dest_dir / "records.jsonl", "w", encoding="utf-8") as f:
                for r in slice_recs:
                    f.write(json.dumps(r, ensure_ascii=False) + "\n")
            meta = {
                "version_tag": args.version_tag,
                "episode_id": golden_id,
                "source_episode_path": f"{args.version_tag}/golden/{golden_id}",
                "tags": tags,
                "reason": f"slice trigger={trigger_type} ts={anchor_ts}",
                "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            }
            (dest_dir / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
            entry["golden_path"] = f"{args.version_tag}/golden/{golden_id}"
        candidates.append(entry)

    with open(candidates_path, "w", encoding="utf-8") as f:
        for c in candidates:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")

    print("triggers_found:", len(triggers))
    print("slices_written:", len(candidates))
    print("golden_candidates:", candidates_path)
    if args.write_golden and candidates:
        print("golden_dir:", golden_root)
    return 0


if __name__ == "__main__":
    sys.exit(main())
