"""Finite controlled Situated-State sequences for regulation-loop evaluation."""

from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path
from typing import Tuple

from capabilities.evaluation.self_field_target_situated_state_perception_foundation.case_definitions_v1 import (
    SituatedStateCaseBindingV1,
    _binding,
)
from capabilities.evaluation.situated_eligibility_gated_real_ocr_execution_integration.case_definitions_v1 import (
    DEFAULT_SOURCE_NAME,
    OCR_ASSET_ROOT,
)


@dataclass(frozen=True)
class RegulationStepBindingV1:
    binding: SituatedStateCaseBindingV1
    execute_if_eligible: bool = True
    defer_reason: str = ""


@dataclass(frozen=True)
class RegulationCaseDefinitionV1:
    case_id: str
    steps: Tuple[RegulationStepBindingV1, ...]


def _with_source(binding: SituatedStateCaseBindingV1, source_ref: str) -> SituatedStateCaseBindingV1:
    request = replace(
        binding.request,
        source_refs=(source_ref,),
        evidence_refs=(f"observation-candidate:{binding.request.case_id}:{binding.request.state_id}",),
    )
    return replace(binding, request=request)


def _step(
    source_ref: str,
    case_id: str,
    state_id: str,
    cycle_index: int,
    *,
    execute_if_eligible: bool = True,
    defer_reason: str = "",
    **kwargs: object,
) -> RegulationStepBindingV1:
    return RegulationStepBindingV1(
        binding=_with_source(_binding(case_id, state_id, cycle_index, **kwargs), source_ref),
        execute_if_eligible=execute_if_eligible,
        defer_reason=defer_reason,
    )


def build_cases_v1(repository_root: Path) -> Tuple[RegulationCaseDefinitionV1, ...]:
    source_ref = str((repository_root / OCR_ASSET_ROOT / DEFAULT_SOURCE_NAME).resolve())
    return (
        RegulationCaseDefinitionV1(
            case_id="CONDITION_GAP_WAITS_WITHOUT_PROVIDER",
            steps=(_step(source_ref, "CONDITION_GAP_WAITS_WITHOUT_PROVIDER", "t0", 0, scale="SMALL"),),
        ),
        RegulationCaseDefinitionV1(
            case_id="DYNAMIC_CONDITION_CHANGE_OPENS_OBSERVATION",
            steps=(
                _step(source_ref, "DYNAMIC_CONDITION_CHANGE_OPENS_OBSERVATION", "t0", 0, scale="SMALL"),
                _step(source_ref, "DYNAMIC_CONDITION_CHANGE_OPENS_OBSERVATION", "t1", 1),
            ),
        ),
        RegulationCaseDefinitionV1(
            case_id="MULTI_STATE_WAIT_THEN_OBSERVE_ONCE",
            steps=(
                _step(source_ref, "MULTI_STATE_WAIT_THEN_OBSERVE_ONCE", "t0", 0, visibility="NOT_VISIBLE"),
                _step(source_ref, "MULTI_STATE_WAIT_THEN_OBSERVE_ONCE", "t1", 1, scale="SMALL"),
                _step(source_ref, "MULTI_STATE_WAIT_THEN_OBSERVE_ONCE", "t2", 2),
            ),
        ),
        RegulationCaseDefinitionV1(
            case_id="OPPORTUNITY_CAN_BE_LOST_BEFORE_EXECUTION",
            steps=(
                _step(source_ref, "OPPORTUNITY_CAN_BE_LOST_BEFORE_EXECUTION", "t0", 0, scale="SMALL"),
                _step(
                    source_ref,
                    "OPPORTUNITY_CAN_BE_LOST_BEFORE_EXECUTION",
                    "t1",
                    1,
                    execute_if_eligible=False,
                    defer_reason="controlled opportunity observation before the next state is evaluated",
                ),
                _step(
                    source_ref,
                    "OPPORTUNITY_CAN_BE_LOST_BEFORE_EXECUTION",
                    "t2",
                    2,
                    motion="HIGH",
                    relation_stability="UNSTABLE",
                ),
            ),
        ),
        RegulationCaseDefinitionV1(
            case_id="OBSERVATION_NOT_REQUIRED_EXITS_REGULATION",
            steps=(_step(source_ref, "OBSERVATION_NOT_REQUIRED_EXITS_REGULATION", "t0", 0, continuation=True),),
        ),
    )


__all__ = ["RegulationCaseDefinitionV1", "RegulationStepBindingV1", "build_cases_v1"]
