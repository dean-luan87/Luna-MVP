"""V0 static verifier for Luna Self / Social Self Architecture Refactoring.

Planning Only: validates conceptual ownership mappings without executing
Runtime, Emotion, Role, Social, Memory migration, or code refactoring.
"""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
JSON_ASSETS = (
    "self_layer_definition_v1.json", "social_self_layer_definition_v1.json",
    "self_social_boundary_contract_v1.json", "internal_external_cognition_mapping_v1.json",
    "self_social_integration_contract_v1.json", "emotion_boundary_reclassification_v1.json",
    "role_system_ownership_mapping_v1.json", "relationship_system_mapping_v1.json",
    "constitution_self_mapping_v1.json", "module_migration_mapping_v1.json",
    "architecture_conflict_update_v1.json", "future_extension_boundary_v2.json",
)
MD_ASSETS = (
    "luna_self_social_self_architecture_refactoring_v1.md",
    "self_social_refactoring_whitebox_v1.md",
    "self_social_refactoring_go_no_go_v1.md",
)


def main() -> int:
    failures: list[str] = []
    checks = 0

    def check(condition: bool, name: str) -> None:
        nonlocal checks
        checks += 1
        if not condition:
            failures.append(name)

    data: dict[str, dict] = {}
    for name in JSON_ASSETS:
        path = BASE / name
        check(path.is_file(), f"missing_json:{name}")
        if path.is_file():
            try:
                data[name] = json.loads(path.read_text(encoding="utf-8"))
                check(True, f"json_parse:{name}")
            except (OSError, json.JSONDecodeError):
                check(False, f"json_parse:{name}")
    for name in MD_ASSETS:
        path = BASE / name
        check(path.is_file(), f"missing_md:{name}")
        if path.is_file():
            check(bool(path.read_text(encoding="utf-8", errors="replace").strip()), f"nonempty_md:{name}")

    self_layer = data.get("self_layer_definition_v1.json", {})
    social = data.get("social_self_layer_definition_v1.json", {})
    boundary = data.get("self_social_boundary_contract_v1.json", {})
    cognition = data.get("internal_external_cognition_mapping_v1.json", {})
    integration = data.get("self_social_integration_contract_v1.json", {})
    emotion = data.get("emotion_boundary_reclassification_v1.json", {})
    role = data.get("role_system_ownership_mapping_v1.json", {})
    relationship = data.get("relationship_system_mapping_v1.json", {})
    constitution = data.get("constitution_self_mapping_v1.json", {})
    migration = data.get("module_migration_mapping_v1.json", {})
    conflicts = data.get("architecture_conflict_update_v1.json", {})
    future = data.get("future_extension_boundary_v2.json", {})

    self_components = [row.get("component") for row in self_layer.get("components", [])]
    check(self_layer.get("layer") == "Self Layer", "self_layer_name")
    check({"Self Identity", "Self Capability", "Self Boundary", "Self Resource", "Self Regulation", "Self Evolution"}.issubset(set(self_components)), "self_components")
    check(all(row.get("answers") and row.get("owns") for row in self_layer.get("components", [])), "self_component_fields")
    check(set(["Social Role", "Relationship", "External Evaluation", "Social Norm"]).issubset(set(self_layer.get("forbidden_domains", []))), "self_social_forbidden")
    check(self_layer.get("rules", {}).get("identity_continuity") is True, "self_identity_continuity")
    check(self_layer.get("rules", {}).get("social_concerns_externalized") is True, "self_social_externalized")

    social_components = [row.get("component") for row in social.get("components", [])]
    check(social.get("layer") == "Social Self Layer", "social_layer_name")
    check({"Social Identity", "Role System", "Relationship System", "Social Norm", "Responsibility System", "Social Adaptation"}.issubset(set(social_components)), "social_components")
    check(all(row.get("answers") and row.get("owns") for row in social.get("components", [])), "social_component_fields")
    check(set(["Core Identity Rewrite", "Constitution Modification", "Self Boundary Rewrite"]).issubset(set(social.get("forbidden_domains", []))), "social_core_forbidden")
    check(social.get("rules", {}).get("role_is_contextual") is True, "social_role_contextual")
    check(social.get("rules", {}).get("identity_continuity_preserved") is True, "social_identity_continuity")

    boundary_rows = boundary.get("boundaries", [])
    boundary_names = [row.get("boundary") for row in boundary_rows]
    check({"Core Identity", "Self Capability", "Role", "Relationship", "Constitution", "Decision"}.issubset(set(boundary_names)), "boundary_concepts")
    check(len(boundary_names) == len(set(boundary_names)), "boundary_unique")
    check(all(row.get("owner") and row.get("integration_access") is not None for row in boundary_rows), "boundary_fields")
    check(set(["Social Self → Core Identity Rewrite", "Social Self → Constitution Modification", "Integration → Direct Decision", "Integration → Direct Action"]).issubset(set(boundary.get("forbidden_edges", []))), "boundary_forbidden_edges")
    check(boundary.get("rules", {}).get("self_social_non_overwrite") is True, "boundary_non_overwrite")
    check(boundary.get("rules", {}).get("integration_candidate_only") is True, "boundary_integration_candidate")

    check(cognition.get("flow") == ["Internal Cognition", "External Cognition", "Brain Integration", "Decision"], "cognition_flow")
    modes = {row.get("mode"): row for row in cognition.get("modes", [])}
    check({"Internal Cognition", "External Cognition", "Brain Integration"}.issubset(modes), "cognition_modes")
    check(modes.get("Internal Cognition", {}).get("owner") == "Self Layer", "internal_owner")
    check(modes.get("External Cognition", {}).get("owner") == "Cognitive Field + Social Self Layer", "external_owner")
    check(modes.get("Brain Integration", {}).get("owner") == "Brain", "integration_brain_owner")
    check(cognition.get("rules", {}).get("internal_external_distinct") is True, "cognition_distinct")
    check(cognition.get("rules", {}).get("brain_integrates") is True, "cognition_brain_integration")

    check(integration.get("owner") == "Cognitive Integration Layer", "integration_owner")
    check(integration.get("flow") == ["Self State", "Social State", "Integration Assessment", "Context Package", "Brain Review", "Possible Candidate Update"], "integration_flow")
    check(set(["Integration Context Candidate", "Self Update Candidate", "Social Adaptation Candidate", "Emotion Context Candidate"]).issubset(set(integration.get("outputs", []))), "integration_outputs")
    check(set(["Direct Self Mutation", "Direct Social Decision", "Direct Brain Override", "Direct Action"]).issubset(set(integration.get("cannot", []))), "integration_forbidden")
    check(integration.get("rules", {}).get("candidate_only") is True, "integration_candidate_only")
    check(integration.get("rules", {}).get("brain_review_required") is True, "integration_brain_review")

    check(emotion.get("new_owner") == "Self-Social Interaction / Integration Layer", "emotion_new_owner")
    check(emotion.get("status") == "context_boundary_only", "emotion_status")
    check(emotion.get("flow") == ["Social Event", "Social Self Interpretation", "Emotion State Candidate", "Integration", "Possible Self/Social Candidate Update"], "emotion_flow")
    check(set(["Direct Decision", "Direct Action", "Value Rewrite", "Identity Rewrite"]).issubset(set(emotion.get("cannot", []))), "emotion_forbidden")
    check(emotion.get("rules", {}).get("no_emotion_runtime") is True, "emotion_no_runtime")
    check(emotion.get("rules", {}).get("integration_context_only") is True, "emotion_context_only")

    check(role.get("owner") == "Social Self Layer", "role_owner")
    check(role.get("role_definition") and role.get("lifecycle") == ["Created", "Active", "Background", "Suspended", "Closed"], "role_definition_lifecycle")
    check(role.get("rules", {}).get("role_is_contextual") is True, "role_contextual")
    check(role.get("rules", {}).get("identity_continuity") is True, "role_identity_boundary")
    check("Role → Identity Rewrite" in role.get("forbidden", []), "role_forbidden")

    check(relationship.get("owner") == "Social Self Layer", "relationship_owner")
    check(relationship.get("states") == ["Initial", "Developing", "Stable", "Changed", "Unknown", "Archived"], "relationship_states")
    check(set(["Participants", "Field", "Time", "Interaction History", "Evidence", "Confidence"]).issubset(set(relationship.get("relationship_context", []))), "relationship_context")
    check(relationship.get("rules", {}).get("relationship_is_candidate") is True, "relationship_candidate")
    check(relationship.get("rules", {}).get("unknown_preserved") is True, "relationship_unknown")

    check(constitution.get("constitution_owner") == "L0 System Constitution", "constitution_owner")
    check(constitution.get("rules", {}).get("constitution_top_level") is True, "constitution_top_level")
    check(constitution.get("rules", {}).get("self_read_only") is True, "constitution_self_read_only")
    check(constitution.get("rules", {}).get("social_self_read_only") is True, "constitution_social_read_only")
    check(set(["Self → Constitution Modification", "Social Self → Constitution Modification", "Integration → Constitution Modification"]).issubset(set(constitution.get("forbidden", []))), "constitution_forbidden")

    mapping_rows = migration.get("mappings", [])
    check(migration.get("migration_type") == "conceptual_ownership_mapping_only", "migration_conceptual_only")
    check(len(mapping_rows) >= 9, "migration_rows")
    check(all(row.get("existing_module") and row.get("new_owner") and row.get("change") and row.get("code_change") is False for row in mapping_rows), "migration_fields")
    check(migration.get("rules", {}).get("no_file_move") is True, "migration_no_move")
    check(migration.get("rules", {}).get("no_code_refactor") is True, "migration_no_refactor")
    check(migration.get("rules", {}).get("no_module_deletion") is True, "migration_no_delete")

    conflict_rows = conflicts.get("conflicts", [])
    check(len(conflict_rows) >= 5, "conflict_rows")
    check(all(row.get("topic") and row.get("resolution") and row.get("status") for row in conflict_rows), "conflict_fields")
    check(conflicts.get("rules", {}).get("all_core_conflicts_resolved") is True, "conflict_resolved")
    check(conflicts.get("rules", {}).get("integration_is_router_not_authority") is True, "conflict_integration_boundary")

    extension_rows = future.get("extensions", [])
    check({"Emotion Engine", "Social Runtime", "Personality Growth", "B Route"}.issubset({row.get("extension") for row in extension_rows}), "future_extensions")
    check(all(row.get("mount") and row.get("status") and row.get("allowed") and row.get("forbidden") for row in extension_rows), "future_fields")
    check(len(future.get("entry_gates", [])) >= 5, "future_gates")
    check(future.get("rules", {}).get("self_social_boundary_required") is True, "future_self_social_gate")
    check(future.get("rules", {}).get("future_not_active") is True, "future_not_active")

    verifier_text = Path(__file__).read_text(encoding="utf-8")
    verifier_ast = ast.parse(verifier_text, filename=str(Path(__file__)))
    imports: set[str] = set()
    for node in ast.walk(verifier_ast):
        if isinstance(node, ast.Import):
            imports.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split(".")[0])
    check(not imports.intersection({"subprocess", "socket", "requests", "cv2", "torch"}), "planning_no_runtime_import")
    check(not imports.intersection({"emotion_runtime", "role_runtime", "social_runtime", "memory_migration", "action_runtime"}), "planning_no_extension_import")
    compile(verifier_text, str(Path(__file__)), "exec")
    check(True, "planning_verifier_compile")

    passed = checks - len(failures)
    print(f"CHECKS: {checks}")
    print(f"FAILED_CHECKS: {failures}")
    print(f"PASSED_CHECK_COUNT: {passed}")
    print(f"FAILED_CHECK_COUNT: {len(failures)}")
    print(f"BLOCKER_COUNT: {len(failures)}")
    if failures:
        print("FINAL_DECISION: BLOCKED_BY_VERIFIER_FAILURE")
        print("READINESS: LUNA_SELF_SOCIAL_SELF_ARCHITECTURE_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_SELF_SOCIAL_SELF_ARCHITECTURE_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    sys.exit(main())
