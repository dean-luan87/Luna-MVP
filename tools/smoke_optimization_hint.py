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
    out = ROOT / "logs" / f"smoke_optimization_hint_{stamp}.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)

    # choose a context likely to trigger high_dead_branch_ratio (same style as metrics smoke)
    ctx = {
        "frame_seq": 1,
        "trace_anchor_id": f"smoke_opt_{stamp}",
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

    oh = d.get("optimization_hint")
    ok = isinstance(oh, dict) and bool(oh.get("optimization_hint_applied")) and bool(oh.get("optimization_hint_type"))

    with out.open("w", encoding="utf-8") as f:
        f.write(json.dumps(d, ensure_ascii=False) + "\n")

    print("jsonl_path:", str(out))
    print("optimization_hint_present:", ok)
    if isinstance(oh, dict):
        print("hint:", oh.get("optimization_hint_type"), "|", oh.get("priority_level"))
        print("module:", oh.get("suggested_optimization_module"))
        print("action:", oh.get("suggested_optimization_action"))
        print("trigger:", oh.get("trigger_issue_type"), "|", oh.get("trigger_issue_reason"))
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())

