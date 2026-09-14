# -*- coding: utf-8 -*-
"""
Navigation Rollback And Interruption Governance Entry v0 (minimal implementation; non-action).

Builds a unified governance entry result object `navigation_rollback_and_interruption_governance_entry_v0`
from already-attached standardized objects (executor status + monitoring status; optional wiring status).

Hard boundaries:
- NOT a rollback engine; NOT an interruption engine; does NOT trigger governance actions.
- Does NOT fabricate missing standardized objects; no time/space anchors; no maps; no voice/memory side effects.
- Does NOT read candidate/gate/stub/raw metadata directly (only consumes standardized objects + optional wiring result).
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

_SCOPE = "navigation_rollback_and_interruption_governance_entry_v0"


def _as_dict(x: Any) -> Optional[Dict[str, Any]]:
    return x if isinstance(x, dict) else None


def _truthy(x: Any) -> bool:
    return x is True


def _extract_executor_governance_triggers(executor_status: Dict[str, Any]) -> set[str]:
    """
    Extracts minimal governance-trigger tokens from implemented executor status object.
    This function is intentionally conservative and only recognizes explicit tokens.
    """
    tokens: set[str] = set()
    ex = executor_status.get("execution_state") if isinstance(executor_status.get("execution_state"), dict) else {}
    an = executor_status.get("anomaly_state") if isinstance(executor_status.get("anomaly_state"), dict) else {}
    tk = executor_status.get("takeover_state") if isinstance(executor_status.get("takeover_state"), dict) else {}

    ex_fact = str(ex.get("execution_fact") or "").strip().lower()
    if ex_fact in ("failed", "execution_failed"):
        tokens.add("execution_failed")
    if ex_fact in ("interrupted", "execution_interrupted"):
        tokens.add("execution_interrupted")
    if ex_fact in ("degraded", "execution_degraded"):
        tokens.add("execution_degraded")

    an_fact = str(an.get("anomaly_fact") or "").strip().lower()
    if an_fact in ("offroute", "deviated", "explicit_offroute"):
        tokens.add("explicit_offroute")
    if an_fact in ("unexecutable", "not_executable", "explicit_unexecutable"):
        tokens.add("explicit_unexecutable")
    if an_fact in ("requires_upstream_intervention", "needs_upstream", "upstream_required"):
        tokens.add("requires_upstream_intervention")
    if _truthy(an.get("suggest_upstream_fallback")):
        tokens.add("requires_upstream_intervention")

    tk_fact = str(tk.get("takeover_fact") or "").strip().lower()
    if tk_fact in ("abnormally_released", "unexpected_release", "takeover_abnormal_release"):
        tokens.add("takeover_abnormal_release")

    return tokens


def _extract_monitoring_governance_triggers(monitoring_status: Dict[str, Any]) -> set[str]:
    """
    Extracts minimal governance-trigger tokens from implemented monitoring status object.
    """
    tokens: set[str] = set()
    ex = monitoring_status.get("execution_monitor") if isinstance(monitoring_status.get("execution_monitor"), dict) else {}
    an = monitoring_status.get("anomaly_monitor") if isinstance(monitoring_status.get("anomaly_monitor"), dict) else {}
    dg = monitoring_status.get("degradation_monitor") if isinstance(monitoring_status.get("degradation_monitor"), dict) else {}

    ex_fact = str(ex.get("execution_monitor_fact") or "").strip().lower()
    if ex_fact in ("failed", "execution_failed"):
        tokens.add("execution_failed")
    if ex_fact in ("interrupted", "execution_interrupted"):
        tokens.add("execution_interrupted")
    if ex_fact in ("degraded", "execution_degraded"):
        tokens.add("execution_degraded")

    an_fact = str(an.get("anomaly_monitor_fact") or "").strip().lower()
    if an_fact in ("offroute", "deviated", "explicit_offroute"):
        tokens.add("explicit_offroute")
    if an_fact in ("unexecutable", "not_executable", "explicit_unexecutable"):
        tokens.add("explicit_unexecutable")
    if an_fact in ("requires_upstream_intervention", "needs_upstream", "upstream_required"):
        tokens.add("requires_upstream_intervention")

    if _truthy(ex.get("upstream_report_required")) or _truthy(an.get("upstream_report_required")):
        tokens.add("requires_upstream_intervention")

    dg_fact = str(dg.get("degradation_monitor_fact") or "").strip().lower()
    if dg_fact in ("degraded", "execution_degraded"):
        tokens.add("execution_degraded")

    return tokens


def evaluate_navigation_rollback_and_interruption_governance_entry_v0(
    *,
    navigation_real_executor_status_v0: Any,
    navigation_execution_monitoring_status_v0: Any,
    navigation_executor_takeover_wiring_v0: Any = None,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Returns (applicable, payload).

    Output policy (consistent):
    - If standardized objects (executor status + monitoring status) both exist and are valid => output tri-state.
    - If both are missing => relevant-only (False, None).
    """
    st = _as_dict(navigation_real_executor_status_v0)
    mon = _as_dict(navigation_execution_monitoring_status_v0)
    wir = _as_dict(navigation_executor_takeover_wiring_v0)

    if not (st or mon or wir):
        return False, None
    if not (st and mon):
        # Some evidence exists but minimal standardized objects missing => blocked.
        payload = {
            "governance_entry_attempted": True,
            "governance_entry_scope": _SCOPE,
            "governance_entry_status": "governance_entry_blocked",
            "reason": "missing_minimum_standardized_objects",
        }
        return True, payload

    # Validate implemented executor status object
    if str(st.get("executor_status_scope") or "") != "navigation_real_executor_status_v0":
        return True, {
            "governance_entry_attempted": True,
            "governance_entry_scope": _SCOPE,
            "governance_entry_status": "governance_entry_blocked",
            "reason": "invalid_executor_status_scope",
        }
    if str(st.get("object_kind") or "") != "implemented_v0":
        return True, {
            "governance_entry_attempted": True,
            "governance_entry_scope": _SCOPE,
            "governance_entry_status": "governance_entry_blocked",
            "reason": "executor_status_not_implemented",
        }

    # Validate implemented monitoring status object
    if str(mon.get("monitoring_status_scope") or "") != "navigation_execution_monitoring_status_v0":
        return True, {
            "governance_entry_attempted": True,
            "governance_entry_scope": _SCOPE,
            "governance_entry_status": "governance_entry_blocked",
            "reason": "invalid_monitoring_status_scope",
        }
    if str(mon.get("object_kind") or "") != "implemented_v0":
        return True, {
            "governance_entry_attempted": True,
            "governance_entry_scope": _SCOPE,
            "governance_entry_status": "governance_entry_blocked",
            "reason": "monitoring_status_not_implemented",
        }

    # Optional wiring consistency check (must NOT expand authority)
    if wir is not None:
        if str(wir.get("wiring_scope") or "") == "navigation_executor_takeover_wiring_v0":
            ws = str(wir.get("wiring_status") or "")
            if ws not in ("wired_ready_to_takeover", "wired_inactive", "not_applicable"):
                return True, {
                    "governance_entry_attempted": True,
                    "governance_entry_scope": _SCOPE,
                    "governance_entry_status": "governance_entry_blocked",
                    "reason": "wiring_status_inconsistent",
                }

    tokens = set()
    tokens |= _extract_executor_governance_triggers(st)
    tokens |= _extract_monitoring_governance_triggers(mon)

    # Minimal eligible event set (design doc)
    eligible = {
        "execution_failed",
        "execution_interrupted",
        "execution_degraded",
        "explicit_offroute",
        "explicit_unexecutable",
        "takeover_abnormal_release",
        "requires_upstream_intervention",
    }
    hit = [t for t in sorted(tokens) if t in eligible]

    if hit:
        status = "governance_entry_open"
        reason = "eligible_event_detected:" + ",".join(hit[:6])
    else:
        status = "governance_entry_not_applicable"
        reason = "no_eligible_event"

    payload = {
        "governance_entry_attempted": True,
        "governance_entry_scope": _SCOPE,
        "governance_entry_status": status,
        "reason": reason[:240],
    }
    return True, payload

