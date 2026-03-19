# -*- coding: utf-8 -*-
import json
import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))


from decision_monitor.builder import DecisionMonitorBuilder  # noqa: E402
from decision_monitor.reasoning_structure_tree import build_reasoning_structure_tree  # noqa: E402


def main() -> int:
    # minimal context injection: reuse existing patterns from other smoke scripts
    stamp = os.environ.get("SMOKE_STAMP") or "smoke"
    out = ROOT / "logs" / f"smoke_experience_evidence_whitebox_trace_{stamp}.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)

    ctx = {
        "frame_seq": 1,
        "trace_anchor_id": f"smoke_{stamp}",
        "current_ts": 0.0,
        # provide minimal visual hints to trigger evidence/hypothesis
        "focus_object_label": "维生素药瓶",
        "visual_audit_objects_main": [
            {"label": "cup", "bbox": [0, 0, 100, 100]},
            {"label": "bottle", "bbox": [20, 20, 40, 60]},
        ],
        # inject feedback to make feedback-driven nodes visible
        "confirmation_input_raw_text": "我打开了，没有",
        "confirmation_input_type": "opened_container",
        # keep experience evolution aggregations stable
        "experience_evolution_prev_snapshot": "[]",
    }

    b = DecisionMonitorBuilder()
    frame = b.build(ctx)
    d = frame.to_dict()

    # validate two new whiteboxes exist
    eh = d.get("evidence_hypothesis_whitebox_trace")
    eg = d.get("experience_governance_whitebox_trace")
    ok_eh = isinstance(eh, dict) and bool(eh.get("whitebox_applied"))
    ok_eg = isinstance(eg, dict) and bool(eg.get("whitebox_applied"))

    # validate structure tree has evidence/hypothesis/governance and an exclusion/pruned
    t = build_reasoning_structure_tree(d).to_dict()
    nodes = t.get("nodes") or []
    types = [n.get("node_type") for n in nodes if isinstance(n, dict)]
    has_ev = "evidence" in types
    has_hyp = "hypothesis" in types
    has_res = "resolution" in types  # governance/resolution both mapped to resolution type
    has_excl = "exclusion" in types

    # write JSONL
    with out.open("w", encoding="utf-8") as f:
        f.write(json.dumps(d, ensure_ascii=False) + "\n")

    print("jsonl_path:", str(out))
    print("evidence_hypothesis_whitebox_trace:", ok_eh)
    print("experience_governance_whitebox_trace:", ok_eg)
    print("tree_nodes:", len(nodes))
    print("tree_has_evidence:", has_ev)
    print("tree_has_hypothesis:", has_hyp)
    print("tree_has_governance_or_resolution:", has_res)
    print("tree_has_exclusion:", has_excl)
    return 0 if (ok_eh and ok_eg and has_ev and has_hyp and has_res and has_excl) else 2


if __name__ == "__main__":
    raise SystemExit(main())

