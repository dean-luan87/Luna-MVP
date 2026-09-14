"""Static final-phase contract verifier for Cognitive Field temporal evolution."""
from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
JSON_FILES = [
    "field_identity_schema.json",
    "field_snapshot_schema.json",
    "field_transition_schema.json",
    "field_transition_matrix.json",
    "field_event_contract.json",
    "field_evolution_history_schema.json",
    "field_temporal_continuity_contract.json",
    "field_relation_contract.json",
    "field_memory_binding_contract.json",
    "field_self_role_binding_contract.json",
    "ownership_registry.json",
    "dependency_boundary.json",
    "negative_guards.json",
    "summary.json",
]
MD_FILES = [
    "field_temporal_evolution_architecture.md",
    "field_transition_model.md",
    "implementation_plan.md",
    "field_temporal_evolution_whitebox_v1.md",
    "field_temporal_evolution_go_no_go_v1.md",
]
VERIFIER = "verify_field_temporal_evolution_architecture_v1.py"


def read_json(name: str) -> dict:
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def main() -> int:
    checks = 0
    failed: list[str] = []

    def check(condition: bool, label: str) -> None:
        nonlocal checks
        checks += 1
        if not condition:
            failed.append(label)

    files = {p.name for p in ROOT.iterdir() if p.is_file()}
    check(set(JSON_FILES) | set(MD_FILES) | {VERIFIER} <= files, "required_assets")
    check({p.name for p in ROOT.glob("*.py")} == {VERIFIER}, "no_runtime_python")
    assets = {name: read_json(name) for name in JSON_FILES}
    for name in JSON_FILES:
        check(isinstance(assets[name], dict), f"json_object:{name}")
    for name in MD_FILES:
        check((ROOT / name).read_text(encoding="utf-8").strip() != "", f"markdown_nonempty:{name}")
    try:
        ast.parse((ROOT / VERIFIER).read_text(encoding="utf-8"))
        check(True, "verifier_ast")
    except SyntaxError:
        check(False, "verifier_ast")

    identity = assets["field_identity_schema.json"]
    dimensions = {"Spatial Continuity", "Temporal Continuity", "Entity Continuity", "Task Continuity", "Role Continuity"}
    check(set(identity["continuity_dimensions"]) == dimensions, "identity_dimensions")
    check(identity["candidate_only"] is True and identity["is_reality"] is False and identity["world_model"] is False, "identity_candidate_boundary")
    check(identity["identity_confirmation"] is False and identity["unknown_preserved"] is True, "identity_unknown")

    snapshot = assets["field_snapshot_schema.json"]
    required_snapshot = {"environment", "entities", "relations", "task", "role", "self_state", "attention_state", "relevant_memory_context"}
    check(required_snapshot <= set(snapshot["fields"]), "snapshot_components")
    check(snapshot["snapshot_is_current"] is True and snapshot["snapshot_is_memory"] is False and snapshot["snapshot_is_reality"] is False, "snapshot_boundary")
    check(snapshot["immutable_reference"] is True and snapshot["field_runtime_write"] is False, "snapshot_immutable")

    transition = assets["field_transition_schema.json"]
    transition_types = {"Stable", "Changed", "Expanded", "Merged", "Split", "Expired", "Replaced"}
    check(set(transition["transition_types"]) == transition_types, "transition_types")
    check(transition["candidate_only"] is True and transition["direct_field_mutation"] is False and transition["direct_action"] is False, "transition_boundary")
    check(transition["direct_memory_write"] is False, "transition_memory_boundary")

    matrix = assets["field_transition_matrix.json"]
    check({item["from"] for item in matrix["allowed_transitions"]} == transition_types, "transition_matrix_coverage")
    check(matrix["transition_is_candidate"] is True and matrix["execution"] is False and matrix["runtime_state_change"] is False, "transition_matrix_candidate")
    check(matrix["review_required"] is True, "transition_matrix_review")

    event = assets["field_event_contract.json"]
    check(event["flow"] == ["Reality Event", "Field Event Candidate", "Field Update Candidate", "Field State Change Candidate"], "event_flow")
    check(set(event["outputs"]) >= {"field_event_candidate", "field_update_candidate", "unknowns"}, "event_outputs")
    check(event["direct_field_runtime_write"] is False and event["direct_reality_write"] is False and event["direct_action"] is False, "event_no_mutation")

    history = assets["field_evolution_history_schema.json"]
    check(history["ordered_history"] is True and history["history_is_memory"] is False and history["history_overwrites_reality"] is False, "history_boundary")
    check(history["candidate_only"] is True and history["append_requires_evidence"] is True and history["memory_consolidation_externalized"] is True, "history_candidate")

    continuity = assets["field_temporal_continuity_contract.json"]
    check(set(continuity["continuity_inputs"]) == {"spatial_continuity", "temporal_continuity", "entity_continuity", "task_continuity", "role_continuity"}, "continuity_inputs")
    check(continuity["same_field_is_candidate"] is True and continuity["time_order_required"] is True and continuity["evidence_required"] is True, "continuity_candidate")
    check(continuity["prediction"] is False and continuity["world_model"] is False and continuity["future_state_inference"] is False, "continuity_no_prediction")

    relation = assets["field_relation_contract.json"]
    check({item["target"] for item in relation["relations"]} == {"Self", "Role", "Memory", "Knowledge"}, "relation_targets")
    check(relation["relation_is_candidate"] is True and relation["field_owns_other_modules"] is False and relation["direct_mutation"] is False, "relation_boundary")

    memory = assets["field_memory_binding_contract.json"]
    check(memory["snapshot_is_memory"] is False and memory["memory_is_field_owner"] is False, "memory_snapshot_boundary")
    check(memory["field_forces_memory_mutation"] is False and memory["memory_forces_field_mutation"] is False, "memory_no_forced_mutation")
    check(memory["current_reality_precedence"] is True and memory["candidate_only"] is True, "memory_current_precedence")

    self_role = assets["field_self_role_binding_contract.json"]
    check({"self_state", "self_capability_boundary", "active_role", "role_responsibility", "task_context"} <= set(self_role["inputs"]), "self_role_inputs")
    check(self_role["self_owns_field"] is False and self_role["role_owns_field"] is False and self_role["field_assigns_identity"] is False, "self_role_ownership")
    check(self_role["candidate_only"] is True and self_role["direct_self_mutation"] is False and self_role["direct_role_mutation"] is False, "self_role_candidate")

    ownership = assets["ownership_registry.json"]
    owners = [item["owner"] for item in ownership["ownership"]]
    check(ownership["unique_owner_required"] is True and len(owners) == len(set(owners)), "unique_owners")
    check({"Cognitive Field", "Field Temporal Evolution", "Memory", "Self Regulation", "Role", "Runtime"} <= set(owners), "ownership_required")
    check(all(item.get("writer") for item in ownership["ownership"]), "writers_declared")

    boundary = assets["dependency_boundary.json"]
    check(boundary["no_parallel_field_implementation"] is True and boundary["no_parallel_memory_implementation"] is True, "no_parallel_implementations")
    check(boundary["architecture_only"] is True and len(boundary["existing_assets_reused"]) >= 5, "reuse_mapping")
    forbidden_dependencies = set(boundary["forbidden_dependencies"])
    check("Field Evolution -> Direct Memory Mutation" in forbidden_dependencies and "Field Transition -> Direct Action" in forbidden_dependencies, "dependency_memory_action")
    check("Field History -> Reality Overwrite" in forbidden_dependencies and "Prediction -> Replace Reality" in forbidden_dependencies, "dependency_reality_prediction")

    guards = assets["negative_guards.json"]
    required_guards = {"runtime_implementation", "field_runtime", "world_model", "b_route_simulation", "prediction_engine", "action_execution", "automatic_learning", "memory_consolidation_runtime", "emotion_runtime", "field_evolution_direct_memory_mutation", "field_transition_direct_action", "field_history_overwrites_reality", "memory_forces_field_change", "prediction_replaces_reality", "parallel_field_implementation", "parallel_memory_implementation"}
    check(required_guards <= set(guards["forbidden"]), "negative_guards")
    check(guards["identity_must_remain_candidate"] is True and guards["snapshot_is_not_memory"] is True and guards["unknown_preserved"] is True and guards["evidence_required_for_history"] is True, "negative_invariants")
    check(guards["no_check_weaken"] is True and guards["no_hardcoded_pass"] is True, "negative_verifier_guards")

    summary = assets["summary.json"]
    check(summary["status"] == "architecture_only", "summary_status")
    check(summary["readiness_token"] == "LUNA_COGNITIVE_FIELD_TEMPORAL_EVOLUTION_ARCHITECTURE_READY", "summary_readiness")
    check(summary["snapshot_is_memory"] is False and summary["runtime_active"] is False and summary["world_model"] is False, "summary_boundary")
    check(summary["canonical_flow"] == ["Reality Event", "Field Event Candidate", "Field Update Candidate", "Field Snapshot", "Field Transition Candidate", "Evolution History Candidate"], "summary_flow")

    forbidden_imports = {"subprocess", "socket", "requests", "cv2", "torch", "transformers"}
    try:
        tree = ast.parse((ROOT / VERIFIER).read_text(encoding="utf-8"))
        imports = {node.names[0].name.split(".")[0] for node in ast.walk(tree) if isinstance(node, ast.Import) and node.names}
        imports |= {node.module.split(".")[0] for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module}
        check(not imports & forbidden_imports, "verifier_no_runtime_imports")
    except SyntaxError:
        check(False, "verifier_no_runtime_imports")

    blockers = len(failed)
    print(f"CHECKS: {checks}")
    print(f"FAILED_CHECKS: {failed}")
    print(f"PASSED_CHECK_COUNT: {checks - blockers}")
    print(f"FAILED_CHECK_COUNT: {blockers}")
    print(f"BLOCKER_COUNT: {blockers}")
    if blockers:
        print("FINAL_DECISION: BLOCKED_BY_VERIFIER_FAILURE")
        print("READINESS: LUNA_COGNITIVE_FIELD_TEMPORAL_EVOLUTION_ARCHITECTURE_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_COGNITIVE_FIELD_TEMPORAL_EVOLUTION_ARCHITECTURE_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
