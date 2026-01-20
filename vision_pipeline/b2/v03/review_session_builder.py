# vision_pipeline/b2/v03/review_session_builder.py
from __future__ import annotations
from typing import List, Dict, Any
import os
import json
import csv


def build_session(
    session_dir: str,
    cases: List[Dict[str, Any]],
):
    os.makedirs(session_dir, exist_ok=True)

    # meta
    meta = {
        "decision_count": len(cases),
        "dominant_factors": list(
            {c["main_factor"] for c in cases if c.get("main_factor")}
        ),
    }
    with open(os.path.join(session_dir, "session_meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

    # timeline
    with open(os.path.join(session_dir, "timeline.md"), "w", encoding="utf-8") as f:
        f.write("# Session Timeline\n\n")
        for c in cases:
            t_str = c.get("t_str", "")
            decision = c.get("decision", "")
            main_factor = c.get("main_factor", "")
            f.write(f"{t_str} – {decision} ({main_factor})\n")

