from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Mapping

from .runner_v1 import REPO_PROVIDER_REGISTRY
from .types_v1 import PROVIDER_REF
from .rf_detr_declaration_validator_v1 import inspect_rf_detr_declarations_v1


PACKAGE_ROOT = Path(__file__).resolve().parent
MANIFEST = PACKAGE_ROOT / "scenario_manifest_v1.json"
RUNNER_SOURCE = PACKAGE_ROOT / "runner_v1.py"
CLIENT_SOURCE = PACKAGE_ROOT / "provider_client_v1.py"
TRANSLATOR_SOURCE = PACKAGE_ROOT / "evidence_translator_v1.py"


def _real_cognitive_handoff_is_valid(case: Mapping[str, Any]) -> bool:
    """Validate the real one-cycle handoff without making A a Decision owner."""

    decision_present = bool(case.get("decision_candidate_present"))
    next_observation_present = bool(case.get("next_observation_candidate_present"))
    sufficiency_status = case.get("sufficiency_status")

    if sufficiency_status == "INSUFFICIENT":
        return (
            next_observation_present
            and not decision_present
            and case.get("next_target") == "Observation"
        )

    if sufficiency_status == "SUFFICIENT":
        if next_observation_present:
            return False
        if decision_present:
            return case.get("decision_candidate_owner") == "Decision Governance"
        return case.get("next_target") == "Decision Governance"

    return False


def _provider_declaration() -> Mapping[str, Any] | None:
    if not REPO_PROVIDER_REGISTRY.is_file():
        return None
    try:
        registry = json.loads(REPO_PROVIDER_REGISTRY.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return next((item for item in registry.get("providers") or () if item.get("provider_id") == PROVIDER_REF), None)


def _source_wiring_checks() -> Dict[str, bool]:
    runner = RUNNER_SOURCE.read_text(encoding="utf-8") if RUNNER_SOURCE.is_file() else ""
    client = CLIENT_SOURCE.read_text(encoding="utf-8") if CLIENT_SOURCE.is_file() else ""
    translator = TRANSLATOR_SOURCE.read_text(encoding="utf-8") if TRANSLATOR_SOURCE.is_file() else ""
    return {
        "real_mode_explicit": "if not request.real_mode" in client and "run_real" in runner,
        "real_mode_uses_provider_client": "invoke_roboflow_provider_v1" in runner and "real_mode=True" in runner,
        "real_mode_does_not_use_native_fixture": "native_payload=None if real_mode else" in runner,
        "api_key_is_environment_supplied": "ROBOFLOW_API_KEY" in client,
        "official_sdk_transport_present": "InferenceHTTPClient" in client and "run_workflow" in client,
        "official_sdk_header_configuration_present": (
            "InferenceConfiguration" in client
            and 'api_key_transport="header"' in client
        ),
        "serverless_workflow_identity_guard_present": (
            "ROBOFLOW_SERVERLESS_API_URL" in client
            and "REAL_PROVIDER_CONFIGURATION_MISMATCH" in client
            and "_declared_workflow_identity" in client
        ),
        "no_fabricated_urllib_transport": "urlopen" not in client and "Transport" not in client,
        "workflow_output_mapping_is_explicit": "workflow_output_mapping" in client and "_sequence_at" in translator,
        "raw_payload_stops_in_translator": "RoboflowNativeResultV1" in translator and "payload = native.payload" in translator,
        "normalized_evidence_types_used": "VisualDetectionEvidenceCandidateV1" in translator and "OCRRawEvidenceV1" in translator,
        "cognitive_adapter_is_downstream": "build_roboflow_cognitive_loop_candidates_v1" in runner,
        "real_does_not_require_user_semantic_assessment": "semantic_assessment = None if real_mode" in runner,
    }


def verify(summary_path: Path) -> Dict[str, Any]:
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    declaration = _provider_declaration()
    declaration_ok = bool(
        declaration
        and declaration.get("owner") == "Provider Governance"
        and declaration.get("provider_family") == "roboflow"
        and declaration.get("execution_mode") == "external_api"
        and declaration.get("provider_contract_version")
        and declaration.get("workflow_ref") == "workflow:roboflow:lei-luan:custom-workflow:v1"
        and set((declaration.get("supported_capabilities") or ())) >= {"object_detection"}
        and declaration.get("provider_adapter_ref") == "adapter:roboflow:vision-evidence:v1"
        and declaration.get("capability_owner") is False
        and declaration.get("model_owner") is False
    )
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.is_file() else {}
    wiring = _source_wiring_checks()
    rf_detr_declarations = inspect_rf_detr_declarations_v1(Path("."))
    cases = tuple(summary.get("cases") or ())
    cycle_1 = next((case for case in cases if case.get("case_id") == "observation_1_insufficient"), {})
    cycle_2 = next((case for case in cases if case.get("case_id") == "observation_2_sufficiency_candidate"), {})
    structural_checks = {
        "runner_all_cases_passed": summary.get("all_cases_passed") is True,
        "provider_declaration_ok": declaration_ok,
        "rf_detr_declarations_ok": rf_detr_declarations.get("all_checks_passed") is True,
        "manifest_does_not_encode_answer": manifest.get("answer_is_not_encoded") is True,
        "provider_result_is_not_decision": all(not bool(case.get("decision_candidate_direct_from_provider", False)) for case in cases),
        "raw_schema_isolated": bool(summary.get("raw_roboflow_payload_not_canonical")),
        "candidate_only": all(bool(case.get("candidate_only")) for case in cases),
        "no_world_truth": not bool(summary.get("world_truth_declared")),
        "no_field_mutation": not bool(summary.get("source_mutation")),
        "no_task_action_execution": not bool(summary.get("task_execution")) and not bool(summary.get("action_execution")),
        "trace_present": all(bool(case.get("trace_refs")) for case in cases),
        "provenance_present": all(bool(case.get("provenance_refs")) for case in cases),
        "source_versions_present": all(bool(case.get("source_version_refs")) for case in cases),
        "caller_wiring_ok": all(wiring.values()),
    }
    mode_scoped_checks = {
        "rf_detr_normalization_cases_passed": {
            "applicable_mode": "structural",
            "applicable": summary.get("mode") == "structural",
            "passed": (
                summary.get("rf_detr_normalization_cases_passed") is True
                if summary.get("mode") == "structural"
                else None
            ),
        },
        "rf_detr_observation_gateway_handoff_ok": {
            "applicable_mode": "structural",
            "applicable": summary.get("mode") == "structural",
            "passed": (
                (
                    summary.get("rf_detr_observation_gateway_handoff_cases_passed") is True
                    and bool(summary.get("rf_detr_normalization_cases"))
                )
                if summary.get("mode") == "structural"
                else None
            ),
        },
        "runner_negative_cases_passed": {
            "applicable_mode": "structural",
            "applicable": summary.get("mode") == "structural",
            "passed": (
                summary.get("all_negative_cases_passed") is True
                if summary.get("mode") == "structural"
                else None
            ),
        },
    }
    if summary.get("mode") == "structural":
        structural_checks.update(
            {
                "runner_negative_cases_passed": summary.get("all_negative_cases_passed") is True,
                "rf_detr_normalization_cases_passed": summary.get("rf_detr_normalization_cases_passed") is True,
                "rf_detr_observation_gateway_handoff_ok": (
                    summary.get("rf_detr_observation_gateway_handoff_cases_passed") is True
                    and bool(summary.get("rf_detr_normalization_cases"))
                ),
                "negative_cases_passed": summary.get("all_negative_cases_passed") is True,
            }
        )
        cycle_2_decision_boundary_ok = (
            bool(cycle_2.get("decision_candidate_present"))
            and cycle_2.get("decision_candidate_owner") == "Decision Governance"
        ) or (
            not bool(cycle_2.get("decision_candidate_present"))
            and cycle_2.get("next_target") == "Decision Governance"
        )
        structural_checks.update(
            {
                "cycle_1_cognitive_boundary_ok": (
                    bool(cycle_1.get("current_world_candidate_present"))
                    and bool(cycle_1.get("hypothesis_candidate_present"))
                    and bool(cycle_1.get("sufficiency_candidate_present"))
                    and cycle_1.get("sufficiency_status") == "INSUFFICIENT"
                    and bool(cycle_1.get("next_observation_candidate_present"))
                    and not bool(cycle_1.get("decision_candidate_present"))
                ),
                "cycle_2_cognitive_boundary_ok": (
                    int(cycle_2.get("detection_evidence_count", 0)) + int(cycle_2.get("ocr_evidence_count", 0)) > 0
                    and bool(cycle_2.get("current_world_candidate_present"))
                    and bool(cycle_2.get("hypothesis_candidate_present"))
                    and cycle_2.get("hypothesis_id") != cycle_1.get("hypothesis_id")
                    and cycle_2.get("hypothesis_revision_parent_ref") == cycle_1.get("hypothesis_id")
                    and bool(cycle_2.get("sufficiency_candidate_present"))
                    and cycle_2.get("sufficiency_status") == "SUFFICIENT"
                    and cycle_1.get("sufficiency_status") != cycle_2.get("sufficiency_status")
                    and cycle_2_decision_boundary_ok
                ),
            }
        )
    if summary.get("mode") == "real":
        real_checks = {
            "provider_invocation_observed": summary.get("provider_invocation") is True,
            "actual_provider_response_received": summary.get("actual_provider_response") is True,
            "response_shape_diagnostics_present": all(
                bool((case.get("response_shape_diagnostics") or {}).get("top_level_type"))
                and bool((case.get("response_shape_diagnostics") or {}).get("governed_output_path"))
                for case in cases
            ) and bool(cases),
            "per_output_shape_diagnostics_present": all(
                set((case.get("response_shape_diagnostics") or {}).get("first_item_keys") or ())
                <= set(
                    ((case.get("response_shape_diagnostics") or {}).get("first_item_output_diagnostics") or {}).keys()
                )
                for case in cases
            ) and bool(cases),
            "provider_result_mapped_to_evidence_or_legal_empty": all(
                bool(case.get("provider_result_accepted"))
                and (
                    int(case.get("detection_evidence_count", 0))
                    + int(case.get("ocr_evidence_count", 0))
                    > 0
                    or bool(case.get("legal_empty_predictions"))
                )
                for case in cases
            ) and bool(cases),
            "observation_gateway_handoff_boundary": all(
                (
                    bool(case.get("observation_gateway_handoff_present"))
                    and bool(case.get("observation_gateway_handoff_candidate_only"))
                    and not bool(case.get("observation_gateway_handoff_admission"))
                )
                or bool(case.get("legal_empty_predictions"))
                for case in cases
            ) and bool(cases),
            "hypothesis_is_cognitive_side_output": any(bool(case.get("hypothesis_candidate_present")) for case in cases),
            "sufficiency_is_cognitive_side_output": any(bool(case.get("sufficiency_candidate_present")) for case in cases),
            "hypothesis_sufficiency_owner_is_a": all(
                case.get("cognitive_source_owner") == "A"
                for case in cases
                if case.get("hypothesis_candidate_present") or case.get("sufficiency_candidate_present")
            ),
            "decision_or_next_observation_is_cognitive_side_output": all(
                _real_cognitive_handoff_is_valid(case) for case in cases
            ) and bool(cases),
            "semantic_assessment_not_supplied_by_user": all(
                case.get("semantic_assessment_supplied") is False for case in cases
            ),
            "goal_concern_refs_preserved": all(
                bool(case.get("goal_ref")) and bool(case.get("concern_ref"))
                for case in cases
            ),
            "provider_identity_preserved": all(
                bool(case.get("provider_ref"))
                and case.get("provider_ref") == case.get("evidence_provider_ref")
                for case in cases
            ),
            "workflow_identity_preserved": all(
                bool(case.get("workflow_ref"))
                and case.get("workflow_ref") == case.get("evidence_workflow_ref")
                for case in cases
            ),
            "model_identity_preserved": all(
                tuple(case.get("model_refs") or ()) == tuple(case.get("evidence_model_refs") or ())
                and bool(case.get("model_refs"))
                for case in cases
            ),
            "workflow_output_mapping_present": all(
                bool((case.get("workflow_output_mapping") or {}).get("detections"))
                and (
                    "text_recognition" not in tuple(case.get("requested_capabilities") or ())
                    or bool((case.get("workflow_output_mapping") or {}).get("ocr"))
                )
                for case in cases
            ),
            "next_observation_refs_preserved": all(
                not bool(case.get("next_observation_candidate_present"))
                or (
                    bool(case.get("information_gap"))
                    and bool(case.get("next_observation_request_ref"))
                    and bool(case.get("next_observation_demand_ref"))
                    and bool(case.get("requested_capabilities"))
                    and bool(case.get("roi_ref"))
                )
                for case in cases
            ),
            "real_provider_not_faked": wiring["real_mode_does_not_use_native_fixture"],
            "official_sdk_header_configuration": wiring["official_sdk_header_configuration_present"],
            "serverless_workflow_identity_guard": wiring["serverless_workflow_identity_guard_present"],
            "no_provider_autonomous_reobservation": all(
                not bool(case.get("provider_autonomous_reobservation")) for case in cases
            ) and bool(cases),
        }
    else:
        real_checks = {
            "real_provider_not_run_in_structural_mode": summary.get("actual_provider_response") is False and not bool(summary.get("provider_invocation")),
            "structural_mode_explicit": summary.get("mode") == "structural",
        }
    checks = {**structural_checks, **real_checks}
    result = {
        "phase": "Phase-P1-Luna-Roboflow-Integrated-Vision-Provider-Cognitive-Loop-PoC-Controlled-Implementation-v1-001",
        "mode": summary.get("mode"),
        "checks": checks,
        "mode_scoped_checks": mode_scoped_checks,
        "source_wiring": wiring,
        "rf_detr_declarations": rf_detr_declarations,
        "all_checks_passed": all(checks.values()),
        "runtime_execution": False,
        "provider_invocation_observed_by_verifier": summary.get("provider_invocation") is True,
        "observation_execution": False,
        "task_execution": False,
        "action_execution": False,
        "source_mutation": False,
        "world_truth_declared": False,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Controlled Roboflow Luna cognitive-loop PoC verifier")
    parser.add_argument("summary", type=Path)
    args = parser.parse_args()
    result = verify(args.summary)
    if not result["all_checks_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
