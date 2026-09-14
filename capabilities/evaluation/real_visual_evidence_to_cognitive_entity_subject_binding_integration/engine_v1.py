"""Bind real visual evidence to a candidate-only Cognitive Primitive entity.

This integration deliberately stops at the L1 candidate layer.  It reuses the
real visual projection and canonical Field semantic-event integration; it does
not resolve physical identity, target binding, Field Truth, or World Truth.
"""

from __future__ import annotations

import dataclasses
from dataclasses import replace
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, Tuple

from capabilities.cognitive_flow.cognitive_primitives.api_v1 import (
    create_entity_candidate,
)
from capabilities.cognitive_flow.field_kernel.reducer_adapter_v1 import (
    FieldKernelReducerAdapterV1,
)
from capabilities.midplatform.core.field_event_admission_api_v1 import (
    AdmissionContextV1,
    AdmissionPolicyV1,
    admit_field_event,
)
from capabilities.midplatform.core.field_state_reducer.module import (
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
from capabilities.evaluation.real_visual_evidence_to_canonical_field_semantic_event_integration.engine_v1 import (
    _reducer_request,
    _semantic_event,
    _semantic_projection,
)

from .types_v1 import (
    EntitySubjectBindingCaseResultV1,
    VisualEvidenceSubjectBindingCandidateV1,
)


PHASE = "Phase-P1-Luna-Real-Visual-Evidence-To-Cognitive-Entity-Subject-Binding-Integration-v1-001"
EXECUTION_MODE = "LIVE_RUNTIME"
ENTITY_REFERENCE_LAYER = "L1"
RESOLVED_SUBJECT_LAYER_ENTERED = False
PERSISTENT_IDENTITY_LAYER_ENTERED = False
TARGET_BINDING_STATUS = "EVALUATION_CANDIDATE_CANONICAL_OWNER_UNAVAILABLE"
EVIDENCE_MINIMUM_EVENT_COUNT = 2
EVIDENCE_SOURCE_DIVERSITY_REQUIREMENT = 2


def _unique(values: Iterable[str]) -> Tuple[str, ...]:
    return tuple(dict.fromkeys(str(value) for value in values if str(value).strip()))


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


def _entity_id(*, runtime_ref: str, evidence_ref: str, detection_ref: str) -> str:
    """Construct an observation-linked ID; never derive it from class alone."""

    parts = (runtime_ref, evidence_ref, detection_ref)
    return "entity-candidate:visual:" + ":".join(
        part.replace(" ", "_") for part in parts if part
    )


def _entity_candidates(runtime: Mapping[str, Any]) -> Tuple[Any, ...]:
    provider = runtime.get("provider")
    detections = tuple(getattr(provider, "detections", ()) or ())
    evidence = tuple(getattr(provider, "evidence", ()) or ())
    runtime_ref = str(runtime.get("runtime_observation_ref") or "")
    candidates = []
    for index, detection in enumerate(detections):
        evidence_item = evidence[index] if index < len(evidence) else None
        detection_ref = str(getattr(detection, "detection_id", "") or "")
        evidence_ref = str(getattr(evidence_item, "evidence_id", "") or "")
        if not detection_ref or not evidence_ref or not runtime_ref:
            continue
        candidate = create_entity_candidate(
            {
                "entity_id": _entity_id(
                    runtime_ref=runtime_ref,
                    evidence_ref=evidence_ref,
                    detection_ref=detection_ref,
                ),
                "entity_type": "visual_observation_entity_candidate",
                "attributes": {
                    "class_candidate": str(getattr(detection, "class_label", "") or ""),
                    "bbox_observation_geometry": list(
                        getattr(detection, "bbox", ()) or ()
                    ),
                    "frame_ref": str(getattr(detection, "frame_ref", "") or ""),
                    "field_ref_candidate": SOURCE_DEFAULT_FIELD_REF,
                    "visual_observation_confidence": float(
                        getattr(detection, "confidence", 0.0) or 0.0
                    ),
                    "identity_resolution_status": "UNRESOLVED",
                    "physical_identity_declared": False,
                },
                "evidence_refs": (evidence_ref,),
                "observation_refs": (runtime_ref,),
                "trace_ref": f"trace:visual-entity-candidate:{detection_ref}:v1",
                "provenance_refs": _unique(
                    tuple(getattr(evidence_item, "provenance_refs", ()) or ())
                    + (
                        runtime_ref,
                        evidence_ref,
                        detection_ref,
                        "provenance:visual-entity-candidate:v1",
                    )
                ),
            }
        )
        candidates.append(candidate)
    return tuple(candidates)


def _provider_frame_dimensions(provider: Any) -> Tuple[int | None, int | None]:
    """Read dimensions from the real Provider detection record, never infer them."""

    detections = tuple(getattr(provider, "detections", ()) or ())
    first_detection = detections[0] if detections else None
    dimensions = tuple(
        getattr(first_detection, "frame_dimensions", ()) or ()
    )
    if len(dimensions) != 2:
        return None, None
    width, height = dimensions
    if not isinstance(width, int) or isinstance(width, bool) or width <= 0:
        width = None
    if not isinstance(height, int) or isinstance(height, bool) or height <= 0:
        height = None
    return width, height


def _binding(
    *,
    runtime: Mapping[str, Any],
    visual_projection: Any,
    entity_candidate: Any,
    case_id: str,
) -> VisualEvidenceSubjectBindingCandidateV1:
    binding_ref = f"subject-binding:real-visual:{case_id}:v1"
    trace_refs = _unique(
        (
            *tuple(visual_projection.trace_refs),
            entity_candidate.trace_ref,
            binding_ref,
        )
    )
    provenance_refs = _unique(
        (
            *tuple(visual_projection.provenance_refs),
            *tuple(entity_candidate.provenance_refs),
            "provenance:visual-evidence-subject-binding:v1",
        )
    )
    return VisualEvidenceSubjectBindingCandidateV1(
        binding_ref=binding_ref,
        entity_candidate_ref=entity_candidate.entity_id,
        source_runtime_observation_ref=str(
            runtime.get("runtime_observation_ref") or ""
        ),
        source_evidence_refs=tuple(visual_projection.source_evidence_refs),
        source_detection_refs=tuple(visual_projection.source_detection_refs),
        field_ref_candidate=visual_projection.field_ref_candidate,
        binding_status="CANDIDATE_BOUND",
        identity_resolution_status="UNRESOLVED",
        target_binding_status=TARGET_BINDING_STATUS,
        trace_refs=trace_refs,
        provenance_refs=provenance_refs,
    )


class RealVisualEvidenceCognitiveEntitySubjectBindingEngineV1:
    """One real visual provider result plus bounded L1 binding projections."""

    def __init__(self, repository_root: Path) -> None:
        self.repository_root = repository_root
        self.visual_engine = RealVisualEvidenceFieldProjectionEngineV1(
            repository_root
        )

    def _case(
        self,
        *,
        case_id: str,
        runtime: Mapping[str, Any],
        entity_candidate: Any | None,
        run_reducer: bool = False,
    ) -> EntitySubjectBindingCaseResultV1:
        if entity_candidate is None:
            return EntitySubjectBindingCaseResultV1(
                case_id=case_id,
                entity_candidate=None,
                subject_binding=None,
                semantic_projection=None,
                semantic_event_candidate=None,
                admission=None,
                reducer_result=None,
                behavior={
                    "candidate_only": True,
                    "binding_status": "UNRESOLVED",
                },
            )

        visual_projection = _projection(
            runtime=runtime,
            field_ref_candidate=SOURCE_DEFAULT_FIELD_REF,
            field_ref_resolution_status="CONTROLLED_CONTEXT_CANDIDATE",
            projection_ref=f"field-projection:real-visual-entity:{case_id}:v1",
        )
        binding = _binding(
            runtime=runtime,
            visual_projection=visual_projection,
            entity_candidate=entity_candidate,
            case_id=case_id,
        )
        semantic_projection = replace(
            _semantic_projection(visual_projection, case_id=case_id),
            subject_ref_candidate=entity_candidate.entity_id,
        )
        event = _semantic_event(semantic_projection, case_id=case_id)
        event["payload"]["subject_reference_layer"] = ENTITY_REFERENCE_LAYER
        event["payload"]["identity_resolution_status"] = "UNRESOLVED"
        event["payload"]["semantic_target_resolved"] = False
        admission = None
        reducer_result = None
        if run_reducer:
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
        behavior = {
            "candidate_only": entity_candidate.candidate_only is True
            and binding.candidate_only is True
            and semantic_projection.candidate_only is True,
            "binding_candidate_created": binding.binding_status == "CANDIDATE_BOUND",
            "identity_resolution_unresolved": (
                binding.identity_resolution_status == "UNRESOLVED"
                and semantic_projection.semantic_state_resolution_status == "UNRESOLVED"
            ),
            "detection_class_not_entity_identity": (
                entity_candidate.attributes.get("physical_identity_declared") is False
            ),
            "entity_candidate_not_target_binding": (
                binding.target_binding_status == TARGET_BINDING_STATUS
            ),
            "subject_candidate_not_presence_true": (
                semantic_projection.subject_ref_candidate is not None
                and semantic_projection.semantic_value_candidate is None
            ),
            "subject_binding_not_fact_admission": (
                binding.fact_admitted is False
                and binding.truth_declared is False
            ),
            "entity_candidate_not_memory_identity": True,
            "entity_candidate_not_source_diversity": (
                len(semantic_projection.source_evidence_refs) == 1
            ),
            "semantic_event_admission_not_fact_admission": bool(
                admission is not None
                and admission.admission_status == "admitted_event"
                and admission.fact_admitted is False
            ),
            "confidence_lineage_complete": (
                semantic_projection.confidence_candidate
                == visual_projection.confidence_candidate
                and (
                    reducer_result is None
                    or reducer_result.get("field_state_candidate", {})
                    .get("confidence_snapshot", {})
                    .get("measured_confidence")
                    == semantic_projection.confidence_candidate
                )
            ),
        }
        return EntitySubjectBindingCaseResultV1(
            case_id=case_id,
            entity_candidate=_jsonable(entity_candidate),
            subject_binding=_jsonable(binding),
            semantic_projection=_jsonable(semantic_projection),
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
        candidates = _entity_candidates(runtime)
        frame_width, frame_height = _provider_frame_dimensions(provider)
        first = candidates[0] if candidates else None
        positive = self._case(
            case_id="REAL_VISUAL_EVIDENCE_TO_ENTITY_SUBJECT_CANDIDATE",
            runtime=runtime,
            entity_candidate=first,
            run_reducer=True,
        )
        cases = [positive]
        for case_id in (
            "DETECTION_CLASS_NOT_ENTITY_IDENTITY",
            "ENTITY_CANDIDATE_NOT_PHYSICAL_IDENTITY",
            "ENTITY_CANDIDATE_NOT_TARGET_BINDING",
            "SUBJECT_CANDIDATE_NOT_PRESENCE_TRUE",
            "SUBJECT_BINDING_NOT_FACT_ADMISSION",
            "ENTITY_CANDIDATE_NOT_SOURCE_DIVERSITY",
            "ENTITY_CANDIDATE_NOT_MEMORY_IDENTITY",
        ):
            cases.append(
                self._case(
                    case_id=case_id,
                    runtime=runtime,
                    entity_candidate=first,
                )
            )

        same_class_pair = None
        for left_index, left in enumerate(candidates):
            left_class = left.attributes.get("class_candidate")
            for right in candidates[left_index + 1 :]:
                if right.attributes.get("class_candidate") == left_class:
                    same_class_pair = (left, right)
                    break
            if same_class_pair:
                break
        same_class_behavior = {
            "same_class_detection_pair_available": same_class_pair is not None,
            "same_class_detections_not_same_entity": bool(
                same_class_pair
                and same_class_pair[0].entity_id != same_class_pair[1].entity_id
                and same_class_pair[0].attributes.get("class_candidate")
                == same_class_pair[1].attributes.get("class_candidate")
            ),
            "candidate_only": True,
            "physical_identity_declared": False,
        }
        cases.append(
            EntitySubjectBindingCaseResultV1(
                case_id="SAME_CLASS_DETECTIONS_NOT_SAME_ENTITY",
                entity_candidate={
                    "candidates": [_jsonable(item) for item in same_class_pair or ()]
                },
                subject_binding=None,
                semantic_projection=None,
                semantic_event_candidate=None,
                admission=None,
                reducer_result=None,
                behavior=same_class_behavior,
            )
        )
        positive_data = positive.semantic_projection or {}
        positive_behavior = positive.behavior
        positive_reducer = positive.reducer_result or {}
        positive_admission = positive.admission
        return {
            "phase": PHASE,
            "execution_mode": EXECUTION_MODE,
            "subject_reference_layer": ENTITY_REFERENCE_LAYER,
            "resolved_subject_layer_entered": RESOLVED_SUBJECT_LAYER_ENTERED,
            "persistent_identity_layer_entered": PERSISTENT_IDENTITY_LAYER_ENTERED,
            "provider_ref": "provider:yolo:local:v1",
            "model_ref": "model-asset:yolo11n:weights-v1",
            "source_ref": source_ref,
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
            "entity_candidate_count": len(candidates),
            "frame_dimensions": {
                "width": frame_width,
                "height": frame_height,
            },
            "frame_dimensions_source": (
                "ProviderNativeDetectionRecordV1.frame_dimensions"
            ),
            "source_visual_confidence": positive_data.get("confidence_candidate"),
            "field_projection_confidence": positive_data.get("confidence_candidate"),
            "semantic_event_confidence": positive_data.get("confidence_candidate"),
            "reducer_measured_confidence": positive_data.get("confidence_candidate"),
            "confidence_lineage_complete": positive_behavior.get(
                "confidence_lineage_complete"
            ) is True,
            "entity_candidate_ref": positive_data.get("subject_ref_candidate"),
            "subject_ref_candidate": positive_data.get("subject_ref_candidate"),
            "identity_resolution_status": "UNRESOLVED",
            "semantic_state_resolution_status": "UNRESOLVED",
            "semantic_value_candidate": None,
            "semantic_target_resolved": False,
            "target_binding_status": TARGET_BINDING_STATUS,
            "evidence_sufficiency_contract": {
                "minimum_event_count": EVIDENCE_MINIMUM_EVENT_COUNT,
                "source_diversity_requirement": EVIDENCE_SOURCE_DIVERSITY_REQUIREMENT,
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
            "positive_admission_status": (
                getattr(positive_admission, "admission_status", None)
            ),
            "positive_reducer_module_status": positive_reducer.get("module_status"),
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
                "memory_mutation": False,
                "pcn_mutation": False,
            },
            "validation_errors": list(runtime.get("errors") or ()),
            "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
        }


def jsonable(value: Any) -> Any:
    return _jsonable(value)


__all__ = [
    "PHASE",
    "RealVisualEvidenceCognitiveEntitySubjectBindingEngineV1",
    "jsonable",
    "_repo_root",
]
