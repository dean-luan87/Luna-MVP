from __future__ import annotations

from typing import List, Dict, Any, Iterable

from .schema import ROIPromotionProposal, ROIProposalEvidence

VALUE_EVENT_TASK_UNBLOCK = "task_unblock"
VALUE_EVENT_SAFETY_RELEASE = "safety_release"
VALUE_EVENT_NAV_PROGRESS = "navigation_progress"
VALUE_EVENT_CONFIRMATION = "confirmation"


def analyze_timeline(
    frames: List[Dict[str, Any]],
    *,
    appear_norm_cap: int = 20,
    promote_threshold: float = 0.7,
    observe_threshold: float = 0.4,
) -> List[ROIPromotionProposal]:
    if not frames:
        return []

    stats: Dict[str, Dict[str, Any]] = {}
    pending: Dict[str, List[float]] = {}
    last_seen: Dict[str, bool] = {}
    current_run: Dict[str, int] = {}
    max_run: Dict[str, int] = {}

    for idx, frame in enumerate(frames):
        ts = float(frame.get("ts", idx))
        roi_kinds = _extract_roi_kinds(frame)
        value_events = _detect_value_events(frames, idx)

        for rk in roi_kinds:
            st = stats.setdefault(
                rk,
                {
                    "appear_count": 0,
                    "latencies": [],
                    "value_hits": set(),
                },
            )
            st["appear_count"] += 1
            pending.setdefault(rk, []).append(ts)

            prev_seen = last_seen.get(rk, False)
            if prev_seen:
                current_run[rk] = current_run.get(rk, 1) + 1
            else:
                current_run[rk] = 1
            max_run[rk] = max(max_run.get(rk, 0), current_run[rk])
            last_seen[rk] = True

        for rk in list(last_seen.keys()):
            if rk not in roi_kinds:
                last_seen[rk] = False
                current_run[rk] = 0

        if value_events:
            for rk, times in pending.items():
                if times:
                    latency = ts - times.pop(0)
                    stats[rk]["latencies"].append(max(0.0, latency))
                    stats[rk]["value_hits"].update(value_events)

    proposals: List[ROIPromotionProposal] = []
    for rk, st in stats.items():
        appear_count = st["appear_count"]
        hit_count = len(st["latencies"])
        hit_rate = hit_count / appear_count if appear_count else 0.0
        avg_latency = (
            sum(st["latencies"]) / hit_count if hit_count else float("inf")
        )
        stability = (max_run.get(rk, 0) / appear_count) if appear_count else 0.0

        score = _score(
            hit_rate,
            _normalize_appear_count(appear_count, cap=appear_norm_cap),
            _inverse_latency(avg_latency),
            stability,
        )
        suggestion = _suggestion(score, promote_threshold, observe_threshold)
        confidence = min(1.0, 0.5 + 0.5 * score)

        evidence = ROIProposalEvidence(
            appear_count=appear_count,
            hit_rate=round(hit_rate, 4),
            avg_latency_s=0.0 if avg_latency == float("inf") else round(avg_latency, 4),
            stability=round(stability, 4),
            value_hits=sorted(st["value_hits"]),
        )
        proposals.append(
            ROIPromotionProposal(
                roi_kind=rk,
                evidence=evidence,
                score=round(score, 4),
                suggestion=suggestion,
                confidence=round(confidence, 4),
            )
        )

    return proposals


def _extract_roi_kinds(frame: Dict[str, Any]) -> List[str]:
    roi_perception = frame.get("roi_perception_debug", {}) or {}
    if roi_perception:
        return list(roi_perception.get("roi_kinds", []) or [])

    roi_debug = frame.get("roi_debug", {}) or {}
    roi_hints = roi_debug.get("roi_hints", []) or []
    return [r.get("area_type") for r in roi_hints if r.get("area_type")]


def _detect_value_events(frames: List[Dict[str, Any]], idx: int) -> List[str]:
    if idx <= 0:
        return _confirmation_events(frames[idx])

    prev = frames[idx - 1]
    curr = frames[idx]

    events: List[str] = []
    if _task_unblock(prev, curr):
        events.append(VALUE_EVENT_TASK_UNBLOCK)
    if _safety_release(prev, curr):
        events.append(VALUE_EVENT_SAFETY_RELEASE)
    if _navigation_progress(prev, curr):
        events.append(VALUE_EVENT_NAV_PROGRESS)
    events.extend(_confirmation_events(curr))
    return events


def _task_unblock(prev: Dict[str, Any], curr: Dict[str, Any]) -> bool:
    prev_states = _task_states(prev)
    curr_states = _task_states(curr)
    blocked = {"waiting", "blocked"}
    for task, prev_state in prev_states.items():
        if prev_state in blocked and curr_states.get(task) not in blocked:
            return True
    return False


def _navigation_progress(prev: Dict[str, Any], curr: Dict[str, Any]) -> bool:
    prev_states = _task_states(prev)
    curr_states = _task_states(curr)
    for task, curr_state in curr_states.items():
        if curr_state in {"completed"} and prev_states.get(task) != "completed":
            return True
    return False


def _safety_release(prev: Dict[str, Any], curr: Dict[str, Any]) -> bool:
    prev_vals = set((prev.get("c_decision") or {}).values())
    curr_vals = set((curr.get("c_decision") or {}).values())
    if not prev_vals:
        return False
    return ({"stop", "hold"} & prev_vals) and ("pass" in curr_vals)


def _confirmation_events(frame: Dict[str, Any]) -> List[str]:
    roi_debug = frame.get("roi_debug", {}) or {}
    roi_hit = roi_debug.get("roi_hit", {}) or {}
    if roi_hit.get("hit"):
        return [VALUE_EVENT_CONFIRMATION]
    return []


def _task_states(frame: Dict[str, Any]) -> Dict[str, str]:
    tasks = frame.get("tasks", []) or []
    out: Dict[str, str] = {}
    for t in tasks:
        name = t.get("task") or "unknown"
        state = str(t.get("state") or "").lower()
        out[name] = state
    return out


def _normalize_appear_count(count: int, *, cap: int) -> float:
    if count <= 0:
        return 0.0
    return min(1.0, count / float(cap))


def _inverse_latency(avg_latency_s: float) -> float:
    if avg_latency_s <= 0 or avg_latency_s == float("inf"):
        return 1.0
    return 1.0 / (1.0 + avg_latency_s)


def _score(hit_rate: float, appear_norm: float, inv_latency: float, stability: float) -> float:
    return (
        0.4 * hit_rate
        + 0.3 * appear_norm
        + 0.2 * inv_latency
        + 0.1 * stability
    )


def _suggestion(score: float, promote_threshold: float, observe_threshold: float) -> str:
    if score >= promote_threshold:
        return "PROMOTE_TO_DEFAULT"
    if score >= observe_threshold:
        return "OBSERVE"
    return "IGNORE"
