from typing import Any, Dict, List


_MAX_HINTS = 3


def _collect_window(timeline: List[Dict[str, Any]], start_ts: float, end_ts: float) -> List[Dict[str, Any]]:
    window = [item for item in timeline if start_ts <= item.get("ts", 0.0) <= end_ts]
    if window:
        return window
    if not timeline:
        return []
    nearest = min(timeline, key=lambda item: abs(item.get("ts", 0.0) - end_ts))
    return [nearest]


def _add_hint(hints: List[str], hint: str) -> None:
    if hint in hints:
        return
    if len(hints) < _MAX_HINTS:
        hints.append(hint)


def build_root_cause_summary(events: List[Dict[str, Any]], timeline: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    summary = []
    for event in events:
        start_ts = event.get("start_ts", 0.0)
        end_ts = event.get("end_ts", 0.0)
        window = _collect_window(timeline, start_ts, end_ts)
        hints: List[str] = []

        if any(item.get("gate") == "BLOCK" for item in window):
            _add_hint(hints, "CAUSE_GATE_BLOCKED_STREAK")
        if any(item.get("distortion_distorted") for item in window):
            _add_hint(hints, "CAUSE_DISTORTION_TRUE")
        if any(item.get("c_decision") == "STOP" for item in window):
            _add_hint(hints, "CAUSE_C_FORCE_STOP")
        if any(item.get("authority_blocked_by") == "HYSTERESIS" for item in window):
            _add_hint(hints, "CAUSE_AUTH_HYSTERESIS_BLOCKED_RECOVERY")
        if event.get("type") == "RISK_RISE":
            for item in window:
                if item.get("risk_level") == "HIGH" and item.get("authority_effective") in {"A1", "A2"}:
                    _add_hint(hints, "CAUSE_RISK_HIGH_BUT_AUTH_NOT_DROP")
                    break

        summary.append({"event_id": event.get("event_id"), "cause_hints": hints})
    return summary
