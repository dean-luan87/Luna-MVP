"""Synthetic scenario specifications for the A semantic migration seam."""

from __future__ import annotations

from typing import Dict, Tuple


def build_a_owned_semantic_decision_cases_v1() -> Tuple[Dict[str, object], ...]:
    rows = [
        ("ND-01", "valid A Current Need decision", "NEED", None),
        ("ND-02", "A selects one Need among alternatives", "NEED", None),
        ("ND-03", "missing SELECT_CURRENT_NEED grant", "NEED", "AUTHORITY_NOT_GRANTED"),
        ("ND-04", "stale A grant cannot select Need", "NEED", "STALE_STATE_VERSION"),
        ("ND-05", "wrong Concern and wrong Work Need scopes blocked", "NEED", "SCOPE_MISMATCH"),
        ("ND-06", "wrong receiver role cannot decide Need", "NEED", "AUTHORITY_NOT_GRANTED"),
        ("ND-07", "revoked and expired A grants cannot decide Need", "NEED", None),
        ("SF-01", "A judges SUFFICIENT", "SUFFICIENCY", None),
        ("SF-02", "A judges INSUFFICIENT", "SUFFICIENCY", None),
        ("SF-03", "A judges REQUIRES_RECONSIDERATION", "SUFFICIENCY", None),
        ("SF-04", "missing local sufficiency authority", "SUFFICIENCY", "AUTHORITY_NOT_GRANTED"),
        ("RC-01", "hypothesis invalidated by new evidence", "RECONSIDERATION", None),
        ("RC-02", "stale Requirement enters A reconsideration", "RECONSIDERATION", None),
        ("RC-03", "A emits replacement Need", "RECONSIDERATION", None),
        ("RC-04", "A records no reconsideration", "RECONSIDERATION", None),
        ("NS-01", "A chooses CONTINUE", "NEXT_STEP", None),
        ("NS-02", "A chooses REQUEST_MORE_EVIDENCE", "NEXT_STEP", None),
        ("NS-03", "A chooses REPLAN", "NEXT_STEP", None),
        ("NS-04", "A chooses STOP_SUFFICIENT", "NEXT_STEP", None),
        ("NS-05", "A chooses WAIT", "NEXT_STEP", None),
        ("NS-06", "A chooses PAUSE", "NEXT_STEP", None),
        ("NS-07", "A chooses DEFER", "NEXT_STEP", None),
        ("CW-01", "Dynamic Flow INSUFFICIENT mapped to A", "COMPATIBILITY", None),
        ("CW-02", "Dynamic Flow SUFFICIENT mapped to A", "COMPATIBILITY", None),
        ("CW-03", "Dynamic Flow RECONSIDER mapped to A", "COMPATIBILITY", None),
        ("CW-04", "compatibility owner is A, not Dynamic Flow", "COMPATIBILITY", None),
        ("MC-01", "Need decision maps to RECORD_NEED_REF", "MECHANICAL", None),
        ("MC-02", "STOP_SUFFICIENT maps to CLOSE and FREEZE", "MECHANICAL", None),
        ("MC-03", "REPLAN maps to mechanical records only", "MECHANICAL", None),
        ("MC-04", "WAIT maps to mechanical WAIT", "MECHANICAL", None),
        ("MC-05", "Loop does not infer semantic disposition", "MECHANICAL", None),
        ("IS-01", "two Concerns remain isolated", "ISOLATION", None),
        ("IS-02", "two A grants remain isolated", "ISOLATION", None),
        ("IS-03", "two Loop states remain isolated", "ISOLATION", None),
        ("NG-01", "no Brain/B/provider/action mutation or external runtime", "NEGATIVE", None),
        ("NG-02", "no Memory/Experience/Scheduler mutation", "NEGATIVE", None),
    ]
    return tuple(
        {
            "scenario_id": scenario_id,
            "title": title,
            "kind": kind,
            "expected_failure_class": expected_failure_class,
        }
        for scenario_id, title, kind, expected_failure_class in rows
    )


__all__ = ["build_a_owned_semantic_decision_cases_v1"]
