#!/usr/bin/env python3
"""Static V0/V2 contract verifier for the canonical architecture map.

The verifier checks only phase assets and contract boundaries. It does not run
runtime code, perform migrations, call models, access hardware, or execute
actions.
"""
import ast
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

MD_REQ = {
    "cognitive_architecture_canonical_model_v1.md": [
        "Cognitive Architecture Consolidation and Dependency Map v1", "Planning Only", "Required Dependency",
        "Optional Dependency", "Candidate Dependency", "Future Interface", "Canonical cognitive domains",
        "Reality / Evidence", "Field Network", "Self (Identity / Capability / State)", "Attention", "Workspace",
        "Drive / Value", "Situation / Hypothesis / Belief / Expectation", "Intent / Goal / Task", "Memory / Experience / Learning",
        "Reflex", "Emotion Context Boundary", "Brain", "Decision Candidate", "Decision Commitment", "Action Request Candidate",
        "Action Boundary", "Reality / Evidence → Field", "Field → Situation", "Global Cognitive State → Brain",
        "Brain → Decision Candidate → Decision Commitment", "Decision Commitment → Action Request Candidate → Action Boundary",
        "Outcome Evidence → Experience → Learning Candidates", "Learning → Reality write", "Emotion Context → Decision override",
        "Capability / Provider → Goal creation", "Provider → Brain Direct Access", "Model → Decision", "Hardware → Goal or Value mutation",
        "Action Boundary → Reality direct write", "Reality is updated only", "Current Evidence has priority",
        "Unknown and provenance are preserved", "Owner", "Writer", "Reader", "Reality: Evidence / Reality Update Pipeline",
        "Attention: Attention System", "Goal and Intent", "Decision: Brain", "Action: Action Boundary",
        "Experience and Learning", "Observe", "Represent", "Understand", "Hypothesize", "Evaluate", "Commit",
        "Prepare Action", "Feedback", "Learn", "Adapt", "No new module creation", "no Runtime implementation",
        "no Model Manager or Provider integration", "no Hardware integration", "no Action execution", "no automatic Learning",
        "no B Simulation", "no Emotion Runtime", "no authority inversion"
    ],
    "cognitive_architecture_whitebox_v1.md": [
        "Cognitive Architecture Consolidation Whitebox v1", "Who owns Reality", "Who owns Field", "Who owns Attention",
        "Who owns Goal and Intent", "Who owns Decision", "Who owns Action", "Who owns Experience and Learning",
        "Who owns Capability", "Evidence → Reality Update Candidate → Reducer", "Reality → Field → Situation / Hypothesis / Expectation",
        "Field + Self + Goal + Task + Attention → Workspace / Global State", "Workspace + Evidence + Candidates → Brain Evaluation",
        "Brain → Decision Candidate → Decision Commitment", "Decision Commitment → Action Request Candidate → Action Boundary",
        "Outcome Evidence → Experience → Learning Candidate", "Learning → Reality", "Emotion Context → Decision",
        "Capability → Goal", "Provider → Brain", "Model → Decision", "Hardware → Value", "Action Boundary → Reality",
        "Unknown", "Provenance", "Required", "Optional", "Candidate", "Future Interface", "reader write authority",
        "Runtime", "Scheduler", "Model", "Provider", "Hardware", "Action", "B Simulation", "automatic Learning"
    ],
    "cognitive_architecture_go_no_go_v1.md": [
        "Cognitive Architecture Consolidation Go / No-Go v1", "Canonical model", "module inventory", "Required",
        "Optional", "Candidate", "Future Interface", "Information-flow matrix", "Authority ownership matrix",
        "Owner", "Writer", "Reader", "Observe", "Represent", "Understand", "Hypothesize", "Evaluate", "Commit",
        "Prepare Action", "Feedback", "Learn", "Adapt", "Unknown", "Provenance", "No new cognitive module",
        "no Runtime implementation", "no model integration", "no hardware integration", "no Action execution",
        "no automatic Learning", "no B Simulation", "no Emotion Runtime", "Learning → Reality", "Emotion → Decision Override",
        "Capability → Goal Creation", "Provider → Brain Direct Access", "no ownership drift", "no hardcoded pass",
        "no deleted checks", "V0 static checks", "V1", "V2 Final Phase Verification", "User Terminal Only", "V3",
        "WAITING_FOR_USER_TERMINAL_VERIFICATION"
    ]
}

JSON_REQ = {
    "cognitive_module_dependency_graph_v1.json": [
        "Cognitive Module Dependency Graph v1", "canonical_module_dependency_graph", "Required Dependency",
        "Optional Dependency", "Candidate Dependency", "Future Interface", "reality_evidence", "field_network", "self",
        "attention", "situation", "hypothesis_belief_expectation", "workspace_global_state", "brain", "intent_goal_task",
        "decision_commitment", "action_boundary", "experience_learning", "governance_plane", "capability_plane", "cognitive_runtime",
        "Reality → Evidence → Field", "Field → Situation", "Situation → Hypothesis / Belief / Expectation",
        "Global Cognitive State → Brain", "Brain → Decision Candidate → Decision Commitment",
        "Decision Commitment → Action Request Candidate → Action Boundary", "Outcome Evidence → Experience → Learning Candidate",
        "Learning → Reality", "Emotion → Decision Override", "Capability → Goal Creation", "Provider → Brain Direct Access",
        "Model → Decision", "Hardware → Identity Mutation", "Action Boundary → Reality Direct Write", "unknowns_are_preserved",
        "provenance_is_preserved", "graph_is_descriptive_not_runtime"
    ],
    "cognitive_information_flow_matrix_v1.json": [
        "Cognitive Information Flow Matrix v1", "source_target_permission_matrix", "provide context", "update candidate",
        "read context", "request validation", "candidate output", "future interface", "forbidden", "Evidence",
        "Reality Update Pipeline", "Field", "Situation", "Learning", "Memory", "Brain", "Decision Commitment", "Action Boundary",
        "Outcome Evidence", "Emotion Context", "Capability", "Provider", "Model", "Reality Direct Write",
        "candidate_is_not_fact", "reader_does_not_gain_writer_authority", "reality_evidence_has_priority",
        "unknowns_are_preserved", "provenance_is_preserved", "matrix_does_not_execute_runtime"
    ],
    "cognitive_authority_ownership_matrix_v1.json": [
        "Cognitive Authority Ownership Matrix v1", "authority_ownership", "Reality", "Evidence / Reality Update Pipeline",
        "Reducer", "Field", "Field System", "Attention", "Attention System", "Goal", "Goal System + Brain Review",
        "Intent", "Intent Contract + Brain Review", "Decision", "Brain", "Decision Commitment", "Decision Governance",
        "Action", "Action Boundary", "Experience", "Experience System", "Learning", "Learning Governance", "Capability",
        "Capability Governance", "Protocol", "Protocol Governance", "owner_is_normative", "writer_must_be_explicit",
        "reader_has_no_implicit_write", "brain_does_not_own_reality", "provider_does_not_own_brain",
        "action_boundary_owns_execution", "unknowns_are_preserved"
    ],
    "cognitive_state_ownership_map_v1.json": [
        "Cognitive State Ownership Map v1", "Owner", "Writer", "Reader", "state_scope", "unknowns", "provenance",
        "Field State", "Self State", "Workspace State", "Attention State", "Hypothesis State", "Belief State",
        "Expectation State", "Goal State", "Task State", "Capability State", "one_normative_owner_per_state",
        "writer_must_be_authorized", "readers_cannot_write_by_reading", "state_transition_is_candidate_based",
        "unknowns_are_preserved", "provenance_is_preserved", "state_map_does_not_implement_runtime"
    ],
    "cognitive_loop_definition_v1.json": [
        "Cognitive Loop Definition v1", "Canonical Cognitive Loop", "Observe", "Represent", "Understand", "Hypothesize",
        "Evaluate", "Commit", "Prepare Action", "Feedback", "Learn", "Adapt", "Observe → Represent", "Represent → Understand",
        "Understand → Hypothesize", "Hypothesize → Evaluate", "Evaluate → Commit", "Commit → Prepare Action",
        "Prepare Action → Feedback", "Feedback → Learn", "Learn → Adapt", "Adapt → Observe", "commit_is_decision_commitment_candidate",
        "prepare_action_is_action_request_candidate_only", "feedback_is_evidence_candidate", "learn_is_candidate_based",
        "adapt_does_not_auto_modify_goal_or_value", "unknowns_are_preserved", "provenance_is_preserved",
        "Action Execution", "Model Runtime", "Hardware Runtime", "B Simulation Runtime", "Automatic Learning",
        "loop_is_definition_not_execution"
    ],
    "cognitive_boundary_audit_v1.json": [
        "Cognitive Architecture Boundary Audit v1", "static_architecture_boundary_audit", "Core", "Governance", "Capability",
        "Runtime", "Future", "Reality", "Field", "Brain", "Memory", "Learning", "Constitution", "Admission", "Registry",
        "Protocol", "Provider", "boundary_checks", "Core owns Self, Field, Brain, Memory, and Learning",
        "Governance owns Constitution, Admission, Registry, and Protocol", "Capability provides capability state/evidence only",
        "Provider cannot access Brain directly", "Learning cannot write Reality", "Emotion Context cannot override Decision",
        "Action Boundary retains execution authority", "Reducer retains Reality write authority", "Learning → Reality",
        "Emotion → Decision Override", "Capability → Goal Creation", "Provider → Brain Direct Access", "Model → Decision",
        "audit_is_static", "no_runtime_execution", "no_model_or_hardware_calls", "unknowns_are_preserved", "provenance_is_preserved"
    ],
    "cognitive_module_inventory_v1.json": [
        "Cognitive Module Inventory v1", "canonical architecture assets only", "inventory_is_not_runtime_input", "Core",
        "Governance", "Capability", "Runtime", "Future Interface", "Reality / Evidence", "Field / Role / Relationship",
        "Self", "Attention / Workspace", "Situation / Hypothesis / Belief / Expectation", "Intent / Goal / Task",
        "Brain / Decision Commitment", "Memory / Experience / Learning", "Reflex / Emotion Context Boundary",
        "Constitution / Governance Plane", "Capability / Model / Hardware / Provider", "Cognitive Runtime / Action Runtime",
        "B Simulation / Emotion Runtime", "no_new_cognitive_module", "module_inventory_is_governance_only",
        "baseline_is_not_runtime_input", "duplicate_ownership_requires_review", "unknowns_are_preserved", "provenance_is_preserved"
    ],
    "cognitive_interface_registry_v1.json": [
        "Cognitive Interface Registry v1", "canonical_interface_reference", "Required Dependency", "Optional Dependency",
        "Candidate Dependency", "Future Interface", "Evidence → Reality Update Pipeline", "Field → Situation", "Attention → Workspace",
        "Memory → Brain", "Brain → Decision Commitment", "Decision Commitment → Action Boundary", "Outcome → Experience / Learning",
        "Capability → Cognitive Core", "Provider → Brain Direct Access", "Model → Decision", "Capability → Goal Creation",
        "Learning → Reality", "Emotion → Decision Override", "Action Boundary → Reality Direct Write", "protocol_binding_required",
        "authority_binding_required", "candidate_output_is_not_authoritative_write", "unknowns_are_preserved",
        "provenance_is_preserved", "registry_does_not_execute"
    ],
    "cognitive_architecture_migration_map_v1.json": [
        "Cognitive Architecture Migration Map v1", "candidate_based_architecture_consolidation", "source_assets", "canonical_targets",
        "Field / Role / Relationship phases", "Self / Attention / Workspace phases", "Situation / Hypothesis / Expectation phases",
        "Intent / Goal / Task phases", "Brain / Decision Commitment phases", "Memory / Learning / Reflex phases",
        "Constitution / Governance / Capability phases", "canonical_target", "migration_status", "candidate", "no_automatic_migration",
        "no_asset_deletion", "no_rename_to_hide_failure", "preserve_provenance", "preserve_unknowns", "compatibility_review_required",
        "governance_approval_required", "runtime_changes_out_of_scope", "interface alias review", "duplicate schema review",
        "authority drift review", "Capability Runtime integration review"
    ]
}


def main() -> int:
    failures = []
    checks = 0
    for name, terms in MD_REQ.items():
        checks += 1
        path = BASE / name
        if not path.is_file():
            failures.append(f"missing required file: {name}")
            continue
        text = path.read_text()
        for term in terms:
            checks += 1
            if term not in text:
                failures.append(f"missing required contract term: {term} in {name}")
    for name, terms in JSON_REQ.items():
        checks += 1
        path = BASE / name
        try:
            text = path.read_text()
            json.loads(text)
        except Exception as exc:
            failures.append(f"JSON parse failure: {name}: {type(exc).__name__}")
            text = ""
        for term in terms:
            checks += 1
            if term not in text:
                failures.append(f"missing required JSON contract term: {term} in {name}")
    print(f"CHECKS: {checks}")
    print(f"FAILED_CHECKS: {failures}")
    print(f"PASSED_CHECK_COUNT: {checks - len(failures)}")
    print(f"FAILED_CHECK_COUNT: {len(failures)}")
    print(f"BLOCKER_COUNT: {len(failures)}")
    if failures:
        print("FINAL_DECISION: BLOCKED_BY_VERIFIER_FAILURE")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
