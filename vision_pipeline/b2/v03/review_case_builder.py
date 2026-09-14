# vision_pipeline/b2/v03/review_case_builder.py
from __future__ import annotations
from typing import Dict, Any, Optional
import os
import json

from .param_diff import diff_param_vector
from .narrative import build_narrative


def build_review_case(
    case_dir: str,
    *,
    human_event: Dict[str, Any],
    b2_event: Optional[Dict[str, Any]],
    evidence_pack: Optional[Dict[str, Any]],
    window_detail: Optional[Dict[str, Any]],
    prev_param_vector: Optional[Dict[str, float]],
) -> Optional[Dict[str, float]]:
    """
    构建一个完整评审 case
    返回：当前 param_vector（供下一个 case 做 diff）
    """
    os.makedirs(case_dir, exist_ok=True)

    # ---------- narrative ----------
    narrative_m = ""
    narrative_l = ""
    if evidence_pack:
        narrative_m = build_narrative(evidence_pack, window_detail, level="M")
        narrative_l = build_narrative(evidence_pack, window_detail, level="L")

    with open(os.path.join(case_dir, "narrative.md"), "w", encoding="utf-8") as f:
        f.write("## Narrative (M)\n\n")
        f.write(narrative_m + "\n\n")
        f.write("## Narrative (L)\n\n")
        f.write(narrative_l + "\n")

    # ---------- params ----------
    cur_param = (evidence_pack or {}).get("param_vector") or {}
    param_diff = diff_param_vector(prev_param_vector, cur_param)

    with open(os.path.join(case_dir, "param.json"), "w", encoding="utf-8") as f:
        json.dump(
            {
                "param_vector": cur_param,
                "param_diff": param_diff,
            },
            f,
            ensure_ascii=False,
            indent=2,
        )

    # ---------- meta ----------
    meta = {
        "human": human_event,
        "b2": b2_event,
        "evidence_ref": (b2_event or {}).get("evidence_ref"),
        "snapshots": {
            "before": "snapshots/before.jpg",
            "at": "snapshots/at.jpg",
            "after": "snapshots/after.jpg",
        },
    }

    with open(os.path.join(case_dir, "meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    return cur_param

