"""Declaration-only Runner for A3 Runtime Capability Assessment v1."""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import asdict, replace
from pathlib import Path
from typing import Any

from .cognitive_analysis_runtime_assessment_types_v1 import (
    RUNTIME_CAPABILITY_ASSESSMENT_PHASE_V1,
    RUNTIME_CAPABILITY_ASSESSMENT_RUN_ID_V1,
    CognitiveAnalysisRuntimeCapabilityAssessmentReportV1,
    CognitiveAnalysisRuntimeCapabilityEntryV1,
)


ASSESSMENT_REPORT_FILENAME_V1 = "cognitive_analysis_runtime_capability_assessment_report_v1.json"


def _canonical_json_v1(value: Any) -> str:
    if hasattr(value, "__dataclass_fields__"):
        value = asdict(value)
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def _capability_inventory_v1() -> tuple[CognitiveAnalysisRuntimeCapabilityEntryV1, ...]:
    boundary = "candidate_only; no Fact, Decision, Action, State, or Memory authority"
    return (
        CognitiveAnalysisRuntimeCapabilityEntryV1("context_interpretation_candidate", ("context_ref",), "context_interpretation_candidate", boundary, "context mutation, raw-state access, or Fact claim"),
        CognitiveAnalysisRuntimeCapabilityEntryV1("evidence_relationship_candidate", ("evidence_refs",), "evidence_relationship_candidate", boundary, "evidence inference/mutation or Fact promotion"),
        CognitiveAnalysisRuntimeCapabilityEntryV1("hypothesis_candidate", ("context_ref", "evidence_refs", "hypothesis_refs"), "hypothesis_assessment_candidate", boundary, "hypothesis generation, forced dominance, or Fact promotion"),
        CognitiveAnalysisRuntimeCapabilityEntryV1("uncertainty_assessment_candidate", ("context_ref", "evidence_refs", "hypothesis_refs"), "uncertainty_assessment_candidate", boundary, "unknown completion or suppressed warning"),
        CognitiveAnalysisRuntimeCapabilityEntryV1("semantic_explanation_candidate", ("context_ref", "evidence_refs", "hypothesis_refs", "analysis_question_ref"), "semantic_explanation_candidate", boundary, "Decision/Action plan, State mutation, or Memory update"),
    )


def run_runtime_capability_assessment_v1(
    output_dir: Path,
) -> CognitiveAnalysisRuntimeCapabilityAssessmentReportV1:
    """Write a fixed inventory only; this function never executes analysis."""
    side_effect_evidence = {
        "runtime_executed": "DECLARED_NOT_EXECUTED",
        "model_invoked": "DECLARED_NOT_EXECUTED",
        "evidence_inferred": "DECLARED_NOT_EXECUTED",
        "hypothesis_generated": "DECLARED_NOT_EXECUTED",
        "state_writeback": "DECLARED_NOT_EXECUTED",
        "decision_generated": "DECLARED_NOT_EXECUTED",
        "action_planned": "DECLARED_NOT_EXECUTED",
        "memory_updated": "DECLARED_NOT_EXECUTED",
    }
    provisional = CognitiveAnalysisRuntimeCapabilityAssessmentReportV1(
        phase=RUNTIME_CAPABILITY_ASSESSMENT_PHASE_V1,
        run_id=RUNTIME_CAPABILITY_ASSESSMENT_RUN_ID_V1,
        capabilities=_capability_inventory_v1(),
        runtime_authorized=False,
        runtime_executed=False,
        model_invoked=False,
        evidence_inferred=False,
        hypothesis_generated=False,
        state_writeback=False,
        decision_generated=False,
        action_planned=False,
        memory_updated=False,
        deterministic_output=False,
        warning_codes=("runtime_not_authorized", "capability_assessment_declaration_only"),
        blocker_count=0,
        final_candidate_decision="RUNTIME_CAPABILITY_ASSESSMENT_CANDIDATE_PASS",
        determinism_status="DETERMINISM_UNVERIFIED",
        determinism_evidence={},
        side_effect_evidence=side_effect_evidence,
    )
    input_serialization = _canonical_json_v1([asdict(item) for item in _capability_inventory_v1()])
    input_digest = hashlib.sha256(input_serialization.encode("utf-8")).hexdigest()
    proof_context = {
        "input_identity": "runtime_capability_inventory_v1",
        "input_digest": f"sha256:{input_digest}",
        "reconstruction_a": "independent_inventory_construction_a",
        "reconstruction_b": "independent_inventory_construction_b",
    }
    candidate_a = replace(
        provisional,
        capabilities=_capability_inventory_v1(),
        determinism_evidence=proof_context,
    )
    candidate_b = replace(
        provisional,
        capabilities=_capability_inventory_v1(),
        determinism_evidence=proof_context,
    )
    canonical_a = _canonical_json_v1(candidate_a)
    canonical_b = _canonical_json_v1(candidate_b)
    deterministic = canonical_a == canonical_b
    proof = {
        **proof_context,
        "canonical_digest_a": f"sha256:{hashlib.sha256(canonical_a.encode('utf-8')).hexdigest()}",
        "canonical_digest_b": f"sha256:{hashlib.sha256(canonical_b.encode('utf-8')).hexdigest()}",
        "comparison": "MATCH" if deterministic else "MISMATCH",
    }
    result = replace(
        provisional,
        deterministic_output=deterministic,
        determinism_status="DETERMINISM_VERIFIED" if deterministic else "DETERMINISM_UNVERIFIED",
        determinism_evidence=proof,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / ASSESSMENT_REPORT_FILENAME_V1).write_text(_canonical_json_v1(result), encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    print(_canonical_json_v1(run_runtime_capability_assessment_v1(Path(args.output_dir))))


if __name__ == "__main__":
    main()
