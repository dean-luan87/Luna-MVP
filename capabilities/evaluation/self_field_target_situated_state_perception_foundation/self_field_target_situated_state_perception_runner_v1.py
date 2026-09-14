"""Controlled runner for Self/Field/Target/Relation condition perception.

This runner evaluates preconditions only.  It does not invoke OCR, a provider,
or a model; the inputs are controlled observation-state candidates.
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import Any, Dict

from capabilities.midplatform.core.situated_capability_preconditions.minimum_situated_condition_resolution_v1 import (
    resolve_minimum_situated_conditions,
)
from capabilities.midplatform.core.situated_capability_preconditions.situated_capability_precondition_engine_v1 import (
    evaluate,
    jsonable as precondition_jsonable,
)
from capabilities.midplatform.core.situated_capability_preconditions.situated_capability_precondition_types_v1 import (
    CapabilityNeedCandidateV1,
    CapabilityPreconditionDefinitionV1,
    SituatedCapabilityPreconditionRequestV1,
    SituatedCapabilityStateV1,
)
from capabilities.midplatform.core.situated_capability_preconditions.situated_state_perception_engine_v1 import (
    derive,
)
from capabilities.evaluation.situated_capability_precondition_cognition_foundation.case_definitions_v1 import (
    ADJUSTMENTS,
    ALL_SUPPORTED_CONDITIONS,
)
from .case_definitions_v1 import build_cases_v1


PHASE = "Phase-P1-Luna-Self-Field-Target-Situated-State-Perception-Foundation-v1-001"
EXECUTION_MODE = "CONTROLLED_SITUATED_STATE_PERCEPTION"


def _repo_root() -> Path:
    for candidate in (Path(__file__).resolve(), *Path(__file__).resolve().parents):
        if all((candidate / marker).exists() for marker in ("capabilities", "docs", "README.md")):
            return candidate
    raise RuntimeError("repository root sentinel not found")


ROOT = _repo_root()
OUTPUT_DIR = ROOT / "_eval_out/self_field_target_situated_state_perception_foundation_v1"


def _definition() -> CapabilityPreconditionDefinitionV1:
    return CapabilityPreconditionDefinitionV1(
        capability_requirement_ref="capability-requirement:text-recognition:v1",
        capability_ref="text_recognition",
        supported_condition_refs=ALL_SUPPORTED_CONDITIONS,
        optional_condition_refs=tuple(),
        adjustment_by_condition_ref=ADJUSTMENTS,
        source_refs=(
            "capabilities/registry/luna_capability_registry_v1.json",
            "capabilities/midplatform/core/situated_capability_preconditions/minimum_situated_condition_resolution_v1.py",
        ),
        provenance_refs=("provenance:capability-definition:text-recognition:v1",),
    )


def _precondition_request(binding: Any) -> SituatedCapabilityPreconditionRequestV1:
    raw = binding.request
    need = CapabilityNeedCandidateV1(
        capability_need_ref=f"capability-need:{raw.case_id}:{raw.state_id}",
        capability_requirement_ref=raw.capability_requirement_ref,
        goal_ref=binding.goal_ref,
        intent_ref="intent:understand-transit-sign:v1",
        concern_ref="concern:transit-sign-text:v1",
        information_need_ref=binding.information_need_ref,
        current_cognitive_state_ref=f"cognitive-state:{raw.case_id}:{raw.state_id}",
        required_information_refs=(binding.information_need_ref,),
        available_information_refs=tuple(),
        information_gap_refs=(f"information-gap:{raw.case_id}:{raw.state_id}",),
        capability_need_active_candidate=binding.capability_need_active_candidate,
        continuation_possible_candidate=binding.continuation_possible_candidate,
        source_refs=(f"controlled:capability-need:{raw.case_id}:{raw.state_id}",),
        provenance_refs=(f"provenance:capability-need:{raw.case_id}:{raw.state_id}",),
    )
    definition = _definition()
    minimum = resolve_minimum_situated_conditions(
        capability_definition=definition,
        information_need_ref=binding.information_need_ref,
        goal_ref=binding.goal_ref,
        intent_ref=need.intent_ref,
        concern_ref=need.concern_ref,
    )
    # No condition status is supplied here.  It is filled only by the
    # situated-state perception engine from Self/Field/Target/Relation inputs.
    empty_state = SituatedCapabilityStateV1(
        situated_state_ref=raw.situated_state_ref,
        capability_requirement_ref=raw.capability_requirement_ref,
        self_state_refs=(raw.self_state.state_ref,),
        field_state_refs=raw.field_state_refs,
        target_refs=raw.target_refs,
        relation_refs=(raw.relative_state.relative_state_ref,),
        temporal_ref=raw.temporal_ref,
        satisfied_condition_refs=tuple(),
        condition_state_refs=tuple(),
        relation_stability_candidate=raw.relative_state.stability_candidate,
        source_refs=raw.source_refs,
        provenance_refs=raw.provenance_refs,
    )
    return SituatedCapabilityPreconditionRequestV1(
        case_id=raw.case_id,
        state_id=raw.state_id,
        cycle_index=raw.cycle_index,
        temporal_ref=raw.temporal_ref,
        capability_need=need,
        precondition_definition=definition,
        minimum_condition_requirement=minimum,
        situated_state=empty_state,
        capability_available_candidate=binding.capability_available_candidate,
        previous_opportunity_status=None,
        source_refs=raw.source_refs,
        provenance_refs=raw.provenance_refs,
    )


def run_controlled() -> Dict[str, Any]:
    records = []
    for binding in build_cases_v1():
        raw = binding.request
        perception = derive(raw)
        precondition_request = _precondition_request(binding)
        evaluated_request = replace(precondition_request, situated_state=perception.situated_state)
        precondition_result = evaluate(evaluated_request)
        records.append({
            "case_id": raw.case_id,
            "state_id": raw.state_id,
            "cycle_index": raw.cycle_index,
            "perception": perception,
            "precondition_result": precondition_result,
        })
    output = {
        "phase": PHASE,
        "execution_mode": EXECUTION_MODE,
        "case_count": len(records),
        "cases": records,
        "forbidden_behaviors": {
            "provider_invocation": False,
            "model_invocation": False,
            "decision_execution": False,
            "task_execution": False,
            "device_control": False,
            "action_execution": False,
            "field_mutation": False,
            "world_truth_declared": False,
        },
        "scenario_id_semantic_driver": False,
        "cycle_index_semantic_driver": False,
        "validation_errors": [],
        "runtime_execution": "NOT_REQUESTED",
        "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
    }
    # The existing candidate serializers preserve all nested contract fields.
    return _jsonable(output)


def _jsonable(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_jsonable(item) for item in value]
    if hasattr(value, "__dataclass_fields__"):
        return precondition_jsonable(value)
    return value


def main() -> None:
    import json
    summary = run_controlled()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output = json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True)
    (OUTPUT_DIR / "runner_summary_v1.json").write_text(output + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()


__all__ = ["EXECUTION_MODE", "PHASE", "run_controlled"]
