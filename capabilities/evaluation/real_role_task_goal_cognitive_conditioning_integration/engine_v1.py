"""Compose real OCR output with existing Role/Task/Goal-conditioned CState."""

from __future__ import annotations

import dataclasses
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Tuple

from capabilities.evaluation.level1_cognitive_evaluation_run.governance_v1 import (
    evaluate_plane_g_compliance_v1,
    validate_plane_g_compliance_v1,
)
from capabilities.midplatform.core.provider_runtime_to_observation_ingress.real_ocr_provider_execution_engine_v1 import (
    RealOCRProviderExecutionEngineV1,
)
from capabilities.midplatform.core.provider_runtime_to_observation_ingress.types_v1 import (
    ProviderObservationIngressCaseV1,
)

from .types_v1 import ConditioningContrastSpecV1, ConditioningSideSpecV1


PHASE = "Phase-P1-Luna-Real-Role-Task-Goal-Cognitive-Conditioning-Integration-v1-001"
EXECUTION_MODE = "LIVE_RUNTIME"


def _jsonable(value: Any) -> Any:
    if dataclasses.is_dataclass(value):
        return {key: _jsonable(item) for key, item in dataclasses.asdict(value).items()}
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_jsonable(item) for item in value]
    return value


def _native_projection(native: Dict[str, Any]) -> Dict[str, Any]:
    """Remove per-execution identity/timing while retaining native OCR content."""

    candidates = []
    for item in native.get("raw_text_candidates") or ():
        if not isinstance(item, dict):
            continue
        candidates.append({
            key: item.get(key)
            for key in (
                "text", "normalized_text", "bbox", "confidence", "line_order",
                "allows_execute_now", "bbox_status", "confidence_status",
            )
        })
    return {
        "provider_id": native.get("provider_id"),
        "model_config_id": native.get("model_config_id"),
        "ocr_runtime_mode": native.get("ocr_runtime_mode"),
        "semantic_interpretation_enabled": native.get("semantic_interpretation_enabled"),
        "raw_text_candidates": candidates,
        "raw_text_joined": native.get("raw_text_joined"),
        "raw_text_joined_strategy": native.get("raw_text_joined_strategy"),
        "allows_execute_now": native.get("allows_execute_now"),
        "runtime_status": native.get("runtime_status"),
        "error_category": native.get("error_category"),
        "empty_result": native.get("empty_result"),
    }


def _fingerprint(projection: Dict[str, Any]) -> str:
    payload = json.dumps(projection, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _semantic_snapshot(proof: Any) -> Dict[str, Any]:
    return {
        "attention_priority_candidate": getattr(proof, "conditioned_attention_priority_candidate", None),
        "attention_relevance_candidate": getattr(proof, "conditioned_attention_relevance_candidate", None),
        "selected_attention_count": getattr(proof, "selected_attention_count", 0),
        "hypothesis_statement_candidate": getattr(proof, "conditioned_hypothesis_statement", None),
        "hypothesis_state": getattr(proof, "conditioned_hypothesis_state", None),
        "current_world_kind_candidate": getattr(proof, "conditioned_world_kind_candidate", None),
        "sufficiency_status": getattr(proof, "sufficiency_status", None),
        "missing_information_refs": list(getattr(proof, "conditioned_missing_information_refs", ()) or ()),
        "stop_present": bool(getattr(proof, "stop_ref", None)),
        "gap_present": bool(getattr(proof, "information_gap_ref", None)),
        "reobservation_present": bool(getattr(proof, "reobservation_ref", None)),
        "relation_interpretation_candidates": list(getattr(proof, "relation_interpretation_candidates", ()) or ()),
        "candidate_only": bool(getattr(proof, "candidate_only", True)),
        "world_truth_declared": bool(getattr(proof, "world_truth_declared", False)),
    }


class RealRoleTaskGoalConditioningEngineV1:
    """Run bounded real OCR sides and compare only cognition-level projections."""

    def __init__(self, *, repository_root: Path) -> None:
        self.repository_root = repository_root
        self.ocr_engine = RealOCRProviderExecutionEngineV1()

    @staticmethod
    def _provider_case(
        contrast: ConditioningContrastSpecV1,
        side: ConditioningSideSpecV1,
        *,
        source_ref: str,
    ) -> ProviderObservationIngressCaseV1:
        execution_ref = f"role-task-goal-conditioning:{contrast.contrast_id}:{side.side_id}:v1"
        return ProviderObservationIngressCaseV1(
            case_id=execution_ref,
            title=f"{contrast.title} / {side.side_id}",
            capability_kind="OCR_TEXT_EVIDENCE",
            capability_ref="text_recognition",
            modality="OCR",
            input_source_ref=source_ref,
            execution_instance_ref=execution_ref,
            information_need_ref=side.information_need_ref,
            required_information_refs=side.required_information_refs,
            available_information_refs=side.available_information_refs,
            context_ref=f"context:real-role-task-goal-conditioning:{contrast.contrast_id}",
            intent_ref=side.goal_ref,
            task_ref=side.task_ref,
            goal_ref=side.goal_ref,
            concern_ref=side.concern_ref,
            role_refs=(side.role_ref,),
            field_refs=contrast.field_refs,
            relation_refs=contrast.relation_refs,
            source_ref=source_ref,
            raw_result_ref=f"provider-native-output:{execution_ref}",
            expected_evidence_kinds=("text_candidate",),
            temporal_ref=f"time:real-role-task-goal-conditioning:{contrast.contrast_id}:{side.side_id}",
            observation_information_refs=side.observed_information_refs,
        )

    @staticmethod
    def _side_record(
        contrast: ConditioningContrastSpecV1,
        side: ConditioningSideSpecV1,
        result: Dict[str, Any],
    ) -> Dict[str, Any]:
        native = result.get("provider") or (result.get("details") or {}).get("provider_native_result") or {}
        provider_request = result.get("provider_request")
        provider_result = result.get("provider_result")
        proof = result.get("cognitive_proof")
        route = result.get("a_route_result")
        details = result.get("details") or {}
        projection = _native_projection(native)
        stage_results = getattr(route, "stage_results", ()) if route else ()
        cstate_reached = any(getattr(stage, "stage_id", None) == "COGNITIVE_STATE" for stage in stage_results)
        errors = list(result.get("errors") or ())
        if not proof:
            errors.append("cognitive_proof_missing")
        if not result.get("runtime_observation_ref"):
            errors.append("runtime_observation_missing")
        if not result.get("gateway_admission_ref"):
            errors.append("gateway_admission_missing")
        plane_g, plane_g_violations = evaluate_plane_g_compliance_v1(
            run_ref=result.get("a_route_execution_ref") or result.get("runtime_observation_ref") or side.side_id,
            execution_mode=EXECUTION_MODE,
            replay_input_ref=result.get("runtime_observation_ref"),
            gateway_admitted=bool(result.get("gateway_admission_ref")),
            cognition_owner_ref=getattr(proof, "owner_ref", None),
            transition_refs=tuple(getattr(proof, "cognitive_transition_refs", ()) if proof else ()),
            model_invocation=bool(result.get("model_invoked")),
            provider_invocation=bool(result.get("provider_invoked")),
            live_observation_execution=bool(result.get("runtime_observation_ref")),
            action_execution=False,
            field_mutation=False,
            world_truth_declared=bool(getattr(proof, "world_truth_declared", False)) if proof else False,
            memory_promotion=False,
            knowledge_promotion=False,
            experience_promotion=False,
            evaluation_constructed_cognition=False,
            whitebox_mutation=False,
            unavailable_metrics=("latency", "resource_usage"),
            sufficiency_ref=getattr(proof, "sufficiency_ref", None),
            sufficiency_owner_ref=getattr(proof, "sufficiency_owner_ref", None),
            information_gap_ref=getattr(proof, "information_gap_ref", None),
            information_gap_owner_ref=getattr(proof, "information_gap_owner_ref", None),
            reobservation_ref=getattr(proof, "reobservation_ref", None),
            reobservation_owner_ref=getattr(proof, "reobservation_owner_ref", None),
            next_cycle_ingress_ref=getattr(proof, "next_cycle_ingress_ref", None),
            hypothesis_revision_ref=getattr(proof, "hypothesis_revision_ref", None),
            hypothesis_revision_owner_ref=getattr(proof, "hypothesis_revision_owner_ref", None),
            stop_ref=getattr(proof, "stop_ref", None),
            stop_owner_ref=getattr(proof, "stop_owner_ref", None),
            premature_stop=bool(getattr(proof, "stop_ref", None) and getattr(proof, "sufficiency_status", None) != "SUFFICIENT"),
            unnecessary_observation=False,
        )
        errors.extend(f"plane_g:{item}" for item in validate_plane_g_compliance_v1(plane_g))
        errors.extend(f"plane_g_violation:{item.violation_id}" for item in plane_g_violations)
        return {
            "side_id": side.side_id,
            "execution_mode": EXECUTION_MODE,
            "source_ref": str(contrast.source_path),
            "role_ref": side.role_ref,
            "task_ref": side.task_ref,
            "goal_ref": side.goal_ref,
            "concern_ref": side.concern_ref,
            "information_need_ref": side.information_need_ref,
            "required_information_refs": list(side.required_information_refs),
            "available_information_refs": list(result.get("available_information_refs") or ()),
            "supported_information_refs": [
                ref for ref in side.required_information_refs
                if ref not in (getattr(proof, "conditioned_missing_information_refs", ()) if proof else ())
            ],
            "evidence_information_refs": _jsonable(result.get("evidence_information_refs") or ()),
            "inherited_information_refs": _jsonable(result.get("inherited_information_refs") or ()),
            "attention_refs": list(getattr(proof, "conditioned_attention_refs", ()) if proof else ()),
            "evidence_relevance": list(getattr(proof, "conditioned_evidence_relevance", ()) if proof else ()),
            "relation_interpretation_candidates": list(getattr(proof, "relation_interpretation_candidates", ()) if proof else ()),
            "current_world_candidate": {
                "ref": getattr(proof, "current_world_ref", None),
                "kind": getattr(proof, "conditioned_world_kind_candidate", None),
            },
            "sufficiency": getattr(proof, "sufficiency_candidate", None).status if proof and getattr(proof, "sufficiency_candidate", None) else None,
            "sufficiency_status": getattr(proof, "sufficiency_candidate", None).status if proof and getattr(proof, "sufficiency_candidate", None) else None,
            "sufficiency_ref": getattr(proof, "sufficiency_ref", None),
            "information_gap_ref": getattr(proof, "information_gap_ref", None),
            "information_gap": _jsonable(getattr(proof, "information_gap_candidate", None)),
            "missing_information_refs": list(getattr(proof, "conditioned_missing_information_refs", ()) if proof else ()),
            "stop_ref": getattr(proof, "stop_ref", None),
            "stop_reason": getattr(proof, "stop_reason", None),
            "provider_ref": getattr(provider_request, "provider_ref", None),
            "model_ref": getattr(provider_request, "model_ref", None),
            "capability_ref": getattr(provider_request, "capability_ref", None),
            "provider_request_ref": getattr(provider_request, "provider_request_ref", None),
            "provider_result_ref": getattr(provider_result, "provider_result_ref", None),
            "execution_instance_ref": getattr(provider_request, "execution_instance_ref", None),
            "provider_real_execution_attempted": bool(result.get("provider_real_execution_attempted")),
            "provider_real_execution_verified": bool(result.get("provider_real_execution_verified")),
            "provider_invoked": bool(result.get("provider_invoked")),
            "model_invoked": bool(result.get("model_invoked")),
            "provider_status": getattr(provider_result, "status", None),
            "empty_result": bool(getattr(provider_result, "empty_result", False)),
            "provider_native_result": _jsonable(native),
            "provider_runtime_result": _jsonable(provider_result),
            "runtime_observation_ref": result.get("runtime_observation_ref"),
            "gateway_admission_ref": result.get("gateway_admission_ref"),
            "evidence_refs": list(result.get("evidence_refs") or ()),
            "recognized_text_candidates": list(native.get("raw_text_candidates") or ()) if isinstance(native, dict) else [],
            "native_observation_projection": projection,
            "native_observation_fingerprint": _fingerprint(projection),
            "a_route_execution_ref": result.get("a_route_execution_ref"),
            "cognitive_state_reached": cstate_reached,
            "cognitive_state_ref": getattr(proof, "execution_ref", None),
            "cognitive_material_snapshot": _semantic_snapshot(proof),
            "recorded_result_used": False,
            "forbidden_behaviors": {
                "scenario_id_driven_cognition": False,
                "identity_only_difference": False,
                "world_truth_declared": bool(getattr(proof, "world_truth_declared", False)) if proof else False,
                "fact_admitted": False,
                "field_mutation": False,
                "decision_execution": False,
                "task_execution": False,
                "action_execution": False,
                "runtime_executor_invocation": False,
                "device_control": False,
            },
            "route": _jsonable(route),
            "gateway": details.get("gateway"),
            "plane_g": {"result": _jsonable(plane_g), "violations": _jsonable(plane_g_violations)},
            "validation_errors": list(dict.fromkeys(str(item) for item in errors)),
        }

    def _run_side(self, contrast: ConditioningContrastSpecV1, side: ConditioningSideSpecV1) -> Dict[str, Any]:
        source_ref = str(contrast.source_path)
        provider_case = self._provider_case(contrast, side, source_ref=source_ref)
        result = self.ocr_engine.run(provider_case, source_ref=source_ref)
        return self._side_record(contrast, side, result)

    @staticmethod
    def _compare(contrast: ConditioningContrastSpecV1, left: Dict[str, Any], right: Dict[str, Any]) -> Dict[str, Any]:
        changed = []
        for name in ("role_ref", "task_ref", "goal_ref", "information_need_ref", "required_information_refs"):
            if left.get(name) != right.get(name):
                changed.append(name)
        left_semantic = left.get("cognitive_material_snapshot") or {}
        right_semantic = right.get("cognitive_material_snapshot") or {}
        material_differences = [
            name for name in left_semantic
            if name not in {"candidate_only", "world_truth_declared"}
            and left_semantic.get(name) != right_semantic.get(name)
        ]
        physical_equal = (
            left.get("source_ref") == right.get("source_ref")
            and left.get("provider_ref") == right.get("provider_ref") == "provider:ocr_v1"
            and left.get("model_ref") == right.get("model_ref") == "model:ocr_v1"
            and left.get("capability_ref") == right.get("capability_ref") == "text_recognition"
            and left.get("native_observation_fingerprint") == right.get("native_observation_fingerprint")
            and left.get("native_observation_projection") == right.get("native_observation_projection")
        )
        expected_dimension = {
            "GOAL": "goal_ref",
            "TASK": "task_ref",
            "ROLE": "role_ref",
        }[contrast.category]
        return {
            "physical_evidence_equivalent": physical_equal,
            "conditioning_dimensions_changed": changed,
            "cognitive_material_differences": material_differences,
            "identity_only_difference": not bool(material_differences),
            "expected_difference_dimension": expected_dimension,
            "expected_difference_observed": expected_dimension in changed and bool(material_differences),
            "unexpected_physical_mutation": not physical_equal,
        }

    def run(self, contrasts: Tuple[ConditioningContrastSpecV1, ...]) -> Dict[str, Any]:
        contrast_results = []
        for contrast in contrasts:
            left = self._run_side(contrast, contrast.left)
            right = self._run_side(contrast, contrast.right)
            contrast_results.append({
                "contrast_id": contrast.contrast_id,
                "category": contrast.category,
                "title": contrast.title,
                "source_ref": str(contrast.source_path),
                "left": left,
                "right": right,
                "comparison": self._compare(contrast, left, right),
            })
        sides = [side for item in contrast_results for side in (item["left"], item["right"])]
        return {
            "phase": PHASE,
            "execution_mode": EXECUTION_MODE,
            "provider_family": "ocr",
            "capability_ref": "text_recognition",
            "provider_ref": "provider:ocr_v1",
            "model_ref": "model:ocr_v1",
            "semantic_driver": "role+task+goal+information_need+admitted_evidence",
            "role_conditioning_canonical_input_gap": False,
            "same_source_required": True,
            "contrasts": contrast_results,
            "side_count": len(sides),
            "real_provider_invocation_count": sum(1 for side in sides if side.get("provider_invoked")),
            "real_model_invocation_count": sum(1 for side in sides if side.get("model_invoked")),
            "recorded_result_used": False,
            "forbidden_behaviors": {
                "scenario_id_driven_cognition": False,
                "identity_only_fake_difference": any(item["comparison"]["identity_only_difference"] for item in contrast_results),
                "world_truth_declared": False,
                "fact_admitted": False,
                "field_mutation": False,
                "decision_execution": False,
                "task_execution": False,
                "action_execution": False,
                "runtime_executor_invocation": False,
                "device_control": False,
            },
            "validation_errors": [
                error for side in sides for error in side.get("validation_errors", ())
            ],
            "operational_result": "PENDING_USER_TERMINAL_VERIFICATION",
            "cognitive_logic_result": "PENDING_USER_TERMINAL_VERIFICATION",
            "final_decision": "PENDING_USER_TERMINAL_VERIFICATION",
            "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
        }


__all__ = ["PHASE", "RealRoleTaskGoalConditioningEngineV1", "_jsonable"]
