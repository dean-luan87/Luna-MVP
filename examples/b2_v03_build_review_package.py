# examples/b2_v03_build_review_package.py
from __future__ import annotations
import os
import json
import argparse

from vision_pipeline.b2.v03.review_case_builder import build_review_case


def load_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_jsonl(path: str):
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--human", default="human_timeline.json")
    ap.add_argument("--b2", default="b2_v03_timeline.jsonl")
    ap.add_argument("--out", default="reports/b2_v03_review")
    args = ap.parse_args()

    human = load_json(args.human)
    b2_events = list(load_jsonl(args.b2))

    os.makedirs(args.out, exist_ok=True)
    os.makedirs(os.path.join(args.out, "cases"), exist_ok=True)

    prev_param = None

    for idx, h in enumerate(human, start=1):
        case_id = f"case_{idx:03d}"
        case_dir = os.path.join(args.out, "cases", case_id)

        # 简化：假设 human 与 b2 已对齐过，直接取最近事件
        b2_event = min(
            b2_events,
            key=lambda e: abs(e.get("t_video", 0.0) - h["t_video"]),
            default=None,
        )

        evidence_pack = None
        window_detail = None
        if b2_event and b2_event.get("evidence_ref"):
            evidence_pack = load_json(b2_event["evidence_ref"])
            # 若你有窗口 detail 文件，可在此加载
            # window_detail = load_json(evidence_pack["window_records_path"])

        prev_param = build_review_case(
            case_dir,
            human_event=h,
            b2_event=b2_event,
            evidence_pack=evidence_pack,
            window_detail=window_detail,
            prev_param_vector=prev_param,
        )

    print(f"[Review Package] generated at {args.out}")


if __name__ == "__main__":
    main()

