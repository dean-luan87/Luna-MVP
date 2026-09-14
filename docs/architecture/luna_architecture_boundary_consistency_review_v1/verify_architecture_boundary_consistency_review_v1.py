"""V0 static verifier for Luna Architecture Boundary Consistency Review.

Planning Only: validates boundary contracts without full repository scanning,
Runtime activation, or code/file migration.
"""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
JSON_ASSETS = (
    "canonical_owner_consistency_review_v1.json", "permission_boundary_consistency_review_v1.json",
    "cognitive_flow_compatibility_review_v1.json", "constitution_scope_review_v1.json",
    "capability_governance_scope_review_v1.json", "emotion_boundary_consistency_review_v1.json",
    "boundary_consistency_conflict_registry_v1.json",
)
MD_ASSETS = ("luna_architecture_boundary_consistency_review_v1.md", "boundary_consistency_whitebox_v1.md", "boundary_consistency_go_no_go_v1.md")


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

    owners = data.get("canonical_owner_consistency_review_v1.json", {})
    permissions = data.get("permission_boundary_consistency_review_v1.json", {})
    flow = data.get("cognitive_flow_compatibility_review_v1.json", {})
    constitution = data.get("constitution_scope_review_v1.json", {})
    capability = data.get("capability_governance_scope_review_v1.json", {})
    emotion = data.get("emotion_boundary_consistency_review_v1.json", {})
    conflicts = data.get("boundary_consistency_conflict_registry_v1.json", {})

    owner_rows = owners.get("owners", [])
    owner_objects = [row.get("object") for row in owner_rows]
    check(len(owner_rows) >= 10, "owner_rows")
    check(len(owner_objects) == len(set(owner_objects)) and all(owner_objects), "owner_objects_unique")
    check(all(row.get("canonical_owner") and row.get("status") for row in owner_rows), "owner_fields")
    check(owners.get("duplicate_owner_candidates") == [], "duplicate_owner_candidates_empty")
    check(owners.get("rules", {}).get("canonical_owner_unique") is True, "owner_unique_rule")
    check(owners.get("rules", {}).get("constitution_not_self_owned") is True, "constitution_not_self_owner")
    check(owners.get("rules", {}).get("capability_governance_independent") is True, "capability_owner_independent")
    check(any(row.get("object") == "Role" and row.get("canonical_owner") == "Social Self Layer" for row in owner_rows), "role_social_owner")
    check(any(row.get("object") == "Relationship" and row.get("canonical_owner") == "Social Self Layer" for row in owner_rows), "relationship_social_owner")
    check(any(row.get("object") == "Emotion Context" and row.get("canonical_owner") == "Integration Layer" for row in owner_rows), "emotion_integration_owner")

    permission_rows = permissions.get("rows", [])
    check(len(permission_rows) >= 5, "permission_rows")
    check(all(row.get("module") and row.get("allowed") is not None and row.get("forbidden") is not None for row in permission_rows), "permission_fields")
    self_row = next((r for r in permission_rows if r.get("module") == "Self Layer"), {})
    social_row = next((r for r in permission_rows if r.get("module") == "Social Self Layer"), {})
    integration_row = next((r for r in permission_rows if r.get("module") == "Integration Layer"), {})
    check("Define Social Role" in self_row.get("forbidden", []) and "Decide Relationship" in self_row.get("forbidden", []), "self_social_permission")
    check("Modify Self Identity" in social_row.get("forbidden", []) and "Modify Constitution" in social_row.get("forbidden", []), "social_self_permission")
    check("Direct Self Mutation" in integration_row.get("forbidden", []) and "Direct Action" in integration_row.get("forbidden", []), "integration_permission")
    check(permissions.get("rules", {}).get("self_social_non_overwrite") is True, "permission_non_overwrite")
    check(permissions.get("rules", {}).get("capability_independent") is True, "permission_capability_independent")

    check(flow.get("legacy_flow") == ["Observation", "Field", "Brain", "Decision"], "legacy_flow")
    check(flow.get("refactored_external_flow") == ["External World", "Social Self", "Integration", "Brain", "Self Evaluation", "Decision"], "refactored_flow")
    check(len(flow.get("canonical_flow", [])) >= 10, "canonical_flow")
    check(len(flow.get("compatibility", [])) >= 4, "flow_compatibility_rows")
    check(all(row.get("legacy_stage") and row.get("new_stage") and row.get("preserved") is True for row in flow.get("compatibility", [])), "flow_compatibility_fields")
    check(flow.get("rules", {}).get("legacy_flow_is_subflow") is True, "legacy_subflow")
    check(flow.get("rules", {}).get("new_layers_do_not_replace_evidence") is True, "flow_evidence_preserved")
    check(flow.get("rules", {}).get("decision_owner_unchanged") is True, "flow_decision_owner")

    check(constitution.get("owner") == "L0 System Constitution", "constitution_scope_owner")
    check(set(["Self Layer", "Social Self Layer", "Integration Layer"]).issubset(set(constitution.get("applies_to", []))), "constitution_applies_to")
    check(constitution.get("is_owned_by_self") is False and constitution.get("is_owned_by_social_self") is False, "constitution_not_member")
    check(constitution.get("rules", {}).get("l0_top_level") is True, "constitution_l0")
    check(constitution.get("rules", {}).get("self_constrained") is True and constitution.get("rules", {}).get("social_self_constrained") is True, "constitution_constrains_both")

    check(capability.get("owner") == "Capability Governance", "capability_scope_owner")
    check(set(["Capability Definition", "Capability Registry", "Capability Lifecycle", "Admission", "Calibration", "Health"]).issubset(set(capability.get("manages", []))), "capability_scope_manages")
    check(set(["Capability Profile", "Limitations", "Self Capability State"]).issubset(set(capability.get("self_knows", []))), "self_capability_knowledge")
    check(capability.get("rules", {}).get("governance_independent") is True, "capability_governance_independent")
    check(capability.get("rules", {}).get("self_is_interface_not_owner") is True, "self_capability_interface")
    check(capability.get("rules", {}).get("capability_not_swallowed_by_self") is True, "capability_not_swallowed")

    check(emotion.get("owner") == "Integration Layer", "emotion_scope_owner")
    check(set(["Self Layer", "Social Self Layer"]).issubset(set(emotion.get("not_owned_by", []))), "emotion_not_self_social")
    check(emotion.get("flow") == ["Social Self Event", "Self Context", "Integration", "Emotion Context Candidate", "Attention/Preference Context"], "emotion_flow")
    check(set(["Enter Self Identity", "Enter Social Self Ownership", "Direct Decision", "Direct Action"]).issubset(set(emotion.get("cannot", []))), "emotion_forbidden")
    check(emotion.get("rules", {}).get("context_only") is True and emotion.get("rules", {}).get("no_emotion_runtime") is True, "emotion_boundary")

    conflict_rows = conflicts.get("conflicts", [])
    check(len(conflict_rows) >= 5, "conflict_rows")
    check(all(row.get("id") and row.get("topic") and row.get("resolution") and row.get("status") for row in conflict_rows), "conflict_fields")
    check(conflicts.get("rules", {}).get("all_conflicts_classified") is True, "conflict_classified")
    check(conflicts.get("rules", {}).get("no_unresolved_owner_conflict") is True, "conflict_owner_resolved")
    check(conflicts.get("rules", {}).get("legacy_references_non_authoritative") is True, "conflict_legacy_non_authoritative")
    check(conflicts.get("rules", {}).get("no_code_change") is True, "conflict_no_code")

    verifier_text = Path(__file__).read_text(encoding="utf-8")
    verifier_ast = ast.parse(verifier_text, filename=str(Path(__file__)))
    imports: set[str] = set()
    for node in ast.walk(verifier_ast):
        if isinstance(node, ast.Import):
            imports.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split(".")[0])
    check(not imports.intersection({"subprocess", "socket", "requests", "cv2", "torch"}), "planning_no_runtime_import")
    check(not imports.intersection({"full_audit", "runtime_activation", "emotion_runtime", "social_runtime"}), "planning_no_full_audit_import")
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
        print("READINESS: LUNA_ARCHITECTURE_BOUNDARY_CONSISTENCY_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_ARCHITECTURE_BOUNDARY_CONSISTENCY_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    sys.exit(main())
