"""Controlled B1 runner for real visual evidence downstream integration.

This runner consumes a previously validated structured YOLO11n evidence
reference.  It deliberately does not invoke a model or provider.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, Tuple


RUNNER_PATH = Path(__file__).resolve()


def _resolve_repo_root() -> Path:
    for candidate in (RUNNER_PATH, *RUNNER_PATH.parents):
        if (
            (candidate / "capabilities").is_dir()
            and (candidate / "docs").is_dir()
            and (candidate / "README.md").is_file()
        ):
            return candidate
    raise RuntimeError("repository root sentinel not found")


REPO_ROOT = _resolve_repo_root()
sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.core.context_foundation.integration.b1_real_visual_evidence_context_world_controlled.b1_real_visual_evidence_context_world_fixture_v1 import (  # noqa: E402
    build_b1_cases_v1,
    build_gateway_handoff_v1,
    build_visual_evidence_reference_v1,
)
from capabilities.midplatform.core.context_foundation.integration.context_world_state_controlled_integration_engine_v1 import (  # noqa: E402
    ContextWorldStateControlledIntegrationEngineV1,
)
from capabilities.midplatform.core.context_foundation.integration.run_context_world_state_controlled_integration_v1 import (  # noqa: E402
    build_runner_result as build_synthetic_regression_result,
)
from capabilities.midplatform.core.observation_gateway.integration.real_visual_evidence_gateway_adapter_v1 import (  # noqa: E402
    REAL_CONTROLLED_EVIDENCE,
    SYNTHETIC_EVIDENCE,
    admit_real_visual_evidence_v1,
)


OUTPUT_DIR = REPO_ROOT / "_eval_out/brain_b1_real_visual_evidence_context_current_world_controlled_implementation_v1"


def _json_value(value: Any) -> Any:
    if isinstance(value, tuple):
        return [_json_value(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _json_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_value(item) for item in value]
    return value


def _context_payload(
    gateway: Any,
    case_id: str,
    *,
    field_relevant: bool = False,
    field_event_admission: bool = False,
    contradiction_refs: Iterable[str] = (),
    occurred_at: str = "",
    received_at: str = "",
) -> Dict[str, Any]:
    evidence_refs = tuple(item.evidence_id for item in gateway.evidence)
    temporal_refs = tuple(item.source_temporal_ref for item in gateway.evidence)
    uncertainty_refs = tuple(
        ref for item in gateway.source_visual_evidence for ref in item.uncertainty_refs
    )
    contradictions = tuple(
        dict.fromkeys(
            (
                *(ref for item in gateway.source_visual_evidence for ref in item.contradiction_refs),
                *tuple(contradiction_refs),
            )
        )
    )
    source_refs = tuple(
        dict.fromkeys(
            (
                *gateway.trace.source_input_refs,
                gateway.trace.root_trace_id,
                gateway.trace.observation_trace_ref,
                *gateway.trace.evidence_trace_refs,
            )
        )
    )
    source_temporal_ref = (
        gateway.source_visual_evidence[0].temporal_ref
        if gateway.source_visual_evidence
        else ""
    )
    observed_at_ref = gateway.ingress.observed_at if gateway.ingress else source_temporal_ref
    valid_from_ref = (
        gateway.ingress.valid_from_candidate
        if gateway.ingress
        else source_temporal_ref
    )
    return {
        "case_id": case_id,
        "observation_ref": gateway.observation.observation_id,
        "evidence_refs": evidence_refs,
        "observation_admitted": gateway.gateway_admission,
        "root_trace_id": gateway.trace.root_trace_id,
        "source_refs": source_refs,
        "uncertainty_refs": uncertainty_refs,
        "contradiction_refs": contradictions,
        # Read semantic source fields, not positional trace slots.  The
        # Gateway trace retains the canonical three-slot lineage for audit,
        # but B1 must not require a particular tuple cardinality to construct
        # its Context payload.
        "observed_at": observed_at_ref,
        "valid_from": valid_from_ref,
        "occurred_at": occurred_at,
        "received_at": received_at,
        "temporal_status": "ACTIVE",
        "field_relevant": field_relevant,
        "field_event_admission": field_event_admission,
        "field_ref": f"field:b1:{case_id}" if field_relevant else "",
    }


def _check(field: str, expected: Any, actual: Any) -> Dict[str, Any]:
    return {
        "field": field,
        "expected": _json_value(expected),
        "actual": _json_value(actual),
        "passed": actual == expected,
    }


def _run_real_case(case: Mapping[str, Any]) -> Dict[str, Any]:
    case_id = str(case["case_id"])
    evidence = build_visual_evidence_reference_v1(
        case_id,
        contradiction=bool(case.get("contradiction")),
    )
    handoff = build_gateway_handoff_v1(evidence)
    gateway = admit_real_visual_evidence_v1(
        handoff,
        (evidence,),
        mode=REAL_CONTROLLED_EVIDENCE,
        observed_at_ref=str(case.get("observed_at") or "") or None,
        valid_from_ref=str(case.get("valid_from") or "") or None,
    )
    duplicate_gateway = None
    if case.get("duplicate"):
        duplicate_gateway = admit_real_visual_evidence_v1(
            handoff,
            (evidence,),
            mode=REAL_CONTROLLED_EVIDENCE,
            seen_handoff_ids=(handoff.handoff_id,),
        )
    context_result = None
    if gateway.gateway_admission and gateway.observation is not None:
        engine = ContextWorldStateControlledIntegrationEngineV1()
        context_result = engine.run_case(
            _context_payload(
                gateway,
                case_id,
                field_relevant=bool(case.get("field_relevant")),
                field_event_admission=bool(case.get("field_event_admission")),
                contradiction_refs=case.get("contradiction_refs", ()),
                occurred_at=str(case.get("occurred_at") or ""),
                received_at=str(case.get("received_at") or ""),
            )
        )
    return {
        "case": dict(case),
        "evidence": evidence,
        "handoff": handoff,
        "gateway": gateway,
        "duplicate_gateway": duplicate_gateway,
        "context_result": context_result,
    }


def _checks_for_case(case_id: str, run: Mapping[str, Any]) -> list[Dict[str, Any]]:
    gateway = run["gateway"]
    evidence = run["evidence"]
    context_result = run["context_result"]
    checks: list[Dict[str, Any]] = []
    behavior = context_result.behavior if context_result is not None else {}
    current_world = context_result.current_world if context_result is not None else None
    context = context_result.context if context_result is not None else None

    if case_id == "B1-01":
        checks.append(_check("gateway_real_evidence_accepted", True, gateway.gateway_admission))
    elif case_id == "B1-02":
        checks.extend(
            [
                _check("gateway_admission", True, gateway.gateway_admission),
                _check("truth_declared", False, gateway.truth_declared),
                _check("fact_admitted", False, gateway.fact_admitted),
                _check("semantic_authority", False, gateway.semantic_authority),
            ]
        )
    elif case_id == "B1-03":
        source = gateway.source_visual_evidence[0]
        checks.extend(
            [
                _check("detection_ref_preserved", evidence.detection_ref, source.detection_ref),
                _check("class_candidate_preserved", evidence.class_candidate, source.class_candidate),
                _check("bbox_preserved", evidence.bbox, source.bbox),
                _check("confidence_preserved", evidence.confidence, source.confidence),
                _check("frame_ref_preserved", evidence.frame_ref, source.frame_ref),
            ]
        )
    elif case_id == "B1-04":
        checks.append(_check("context_handoff_created", True, behavior.get("observation_context_handoff_present")))
    elif case_id == "B1-05":
        checks.append(_check("context_candidate_created", True, behavior.get("context_candidate_present")))
    elif case_id == "B1-06":
        checks.append(_check("current_world_candidate_created", True, behavior.get("current_world_candidate_present")))
    elif case_id == "B1-07":
        checks.extend(
            [
                _check("current_world_candidate_only", True, bool(current_world and current_world.candidate_only)),
                _check("current_world_truth_declaration", False, bool(current_world and current_world.field_truth_declaration)),
                _check("current_world_field_mutation", False, bool(current_world and current_world.field_mutation)),
            ]
        )
    elif case_id == "B1-08":
        path = tuple(context_result.trace.reverse_lookup_path) if context_result else ()
        checks.extend(
            [
                _check("provenance_reverse_lookup_complete", True, behavior.get("provenance_reverse_lookup_complete")),
                _check("reverse_path_reaches_evidence", True, any(evidence.evidence_id in item for item in path)),
                _check("reverse_path_reaches_frame", True, evidence.frame_ref in path),
            ]
        )
    elif case_id == "B1-09":
        checks.extend(
            [
                _check("gateway_temporal_ref", True, bool(gateway.trace.temporal_lineage)),
                _check("context_temporal_refs", True, bool(context and context.temporal_refs)),
                _check("temporal_lineage_preserved", True, behavior.get("temporal_lineage_preserved")),
            ]
        )
    elif case_id == "B1-10":
        checks.extend(
            [
                _check("source_uncertainty_refs", True, bool(evidence.uncertainty_refs)),
                _check("context_uncertainty_refs", True, bool(context and context.uncertainty_refs)),
            ]
        )
    elif case_id == "B1-11":
        checks.extend(
            [
                _check("source_contradiction_refs", True, bool(evidence.contradiction_refs)),
                _check("context_contradiction_refs", True, bool(context and context.contradiction_refs)),
                _check("context_contested", "CONTESTED", context.context_status if context else ""),
            ]
        )
    elif case_id == "B1-12":
        checks.extend(
            [
                _check("field_event_candidate_created", False, behavior.get("field_event_candidate_present")),
                _check("field_state_mutation", False, behavior.get("field_state_mutation")),
            ]
        )
    elif case_id == "B1-13":
        checks.extend(
            [
                _check("field_event_candidate_created", True, behavior.get("field_event_candidate_present")),
                _check("field_event_admitted", True, behavior.get("field_event_admitted")),
                _check("reducer_eligible", True, behavior.get("reducer_eligible")),
            ]
        )
    elif case_id == "B1-14":
        checks.extend(
            [
                _check("reducer_eligible", True, behavior.get("reducer_eligible")),
                _check("reducer_invoked", False, behavior.get("reducer_invoked")),
                _check("reducer_is_single_mutation_authority", True, behavior.get("reducer_is_single_mutation_authority")),
            ]
        )
    elif case_id == "B1-15":
        checks.extend(
            [
                _check("field_state_mutation", False, behavior.get("field_state_mutation")),
                _check("observation_can_mutate_field", False, behavior.get("observation_can_mutate_field")),
            ]
        )
    elif case_id == "B1-16":
        checks.extend(
            [
                _check("current_world_field_mutation", False, behavior.get("current_world_field_mutation")),
                _check("current_world_is_field_truth", False, behavior.get("current_world_is_field_truth")),
            ]
        )
    elif case_id == "B1-17":
        checks.extend(
            [
                _check("intent_reference_read_only", False, behavior.get("intent_reference_read_only")),
                _check("task_context_present", False, behavior.get("task_context_present")),
                _check("mutation_authority", False, behavior.get("mutation_authority")),
            ]
        )
    elif case_id == "B1-18":
        checks.extend(
            [
                _check("natural_language_conclusion_ref", "", evidence.natural_language_conclusion_ref),
                _check("semantic_compression_execution", False, behavior.get("semantic_compression_execution")),
            ]
        )
    elif case_id == "B1-19":
        checks.extend(
            [
                _check("ocr_execution", False, behavior.get("ocr_evidence_is_world_fact")),
                _check("slam_execution", False, behavior.get("slam_geometry_is_semantic_truth")),
                _check("vlm_execution", False, behavior.get("model_call")),
            ]
        )
    elif case_id == "B1-20":
        duplicate = run["duplicate_gateway"]
        checks.extend(
            [
                _check("first_admission", True, gateway.gateway_admission),
                _check("duplicate_rejected", True, bool(duplicate and not duplicate.gateway_admission)),
                _check("duplicate_error", True, bool(duplicate and "DUPLICATE_REAL_EVIDENCE" in duplicate.errors)),
            ]
        )
    elif case_id == "B1-21":
        synthetic = run["synthetic_regression"]
        checks.append(_check("synthetic_regression_preserved", True, synthetic["summary"]["all_cases_passed"]))
    elif case_id == "B1-22":
        differential = run["differential"]
        real_gateway = differential["real_gateway"]
        synthetic_gateway = differential["synthetic_gateway"]
        real_result = differential["real"]
        synthetic_result = differential["synthetic"]
        real_context = real_result.context
        synthetic_context = synthetic_result.context
        real_world = real_result.current_world
        synthetic_world = synthetic_result.current_world
        checks.extend(
            [
                _check("gateway_governance_compatible", True, real_gateway.gateway_admission == synthetic_gateway.gateway_admission),
                _check("context_governance_compatible", True, bool(real_context and synthetic_context)),
                _check("world_candidate_governance_compatible", True, bool(real_world and synthetic_world)),
                _check("mutation_guard_compatible", True, real_result.behavior["field_state_mutation"] is False and synthetic_result.behavior["field_state_mutation"] is False),
                _check("gateway_provenance_compatible", True, bool(real_gateway.trace.provenance_refs) == bool(synthetic_gateway.trace.provenance_refs)),
                _check("context_provenance_compatible", True, bool(real_result.trace.provenance_refs) == bool(synthetic_result.trace.provenance_refs)),
                _check("gateway_temporal_compatible", True, bool(real_gateway.trace.temporal_lineage) == bool(synthetic_gateway.trace.temporal_lineage)),
                _check("context_temporal_compatible", True, bool(real_context and real_context.temporal_refs) == bool(synthetic_context and synthetic_context.temporal_refs)),
                _check("uncertainty_compatible", True, bool(real_context and real_context.uncertainty_refs) == bool(synthetic_context and synthetic_context.uncertainty_refs)),
                _check("contradiction_compatible", True, bool(real_context and real_context.contradiction_refs) == bool(synthetic_context and synthetic_context.contradiction_refs)),
                _check("gateway_candidate_only_compatible", True, real_gateway.candidate_only is True and synthetic_gateway.candidate_only is True),
                _check("gateway_truth_false_compatible", True, real_gateway.truth_declared is False and synthetic_gateway.truth_declared is False),
                _check("context_candidate_only_compatible", True, bool(real_context and synthetic_context and real_context.candidate_only is True and synthetic_context.candidate_only is True)),
                _check("context_truth_false_compatible", True, bool(real_context and synthetic_context and real_context.truth_declared is False and synthetic_context.truth_declared is False)),
                _check("world_candidate_only_compatible", True, bool(real_world and synthetic_world and real_world.candidate_only is True and synthetic_world.candidate_only is True)),
                _check("world_truth_false_compatible", True, bool(real_world and synthetic_world and real_world.field_truth_declaration is False and synthetic_world.field_truth_declaration is False)),
            ]
        )
    elif case_id == "B1-23":
        checks.extend(
            [
                _check("gateway_admission", True, gateway.gateway_admission),
                _check("context_candidate", True, bool(context_result and context_result.context)),
                _check("current_world_candidate", True, bool(current_world)),
                _check("provenance_chain_complete", True, bool(context_result and context_result.trace.reverse_lookup_path)),
                _check("field_state_mutation", False, behavior.get("field_state_mutation")),
            ]
        )
    return checks


def build_runner_result() -> Dict[str, Any]:
    synthetic_regression = build_synthetic_regression_result()
    case_results = []
    traces = []
    retained_real_run = None
    for case in build_b1_cases_v1():
        run = _run_real_case(case)
        run["synthetic_regression"] = synthetic_regression
        if case["case_id"] == "B1-22":
            synthetic_evidence = build_visual_evidence_reference_v1("B1-22-SYN", synthetic=True)
            synthetic_handoff = build_gateway_handoff_v1(synthetic_evidence, synthetic=True)
            synthetic_gateway = admit_real_visual_evidence_v1(
                synthetic_handoff,
                (synthetic_evidence,),
                mode=SYNTHETIC_EVIDENCE,
            )
            synthetic_result = ContextWorldStateControlledIntegrationEngineV1().run_case(
                _context_payload(synthetic_gateway, "B1-22-SYN")
            )
            run["differential"] = {
                "real": run["context_result"],
                "synthetic": synthetic_result,
                "real_gateway": run["gateway"],
                "synthetic_gateway": synthetic_gateway,
            }
        checks = _checks_for_case(str(case["case_id"]), run)
        actual = {
            "gateway_admission": run["gateway"].gateway_admission,
            "gateway_errors": run["gateway"].errors,
            "context_candidate_created": bool(run["context_result"] and run["context_result"].context),
            "current_world_candidate_created": bool(run["context_result"] and run["context_result"].current_world),
            "field_event_candidate_created": bool(run["context_result"] and run["context_result"].field_event_handoff),
            "field_state_mutation_executed": bool(run["context_result"] and run["context_result"].behavior.get("field_state_mutation")),
            "source_evidence": asdict(run["evidence"]),
        }
        case_results.append(
            {
                "case_id": case["case_id"],
                "title": case["title"],
                "checks": checks,
                "all_checks_passed": all(item["passed"] for item in checks),
                "actual": _json_value(actual),
                "result": _json_value(asdict(run["context_result"])) if run["context_result"] else None,
            }
        )
        if case["case_id"] == "B1-23":
            retained_real_run = run
        if run["context_result"] is not None:
            traces.append(_json_value(asdict(run["context_result"].trace)))
        else:
            traces.append(_json_value(asdict(run["gateway"].trace)))

    failed_ids = [item["case_id"] for item in case_results if not item["all_checks_passed"]]
    final_run = retained_real_run
    gateway = final_run["gateway"]
    context_result = final_run["context_result"]
    behavior = context_result.behavior
    summary = {
        "phase": "Phase-Luna-Brain-B1-Real-Visual-Evidence-Context-Current-World-Controlled-Implementation-v1-001",
        "mode": "HYBRID_B1_REAL_VISUAL_EVIDENCE",
        "owner": "Observation Gateway / Context Foundation / Cognitive State Formation",
        "real_components": ["VISION_YOLO11N_EVIDENCE_REFERENCE"],
        "synthetic_components": ["Context Foundation", "Field Event Admission", "Field State Reducer", "Current World candidate formation"],
        "b1_scenario_count": len(case_results),
        "all_cases_passed": not failed_ids,
        "failed_case_ids": failed_ids,
        "gateway_real_evidence_accepted": gateway.gateway_admission,
        "gateway_admission": gateway.gateway_admission,
        "context_handoff_created": bool(context_result.observation_context_handoff),
        "context_candidate_created": bool(context_result.context),
        "field_event_candidate_created": bool(context_result.field_event_handoff),
        "field_event_admitted": bool(behavior.get("field_event_admitted")),
        "reducer_eligible": bool(behavior.get("reducer_eligible")),
        "field_state_mutation_executed": False,
        "current_world_candidate_created": bool(context_result.current_world),
        "current_world_truth_declared": False,
        "real_evidence_ref": gateway.evidence[0].evidence_id,
        "context_ref": context_result.context.context_ref,
        "current_world_ref": context_result.current_world.current_world_id,
        "provenance_chain_complete": bool(context_result.trace.reverse_lookup_path),
        "temporal_refs_preserved": bool(context_result.context.temporal_refs),
        "uncertainty_refs_preserved": bool(context_result.context.uncertainty_refs),
        "contradiction_refs_preserved": bool(context_result.context.contradiction_refs),
        "provider_semantic_authority": False,
        "automatic_fact_admission": False,
        "semantic_compression": False,
        "intent_mutation": False,
        "decision_mutation": False,
        "task_mutation": False,
        "field_mutation": False,
        "current_world_direct_mutation": False,
        "provider_invocation": False,
        "model_call": False,
        "ocr_execution": False,
        "slam_execution": False,
        "vlm_execution": False,
        "runtime_execution": False,
        "synthetic_regression_preserved": synthetic_regression["summary"]["all_cases_passed"],
        "differential_validation_passed": all(
            item["all_checks_passed"] for item in case_results if item["case_id"] == "B1-22"
        ),
        "candidate_only": True,
        "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
    }
    return {"summary": summary, "case_results": case_results, "traces": traces}


def write_runner_artifacts(payload: Mapping[str, Any]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "b1_real_visual_evidence_context_world_result_v1.json").write_text(
        json.dumps(payload["summary"], indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (OUTPUT_DIR / "b1_real_visual_evidence_context_world_case_results_v1.json").write_text(
        json.dumps(payload["case_results"], indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (OUTPUT_DIR / "b1_real_visual_evidence_context_world_trace_v1.json").write_text(
        json.dumps({"case_traces": payload["traces"]}, indent=2, ensure_ascii=False), encoding="utf-8"
    )


if __name__ == "__main__":
    result = build_runner_result()
    write_runner_artifacts(result)
    print(json.dumps(result["summary"], indent=2, ensure_ascii=False))
