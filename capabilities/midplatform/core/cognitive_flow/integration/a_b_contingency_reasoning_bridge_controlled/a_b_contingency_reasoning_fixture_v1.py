"""Compact synthetic scenario plan for B Contingency Reasoning."""

from __future__ import annotations

from typing import Dict, Tuple


def build_a_b_contingency_cases_v1() -> Tuple[Dict[str, object], ...]:
    rows = [
        ("AB-01", "valid A uncertainty trigger", "TRIGGER"), ("AB-02", "no uncertainty means no B", "TRIGGER"),
        ("AB-03", "missing A REQUEST_B authority", "TRIGGER"), ("AB-04", "wrong Concern", "TRIGGER"),
        ("AB-05", "stale A state", "TRIGGER"), ("AB-06", "revoked A grant", "TRIGGER"),
        ("BG-01", "valid derived B grant", "GRANT"), ("BG-02", "authority outside A delegation scope", "GRANT"),
        ("BG-03", "authority outside B capability boundary", "GRANT"), ("BG-04", "resource limit narrows grant", "GRANT"),
        ("BG-05", "safety limit narrows grant", "GRANT"), ("BG-06", "permission limit narrows grant", "GRANT"),
        ("BR-01", "bounded scenario result", "RESULT"), ("BR-02", "depth limit stop", "RESULT"),
        ("BR-03", "branch limit stop", "RESULT"), ("BR-04", "resource stop", "RESULT"),
        ("BR-05", "stale source result stop", "RESULT"), ("BR-06", "revoked grant result stop", "RESULT"),
        ("RT-01", "B returns to A", "RETURN"), ("RT-02", "B has no direct Loop return", "RETURN"),
        ("RT-03", "B has no direct Brain adoption", "RETURN"), ("RT-04", "B result is non-binding", "RETURN"),
        ("AE-01", "A USE", "EVALUATION"), ("AE-02", "A PARTIAL_USE", "EVALUATION"),
        ("AE-03", "A KEEP_AVAILABLE", "EVALUATION"), ("AE-04", "A SUPERSEDE", "EVALUATION"),
        ("AE-05", "A DISCARD", "EVALUATION"), ("AE-06", "A REQUEST_UPDATED_B", "EVALUATION"),
        ("CC-01", "A active and B active candidate", "CONCURRENCY"),
        ("CC-02", "A paused or waiting and B active candidate", "CONCURRENCY"),
        ("CC-03", "B finish does not auto-resume A", "CONCURRENCY"),
        ("ST-01", "B remains relevant", "STALENESS"), ("ST-02", "B stale after world change", "STALENESS"),
        ("ST-03", "B retained but unused", "STALENESS"),
        ("IS-01", "two B requests and Concerns are isolated", "ISOLATION"),
        ("NG-01", "B escalation and external runtime guards", "NEGATIVE"),
    ]
    return tuple({"scenario_id": i, "title": t, "kind": k} for i, t, k in rows)


__all__ = ["build_a_b_contingency_cases_v1"]
