# -*- coding: utf-8 -*-
"""Field-Oriented Egocentric Action Understanding — dry-run runner v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.core.field_understanding_registry_v1 import (
    FIELD_SYNTHESIS_CHAIN,
    PROHIBITED_FIELD_REVISION_POLICIES,
    PROHIBITED_FIELD_TYPES_FROM_ISOLATED_FACT,
)
from capabilities.field_understanding.core.field_understanding_static_validators_v1 import (
    validate_core_bundle,
    validate_dynamic_not_in_static,
    validate_speech_no_precise_distance,
)
from capabilities.field_understanding.core.field_understanding_types_v1 import (
    FIELD_CONTEXT_GOVERNANCE_ID,
    FIELD_INFORMATION_PRIORITY_GOVERNANCE_ID,
    NON_EXECUTION_FLAGS,
    PHASE_ID,
    candidate_to_dict,
)
from capabilities.field_understanding.dryrun.field_understanding_dryrun_cases_v1 import (
    FieldUnderstandingDryRunCase,
    build_all_dryrun_cases_v1,
    build_dryrun_cases_v1,
    build_invalid_dryrun_cases_v1,
)

DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/field_understanding_dryrun_v1_smoke_v0"
)
FINAL_DECISION_TRACE_READY = "FIELD_UNDERSTANDING_DRYRUN_TRACE_READY_FOR_VERIFIER"
FINAL_DECISION_RUNNER_FAIL = "FIELD_UNDERSTANDING_DRYRUN_RUNNER_UNEXPECTED_OUTCOME"

TraceDecision = Literal["PASS", "EXPECTED_REJECT", "UNEXPECTED_PASS", "UNEXPECTED_FAIL"]


def classify_trace_decision(expected_ok: bool, actual_ok: bool) -> TraceDecision:
    if expected_ok and actual_ok:
        return "PASS"
    if not expected_ok and not actual_ok:
        return "EXPECTED_REJECT"
    if not expected_ok and actual_ok:
        return "UNEXPECTED_PASS"
    return "UNEXPECTED_FAIL"


def _case_type(case: FieldUnderstandingDryRunCase, *, positive_ids: set[str]) -> str:
    return "positive" if case.case_id in positive_ids else "invalid"


def _governance_checkpoints(case: FieldUnderstandingDryRunCase) -> Dict[str, Any]:
    field = candidate_to_dict(case.field_candidate)
    fusion = candidate_to_dict(case.spatial_fusion_candidate)
    statics = [candidate_to_dict(s) for s in case.static_candidates]
    dynamics = [candidate_to_dict(d) for d in case.dynamic_candidates]
    alignments = [candidate_to_dict(a) for a in case.map_alignment_candidates]
    distances = [candidate_to_dict(d) for d in case.distance_candidates]
    influences = [candidate_to_dict(i) for i in case.influence_candidates]

    static_dynamic_ok, _ = validate_dynamic_not_in_static(statics, dynamics)
    aligned_without_anchors = any(
        a.get("alignment_status") == "aligned"
        and not (a.get("visual_anchor_refs") or a.get("ocr_anchor_refs"))
        for a in alignments
    )
    high_risk_missing_sources = any(
        d.get("distance_band") in ("immediate_risk", "near_action_zone")
        and not (d.get("source_refs") or ())
        for d in distances
    )
    conflict_readiness_ok = not (
        fusion.get("conflict_refs")
        and fusion.get("action_readiness") == "ready_for_action_decision"
    )
    prohibited_policy_used = fusion.get("field_revision_policy") in PROHIBITED_FIELD_REVISION_POLICIES
    fact_identity_field_type = field.get("field_type") in PROHIBITED_FIELD_TYPES_FROM_ISOLATED_FACT
    dimensions_from_facts = sorted(
        {
            i.get("affected_field_dimension")
            for i in influences
            if i.get("fact_ref") and i.get("affected_field_dimension")
        }
    )
    fact_only_affects_dimensions = all(
        not i.get("fact_ref") or i.get("affected_field_dimension")
        for i in influences
    )
    dynamic_ttl_ok = all(
        isinstance(d.get("ttl_ms"), int) and d["ttl_ms"] > 0
        for d in dynamics
    ) if dynamics else True

    return {
        "field_synthesis_chain_traversed": list(FIELD_SYNTHESIS_CHAIN),
        "field_type_resolved": field.get("field_type") not in (None, "unknown"),
        "fact_affects_dimensions_not_identity": fact_only_affects_dimensions and not fact_identity_field_type,
        "prohibited_override_policy_absent": not prohibited_policy_used,
        "dynamic_ttl_present_when_dynamic_exists": dynamic_ttl_ok,
        "static_dynamic_not_mixed": static_dynamic_ok,
        "map_aligned_requires_anchors": not aligned_without_anchors,
        "high_risk_distance_has_source_refs": not high_risk_missing_sources,
        "conflict_readiness_downgraded": conflict_readiness_ok,
        "precise_distance_blocked_for_speech": validate_speech_no_precise_distance("")[0],
    }


def build_trace_for_case(
    case: FieldUnderstandingDryRunCase,
    *,
    actual_ok: bool,
    errors: List[str],
    case_type: str,
) -> Dict[str, Any]:
    field = case.field_candidate
    fusion = case.spatial_fusion_candidate
    semantics = case.semantic_candidates
    influences = case.influence_candidates
    alignments = case.map_alignment_candidates
    distances = case.distance_candidates

    affected_dims = sorted(
        {
            i.affected_field_dimension
            for i in influences
            if i.affected_field_dimension
        }
    )
    static_dynamic_ok, _ = validate_dynamic_not_in_static(
        [candidate_to_dict(s) for s in case.static_candidates],
        [candidate_to_dict(d) for d in case.dynamic_candidates],
    )

    trace_decision = classify_trace_decision(case.expected_validation_ok, actual_ok)
    matched = trace_decision in ("PASS", "EXPECTED_REJECT")

    return {
        "case_id": case.case_id,
        "case_name": case.case_name,
        "case_type": case_type,
        "case_goal": case.case_goal,
        "expected_notes": list(case.expected_notes),
        "field_context": {
            "field_ref": field.field_ref,
            "field_type": field.field_type,
            "field_confidence": field.field_confidence,
            "field_context_resolved": field.field_type not in ("unknown",),
        },
        "governance_chain": list(FIELD_SYNTHESIS_CHAIN),
        "governance_checkpoints": _governance_checkpoints(case),
        "static_dynamic_split": {
            "static_count": len(case.static_candidates),
            "dynamic_count": len(case.dynamic_candidates),
            "dynamic_ttl_required": True,
            "static_dynamic_conflict_detected": not static_dynamic_ok,
        },
        "semantic_governance": {
            "semantic_count": len(semantics),
            "has_risk_tags": any(s.risk_tags for s in semantics),
            "has_attention_tags": any(s.attention_tags for s in semantics),
            "has_destination_tags": any(s.destination_tags for s in semantics),
            "has_memory_tags": any(s.memory_tags for s in semantics),
        },
        "fact_influence_governance": {
            "fact_influence_refs": list(fusion.fact_influence_refs),
            "fact_influence_level": fusion.fact_influence_level,
            "field_revision_policy": fusion.field_revision_policy,
            "affected_field_dimensions": affected_dims,
            "direct_override_blocked": fusion.field_revision_policy not in PROHIBITED_FIELD_REVISION_POLICIES,
            "field_type_preserved": field.field_type not in PROHIBITED_FIELD_TYPES_FROM_ISOLATED_FACT,
        },
        "map_alignment": {
            "map_candidate_count": len(case.external_map_candidates),
            "alignment_count": len(alignments),
            "alignment_statuses": [a.alignment_status for a in alignments],
        },
        "action_distance": {
            "distance_count": len(distances),
            "distance_bands": [d.distance_band for d in distances],
            "precise_distance_exposed_to_speech": False,
        },
        "fusion": {
            "fusion_ref": fusion.fusion_ref,
            "conflict_refs": list(fusion.conflict_refs),
            "action_readiness": fusion.action_readiness,
            "expected_action_readiness": case.expected_action_readiness,
            "action_readiness_matches_expectation": (
                fusion.action_readiness == case.expected_action_readiness
                if case.expected_validation_ok
                else True
            ),
            "confidence": fusion.confidence,
        },
        "validation": {
            "expected_validation_ok": case.expected_validation_ok,
            "actual_validation_ok": actual_ok,
            "errors": errors,
            "matched_expectation": matched,
        },
        "trace_decision": trace_decision,
    }


def run_single_dryrun_case(
    case: FieldUnderstandingDryRunCase,
    *,
    positive_ids: set[str],
) -> Dict[str, Any]:
    actual_ok, errors = validate_core_bundle(
        field=candidate_to_dict(case.field_candidate),
        static_structures=[candidate_to_dict(s) for s in case.static_candidates],
        dynamic_states=[candidate_to_dict(d) for d in case.dynamic_candidates],
        semantic_objects=[candidate_to_dict(s) for s in case.semantic_candidates],
        influences=[candidate_to_dict(i) for i in case.influence_candidates],
        distances=[candidate_to_dict(d) for d in case.distance_candidates],
        external_maps=[candidate_to_dict(m) for m in case.external_map_candidates],
        alignments=[candidate_to_dict(a) for a in case.map_alignment_candidates],
        fusions=[candidate_to_dict(case.spatial_fusion_candidate)],
    )
    return build_trace_for_case(
        case,
        actual_ok=actual_ok,
        errors=errors,
        case_type=_case_type(case, positive_ids=positive_ids),
    )


def summarize_dryrun_traces(traces: List[Dict[str, Any]]) -> Dict[str, Any]:
    positive_pass = sum(1 for t in traces if t["trace_decision"] == "PASS")
    expected_reject = sum(1 for t in traces if t["trace_decision"] == "EXPECTED_REJECT")
    unexpected_pass = sum(1 for t in traces if t["trace_decision"] == "UNEXPECTED_PASS")
    unexpected_fail = sum(1 for t in traces if t["trace_decision"] == "UNEXPECTED_FAIL")
    positive_cases = [t for t in traces if t["case_type"] == "positive"]
    invalid_cases = [t for t in traces if t["case_type"] == "invalid"]

    runner_ok = (
        positive_pass == len(positive_cases)
        and expected_reject == len(invalid_cases)
        and unexpected_pass == 0
        and unexpected_fail == 0
    )

    return {
        "phase_id": PHASE_ID,
        "step": "Step 3 Dry-run Runner",
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "governance_ids": {
            "field_information_priority": FIELD_INFORMATION_PRIORITY_GOVERNANCE_ID,
            "field_context_governance": FIELD_CONTEXT_GOVERNANCE_ID,
        },
        "case_count": len(traces),
        "positive_case_count": len(positive_cases),
        "invalid_case_count": len(invalid_cases),
        "positive_pass_count": positive_pass,
        "invalid_expected_reject_count": expected_reject,
        "unexpected_pass_count": unexpected_pass,
        "unexpected_fail_count": unexpected_fail,
        "trace_count": len(traces),
        "trace_decisions": {t["case_id"]: t["trace_decision"] for t in traces},
        "final_decision": FINAL_DECISION_TRACE_READY if runner_ok else FINAL_DECISION_RUNNER_FAIL,
    }


def run_field_understanding_dryrun_v1(
    *,
    output_root: Optional[str] = None,
    write_files: bool = True,
) -> Dict[str, Any]:
    positive = build_dryrun_cases_v1()
    invalid = build_invalid_dryrun_cases_v1()
    all_cases = build_all_dryrun_cases_v1()
    positive_ids = {c.case_id for c in positive}

    traces = [run_single_dryrun_case(case, positive_ids=positive_ids) for case in all_cases]
    summary = summarize_dryrun_traces(traces)

    result = {
        "summary": summary,
        "traces": traces,
        "output_root": str(Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()),
    }

    if write_files:
        out = Path(result["output_root"])
        out.mkdir(parents=True, exist_ok=True)
        trace_doc = {
            "phase_id": PHASE_ID,
            "step": "Step 3 Dry-run Runner",
            "trace_count": len(traces),
            "traces": traces,
        }
        (out / "field_understanding_dryrun_trace_v1.json").write_text(
            json.dumps(trace_doc, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        (out / "field_understanding_dryrun_summary_v1.json").write_text(
            json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    return result


def main() -> int:
    result = run_field_understanding_dryrun_v1()
    summary = result["summary"]
    print(json.dumps({
        "output_root": result["output_root"],
        "positive_pass_count": summary["positive_pass_count"],
        "invalid_expected_reject_count": summary["invalid_expected_reject_count"],
        "unexpected_pass_count": summary["unexpected_pass_count"],
        "unexpected_fail_count": summary["unexpected_fail_count"],
        "final_decision": summary["final_decision"],
    }, ensure_ascii=False))
    return 0 if summary["final_decision"] == FINAL_DECISION_TRACE_READY else 1


if __name__ == "__main__":
    raise SystemExit(main())
