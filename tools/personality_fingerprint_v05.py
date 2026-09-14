# tools/personality_fingerprint_v05.py
# v0.5 - Personality Fingerprint (Base / Non-semantic)

from typing import Dict, Any, List


def build_personality_fingerprint(trace_events: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Build a read-only behavior fingerprint from trace events.
    This function MUST NOT be used in runtime logic.
    """

    total_frames = 0
    duration_sec = 0.0

    gate_active = 0
    gate_read_only = 0
    gate_suspended = 0
    gate_state_switch = 0
    last_gate_state = None

    tick_count = 0
    no_op_count = 0
    meaningful_decisions = 0

    stability_sum = 0.0
    stability_count = 0

    first_ts = None
    last_ts = None

    for ev in trace_events:
        ev_type = ev.get("event_type")

        ts = ev.get("time", {}).get("ts")
        if ts is not None:
            if first_ts is None:
                first_ts = ts
            last_ts = ts

        if ev_type == "GATE_RUNTIME_PROFILE":
            total_frames += 1

            # 支持两种格式
            gate_info = ev.get("gate_runtime_profile") or ev.get("gate", {})
            gate_state = gate_info.get("gate_mode") or gate_info.get("mode")
            
            if gate_state == "ACTIVE":
                gate_active += 1
            elif gate_state == "READ_ONLY":
                gate_read_only += 1
            elif gate_state == "SUSPENDED":
                gate_suspended += 1

            if last_gate_state is not None and gate_state != last_gate_state:
                gate_state_switch += 1
            last_gate_state = gate_state

            # 提取稳定性分数（支持多种路径）
            view_state = ev.get("view_state") or gate_info.get("meta", {}).get("gate_eval", {}).get("details", {})
            stability = view_state.get("stability_score") if isinstance(view_state, dict) else None
            if isinstance(stability, (int, float)):
                stability_sum += stability
                stability_count += 1

        elif ev_type == "tick":
            tick_count += 1
            impact = ev.get("impact") or ev.get("impact_evaluation", {}).get("impact")
            if impact == "NO_OP":
                no_op_count += 1
            else:
                meaningful_decisions += 1

    if first_ts is not None and last_ts is not None:
        duration_sec = max(0.0, last_ts - first_ts)

    def ratio(x, base):
        return round(x / base, 4) if base > 0 else 0.0

    fingerprint = {
        "personality_fingerprint": {
            "window": {
                "duration_sec": round(duration_sec, 2),
                "frame_count": total_frames,
            },
            "gate_profile": {
                "active_ratio": ratio(gate_active, total_frames),
                "read_only_ratio": ratio(gate_read_only, total_frames),
                "suspended_ratio": ratio(gate_suspended, total_frames),
                "state_switch_per_min": round(
                    (gate_state_switch / duration_sec) * 60, 3
                ) if duration_sec > 0 else 0.0,
            },
            "decision_profile": {
                "tick_per_min": round(
                    (tick_count / duration_sec) * 60, 3
                ) if duration_sec > 0 else 0.0,
                "no_op_ratio": ratio(no_op_count, tick_count),
                "meaningful_decisions": meaningful_decisions,
            },
            "stability_profile": {
                "avg_stability_score": round(
                    stability_sum / stability_count, 4
                ) if stability_count > 0 else None
            }
        }
    }

    return fingerprint
