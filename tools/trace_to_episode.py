#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第二步落地：把 a3_trace.jsonl 转为 library_store episode，供 D0.1 parity 使用。
不改 main、不改 runtime；只读 trace，只写 library_store。
"""
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def main() -> int:
    import argparse
    p = argparse.ArgumentParser(description="Trace → library_store episode（6m42s 等视频先跑 run_video_a3_trace 再跑本脚本）")
    p.add_argument("--trace", default=os.path.join(ROOT, "logs", "a3_trace.jsonl"), help="a3_trace.jsonl 路径")
    p.add_argument("--base-dir", default=os.path.join(ROOT, "library_store"))
    p.add_argument("--version-tag", default="v1.1")
    p.add_argument("--date", default=None, help="YYYYMMDD，默认今天")
    p.add_argument("--session", default="video-6m42s")
    p.add_argument("--episode-id", default="EPISODE_6M42S", help="Episode 目录名")
    p.add_argument("--max-records", type=int, default=None, help="最多写入条数（默认全部）")
    args = p.parse_args()

    trace_path = Path(args.trace)
    if not trace_path.is_file():
        print("ERROR: trace 不存在:", trace_path, file=sys.stderr)
        return 2

    date = args.date or datetime.now(timezone.utc).strftime("%Y%m%d")
    base = Path(args.base_dir) / args.version_tag / "episodes" / date / args.session / args.episode_id
    base.mkdir(parents=True, exist_ok=True)

    records: list[dict] = []
    with open(trace_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if args.max_records is not None and len(records) >= args.max_records:
                break
            # trace 一行 → OBS_V1 一条；decision 可能为空（未采样帧）
            rec = {
                "record_type": "OBS_V1",
                "ts": row.get("ts"),
                "seq": row.get("seq", len(records)),
                "sampled": row.get("sampled", False),
                "obs": row.get("obs", {}),
                "decision": row.get("decision", {}),
            }
            # 保证 decision 里至少有三件套键（值可为 None）
            d = rec["decision"]
            if not isinstance(d, dict):
                d = {}
                rec["decision"] = d
            for k in ("safety_level", "control_mode", "pal_lookahead_m"):
                if k not in d:
                    d[k] = rec["obs"].get("control_mode") if k == "control_mode" else None
            records.append(rec)

    with open(base / "records.jsonl", "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    meta = {
        "version_tag": args.version_tag,
        "session_id": args.session,
        "episode_id": args.episode_id,
        "trigger_type": "VIDEO_TRACE",
        "trigger_ts": records[0].get("ts") if records else 0,
        "trigger_seq": records[0].get("seq") if records else 0,
        "record_count": len(records),
        "source_trace": str(trace_path),
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    with open(base / "meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    rel_path = f"{args.version_tag}/episodes/{date}/{args.session}/{args.episode_id}"
    index_row = {
        "version_tag": args.version_tag,
        "session_id": args.session,
        "episode_id": args.episode_id,
        "trigger_type": "VIDEO_TRACE",
        "trigger_seq": meta["trigger_seq"],
        "trigger_ts": meta["trigger_ts"],
        "record_count": len(records),
        "created_at": meta["created_at"],
        "path": rel_path,
    }
    index_path = Path(args.base_dir) / args.version_tag / "episodes_index.jsonl"
    index_path.parent.mkdir(parents=True, exist_ok=True)
    with open(index_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(index_row, ensure_ascii=False) + "\n")

    print("episode_dir:", base)
    print("episode_rel_path:", rel_path)
    print("record_count:", len(records))
    print("episodes_index 已追加一行")
    return 0


if __name__ == "__main__":
    sys.exit(main())
