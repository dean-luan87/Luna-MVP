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
    out = ROOT / "logs" / f"smoke_reasoning_tree_metrics_{stamp}.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)

    ctx = {
        "frame_seq": 1,
        "trace_anchor_id": f"smoke_metrics_{stamp}",
        "current_ts": 0.0,
        "focus_object_label": "维生素药瓶",
        "visual_audit_objects_main": [
            {"label": "cup", "bbox": [0, 0, 100, 100]},
            {"label": "bottle", "bbox": [20, 20, 40, 60]},
        ],
        "confirmation_input_raw_text": "我打开了，没有",
        "confirmation_input_type": "opened_container",
        "experience_evolution_prev_snapshot": "[]",
    }

    b = DecisionMonitorBuilder()
    frame = b.build(ctx)
    d = frame.to_dict()

    m = d.get("reasoning_tree_metrics")
    ok = isinstance(m, dict) and bool(m.get("metrics_applied")) and ("tree_depth" in m) and ("possible_tree_issue_type" in m)

    with out.open("w", encoding="utf-8") as f:
        f.write(json.dumps(d, ensure_ascii=False) + "\n")

    print("jsonl_path:", str(out))
    print("metrics_present:", ok)
    if isinstance(m, dict):
        print("metrics_summary:", m.get("metrics_summary"))
        print("issue:", m.get("possible_tree_issue_type"), "|", m.get("possible_tree_issue_reason"))
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())

