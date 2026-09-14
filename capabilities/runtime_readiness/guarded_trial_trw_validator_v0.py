# -*- coding: utf-8 -*-
"""
Guarded trial TRW field validation skeleton v0.

Does not fabricate missing trace_id/session_id; records them in missing_fields.
"""

from __future__ import annotations

from typing import Any, Dict, List, Mapping, MutableMapping


def _non_empty(val: Any) -> bool:
    if val is None:
        return False
    if isinstance(val, str):
        return bool(val.strip())
    if isinstance(val, (dict, list)):
        return len(val) > 0
    return True


def _pending_ref_ok(d: Mapping[str, Any]) -> bool:
    p = d.get("pending_ref")
    return p is True or p == "true" or p == 1 or p == "1"


def validate_guarded_trial_trw_fields_v0(trw: Mapping[str, Any]) -> Dict[str, Any]:
    """
    Validate minimal TRW envelope for guarded trials.

    trace_id / session_id are optional for validity but listed in missing_fields when absent.
    """
    missing: List[str] = []
    d: Dict[str, Any] = dict(trw) if trw is not None else {}

    if not _non_empty(d.get("request_id")):
        missing.append("request_id")
    if not _non_empty(d.get("hard_audit")):
        missing.append("hard_audit")

    if not (_non_empty(d.get("runtime_run_id")) or _non_empty(d.get("source_run_id"))):
        missing.append("runtime_run_id_or_source_run_id")

    for opt in ("trace_id", "session_id"):
        if not _non_empty(d.get(opt)):
            missing.append(opt)

    refs_present = all(_non_empty(d.get(k)) for k in ("trace_ref", "replay_ref", "whitebox_ref"))
    if not refs_present and not _pending_ref_ok(d):
        for k in ("trace_ref", "replay_ref", "whitebox_ref"):
            if not _non_empty(d.get(k)):
                missing.append(k)

    critical_fail = (
        not _non_empty(d.get("request_id"))
        or not _non_empty(d.get("hard_audit"))
        or not (_non_empty(d.get("runtime_run_id")) or _non_empty(d.get("source_run_id")))
        or (not refs_present and not _pending_ref_ok(d))
    )

    valid = not critical_fail
    return {
        "valid": valid,
        "decision": "ok" if valid else "blocked_missing_trw",
        "missing_fields": missing,
        "note": None if valid else "missing_required_trw_fields",
    }


def attach_missing_fields_record_v0(target: MutableMapping[str, Any], missing: List[str]) -> None:
    """Helper: write missing_fields sidecar without inventing trace/session."""
    target["missing_fields"] = list(missing)
