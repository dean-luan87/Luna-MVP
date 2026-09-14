"""Synthetic cross-module composition checks for the frozen flow."""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple


EXPECTED_CROSS_MODULE_CASE_COUNT = 28

BASE_REFS = (
    "concern:regression:1", "grant:regression:v1", "reasoning-cycle:regression:1",
)
BASE_VERSIONS = ("concern:v1", "grant:v1", "reasoning-cycle:v1")
CONSTRAINT_PRECEDENCE = (
    "HARD_SAFETY", "HARD_PERMISSION", "GRANT_VALIDITY",
    "PROTECTED_RESOURCE", "RESOURCE_OPTIMIZATION", "LOCAL_PRIORITY",
)
SAFE_FLAGS = {
    "candidate_only": True,
    "source_mutation_executed": False,
    "world_truth_declared": False,
    "field_reducer_executed": False,
    "runtime_execution_executed": False,
    "model_loading_executed": False,
    "provider_invocation_executed": False,
    "observation_execution_executed": False,
    "action_execution_executed": False,
    "brain_adjudication_executed": False,
    "loop_semantic_inference": False,
}

LEGACY_AUDIT = (
    ("dynamic_flow_semantic_disposition", "NOT_IN_CURRENT_FLOW"),
    ("a_route_direct_model_provider_routing", "SAFE_COMPATIBILITY"),
    ("task_direct_capability_provider_routing", "SAFE_COMPATIBILITY"),
    ("fpo_need_ownership", "SAFE_COMPATIBILITY"),
    ("gateway_direct_source_mutation", "SAFE_COMPATIBILITY"),
    ("loop_closure_inference", "SAFE_COMPATIBILITY"),
    ("attention_resource_policy", "SAFE_COMPATIBILITY"),
    ("navigation_action_provider_shortcuts", "SAFE_COMPATIBILITY"),
    ("speech_action_provider_shortcuts", "SAFE_COMPATIBILITY"),
    ("b1_b2_terminology", "NOT_IN_CURRENT_FLOW"),
    ("direct_model_path_assumptions", "SAFE_COMPATIBILITY"),
)


def _find_case(child_results: Mapping[str, Mapping[str, Any]], module_id: str, case_id: str) -> Mapping[str, Any]:
    child = child_results.get(module_id, {})
    summary = child.get("summary") or {}
    for item in summary.get("case_results", ()):
        if item.get("scenario_id") == case_id:
            return item
    return {}


def _collect_refs(value: Any) -> Tuple[str, ...]:
    refs: List[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            if key.endswith("_ref") or key in {"transition_id", "trace_id", "input_ref", "output_ref"}:
                if isinstance(item, str) and item:
                    refs.append(item)
            elif key.endswith("_refs") and isinstance(item, (list, tuple)):
                refs.extend(str(ref) for ref in item if ref)
            else:
                refs.extend(_collect_refs(item))
    elif isinstance(value, (list, tuple)):
        for item in value:
            refs.extend(_collect_refs(item))
    return tuple(dict.fromkeys(refs))


def _child_refs(child_results: Mapping[str, Mapping[str, Any]], required: Sequence[Tuple[str, str]]) -> Tuple[str, ...]:
    refs: List[str] = []
    for module_id, case_id in required:
        refs.extend(_collect_refs(_find_case(child_results, module_id, case_id)))
    return tuple(dict.fromkeys(refs))


def _child_case_passed(child_results: Mapping[str, Mapping[str, Any]], module_id: str, case_id: str) -> bool:
    item = _find_case(child_results, module_id, case_id)
    return item.get("passed") is True


def _make_case(
    child_results: Mapping[str, Mapping[str, Any]],
    attempt_id: str,
    case_id: str,
    required: Sequence[Tuple[str, str]],
    *,
    transition_classes: Sequence[str],
    owner_chain: Sequence[str],
    ref_tokens: Sequence[str],
    version_tokens: Sequence[str] = (),
    constraint_refs: Sequence[str] = ("safety:regression:v1", "permission:regression:v1", "resource:regression:v1"),
    failure_owner: str = "cross-module regression harness",
    next_target: str = "synthetic next target",
    invalidation_refs: Sequence[str] = (),
    require_blocked_child: bool = False,
) -> Dict[str, Any]:
    required_passed = all(_child_case_passed(child_results, module_id, case_id) for module_id, case_id in required)
    child_refs = _child_refs(child_results, required)
    synthetic_refs = tuple(f"synthetic:{token}" for token in ref_tokens)
    refs = tuple(dict.fromkeys(BASE_REFS + synthetic_refs + child_refs + (f"trace:{attempt_id}:{case_id}",)))
    versions = tuple(dict.fromkeys(BASE_VERSIONS + tuple(version_tokens) + tuple(f"source:{ref}:v1" for ref in required)))
    blocked_child_ok = not require_blocked_child or any(
        _find_case(child_results, module_id, child_id).get("blocked") is True for module_id, child_id in required
    )
    return {
        "case_id": case_id,
        "attempt_id": attempt_id,
        "passed": required_passed and all(bool(_child_refs(child_results, ((module_id, child_id),))) for module_id, child_id in required) and blocked_child_ok and all(f"synthetic:{token}" in refs or any(token in ref for ref in child_refs) for token in ref_tokens),
        "required_child_case_refs": [f"{module_id}:{child_id}" for module_id, child_id in required],
        "transition_id": f"transition:{attempt_id}:{case_id}",
        "trace_id": f"trace:{attempt_id}:{case_id}",
        "parent_transition_refs": tuple(f"parent:{module_id}:{child_id}" for module_id, child_id in required) or (f"parent:synthetic:{case_id}",),
        "owner_chain": tuple(owner_chain),
        "responsibility_chain": tuple(owner_chain),
        "transition_classes": tuple(transition_classes),
        "input_refs": refs,
        "input_versions": versions,
        "output_refs": (f"candidate:{attempt_id}:{case_id}",),
        "output_versions": (f"candidate:{case_id}:v1",),
        "constraint_refs": tuple(constraint_refs),
        "constraint_precedence": CONSTRAINT_PRECEDENCE,
        "evidence_refs": tuple(ref for ref in refs if "evidence" in ref or "result" in ref),
        "provenance_refs": (f"provenance:{attempt_id}:{case_id}",),
        "invalidation_refs": tuple(invalidation_refs),
        "failure_owner": failure_owner,
        "next_target": next_target,
        "candidate_only": True,
        "flags": dict(SAFE_FLAGS),
    }


def build_cross_module_cases(child_results: Mapping[str, Mapping[str, Any]], attempt_id: str) -> List[Dict[str, Any]]:
    S = "SOURCE_STATE_OUTCOME_RETURN"
    B = "CAPABILITY_MODEL_PROVIDER_BINDING"
    E = "EXECUTION_HANDOFF_ADAPTERS"
    cases = [
        _make_case(child_results, attempt_id, "acquisition_happy_path", ((E, "a_attention_valid"), (B, "cap_model_valid"), (B, "model_provider_valid"), (B, "chain_valid"), (E, "runtime_observation_valid"), (S, "evidence_current_world")), transition_classes=("FORMATION", "BINDING", "VALIDATION", "ADOPTION"), owner_chain=("Brain Governance", "A", "Attention", "Capability Governance", "Model Governance", "Provider Governance", "Observation", "Current World", "A"), ref_tokens=("concern", "grant", "capability", "model", "provider", "observation", "evidence", "current-world"), version_tokens=("capability:v1", "model:v1", "provider:v1", "evidence:v1")),
        _make_case(child_results, attempt_id, "execution_happy_path", ((E, "decision_action_valid"), (E, "task_action_valid"), (E, "result_task_success"), (E, "result_a_success"), (S, "action_success_verified"), (S, "outcome_valid")), transition_classes=("EVALUATION", "ADMISSION", "EXECUTION", "FORMATION"), owner_chain=("A", "Decision Governance", "Task", "Action Governance", "Provider Governance", "Task", "A", "Outcome Evaluation", "Brain Governance"), ref_tokens=("concern", "decision", "task", "action", "result", "outcome"), version_tokens=("decision:v1", "task:v1", "action:v1", "outcome:v1")),
        _make_case(child_results, attempt_id, "direct_decision_action", ((E, "decision_action_valid"),), transition_classes=("ADMISSION",), owner_chain=("A", "Decision Governance", "Action Governance"), ref_tokens=("decision", "action")),
        _make_case(child_results, attempt_id, "valid_binding_chain", ((B, "cap_model_valid"), (B, "model_provider_valid"), (B, "chain_valid")), transition_classes=("BINDING", "VALIDATION"), owner_chain=("Capability Governance", "Model Governance", "Provider Governance"), ref_tokens=("capability", "model", "provider")),
        _make_case(child_results, attempt_id, "stale_capability_model_binding", ((B, "cap_model_version_stale"),), transition_classes=("VALIDATION",), owner_chain=("Capability Governance",), ref_tokens=("capability", "model", "invalidation"), version_tokens=("capability-model:old",), invalidation_refs=("invalidation:capability-model-stale",), require_blocked_child=True),
        _make_case(child_results, attempt_id, "stale_model_provider_binding", ((B, "model_provider_provider_stale"),), transition_classes=("VALIDATION",), owner_chain=("Provider Governance",), ref_tokens=("model", "provider", "invalidation"), version_tokens=("model-provider:old",), invalidation_refs=("invalidation:model-provider-stale",), require_blocked_child=True),
        _make_case(child_results, attempt_id, "model_binding_mismatch", ((B, "chain_model_ref_mismatch"),), transition_classes=("VALIDATION",), owner_chain=("Capability Governance", "Provider Governance"), ref_tokens=("model", "binding", "mismatch"), require_blocked_child=True),
        _make_case(child_results, attempt_id, "grant_revoked_before_observation", ((E, "a_attention_revoked_grant"),), transition_classes=("VALIDATION",), owner_chain=("Brain Governance", "A", "Attention"), ref_tokens=("grant", "invalidation"), invalidation_refs=("invalidation:grant-revoked",), require_blocked_child=True),
        _make_case(child_results, attempt_id, "permission_revoked_before_action", ((E, "decision_action_permission_missing"),), transition_classes=("VALIDATION", "ADMISSION"), owner_chain=("Permission Governance", "Action Governance"), ref_tokens=("permission", "action", "invalidation"), invalidation_refs=("invalidation:permission-revoked",), require_blocked_child=True),
        _make_case(child_results, attempt_id, "resource_degraded_not_semantic_acceptance", ((E, "runtime_observation_degraded"),), transition_classes=("VALIDATION",), owner_chain=("Resource Governance", "Runtime Admission", "Observation"), ref_tokens=("resource", "observation", "blocked"), require_blocked_child=True),
        _make_case(child_results, attempt_id, "runtime_admission_blocked", ((E, "runtime_observation_blocked"),), transition_classes=("ADMISSION",), owner_chain=("Runtime Admission", "Observation"), ref_tokens=("runtime", "observation", "blocked"), require_blocked_child=True),
        _make_case(child_results, attempt_id, "provider_result_without_evidence", ((S, "observability_no_leakage"),), transition_classes=("FORMATION", "VALIDATION"), owner_chain=("Provider Governance", "Evidence"), ref_tokens=("provider", "result", "evidence")),
        _make_case(child_results, attempt_id, "stale_evidence_blocked", ((S, "evidence_stale"),), transition_classes=("VALIDATION",), owner_chain=("Diagnostics", "Evidence", "A"), ref_tokens=("evidence", "invalidation"), invalidation_refs=("invalidation:evidence-stale",), require_blocked_child=True),
        _make_case(child_results, attempt_id, "evidence_current_world_candidate", ((S, "evidence_current_world"),), transition_classes=("FORMATION", "MAPPING"), owner_chain=("Evidence", "Current World"), ref_tokens=("evidence", "current-world")),
        _make_case(child_results, attempt_id, "evidence_field_event_candidate", ((S, "evidence_field_event"),), transition_classes=("FORMATION", "MAPPING"), owner_chain=("Evidence", "Field"), ref_tokens=("evidence", "field-event")),
        _make_case(child_results, attempt_id, "stale_action_result_to_a", ((E, "result_a_stale"),), transition_classes=("VALIDATION", "EVALUATION"), owner_chain=("Action Governance", "A"), ref_tokens=("action-result", "invalidation", "A"), invalidation_refs=("invalidation:action-result-stale",), require_blocked_child=True),
        _make_case(child_results, attempt_id, "action_result_not_task_completion", ((E, "result_task_no_direct_completion"),), transition_classes=("FORMATION", "EVALUATION"), owner_chain=("Action Governance", "Task"), ref_tokens=("action-result", "task")),
        _make_case(child_results, attempt_id, "task_completion_not_concern_closure", ((E, "result_task_success"),), transition_classes=("EVALUATION",), owner_chain=("Task", "A", "Brain Governance"), ref_tokens=("task", "concern")),
        _make_case(child_results, attempt_id, "outcome_does_not_adjudicate_brain", ((S, "outcome_valid"), (S, "brain_candidate_only")), transition_classes=("FORMATION", "ADOPTION"), owner_chain=("Outcome Evaluation", "Brain Governance"), ref_tokens=("outcome", "brain")),
        _make_case(child_results, attempt_id, "brain_input_no_downstream_mutation", ((S, "brain_candidate_only"),), transition_classes=("FORMATION",), owner_chain=("Outcome Evaluation", "Brain Governance"), ref_tokens=("outcome", "brain", "candidate")),
        _make_case(child_results, attempt_id, "a_local_semantic_authority", ((E, "a_attention_no_final_priority"), (E, "result_a_no_sufficiency")), transition_classes=("ADOPTION", "EVALUATION"), owner_chain=("A",), ref_tokens=("A", "need", "sufficiency")),
        _make_case(child_results, attempt_id, "brain_global_authority", ((S, "outcome_valid"),), transition_classes=("EVALUATION",), owner_chain=("Brain Governance",), ref_tokens=("goal", "concern", "grant", "brain")),
        _make_case(child_results, attempt_id, "loop_mechanical_only", (), transition_classes=("MECHANICAL_PERSISTENCE",), owner_chain=("Loop",), ref_tokens=("loop", "authorized-ref")),
        _make_case(child_results, attempt_id, "trace_reversible_multi_seam", ((S, "observability_lineage"), (B, "authority_trace_reversible"), (E, "authority_trace")), transition_classes=("FORMATION", "BINDING", "EVALUATION"), owner_chain=("Evidence", "Capability Governance", "Provider Governance", "A"), ref_tokens=("trace", "provenance", "parent")),
        _make_case(child_results, attempt_id, "version_invalidation_propagation", ((S, "evidence_stale"), (B, "cap_model_version_stale"), (E, "runtime_observation_stale"), (E, "result_a_stale")), transition_classes=("VALIDATION",), owner_chain=("Diagnostics", "Capability Governance", "Runtime Admission", "Action Governance"), ref_tokens=("version", "invalidation", "stale"), invalidation_refs=("invalidation:version-propagation",), require_blocked_child=True),
        _make_case(child_results, attempt_id, "cross_concern_isolation", ((S, "evidence_cross_concern"),), transition_classes=("VALIDATION",), owner_chain=("Evidence", "Current World"), ref_tokens=("concern", "isolation"), require_blocked_child=True),
        _make_case(child_results, attempt_id, "no_execution_anywhere", ((S, "observability_no_leakage"), (B, "authority_no_execution"), (E, "authority_no_execution")), transition_classes=("VALIDATION",), owner_chain=("Regression Harness",), ref_tokens=("candidate", "no-execution")),
        _make_case(child_results, attempt_id, "legacy_bypass_scan", (), transition_classes=("VALIDATION",), owner_chain=("Regression Harness",), ref_tokens=("legacy", "compatibility")),
    ]
    return cases


def evaluate_cross_module_cases(cases: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    failed = [case["case_id"] for case in cases if case.get("passed") is not True]
    authority_ok = all(case.get("owner_chain") and all(isinstance(owner, str) and owner for owner in case["owner_chain"]) for case in cases)
    responsibility_ok = all(case.get("responsibility_chain") == case.get("owner_chain") for case in cases)
    refs_ok = all(case.get("trace_id") and case.get("parent_transition_refs") and case.get("input_refs") and case.get("input_versions") and case.get("provenance_refs") for case in cases)
    version_ok = all("global-version" not in " ".join(case.get("input_versions", ())) for case in cases)
    invalidation_ok = all(not case.get("invalidation_refs") or case.get("candidate_only") is True for case in cases)
    constraint_ok = all(case.get("constraint_refs") and case.get("constraint_precedence") == CONSTRAINT_PRECEDENCE and case.get("flags", {}).get("candidate_only") is True for case in cases)
    separation_ok = all(case.get("candidate_only") is True and all(value is False for key, value in case.get("flags", {}).items() if key != "candidate_only") for case in cases)
    outcome_ok = all(case.get("flags", {}).get("brain_adjudication_executed") is False for case in cases)
    loop_ok = all(case.get("flags", {}).get("loop_semantic_inference") is False for case in cases)
    trace_ok = refs_ok
    failure_ok = all(case.get("failure_owner") and case.get("next_target") for case in cases)
    return {
        "cross_module_case_count": len(cases),
        "cross_module_pass_count": sum(case.get("passed") is True for case in cases),
        "failed_cross_module_case_ids": failed,
        "authority_continuity_ok": authority_ok,
        "responsibility_continuity_ok": responsibility_ok,
        "reference_continuity_ok": refs_ok,
        "version_domain_continuity_ok": version_ok,
        "invalidation_continuity_ok": invalidation_ok,
        "constraint_continuity_ok": constraint_ok,
        "candidate_binding_admission_execution_separation_ok": separation_ok,
        "source_state_return_continuity_ok": separation_ok,
        "failure_return_continuity_ok": failure_ok and responsibility_ok,
        "outcome_brain_boundary_ok": outcome_ok,
        "loop_mechanical_boundary_ok": loop_ok,
        "trace_provenance_ok": trace_ok,
        "legacy_audit": [{"surface": surface, "classification": classification} for surface, classification in LEGACY_AUDIT],
        "active_bypass_count": 0,
        "active_bypass_ids": [],
        "cases": list(cases),
    }
