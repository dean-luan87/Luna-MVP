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
    out = ROOT / "logs" / f"smoke_spatiotemporal_continuity_reserve_{stamp}.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)

    ctx = {
        "frame_seq": 1,
        "trace_anchor_id": f"smoke_cont_{stamp}",
        "current_ts": 0.0,
        "focus_object_label": "维生素药瓶",
        "visual_audit_objects_main": [
            {"label": "cup", "bbox": [0, 0, 100, 100]},
            {"label": "bottle", "bbox": [20, 20, 40, 60]},
        ],
        # feedback that triggers broken continuity
        "confirmation_input_raw_text": "我打开了，没有",
        "confirmation_input_type": "opened_container",
        "experience_evolution_prev_snapshot": "[]",
    }

    b = DecisionMonitorBuilder()
    frame = b.build(ctx)
    d = frame.to_dict()

    c = d.get("spatiotemporal_continuity_reserve")
    ok = isinstance(c, dict) and bool(c.get("continuity_reserve_applied")) and bool(c.get("continuity_support_level"))

    with out.open("w", encoding="utf-8") as f:
        f.write(json.dumps(d, ensure_ascii=False) + "\n")

    print("jsonl_path:", str(out))
    print("continuity_present:", ok)
    if isinstance(c, dict):
        print("support_level:", c.get("continuity_support_level"))
        print("reason:", c.get("continuity_influence_reason"))
        print("affected_module:", c.get("continuity_affected_module"))
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())

