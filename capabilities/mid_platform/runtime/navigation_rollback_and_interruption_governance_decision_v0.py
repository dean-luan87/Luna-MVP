# -*- coding: utf-8 -*-
"""
Navigation Rollback And Interruption Governance Decision v0 (minimal implementation; non-action).

Builds a unified governance decision result object `navigation_rollback_and_interruption_governance_decision_v0`
from standardized objects (governance entry + executor status + monitoring status; optional wiring status).

Hard boundaries:
- NOT a rollback engine; NOT an interruption engine; NOT a release-control executor.
- Does NOT trigger governance actions; no time/space anchors; no maps; no voice/memory side effects.
- Does NOT read candidate/gate/stub/raw metadata directly.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

_SCOPE = "navigation_rollback_and_interruption_governance_decision_v0"


def _as_dict(x: Any) -> Optional[Dict[str, Any]]:
    return x if isinstance(x, dict) else None


def _extract_tokens(executor_status: Dict[str, Any], monitoring_status: Dict[str, Any]) -> set[str]:
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
    if an.get("suggest_upstream_fallback") is True:
        tokens.add("requires_upstream_intervention")

    tk_fact = str(tk.get("takeover_fact") or "").strip().lower()
    if tk_fact in ("abnormally_released", "unexpected_release", "takeover_abnormal_release"):
        tokens.add("takeover_abnormal_release")

    mex = monitoring_status.get("execution_monitor") if isinstance(monitoring_status.get("execution_monitor"), dict) else {}
    man = monitoring_status.get("anomaly_monitor") if isinstance(monitoring_status.get("anomaly_monitor"), dict) else {}
    mdg = monitoring_status.get("degradation_monitor") if isinstance(monitoring_status.get("degradation_monitor"), dict) else {}

    mex_fact = str(mex.get("execution_monitor_fact") or "").strip().lower()
    if mex_fact in ("failed", "execution_failed"):
        tokens.add("execution_failed")
    if mex_fact in ("interrupted", "execution_interrupted"):
        tokens.add("execution_interrupted")
    if mex_fact in ("degraded", "execution_degraded"):
        tokens.add("execution_degraded")

    man_fact = str(man.get("anomaly_monitor_fact") or "").strip().lower()
    if man_fact in ("offroute", "deviated", "explicit_offroute"):
        tokens.add("explicit_offroute")
    if man_fact in ("unexecutable", "not_executable", "explicit_unexecutable"):
        tokens.add("explicit_unexecutable")

    if mex.get("upstream_report_required") is True or man.get("upstream_report_required") is True:
        tokens.add("requires_upstream_intervention")

    mdg_fact = str(mdg.get("degradation_monitor_fact") or "").strip().lower()
    if mdg_fact in ("degraded", "execution_degraded"):
        tokens.add("execution_degraded")

    return tokens


def evaluate_navigation_rollback_and_interruption_governance_decision_v0(
    *,
    navigation_rollback_and_interruption_governance_entry_v0: Any,
    navigation_real_executor_status_v0: Any,
    navigation_execution_monitoring_status_v0: Any,
    navigation_executor_takeover_wiring_v0: Any = None,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Returns (applicable, payload).

    Output policy (consistent):
    - If governance entry object is missing => relevant-only (False, None).
    - If governance entry exists but is not open => relevant-only (False, None).
    - If entry is open but standardized objects invalid/missing => output blocked.
    - Otherwise => output one of the 5 decision statuses.
    """
    ge = _as_dict(navigation_rollback_and_interruption_governance_entry_v0)
    if not ge:
        return False, None

    if str(ge.get("governance_entry_scope") or "") != "navigation_rollback_and_interruption_governance_entry_v0":
        return False, None
    if str(ge.get("governance_entry_status") or "") != "governance_entry_open":
        return False, None

    st = _as_dict(navigation_real_executor_status_v0)
    mon = _as_dict(navigation_execution_monitoring_status_v0)
    wir = _as_dict(navigation_executor_takeover_wiring_v0)

    if not (st and mon):
        return True, {
            "governance_decision_attempted": True,
            "governance_decision_scope": _SCOPE,
            "governance_decision_status": "governance_decision_blocked",
            "reason": "missing_minimum_standardized_objects",
        }

    if str(st.get("executor_status_scope") or "") != "navigation_real_executor_status_v0" or str(st.get("object_kind") or "") != "implemented_v0":
        return True, {
            "governance_decision_attempted": True,
            "governance_decision_scope": _SCOPE,
            "governance_decision_status": "governance_decision_blocked",
            "reason": "invalid_executor_status_object",
        }
    if str(mon.get("monitoring_status_scope") or "") != "navigation_execution_monitoring_status_v0" or str(mon.get("object_kind") or "") != "implemented_v0":
        return True, {
            "governance_decision_attempted": True,
            "governance_decision_scope": _SCOPE,
            "governance_decision_status": "governance_decision_blocked",
            "reason": "invalid_monitoring_status_object",
        }

    # Optional wiring consistency check (no authority expansion)
    if wir is not None and str(wir.get("wiring_scope") or "") == "navigation_executor_takeover_wiring_v0":
        ws = str(wir.get("wiring_status") or "")
        if ws not in ("wired_ready_to_takeover", "wired_inactive", "not_applicable"):
            return True, {
                "governance_decision_attempted": True,
                "governance_decision_scope": _SCOPE,
                "governance_decision_status": "governance_decision_blocked",
                "reason": "wiring_status_inconsistent",
            }

    tokens = _extract_tokens(st, mon)

    # Minimal decision rules (frozen doc)
    decision = "hold_for_governance"
    if "execution_failed" in tokens or "explicit_unexecutable" in tokens:
        decision = "recommend_rollback"
    elif "execution_interrupted" in tokens or "takeover_abnormal_release" in tokens:
        decision = "recommend_release_control" if "takeover_abnormal_release" in tokens else "recommend_interrupt"
    elif "execution_degraded" in tokens or "explicit_offroute" in tokens or "requires_upstream_intervention" in tokens:
        decision = "recommend_interrupt" if ("explicit_offroute" in tokens) else "hold_for_governance"

    payload = {
        "governance_decision_attempted": True,
        "governance_decision_scope": _SCOPE,
        "governance_decision_status": decision,
        "reason": ("tokens:" + ",".join(sorted(tokens))[:200]) if tokens else "no_tokens",
    }
    return True, payload

