from typing import Any, Dict

# === Alignment Note ===
# This module corresponds to the DebugView spec.
# Original issue proposal used debug_view/* paths; this file is the stable implementation.


_AUTHORITY_ORDER = ["A1", "A2", "A3", "A4", "A5"]
_ALLOWED_KEYS = {
    "authority",
    "abilities",
    "gate",
    "c_decision",
    "bc_action",
    "risk",
    "distortion",
    "envelope",
    "threshold_version_id",
    "rollout_state",
}
_FORBIDDEN_KEYS = {"decision", "selected_result", "reason"}


def _rank(level) -> int:
    value = level.value if hasattr(level, "value") else str(level)
    return _AUTHORITY_ORDER.index(value)


def assert_debug_view_input(bc_snapshot: Dict[str, Any]) -> None:
    for key in _FORBIDDEN_KEYS:
        assert key not in bc_snapshot, "[DEBUGVIEW-INV] forbidden key present"
    # allow only whitelisted keys for debug_view input
    extra = set(bc_snapshot.keys()) - _ALLOWED_KEYS
    assert not extra, "[DEBUGVIEW-INV] unexpected keys in debug_view input"


def build_debug_view(
    *,
    raw_authority,
    effective_authority,
    blocked_by: str,
    authority_since: float,
    risk_signal,
    risk_vo: Any,
    gate_blocked: bool,
    abilities,
    attempting_recovery: bool,
    distortion_distorted: bool,
    envelope_signal: Any,
) -> Dict[str, Any]:
    recovery_blockers = []
    if distortion_distorted:
        recovery_blockers.append("DISTORTED")
    if risk_signal.present:
        recovery_blockers.append("RISK")
    if blocked_by == "HYSTERESIS":
        recovery_blockers.append("COOLDOWN")

    recovery_candidate = _rank(raw_authority) > _rank(effective_authority)
    recovery_eligible = attempting_recovery and not recovery_blockers

    primary_blocker = None
    if distortion_distorted:
        primary_blocker = "DISTORTION"
    elif risk_signal.present:
        primary_blocker = "RISK"
    elif blocked_by == "HYSTERESIS":
        primary_blocker = "COOLDOWN"

    envelope_reason = "OK"
    if gate_blocked:
        envelope_reason = "HARD_GATE"
    elif not getattr(abilities, "allow_output", True):
        envelope_reason = "ABILITY_DISABLED"
    elif risk_signal.present:
        envelope_reason = "RISK_PRESSURE"
    elif distortion_distorted:
        envelope_reason = "DISTORTION"

    return {
        "authority_panel": {
            "raw": raw_authority.value if hasattr(raw_authority, "value") else str(raw_authority),
            "effective": effective_authority.value if hasattr(effective_authority, "value") else str(effective_authority),
            "blocked_by": blocked_by,
            "recovery_candidate": recovery_candidate,
            "recovery_eligible": recovery_eligible,
            "recovery_blockers": recovery_blockers,
            "primary_blocker": primary_blocker,
            "since": authority_since,
        },
        "risk_panel": {
            "present": risk_signal.present,
            "level": "NONE" if not risk_signal.present else risk_signal.level,
            "type": risk_signal.type,
            "time_to_risk": risk_signal.time_to_event,
            "reason_codes": list(risk_signal.reason_codes),
            "vo": risk_vo or {},
        },
        "envelope": envelope_signal or {},
        "envelope_panel": {
            "within_envelope": envelope_reason == "OK",
            "envelope_reason": envelope_reason,
        },
    }


def build_debug_view_from_snapshot(bc_snapshot: Dict[str, Any]) -> Dict[str, Any]:
    assert_debug_view_input(bc_snapshot)
    authority = bc_snapshot.get("authority", {})
    return build_debug_view(
        raw_authority=authority.get("raw"),
        effective_authority=authority.get("effective"),
        blocked_by=authority.get("blocked_by"),
        authority_since=authority.get("since"),
        risk_signal=bc_snapshot.get("risk"),
        gate_blocked=bc_snapshot.get("gate") == "BLOCK",
        abilities=bc_snapshot.get("abilities"),
        attempting_recovery=True,
        distortion_distorted=bool(bc_snapshot.get("distortion", {}).get("distorted", False)),
    )
