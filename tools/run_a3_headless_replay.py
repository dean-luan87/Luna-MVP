#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
D0.1: Headless A3 逐帧重放。只读 library_store/.../records.jsonl，只写 outputs/<version>/headless_parity/<episode_id>/<patch_stem>/。
产出 candidate_decisions.jsonl + replay_meta.json。
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))

OBS_V1 = "OBS_V1"


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


def _load_json(path: Path) -> dict | None:
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def main() -> int:
    import argparse
    p = argparse.ArgumentParser(description="D0.1: Run headless A3 replay, write candidate_decisions.jsonl")
    p.add_argument("--base-dir", default=os.path.join(ROOT, "library_store"))
    p.add_argument("--version-tag", default="v1.1")
    p.add_argument("--episode", required=True, help="e.g. v1.1/episodes/20260209/fake-session-001/SPEECH_12")
    p.add_argument("--patch", default=os.path.join(ROOT, "patches", "empty_patch.json"))
    p.add_argument("--out-dir", default=os.path.join(ROOT, "outputs"))
    args = p.parse_args()

    from a3_headless_adapter import A3HeadlessAdapter

    base_dir = Path(args.base_dir)
    episode_dir = base_dir / args.episode.strip("/")
    records_path = episode_dir / "records.jsonl"
    meta_path = episode_dir / "meta.json"
    if not records_path.is_file():
        print("ERROR: records not found:", records_path, file=sys.stderr)
        return 2

    records = _load_jsonl(records_path)
    obs_v1 = [r for r in records if (r.get("record_type") or "").strip() == OBS_V1]
    meta = _load_json(meta_path) or {}
    episode_id = meta.get("episode_id") or episode_dir.name

    patch_path = Path(args.patch)
    patch_config: dict = {}
    if patch_path.is_file():
        patch_config = _load_json(patch_path) or {}
    patch_stem = patch_path.stem if patch_path.suffix else (patch_path.name or "baseline")
    if not patch_config:
        patch_stem = "empty_patch"

    out_version = Path(args.out_dir.rstrip("/")) / args.version_tag
    replay_dir = out_version / "headless_parity" / episode_id / patch_stem
    replay_dir.mkdir(parents=True, exist_ok=True)

    adapter = A3HeadlessAdapter(base_config={}, patch_config=patch_config)
    adapter.reset()

    decisions: list[dict] = []
    for r in obs_v1:
        ts = r.get("ts", 0.0)
        out = adapter.tick(r, virtual_ts=ts)
        decisions.append(out)

    candidate_path = replay_dir / "candidate_decisions.jsonl"
    with open(candidate_path, "w", encoding="utf-8") as f:
        for d in decisions:
            f.write(json.dumps(d, ensure_ascii=False) + "\n")

    patch_hash = hashlib.sha256(json.dumps(patch_config, sort_keys=True).encode()).hexdigest()[:16]
    replay_meta = {
        "version_tag": args.version_tag,
        "episode_id": episode_id,
        "episode_path": args.episode.strip("/"),
        "patch_stem": patch_stem,
        "patch_hash": patch_hash,
        "frame_count": len(decisions),
        "fields": ["seq", "safety_level", "control_mode", "pal_lookahead_m"],
    }
    meta_path_out = replay_dir / "replay_meta.json"
    with open(meta_path_out, "w", encoding="utf-8") as f:
        json.dump(replay_meta, f, ensure_ascii=False, indent=2)

    print("candidate_decisions:", candidate_path)
    print("replay_meta:", meta_path_out)
    print("frame_count:", len(decisions))
    return 0


if __name__ == "__main__":
    sys.exit(main())
