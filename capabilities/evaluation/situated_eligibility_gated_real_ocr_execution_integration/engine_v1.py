"""Gate the existing real OCR runtime with Situated Eligibility."""

from __future__ import annotations

import dataclasses
from pathlib import Path
from typing import Any, Dict, Tuple

from capabilities.evaluation.self_field_target_situated_state_perception_foundation.self_field_target_situated_state_perception_runner_v1 import (
    _precondition_request,
)
from capabilities.midplatform.core.provider_runtime_to_observation_ingress.real_ocr_provider_execution_engine_v1 import (
    RealOCRProviderExecutionEngineV1,
)
from capabilities.midplatform.core.provider_runtime_to_observation_ingress.types_v1 import (
    ProviderObservationIngressCaseV1,
)
from capabilities.midplatform.core.situated_capability_preconditions.situated_capability_precondition_engine_v1 import (
    evaluate,
)
from capabilities.midplatform.core.situated_capability_preconditions.situated_state_perception_engine_v1 import (
    derive,
)
from .case_definitions_v1 import build_cases_v1
from .types_v1 import (
    GatedOCRExecutionRecordV1,
    SituatedCapabilityExecutionAdmissionV1,
)


PHASE = "Phase-P1-Luna-Situated-Eligibility-Gated-Real-OCR-Execution-Integration-v1-001"
EXECUTION_MODE = "LIVE_RUNTIME"


def _jsonable(value: Any) -> Any:
    if dataclasses.is_dataclass(value):
        return {key: _jsonable(item) for key, item in dataclasses.asdict(value).items()}
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_jsonable(item) for item in value]
    return value


class SituatedEligibilityGatedRealOCRExecutionEngineV1:
    """Evaluate Situated Eligibility before the only real OCR call site."""

    def __init__(self, *, repository_root: Path) -> None:
        self.repository_root = repository_root
        self.ocr_engine = RealOCRProviderExecutionEngineV1()

    @staticmethod
    def _provider_case(
        binding: Any,
        source_ref: str,
        *,
        observation_cycle_index: int | None = None,
    ) -> ProviderObservationIngressCaseV1:
        raw = binding.request
        execution_ref = f"situated-eligibility-gated-ocr:{raw.case_id}:{raw.state_id}"
        return ProviderObservationIngressCaseV1(
            case_id=execution_ref,
            title=f"{raw.case_id} after situated eligibility admission",
            capability_kind="OCR_TEXT_EVIDENCE",
            capability_ref="text_recognition",
            modality="OCR",
            input_source_ref=source_ref,
            execution_instance_ref=execution_ref,
            information_need_ref=binding.information_need_ref,
            required_information_refs=(binding.information_need_ref,),
            available_information_refs=tuple(),
            context_ref=f"context:situated-eligibility-gated-ocr:{raw.case_id}",
            intent_ref="intent:understand-transit-sign:v1",
            task_ref="task:observe-text",
            goal_ref=binding.goal_ref,
            concern_ref="concern:transit-sign-text:v1",
            role_refs=("role:observer",),
            field_refs=raw.field_state_refs,
            relation_refs=(raw.relative_state.relative_state_ref,),
            source_ref=source_ref,
            raw_result_ref=f"provider-native-output:{execution_ref}",
            expected_evidence_kinds=("text_candidate",),
            temporal_ref=raw.temporal_ref,
            observation_information_refs=(binding.information_need_ref,),
            # Regulation state ordering and cognitive observation cycles are
            # different namespaces.  Existing callers retain the historical
            # binding value; an upper-layer integration may provide the
            # canonical cognitive cycle after a real observation is admitted.
            cycle_index=(
                raw.cycle_index
                if observation_cycle_index is None
                else observation_cycle_index
            ),
            spatial_refs=(raw.relative_state.relative_state_ref,),
        )

    @staticmethod
    def _admission(precondition: Any) -> SituatedCapabilityExecutionAdmissionV1:
        eligibility = precondition.eligibility
        admitted = eligibility.eligible_now is True
        reason = (
            "Situated Eligibility is true; existing Provider Runtime admission remains required"
            if admitted
            else "Situated Eligibility is false; real Provider Runtime invocation is blocked before its call site"
        )
        trace = tuple(dict.fromkeys((*precondition.trace_refs, eligibility.eligibility_ref)))
        return SituatedCapabilityExecutionAdmissionV1(
            admission_ref=f"situated-execution-admission:{precondition.case_id}:{precondition.state_id}",
            capability_requirement_ref=eligibility.capability_requirement_ref,
            eligibility_ref=eligibility.eligibility_ref,
            eligible_now=eligibility.eligible_now,
            provider_execution_admitted=admitted,
            reason=reason,
            trace_refs=trace,
            provenance_refs=trace,
        )

    @staticmethod
    def _events_for_runtime(result: Dict[str, Any]) -> Tuple[str, ...]:
        events = ["REAL_PROVIDER_INVOCATION", "PROVIDER_RUNTIME_RESULT"]
        if result.get("runtime_observation_ref"):
            events.append("RUNTIME_OBSERVATION")
        if result.get("gateway_admission_ref"):
            events.append("OBSERVATION_GATEWAY")
        if result.get("evidence_refs"):
            events.append("EVIDENCE_CANDIDATE")
        if result.get("a_route_execution_ref"):
            events.append("A_ROUTE")
        if result.get("cognitive_proof") is not None:
            events.append("COGNITIVE_STATE")
        return tuple(events)

    def run_binding(
        self,
        binding: Any,
        *,
        observation_cycle_index: int | None = None,
    ) -> GatedOCRExecutionRecordV1:
        raw = binding.request
        source_ref = raw.source_refs[0]
        perception = derive(raw)
        precondition_request = _precondition_request(binding)
        precondition = evaluate(dataclasses.replace(precondition_request, situated_state=perception.situated_state))
        admission = self._admission(precondition)
        pre_events = (
            "SITUATED_STATE_PERCEPTION",
            "SITUATED_FEASIBILITY",
            "SITUATED_OPPORTUNITY",
            "SITUATED_ELIGIBILITY",
        )
        if not admission.provider_execution_admitted:
            return GatedOCRExecutionRecordV1(
                case_id=raw.case_id,
                state_id=raw.state_id,
                execution_mode=EXECUTION_MODE,
                source_ref=source_ref,
                situated_precondition_result=precondition,
                execution_admission=admission,
                execution_events=pre_events + ("PROVIDER_EXECUTION_BLOCKED",),
                runtime_result=None,
                provider_real_execution_attempted=False,
                provider_real_execution_verified=False,
                provider_invoked=False,
                model_invoked=False,
                recorded_provider_result_used=False,
            )

        provider_case = self._provider_case(
            binding,
            source_ref,
            observation_cycle_index=observation_cycle_index,
        )
        # This is the sole real OCR call.  It is intentionally below the gate.
        runtime_result = self.ocr_engine.run(provider_case, source_ref=source_ref)
        errors = tuple(str(item) for item in (runtime_result.get("errors") or ()))
        return GatedOCRExecutionRecordV1(
            case_id=raw.case_id,
            state_id=raw.state_id,
            execution_mode=EXECUTION_MODE,
            source_ref=source_ref,
            situated_precondition_result=precondition,
            execution_admission=admission,
            execution_events=pre_events + ("PROVIDER_EXECUTION_ADMITTED",) + self._events_for_runtime(runtime_result),
            runtime_result=runtime_result,
            provider_real_execution_attempted=bool(runtime_result.get("provider_real_execution_attempted")),
            provider_real_execution_verified=bool(runtime_result.get("provider_real_execution_verified")),
            provider_invoked=bool(runtime_result.get("provider_invoked")),
            model_invoked=bool(runtime_result.get("model_invoked")),
            recorded_provider_result_used=False,
            validation_errors=errors,
        )

    def run_controlled_bindings(self) -> Tuple[GatedOCRExecutionRecordV1, ...]:
        return tuple(self.run_binding(binding) for binding in build_cases_v1(self.repository_root))


def jsonable(value: Any) -> Any:
    return _jsonable(value)


__all__ = [
    "EXECUTION_MODE",
    "PHASE",
    "SituatedEligibilityGatedRealOCRExecutionEngineV1",
    "jsonable",
]
