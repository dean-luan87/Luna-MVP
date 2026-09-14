#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成 3 个假 episode 到指定目录，用于 D0 测试。
目录结构：out_dir/v1.1/episodes/YYYYMMDD/session-id/episode_id/{meta.json, records.jsonl}
"""
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def make_fake_records(n: int = 4) -> list:
    out = []
    for i in range(n):
        out.append({
            "record_type": "OBS_V1",
            "ts": float(i + 1),
            "seq": i,
            "sampled": True,
            "obs": {"motion": 0.0, "path": 0.0, "branch": 0.0, "roi": 0},
            "decision": {"safety_level": "SAFE", "control_mode": "ASSISTED"},
        })
    return out


def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--out-dir", default=os.path.join(ROOT, "library_store"), help="Base output dir (e.g. library_store or temp)")
    p.add_argument("--version-tag", default="v1.1")
    p.add_argument("--date", default="20260209")
    p.add_argument("--session", default="fake-session-d0")
    p.add_argument("--count", type=int, default=3, help="Number of fake episodes")
    args = p.parse_args()
    base = Path(args.out_dir) / args.version_tag / "episodes" / args.date / args.session
    episode_ids = [f"FAKE_{i}" for i in range(1, args.count + 1)]
    for eid in episode_ids:
        ep_dir = base / eid
        ep_dir.mkdir(parents=True, exist_ok=True)
        meta = {
            "version_tag": args.version_tag,
            "session_id": args.session,
            "episode_id": eid,
            "trigger_type": "FAKE",
            "trigger_ts": 1.0,
            "trigger_seq": 0,
            "pre_n": 1,
            "post_n": 1,
            "record_count": 4,
            "created_at": "2026-02-09T12:00:00Z",
        }
        (ep_dir / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
        records = make_fake_records(4)
        with (ep_dir / "records.jsonl").open("w", encoding="utf-8") as f:
            for r in records:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
    rel = f"{args.version_tag}/episodes/{args.date}/{args.session}"
    print("fake episodes under:", base)
    print("episode_rel_path example:", f"{rel}/FAKE_1")
    return 0


if __name__ == "__main__":
    sys.exit(main())
