# examples/b2_v03_dump_snapshots.py
from __future__ import annotations
import json
import os
import argparse

from vision_pipeline.b2.v03.snapshot_dumper import SnapshotDumper


def load_jsonl(path: str):
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def safe_name(s: str) -> str:
    return s.replace(":", "_").replace(" ", "_")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--timeline", required=True)
    ap.add_argument("--out", default="snapshots")
    ap.add_argument("--only_decision", action="store_true")
    args = ap.parse_args()

    dumper = SnapshotDumper(args.video, args.out)

    count = 0
    for e in load_jsonl(args.timeline):
        if args.only_decision and e.get("event_type") != "DECISION":
            continue

        t_str = safe_name(e.get("t_str", "00_00"))
        decision = e.get("decision", "event")
        main_factor = e.get("main_factor", "")
        keyframes = e.get("keyframes", {})

        folder = f"{t_str}_{decision}_{main_factor}".strip("_")
        base = os.path.join(args.out, folder)

        dumper.dump(keyframes.get("before"), os.path.join(base, "before.jpg"))
        dumper.dump(keyframes.get("at"), os.path.join(base, "at.jpg"))
        dumper.dump(keyframes.get("after"), os.path.join(base, "after.jpg"))

        count += 1

    dumper.close()
    print(f"[Snapshot] dumped {count} events → {args.out}")


if __name__ == "__main__":
    main()

