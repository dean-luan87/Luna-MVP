"""Controlled Evidence -> Context / Field / Current World integration."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass, replace
from typing import Any, Dict, Iterable, Mapping, Tuple

from capabilities.cognitive_flow.field_kernel.core.field_state_v1 import (
    FieldStateV1,
    field_state_from_reducer_output_v1,
)
from capabilities.cognitive_flow.field_kernel.reducer_adapter_v1 import (
    FieldKernelReducerAdapterV1,
)
from capabilities.midplatform.core.context_foundation.context_foundation_skeleton_v1 import (
    ContextFoundationSkeletonV1,
)
from capabilities.midplatform.core.context_foundation.context_foundation_types_v1 import (
    ContextAssemblyInputV1,
    TemporalScopeReferenceV1,
)
from capabilities.midplatform.core.context_foundation.context_projection_types_v1 import (
    ProjectionReferenceV1,
)
from capabilities.midplatform.core.cognitive_state_formation.current_world_types_v1 import (
    CurrentWorldCandidateV1,
)
from capabilities.midplatform.core.evidence_to_field_event_adapter_v1 import (
    BLOCKED_STATUS,
    form_field_event_candidate_from_evidence,
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
from capabilities.midplatform.core.observation_gateway.observation_gateway_core_types_v1 import (
    PerceptionEvidenceV1,
)
from capabilities.midplatform.protocol_manager.module.governance_verification_backbone_v1 import (
    CORE_GOVERNANCE_RULE_REGISTRY_V1,
    resolve_applicable_governance_set,
    run_governance_postflight,
    run_governance_preflight,
)

from .fixtures_v1 import (
    CONTEXT_REF,
    EVALUATED_AT,
    EVALUATION_MARKER,
    FIELD_REF,
    FieldIntegrationCaseV1,
    build_evidence_context_field_current_world_cases_v1,
    valid_authority_records,
    valid_profile,
)


OBSERVED_AT = EVALUATED_AT


def _json_safe(value: Any) -> Any:
    if is_dataclass(value):
        return _json_safe(asdict(value))
    if isinstance(value, Mapping):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_json_safe(item) for item in value]
    return value


def _mapping(value: Any) -> Mapping[str, Any]:
    """Normalize nullable/non-mapping projections without inventing fields."""

    return value if isinstance(value, Mapping) else {}


def _reducer_status_from_result(result: Any) -> str:
    """Project the case result status without treating module diagnostics as failure."""

    reducer_result = _mapping(result)
    if not reducer_result:
        return "NO_REDUCER"

    module_status = str(reducer_result.get("module_status") or "")
    if module_status in {
        "internal_error",
        "rejected_input",
        "governance_review_required",
        "unresolved",
        "conflicted",
        "temporally_invalid",
    }:
        return module_status
    if reducer_result.get("field_state_candidate") is not None:
        return "completed_candidate"
    if module_status in {"no_state_change", "insufficient_evidence"}:
        return "NO_UPDATE"
    return module_status or "NO_REDUCER"


def _aggregate_reducer_status(statuses: Iterable[str]) -> str:
    """Aggregate batch statuses deterministically without last-batch overwrite."""

    values = tuple(status for status in statuses if status)
    if not values:
        return "NO_REDUCER"
    for status in (
        "internal_error",
        "rejected_input",
        "governance_review_required",
        "unresolved",
        "conflicted",
        "temporally_invalid",
    ):
        if status in values:
            return status
    if "completed_candidate" in values:
        return "completed_candidate"
    if all(status == "NO_UPDATE" for status in values):
        return "NO_UPDATE"
    return values[0]


def _unique(values: Iterable[str]) -> Tuple[str, ...]:
    return tuple(dict.fromkeys(str(value) for value in values if str(value).strip()))


def _evidence(case: FieldIntegrationCaseV1, index: int) -> PerceptionEvidenceV1:
    scenario = case.scenario if case.scenario != "normal" else "abstract"
    provider_ref = f"provider:synthetic:{scenario}:{index}"
    observation_ref = f"runtime-observation:controlled:{case.case_id}:{index}"
    execution_ref = f"execution-instance:controlled:{case.case_id}:{index}"
    result_ref = f"provider-result:controlled:{case.case_id}:{index}"
    evidence_ref = f"evidence:controlled:{case.case_id}:{index}"
    model_ref = "model:controlled:explicit" if case.case_id == "EXPLICIT_MODEL_CARRY_FORWARD" else None
    return PerceptionEvidenceV1(
        evidence_id=evidence_ref,
        evidence_type="controlled_runtime_observation_evidence",
        source_provider=provider_ref,
        source_capability=f"capability:abstract:{scenario}",
        source_model_ref=model_ref,
        source_region_ref=None,
        source_temporal_ref=f"temporal:controlled:{case.case_id}:{index}",
        raw_output_ref=result_ref,
        confidence_candidate=0.8,
        quality_candidate=0.8,
        uncertainty_refs=(),
        contradiction_refs=(),
        correction_refs=(),
        trace_ref=f"trace:evidence:controlled:{case.case_id}:{index}",
        provenance_refs=(
            provider_ref,
            f"capability:abstract:{scenario}",
            f"binding:controlled:{case.case_id}:{index}",
            f"grant:controlled:{case.case_id}:{index}",
            f"allocation:controlled:{case.case_id}:{index}",
            execution_ref,
            f"session:controlled:{case.case_id}:{index}",
            f"invocation:controlled:{case.case_id}:{index}",
            result_ref,
            observation_ref,
            f"gateway-admission:controlled:{case.case_id}:{index}",
        ),
        sensitivity="NORMAL",
        candidate_only=True,
        fact_declared=False,
        candidate_payload={"opaque_payload_ref": f"payload:synthetic:opaque:{scenario}:{index}"},
    )


def _context(case: FieldIntegrationCaseV1, evidence_ref: str) -> Dict[str, Any] | None:
    if case.context_mismatch:
        return None
    field_ref = case.field_ref or FIELD_REF
    field_projection = ProjectionReferenceV1(
        source_owner=("Field State Reducer" if case.context_owner_mismatch else "Field State System"),
        projection_id=field_ref,
        projection_version="v1",
        timestamp=EVALUATED_AT,
        validity="candidate",
        confidence=0.8,
        unknown_state="known" if not case.insufficient_evidence else "unknown",
        provenance=(evidence_ref, f"context:{case.case_id}"),
        projection_kind="field",
        trace_reference=f"trace:context-field:{case.case_id}",
    )
    observation_projection = ProjectionReferenceV1(
        source_owner=("Observation Gateway Governance" if case.context_owner_mismatch else "Observation Manager"),
        projection_id=f"observation:{case.case_id}",
        projection_version="v1",
        timestamp=EVALUATED_AT,
        validity="admitted",
        confidence=0.8,
        unknown_state="known" if not case.insufficient_evidence else "uncertain",
        provenance=(evidence_ref, f"context:{case.case_id}"),
        projection_kind="observation",
        trace_reference=f"trace:context-observation:{case.case_id}",
    )
    envelope = ContextFoundationSkeletonV1().assemble_context(
        ContextAssemblyInputV1(
            context_id=f"context:controlled:{case.case_id}",
            version="v1",
            temporal_scope=TemporalScopeReferenceV1(
                scope_id=f"temporal-scope:controlled:{case.case_id}",
                valid_from_reference=EVALUATED_AT,
                valid_until_reference="",
                expiry_condition_reference="governed_temporal_invalidated",
                reset_condition_reference="next_cognitive_cycle",
            ),
            field_projection_reference=field_projection,
            observation_projection_reference=observation_projection,
            provenance=(evidence_ref, f"context:{case.case_id}"),
            trace_timestamp=EVALUATED_AT,
        )
    )
    return _json_safe(envelope)


def _malformed_evidence(evidence: PerceptionEvidenceV1) -> Dict[str, Any]:
    value = _json_safe(evidence)
    value.pop("evidence_id", None)
    return value


def _lineage_broken_evidence(evidence: PerceptionEvidenceV1) -> Dict[str, Any]:
    value = _json_safe(evidence)
    value["provenance_refs"] = []
    return value


def _reducer_request(
    *,
    case: FieldIntegrationCaseV1,
    field_ref: str,
    admitted_events: Tuple[Dict[str, Any], ...],
    evidence_refs: Tuple[str, ...],
) -> FieldStateReducerModuleRequestV1:
    event_refs = tuple(str(admitted_event.get("event_id", "")) for admitted_event in admitted_events)
    conflict_refs = event_refs if case.conflict else ()
    temporal_status = "expired" if case.expired_overlay else "active"
    if case.stale_evidence:
        temporal_status = "stale"
    overlay_refs = (f"overlay:controlled:{case.case_id}",) if case.temporary_overlay else ()
    reducer_events = []
    for admitted_event in admitted_events:
        reducer_event = dict(admitted_event)
        reducer_event.update(
            {
                "admitted": True,
                "raw_observation": False,
                "source_id": str(_mapping(admitted_event.get("payload")).get("source_provider", "source:controlled")),
                "event_time": OBSERVED_AT,
                "admission_id": f"admission:{admitted_event.get('event_id', '')}",
            }
        )
        reducer_events.append(reducer_event)
    return FieldStateReducerModuleRequestV1(
        reducer_request_id=f"reducer-request:controlled:{case.case_id}",
        reducer_run_id=f"reducer-run:controlled:{case.case_id}",
        field_id=field_ref,
        requested_state_type="temporary_overlay_state" if case.temporary_overlay else "accessibility_state",
        admitted_events=tuple(reducer_events),
        existing_state_snapshot={},
        temporal_snapshot={
            "snapshot_id": f"temporal-snapshot:controlled:{case.case_id}",
            "status": temporal_status,
            "refresh_evidence_available": case.refresh,
            "new_event_available": True,
            "sufficient_evidence": not case.insufficient_evidence,
            "confidence_snapshot": {"measured_confidence": 0.8},
        },
        policy_registry_snapshot={"version": "v1"},
        evaluation_contract_snapshot={"version": "v1"},
        selection_contract_snapshot={"version": "v1"},
        reduction_contract_snapshot={"version": "v1"},
        conflict_snapshot={
            "tags": ["controlled_conflict"] if case.conflict else [],
            "conflict_type": "competing_field_events" if case.conflict else "none",
            "unresolved": case.conflict,
            "preserve_conflict": case.conflict,
            "provisional_candidate_allowed": True,
            "conflicting_event_refs": list(conflict_refs),
            "resolution_available": False if case.conflict else True,
        },
        overlay_snapshot={
            "overlay_refs": list(overlay_refs),
            "overlay_active": case.temporary_overlay and not case.expired_overlay,
            "overlay_expired": case.expired_overlay,
            "substrate_mutation_requested": False,
        },
        owner_correction_snapshot={
            "owner_correction_refs": [f"correction:controlled:{case.case_id}"] if case.correction else [],
        },
        provenance_snapshot={
            "source_id": "source:controlled:evidence",
            "event_id": event_refs[0] if event_refs else "",
            "event_time": OBSERVED_AT,
            "admission_id": f"admission:{event_refs[0]}" if event_refs else "",
            "available_keys": ["source_id", "event_id", "event_time", "admission_id"],
            "source_ids": ["source:controlled:evidence"],
            "confidence_policy_snapshot": {"measured_confidence": 0.8},
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
            "evidence_refs": list(evidence_refs),
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


def _field_state_from_candidate(
    candidate: Mapping[str, Any], admitted_event: Mapping[str, Any], case: FieldIntegrationCaseV1
) -> FieldStateV1:
    state_id = str(candidate.get("state_candidate_id") or f"field-state:{case.case_id}")
    return field_state_from_reducer_output_v1(
        {
            "produced_by": "field_state_reducer",
            "reducer_output_ref": f"reducer-output:controlled:{case.case_id}",
            "state_id": state_id,
            "target_ref": str(admitted_event.get("field_ref") or case.field_ref),
            "state_type": str(candidate.get("state_type") or "accessibility_state"),
            "value": dict(candidate.get("candidate_value") or {}),
            "valid_time": {
                "effective_from": admitted_event.get("occurred_at"),
                "effective_until": None,
            },
            "evidence_refs": tuple(admitted_event.get("evidence_refs") or ()),
            "source_chain": tuple(admitted_event.get("source_chain") or ()),
            "trace_ref": str(candidate.get("trace_ref") or admitted_event.get("trace_ref") or ""),
            "provenance": {
                "evidence_refs": tuple(admitted_event.get("evidence_refs") or ()),
                "source_chain": tuple(admitted_event.get("source_chain") or ()),
                "context_ref": CONTEXT_REF,
            },
            "candidate_only": True,
        }
    )


def _current_world_candidate(
    case: FieldIntegrationCaseV1,
    context: Mapping[str, Any] | None,
    field_states: Tuple[FieldStateV1, ...],
    evidence_refs: Tuple[str, ...],
    event_refs: Tuple[str, ...],
) -> CurrentWorldCandidateV1 | None:
    if context is None:
        return None
    conflict_refs = event_refs if case.conflict else ()
    return CurrentWorldCandidateV1(
        current_world_id=f"current-world:controlled:{case.case_id}",
        attention_refs=(),
        active_hypothesis_refs=(),
        alternative_hypothesis_refs=(),
        context_refs=(str(context.get("context_id") or ""),),
        field_state_refs=tuple(state.state_id for state in field_states),
        pcn_refs=(),
        intent_refs=(),
        observation_refs=tuple(
            f"runtime-observation:controlled:{case.case_id}:{index}"
            for index, _ in enumerate(evidence_refs, start=1)
        ),
        uncertainty_refs=(f"uncertainty:controlled:{case.case_id}",) if case.insufficient_evidence else (),
        conflict_refs=conflict_refs,
        temporal_refs=(f"temporal:controlled:{case.case_id}",),
        source_versions={"field": "luna.field_kernel.v1", "context": "context-foundation.v1"},
        world_state_kind_candidate="conflicted_world" if case.conflict else "partial_world",
        world_stability_candidate="UNKNOWN" if case.insufficient_evidence else "CANDIDATE",
        trace_ref=f"trace:current-world:controlled:{case.case_id}",
        provenance_refs=_unique((*evidence_refs, *event_refs, f"context:{case.case_id}")),
        candidate_only=True,
        field_mutation=False,
        field_entity_creation=False,
        field_confidence_mutation=False,
        field_transition=False,
        event_admission=False,
        reducer_invocation_as_mutation_authority=False,
        field_truth_declaration=False,
    )


class EvidenceContextFieldCurrentWorldControlledEngineV1:
    """Run the bounded evidence-to-representation seam without persistence."""

    def run(self) -> Dict[str, Any]:
        profile = valid_profile()
        results = []
        for case in build_evidence_context_field_current_world_cases_v1():
            records = case.authority_records or valid_authority_records()
            applicable = resolve_applicable_governance_set(profile, CORE_GOVERNANCE_RULE_REGISTRY_V1)
            preflight = run_governance_preflight(
                profile,
                CORE_GOVERNANCE_RULE_REGISTRY_V1,
                records,
                tuple(profile.protocol_refs),
            )
            evidence_objects = tuple(
                _evidence(case, index)
                for index in (1, 2)
                if case.scenario in {"both", "conflict"}
            )
            if not evidence_objects:
                evidence_objects = (_evidence(case, 1),)
            evidence_values: Tuple[Any, ...] = tuple(evidence_objects)
            if case.malformed_evidence:
                evidence_values = (_malformed_evidence(evidence_objects[0]),)
            elif case.malformed_lineage:
                evidence_values = (_lineage_broken_evidence(evidence_objects[0]),)

            context_error = None
            try:
                context = _context(case, str(_json_safe(evidence_values[0]).get("evidence_id", "")) if isinstance(_json_safe(evidence_values[0]), Mapping) else "")
            except ValueError as exc:
                context = None
                context_error = str(exc)
            candidate_results = []
            admission_results = []
            admitted_events = []
            replay_admission = None
            reducer_result = None
            reducer_batch_statuses: Tuple[str, ...] = ()
            field_state = None
            field_states: Tuple[FieldStateV1, ...] = ()
            event_candidate_values = []
            if preflight.status == "PASS" and not case.insufficient_evidence and not case.stale_evidence and context_error is None:
                for index, evidence in enumerate(evidence_values, start=1):
                    if case.context_mismatch:
                        context_ref = ""
                    else:
                        context_ref = CONTEXT_REF
                    formation = form_field_event_candidate_from_evidence(
                        evidence,
                        field_ref=case.field_ref,
                        context_ref=context_ref,
                        occurred_at=OBSERVED_AT,
                        observed_at=OBSERVED_AT,
                        received_at=OBSERVED_AT,
                        correction_refs=(f"correction:controlled:{case.case_id}",) if case.correction else (),
                        supersedes_ref=(f"event:prior:{case.case_id}" if case.reopened else ""),
                    )
                    candidate_results.append(formation)
                    if formation.event_candidate is None:
                        continue
                    event_candidate_values.append(formation.event_candidate)
                    if case.skip_event_admission:
                        continue
                    admission = admit_field_event(
                        formation.event_candidate,
                        AdmissionPolicyV1(evaluated_at=EVALUATED_AT),
                        AdmissionContextV1(),
                    )
                    admission_results.append(admission)
                    if admission.reducer_eligible:
                        adapter = FieldKernelReducerAdapterV1.adapt_admitted_event(admission)
                        admitted_events.append(dict(adapter.reducer_input_candidate))
                if case.duplicate_event and event_candidate_values:
                    replay_admission = admit_field_event(
                        event_candidate_values[0],
                        AdmissionPolicyV1(evaluated_at=EVALUATED_AT),
                        AdmissionContextV1(known_event_ids=(event_candidate_values[0].event_id,)),
                    )
                if admitted_events:
                    reducer_requests = (
                        (tuple(admitted_events),)
                        if case.scenario != "both"
                        else tuple((admitted_event,) for admitted_event in admitted_events)
                    )
                    reducer_results = []
                    for index, reducer_event_batch in enumerate(reducer_requests, start=1):
                        reducer_case = (
                            replace(case, case_id=f"{case.case_id}:{index}")
                            if case.scenario == "both"
                            else case
                        )
                        reducer_request = _reducer_request(
                            case=reducer_case,
                            field_ref=case.field_ref,
                            admitted_events=tuple(reducer_event_batch),
                            evidence_refs=tuple(
                                ref
                                for admitted_event in reducer_event_batch
                                for ref in (admitted_event.get("evidence_refs") or ())
                            ),
                        )
                        reducer_results.append(
                            module_result_to_dict(FieldStateReducerModuleV1.reduce(reducer_request))
                        )
                    reducer_batch_statuses = tuple(
                        _reducer_status_from_result(result)
                        for result in reducer_results
                    )
                    reducer_result = reducer_results[0]
                    for index, (one_result, source_event) in enumerate(zip(reducer_results, admitted_events), start=1):
                        candidate = one_result.get("field_state_candidate")
                        if isinstance(candidate, Mapping) and candidate:
                            field_states = (
                                *field_states,
                                _field_state_from_candidate(
                                    candidate,
                                    source_event,
                                    replace(case, case_id=f"{case.case_id}:{index}")
                                    if case.scenario == "both"
                                    else case,
                                ),
                            )
                    field_state = field_states[0] if field_states else None

            first_candidate = candidate_results[0] if candidate_results else None
            first_admission = admission_results[0] if admission_results else None
            event_status = (
                "NOT_ATTEMPTED"
                if first_candidate is None
                else "REQUIRES_ADMISSION"
                if case.skip_event_admission
                else first_admission.admission_status if first_admission else "NOT_ATTEMPTED"
            )
            candidate_status = (
                "NOT_EXECUTED"
                if preflight.status != "PASS" or case.insufficient_evidence
                else BLOCKED_STATUS
                if case.stale_evidence or case.malformed_lineage
                else _json_safe(first_candidate).get("formation_status", "NOT_ATTEMPTED")
                if first_candidate
                else "NOT_ATTEMPTED"
            )
            if case.malformed_evidence or case.context_mismatch or context_error is not None:
                candidate_status = "INVALID_INPUT"
            if reducer_result is not None:
                reducer_status = _aggregate_reducer_status(reducer_batch_statuses)
            elif case.insufficient_evidence:
                reducer_status = "NO_UPDATE"
            else:
                reducer_status = "NO_REDUCER"
            current_world_candidate = _current_world_candidate(
                case,
                context,
                field_states,
                tuple(str(_json_safe(item).get("evidence_id", "")) for item in evidence_values if isinstance(_json_safe(item), Mapping)),
                tuple(str(event.event_id) for event in event_candidate_values),
            )
            current_world_mapping = _json_safe(current_world_candidate)
            artifact = {
                "candidate_only": True,
                "read_only": True,
                "truth_declared": case.world_truth_attempt,
                "world_truth_declared": case.world_truth_attempt,
                "runtime_started": False,
                "execution_instance_created": False,
                "provider_session_started": False,
                "resource_allocated": False,
                "gateway_submission": False,
                "resource_allocation": False,
                "provider_invocation": False,
                "model_invocation": False,
                "field_state_mutated": False,
                "authoritative_effects": False,
                "mutation_effects": case.direct_mutation_attempt,
                "field_state_candidate_created": field_state is not None,
            }
            postflight = run_governance_postflight(profile, artifact) if preflight.status == "PASS" else None
            results.append(
                {
                    "case_id": case.case_id,
                    "expected": _json_safe(case),
                    "applicable_governance": _json_safe(applicable),
                    "governance_preflight": _json_safe(preflight),
                    "governance_postflight": _json_safe(postflight),
                    "business_engine_executed": preflight.status == "PASS",
                    "context_error": context_error,
                    "evidence": [_json_safe(item) for item in evidence_values],
                    "context": context,
                    "field_event_candidate": _json_safe(first_candidate.event_candidate if first_candidate else None),
                    "field_event_formation": _json_safe(first_candidate),
                    "field_event_admission": _json_safe(first_admission),
                    "replay_admission": _json_safe(replay_admission),
                    "reducer_result": reducer_result,
                    "reducer_batch_statuses": list(reducer_batch_statuses),
                    "reducer_module_status": str(_mapping(reducer_result).get("module_status") or "") if reducer_result else None,
                    "field_state": _json_safe(field_state),
                    "field_states": _json_safe(field_states),
                    "current_world": current_world_mapping,
                    "candidate_status": candidate_status,
                    "admission_status": event_status,
                    "reducer_status": reducer_status,
                    "field_ref": case.field_ref,
                    "event_count": len(admitted_events),
                    "field_state_count": len(field_states),
                    "artifact": artifact,
                    "behavior": {
                        "evidence_is_not_event": True,
                        "candidate_only": True,
                        "event_admitted": bool(first_admission and first_admission.reducer_eligible),
                        "reducer_is_single_mutation_authority": True,
                        "field_state_mutation_executed": False,
                        "context_reference_only": context is not None,
                        "context_truth_source": False,
                        "current_world_candidate_only": current_world_candidate is None or bool(current_world_candidate.candidate_only),
                        "unknown_preserved": case.insufficient_evidence,
                        "conflict_preserved": case.conflict,
                        "correction_lineage_preserved": case.correction,
                        "opaque_payload_preserved": all(
                            "opaque_payload_ref" in json_value.get("candidate_payload", {})
                            for json_value in [_json_safe(item) for item in evidence_values]
                            if isinstance(json_value, Mapping)
                        ),
                        "no_semantic_interpretation": True,
                        "no_world_truth": case.world_truth_attempt is False,
                        "no_memory_experience_decision_action": True,
                    },
                }
            )
        return {
            "phase": PHASE,
            "source_mode": EVALUATION_MARKER,
            "governance_backbone_reused": True,
            "canonical_field_state_type": "capabilities.cognitive_flow.field_kernel.core.field_state_v1.FieldStateV1",
            "canonical_field_reducer_owner": "Field State Reducer",
            "canonical_event_admission_owner": "Field Event Admission",
            "canonical_context_owner": "Context Foundation",
            "canonical_current_world_type": "CurrentWorldCandidateV1",
            "reducer_unique_mutation_authority": True,
            "bridge_semantic_authority": False,
            "synthetic_only": True,
            "controlled": True,
            "field_state_persisted": False,
            "current_world_mutated": False,
            "truth_declared": False,
            "world_truth_declared": False,
            "memory_mutated": False,
            "experience_mutated": False,
            "decision_executed": False,
            "task_executed": False,
            "action_executed": False,
            "provider_invoked": False,
            "model_invoked": False,
            "network_called": False,
            "subprocess_started": False,
            "thread_started": False,
            "socket_used": False,
            "gateway_called": False,
            "observation_demand_created": False,
            "cases": results,
            "controlled_case_count": len(results),
            "status": "READY_FOR_USER_VERIFICATION",
        }


PHASE = "Phase-Evidence-Context-Field-Current-World-Controlled-Integration-v1-001"


__all__ = ["EvidenceContextFieldCurrentWorldControlledEngineV1"]
