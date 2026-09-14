# -*- coding: utf-8 -*-
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from decision_monitor.builder import DecisionMonitorBuilder  # noqa: E402


def main() -> int:
    stamp = os.environ.get("SMOKE_STAMP") or "smoke"
    out = ROOT / "logs" / f"smoke_memory_novel_information_channel_{stamp}.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)

    ctx = {
        "frame_seq": 1,
        "current_ts": 0.0,
        "trace_anchor_id": f"smoke_mn_{stamp}",
        "focus_object_label": "bottle",
        # memory-ish
        "object_last_confirmed_location": "table",
        "object_last_confirmed_ts": 1.0,
        # newly observed
        "visual_audit_objects_main": [{"label": "bottle", "bbox": [10, 10, 50, 80]}, {"label": "cup", "bbox": [0, 0, 60, 60]}],
        # user provided
        "confirmation_input_raw_text": "我打开了",
        "confirmation_input_type": "opened_container",
    }

    frame = DecisionMonitorBuilder().build(ctx).to_dict()
    mn = frame.get("memory_novel_information_channel") if isinstance(frame.get("memory_novel_information_channel"), dict) else None
    ok = isinstance(mn, dict) and bool(mn.get("channel_applied"))
    ok = ok and bool(mn.get("dominant_reasoning_channel")) and bool(mn.get("dominant_decision_channel"))
    # candidate is optional; but ensure channels exist
    ch = mn.get("information_channels") if isinstance(mn, dict) else None
    ok = ok and isinstance(ch, list) and len(ch) >= 2

    out.write_text(json.dumps(frame, ensure_ascii=False) + "\n", encoding="utf-8")

    print("jsonl_path:", str(out))
    print("channel_present:", bool(mn is not None))
    if isinstance(mn, dict):
        print("dominant_reasoning_channel:", mn.get("dominant_reasoning_channel"))
        print("dominant_decision_channel:", mn.get("dominant_decision_channel"))
        print("counts:", mn.get("memory_channel_count"), mn.get("novel_channel_count"), mn.get("hybrid_channel_count"))
        cand = mn.get("novel_memory_candidate")
        if isinstance(cand, dict):
            print("novel_memory_candidate:", cand.get("candidate_label"), "ready:", cand.get("candidate_ready_for_memory"))
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())

