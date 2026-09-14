"""Two-call real YOLO projection into temporal visual relation candidates.

The repository has local multi-image assets, but their manifest identifies
different street scenes rather than a continuous sequence.  This phase uses a
deterministic image-derived fallback frame and marks that boundary explicitly.
The YOLO Provider Runtime is still called twice on two local image inputs; no
tracking, identity resolution, OCR, SLAM, or action runtime is introduced.
"""

from __future__ import annotations

import dataclasses
import math
from dataclasses import replace
from pathlib import Path
from typing import Any, Dict, Iterable, Optional, Tuple

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
from capabilities.evaluation.situated_capability_precondition_cognition_foundation.case_definitions_v1 import (
    ADJUSTMENTS,
    ALL_SUPPORTED_CONDITIONS,
)

from .types_v1 import (
    CrossFrameTargetAssociationCandidateV1,
    MultiFrameVisualObservationV1,
    TemporalVisualRelationMetricsV1,
    VisualRelationStabilityCandidateV1,
)


PHASE = "Phase-P1-Luna-Real-MultiFrame-Visual-Situated-State-Integration-v1-001"
EXECUTION_MODE = "LIVE_RUNTIME"
MULTIFRAME_SOURCE_MODE = "CONTROLLED_TEMPORAL_VISUAL_TRANSITION"
PROVIDER_REF = "provider:yolo:local:v1"
MODEL_REF = "model-asset:yolo11n:weights-v1"
MODEL_PATH = "vision/detection/yolo/yolo11n.pt"
SOURCE_IMAGE = "_tmp_eval_inputs/roboflow_real_exit_v1/source_image.jpg"
FRAME_A_REF = "frame:real-multiframe:source-a:v1"
FRAME_B_REF = "frame:real-multiframe:controlled-transform-b:v1"


def _repo_root() -> Path:
    path = Path(__file__).resolve()
    for candidate in (path, *path.parents):
        if all((candidate / marker).exists() for marker in ("capabilities", "docs", "README.md")):
            return candidate
    raise RuntimeError("repository root sentinel not found")


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


def _controlled_transform(source_ref: str, destination: Path) -> str:
    """Create a clearly labelled derived frame from an existing local image."""
    from PIL import Image

    destination.parent.mkdir(parents=True, exist_ok=True)
    image = Image.open(source_ref)
    transpose = getattr(getattr(Image, "Transpose", Image), "FLIP_LEFT_RIGHT")
    image.transpose(transpose).save(destination)
    return str(destination)


def _frame_observation(
    runtime: Dict[str, Any],
    *,
    frame_ref: str,
    source_ref: str,
) -> MultiFrameVisualObservationV1:
    provider = runtime.get("provider")
    detection = tuple(getattr(provider, "detections", ()) or ())[:1]
    item = detection[0] if detection else None
    dimensions = tuple(getattr(item, "frame_dimensions", ()) or ()) if item else tuple()
    bbox_raw = tuple(float(value) for value in (getattr(item, "bbox", ()) or ())) if item else tuple()
    return MultiFrameVisualObservationV1(
        frame_ref=frame_ref,
        source_ref=source_ref,
        runtime_observation_ref=runtime.get("runtime_observation_ref"),
        provider_request_ref=getattr(runtime.get("provider_request"), "provider_request_ref", None),
        provider_result_ref=getattr(runtime.get("provider_result"), "provider_result_ref", None),
        temporal_ref=getattr(runtime.get("provider_request"), "temporal_ref", None),
        detection_ref=getattr(item, "detection_id", None) if item else None,
        class_label=getattr(item, "class_label", None) if item else None,
        confidence=getattr(item, "confidence", None) if item else None,
        frame_width=int(dimensions[0]) if len(dimensions) == 2 else None,
        frame_height=int(dimensions[1]) if len(dimensions) == 2 else None,
        bbox=bbox_raw if len(bbox_raw) == 4 else None,
        trace_refs=_unique(
            (
                runtime.get("runtime_observation_ref") or "",
                getattr(runtime.get("provider_request"), "provider_request_ref", ""),
            )
        ),
        provenance_refs=_unique((getattr(runtime.get("provider_result"), "provider_result_ref", ""),)),
    )


def _bbox_geometry(frame: MultiFrameVisualObservationV1) -> Optional[Dict[str, Any]]:
    if not frame.bbox or not frame.frame_width or not frame.frame_height:
        return None
    x1, y1, x2, y2 = frame.bbox
    width = float(frame.frame_width)
    height = float(frame.frame_height)
    box_width = x2 - x1
    box_height = y2 - y1
    center = ((x1 + x2) / 2.0, (y1 + y2) / 2.0)
    return {
        "center": center,
        "normalized_center": (center[0] / width, center[1] / height),
        "normalized_size": (box_width / width, box_height / height),
        "area_ratio": (box_width * box_height) / (width * height),
    }


def _visual_definition() -> CapabilityPreconditionDefinitionV1:
    return CapabilityPreconditionDefinitionV1(
        capability_requirement_ref="capability-requirement:text-recognition:v1",
        capability_ref="text_recognition",
        supported_condition_refs=ALL_SUPPORTED_CONDITIONS,
        optional_condition_refs=tuple(),
        adjustment_by_condition_ref=ADJUSTMENTS,
        source_refs=("capabilities/registry/luna_capability_registry_v1.json",),
        provenance_refs=("provenance:capability-definition:text-recognition:v1",),
    )


def _situated_state_request(frame: MultiFrameVisualObservationV1) -> SituatedStatePerceptionRequestV1:
    visibility = "VISIBLE" if frame.detection_ref else "UNKNOWN"
    complete = "COMPLETE" if frame.bbox and frame.frame_width and frame.frame_height and 0 <= frame.bbox[0] < frame.bbox[2] <= frame.frame_width and 0 <= frame.bbox[1] < frame.bbox[3] <= frame.frame_height else "UNKNOWN"
    temporal_ref = frame.temporal_ref or f"temporal:real-multiframe:{frame.frame_ref}"
    self_state = SelfPerceptualViewpointStateV1(
        state_ref=f"self-state:real-multiframe:{frame.frame_ref}",
        self_ref="self:luna:v1",
        temporal_ref=temporal_ref,
        orientation_candidate="UNKNOWN",
        motion_state_candidate="UNKNOWN",
        stability_candidate="UNKNOWN",
        current_view_ref=f"view:real-multiframe:{frame.frame_ref}",
        visible_region_refs=("target:visual-detection-candidate:v1",) if frame.detection_ref else tuple(),
        sensor_availability_candidate="AVAILABLE",
        sensor_availability_refs=("sensor:vision:v1",),
        source_refs=(frame.source_ref,),
        provenance_refs=(f"provenance:real-multiframe:self:{frame.frame_ref}",),
    )
    relative = RelativeObservationStateV1(
        relative_state_ref=f"relative-state:real-multiframe:{frame.frame_ref}",
        self_state_ref=self_state.state_ref,
        target_ref="target:visual-detection-candidate:v1",
        field_ref="field:visual-frame:v1",
        observation_requirement_ref="observation-requirement:visual-detection:v1",
        temporal_ref=temporal_ref,
        target_visibility_candidate=visibility,
        target_completeness_candidate=complete,
        target_scale_candidate="UNKNOWN",
        relative_orientation_candidate="UNKNOWN",
        relative_motion_candidate="UNKNOWN",
        stability_candidate="UNKNOWN",
        occlusion_candidate="UNKNOWN",
        source_refs=(frame.source_ref, frame.frame_ref),
        provenance_refs=(f"provenance:real-multiframe:relative:{frame.frame_ref}",),
    )
    return SituatedStatePerceptionRequestV1(
        case_id="REAL_MULTIFRAME_VISUAL_SITUATED_STATE",
        state_id=frame.frame_ref,
        cycle_index=0,
        temporal_ref=temporal_ref,
        capability_requirement_ref="capability-requirement:text-recognition:v1",
        situated_state_ref=f"situated-capability-state:real-multiframe:{frame.frame_ref}",
        self_state=self_state,
        relative_state=relative,
        field_state_refs=("field:visual-frame:v1",),
        target_refs=("target:visual-detection-candidate:v1",),
        evidence_refs=(frame.detection_ref,) if frame.detection_ref else tuple(),
        source_refs=(frame.source_ref,),
        provenance_refs=(f"provenance:real-multiframe:source:{frame.frame_ref}",),
    )


def _precondition(frame: MultiFrameVisualObservationV1) -> Any:
    raw = _situated_state_request(frame)
    definition = _visual_definition()
    need = CapabilityNeedCandidateV1(
        capability_need_ref=f"capability-need:real-multiframe:{frame.frame_ref}",
        capability_requirement_ref=raw.capability_requirement_ref,
        goal_ref="goal:read-primary-transit-sign:v1",
        intent_ref="intent:understand-transit-sign:v1",
        concern_ref="concern:transit-sign-text:v1",
        information_need_ref=PRIMARY_SIGN_TEXT_INFORMATION_NEED,
        current_cognitive_state_ref=f"cognitive-state:real-multiframe:{frame.frame_ref}",
        required_information_refs=(PRIMARY_SIGN_TEXT_INFORMATION_NEED,),
        available_information_refs=tuple(),
        information_gap_refs=(f"information-gap:real-multiframe:{frame.frame_ref}",),
        capability_need_active_candidate=True,
        continuation_possible_candidate=False,
        source_refs=(f"controlled:cognitive-context:real-multiframe:{frame.frame_ref}",),
        provenance_refs=(f"provenance:cognitive-context:real-multiframe:{frame.frame_ref}",),
    )
    minimum = resolve_minimum_situated_conditions(
        capability_definition=definition,
        information_need_ref=need.information_need_ref,
        goal_ref=need.goal_ref,
        intent_ref=need.intent_ref,
        concern_ref=need.concern_ref,
    )
    precondition_request = SituatedCapabilityPreconditionRequestV1(
        case_id=raw.case_id,
        state_id=raw.state_id,
        cycle_index=raw.cycle_index,
        temporal_ref=raw.temporal_ref,
        capability_need=need,
        precondition_definition=definition,
        minimum_condition_requirement=minimum,
        situated_state=derive(raw).situated_state,
        capability_available_candidate=True,
        previous_opportunity_status=None,
        source_refs=raw.source_refs,
        provenance_refs=raw.provenance_refs,
    )
    return evaluate(precondition_request)


class RealMultiFrameVisualSituatedStateEngineV1:
    """Invoke the existing real YOLO runtime twice and compare candidates."""

    def __init__(self, repository_root: Path) -> None:
        self.repository_root = repository_root
        self.provider_engine = RealProviderExecutionEngineV1(repository_root)

    def _run_frame(self, source_ref: str, frame_ref: str, suffix: str) -> Dict[str, Any]:
        case = replace(
            build_provider_observation_cases_v1()[0],
            case_id=f"REAL_MULTIFRAME_VISUAL_{suffix.upper()}",
            title=f"real YOLO11n visual observation {suffix}",
            execution_instance_ref=f"provider-runtime:real-multiframe:{suffix}:v1",
            input_source_ref=source_ref,
            source_ref=source_ref,
            raw_result_ref=f"provider-native-output:real-multiframe:{suffix}:v1",
            temporal_ref=f"temporal:real-multiframe:{suffix}:v1",
        )
        return self.provider_engine.run(
            case,
            source_ref=source_ref,
            model_path=str(self.repository_root / MODEL_PATH),
        )

    def run(self, *, source_ref: str) -> Dict[str, Any]:
        transformed_ref = _controlled_transform(
            source_ref,
            self.repository_root / "_eval_out/real_multiframe_visual_situated_state_integration_v1/controlled_frame_b.png",
        )
        runtime_a = self._run_frame(source_ref, FRAME_A_REF, "a")
        runtime_b = self._run_frame(transformed_ref, FRAME_B_REF, "b")
        frame_a = _frame_observation(runtime_a, frame_ref=FRAME_A_REF, source_ref=source_ref)
        frame_b = _frame_observation(runtime_b, frame_ref=FRAME_B_REF, source_ref=transformed_ref)
        geometry_a = _bbox_geometry(frame_a)
        geometry_b = _bbox_geometry(frame_b)
        metric_values = None
        if geometry_a and geometry_b:
            delta_center = tuple(geometry_b["normalized_center"][index] - geometry_a["normalized_center"][index] for index in (0, 1))
            delta_size = tuple(geometry_b["normalized_size"][index] - geometry_a["normalized_size"][index] for index in (0, 1))
            metric_values = TemporalVisualRelationMetricsV1(
                metrics_ref="temporal-visual-relation-metrics:real-multiframe:v1",
                frame_a_ref=frame_a.frame_ref,
                frame_b_ref=frame_b.frame_ref,
                normalized_center_a=geometry_a["normalized_center"],
                normalized_center_b=geometry_b["normalized_center"],
                normalized_size_a=geometry_a["normalized_size"],
                normalized_size_b=geometry_b["normalized_size"],
                area_ratio_a=geometry_a["area_ratio"],
                area_ratio_b=geometry_b["area_ratio"],
                delta_center=delta_center,
                delta_center_distance=math.sqrt(delta_center[0] ** 2 + delta_center[1] ** 2),
                delta_size=delta_size,
                delta_area=geometry_b["area_ratio"] - geometry_a["area_ratio"],
                temporal_refs=tuple(ref for ref in (frame_a.temporal_ref, frame_b.temporal_ref) if ref),
                trace_refs=_unique((*frame_a.trace_refs, *frame_b.trace_refs)),
                provenance_refs=_unique((*frame_a.provenance_refs, *frame_b.provenance_refs)),
            )
        association = CrossFrameTargetAssociationCandidateV1(
            association_ref="cross-frame-target-association:real-multiframe:v1",
            frame_a_ref=frame_a.frame_ref,
            frame_b_ref=frame_b.frame_ref,
            detection_a_ref=frame_a.detection_ref or "",
            detection_b_ref=frame_b.detection_ref or "",
            association_basis=("class_compatibility_candidate", "bbox_geometry_candidate", "controlled_target_binding"),
            association_confidence_candidate=None,
            semantic_identity_resolved=False,
            physical_identity_declared=False,
            trace_refs=_unique((*frame_a.trace_refs, *frame_b.trace_refs)),
            provenance_refs=("provenance:cross-frame-association:real-multiframe:v1",),
        )
        stability = VisualRelationStabilityCandidateV1(
            stability_ref="visual-relation-stability:real-multiframe:v1",
            association_ref=association.association_ref,
            metrics_ref=metric_values.metrics_ref if metric_values else "",
            status="UNKNOWN",
            threshold_ref=None,
            reason="no canonical temporal stability threshold; visual metrics remain candidates only",
            trace_refs=_unique((*association.trace_refs, *(metric_values.trace_refs if metric_values else ()))),
            provenance_refs=("provenance:visual-relation-stability:real-multiframe:v1",),
        )
        preconditions = (_precondition(frame_a), _precondition(frame_b))
        return {
            "phase": PHASE,
            "execution_mode": EXECUTION_MODE,
            "multiframe_source_mode": MULTIFRAME_SOURCE_MODE,
            "real_multiframe_asset_gap": True,
            "source_refs": (source_ref, transformed_ref),
            "provider_ref": PROVIDER_REF,
            "model_ref": MODEL_REF,
            "provider_invocation_count": sum(bool(item.get("provider_invoked")) for item in (runtime_a, runtime_b)),
            "model_invocation_count": sum(bool(item.get("model_invoked")) for item in (runtime_a, runtime_b)),
            "recorded_provider_result_used": False,
            "observations": (frame_a, frame_b),
            "association": association,
            "temporal_metrics": metric_values,
            "stability": stability,
            "precondition_results": preconditions,
            "stability_threshold_defined": False,
            "stability_threshold_ref": None,
            "provider_native_results": (runtime_a.get("provider"), runtime_b.get("provider")),
            "provider_runtime_results": (runtime_a.get("provider_result"), runtime_b.get("provider_result")),
            "runtime_validation_errors": tuple((*runtime_a.get("errors", ()), *runtime_b.get("errors", ()))),
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
                "ocr_invocation": False,
                "slam_invocation": False,
            },
            "validation_errors": tuple(),
            "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
        }


def jsonable(value: Any) -> Any:
    return _jsonable(value)


__all__ = ["EXECUTION_MODE", "PHASE", "RealMultiFrameVisualSituatedStateEngineV1", "jsonable"]
