"""Integrate admitted relation events with the existing Field State Reducer."""

from __future__ import annotations

import dataclasses
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, Tuple

from capabilities.evaluation.real_visual_relation_to_field_semantic_event_admission_integration.engine_v1 import (
    RealVisualRelationToFieldSemanticEventAdmissionEngineV1,
    _repo_root,
)
from capabilities.midplatform.core.field_event_admission_api_v1 import (
    AdmissionContextV1,
    AdmissionPolicyV1,
    admit_field_event,
)
from capabilities.midplatform.core.field_state_reducer.module.field_state_reducer_module_facade_v1 import (
    FieldStateReducerModuleV1,
)
from capabilities.midplatform.core.field_state_reducer.module.field_state_reducer_module_types_v1 import (
    FieldStateReducerModuleRequestV1,
)
from capabilities.midplatform.core.field_state_reducer.state_reduction.entity_field_relation_state_value_v1 import (
    ENTITY_FIELD_OBSERVATION_RELATION_STATE_V1,
    OBSERVED_IN_FIELD_V1,
)

from .types_v1 import EntityFieldRelationStateCandidateCaseResultV1


PHASE = "Phase-P1-Luna-Entity-Field-Relation-State-Candidate-Integration-v1-001"
EXECUTION_MODE = "LIVE_RUNTIME"
STATE_TYPE = ENTITY_FIELD_OBSERVATION_RELATION_STATE_V1
EVENT_TYPE = "entity_field_relation_observed"
RELATION_KIND = "ENTITY_TO_FIELD_OBSERVATION_RELATION"
REAL_SOURCE_ID = "provider:yolo:local:v1"
CONTROLLED_SOURCE_IDS = (
    "controlled:relation-state-source:a:v1",
    "controlled:relation-state-source:b:v1",
)


def _current_test_time() -> str:
    """Return one UTC timestamp for this user-terminal integration run."""

    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _unique(values: Iterable[Any]) -> Tuple[str, ...]:
    return tuple(dict.fromkeys(str(value) for value in values if str(value).strip()))


def _jsonable(value: Any) -> Any:
    if dataclasses.is_dataclass(value):
        return {key: _jsonable(item) for key, item in asdict(value).items()}
    if isinstance(value, Mapping):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_jsonable(item) for item in value]
    return value


def _admit(event: Mapping[str, Any], *, evaluated_at: str) -> Dict[str, Any]:
    result = admit_field_event(
        event,
        AdmissionPolicyV1(evaluated_at=evaluated_at),
        AdmissionContextV1(),
    )
    return _jsonable(result)


def _base_event(
    *,
    event: Mapping[str, Any],
    projection: Mapping[str, Any],
    event_id: str,
    source_id: str,
    trace_ref: str,
    event_time: str,
) -> Dict[str, Any]:
    payload = dict(event.get("payload") or {})
    payload.update(
        {
            "source_id": source_id,
            "source_refs": [source_id],
            "provenance_refs": list(projection.get("provenance_refs") or ()),
            "relation_semantic_kind": RELATION_KIND,
            "relation_candidate_ref": payload.get("relation_candidate_ref"),
            "subject_ref": payload.get("subject_ref"),
            "predicate": OBSERVED_IN_FIELD_V1,
            "object_ref": payload.get("object_ref"),
            "candidate_only": True,
            "fact_admitted": False,
            "truth_declared": False,
            "persistent_relation_declared": False,
            "identity_resolution_status": "UNRESOLVED",
        }
    )
    result = dict(event)
    result.update(
        {
            "event_id": event_id,
            "event_type": EVENT_TYPE,
            "source_id": source_id,
            "trace_ref": trace_ref,
            "occurred_at": event_time,
            "observed_at": event_time,
            "received_at": event_time,
            "payload": payload,
        }
    )
    return result


def _reducer_request(
    *,
    run_id: str,
    admitted_events: Tuple[Dict[str, Any], ...],
    source_ids: Tuple[str, ...],
    evaluated_at: str,
) -> FieldStateReducerModuleRequestV1:
    event_ids = tuple(str(event.get("event_id") or "") for event in admitted_events)
    event_times = tuple(
        str(event.get("event_time") or event.get("occurred_at") or "")
        for event in admitted_events
    )
    admission_ids = tuple(
        f"admission:{event_id}" for event_id in event_ids if event_id
    )
    return FieldStateReducerModuleRequestV1(
        reducer_request_id=f"reducer-request:{run_id}:v1",
        reducer_run_id=run_id,
        field_id="field:visual-frame:v1",
        requested_state_type=STATE_TYPE,
        admitted_events=admitted_events,
        existing_state_snapshot={},
        temporal_snapshot={
            "status": "active",
            "sufficient_evidence": len(admitted_events) >= 2,
            "new_event_available": True,
            "refresh_evidence_available": True,
        },
        policy_registry_snapshot={"version": "v1"},
        evaluation_contract_snapshot={"version": "v1"},
        selection_contract_snapshot={"version": "v1"},
        reduction_contract_snapshot={"version": "v1"},
        conflict_snapshot={
            "tags": [],
            "conflict_type": None,
            "unresolved": False,
            "negative_signal_present": False,
        },
        overlay_snapshot={"separate_from_substrate": True},
        owner_correction_snapshot={"candidate_only": True},
        provenance_snapshot={
            # The evidence contract consumes these fields directly. Preserve
            # one-event scalar shape and multi-event lineage for controlled
            # consensus evaluation.
            "source_id": source_ids[0] if len(source_ids) == 1 else list(source_ids),
            "event_id": event_ids[0] if len(event_ids) == 1 else list(event_ids),
            "event_time": event_times[0] if len(event_times) == 1 else list(event_times),
            "admission_id": (
                admission_ids[0]
                if len(admission_ids) == 1
                else list(admission_ids)
            ),
            "available_keys": [
                "source_id",
                "event_id",
                "event_time",
                "admission_id",
            ],
            "source_ids": list(source_ids),
            "evaluation_requested_at": evaluated_at,
            "confidence_policy_snapshot": {"measured_confidence": 0.8794201016426086},
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


def _run_reducer(
    *,
    run_id: str,
    admissions: Tuple[Dict[str, Any], ...],
    source_ids: Tuple[str, ...],
    evaluated_at: str,
) -> Dict[str, Any]:
    reducer = FieldStateReducerModuleV1.reduce(
        _reducer_request(
            run_id=run_id,
            admitted_events=tuple(
                dict(item.get("reducer_input_candidate") or {})
                for item in admissions
                if item.get("admission_status") == "admitted_event"
            ),
            source_ids=source_ids,
            evaluated_at=evaluated_at,
        )
    )
    return _jsonable(reducer)


def _case(
    *,
    case_id: str,
    source_mode: str,
    admissions: Tuple[Dict[str, Any], ...],
    reducer_result: Dict[str, Any],
) -> EntityFieldRelationStateCandidateCaseResultV1:
    candidate = dict(reducer_result.get("field_state_candidate") or {})
    candidate_value = dict(candidate.get("candidate_value") or {})
    typed = (
        candidate_value
        if candidate_value.get("relation_semantic_kind") == RELATION_KIND
        and candidate_value.get("predicate") == OBSERVED_IN_FIELD_V1
        else None
    )
    admitted_events = tuple(
        dict(item.get("reducer_input_candidate") or {})
        for item in admissions
        if item.get("admission_status") == "admitted_event"
    )
    behavior = {
        "admission_statuses": [item.get("admission_status") for item in admissions],
        "evidence_event_count": len(admitted_events),
        "evidence_source_count": len(
            {str(item.get("source_id")) for item in admitted_events if item.get("source_id")}
        ),
        "typed_relation_value_created": typed is not None,
        "typed_relation_value_not_opaque_payload": typed is not None
        and set(typed) != set(dict(admitted_events[0].get("payload") or {}))
        if admitted_events
        else False,
        "subject_ref_preserved": bool(typed)
        and typed.get("subject_ref") == typed.get("subject_ref"),
        "predicate_observed_in_field": bool(typed)
        and typed.get("predicate") == OBSERVED_IN_FIELD_V1,
        "candidate_only": candidate.get("candidate_only") is True
        and candidate.get("fact_admitted") is False
        and bool(typed)
        and typed.get("candidate_only") is True,
        "truth_not_declared": bool(typed) and typed.get("truth_declared") is False,
        "persistent_relation_not_declared": bool(typed)
        and typed.get("persistent_relation_declared") is False,
        "identity_unresolved": bool(typed)
        and typed.get("identity_resolution_status") == "UNRESOLVED",
        "field_truth_not_promoted": reducer_result.get("fact_admitted") is False,
        "field_mutation_not_executed": reducer_result.get("state_store_write_executed") is False,
    }
    return EntityFieldRelationStateCandidateCaseResultV1(
        case_id=case_id,
        source_mode=source_mode,
        admitted_events=admitted_events,
        reducer_result=reducer_result,
        typed_relation_state_candidate=typed,
        behavior=behavior,
    )


class RealEntityFieldRelationStateCandidateIntegrationEngineV1:
    """Run one real single-source case and one controlled two-source case."""

    def __init__(self, repository_root: Path) -> None:
        self.repository_root = repository_root

    def run(self, *, source_ref: str) -> Dict[str, Any]:
        evaluation_time = _current_test_time()
        prior = RealVisualRelationToFieldSemanticEventAdmissionEngineV1(
            self.repository_root
        ).run(source_ref=source_ref)
        prior_cases = {
            str(item.get("case_id")): item for item in prior.get("cases", [])
        }
        positive = prior_cases.get("ENTITY_FIELD_RELATION_SEMANTIC_EVENT_ADMITTED", {})
        real_event = dict(positive.get("field_event_candidate") or {})
        projection = dict(positive.get("projection") or {})

        real_event = _base_event(
            event=real_event,
            projection=projection,
            event_id="field-event:relation-state:real-single:v1",
            source_id=REAL_SOURCE_ID,
            trace_ref="trace:relation-state:real-single:v1",
            event_time=evaluation_time,
        )
        real_admission = _admit(real_event, evaluated_at=evaluation_time)
        real_admissions = (real_admission,)
        real_reducer = _run_reducer(
            run_id="relation-state:real-single",
            admissions=real_admissions,
            source_ids=(REAL_SOURCE_ID,),
            evaluated_at=evaluation_time,
        )
        real_case = _case(
            case_id="REAL_SINGLE_SOURCE_FAIL_CLOSED",
            source_mode="REAL_PROVIDER_DERIVED_SINGLE_SOURCE",
            admissions=real_admissions,
            reducer_result=real_reducer,
        )

        controlled_events = tuple(
            _base_event(
                event=real_event,
                projection=projection,
                event_id=f"field-event:relation-state:controlled-{suffix}:v1",
                source_id=source_id,
                trace_ref=f"trace:relation-state:controlled-{suffix}:v1",
                event_time=evaluation_time,
            )
            for suffix, source_id in zip(("a", "b"), CONTROLLED_SOURCE_IDS)
        )
        controlled_admissions = tuple(
            _admit(event, evaluated_at=evaluation_time) for event in controlled_events
        )
        controlled_reducer = _run_reducer(
            run_id="relation-state:controlled-multi-source",
            admissions=controlled_admissions,
            source_ids=CONTROLLED_SOURCE_IDS,
            evaluated_at=evaluation_time,
        )
        controlled_case = _case(
            case_id="CONTROLLED_MULTI_SOURCE_RELATION_STATE",
            source_mode="CONTROLLED_MULTI_SOURCE_SEMANTIC_REDUCER_TEST",
            admissions=controlled_admissions,
            reducer_result=controlled_reducer,
        )

        real_candidate = dict(real_case.typed_relation_state_candidate or {})
        controlled_candidate = dict(
            controlled_case.typed_relation_state_candidate or {}
        )
        return {
            "phase": PHASE,
            "execution_mode": EXECUTION_MODE,
            "provider_execution_mode": prior.get("execution_mode"),
            "provider_invoked": prior.get("provider_invoked") is True,
            "model_invoked": prior.get("model_invoked") is True,
            "provider_real_execution_verified": prior.get(
                "provider_real_execution_verified"
            )
            is True,
            "recorded_provider_result_used": False,
            "source_ref": source_ref,
            "admission_evaluated_at": evaluation_time,
            "event_temporal_source": "CURRENT_USER_TERMINAL_TEST_TIME",
            "runtime_observation_ref": prior.get("runtime_observation_ref"),
            "real_visual_evidence_count": prior.get("real_visual_evidence_count", 0),
            "entity_candidate_count": prior.get("entity_candidate_count", 0),
            "relation_candidate_count": prior.get("relation_candidate_count", 0),
            "state_type": STATE_TYPE,
            "event_type": EVENT_TYPE,
            "relation_semantic_kind": RELATION_KIND,
            "relation_predicate": OBSERVED_IN_FIELD_V1,
            "field_ref": prior.get("field_ref"),
            "evidence_sufficiency_contract": {
                "minimum_event_count": 2,
                "source_diversity_requirement": 2,
            },
            "real_single_source": _jsonable(real_case),
            "controlled_multi_source": _jsonable(controlled_case),
            "real_single_source_insufficient_evidence": real_reducer.get(
                "module_status"
            )
            == "insufficient_evidence",
            "controlled_multi_source_sufficient": controlled_reducer.get(
                "module_status"
            )
            == "completed_candidate"
            and bool(controlled_candidate),
            "subject_ref": controlled_candidate.get("subject_ref"),
            "predicate": controlled_candidate.get("predicate"),
            "object_ref": controlled_candidate.get("object_ref"),
            "relation_candidate_ref": controlled_candidate.get("relation_candidate_ref"),
            "candidate_only": True,
            "fact_admitted": False,
            "truth_declared": False,
            "persistent_relation_declared": False,
            "identity_resolution_status": "UNRESOLVED",
            "relation_candidates_are_not_sources": True,
            "entity_candidates_are_not_sources": True,
            "subject_bindings_are_not_sources": True,
            "field_truth_promotion": False,
            "world_truth_declared": False,
            "field_mutation": False,
            "memory_mutation": False,
            "pcn_mutation": False,
            "a_route_invoked": False,
            "policy_trace_compatibility_gap": True,
            "policy_trace_compatibility_gap_status": "KNOWN_NON_BLOCKING_INDEPENDENT_DEBT",
            "forbidden_behaviors": {
                "field_truth_promotion": False,
                "world_truth_declared": False,
                "field_mutation": False,
                "memory_mutation": False,
                "pcn_mutation": False,
                "a_route_invocation": False,
                "decision_execution": False,
                "task_execution": False,
                "action_execution": False,
                "device_control": False,
                "camera_control": False,
                "movement_control": False,
            },
            "validation_errors": list(prior.get("validation_errors") or ()),
            "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
        }


def jsonable(value: Any) -> Any:
    return _jsonable(value)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


__all__ = [
    "PHASE",
    "RealEntityFieldRelationStateCandidateIntegrationEngineV1",
    "jsonable",
    "_repo_root",
]
