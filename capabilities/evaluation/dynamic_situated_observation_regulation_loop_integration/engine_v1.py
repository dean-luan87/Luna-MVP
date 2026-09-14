"""Bounded regulation-loop composition over existing Situated and OCR owners."""

from __future__ import annotations

import dataclasses
from pathlib import Path
from typing import Any, Dict, Tuple

from capabilities.evaluation.self_field_target_situated_state_perception_foundation.self_field_target_situated_state_perception_runner_v1 import (
    _precondition_request,
)
from capabilities.evaluation.situated_eligibility_gated_real_ocr_execution_integration.engine_v1 import (
    EXECUTION_MODE as OCR_EXECUTION_MODE,
    SituatedEligibilityGatedRealOCRExecutionEngineV1,
)
from capabilities.midplatform.core.situated_capability_preconditions.situated_capability_precondition_engine_v1 import (
    evaluate,
)
from capabilities.midplatform.core.situated_capability_preconditions.situated_state_perception_engine_v1 import (
    derive,
)

from .case_definitions_v1 import RegulationCaseDefinitionV1, RegulationStepBindingV1, build_cases_v1
from .types_v1 import (
    DynamicObservationRegulationCaseResultV1,
    DynamicObservationRegulationStateV1,
)


PHASE = "Phase-P1-Luna-Dynamic-Situated-Observation-Regulation-Loop-Integration-v1-001"
EXECUTION_MODE = OCR_EXECUTION_MODE
SITUATED_STATE_MODE = "CONTROLLED_SITUATED_STATE_CANDIDATES"
PROVIDER_EXECUTION_MODE = "EXISTING_GATED_REAL_OCR"


def _jsonable(value: Any) -> Any:
    if dataclasses.is_dataclass(value):
        return {key: _jsonable(item) for key, item in dataclasses.asdict(value).items()}
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_jsonable(item) for item in value]
    return value


def _value(value: Any, key: str, default: Any = None) -> Any:
    if isinstance(value, dict):
        return value.get(key, default)
    return getattr(value, key, default)


def _runtime_ref(runtime: Dict[str, Any] | None, key: str) -> str | None:
    if not runtime:
        return None
    value = runtime.get(key)
    return value if isinstance(value, str) and value else None


def _nested_runtime_ref(runtime: Dict[str, Any] | None, key: str, ref_key: str) -> str | None:
    if not runtime:
        return None
    return _value(runtime.get(key), ref_key)


class DynamicSituatedObservationRegulationLoopEngineV1:
    """Evaluate finite situated states and call existing OCR only when admitted."""

    def __init__(self, *, repository_root: Path) -> None:
        self.repository_root = repository_root
        self.gated_ocr_engine = SituatedEligibilityGatedRealOCRExecutionEngineV1(
            repository_root=repository_root,
        )

    @staticmethod
    def _precondition(step: RegulationStepBindingV1) -> object:
        raw = step.binding.request
        perception = derive(raw)
        request = _precondition_request(step.binding)
        return evaluate(dataclasses.replace(request, situated_state=perception.situated_state))

    @staticmethod
    def _status(precondition: Any, *, deferred: bool, runtime: Dict[str, Any] | None) -> str:
        if precondition.necessity.status == "NOT_REQUIRED":
            return "OBSERVATION_NOT_REQUIRED"
        if not precondition.eligibility.eligible_now:
            return "WAITING_FOR_CONDITION_CHANGE"
        if deferred:
            return "OPPORTUNITY_OPEN"
        if runtime and runtime.get("sufficiency_status") == "SUFFICIENT":
            return "INFORMATION_SUFFICIENT"
        if runtime and runtime.get("sufficiency_status") == "INSUFFICIENT":
            return "INFORMATION_STILL_MISSING"
        return "OBSERVATION_EXECUTED"

    @staticmethod
    def _events(
        precondition: Any,
        *,
        deferred: bool,
        runtime: Dict[str, Any] | None,
    ) -> Tuple[str, ...]:
        events = [
            "SITUATED_STATE_REEVALUATED",
            "CAPABILITY_NECESSITY_EVALUATED",
            "SITUATED_FEASIBILITY_EVALUATED",
            "CONDITION_GAP_EVALUATED",
            "ADJUSTMENT_NEED_EVALUATED",
            "CAPABILITY_OPPORTUNITY_EVALUATED",
            "SITUATED_ELIGIBILITY_EVALUATED",
        ]
        if not precondition.eligibility.eligible_now:
            events.append("WAIT_FOR_SITUATED_STATE_CHANGE")
        elif deferred:
            events.append("OPPORTUNITY_OPEN_EXECUTION_DEFERRED")
        elif runtime is not None:
            events.extend(("EXECUTION_ADMISSION", "PROVIDER_RUNTIME", "POST_OBSERVATION_COGNITION"))
        return tuple(events)

    def run_step(
        self,
        step: RegulationStepBindingV1,
        *,
        previous_regulation_ref: str | None,
        observation_cycle_index: int,
    ) -> DynamicObservationRegulationStateV1:
        raw = step.binding.request
        precondition = self._precondition(step)
        eligible = precondition.eligibility.eligible_now is True
        deferred = bool(eligible and not step.execute_if_eligible)
        execution_record = None
        runtime: Dict[str, Any] | None = None

        if eligible and not deferred:
            # The existing gate owns the only real OCR call and re-evaluates the
            # current precondition immediately before entering Provider Runtime.
            execution_record = self.gated_ocr_engine.run_binding(
                step.binding,
                observation_cycle_index=observation_cycle_index,
            )
            runtime = execution_record.runtime_result

        if execution_record is not None:
            admission = execution_record.execution_admission
            provider_attempted = execution_record.provider_real_execution_attempted
            provider_verified = execution_record.provider_real_execution_verified
            provider_invoked = execution_record.provider_invoked
            model_invoked = execution_record.model_invoked
            recorded_used = execution_record.recorded_provider_result_used
        else:
            admission = (
                self.gated_ocr_engine._admission(precondition)
                if not deferred
                else None
            )
            provider_attempted = False
            provider_verified = False
            provider_invoked = False
            model_invoked = False
            recorded_used = False

        proof = runtime.get("cognitive_proof") if runtime else None
        pre_need = precondition.necessity
        feasibility = precondition.feasibility
        opportunity = precondition.opportunity
        eligibility = precondition.eligibility
        real_invocation = bool(provider_attempted and provider_invoked and model_invoked)
        condition_gaps = tuple(item.condition_gap_ref for item in precondition.condition_gaps)
        adjustments = tuple(item.adjustment_need_ref for item in precondition.adjustment_needs)
        provider_result = runtime.get("provider_result") if runtime else None
        trace = tuple(dict.fromkeys(
            (
                *precondition.trace_refs,
                raw.situated_state_ref,
                *(admission.trace_refs if admission else ()),
                *(
                    ref
                    for ref in (
                        _nested_runtime_ref(runtime, "provider_request", "provider_request_ref"),
                        _nested_runtime_ref(runtime, "provider_result", "provider_result_ref"),
                        _runtime_ref(runtime, "runtime_observation_ref"),
                        _runtime_ref(runtime, "gateway_admission_ref"),
                        _runtime_ref(runtime, "a_route_execution_ref"),
                    )
                    if ref
                ),
                *((previous_regulation_ref,) if previous_regulation_ref else ()),
            )
        ))
        provenance = tuple(dict.fromkeys((*precondition.provenance_refs, *trace)))
        return DynamicObservationRegulationStateV1(
            regulation_ref=f"dynamic-observation-regulation:{raw.case_id}:{raw.state_id}",
            case_id=raw.case_id,
            state_id=raw.state_id,
            cycle_index=raw.cycle_index,
            observation_cycle_index=(
                observation_cycle_index if real_invocation else None
            ),
            capability_need_ref=pre_need.capability_need_ref,
            information_need_ref=pre_need.required_information_refs[0] if pre_need.required_information_refs else "",
            capability_requirement_ref=pre_need.capability_requirement_ref,
            current_situated_state_ref=feasibility.situated_state_ref,
            feasibility_ref=feasibility.feasibility_ref,
            condition_gap_refs=condition_gaps,
            adjustment_need_refs=adjustments,
            opportunity_ref=opportunity.opportunity_ref,
            eligibility_ref=eligibility.eligibility_ref,
            execution_admission_ref=admission.admission_ref if admission else None,
            provider_result_ref=_value(provider_result, "provider_result_ref"),
            runtime_observation_ref=_runtime_ref(runtime, "runtime_observation_ref"),
            gateway_admission_ref=_runtime_ref(runtime, "gateway_admission_ref"),
            evidence_refs=tuple(runtime.get("evidence_refs") or ()) if runtime else tuple(),
            a_route_execution_ref=_runtime_ref(runtime, "a_route_execution_ref"),
            cognitive_state_ref=_value(proof, "execution_ref"),
            sufficiency_ref=_runtime_ref(runtime, "sufficiency_ref"),
            sufficiency_status=runtime.get("sufficiency_status") if runtime else None,
            information_gap_ref=_runtime_ref(runtime, "information_gap_ref"),
            stop_ref=_runtime_ref(runtime, "stop_ref"),
            regulation_status=self._status(precondition, deferred=deferred, runtime=runtime),
            temporal_ref=raw.temporal_ref,
            previous_regulation_ref=previous_regulation_ref,
            provider_execution_admitted=admission.provider_execution_admitted if admission else False,
            provider_real_execution_attempted=provider_attempted,
            provider_real_execution_verified=provider_verified,
            provider_invoked=provider_invoked,
            model_invoked=model_invoked,
            provider_invocation_count=int(real_invocation),
            model_invocation_count=int(real_invocation),
            recorded_provider_result_used=recorded_used,
            situated_precondition_result=precondition,
            execution_admission=admission,
            provider_runtime_result=runtime,
            execution_events=self._events(precondition, deferred=deferred, runtime=runtime),
            trace_refs=trace,
            provenance_refs=provenance,
            validation_errors=tuple(runtime.get("errors") or ()) if runtime else tuple(),
        )

    def run_case(self, case: RegulationCaseDefinitionV1) -> DynamicObservationRegulationCaseResultV1:
        states = []
        previous = None
        observation_count = 0
        for step in case.steps:
            state = self.run_step(
                step,
                previous_regulation_ref=previous,
                observation_cycle_index=observation_count + 1,
            )
            states.append(state)
            previous = state.regulation_ref
            observation_count += state.provider_invocation_count
        final_state = states[-1]
        return DynamicObservationRegulationCaseResultV1(
            case_id=case.case_id,
            goal_ref=case.steps[0].binding.goal_ref,
            intent_ref="intent:understand-transit-sign:v1",
            concern_ref="concern:transit-sign-text:v1",
            information_need_ref=case.steps[0].binding.information_need_ref,
            capability_requirement_ref=case.steps[0].binding.request.capability_requirement_ref,
            states=tuple(states),
            observation_cycle_count=observation_count,
            real_provider_invocation_count=observation_count,
            final_regulation_status=final_state.regulation_status,
            validation_errors=tuple(error for state in states for error in state.validation_errors),
        )

    def run_cases(self) -> Tuple[DynamicObservationRegulationCaseResultV1, ...]:
        return tuple(self.run_case(case) for case in build_cases_v1(self.repository_root))


def jsonable(value: Any) -> Any:
    return _jsonable(value)


__all__ = [
    "EXECUTION_MODE",
    "PHASE",
    "PROVIDER_EXECUTION_MODE",
    "SITUATED_STATE_MODE",
    "DynamicSituatedObservationRegulationLoopEngineV1",
    "jsonable",
]
