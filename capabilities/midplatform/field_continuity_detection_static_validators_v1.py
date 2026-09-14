# -*- coding: utf-8 -*-
"""Field Continuity Detection — static validators v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.midplatform.field_continuity_detection_types_v1 import (
    CONTINUITY_STATUSES,
    DECISION_FIELDS,
    NON_EXECUTION_FLAGS,
    RECOMMENDED_ACTIONS,
    SIGNAL_RESULT_FIELDS,
    SUPPORT_STATUSES,
)


def validate_signal_result_candidate(sig: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in SIGNAL_RESULT_FIELDS if f not in sig]
    if sig.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    if sig.get("support_status") not in SUPPORT_STATUSES:
        issues.append("invalid_support_status")
    return len(issues) == 0, issues


def validate_signal_bundle_candidate(bundle: Dict[str, Any]) -> Tuple[bool, List[str]]:
    signals = bundle.get("signals") or []
    if len(signals) < 8:
        return False, ["insufficient_signals"]
    issues: List[str] = []
    for s in signals:
        ok, sub = validate_signal_result_candidate(s)
        if not ok:
            issues.extend(sub)
    return len(issues) == 0, issues


def validate_continuity_decision_candidate(dec: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in DECISION_FIELDS if f not in dec]
    if dec.get("continuity_status") not in CONTINUITY_STATUSES:
        issues.append("invalid_continuity_status")
    if dec.get("recommended_action") not in RECOMMENDED_ACTIONS:
        issues.append("invalid_recommended_action")
    flags = dec.get("non_execution_flags") or {}
    if flags.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    return len(issues) == 0, issues


def validate_state_transition_candidate(tr: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    for f in ("transition_id", "from_state", "to_state", "transition_allowed", "candidate_only"):
        if f not in tr:
            issues.append(f"missing_{f}")
    if tr.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    return len(issues) == 0, issues


def validate_dryrun_result_candidate(res: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    for f in ("case_id", "expected_status", "actual_status", "expected_action", "actual_action", "case_passed"):
        if f not in res:
            issues.append(f"missing_{f}")
    return len(issues) == 0, issues


def validate_non_execution_boundary(flags: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [k for k, v in NON_EXECUTION_FLAGS.items() if flags.get(k) is not True]
    return len(issues) == 0, issues
