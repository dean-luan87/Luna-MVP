"""V0 static contract verifier for the Cognitive Goal Architecture phase."""
from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
JSON_FILES = [
    "goal_schema.json", "goal_type_registry.json", "goal_source_contract.json",
    "goal_hierarchy_contract.json", "goal_priority_contract.json",
    "goal_lifecycle_contract.json", "goal_candidate_contract.json",
    "goal_self_governance_contract.json", "goal_task_relation.json",
    "goal_memory_relation.json", "goal_schema_relation.json",
    "goal_value_boundary.json", "ownership_registry.json",
    "dependency_boundary.json", "negative_guards.json", "summary.json",
]
MD_FILES = ["cognitive_goal_architecture.md", "goal_hierarchy_model.md", "goal_governance_model.md", "implementation_plan.md"]
VERIFIER = "verify_cognitive_goal_architecture_v1.py"


def load(name: str) -> dict:
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
    assets: dict[str, dict] = {}
    for name in JSON_FILES:
        try:
            assets[name] = load(name)
            check(isinstance(assets[name], dict), f"json_object:{name}")
        except (OSError, json.JSONDecodeError):
            check(False, f"json_parse:{name}")
    for name in MD_FILES:
        try:
            check((ROOT / name).read_text(encoding="utf-8").strip() != "", f"markdown_nonempty:{name}")
        except OSError:
            check(False, f"markdown_read:{name}")
    try:
        ast.parse((ROOT / VERIFIER).read_text(encoding="utf-8"))
        check(True, "verifier_ast")
    except (OSError, SyntaxError):
        check(False, "verifier_ast")

    schema = assets["goal_schema.json"]
    check({"goal_id", "goal_type", "source", "desired_state", "field_ref", "lifecycle_state", "priority_candidate", "provenance", "unknowns"} <= set(schema["required"]), "schema_fields")
    check(schema["goal_is_task"] is False and schema["goal_is_desire"] is False and schema["candidate_only"] is True and schema["self_governance_required"] is True and schema["action_execution"] is False, "schema_boundary")

    types = assets["goal_type_registry.json"]
    expected_types = {"Existence Goal", "Capability Goal", "Social Goal", "Task Goal"}
    check({x["name"] for x in types["types"]} == expected_types, "goal_type_coverage")
    check([x["level"] for x in types["types"]] == [0, 1, 2, 3], "goal_levels")
    check(types["candidate_required"] is True and types["automatic_generation"] is False and types["goal_is_not_task"] is True and types["goal_is_not_desire"] is True, "goal_type_boundary")

    sources = assets["goal_source_contract.json"]
    expected_sources = {"Self-Originated Goal", "User-Originated Goal", "Environment-Originated Goal", "System-Originated Goal"}
    check(set(sources["sources"]) == expected_sources, "goal_sources")
    check(sources["source_is_provenance_not_authority"] is True and sources["candidate_only"] is True and sources["self_governance_required"] is True and sources["automatic_goal_generation"] is False, "source_boundary")

    hierarchy = assets["goal_hierarchy_contract.json"]
    check([x["name"] for x in hierarchy["levels"]] == ["Existence Goal", "Capability Goal", "Social Goal", "Task Goal"], "hierarchy_order")
    check(hierarchy["lower_level_cannot_violate_higher_level"] is True and hierarchy["task_goal_connects_task_manager"] is True and hierarchy["task_manager_is_not_goal_owner"] is True and hierarchy["goal_does_not_execute"] is True, "hierarchy_boundary")

    priority = assets["goal_priority_contract.json"]
    check(set(priority["inputs"]) == {"Safety", "Self Preservation", "User Need", "Capability State", "Resource Cost", "Time Constraint"}, "priority_inputs")
    check(priority["output"] == "Goal Priority Candidate" and priority["algorithm_implemented"] is False and priority["candidate_only"] is True and priority["self_review_required"] is True and priority["priority_does_not_execute"] is True, "priority_boundary")

    lifecycle = assets["goal_lifecycle_contract.json"]
    check(lifecycle["states"] == ["Detected", "Candidate", "Evaluated", "Admitted", "Active", "Progressing", "Completed", "Expired", "Archived"], "lifecycle_states")
    check(lifecycle["automatic_transition"] is False and lifecycle["governance_admission_required"] is True and lifecycle["runtime_implemented"] is False, "lifecycle_boundary")

    candidate = assets["goal_candidate_contract.json"]
    check(set(candidate["inputs"]) == {"Field", "Intent", "Drive", "Value Context", "Self State", "Capability State", "Task Context", "Memory Context", "Schema Context"}, "candidate_inputs")
    check(set(candidate["required_review"]) == {"reasonability", "capability", "resource", "stability", "Constitution"}, "candidate_review")
    check(candidate["candidate_only"] is True and candidate["automatic_goal_creation"] is False and candidate["automatic_goal_adjustment"] is False and candidate["action_execution"] is False, "candidate_boundary")

    self_governance = assets["goal_self_governance_contract.json"]
    check(self_governance["owner"] == "Self" and self_governance["controller"] == "Self Goal Governance", "self_owner")
    check(set(self_governance["outputs"]) == {"Approved Goal", "Rejected Goal", "Deferred Goal", "Revised Goal Candidate"}, "self_outputs")
    check(set(self_governance["review"]) == {"reasonability", "capability boundary", "resource cost", "system stability", "Constitution compliance"}, "self_review")
    check({"modify_identity", "modify_value", "modify_constitution", "rewrite_brain_rules", "modify_reality", "direct_action", "automatic_goal_generation", "automatic_goal_adjustment"} <= set(self_governance["forbidden"]), "self_forbidden")

    relation = assets["goal_task_relation.json"]
    check(relation["flow"] == ["Goal", "Task", "Decision Candidate", "Action Boundary"], "goal_task_flow")
    check(relation["goal_is_not_task"] is True and relation["task_manager_reuse_required"] is True and relation["task_does_not_modify_goal"] is True and relation["goal_does_not_direct_action"] is True, "goal_task_boundary")
    check(relation["parallel_task_manager_forbidden"] is True and relation["parallel_goal_manager_forbidden"] is True and relation["action_execution"] is False, "manager_duplication_guard")

    memory = assets["goal_memory_relation.json"]
    check(memory["memory_can_create_goal_automatically"] is False and memory["memory_can_modify_goal"] is False and memory["current_reality_precedence"] is True and memory["candidate_only"] is True, "memory_boundary")
    schema_relation = assets["goal_schema_relation.json"]
    check(schema_relation["schema_can_create_goal_automatically"] is False and schema_relation["schema_can_modify_goal"] is False and schema_relation["current_evidence_precedence"] is True and schema_relation["candidate_only"] is True, "schema_boundary")
    value = assets["goal_value_boundary.json"]
    check(value["interface_status"] == "reserved" and value["value_creates_goal_directly"] is False and value["value_modifies_goal_directly"] is False and value["value_implementation"] is False, "value_boundary")

    ownership = assets["ownership_registry.json"]
    owners = [x["owner"] for x in ownership["ownership"]]
    required_owners = {"Self", "Goal Layer", "Value Layer", "Task Manager", "Brain", "Runtime", "Memory", "Schema", "Field"}
    check(ownership["unique_owner_required"] is True and len(owners) == len(set(owners)), "unique_owners")
    check(required_owners <= set(owners), "ownership_coverage")
    check(all(x.get("writer") and x.get("reader") for x in ownership["ownership"]), "ownership_writer_reader")

    dependency = assets["dependency_boundary.json"]
    forbidden = set(dependency["forbidden_dependencies"])
    required_forbidden = {"Goal -> Direct Action", "Task -> Modify Goal", "Memory -> Create Goal Automatically", "Emotion -> Modify Goal", "B Route -> Override Current Goal", "Goal -> Ignore Self Boundary"}
    check(required_forbidden <= forbidden, "dependency_forbidden")
    check(dependency["no_parallel_task_manager"] is True and dependency["no_parallel_goal_manager"] is True and dependency["goal_runtime"] is False and dependency["action_execution"] is False and dependency["model_integration"] is False, "dependency_boundary")

    guards = assets["negative_guards.json"]
    required_guards = {"goal_direct_action", "task_modify_goal", "memory_automatic_goal", "emotion_modify_goal", "b_route_override_goal", "goal_ignore_self_boundary", "goal_runtime", "automatic_goal_generation", "automatic_goal_adjustment", "task_execution", "action_execution", "emotion_runtime", "b_route", "model_calls", "provider_calls", "hardware_control", "parallel_task_manager", "parallel_goal_manager"}
    check(required_guards <= set(guards["forbidden"]), "negative_guards")
    check(guards["goal_is_not_task"] is True and guards["goal_is_not_desire"] is True and guards["candidate_only"] is True and guards["self_governance_required"] is True and guards["no_check_weaken"] is True and guards["no_hardcoded_pass"] is True, "negative_invariants")

    summary = assets["summary.json"]
    check(summary["status"] == "architecture_only" and summary["readiness_token"] == "LUNA_COGNITIVE_GOAL_ARCHITECTURE_READY", "summary_status")
    check(summary["goal_types"] == ["Existence Goal", "Capability Goal", "Social Goal", "Task Goal"] and summary["goal_sources"] == ["Self-Originated Goal", "User-Originated Goal", "Environment-Originated Goal", "System-Originated Goal"], "summary_taxonomy")
    check(summary["lifecycle"] == ["Detected", "Candidate", "Evaluated", "Admitted", "Active", "Progressing", "Completed", "Expired", "Archived"], "summary_lifecycle")
    check(summary["task_manager_reuse"] is True and summary["runtime"] is False and summary["goal_runtime"] is False and summary["automatic_goal_generation"] is False and summary["automatic_goal_adjustment"] is False and summary["action_execution"] is False, "summary_boundary")
    check(len(summary["reusable_assets"]) >= 4 and len(summary["parallel_risks"]) >= 3 and len(summary["migration_mapping"]) >= 2, "summary_inventory")

    forbidden_imports = {"subprocess", "socket", "requests", "cv2", "torch", "transformers", "sqlite3", "psycopg2"}
    try:
        tree = ast.parse((ROOT / VERIFIER).read_text(encoding="utf-8"))
        imports = {n.names[0].name.split(".")[0] for n in ast.walk(tree) if isinstance(n, ast.Import) and n.names}
        imports |= {n.module.split(".")[0] for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) and n.module}
        check(not imports & forbidden_imports, "verifier_no_runtime_imports")
    except (OSError, SyntaxError):
        check(False, "verifier_no_runtime_imports")

    blockers = len(failed)
    print(f"CHECKS: {checks}")
    print(f"FAILED_CHECKS: {failed}")
    print(f"PASSED_CHECK_COUNT: {checks - blockers}")
    print(f"FAILED_CHECK_COUNT: {blockers}")
    print(f"BLOCKER_COUNT: {blockers}")
    if blockers:
        print("FINAL_DECISION: BLOCKED_BY_VERIFIER_FAILURE")
        print("READINESS: LUNA_COGNITIVE_GOAL_ARCHITECTURE_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_COGNITIVE_GOAL_ARCHITECTURE_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
