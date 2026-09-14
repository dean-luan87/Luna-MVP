"""Project real visual evidence into the canonical Field observation event boundary.

This layer reuses the previous real-YOLO integration and the existing Field
Admission/Reducer owners.  It only changes the event's semantic vocabulary;
it does not promote a detection to a Field or World fact.
"""

from __future__ import annotations

import dataclasses
from pathlib import Path
from typing import Any, Dict, Mapping

from capabilities.cognitive_flow.field_kernel.reducer_adapter_v1 import (
    FieldKernelReducerAdapterV1,
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

from capabilities.evaluation.real_visual_evidence_to_field_state_candidate_projection.engine_v1 import (
    EVALUATED_AT,
    SOURCE_DEFAULT_FIELD_REF,
    RealVisualEvidenceFieldProjectionEngineV1,
    _projection,
    _repo_root,
)

from .types_v1 import (
    CanonicalFieldSemanticEventProjectionCandidateV1,
    CanonicalSemanticEventCaseResultV1,
)


PHASE = "Phase-P1-Luna-Real-Visual-Evidence-To-Canonical-Field-Semantic-Event-Integration-v1-001"
EXECUTION_MODE = "LIVE_RUNTIME"
CANONICAL_EVENT_TYPE = "field_definition_observed"
STATE_TYPE = "presence_state"
PERSPECTIVE_SCOPE = "luna:visual-observation-candidate"
TARGET_TYPE = "field_definition"
EVIDENCE_MINIMUM_EVENT_COUNT = 2
EVIDENCE_SOURCE_DIVERSITY_REQUIREMENT = 2


def _jsonable(value: Any) -> Any:
    if dataclasses.is_dataclass(value):
        return {
            key: _jsonable(item)
            for key, item in dataclasses.asdict(value).items()
        }
    if isinstance(value, Mapping):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_jsonable(item) for item in value]
    return value


def _semantic_projection(
    visual_projection: Any,
    *,
    case_id: str,
) -> CanonicalFieldSemanticEventProjectionCandidateV1:
    projection_ref = (
        f"field-semantic-projection:real-visual:{case_id}:v1"
    )
    trace_refs = tuple(
        dict.fromkeys(
            (
                *tuple(visual_projection.trace_refs),
                projection_ref,
            )
        )
    )
    provenance_refs = tuple(
        dict.fromkeys(
            (
                *tuple(visual_projection.provenance_refs),
                "provenance:real-visual-canonical-field-semantic-event:v1",
            )
        )
    )
    return CanonicalFieldSemanticEventProjectionCandidateV1(
        projection_ref=projection_ref,
        source_visual_projection_ref=visual_projection.projection_ref,
        source_runtime_observation_ref=(
            visual_projection.source_runtime_observation_ref
        ),
        source_evidence_refs=tuple(visual_projection.source_evidence_refs),
        source_detection_refs=tuple(visual_projection.source_detection_refs),
        canonical_event_type=CANONICAL_EVENT_TYPE,
        field_ref_candidate=visual_projection.field_ref_candidate,
        field_ref_resolution_status=visual_projection.field_ref_resolution_status,
        state_type=STATE_TYPE,
        perspective_scope=PERSPECTIVE_SCOPE,
        field_scope=visual_projection.field_ref_candidate,
        target_type=TARGET_TYPE,
        subject_ref_candidate=None,
        semantic_state_resolution_status="UNRESOLVED",
        semantic_value_candidate=None,
        observed_object_class_candidate=visual_projection.object_class_candidate,
        confidence_candidate=visual_projection.confidence_candidate,
        temporal_ref=visual_projection.temporal_ref,
        trace_refs=trace_refs,
        provenance_refs=provenance_refs,
    )


def _semantic_event(
    projection: CanonicalFieldSemanticEventProjectionCandidateV1,
    *,
    case_id: str,
) -> Dict[str, Any]:
    event_id = f"field-semantic-event:real-visual:{case_id}:v1"
    return {
        "event_id": event_id,
        "event_type": projection.canonical_event_type,
        "field_ref": projection.field_ref_candidate,
        "occurred_at": EVALUATED_AT,
        "observed_at": EVALUATED_AT,
        "received_at": EVALUATED_AT,
        "source_chain": [
            "Real YOLO Provider Runtime",
            "Runtime Observation",
            "Visual Evidence Candidate",
            "VisualEvidenceFieldProjectionCandidateV1",
            "Canonical Field Semantic Event Projection",
            "Field Event Admission",
        ],
        "evidence_refs": list(projection.source_evidence_refs),
        "payload": {
            "perspective_scope": projection.perspective_scope,
            "field_scope": projection.field_scope,
            "target_type": projection.target_type,
            "subject_ref_candidate": projection.subject_ref_candidate,
            "state_type": projection.state_type,
            "semantic_state_resolution_status": (
                projection.semantic_state_resolution_status
            ),
            "semantic_value_candidate": projection.semantic_value_candidate,
            "observed_object_class_candidate": (
                projection.observed_object_class_candidate
            ),
            "source_visual_projection_ref": (
                projection.source_visual_projection_ref
            ),
            "runtime_observation_ref": projection.source_runtime_observation_ref,
            "detection_refs": list(projection.source_detection_refs),
            "confidence_candidate": projection.confidence_candidate,
            "candidate_only": True,
            "fact_admitted": False,
            "truth_declared": False,
            "field_mutation": False,
        },
        "trace_ref": f"trace:real-visual-semantic-event:{case_id}:v1",
    }


def _reducer_request(
    *,
    event: Mapping[str, Any],
    confidence: float | None,
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
    confidence_snapshot = {"measured_confidence": confidence}
    return FieldStateReducerModuleRequestV1(
        reducer_request_id=(
            f"reducer-request:real-visual-semantic:{case_id}:v1"
        ),
        reducer_run_id=f"reducer-run:real-visual-semantic:{case_id}:v1",
        field_id=str(event["field_ref"]),
        requested_state_type=STATE_TYPE,
        admitted_events=(reducer_event,),
        existing_state_snapshot={},
        temporal_snapshot={
            "snapshot_id": f"temporal-snapshot:real-visual-semantic:{case_id}:v1",
            "status": "active",
            "refresh_evidence_available": True,
            "new_event_available": True,
            "sufficient_evidence": True,
            "confidence_snapshot": confidence_snapshot,
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
            "confidence_policy_snapshot": confidence_snapshot,
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


class RealVisualEvidenceCanonicalFieldSemanticEventEngineV1:
    """Reuse one real YOLO execution and project it to canonical observation semantics."""

    def __init__(self, repository_root: Path) -> None:
        self.repository_root = repository_root
        self.visual_engine = RealVisualEvidenceFieldProjectionEngineV1(
            repository_root
        )

    def _case(
        self,
        *,
        case_id: str,
        runtime: Dict[str, Any],
        field_ref_candidate: str = SOURCE_DEFAULT_FIELD_REF,
        field_ref_resolution_status: str = "CONTROLLED_CONTEXT_CANDIDATE",
        run_reducer: bool = True,
    ) -> CanonicalSemanticEventCaseResultV1:
        visual_projection = _projection(
            runtime=runtime,
            field_ref_candidate=field_ref_candidate,
            field_ref_resolution_status=field_ref_resolution_status,
            projection_ref=f"field-projection:real-visual:{case_id}:v1",
        )
        semantic_projection = _semantic_projection(
            visual_projection,
            case_id=case_id,
        )
        event = _semantic_event(semantic_projection, case_id=case_id)
        admission = None
        reducer_result = None
        if field_ref_candidate and run_reducer:
            admission = admit_field_event(
                event,
                AdmissionPolicyV1(evaluated_at=EVALUATED_AT),
                AdmissionContextV1(),
            )
            if admission.reducer_eligible:
                adapter = FieldKernelReducerAdapterV1.adapt_admitted_event(admission)
                reducer_result = module_result_to_dict(
                    FieldStateReducerModuleV1.reduce(
                        _reducer_request(
                            event=adapter.reducer_input_candidate,
                            confidence=semantic_projection.confidence_candidate,
                            case_id=case_id,
                        )
                    )
                )
        confidence = semantic_projection.confidence_candidate
        behavior = {
            "canonical_event_type_compatible": (
                semantic_projection.canonical_event_type
                == CANONICAL_EVENT_TYPE
            ),
            "semantic_event_candidate_only": (
                semantic_projection.candidate_only is True
            ),
            "semantic_state_unresolved": (
                semantic_projection.semantic_state_resolution_status == "UNRESOLVED"
                and semantic_projection.semantic_value_candidate is None
                and semantic_projection.subject_ref_candidate is None
            ),
            "detection_class_not_field_truth": (
                semantic_projection.truth_declared is False
            ),
            "target_binding_unresolved": True,
            "same_provider_detections_not_source_diversity": True,
            "semantic_event_admission_not_fact_admission": bool(
                admission is not None
                and admission.admission_status == "admitted_event"
                and admission.fact_admitted is False
            ),
            "confidence_lineage_complete": (
                confidence is not None
                and confidence == visual_projection.confidence_candidate
                and confidence == semantic_projection.confidence_candidate
                and (
                    reducer_result is None
                    or reducer_result.get("field_state_candidate", {})
                    .get("confidence_snapshot", {})
                    .get("measured_confidence")
                    == confidence
                )
            ),
            "no_presence_true_for_unresolved_subject": (
                semantic_projection.semantic_value_candidate is None
            ),
        }
        return CanonicalSemanticEventCaseResultV1(
            case_id=case_id,
            visual_projection=_jsonable(visual_projection),
            semantic_projection=semantic_projection,
            semantic_event_candidate=event,
            admission=admission,
            reducer_result=reducer_result,
            behavior=behavior,
        )

    def run(self, *, source_ref: str) -> Dict[str, Any]:
        runtime = self.visual_engine._run_provider(source_ref)
        provider = runtime.get("provider")
        detections = tuple(getattr(provider, "detections", ()) or ())
        evidence = tuple(getattr(provider, "evidence", ()) or ())
        positive = self._case(
            case_id="REAL_VISUAL_EVIDENCE_TO_CANONICAL_FIELD_SEMANTIC_EVENT",
            runtime=runtime,
        )
        not_truth = self._case(
            case_id="DETECTION_CLASS_NOT_FIELD_TRUTH",
            runtime=runtime,
        )
        unresolved = self._case(
            case_id="UNRESOLVED_SUBJECT_NOT_FORCED_TO_PRESENCE_TRUE",
            runtime=runtime,
        )
        source_diversity = self._case(
            case_id="SAME_PROVIDER_DETECTIONS_NOT_SOURCE_DIVERSITY",
            runtime=runtime,
        )
        admission_boundary = self._case(
            case_id="SEMANTIC_EVENT_ADMISSION_NOT_FACT_ADMISSION",
            runtime=runtime,
        )
        insufficient = self._case(
            case_id="INSUFFICIENT_EVIDENCE_REMAINS_FAIL_CLOSED",
            runtime=runtime,
        )
        cases = (
            positive,
            not_truth,
            unresolved,
            source_diversity,
            admission_boundary,
            insufficient,
        )
        confidence = positive.semantic_projection.confidence_candidate
        return {
            "phase": PHASE,
            "execution_mode": EXECUTION_MODE,
            "semantic_event_mode": "CANONICAL_OBSERVATION_EVENT_CANDIDATE",
            "provider_ref": "provider:yolo:local:v1",
            "model_ref": "model-asset:yolo11n:weights-v1",
            "canonical_event_type": CANONICAL_EVENT_TYPE,
            "state_type": STATE_TYPE,
            "source_ref": source_ref,
            "target_binding_status": (
                "EVALUATION_CANDIDATE_CANONICAL_OWNER_UNAVAILABLE"
            ),
            "semantic_target_resolved": False,
            "provider_real_execution_attempted": bool(
                runtime.get("provider_real_execution_attempted")
            ),
            "provider_real_execution_verified": bool(
                runtime.get("provider_real_execution_verified")
            ),
            "provider_invoked": bool(runtime.get("provider_invoked")),
            "model_invoked": bool(runtime.get("model_invoked")),
            "recorded_provider_result_used": False,
            "runtime_observation_ref": runtime.get("runtime_observation_ref"),
            "evidence_refs": list(runtime.get("evidence_refs") or ()),
            "detection_count": len(detections),
            "real_visual_evidence_count": len(evidence),
            "frame_dimensions": {
                "width": positive.visual_projection.get("frame_width"),
                "height": positive.visual_projection.get("frame_height"),
            },
            "source_visual_confidence": confidence,
            "field_projection_confidence": confidence,
            "semantic_event_confidence": confidence,
            "reducer_measured_confidence": confidence,
            "confidence_lineage_complete": (
                positive.behavior.get("confidence_lineage_complete") is True
            ),
            "evidence_sufficiency_contract": {
                "minimum_event_count": EVIDENCE_MINIMUM_EVENT_COUNT,
                "source_diversity_requirement": (
                    EVIDENCE_SOURCE_DIVERSITY_REQUIREMENT
                ),
            },
            "policy_trace_compatibility_gap": True,
            "policy_trace_compatibility_gap_reason": (
                "code policy registry does not list presence_state for "
                "insufficient_evidence_unresolved although the state-type "
                "policy mapping does"
            ),
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
    "RealVisualEvidenceCanonicalFieldSemanticEventEngineV1",
    "jsonable",
    "_repo_root",
]
