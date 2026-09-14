"""Synthetic scenario specifications for authority-grant control."""

from __future__ import annotations

from typing import Dict, Tuple


def build_authority_grant_cases_v1() -> Tuple[Dict[str, object], ...]:
    rows = [
        ("AG-01", "valid A grant", "A_GRANT", None),
        ("AG-02", "missing Concern scope", "A_GRANT", "SCOPE_MISMATCH"),
        ("AG-03", "wrong receiver role", "A_GRANT", "AUTHORITY_NOT_GRANTED"),
        ("AG-04", "unsupported authority", "A_GRANT", "CAPABILITY_BOUNDARY_VIOLATION"),
        ("AG-05", "authority outside A boundary", "A_GRANT", "CAPABILITY_BOUNDARY_VIOLATION"),
        ("AG-06", "stale source state", "A_GRANT", "STALE_STATE_VERSION"),
        ("AG-07", "revoked grant", "A_GRANT", "GRANT_REVOKED"),
        ("AG-08", "expired grant", "A_GRANT", "GRANT_EXPIRED"),
        ("AG-09", "invalid responsibility binding", "A_GRANT", "RESPONSIBILITY_BINDING_INVALID"),
        ("MC-01", "accepted mechanical persistence", "MECHANICAL", None),
        ("MC-02", "forbidden semantic command", "MECHANICAL", "CAPABILITY_BOUNDARY_VIOLATION"),
        ("MC-03", "record state version", "MECHANICAL", None),
        ("MC-04", "pause mechanically", "MECHANICAL", None),
        ("MC-05", "wait mechanically", "MECHANICAL", None),
        ("MC-06", "resume recorded state", "MECHANICAL", None),
        ("MC-07", "freeze final state", "MECHANICAL", None),
        ("MC-08", "archive history boundary", "MECHANICAL", None),
        ("MC-09", "stored refs do not become semantic judgment", "MECHANICAL", None),
        ("BG-01", "valid derived B grant", "B_DERIVATION", None),
        ("BG-02", "A lacks REQUEST_B", "B_DERIVATION", "AUTHORITY_NOT_GRANTED"),
        ("BG-03", "B authority expansion blocked", "B_DERIVATION", "CAPABILITY_BOUNDARY_VIOLATION"),
        ("BG-04", "B Concern creation blocked", "B_DERIVATION", "CAPABILITY_BOUNDARY_VIOLATION"),
        ("BG-05", "recursive B request blocked", "B_DERIVATION", "AUTHORITY_NOT_GRANTED"),
        ("BG-06", "B Loop control blocked", "B_DERIVATION", "CAPABILITY_BOUNDARY_VIOLATION"),
        ("BG-07", "B resource expansion blocked", "B_DERIVATION", "SCOPE_MISMATCH"),
        ("BG-08", "B depth expansion blocked", "B_DERIVATION", "SCOPE_MISMATCH"),
        ("RB-01", "valid responsibility binding", "BINDING", None),
        ("RB-02", "no authority and no responsibility", "BINDING", "RESPONSIBILITY_BINDING_INVALID"),
        ("RB-03", "authority requires responsibility", "BINDING", "RESPONSIBILITY_BINDING_INVALID"),
        ("RB-04", "result receiver preserved", "BINDING", None),
        ("RB-05", "error owner preserved", "BINDING", None),
        ("IS-01", "two Concern grants do not cross", "ISOLATION", "SCOPE_MISMATCH"),
        ("IS-02", "two Loop instances do not cross mutate", "ISOLATION", None),
        ("IS-03", "same A role has separate scopes", "ISOLATION", "SCOPE_MISMATCH"),
        ("NG-01", "candidate-only runtime guards", "NEGATIVE", None),
        ("NG-02", "no external execution or mutation", "NEGATIVE", None),
    ]
    return tuple(
        {
            "scenario_id": case_id,
            "title": title,
            "kind": kind,
            "expected_failure_class": expected,
        }
        for case_id, title, kind, expected in rows
    )


__all__ = ["build_authority_grant_cases_v1"]
