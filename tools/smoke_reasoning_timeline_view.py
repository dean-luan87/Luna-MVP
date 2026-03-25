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
    out = ROOT / "logs" / f"smoke_reasoning_timeline_view_{stamp}.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)

    ctx = {
        "frame_seq": 1,
        "current_ts": 0.0,
        "trace_anchor_id": f"smoke_timeline_{stamp}",
        "focus_object_label": "bottle",
        "minimum_mode_active": True,
        "visual_audit_objects_main": [{"label": "bottle", "bbox": [10, 10, 50, 80]}],
        "confirmation_input_raw_text": "我看过了没有",
        "confirmation_input_type": "checked_and_not_found",
        "optimization_baseline_metrics": {
            "tree_depth": 6,
            "branch_count": 3,
            "dead_branch_count": 3,
            "resolution_path_length": 0,
            "effective_feedback_count": 1,
            "prune_rate": 0.8,
            "issue_type": "high_dead_branch_ratio",
        },
    }

    frame = DecisionMonitorBuilder().build(ctx).to_dict()
    tv = frame.get("reasoning_timeline_view") if isinstance(frame.get("reasoning_timeline_view"), dict) else None
    ok = isinstance(tv, dict) and bool(tv.get("timeline_applied"))
    ev = tv.get("events") if isinstance(tv, dict) else None
    ok = ok and isinstance(ev, list) and len(ev) >= 4
    ok = ok and bool(tv.get("key_transition_summary")) if isinstance(tv, dict) else False

    out.write_text(json.dumps(frame, ensure_ascii=False) + "\n", encoding="utf-8")

    print("jsonl_path:", str(out))
    print("timeline_present:", bool(tv is not None))
    if isinstance(tv, dict):
        print("events_count:", len(tv.get("events") or []))
        print("key_transition_count:", tv.get("key_transition_count"))
        print("key_transition_summary:", tv.get("key_transition_summary"))
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())

