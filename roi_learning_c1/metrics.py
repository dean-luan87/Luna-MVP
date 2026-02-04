from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set


@dataclass
class ROIStats:
    appear_count: int = 0
    hit_count: int = 0
    total_latency_s: float = 0.0
    latency_count: int = 0
    stable_hits: int = 0
    stable_total: int = 0
    value_hits: Optional[Set[str]] = None

    def __post_init__(self):
        if self.value_hits is None:
            self.value_hits = set()

    def as_evidence(self) -> Dict[str, Any]:
        hit_rate = (self.hit_count / self.appear_count) if self.appear_count else 0.0
        avg_latency = (
            self.total_latency_s / self.latency_count
            if self.latency_count
            else 9999.0
        )
        stability = (
            (self.stable_hits / self.stable_total) if self.stable_total else 0.0
        )
        return {
            "appear_count": self.appear_count,
            "hit_rate": round(hit_rate, 4),
            "avg_latency_s": round(avg_latency, 4) if avg_latency < 9999.0 else None,
            "stability": round(stability, 4),
            "value_hits": sorted(list(self.value_hits or set())),
        }


def _extract_roi_kinds(frame: Dict[str, Any]) -> List[str]:
    roi_debug = frame.get("roi_debug") or {}
    roi_hints = roi_debug.get("roi_hints") or []
    kinds = []
    for r in roi_hints:
        k = r.get("area_type") or r.get("roi_kind") or r.get("kind")
        if k:
            kinds.append(str(k))
    return kinds


def _roi_hit(frame: Dict[str, Any]) -> bool:
    roi_debug = frame.get("roi_debug") or {}
    hit = (roi_debug.get("roi_hit") or {}).get("hit")
    if isinstance(hit, bool):
        return hit
    return False


def _perception_reference_count(frame: Dict[str, Any]) -> int:
    p = frame.get("roi_perception_debug") or {}
    if not p:
        return 0
    return int(p.get("reference_count") or 0)


def compute_roi_metrics(frames: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """
    v0 metric definition:
    - appear_count: number of frames where roi_kind appears
    - hit_count: count as hit when (roi_hit == True) OR (roi_perception_debug.reference_count > 0)
    - stability: approximate consecutive hit rate per roi_kind
    - latency: optional (disabled unless explicit fields exist)
    """
    stats: Dict[str, ROIStats] = {}
    prev_hit: Dict[str, Optional[bool]] = {}

    for frame in frames:
        roi_kinds = _extract_roi_kinds(frame)
        if not roi_kinds:
            continue

        hit_flag = _roi_hit(frame) or (_perception_reference_count(frame) > 0)

        for k in roi_kinds:
            s = stats.setdefault(k, ROIStats())
            s.appear_count += 1
            if hit_flag:
                s.hit_count += 1
                s.value_hits.add("roi_hit_or_reference")

            if k in prev_hit:
                s.stable_total += 1
                if prev_hit[k] is True and hit_flag is True:
                    s.stable_hits += 1
            prev_hit[k] = hit_flag

    return {k: st.as_evidence() for k, st in stats.items()}
