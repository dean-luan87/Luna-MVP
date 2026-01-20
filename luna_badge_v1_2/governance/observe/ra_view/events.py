from typing import Any, Dict, List


def segment_events(timeline: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    events = []
    if len(timeline) < 2:
        return events

    def _risk_level(value: Any) -> str:
        return str(value) if value is not None else "NONE"

    def _auth_level(value: Any) -> str:
        return str(value) if value is not None else "A1"

    def _envelope(value: Any) -> str:
        return str(value) if value is not None else "WITHIN_ENVELOPE"

    event_id = 0
    for idx in range(1, len(timeline)):
        prev = timeline[idx - 1]
        curr = timeline[idx]
        prev_risk = _risk_level(prev.get("risk_level"))
        curr_risk = _risk_level(curr.get("risk_level"))
        prev_auth = _auth_level(prev.get("authority_effective"))
        curr_auth = _auth_level(curr.get("authority_effective"))
        prev_env = _envelope(prev.get("envelope_status"))
        curr_env = _envelope(curr.get("envelope_status"))

        def _emit(kind: str, before: Dict[str, Any], after: Dict[str, Any]) -> None:
            nonlocal event_id
            events.append(
                {
                    "event_id": f"ev_{event_id}",
                    "type": kind,
                    "start_ts": before.get("ts", 0.0),
                    "end_ts": after.get("ts", 0.0),
                    "before": before,
                    "after": after,
                    "duration_ms": max(0.0, (after.get("ts", 0.0) - before.get("ts", 0.0)) * 1000.0),
                }
            )
            event_id += 1

        before = {
            "risk_level": prev_risk,
            "authority_effective": prev_auth,
            "envelope_status": prev_env,
            "gate": prev.get("gate"),
            "distortion_distorted": prev.get("distortion_distorted"),
            "c_decision": prev.get("c_decision"),
            "authority_blocked_by": prev.get("authority_blocked_by"),
        }
        after = {
            "risk_level": curr_risk,
            "authority_effective": curr_auth,
            "envelope_status": curr_env,
            "gate": curr.get("gate"),
            "distortion_distorted": curr.get("distortion_distorted"),
            "c_decision": curr.get("c_decision"),
            "authority_blocked_by": curr.get("authority_blocked_by"),
        }

        if prev_risk in {"LOW", "NONE"} and curr_risk in {"MEDIUM", "HIGH"}:
            _emit("RISK_RISE", before, after)
        if prev_risk in {"MEDIUM", "HIGH"} and curr_risk in {"LOW", "NONE"}:
            _emit("RISK_FALL", before, after)
        if prev_auth in {"A1", "A2"} and curr_auth not in {"A1", "A2"}:
            _emit("AUTH_DROP", before, after)
        if prev_auth not in {"A1", "A2"} and curr_auth in {"A1", "A2"}:
            _emit("AUTH_RISE", before, after)
        if prev_env in {"WITHIN_ENVELOPE", "SAFE_ENOUGH"} and curr_env in {"ADMISSIBLE", "UNACCEPTABLE"}:
            _emit("ENVELOPE_NEAR_BOUNDARY", before, after)

    return events
