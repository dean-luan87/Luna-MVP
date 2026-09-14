"""Real YOLO output to existing Situated State condition integration.

The engine deliberately has one provider call site.  It consumes the existing
real YOLO11n Provider Runtime result, derives visual candidates from the native
detection and frame geometry, and then delegates condition assessment to the
canonical Situated State Perception and Situated Capability Preconditions
engines.  It does not invoke OCR or create a second runtime.
"""

from __future__ import annotations

import dataclasses
from dataclasses import replace
from pathlib import Path
from typing import Any, Dict, Iterable, Tuple

from capabilities.evaluation.situated_capability_precondition_cognition_foundation.case_definitions_v1 import (
    ADJUSTMENTS,
    ALL_SUPPORTED_CONDITIONS,
)
from capabilities.midplatform.core.provider_runtime_to_observation_ingress.fixtures_v1 import (
    build_provider_observation_cases_v1,
)
from capabilities.midplatform.core.provider_runtime_to_observation_ingress.real_provider_execution_engine_v1 import (
    RealProviderExecutionEngineV1,
)
from capabilities.midplatform.core.situated_capability_preconditions.minimum_situated_condition_resolution_v1 import (
    PRIMARY_SIGN_TEXT_INFORMATION_NEED,
    resolve_minimum_situated_conditions,
)
from capabilities.midplatform.core.situated_capability_preconditions.situated_capability_precondition_engine_v1 import (
    evaluate,
)
from capabilities.midplatform.core.situated_capability_preconditions.situated_capability_precondition_types_v1 import (
    CapabilityNeedCandidateV1,
    CapabilityPreconditionDefinitionV1,
    SituatedCapabilityPreconditionRequestV1,
)
from capabilities.midplatform.core.situated_capability_preconditions.situated_state_perception_engine_v1 import (
    derive,
)
from capabilities.midplatform.core.situated_capability_preconditions.situated_state_perception_types_v1 import (
    SituatedStatePerceptionRequestV1,
)
from capabilities.midplatform.field_perception_orchestrator.integration.active_observation_precondition_types_v1 import (
    RelativeObservationStateV1,
    SelfPerceptualViewpointStateV1,
)

from .types_v1 import (
    RealVisualSituatedStateSourceV1,
    VisualSituatedCaseResultV1,
    VisualTargetBindingCandidateV1,
)


PHASE = "Phase-P1-Luna-Real-Visual-Situated-State-Source-Integration-v1-001"
EXECUTION_MODE = "LIVE_RUNTIME"
VISUAL_STATE_SOURCE_MODE = "REAL_PROVIDER_DERIVED"
PROVIDER_FAMILY = "yolo"
PROVIDER_REF = "provider:yolo:local:v1"
MODEL_REF = "model-asset:yolo11n:weights-v1"
CAPABILITY_REF = "object_detection"
CAPABILITY_REQUIREMENT_REF = "capability-requirement:object-detection:v1"
TARGET_REQUIREMENT_REF = "target-requirement:visual-detection-candidate:v1"
TARGET_REF = "target:visible-transit-sign:v1"
FIELD_REF = "field:station-signage:v1"
OBSERVATION_REQUIREMENT_REF = "observation-requirement:station-sign:v1"
GOAL_REF = "goal:read-primary-transit-sign:v1"
INTENT_REF = "intent:understand-transit-sign:v1"
CONCERN_REF = "concern:transit-sign-text:v1"


def _unique(values: Iterable[str]) -> Tuple[str, ...]:
    return tuple(dict.fromkeys(str(value) for value in values if str(value).strip()))


def _jsonable(value: Any) -> Any:
    if dataclasses.is_dataclass(value):
        return {key: _jsonable(item) for key, item in dataclasses.asdict(value).items()}
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_jsonable(item) for item in value]
    return value


def _repo_root() -> Path:
    path = Path(__file__).resolve()
    for candidate in (path, *path.parents):
        if all((candidate / marker).exists() for marker in ("capabilities", "docs", "README.md")):
            return candidate
    raise RuntimeError("repository root sentinel not found")


def _detection_fields(provider: Any) -> Tuple[Any, int | None, int | None, Tuple[float, float, float, float] | None]:
    detections = tuple(getattr(provider, "detections", ()) or ())
    if not detections:
        return None, None, None, None
    detection = detections[0]
    dimensions = tuple(getattr(detection, "frame_dimensions", ()) or ())
    bbox = tuple(float(value) for value in (getattr(detection, "bbox", ()) or ()))
    width = int(dimensions[0]) if len(dimensions) == 2 and dimensions[0] > 0 else None
    height = int(dimensions[1]) if len(dimensions) == 2 and dimensions[1] > 0 else None
    normalized_bbox = bbox if len(bbox) == 4 else None
    return detection, width, height, normalized_bbox


def _bbox_inside_frame(
    bbox: Tuple[float, float, float, float] | None,
    width: int | None,
    height: int | None,
) -> bool:
    if bbox is None or width is None or height is None:
        return False
    x1, y1, x2, y2 = bbox
    return 0 <= x1 < x2 <= width and 0 <= y1 < y2 <= height


def _scale_metrics(
    bbox: Tuple[float, float, float, float] | None,
    width: int | None,
    height: int | None,
) -> Dict[str, float]:
    if bbox is None or width is None or height is None:
        return {}
    x1, y1, x2, y2 = bbox
    box_width = max(0.0, x2 - x1)
    box_height = max(0.0, y2 - y1)
    return {
        "width_ratio": box_width / width,
        "height_ratio": box_height / height,
        "area_ratio": (box_width * box_height) / (width * height),
    }


def _visual_definition() -> CapabilityPreconditionDefinitionV1:
    """Reuse the existing text-recognition condition dimensions for E2E proof."""
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


def _visual_request(
    *,
    case_id: str,
    state_id: str,
    source_ref: str,
    runtime_observation_ref: str | None,
    evidence_refs: Tuple[str, ...],
    detection_ref: str | None,
    visibility: str,
    completeness: str,
    scale: str,
) -> SituatedStatePerceptionRequestV1:
    temporal_ref = f"temporal:real-visual:{case_id}:{state_id}"
    self_state = SelfPerceptualViewpointStateV1(
        state_ref=f"self-state:real-visual:{case_id}:{state_id}",
        self_ref="self:luna:v1",
        temporal_ref=temporal_ref,
        orientation_candidate="UNKNOWN",
        motion_state_candidate="UNKNOWN",
        stability_candidate="UNKNOWN",
        current_view_ref=f"view:real-visual:{case_id}:{state_id}",
        visible_region_refs=(TARGET_REF,) if detection_ref else tuple(),
        sensor_availability_candidate="AVAILABLE",
        sensor_availability_refs=("sensor:vision:v1",),
        source_refs=(source_ref,),
        provenance_refs=(f"provenance:real-visual-self:{case_id}:{state_id}",),
    )
    relative = RelativeObservationStateV1(
        relative_state_ref=f"relative-state:real-visual:{case_id}:{state_id}",
        self_state_ref=self_state.state_ref,
        target_ref=TARGET_REF,
        field_ref=FIELD_REF,
        observation_requirement_ref=OBSERVATION_REQUIREMENT_REF,
        temporal_ref=temporal_ref,
        target_visibility_candidate=visibility,
        target_completeness_candidate=completeness,
        target_scale_candidate=scale,
        relative_orientation_candidate="UNKNOWN",
        relative_motion_candidate="UNKNOWN",
        stability_candidate="UNKNOWN",
        occlusion_candidate="UNKNOWN",
        source_refs=(source_ref,),
        provenance_refs=(f"provenance:real-visual-relative:{case_id}:{state_id}",),
    )
    return SituatedStatePerceptionRequestV1(
        case_id=case_id,
        state_id=state_id,
        cycle_index=0,
        temporal_ref=temporal_ref,
        capability_requirement_ref="capability-requirement:text-recognition:v1",
        situated_state_ref=f"situated-capability-state:real-visual:{case_id}:{state_id}",
        self_state=self_state,
        relative_state=relative,
        field_state_refs=(FIELD_REF,),
        target_refs=(TARGET_REF,),
        evidence_refs=evidence_refs,
        source_refs=(source_ref,),
        provenance_refs=(f"provenance:real-visual-source:{case_id}:{state_id}",),
    )


def _precondition_request(raw: SituatedStatePerceptionRequestV1) -> SituatedCapabilityPreconditionRequestV1:
    need = CapabilityNeedCandidateV1(
        capability_need_ref=f"capability-need:real-visual:{raw.case_id}:{raw.state_id}",
        capability_requirement_ref=raw.capability_requirement_ref,
        goal_ref=GOAL_REF,
        intent_ref=INTENT_REF,
        concern_ref=CONCERN_REF,
        information_need_ref=PRIMARY_SIGN_TEXT_INFORMATION_NEED,
        current_cognitive_state_ref=f"cognitive-state:real-visual:{raw.case_id}:{raw.state_id}",
        required_information_refs=(PRIMARY_SIGN_TEXT_INFORMATION_NEED,),
        available_information_refs=tuple(),
        information_gap_refs=(f"information-gap:real-visual:{raw.case_id}:{raw.state_id}",),
        capability_need_active_candidate=True,
        continuation_possible_candidate=False,
        source_refs=(f"controlled:cognitive-context:real-visual:{raw.case_id}:{raw.state_id}",),
        provenance_refs=(f"provenance:cognitive-context:real-visual:{raw.case_id}:{raw.state_id}",),
    )
    definition = _visual_definition()
    minimum = resolve_minimum_situated_conditions(
        capability_definition=definition,
        information_need_ref=need.information_need_ref,
        goal_ref=need.goal_ref,
        intent_ref=need.intent_ref,
        concern_ref=need.concern_ref,
    )
    state = dataclasses.replace(
        # The canonical perception engine owns condition candidates; this
        # placeholder contains no fixture-declared satisfaction.
        derive(raw).situated_state,
        satisfied_condition_refs=tuple(),
        condition_state_refs=tuple(),
    )
    return SituatedCapabilityPreconditionRequestV1(
        case_id=raw.case_id,
        state_id=raw.state_id,
        cycle_index=raw.cycle_index,
        temporal_ref=raw.temporal_ref,
        capability_need=need,
        precondition_definition=definition,
        minimum_condition_requirement=minimum,
        situated_state=state,
        capability_available_candidate=True,
        previous_opportunity_status=None,
        source_refs=raw.source_refs,
        provenance_refs=raw.provenance_refs,
    )


class RealVisualSituatedStateSourceEngineV1:
    """Run one real YOLO call, then derive bounded visual conditions."""

    provider_invocation_authority = "Capability/Provider Runtime"
    provider_family = PROVIDER_FAMILY
    execution_mode = EXECUTION_MODE

    def __init__(self, repository_root: Path) -> None:
        self.repository_root = repository_root
        self.provider_engine = RealProviderExecutionEngineV1(repository_root)

    def _run_provider(self, source_ref: str) -> Dict[str, Any]:
        base_case = build_provider_observation_cases_v1()[0]
        case = replace(
            base_case,
            case_id="REAL_VISUAL_SITUATED_STATE_SOURCE",
            title="real YOLO11n detection supplies visual situated-state candidates",
            execution_instance_ref="provider-runtime:real-visual-situated-state-source:v1",
            input_source_ref=source_ref,
            source_ref=source_ref,
            raw_result_ref="provider-native-output:real-visual-situated-state-source:v1",
        )
        return self.provider_engine.run(
            case,
            source_ref=source_ref,
            model_path=str(self.repository_root / "vision/detection/yolo/yolo11n.pt"),
        )

    def run(self, *, source_ref: str) -> Dict[str, Any]:
        # Sole real provider call site for this phase.  All five cases below
        # reuse this one native result; none of them calls YOLO a second time.
        runtime = self._run_provider(source_ref)
        provider = runtime.get("provider")
        provider_result = runtime.get("provider_result")
        detection, width, height, bbox = _detection_fields(provider)
        detection_ref = getattr(detection, "detection_id", None) if detection else None
        evidence_refs = tuple(runtime.get("evidence_refs") or ())
        runtime_observation_ref = runtime.get("runtime_observation_ref")
        visible = "VISIBLE" if detection is not None else "UNKNOWN"
        complete = "COMPLETE" if _bbox_inside_frame(bbox, width, height) else "UNKNOWN"
        metrics = _scale_metrics(bbox, width, height)
        scale_status = "UNKNOWN"
        stable_status = "UNKNOWN"
        binding = VisualTargetBindingCandidateV1(
            binding_ref="visual-target-binding:real-yolo11n-detection:v1",
            target_requirement_ref=TARGET_REQUIREMENT_REF,
            target_ref=TARGET_REF,
            detection_ref=detection_ref or "",
            source_ref=source_ref,
            semantic_target_resolved=False,
            trace_refs=_unique((runtime_observation_ref or "", *evidence_refs)),
            provenance_refs=("provenance:real-visual-target-binding:v1",),
        )
        source = RealVisualSituatedStateSourceV1(
            source_ref=source_ref,
            runtime_observation_ref=runtime_observation_ref,
            evidence_refs=evidence_refs,
            detection_ref=detection_ref,
            target_binding_ref=binding.binding_ref,
            frame_width=width,
            frame_height=height,
            bbox=bbox,
            target_visibility_candidate=visible,
            target_completeness_candidate=complete,
            target_scale_metrics=metrics,
            target_scale_condition_status=scale_status,
            stable_relation_status=stable_status,
            condition_state_candidate_refs=tuple(),
            trace_refs=_unique((runtime_observation_ref or "", *evidence_refs)),
            provenance_refs=("provenance:real-visual-situated-state-source:v1",),
        )
        raw = _visual_request(
            case_id="REAL_VISUAL_SITUATED_STATE_SOURCE",
            state_id="real-frame-0",
            source_ref=source_ref,
            runtime_observation_ref=runtime_observation_ref,
            evidence_refs=evidence_refs,
            detection_ref=detection_ref,
            visibility=visible,
            completeness=complete,
            scale=scale_status,
        )
        perception = derive(raw)
        precondition = evaluate(replace(_precondition_request(raw), situated_state=perception.situated_state))
        condition_refs = tuple(item.condition_ref for item in perception.condition_candidates)
        source = replace(source, condition_state_candidate_refs=condition_refs)
        cases = (
            VisualSituatedCaseResultV1("REAL_DETECTION_SUPPORTS_TARGET_VISIBLE", source, binding, perception, precondition),
            VisualSituatedCaseResultV1("REAL_BBOX_SUPPORTS_FRAME_COMPLETENESS", source, binding, perception, precondition),
            VisualSituatedCaseResultV1("REAL_VISUAL_SCALE_METRIC_DERIVED", source, binding, perception, precondition),
            VisualSituatedCaseResultV1("SINGLE_FRAME_CANNOT_PROVE_STABLE_RELATION", source, binding, perception, precondition),
            VisualSituatedCaseResultV1("UNKNOWN_CONDITION_FAILS_CLOSED", source, binding, perception, precondition),
        )
        return {
            "phase": PHASE,
            "execution_mode": EXECUTION_MODE,
            "visual_state_source_mode": VISUAL_STATE_SOURCE_MODE,
            "provider_execution_mode": EXECUTION_MODE,
            "selected_provider": PROVIDER_REF,
            "provider_family": PROVIDER_FAMILY,
            "model_ref": MODEL_REF,
            "capability_ref": CAPABILITY_REF,
            "capability_requirement_ref": getattr(
                runtime.get("provider_request"),
                "capability_requirement_ref",
                CAPABILITY_REQUIREMENT_REF,
            ),
            "source_ref": source_ref,
            "provider_real_execution_attempted": bool(runtime.get("provider_real_execution_attempted")),
            "provider_real_execution_verified": bool(runtime.get("provider_real_execution_verified")),
            "provider_invoked": bool(runtime.get("provider_invoked")),
            "model_invoked": bool(runtime.get("model_invoked")),
            "recorded_provider_result_used": False,
            "provider_status": getattr(provider_result, "status", None),
            "provider_request_ref": getattr(runtime.get("provider_request"), "provider_request_ref", None),
            "provider_result_ref": getattr(provider_result, "provider_result_ref", None),
            "runtime_observation_ref": runtime_observation_ref,
            "gateway_admission_ref": runtime.get("gateway_admission_ref"),
            "evidence_refs": list(evidence_refs),
            "frame_dimensions": {"width": source.frame_width, "height": source.frame_height},
            "detection_ref": source.detection_ref,
            "target_binding": binding,
            "target_binding_status": "EVALUATION_CANDIDATE_CANONICAL_OWNER_UNAVAILABLE",
            "visual_source": source,
            "provider_native_result": provider,
            "provider_runtime_result": provider_result,
            "cases": cases,
            "forbidden_behaviors": {
                "provider_invocation": False,
                "model_invocation": False,
                "decision_execution": False,
                "task_execution": False,
                "action_execution": False,
                "device_control": False,
                "camera_control": False,
                "movement_control": False,
                "field_mutation": False,
                "world_truth_declared": False,
            },
            "validation_errors": list(runtime.get("errors") or ()),
            "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
        }


def jsonable(value: Any) -> Any:
    return _jsonable(value)


__all__ = [
    "EXECUTION_MODE",
    "MODEL_REF",
    "PHASE",
    "PROVIDER_REF",
    "RealVisualSituatedStateSourceEngineV1",
    "jsonable",
]
