"""Compact synthetic scenario specifications for the working-envelope seam."""

from __future__ import annotations

from typing import Dict, Tuple


def build_scenarios() -> Tuple[Dict[str, object], ...]:
    definitions = (
        ("WE-01", "valid working envelope composition"),
        ("WE-02", "envelope keeps authoritative state as refs"),
        ("WE-03", "Role and Perspective refs preserved"),
        ("WE-04", "Field and Current World refs preserved"),
        ("WE-05", "Context ref preserved"),
        ("WE-06", "Task and Behavior refs preserved"),
        ("WE-07", "Emotion modulation ref preserved"),
        ("WE-08", "Experience prior and Attention refs preserved"),
        ("EI-01", "no material environment impact"),
        ("EI-02", "Role change requires hypothesis reassessment"),
        ("EI-03", "Field change requires Need reassessment"),
        ("EI-04", "Task change requires replan"),
        ("EI-05", "Emotion/resource change affects sufficiency assessment"),
        ("EI-06", "Current World and permission change may pause"),
        ("NR-01", "A forms object-detection cognitive requirement"),
        ("NR-02", "A forms text-recognition cognitive requirement"),
        ("NR-03", "cognitive requirement has no provider identity"),
        ("NR-04", "wrong Concern blocks requirement formation"),
        ("NR-05", "stale A grant blocks requirement formation"),
        ("CB-01", "object requirement is in existing capability scope"),
        ("CB-02", "out-of-scope requirement produces existing gap"),
        ("CB-03", "existing resolution returns a candidate"),
        ("CB-04", "A does not select model or provider"),
        ("CB-05", "Brain does not select model or provider"),
        ("OB-01", "Observation Gateway admits a candidate"),
        ("OB-02", "Observation Gateway boundary can reject a candidate"),
        ("OB-03", "observation path has no real invocation"),
        ("OB-04", "Observation does not create a Cognitive Need"),
        ("ER-01", "evidence returns to A"),
        ("ER-02", "returned evidence can remain insufficient"),
        ("ER-03", "returned evidence can become sufficient"),
        ("ER-04", "returned evidence can trigger A reconsideration and B candidate"),
        ("IV-01", "Current World change creates invalidation"),
        ("IV-02", "Role and Field change create invalidation for A assessment"),
        ("IV-03", "invalidation is not a semantic decision"),
        ("IS-01", "two Concerns, envelopes, and requirements remain isolated"),
    )
    return tuple({"case_id": case_id, "title": title} for case_id, title in definitions)

