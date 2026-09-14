"""Plane A behavioral assertions for the minimum sufficient cognition loop."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from capabilities.midplatform.core.a_route_orchestration.a_route_orchestration_core_types_v1 import (
    ARouteCognitiveExecutionEvidenceV1,
)


PLANE_A_ASSERTION_STATUSES = ("PASS", "FAIL", "NOT_APPLICABLE", "INCOMPLETE")
PLANE_A_ASSERTION_IDS = (
    "COGNITION_EXECUTED",
    "SUFFICIENCY_BEHAVIOR",
    "REOBSERVATION_BEHAVIOR",
    "STOP_CORRECTNESS",
    "HYPOTHESIS_REVISION_BEHAVIOR",
    "MINIMUM_SUFFICIENT_COGNITION",
)


@dataclass(frozen=True)
class PlaneAAssertionResultV1:
    assertion_id: str
    status: str
    evidence_refs: Tuple[str, ...]
    notes: str


@dataclass(frozen=True)
class PlaneALoopResultV1:
    result_ref: str
    case_ref: str
    expected_behavior: str
    status: str
    assertion_results: Tuple[PlaneAAssertionResultV1, ...]
    evaluation_only: bool = True


def _result(assertion_id: str, status: str, proof: ARouteCognitiveExecutionEvidenceV1, refs: Tuple[str, ...], notes: str):
    return PlaneAAssertionResultV1(assertion_id, status, refs or (proof.execution_ref,), notes)


def evaluate_plane_a_loop_case_v1(
    *,
    result_ref: str,
    case_ref: str,
    expected_behavior: str,
    proofs: Tuple[ARouteCognitiveExecutionEvidenceV1, ...],
    unnecessary_observation: bool,
) -> PlaneALoopResultV1:
    if not proofs:
        raise ValueError("plane_a_requires_canonical_proof")
    first = proofs[0]
    final = proofs[-1]
    multi_cycle = len(proofs) == 2
    has_gap = any(proof.information_gap_ref for proof in proofs)
    has_reobservation = any(proof.reobservation_ref for proof in proofs)
    has_revision = any(proof.hypothesis_revision_ref for proof in proofs)
    has_stop = final.stop_ref is not None
    sufficient_final = final.sufficiency_status == "SUFFICIENT"
    assertions = (
        _result("COGNITION_EXECUTED", "PASS" if all(p.runtime_executed for p in proofs) else "FAIL", final, tuple(p.execution_ref for p in proofs), "canonical runtime execution proof"),
        _result("SUFFICIENCY_BEHAVIOR", "PASS" if sufficient_final and all(p.sufficiency_ref for p in proofs) else "FAIL", final, tuple(p.sufficiency_ref for p in proofs if p.sufficiency_ref), "canonical sufficiency refs and final sufficient state"),
        _result("REOBSERVATION_BEHAVIOR", ("PASS" if has_gap and has_reobservation and multi_cycle else "NOT_APPLICABLE") if expected_behavior == "sufficient-and-stop" else ("PASS" if has_gap and has_reobservation else "FAIL"), final, tuple(p.reobservation_ref for p in proofs if p.reobservation_ref), "gap-triggered re-observation"),
        _result("STOP_CORRECTNESS", "PASS" if has_stop and sufficient_final and final.stop_reason else "FAIL", final, (final.stop_ref,) if final.stop_ref else (), "stop follows final sufficiency with explicit reason"),
        _result("HYPOTHESIS_REVISION_BEHAVIOR", ("PASS" if has_revision else "FAIL") if expected_behavior != "sufficient-and-stop" else "NOT_APPLICABLE", final, tuple(p.hypothesis_revision_ref for p in proofs if p.hypothesis_revision_ref), "second-cycle hypothesis revision"),
        _result("MINIMUM_SUFFICIENT_COGNITION", "PASS" if not unnecessary_observation and sufficient_final else "FAIL", final, (final.sufficiency_ref,) if final.sufficiency_ref else (), "no unnecessary observation after minimum sufficiency"),
    )
    status = "PASS" if all(item.status in {"PASS", "NOT_APPLICABLE"} for item in assertions) else "FAIL"
    return PlaneALoopResultV1(result_ref, case_ref, expected_behavior, status, assertions)


def validate_plane_a_loop_result_v1(result: PlaneALoopResultV1) -> Tuple[str, ...]:
    errors = []
    if not result.evaluation_only or result.status not in {"PASS", "FAIL", "INCOMPLETE"}:
        errors.append("plane_a_loop_result_boundary_invalid")
    if tuple(item.assertion_id for item in result.assertion_results) != PLANE_A_ASSERTION_IDS:
        errors.append("plane_a_assertion_set_invalid")
    for item in result.assertion_results:
        if item.status not in PLANE_A_ASSERTION_STATUSES:
            errors.append(f"plane_a_assertion_status_invalid:{item.assertion_id}")
    return tuple(errors)
