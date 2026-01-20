import os
from enum import Enum
from typing import Iterable


class InvariantMode(Enum):
    OFF = "OFF"
    SHADOW = "SHADOW"
    DEBUG = "DEBUG"


def get_invariant_mode() -> InvariantMode:
    value = os.getenv("LUNA_INVARIANTS", "OFF").upper()
    for mode in InvariantMode:
        if value == mode.value:
            return mode
    return InvariantMode.OFF


def _enforce(condition: bool, message: str) -> None:
    mode = get_invariant_mode()
    if mode == InvariantMode.OFF:
        return
    if mode == InvariantMode.DEBUG:
        assert condition, message
        return
    # SHADOW: do not raise, reserved for logging-only usage.
    return


FORBIDDEN_B_FIELDS = {
    "authority",
    "abilities",
    "gate",
    "decision",
    "level",
    "impact",
    "must_stop",
    "intervention_level",
}

_AUTHORITY_ORDER = ["A1", "A2", "A3", "A4", "A5"]


def _authority_rank(level) -> int:
    value = level.value if hasattr(level, "value") else str(level)
    return _AUTHORITY_ORDER.index(value)


def assert_b_invariants(b_output: dict) -> None:
    for key in FORBIDDEN_B_FIELDS:
        _enforce(key not in b_output, f"[B-INV] forbidden field leaked: {key}")


ALLOWED_C_DECISIONS = {"STOP", "HOLD", "REQUEST_TAKEOVER"}
FORBIDDEN_KEYS_IN_C_INPUT = {
    "risk",
    "risk_level",
    "risk_type",
    "authority",
    "abilities",
    "bc_action",
}


def assert_c_invariants(c_decision: str) -> None:
    _enforce(
        c_decision in ALLOWED_C_DECISIONS,
        "[C-INV] decision must be STOP/HOLD/REQUEST_TAKEOVER",
    )


def assert_c_input_invariants(system_snapshot: dict) -> None:
    if not isinstance(system_snapshot, dict):
        return
    for key in FORBIDDEN_KEYS_IN_C_INPUT:
        _enforce(key not in system_snapshot, f"[C-INV] must not read {key}")


def assert_no_semantic_leak(c_decision: dict) -> None:
    for forbidden in ("candidates", "assumptions", "options"):
        _enforce(forbidden not in c_decision, "[C-INV] semantic leakage")


REQUIRED_BC_SNAPSHOT_FIELDS = {
    "authority",
    "abilities",
    "gate",
    "decision",
    "distortion",
    "c_decision",
    "bc_action",
    "can_recover",
}


def assert_bc_snapshot_invariants(bc_snapshot: dict) -> None:
    for key in REQUIRED_BC_SNAPSHOT_FIELDS:
        _enforce(key in bc_snapshot, f"[BC-INV] missing snapshot field: {key}")
    for forbidden in ("used_as_input", "fed_back"):
        _enforce(forbidden not in bc_snapshot, "[BC-INV] snapshot write-only")


def assert_bc_used_candidates(
    used_candidates: Iterable[str],
    b_outputs: Iterable[dict],
) -> None:
    model_ids = {o.get("model_id") for o in b_outputs if isinstance(o, dict)}
    for cand in used_candidates:
        _enforce(cand in model_ids, "[BC-INV] used_candidates must come from B")


def assert_bc_decision_not_from_risk(decision_trace: dict) -> None:
    if not isinstance(decision_trace, dict):
        return
    reason = str(decision_trace.get("reason", ""))
    for key in ("risk_level", "risk_type"):
        _enforce(key not in reason, "[BC-INV] must not arbitrate directly on risk")


def assert_risk_not_used_for_decision(result: dict) -> None:
    if not isinstance(result, dict):
        return
    reason = str(result.get("reason", "")).lower()
    _enforce("risk" not in reason, "[BC-INV] risk must not drive decision reason")


def assert_risk_not_lowering_authority(raw, effective, risk_present: bool) -> None:
    if risk_present:
        _enforce(
            _authority_rank(effective) >= _authority_rank(raw),
            "[AUTH-INV] risk must not lower authority",
        )


FORBIDDEN_RISK_OUTPUT_KEYS = {
    "action",
    "decision",
    "must_stop",
    "hold",
    "takeover",
}


def assert_risk_is_readonly(output: dict) -> None:
    if not isinstance(output, dict):
        return
    for key in FORBIDDEN_RISK_OUTPUT_KEYS:
        _enforce(key not in output, "[RISK-INV] must not emit action fields")


def assert_bc_snapshot_risk_invariants(bc_snapshot: dict) -> None:
    risk = bc_snapshot.get("risk", {})
    if not isinstance(risk, dict):
        return
    forbidden = {"action", "decision", "STOP", "HOLD", "REQUEST_TAKEOVER"}
    _enforce(forbidden.isdisjoint(risk.keys()), "[BC-INV] risk must be advisory only")
