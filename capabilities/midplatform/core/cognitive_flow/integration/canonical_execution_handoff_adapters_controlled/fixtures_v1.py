"""Synthetic fixtures for the five canonical execution handoff seams."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Optional

from capabilities.midplatform.core.cognitive_flow.integration.logical_capability_to_runtime_admission_candidate_adapter_controlled.logical_capability_runtime_admission_types_v1 import ExecutableCapabilityCandidateV1, RuntimeAdmissionAssessmentCandidateV1

from .types_v1 import ACognitiveRequirementInputV1, ActionResultInputV1, DecisionActionInputV1, RuntimeObservationInputV1, TaskActionInputV1


@dataclass(frozen=True)
class HandoffScenarioV1:
    scenario_id: str
    category: str
    description: str
    expected_blocked: bool
    expected_failure: Optional[str] = None
    focus: Optional[str] = None


CONCERN = "concern:synthetic:1"
REASONING = "reasoning-cycle:synthetic:1"
NEED = "need:synthetic:1"
REQUIREMENT = "cognitive-requirement:synthetic:1"
CAPABILITY = "capability:object-detection"
MODEL_BINDING = "binding:capability-model:synthetic"
PROVIDER_BINDING = "binding:model-provider:synthetic"


def _a_input(scenario_id: str, **changes: object) -> ACognitiveRequirementInputV1:
    data = ACognitiveRequirementInputV1(
        concern_ref=CONCERN, reasoning_cycle_ref=REASONING, cognitive_need_ref=NEED,
        cognitive_requirement_ref=REQUIREMENT, target_ref="target:synthetic:entrance",
        expected_evidence_refs=("evidence:detection",), semantic_relevance_refs=("relevance:entrance",),
        role_refs=("role:observer",), perspective_refs=("perspective:field",), task_refs=("task:synthetic",),
        context_refs=("context:synthetic",), safety_refs=("safety:v1",), permission_refs=("permission:sensor:v1",),
        resource_refs=("resource:vision:v1",), grant_ref="grant:synthetic:v1",
        source_version_refs=("concern:v1", "need:v1", "requirement:v1"), invalidation_refs=(), status="CURRENT",
        trace_refs=(f"trace:a-attention:{scenario_id}",), provenance_refs=(f"prov:fixture:{scenario_id}",),
    )
    return replace(data, **changes)


def _assessment(*, status: str = "READY_FOR_EXECUTABLE_CANDIDATE", stale: tuple[str, ...] = ()) -> RuntimeAdmissionAssessmentCandidateV1:
    return RuntimeAdmissionAssessmentCandidateV1(
        admission_candidate_ref="runtime-admission:synthetic", logical_resolution_ref="logical-resolution:synthetic",
        logical_capability_ref=CAPABILITY, capability_slot_ref="slot:vision", model_asset_ref="model:yolo11n",
        model_version_ref="model-version:yolo11n:v1", governed_model_path_ref="ref:model:yolo11n",
        declared_checksum_ref="declared:checksum:yolo11n:v1", observed_integrity_evidence_ref="integrity:evidence:v1",
        dependency_health_refs=("dependency:verified",), device_runtime_health_refs=("device:verified",),
        provider_compatibility_refs=(PROVIDER_BINDING,), permission_refs=("permission:sensor:v1",), resource_refs=("resource:vision:v1",), safety_refs=("safety:v1",),
        source_acquisition_context_ref="context:synthetic", source_state_version_ref="source-state:v1",
        admission_status=status, admitted_model_asset_ref="model:yolo11n" if status == "READY_FOR_EXECUTABLE_CANDIDATE" else None,
        admitted_provider_compatibility_ref=PROVIDER_BINDING if status == "READY_FOR_EXECUTABLE_CANDIDATE" else None,
        blocking_reason_refs=(), evidence_refs=("integrity:evidence:v1",), valid_state_version_ref="source-state:v1",
        expiry_staleness_refs=stale, trace_refs=("trace:runtime:synthetic",), provenance_refs=("prov:runtime:synthetic",),
    )


def _executable(*, stale: tuple[str, ...] = (), capability: str = CAPABILITY) -> ExecutableCapabilityCandidateV1:
    return ExecutableCapabilityCandidateV1(
        executable_capability_ref="executable-capability:synthetic", admission_candidate_ref="runtime-admission:synthetic",
        logical_resolution_ref="logical-resolution:synthetic", logical_capability_ref=capability, capability_slot_ref="slot:vision",
        admitted_model_asset_ref="model:yolo11n", admitted_model_version_ref="model-version:yolo11n:v1", governed_model_path_ref="ref:model:yolo11n",
        admitted_provider_compatibility_ref=PROVIDER_BINDING, source_acquisition_context_ref="context:synthetic",
        source_state_version_ref="source-state:v1", permission_refs=("permission:sensor:v1",), resource_refs=("resource:vision:v1",), safety_refs=("safety:v1",),
        valid_state_version_ref="source-state:v1", expiry_staleness_refs=stale, trace_refs=("trace:executable:synthetic",), provenance_refs=("prov:executable:synthetic",),
    )


def _runtime_input(scenario_id: str, **changes: object) -> RuntimeObservationInputV1:
    executable = _executable()
    assessment = _assessment()
    data = RuntimeObservationInputV1(
        executable_candidate=executable, runtime_assessment=assessment, cognitive_requirement_ref=REQUIREMENT, concern_ref=CONCERN,
        attention_refs=("attention-input:synthetic",), target_refs=("target:synthetic:entrance",), focus_refs=("focus:entrance",),
        grant_refs=("grant:synthetic:v1",), permission_refs=("permission:sensor:v1",), safety_refs=("safety:v1",), resource_refs=("resource:vision:v1",),
        model_binding_ref=MODEL_BINDING, provider_binding_ref=PROVIDER_BINDING, expected_capability_ref=CAPABILITY,
        expected_model_binding_ref=MODEL_BINDING, expected_provider_binding_ref=PROVIDER_BINDING,
        source_version_refs=("requirement:v1", "executable:v1", "runtime-admission:v1"), invalidation_refs=(), permission_status="GRANTED",
        trace_refs=(f"trace:runtime-observation:{scenario_id}",), provenance_refs=(f"prov:fixture:{scenario_id}",),
    )
    return replace(data, **changes)


def _decision_input(scenario_id: str, **changes: object) -> DecisionActionInputV1:
    data = DecisionActionInputV1(
        decision_ref="decision:synthetic:1", decision_version="decision:v1", decision_status="APPROVED", concern_ref=CONCERN,
        intent_ref="intent:synthetic:1", action_type="SPEAK_CANDIDATE", target_ref="target:user:1", precondition_refs=("precondition:ready",),
        permission_refs=("permission:speech:v1",), safety_refs=("safety:speech:v1",), resource_refs=("resource:speech:v1",), grant_refs=("grant:synthetic:v1",),
        confirmation_refs=("confirmation:not-required",), idempotency_refs=("idempotency:decision:1",), source_version_refs=("decision:v1", "intent:v1"),
        invalidation_refs=(), trace_refs=(f"trace:decision-action:{scenario_id}",), provenance_refs=(f"prov:fixture:{scenario_id}",),
    )
    return replace(data, **changes)


def _task_input(scenario_id: str, **changes: object) -> TaskActionInputV1:
    data = TaskActionInputV1(
        task_ref="task:synthetic:1", task_version="task:v1", task_status="READY", source_decision_ref="decision:synthetic:1",
        action_type="SPEAK_CANDIDATE", target_ref="target:user:1", dependency_refs=(), blocker_refs=(), precondition_refs=("precondition:ready",),
        permission_refs=("permission:speech:v1",), safety_refs=("safety:speech:v1",), resource_refs=("resource:speech:v1",), grant_refs=("grant:synthetic:v1",),
        source_version_refs=("task:v1", "decision:v1"), invalidation_refs=(), trace_refs=(f"trace:task-action:{scenario_id}",), provenance_refs=(f"prov:fixture:{scenario_id}",),
    )
    return replace(data, **changes)


def _result_input(scenario_id: str, **changes: object) -> ActionResultInputV1:
    data = ActionResultInputV1(
        action_result_ref="action-result:synthetic:1", action_result_version="action-result:v1", task_ref="task:synthetic:1", concern_ref=CONCERN,
        status="SUCCESS", progress_refs=("progress:0.8",), completion_evidence_refs=("completion-evidence:candidate",), effect_evidence_refs=("effect-evidence:candidate",),
        failure_refs=(), source_state_update_refs=("source-update:candidate",), uncertainty_refs=(), partiality="COMPLETE_CANDIDATE",
        source_version_refs=("action-result:v1", "task:v1", "source-state:v1"), invalidation_refs=(), trace_refs=(f"trace:action-result:{scenario_id}",), provenance_refs=(f"prov:fixture:{scenario_id}",),
        action_execution_executed=False,
    )
    return replace(data, **changes)


SCENARIOS = (
    HandoffScenarioV1("a_attention_valid", "A_ATTENTION", "valid Requirement handoff", False),
    HandoffScenarioV1("a_attention_missing_need", "A_ATTENTION", "missing Need ref", True, "COGNITIVE_NEED_MISSING"),
    HandoffScenarioV1("a_attention_missing_requirement", "A_ATTENTION", "missing Requirement ref", True, "COGNITIVE_REQUIREMENT_MISSING"),
    HandoffScenarioV1("a_attention_stale", "A_ATTENTION", "stale Requirement", True, "A_REQUIREMENT_STALE"),
    HandoffScenarioV1("a_attention_revoked_grant", "A_ATTENTION", "revoked Grant", True, "GRANT_REVOKED"),
    HandoffScenarioV1("a_attention_optional_refs", "A_ATTENTION", "Role/Context optional refs preserved", False, focus="optional_refs"),
    HandoffScenarioV1("a_attention_no_final_priority", "A_ATTENTION", "A does not assign final priority", False, focus="no_final_priority"),
    HandoffScenarioV1("a_attention_need_immutable", "A_ATTENTION", "A cannot mutate Need", False, focus="need_immutable"),
    HandoffScenarioV1("runtime_observation_valid", "RUNTIME_OBSERVATION", "executable candidate valid", False),
    HandoffScenarioV1("runtime_observation_missing_executable", "RUNTIME_OBSERVATION", "executable candidate missing", True, "EXECUTABLE_CAPABILITY_MISSING"),
    HandoffScenarioV1("runtime_observation_blocked", "RUNTIME_OBSERVATION", "Runtime Admission blocked", True, "RUNTIME_ADMISSION_NOT_READY"),
    HandoffScenarioV1("runtime_observation_degraded", "RUNTIME_OBSERVATION", "Runtime Admission degraded", True, "RUNTIME_ADMISSION_NOT_READY"),
    HandoffScenarioV1("runtime_observation_stale", "RUNTIME_OBSERVATION", "Runtime Admission stale", True, "RUNTIME_ADMISSION_STALE"),
    HandoffScenarioV1("runtime_observation_capability_mismatch", "RUNTIME_OBSERVATION", "capability mismatch", True, "CAPABILITY_REF_MISMATCH"),
    HandoffScenarioV1("runtime_observation_model_binding_mismatch", "RUNTIME_OBSERVATION", "model binding mismatch", True, "BINDING_REF_MISMATCH"),
    HandoffScenarioV1("runtime_observation_source_stale", "RUNTIME_OBSERVATION", "source version stale", True, "SOURCE_VERSION_STALE"),
    HandoffScenarioV1("runtime_observation_permission_revoked", "RUNTIME_OBSERVATION", "permission revoked", True, "PERMISSION_REVOKED"),
    HandoffScenarioV1("runtime_observation_not_executed", "RUNTIME_OBSERVATION", "Observation not executed", False, focus="not_executed"),
    HandoffScenarioV1("decision_action_valid", "DECISION_ACTION", "valid bounded direct Action handoff", False),
    HandoffScenarioV1("decision_action_not_approved", "DECISION_ACTION", "Decision not approved", True, "DECISION_REJECTED"),
    HandoffScenarioV1("decision_action_revoked", "DECISION_ACTION", "Decision revoked", True, "DECISION_REVOKED"),
    HandoffScenarioV1("decision_action_superseded", "DECISION_ACTION", "Decision superseded", True, "DECISION_SUPERSEDED"),
    HandoffScenarioV1("decision_action_stale", "DECISION_ACTION", "stale Decision", True, "DECISION_STALE_OR_REVOKED"),
    HandoffScenarioV1("decision_action_target_missing", "DECISION_ACTION", "target missing", True, "ACTION_TARGET_OR_PRECONDITION_MISSING"),
    HandoffScenarioV1("decision_action_permission_missing", "DECISION_ACTION", "permission missing/revoked", True, "ACTION_CONSTRAINT_REF_MISSING"),
    HandoffScenarioV1("decision_action_safety_blocked", "DECISION_ACTION", "safety blocked", True, "ACTION_CONSTRAINT_REF_MISSING"),
    HandoffScenarioV1("decision_action_not_executed", "DECISION_ACTION", "Action not admitted/executed", False, focus="not_executed"),
    HandoffScenarioV1("task_action_valid", "TASK_ACTION", "valid Task Action handoff", False),
    HandoffScenarioV1("task_action_not_ready", "TASK_ACTION", "Task not ready", True, "TASK_NOT_READY"),
    HandoffScenarioV1("task_action_dependency_blocked", "TASK_ACTION", "dependency blocked", True, "TASK_DEPENDENCY_BLOCKED"),
    HandoffScenarioV1("task_action_stale", "TASK_ACTION", "Task stale", True, "TASK_STALE"),
    HandoffScenarioV1("task_action_decision_missing", "TASK_ACTION", "source Decision missing", True, "SOURCE_DECISION_MISSING"),
    HandoffScenarioV1("task_action_target_missing", "TASK_ACTION", "target missing", True, "ACTION_TARGET_MISSING"),
    HandoffScenarioV1("task_action_not_executed", "TASK_ACTION", "Task does not execute Action", False, focus="not_executed"),
    HandoffScenarioV1("result_task_success", "RESULT_TASK", "successful result to Task", False),
    HandoffScenarioV1("result_task_partial", "RESULT_TASK", "partial result to Task", False),
    HandoffScenarioV1("result_task_failed", "RESULT_TASK", "failed result to Task", False),
    HandoffScenarioV1("result_a_success", "RESULT_A", "successful result to A", False),
    HandoffScenarioV1("result_a_uncertain", "RESULT_A", "uncertain result to A", False),
    HandoffScenarioV1("result_a_stale", "RESULT_A", "stale result blocked", True, "ACTION_RESULT_STALE"),
    HandoffScenarioV1("result_task_no_direct_completion", "RESULT_TASK", "result does not mark Task complete directly", False, focus="no_direct_completion"),
    HandoffScenarioV1("result_a_no_sufficiency", "RESULT_A", "result does not set Sufficiency directly", False, focus="no_sufficiency"),
    HandoffScenarioV1("authority_owners", "AUTHORITY", "all authority owners preserved", False, focus="owners"),
    HandoffScenarioV1("authority_responsibilities", "AUTHORITY", "all responsibility owners preserved", False, focus="responsibilities"),
    HandoffScenarioV1("authority_trace", "AUTHORITY", "trace/provenance reversible", False, focus="trace"),
    HandoffScenarioV1("authority_versions", "AUTHORITY", "version lineage preserved", False, focus="versions"),
    HandoffScenarioV1("authority_invalidation", "AUTHORITY", "invalidation preserved", True, "A_REQUIREMENT_STALE", focus="invalidation"),
    HandoffScenarioV1("authority_no_execution", "AUTHORITY", "no runtime/action/provider execution", False, focus="no_execution"),
)


def a_input_for(scenario_id: str) -> ACognitiveRequirementInputV1:
    changes: dict[str, object] = {}
    if scenario_id == "a_attention_missing_need": changes["cognitive_need_ref"] = None
    if scenario_id == "a_attention_missing_requirement": changes["cognitive_requirement_ref"] = None
    if scenario_id == "a_attention_stale": changes.update(status="STALE", invalidation_refs=("invalidation:requirement-stale",))
    if scenario_id == "a_attention_revoked_grant": changes["grant_ref"] = "grant:revoked:v1"
    if scenario_id == "authority_invalidation": changes.update(status="STALE", invalidation_refs=("invalidation:authority-check",))
    return _a_input(scenario_id, **changes)


def runtime_input_for(scenario_id: str) -> RuntimeObservationInputV1:
    changes: dict[str, object] = {}
    if scenario_id == "runtime_observation_missing_executable": changes.update(executable_candidate=None, runtime_assessment=None)
    if scenario_id == "runtime_observation_blocked": changes["runtime_assessment"] = _assessment(status="ADMISSION_BLOCKED_PERMISSION")
    if scenario_id == "runtime_observation_degraded": changes["runtime_assessment"] = _assessment(status="DEGRADED_CANDIDATE")
    if scenario_id == "runtime_observation_stale": changes["runtime_assessment"] = _assessment(status="STALE_ADMISSION_CANDIDATE", stale=("stale:runtime",))
    if scenario_id == "runtime_observation_capability_mismatch": changes["expected_capability_ref"] = "capability:other"
    if scenario_id == "runtime_observation_model_binding_mismatch": changes["expected_model_binding_ref"] = "binding:capability-model:other"
    if scenario_id == "runtime_observation_source_stale": changes.update(executable_candidate=replace(_executable(), valid_state_version_ref="source-state:old"), invalidation_refs=("invalidation:source-version-stale",))
    if scenario_id == "runtime_observation_permission_revoked": changes.update(permission_status="REVOKED", permission_refs=("permission:revoked:v1",))
    return _runtime_input(scenario_id, **changes)


def decision_input_for(scenario_id: str) -> DecisionActionInputV1:
    changes: dict[str, object] = {}
    if scenario_id == "decision_action_not_approved": changes["decision_status"] = "REJECTED"
    if scenario_id == "decision_action_revoked": changes["decision_status"] = "REVOKED"
    if scenario_id == "decision_action_superseded": changes["decision_status"] = "SUPERSEDED"
    if scenario_id == "decision_action_stale": changes.update(decision_status="APPROVED", invalidation_refs=("invalidation:decision-stale",))
    if scenario_id == "decision_action_target_missing": changes.update(target_ref=None, precondition_refs=())
    if scenario_id == "decision_action_permission_missing": changes["permission_refs"] = ()
    if scenario_id == "decision_action_safety_blocked": changes["safety_refs"] = ()
    return _decision_input(scenario_id, **changes)


def task_input_for(scenario_id: str) -> TaskActionInputV1:
    changes: dict[str, object] = {}
    if scenario_id == "task_action_not_ready": changes["task_status"] = "BLOCKED"
    if scenario_id == "task_action_dependency_blocked": changes["dependency_refs"] = ("dependency:blocked",)
    if scenario_id == "task_action_stale": changes["invalidation_refs"] = ("invalidation:task-stale",)
    if scenario_id == "task_action_decision_missing": changes["source_decision_ref"] = None
    if scenario_id == "task_action_target_missing": changes["target_ref"] = None
    return _task_input(scenario_id, **changes)


def result_input_for(scenario_id: str) -> ActionResultInputV1:
    changes: dict[str, object] = {}
    if scenario_id == "result_task_partial": changes.update(status="PARTIAL", partiality="PARTIAL_CANDIDATE")
    if scenario_id == "result_task_failed": changes.update(status="FAILED", failure_refs=("failure:action:candidate",), partiality="FAILED_CANDIDATE")
    if scenario_id == "result_a_uncertain": changes.update(status="UNCERTAIN", uncertainty_refs=("uncertainty:effect",), partiality="UNCERTAIN_CANDIDATE")
    if scenario_id == "result_a_stale": changes.update(status="SUCCESS", invalidation_refs=("invalidation:action-result-stale",))
    if scenario_id == "result_a_no_sufficiency": changes.update(effect_evidence_refs=(), partiality="UNCERTAIN_CANDIDATE")
    return _result_input(scenario_id, **changes)
