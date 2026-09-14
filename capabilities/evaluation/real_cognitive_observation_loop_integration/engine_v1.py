"""Compose real OCR observations with the existing canonical cognitive loop."""

from __future__ import annotations

import dataclasses
from pathlib import Path
from typing import Any, Dict, Iterable, Tuple

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

from .types_v1 import RealCognitiveObservationCaseV1, RealOCRObservationBindingV1


PHASE = "Phase-P1-Luna-Real-Cognitive-Observation-Loop-Integration-v1-001"
EXECUTION_MODE = "LIVE_RUNTIME"
MAX_OBSERVATION_CYCLES = 2


def _jsonable(value: Any) -> Any:
    if dataclasses.is_dataclass(value):
        return {key: _jsonable(item) for key, item in dataclasses.asdict(value).items()}
    if isinstance(value, dict):
        return {key: _jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_jsonable(item) for item in value]
    return value


def _tuple(value: Iterable[str] | None) -> Tuple[str, ...]:
    return tuple(str(item) for item in (value or ()))


def _native_candidates(result: Dict[str, Any]) -> list[Dict[str, Any]]:
    native = result.get("provider") or (result.get("details") or {}).get("provider_native_result") or {}
    candidates = native.get("raw_text_candidates") if isinstance(native, dict) else ()
    return [item for item in candidates if isinstance(item, dict)] if isinstance(candidates, list) else []


class RealCognitiveObservationLoopEngineV1:
    """Run no more than two real OCR observations under canonical cognition."""

    def __init__(self, *, repository_root: Path) -> None:
        self.repository_root = repository_root
        self.ocr_engine = RealOCRProviderExecutionEngineV1()

    @staticmethod
    def _execution_instance_ref(case_id: str, binding: RealOCRObservationBindingV1, cycle_index: int) -> str:
        # The semantic decision never branches on this identity.  The stable
        # tokens make evidence/relevance lineage readable in terminal output.
        return f"cognitive-observation-loop:{case_id}:location:cycle-{cycle_index}:{binding.binding_ref}"

    def _provider_case(
        self,
        case: RealCognitiveObservationCaseV1,
        binding: RealOCRObservationBindingV1,
        cycle_index: int,
        *,
        prior: Dict[str, Any] | None,
    ) -> ProviderObservationIngressCaseV1:
        prior = prior or {}
        return ProviderObservationIngressCaseV1(
            case_id=f"{case.case_id}:cycle-{cycle_index}",
            title=f"{case.title} cycle {cycle_index}",
            capability_kind="OCR_TEXT_EVIDENCE",
            capability_ref="text_recognition",
            modality="OCR",
            input_source_ref=binding.source_ref,
            execution_instance_ref=self._execution_instance_ref(case.case_id, binding, cycle_index),
            information_need_ref=case.information_need_ref,
            required_information_refs=case.required_information_refs,
            available_information_refs=_tuple(prior.get("available_information_refs")),
            context_ref=f"context:real-cognitive-observation-loop:{case.case_id}",
            intent_ref=case.goal_ref,
            task_ref=case.task_ref,
            goal_ref=case.goal_ref,
            concern_ref=case.concern_ref,
            role_refs=case.role_refs,
            field_refs=case.field_refs,
            relation_refs=case.relation_refs,
            source_ref=binding.source_ref,
            raw_result_ref="provider-native-output:pending",
            expected_evidence_kinds=("text_candidate",),
            temporal_ref=f"time:real-cognitive-observation-loop:{case.case_id}:cycle-{cycle_index}",
            observation_information_refs=binding.information_refs,
            cycle_index=cycle_index,
            prior_current_world_ref=prior.get("current_world_ref"),
            prior_hypothesis_refs=_tuple(prior.get("hypothesis_refs")),
            prior_information_gap_ref=prior.get("information_gap_ref"),
            prior_reobservation_ref=prior.get("reobservation_ref"),
            prior_next_cycle_ingress_ref=prior.get("next_cycle_ingress_ref"),
            prior_sufficiency_candidate=prior.get("sufficiency_candidate"),
            prior_information_gap_candidate=prior.get("information_gap_candidate"),
            prior_reobservation_candidate=prior.get("reobservation_candidate"),
            spatial_refs=(binding.source_region_ref,),
        )

    @staticmethod
    def _cycle_record(
        *,
        case: RealCognitiveObservationCaseV1,
        binding: RealOCRObservationBindingV1,
        cycle_index: int,
        result: Dict[str, Any],
        prior: Dict[str, Any] | None,
    ) -> Tuple[Dict[str, Any], Any]:
        proof = result.get("cognitive_proof")
        provider_result = result.get("provider_result")
        route = result.get("a_route_result")
        details = result.get("details") or {}
        native = result.get("provider") or details.get("provider_native_result") or {}
        gateway = details.get("gateway") or {}
        errors = list(result.get("errors") or ())
        if proof is None:
            errors.append("cognitive_proof_missing")
        if result.get("runtime_observation_ref") is None:
            errors.append("runtime_observation_missing")
        if not result.get("gateway_admission_ref"):
            errors.append("gateway_admission_missing")

        stage_results = getattr(route, "stage_results", ()) if route is not None else ()
        cognitive_state_ref = None
        for stage in stage_results:
            if getattr(stage, "stage_id", None) == "COGNITIVE_STATE":
                cognitive_state_ref = (getattr(stage, "output_refs", ()) or (None,))[0]
                break
        if proof is not None and cognitive_state_ref is None:
            cognitive_state_ref = proof.execution_ref

        record = {
            "cycle_index": cycle_index,
            "execution_mode": EXECUTION_MODE,
            "source_binding_ref": binding.binding_ref,
            "source_region_ref": binding.source_region_ref,
            "source_ref": binding.source_ref,
            "observation_information_refs": list(binding.information_refs),
            "observation_demand_ref": getattr(result.get("provider_request"), "observation_demand_ref", None),
            "capability_requirement_ref": result.get("capability_requirement_ref"),
            "capability_ref": getattr(result.get("provider_request"), "capability_ref", None),
            "provider_ref": getattr(result.get("provider_request"), "provider_ref", None),
            "model_ref": getattr(result.get("provider_request"), "model_ref", None),
            "provider_request_ref": getattr(result.get("provider_request"), "provider_request_ref", None),
            "provider_result_ref": getattr(provider_result, "provider_result_ref", None),
            "execution_instance_ref": getattr(result.get("provider_request"), "execution_instance_ref", None),
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
            "recognized_text_candidates": _native_candidates(result),
            "a_route_execution_ref": result.get("a_route_execution_ref"),
            "cognitive_state_ref": cognitive_state_ref,
            "cognitive_transition_refs": list(getattr(proof, "cognitive_transition_refs", ()) if proof else ()),
            "previous_cognitive_state_ref": (prior or {}).get("cognitive_state_ref"),
            "sufficiency_ref": getattr(proof, "sufficiency_ref", None),
            "sufficiency_status": getattr(proof, "sufficiency_status", None),
            "sufficiency_candidate": _jsonable(getattr(proof, "sufficiency_candidate", None)),
            "information_gap_ref": getattr(proof, "information_gap_ref", None),
            "information_gap_candidate": _jsonable(getattr(proof, "information_gap_candidate", None)),
            "information_need_ref": case.information_need_ref,
            "gap_source_cognitive_state_ref": cognitive_state_ref,
            "gap_reason": getattr(getattr(proof, "information_gap_candidate", None), "reason", None),
            "missing_requirement_refs": list(getattr(getattr(proof, "information_gap_candidate", None), "missing_information_refs", ()) if proof else ()),
            "reobservation_request_ref": getattr(proof, "reobservation_ref", None),
            "reobservation_candidate": _jsonable(getattr(proof, "reobservation_candidate", None)),
            "next_cycle_ingress_ref": getattr(proof, "next_cycle_ingress_ref", None),
            "hypothesis_revision_ref": getattr(proof, "hypothesis_revision_ref", None),
            "stop_ref": getattr(proof, "stop_ref", None),
            "stop_reason": getattr(proof, "stop_reason", None),
            "conditioned_evidence_relevance": list(getattr(proof, "conditioned_evidence_relevance", ()) if proof else ()),
            "conditioned_missing_information_refs": list(getattr(proof, "conditioned_missing_information_refs", ()) if proof else ()),
            "available_information_refs": list(result.get("available_information_refs") or ()),
            "required_information_refs": list(case.required_information_refs),
            "prior_information_gap_ref": (prior or {}).get("information_gap_ref"),
            "prior_reobservation_ref": (prior or {}).get("reobservation_ref"),
            "prior_next_cycle_ingress_ref": (prior or {}).get("next_cycle_ingress_ref"),
            "recorded_provider_result_used": False,
            "forbidden_behaviors": {
                "scenario_id_driven_cognition": False,
                "world_truth_declared": False,
                "fact_admitted": False,
                "field_mutation": False,
                "decision_execution": False,
                "task_execution": False,
                "action_execution": False,
                "runtime_executor_invocation": False,
                "device_control": False,
            },
            "gateway": gateway,
            "a_route": _jsonable(route),
            "validation_errors": list(dict.fromkeys(str(item) for item in errors)),
        }
        return record, proof

    @staticmethod
    def _select_reobservation_binding(
        case: RealCognitiveObservationCaseV1,
        missing_information_refs: Iterable[str],
    ) -> RealOCRObservationBindingV1 | None:
        missing = set(missing_information_refs)
        binding = case.second_binding
        if binding is not None and missing.intersection(binding.information_refs):
            return binding
        return None

    @staticmethod
    def _prior_payload(record: Dict[str, Any], proof: Any) -> Dict[str, Any]:
        return {
            "available_information_refs": record.get("available_information_refs", ()),
            "current_world_ref": getattr(proof, "current_world_ref", None),
            "hypothesis_refs": getattr(proof, "hypothesis_refs", ()),
            "information_gap_ref": getattr(proof, "information_gap_ref", None),
            "reobservation_ref": getattr(proof, "reobservation_ref", None),
            "next_cycle_ingress_ref": getattr(proof, "next_cycle_ingress_ref", None),
            "sufficiency_candidate": getattr(proof, "sufficiency_candidate", None),
            "information_gap_candidate": getattr(proof, "information_gap_candidate", None),
            "reobservation_candidate": getattr(proof, "reobservation_candidate", None),
            "cognitive_state_ref": record.get("cognitive_state_ref"),
        }

    @staticmethod
    def _plane_g(record: Dict[str, Any], proof: Any) -> Dict[str, Any]:
        plane_g, violations = evaluate_plane_g_compliance_v1(
            run_ref=record.get("a_route_execution_ref") or record.get("execution_instance_ref") or "real-cognitive-observation-loop",
            execution_mode=EXECUTION_MODE,
            replay_input_ref=record.get("runtime_observation_ref"),
            gateway_admitted=bool(record.get("gateway_admission_ref")),
            cognition_owner_ref=getattr(proof, "owner_ref", None),
            transition_refs=tuple(getattr(proof, "cognitive_transition_refs", ()) if proof else ()),
            model_invocation=bool(record.get("model_invoked")),
            provider_invocation=bool(record.get("provider_invoked")),
            live_observation_execution=bool(record.get("runtime_observation_ref")),
            action_execution=False,
            field_mutation=False,
            world_truth_declared=False,
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
        return {
            "result": _jsonable(plane_g),
            "violations": _jsonable(violations),
            "validation_errors": list(validate_plane_g_compliance_v1(plane_g)),
        }

    def _run_cycle(
        self,
        case: RealCognitiveObservationCaseV1,
        binding: RealOCRObservationBindingV1,
        cycle_index: int,
        *,
        prior: Dict[str, Any] | None,
    ) -> Tuple[Dict[str, Any], Any]:
        provider_case = self._provider_case(case, binding, cycle_index, prior=prior)
        result = self.ocr_engine.run(provider_case, source_ref=binding.source_ref)
        record, proof = self._cycle_record(
            case=case,
            binding=binding,
            cycle_index=cycle_index,
            result=result,
            prior=prior,
        )
        record["plane_g"] = self._plane_g(record, proof)
        request = result.get("provider_request")
        record["trace_refs"] = list(dict.fromkeys(
            (*(getattr(request, "trace_refs", ()) if request else ()),
             *(getattr(result.get("provider_result"), "trace_refs", ()) if result.get("provider_result") else ()),
             *(getattr(proof, "cognitive_transition_refs", ()) if proof else ())),
        ))
        record["provenance_refs"] = list(dict.fromkeys(
            (*(getattr(request, "provenance_refs", ()) if request else ()),
             *(getattr(result.get("provider_result"), "provenance_refs", ()) if result.get("provider_result") else ())),
        ))
        return record, proof

    def run_case(self, case: RealCognitiveObservationCaseV1) -> Dict[str, Any]:
        cycles: list[Dict[str, Any]] = []
        first, proof = self._run_cycle(case, case.first_binding, 1, prior=None)
        cycles.append(first)

        # Sufficiency is read from the canonical proof.  The cycle index only
        # bounds ordering; it never decides whether a gap exists.
        if proof is not None and getattr(proof, "sufficiency_status", None) == "INSUFFICIENT":
            gap = getattr(proof, "information_gap_candidate", None)
            missing = getattr(gap, "missing_information_refs", ()) if gap is not None else ()
            next_binding = self._select_reobservation_binding(case, missing)
            if len(cycles) < MAX_OBSERVATION_CYCLES and gap is not None and getattr(proof, "reobservation_ref", None) and next_binding is not None:
                second, second_proof = self._run_cycle(
                    case,
                    next_binding,
                    2,
                    prior=self._prior_payload(first, proof),
                )
                cycles.append(second)

        final = cycles[-1]
        final_sufficiency = final.get("sufficiency_status")
        final_stop = final.get("stop_ref")
        post_sufficiency_reobservation = bool(
            final_sufficiency == "SUFFICIENT" and len(cycles) > 1
            and any(item.get("cycle_index", 0) > final.get("cycle_index", 0) for item in cycles)
        )
        return {
            "phase": PHASE,
            "execution_mode": EXECUTION_MODE,
            "case_id": case.case_id,
            "goal_ref": case.goal_ref,
            "concern_ref": case.concern_ref,
            "information_need_ref": case.information_need_ref,
            "required_information_refs": list(case.required_information_refs),
            "semantic_driver": "goal+information_need+required_and_admitted_evidence",
            "observation_cycles": cycles,
            "observation_cycle_count": len(cycles),
            "revision_occurred": bool(final.get("hypothesis_revision_ref")),
            "final_sufficiency": final_sufficiency,
            "final_stop": final_stop,
            "post_sufficiency_reobservation": post_sufficiency_reobservation,
            "recorded_result_used": False,
            "forbidden_behaviors": {
                "scenario_id_driven_cognition": False,
                "provider_success_as_sufficiency": False,
                "world_truth_declared": False,
                "fact_admitted": False,
                "field_mutation": False,
                "decision_execution": False,
                "task_execution": False,
                "action_execution": False,
                "runtime_executor_invocation": False,
                "device_control": False,
                "cycle_three": False,
            },
            "validation_errors": list(dict.fromkeys(
                error
                for cycle in cycles
                for error in cycle.get("validation_errors", ())
            )),
            "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
        }


__all__ = ["RealCognitiveObservationLoopEngineV1", "PHASE"]
