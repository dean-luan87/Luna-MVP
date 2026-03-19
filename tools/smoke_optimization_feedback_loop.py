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
    out = ROOT / "logs" / f"smoke_optimization_feedback_loop_{stamp}.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)

    # Provide a baseline that is slightly worse than expected current metrics to trigger "improved".
    baseline = {
        "tree_depth": 6,
        "branch_count": 3,
        "dead_branch_count": 3,
        "resolution_path_length": 0,
        "effective_feedback_count": 1,
        "prune_rate": 0.8,
        "issue_type": "high_dead_branch_ratio",
    }

    ctx = {
        "frame_seq": 1,
        "trace_anchor_id": f"smoke_ofl_{stamp}",
        "current_ts": 0.0,
        "focus_object_label": "维生素药瓶",
        "visual_audit_objects_main": [
            {"label": "cup", "bbox": [0, 0, 100, 100]},
            {"label": "bottle", "bbox": [20, 20, 40, 60]},
        ],
        "confirmation_input_raw_text": "我打开了，没有",
        "confirmation_input_type": "opened_container",
        "experience_evolution_prev_snapshot": "[]",
        "optimization_baseline_metrics": baseline,
    }

    b = DecisionMonitorBuilder()
    frame = b.build(ctx)
    d = frame.to_dict()

    ofl = d.get("optimization_feedback_loop")
    ok = isinstance(ofl, dict) and bool(ofl.get("optimization_feedback_applied")) and bool(ofl.get("validation_result"))

    with out.open("w", encoding="utf-8") as f:
        f.write(json.dumps(d, ensure_ascii=False) + "\n")

    print("jsonl_path:", str(out))
    print("feedback_loop_present:", ok)
    if isinstance(ofl, dict):
        print("validation:", ofl.get("validation_result"), "| worth_persisting:", ofl.get("worth_persisting_to_library"))
        print("next_step:", ofl.get("suggested_next_step"))
        print("delta:", "Δdead", ofl.get("delta_dead_branch_count"), "Δprune", ofl.get("delta_prune_rate"))
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())

