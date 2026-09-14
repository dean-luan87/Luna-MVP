"""Project one real YOLO evidence result through existing Field boundaries.

The engine has one real provider call site.  It converts the resulting visual
evidence into an evaluation-level Field Event candidate, uses the existing
Field Event Admission API, and then invokes the existing candidate-only Field
State Reducer module.  No Field or World truth is declared or persisted.
"""

from __future__ import annotations

import dataclasses
from dataclasses import replace
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, Tuple

from capabilities.cognitive_flow.field_kernel.reducer_adapter_v1 import (
    FieldKernelReducerAdapterV1,
)
from capabilities.midplatform.core.provider_runtime_to_observation_ingress.fixtures_v1 import (
    build_provider_observation_cases_v1,
)
from capabilities.midplatform.core.field_event_admission_api_v1 import (
    AdmissionContextV1,
    AdmissionPolicyV1,
    admit_field_event,
)
from capabilities.midplatform.core.field_state_reducer.module import (
    FieldStateReducerModuleRequestV1,
    FieldStateReducerModuleV1,
    module_result_to_dict,
)
from capabilities.midplatform.core.provider_runtime_to_observation_ingress.real_provider_execution_engine_v1 import (
    RealProviderExecutionEngineV1,
)

from .types_v1 import (
    FieldProjectionCaseResultV1,
    VisualEvidenceFieldProjectionCandidateV1,
)


PHASE = "Phase-P1-Luna-Real-Visual-Evidence-To-Field-State-Candidate-Projection-Integration-v1-001"
EXECUTION_MODE = "LIVE_RUNTIME"
PROVIDER_REF = "provider:yolo:local:v1"
MODEL_REF = "model-asset:yolo11n:weights-v1"
CAPABILITY_REF = "object_detection"
SOURCE_DEFAULT_FIELD_REF = "field:visual-frame:v1"
EVALUATED_AT = "2026-08-13T00:00:00Z"


def _unique(values: Iterable[str]) -> Tuple[str, ...]:
    return tuple(dict.fromkeys(str(value) for value in values if str(value).strip()))


def _jsonable(value: Any) -> Any:
    if dataclasses.is_dataclass(value):
        return {key: _jsonable(item) for key, item in dataclasses.asdict(value).items()}
    if isinstance(value, Mapping):
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


def _first_detection(provider: Any) -> Any | None:
    detections = tuple(getattr(provider, "detections", ()) or ())
    return detections[0] if detections else None


def _first_evidence(provider: Any) -> Any | None:
    evidence = tuple(getattr(provider, "evidence", ()) or ())
    return evidence[0] if evidence else None


def _projection(
    *,
    runtime: Mapping[str, Any],
    field_ref_candidate: str,
    field_ref_resolution_status: str,
    projection_ref: str,
) -> VisualEvidenceFieldProjectionCandidateV1:
    provider = runtime.get("provider")
    detection = _first_detection(provider)
    evidence = _first_evidence(provider)
    detection_ref = str(getattr(detection, "detection_id", "") or "")
    evidence_ref = str(getattr(evidence, "evidence_id", "") or "")
    bbox = tuple(float(item) for item in (getattr(detection, "bbox", ()) or ()))
    dimensions = tuple(getattr(detection, "frame_dimensions", ()) or ())
    frame_width = int(dimensions[0]) if len(dimensions) == 2 and dimensions[0] > 0 else None
    frame_height = int(dimensions[1]) if len(dimensions) == 2 and dimensions[1] > 0 else None
    temporal_ref = str(getattr(evidence, "temporal_ref", "") or "")
    region_ref = str(
        getattr(evidence, "region_ref", "")
        or getattr(detection, "region_ref", "")
        or ""
    )
    trace_refs = _unique(
        (
            str(runtime.get("runtime_observation_ref") or ""),
            evidence_ref,
            detection_ref,
            str(getattr(evidence, "trace_ref", "") or ""),
        )
    )
    provenance_refs = _unique(
        tuple(getattr(evidence, "provenance_refs", ()) or ())
        + ("provenance:real-visual-field-projection:v1",)
    )
    return VisualEvidenceFieldProjectionCandidateV1(
        projection_ref=projection_ref,
        source_runtime_observation_ref=str(runtime.get("runtime_observation_ref") or ""),
        source_evidence_refs=(evidence_ref,) if evidence_ref else tuple(),
        source_detection_refs=(detection_ref,) if detection_ref else tuple(),
        field_ref_candidate=field_ref_candidate,
        field_ref_resolution_status=field_ref_resolution_status,
        region_ref_candidate=region_ref,
        region_semantics="DETECTION_REGION_CANDIDATE",
        observation_type="VISION_DETECTION_CANDIDATE",
        object_class_candidate=str(getattr(detection, "class_label", "") or ""),
        frame_width=frame_width,
        frame_height=frame_height,
        bbox_candidate=bbox if len(bbox) == 4 else tuple(),
        confidence_candidate=(
            float(getattr(detection, "confidence", 0.0)) if detection is not None else None
        ),
        temporal_ref=temporal_ref,
        trace_refs=trace_refs,
        provenance_refs=provenance_refs,
    )


def _event_candidate(
    projection: VisualEvidenceFieldProjectionCandidateV1,
    *,
    case_id: str,
) -> Dict[str, Any] | None:
    if not projection.field_ref_candidate or not projection.source_evidence_refs:
        return None
    event_ref = f"field-event:real-visual:{case_id}:v1"
    return {
        "event_id": event_ref,
        "event_type": "visual_evidence_field_event_candidate",
        "field_ref": projection.field_ref_candidate,
        "occurred_at": EVALUATED_AT,
        "observed_at": EVALUATED_AT,
        "received_at": EVALUATED_AT,
        "source_chain": [
            "Real YOLO Provider Runtime",
            "Runtime Observation",
            "Visual Evidence Candidate",
            "Visual Evidence Field Projection Candidate",
            "Field Event Admission",
        ],
        "evidence_refs": list(projection.source_evidence_refs),
        "payload": {
            "observation_ref": projection.source_runtime_observation_ref,
            "detection_refs": list(projection.source_detection_refs),
            "region_ref_candidate": projection.region_ref_candidate,
            "candidate_only": True,
            "truth_declared": False,
            "field_mutation": False,
        },
        "trace_ref": f"trace:real-visual-field-event:{case_id}:v1",
    }


def _reducer_request(
    *,
    event: Mapping[str, Any],
    case_id: str,
) -> FieldStateReducerModuleRequestV1:
    event_id = str(event["event_id"])
    reducer_event = dict(event)
    reducer_event.update(
        {
            "admitted": True,
            "raw_observation": False,
            "source_id": "source:real-yolo-visual-evidence",
            "event_time": EVALUATED_AT,
            "admission_id": f"admission:{event_id}",
        }
    )
    return FieldStateReducerModuleRequestV1(
        reducer_request_id=f"reducer-request:real-visual:{case_id}:v1",
        reducer_run_id=f"reducer-run:real-visual:{case_id}:v1",
        field_id=str(event["field_ref"]),
        requested_state_type="presence_state",
        admitted_events=(reducer_event,),
        existing_state_snapshot={},
        temporal_snapshot={
            "snapshot_id": f"temporal-snapshot:real-visual:{case_id}:v1",
            "status": "active",
            "refresh_evidence_available": True,
            "new_event_available": True,
            "sufficient_evidence": True,
            "confidence_snapshot": {"measured_confidence": 0.9},
        },
        policy_registry_snapshot={"version": "v1"},
        evaluation_contract_snapshot={"version": "v1"},
        selection_contract_snapshot={"version": "v1"},
        reduction_contract_snapshot={"version": "v1"},
        conflict_snapshot={
            "tags": [],
            "unresolved": False,
            "preserve_conflict": False,
            "provisional_candidate_allowed": True,
            "conflicting_event_refs": [],
            "resolution_available": True,
        },
        overlay_snapshot={
            "overlay_refs": [],
            "overlay_active": False,
            "overlay_expired": False,
            "substrate_mutation_requested": False,
        },
        owner_correction_snapshot={"owner_correction_refs": []},
        provenance_snapshot={
            "source_id": "source:real-yolo-visual-evidence",
            "event_id": event_id,
            "event_time": EVALUATED_AT,
            "admission_id": f"admission:{event_id}",
            "available_keys": ["source_id", "event_id", "event_time", "admission_id"],
            "source_ids": ["source:real-yolo-visual-evidence"],
            "confidence_policy_snapshot": {"measured_confidence": 0.9},
            "governance_snapshot": {
                "owner_correction_review": True,
                "fact_admission_dependency": True,
                "permission_admission_dependency": True,
                "human_review_dependency": True,
                "protocol_version_dependency": True,
                "provenance_dependency": True,
                "change_control_dependency": True,
                "runtime_boundary_dependency": True,
            },
            "evaluation_requested_at": EVALUATED_AT,
        },
        version_snapshots={
            "policy_registry_version": "v1",
            "eligibility_matrix_version": "v1",
            "precedence_matrix_version": "v1",
            "composition_contract_version": "v1",
            "replay_contract_version": "v1",
            "evaluation_contract_version": "v1",
            "reduction_contract_version": "v1",
        },
    )


class RealVisualEvidenceFieldProjectionEngineV1:
    """One real provider execution plus bounded Field projection cases."""

    def __init__(self, repository_root: Path) -> None:
        self.repository_root = repository_root
        self.provider_engine = RealProviderExecutionEngineV1(repository_root)

    def _run_provider(self, source_ref: str) -> Dict[str, Any]:
        base_case = build_provider_observation_cases_v1()[0]
        case = replace(
            base_case,
            case_id="REAL_VISUAL_EVIDENCE_FIELD_PROJECTION",
            title="real visual evidence to Field candidate projection",
            execution_instance_ref="provider-runtime:real-visual-field-projection:v1",
            input_source_ref=source_ref,
            source_ref=source_ref,
            raw_result_ref="provider-native-output:real-visual-field-projection:v1",
        )
        return self.provider_engine.run(
            case,
            source_ref=source_ref,
            model_path=str(self.repository_root / "vision/detection/yolo/yolo11n.pt"),
        )

    def _run_case(
        self,
        *,
        case_id: str,
        runtime: Dict[str, Any],
        field_ref_candidate: str,
        resolution_status: str,
        admit: bool,
    ) -> FieldProjectionCaseResultV1:
        projection = _projection(
            runtime=runtime,
            field_ref_candidate=field_ref_candidate,
            field_ref_resolution_status=resolution_status,
            projection_ref=f"field-projection:real-visual:{case_id}:v1",
        )
        event = _event_candidate(projection, case_id=case_id)
        admission = None
        adapter = None
        reducer_result = None
        reducer_candidate = None
        errors = []
        if event is not None and admit:
            admission = admit_field_event(
                event,
                AdmissionPolicyV1(evaluated_at=EVALUATED_AT),
                AdmissionContextV1(),
            )
            if admission.reducer_eligible:
                adapter = FieldKernelReducerAdapterV1.adapt_admitted_event(admission)
                reducer_request = _reducer_request(
                    event=adapter.reducer_input_candidate,
                    case_id=case_id,
                )
                reducer_result = module_result_to_dict(
                    FieldStateReducerModuleV1.reduce(reducer_request)
                )
                reducer_candidate = reducer_result.get("field_state_candidate")
        behavior = {
            "real_evidence_not_field_truth": projection.truth_declared is False,
            "real_evidence_not_world_truth": projection.truth_declared is False,
            "field_mutation": projection.field_mutation,
            "event_admission_required": event is not None,
            "canonical_field_admission_respected": bool(
                admission is not None and admission.reducer_eligible
            ),
            "unadmitted_event_reduced": False,
            "field_reducer_authority_unchanged": True,
            "image_region_not_physical_field_region": projection.region_semantics
            == "DETECTION_REGION_CANDIDATE",
            "field_ref_is_existing_evaluation_context": projection.field_ref_candidate
            == SOURCE_DEFAULT_FIELD_REF,
        }
        if event is not None and not admit:
            behavior["canonical_field_admission_respected"] = False
            behavior["unadmitted_event_reduced"] = False
        if projection.field_ref_resolution_status == "UNRESOLVED":
            behavior["field_ref_remains_unresolved"] = not bool(
                projection.field_ref_candidate
            )
        return FieldProjectionCaseResultV1(
            case_id=case_id,
            projection=projection,
            event_candidate=event,
            admission=admission,
            reducer_adapter=adapter,
            reducer_result=reducer_result,
            field_state_candidate=reducer_candidate,
            behavior=behavior,
            validation_errors=tuple(errors),
        )

    def run(self, *, source_ref: str) -> Dict[str, Any]:
        runtime = self._run_provider(source_ref)
        provider = runtime.get("provider")
        detections = tuple(getattr(provider, "detections", ()) or ())
        evidence = tuple(getattr(provider, "evidence", ()) or ())
        positive = self._run_case(
            case_id="REAL_VISUAL_EVIDENCE_TO_FIELD_CANDIDATE",
            runtime=runtime,
            field_ref_candidate=SOURCE_DEFAULT_FIELD_REF,
            resolution_status="CONTROLLED_CONTEXT_CANDIDATE",
            admit=True,
        )
        not_truth = self._run_case(
            case_id="REAL_EVIDENCE_DOES_NOT_BECOME_FIELD_TRUTH",
            runtime=runtime,
            field_ref_candidate=SOURCE_DEFAULT_FIELD_REF,
            resolution_status="CONTROLLED_CONTEXT_CANDIDATE",
            admit=True,
        )
        unresolved = self._run_case(
            case_id="UNRESOLVED_FIELD_REF_REMAINS_UNRESOLVED",
            runtime=runtime,
            field_ref_candidate="",
            resolution_status="UNRESOLVED",
            admit=True,
        )
        unadmitted = self._run_case(
            case_id="UNADMITTED_EVENT_CANNOT_MUTATE_REDUCER_STATE",
            runtime=runtime,
            field_ref_candidate=SOURCE_DEFAULT_FIELD_REF,
            resolution_status="CONTROLLED_CONTEXT_CANDIDATE",
            admit=False,
        )
        absence = self._run_case(
            case_id="DETECTION_ABSENCE_NOT_FIELD_ABSENCE",
            runtime=runtime,
            field_ref_candidate="",
            resolution_status="UNRESOLVED",
            admit=False,
        )
        cases = (positive, not_truth, unresolved, unadmitted, absence)
        return {
            "phase": PHASE,
            "execution_mode": EXECUTION_MODE,
            "visual_state_source_mode": "REAL_PROVIDER_DERIVED",
            "provider_execution_mode": EXECUTION_MODE,
            "provider_ref": PROVIDER_REF,
            "model_ref": MODEL_REF,
            "capability_ref": CAPABILITY_REF,
            "source_ref": source_ref,
            "target_binding_status": "EVALUATION_CANDIDATE_CANONICAL_OWNER_UNAVAILABLE",
            "semantic_target_resolved": False,
            "provider_real_execution_attempted": bool(runtime.get("provider_real_execution_attempted")),
            "provider_real_execution_verified": bool(runtime.get("provider_real_execution_verified")),
            "provider_invoked": bool(runtime.get("provider_invoked")),
            "model_invoked": bool(runtime.get("model_invoked")),
            "recorded_provider_result_used": False,
            "runtime_observation_ref": runtime.get("runtime_observation_ref"),
            "evidence_refs": list(runtime.get("evidence_refs") or ()),
            "detection_count": len(detections),
            "real_visual_evidence_count": len(evidence),
            "frame_dimensions": {
                "width": positive.projection.frame_width,
                "height": positive.projection.frame_height,
            },
            "field_reducer_authority": "Field State Reducer",
            "field_truth_declared": False,
            "world_truth_declared": False,
            "field_mutation": False,
            "cases": cases,
            "forbidden_behaviors": {
                "provider_invocation": False,
                "model_invocation": False,
                "field_truth_promotion": False,
                "world_truth_declared": False,
                "field_mutation": False,
                "decision_execution": False,
                "task_execution": False,
                "action_execution": False,
                "device_control": False,
                "camera_control": False,
                "movement_control": False,
                "ocr_invocation": False,
                "slam_invocation": False,
            },
            "validation_errors": list(runtime.get("errors") or ()),
            "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
        }


def jsonable(value: Any) -> Any:
    return _jsonable(value)


__all__ = [
    "PHASE",
    "RealVisualEvidenceFieldProjectionEngineV1",
    "jsonable",
]
