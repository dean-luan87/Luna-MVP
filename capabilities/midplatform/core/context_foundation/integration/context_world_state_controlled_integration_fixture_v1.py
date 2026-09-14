"""Synthetic C01-C36 controlled Context / Field / World scenarios."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple


def _base(case_id: str, title: str) -> Dict[str, Any]:
    return {
        "case_id": case_id,
        "title": title,
        "root_trace_id": f"root-trace:{case_id}",
        "observation_ref": f"observation:{case_id}",
        "evidence_refs": (f"evidence:{case_id}:1",),
        "source_refs": (f"source:{case_id}",),
        "task_refs": (f"task:{case_id}",),
        "field_refs": (),
        "field_ref": f"field:{case_id}",
        "intent_ref": f"intent:{case_id}",
        "pcn_ref": f"pcn:{case_id}",
        "observation_admitted": True,
        "field_relevant": False,
        "field_event_admission": False,
        "contradiction_refs": (),
        "field_conflict_refs": (),
        "correction_refs": (),
        "uncertainty_refs": (),
        "temporal_status": "ACTIVE",
        "observed_at": "2026-08-13T00:00:00Z",
        "valid_from": "2026-08-13T00:00:00Z",
        "valid_until": "",
        "expected": {},
    }


def _case(case_id: str, title: str, expected: Dict[str, Any], **updates: Any) -> Dict[str, Any]:
    request = _base(case_id, title)
    request.update(updates)
    request["expected"] = expected
    return {"case_id": case_id, "title": title, "request": request, "expected": expected}


def build_context_world_state_cases_v1() -> Tuple[Dict[str, Any], ...]:
    cases: List[Dict[str, Any]] = [
        _case("C01", "Admitted observation forms context candidate", {"observation_context_handoff_present": True, "context_candidate_present": True, "context_mutation": False}),
        _case("C02", "Observation does not directly mutate field", {"field_state_mutation": False, "observation_can_mutate_field": False}),
        _case("C03", "Field-relevant observation forms field event candidate", {"field_event_candidate_present": True, "field_event_admission_required": True, "field_state_mutation": False}, field_relevant=True),
        _case("C04", "Field event requires admission before reducer eligibility", {"field_event_candidate_present": True, "field_event_admitted": False, "reducer_eligible": False}, field_relevant=True),
        _case("C05", "Field State Reducer remains sole mutation authority", {"field_event_admitted": True, "reducer_eligible": True, "reducer_invoked": False, "reducer_is_single_mutation_authority": True, "field_state_mutation": False}, field_relevant=True, field_event_admission=True),
        _case("C06", "Context references Field State read-only", {"context_candidate_present": True, "context_field_refs_read_only": True, "context_mutation": False}, field_refs=("field:C06",)),
        _case("C07", "Current World references Context and Field State", {"current_world_candidate_present": True, "current_world_refs_context": True, "current_world_refs_field_state": True}, field_refs=("field:C07",)),
        _case("C08", "Current World is not Field State", {"current_world_candidate_present": True, "current_world_is_field_truth": False, "current_world_field_mutation": False}, field_refs=("field:C08",)),
        _case("C09", "Conflicting observations remain contested", {"context_status": "CONTESTED", "contradiction_preserved": True, "current_world_is_field_truth": False}, contradiction_refs=("contradiction:C09",)),
        _case("C10", "Observation conflict with existing Field State remains visible", {"field_event_candidate_present": True, "current_world_candidate_present": True, "contradiction_preserved": True, "current_world_is_field_truth": False}, field_relevant=True, field_event_admission=True, field_conflict_refs=("field-conflict:C10",)),
        _case("C11", "Stale observation degrades downstream candidate", {"temporal_status": "STALE", "context_status": "DEGRADED_STALE", "temporal_lineage_preserved": True}, stale=True),
        _case("C12", "Expired observation does not form active context", {"temporal_status": "EXPIRED", "context_candidate_present": False, "current_world_candidate_present": False}, expired=True, observation_admitted=False),
        _case("C13", "Refreshed observation preserves temporal lineage", {"temporal_status": "REFRESHED", "context_candidate_present": True, "temporal_lineage_preserved": True}, refresh=True),
        _case("C14", "Revoked source is not admitted downstream", {"temporal_status": "REVOKED", "context_candidate_present": False, "current_world_candidate_present": False}, source_revoked=True, observation_admitted=False),
        _case("C15", "Superseded Field information preserves lineage", {"temporal_status": "SUPERSEDED", "field_event_candidate_present": True, "field_event_admitted": False, "temporal_lineage_preserved": True}, field_relevant=True, field_event_admission=True, superseded=True),
        _case("C16", "User correction preserves correction lineage", {"correction_lineage_preserved": True, "provenance_reverse_lookup_complete": True}, correction_refs=("correction:user:C16",)),
        _case("C17", "OCR evidence is not a World fact", {"source_truth_declared": False, "ocr_evidence_is_world_fact": False}, source_kind="OCR"),
        _case("C18", "YOLO detection is not object truth", {"source_truth_declared": False, "visual_detection_is_object_truth": False}, source_kind="VISION"),
        _case("C19", "SLAM geometry is not semantic truth", {"source_truth_declared": False, "slam_geometry_is_semantic_truth": False}, source_kind="SLAM_SPATIAL"),
        _case("C20", "Task context participates in context assembly", {"task_context_present": True, "context_candidate_present": True}),
        _case("C21", "Intent reference is read-only", {"intent_reference_read_only": True, "context_mutation": False}),
        _case("C22", "PCN reference is read-only", {"pcn_reference_read_only": True, "context_mutation": False}),
        _case("C23", "Duplicate observation handoff is guarded", {"duplicate_observation_guard": False, "observation_context_handoff_present": False}, duplicate_observation_handoff=True),
        _case("C24", "Duplicate Field Event is guarded", {"duplicate_field_event_guard": False, "field_event_candidate_present": False}, field_relevant=True, duplicate_field_event=True),
        _case("C25", "Duplicate Context update is guarded", {"duplicate_context_guard": False, "context_candidate_present": False}, duplicate_context_update=True),
        _case("C26", "Duplicate Current World candidate is guarded", {"duplicate_current_world_guard": False, "current_world_candidate_present": False}, duplicate_current_world=True),
        _case("C27", "Provenance reverse lookup is preserved", {"provenance_reverse_lookup_complete": True, "current_world_candidate_present": True}),
        _case("C28", "Unresolved contradiction remains unresolved", {"context_status": "CONTESTED", "contradiction_preserved": True, "current_world_is_field_truth": False}, contradiction_refs=("contradiction:unresolved:C28",), uncertainty_refs=("uncertainty:C28",)),
        _case("C29", "Temporal validity is preserved end to end", {"temporal_lineage_preserved": True, "provenance_reverse_lookup_complete": True}, valid_until="2026-08-13T01:00:00Z"),
        _case("C30", "A Route next cognitive stage receives candidate handoff", {"a_route_handoff_candidate_present": True, "runtime_handoff_ready": False, "mutation_authority": False}),
        _case("C31", "No runtime execution", {"runtime_handoff_ready": False, "field_state_mutation": False}),
        _case("C32", "No provider or model invocation", {"provider_invocation": False, "model_call": False}),
        _case("C33", "No second Field State writer", {"reducer_is_single_mutation_authority": True, "field_state_mutation": False}),
        _case("C34", "Emotion Engine remains deferred", {"emotion_engine_execution": False}),
        _case("C35", "B Route remains deferred", {"b_route_execution": False}),
        _case("C36", "Semantic compression remains deferred", {"semantic_compression_execution": False}),
    ]
    return tuple(cases)
