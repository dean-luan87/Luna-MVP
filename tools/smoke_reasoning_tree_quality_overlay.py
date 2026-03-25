# -*- coding: utf-8 -*-
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from decision_monitor.builder import DecisionMonitorBuilder


def main() -> int:
    stamp = os.environ.get("SMOKE_STAMP") or "smoke"
    out = ROOT / "logs" / f"smoke_reasoning_tree_quality_overlay_{stamp}.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)

    ctx = {
        "frame_seq": 1,
        "trace_anchor_id": f"smoke_quality_{stamp}",
        "current_ts": 0.0,
        "focus_object_label": "bottle",
        "visual_audit_objects_main": [{"label": "bottle", "bbox": [10, 10, 50, 80]}],
        "confirmation_input_raw_text": "找到了",
        "confirmation_input_type": "target_found",
    }
    b = DecisionMonitorBuilder()
    frame = b.build(ctx)
    d = frame.to_dict()

    overlay = d.get("reasoning_tree_quality_overlay")
    if overlay is not None and hasattr(overlay, "to_dict"):
        overlay = overlay.to_dict()
    ok = isinstance(overlay, dict) and bool(overlay.get("quality_overlay_applied"))
    ok = ok and overlay.get("quality_grade") in ("good", "acceptable", "poor")
    ok = ok and (overlay.get("score_penalty_sources") is not None or overlay.get("score_bonus_sources") is not None)
    ann = overlay.get("node_quality_annotations") if isinstance(overlay, dict) else {}
    ok = ok and isinstance(ann, dict)

    with out.open("w", encoding="utf-8") as f:
        f.write(json.dumps(d, ensure_ascii=False) + "\n")

    print("jsonl_path:", str(out))
    print("overlay_present:", ok)
    if isinstance(overlay, dict):
        print("quality_grade:", overlay.get("quality_grade"))
        print("structure_score:", overlay.get("structure_score"), "convergence_score:", overlay.get("convergence_score"))
        print("penalty_sources:", overlay.get("score_penalty_sources"))
        print("node_annotations_count:", len(overlay.get("node_quality_annotations") or {}))
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
