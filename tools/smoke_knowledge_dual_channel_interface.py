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
    out = ROOT / "logs" / f"smoke_knowledge_dual_channel_interface_{stamp}.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)

    # baseline/hint context similar to previous smokes
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
        "trace_anchor_id": f"smoke_kdc_{stamp}",
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

    k = d.get("knowledge_dual_channel_interface")
    ok = isinstance(k, dict) and bool(k.get("interface_applied"))
    ok = ok and isinstance(k.get("persist_candidate"), dict) and isinstance(k.get("optimization_candidate"), dict) and isinstance(k.get("injection_slot"), dict)

    with out.open("w", encoding="utf-8") as f:
        f.write(json.dumps(d, ensure_ascii=False) + "\n")

    print("jsonl_path:", str(out))
    print("interface_present:", ok)
    if isinstance(k, dict):
        pc = k.get("persist_candidate") or {}
        oc = k.get("optimization_candidate") or {}
        slot = k.get("injection_slot") or {}
        print("persist:", pc.get("persist_candidate_type"), "worth=", pc.get("worth_persisting"))
        print("optimization:", oc.get("optimization_candidate_type"), "needs_external=", oc.get("needs_external_strategy_support"), "lookup=", oc.get("suggested_library_lookup_type"))
        print("injection:", slot.get("injection_target_module"), "mode=", slot.get("injection_mode"))
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())

