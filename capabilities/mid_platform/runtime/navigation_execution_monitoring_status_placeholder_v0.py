from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

_SCOPE = "navigation_execution_monitoring_status_v0"


def _as_dict(x: Any) -> Optional[Dict[str, Any]]:
    if isinstance(x, dict):
        return x
    return None


def evaluate_navigation_execution_monitoring_status_placeholder_v0(
    *,
    navigation_executor_takeover_stub_v0: Any,
    navigation_real_executor_status_v0: Any,
    navigation_real_executor_input_v0: Any = None,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Read-only placeholder that materializes a unified execution-monitoring status object.

    Relevant-only: if minimum upstream evidence is not present, returns (False, None).
    Must NOT simulate real execution states; emits placeholder states only.
    """
    tk = _as_dict(navigation_executor_takeover_stub_v0)
    st = _as_dict(navigation_real_executor_status_v0)
    inp = _as_dict(navigation_real_executor_input_v0)

    if not (tk and st):
        return False, None

    # Minimal sanity: ensure inputs are from our known scopes (avoid treating unrelated dicts as evidence).
    if str(tk.get("takeover_scope") or "") != "navigation_executor_takeover_stub_v0":
        return False, None
    if str(st.get("executor_status_scope") or "") != "navigation_real_executor_status_v0":
        return False, None

    if inp is not None:
        if str(inp.get("executor_input_scope") or "") != "navigation_real_executor_input_v0":
            return False, None
        if str(inp.get("consume_mode") or "") != "read_only":
            return False, None

    # Placeholder monitoring object MUST NOT look like a running monitoring loop.
    return True, {
        "monitoring_status_present": True,
        "monitoring_status_scope": _SCOPE,
        "takeover_monitor_state": "pre_execution_placeholder",
        "execution_monitor_state": "not_started_placeholder",
        "anomaly_monitor_state": "unknown_placeholder",
        "degradation_monitor_state": "unknown_placeholder",
        "upstream_report_required": False,
        "consume_mode": "read_only",
    }

