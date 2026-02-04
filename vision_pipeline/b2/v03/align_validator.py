# vision_pipeline/b2/v03/align_validator.py
from __future__ import annotations
from typing import List, Dict, Any, Optional


def parse_expected(s: str) -> List[str]:
    return [x.strip() for x in s.split("|") if x.strip()]


def find_match(
    b2_events: List[Dict[str, Any]],
    t_video: float,
    expected: List[str],
    max_dt: float,
) -> Optional[Dict[str, Any]]:
    best = None
    best_dt = 1e9

    for e in b2_events:
        if expected and e.get("decision") not in expected:
            continue
        dt = abs(e.get("t_video", 0.0) - t_video)
        if dt < best_dt:
            best_dt = dt
            best = e

    if best is None or best_dt > max_dt:
        return None

    best["_dt"] = best_dt
    return best

