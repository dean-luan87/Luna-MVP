"""Focused synthetic scenarios for the first Loop semantic cutover."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class CutoverScenarioSpecV1:
    scenario_id: str
    title: str
    family: str
    disposition: str = ""
    closure_reason: str = ""
    closure_disposition: str = ""
    expected_accepted: bool = True
    invalid_issuer: bool = False
    stale_state: bool = False
    revoked: bool = False
    expired: bool = False
    compatibility_source_only: bool = False
    changed_refs: bool = False
    cross_concern: bool = False
    brain_owner: bool = False
    missing_reason: bool = False


def build_cutover_scenario_specs_v1() -> Tuple[CutoverScenarioSpecV1, ...]:
    return (
        CutoverScenarioSpecV1("RS-01", "A supplies KEEP resume", "RESUME", "KEEP"),
        CutoverScenarioSpecV1("RS-02", "A supplies REPLAN resume", "RESUME", "REPLAN"),
        CutoverScenarioSpecV1("RS-03", "A supplies SUPERSEDE resume", "RESUME", "SUPERSEDE"),
        CutoverScenarioSpecV1("RS-04", "A supplies COMPLETE resume", "RESUME", "COMPLETE"),
        CutoverScenarioSpecV1("RS-05", "A supplies WAITING resume", "RESUME", "WAITING"),
        CutoverScenarioSpecV1("RS-06", "non-A issuer cannot supply resume", "RESUME", "KEEP", expected_accepted=False, invalid_issuer=True),
        CutoverScenarioSpecV1("RS-07", "stale source cannot supply resume", "RESUME", "REPLAN", expected_accepted=False, stale_state=True),
        CutoverScenarioSpecV1("RS-08", "revoked grant cannot supply resume", "RESUME", "KEEP", expected_accepted=False, revoked=True),
        CutoverScenarioSpecV1("RS-09", "expired grant cannot supply resume", "RESUME", "KEEP", expected_accepted=False, expired=True),
        CutoverScenarioSpecV1("LD-01", "A supplies SUFFICIENT disposition", "LOCAL", "SUFFICIENT"),
        CutoverScenarioSpecV1("LD-02", "A supplies INSUFFICIENT disposition", "LOCAL", "INSUFFICIENT"),
        CutoverScenarioSpecV1("LD-03", "A supplies RECONSIDER disposition", "LOCAL", "RECONSIDER"),
        CutoverScenarioSpecV1("LD-04", "A supplies DEFER disposition", "LOCAL", "DEFER"),
        CutoverScenarioSpecV1("LD-05", "Loop records supplied disposition only", "LOCAL", "INSUFFICIENT"),
        CutoverScenarioSpecV1("LD-06", "legacy local output is compatibility-only", "LOCAL", "RECONSIDER", compatibility_source_only=True),
        CutoverScenarioSpecV1("CL-01", "concern resolved supplied by A", "CLOSURE", closure_reason="COGNITIVE_CONCERN_RESOLVED", closure_disposition="COMPLETED"),
        CutoverScenarioSpecV1("CL-02", "Brain governed stop supplied", "CLOSURE", closure_reason="BRAIN_GOVERNED_STOP", closure_disposition="STOPPED", brain_owner=True),
        CutoverScenarioSpecV1("CL-03", "intent superseded supplied", "CLOSURE", closure_reason="INTENT_SUPERSEDED", closure_disposition="SUPERSEDED"),
        CutoverScenarioSpecV1("CL-04", "safety termination supplied", "CLOSURE", closure_reason="SAFETY_GOVERNED_TERMINATION", closure_disposition="STOPPED"),
        CutoverScenarioSpecV1("CL-05", "resource value stop supplied", "CLOSURE", closure_reason="RESOURCE_VALUE_TOO_LOW", closure_disposition="ABANDONED_BY_VALUE"),
        CutoverScenarioSpecV1("CL-06", "Loop cannot construct closure reason", "CLOSURE", closure_reason="", closure_disposition="COMPLETED", expected_accepted=False, missing_reason=True),
        CutoverScenarioSpecV1("CL-07", "closure rejected before mechanical close", "CLOSURE", closure_reason="COGNITIVE_CONCERN_RESOLVED", closure_disposition="COMPLETED", expected_accepted=False, revoked=True),
        CutoverScenarioSpecV1("CT-01", "changed refs with supplied KEEP", "CONTINUITY", "KEEP", changed_refs=True),
        CutoverScenarioSpecV1("CT-02", "changed refs with supplied REPLAN", "CONTINUITY", "REPLAN", changed_refs=True),
        CutoverScenarioSpecV1("CT-03", "same refs with supplied SUPERSEDE", "CONTINUITY", "SUPERSEDE"),
        CutoverScenarioSpecV1("CT-04", "raw comparison is not semantic judgment", "CONTINUITY", "KEEP", changed_refs=True),
        CutoverScenarioSpecV1("IS-01", "two Loop instances remain isolated", "ISOLATION"),
        CutoverScenarioSpecV1("IS-02", "two grants remain isolated", "ISOLATION"),
        CutoverScenarioSpecV1("IS-03", "cross-concern command is rejected", "ISOLATION", cross_concern=True, expected_accepted=False),
        CutoverScenarioSpecV1("NG-01", "Loop semantic command is rejected", "NEGATIVE", expected_accepted=False),
        CutoverScenarioSpecV1("NG-02", "no Provider/model/runtime path", "NEGATIVE"),
        CutoverScenarioSpecV1("NG-03", "no Action/Learning/Memory path", "NEGATIVE"),
        CutoverScenarioSpecV1("NG-04", "legacy helpers are compatibility source only", "NEGATIVE", compatibility_source_only=True),
    )


__all__ = ["CutoverScenarioSpecV1", "build_cutover_scenario_specs_v1"]
