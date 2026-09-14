"""V0 static verifier for Luna System Constitution and Governance Architecture.

Planning Only: checks governance contracts without executing Runtime or any
external model, provider, hardware, action, Emotion, Social, or self-modifying
behavior.
"""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
JSON_ASSETS = (
    "constitution_principles_v1.json", "authority_hierarchy_v1.json",
    "permission_governance_matrix_v1.json", "conflict_resolution_policy_v1.json",
    "change_control_contract_v1.json", "module_ownership_governance_v1.json",
    "system_invariant_schema_v1.json", "safety_boundary_contract_v1.json",
    "future_extension_boundary_v1.json", "constitution_core_mapping_v1.json",
)
MD_ASSETS = ("luna_system_constitution_v1.md", "governance_whitebox_v1.md", "governance_go_no_go_v1.md")


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

    principles = data.get("constitution_principles_v1.json", {})
    hierarchy = data.get("authority_hierarchy_v1.json", {})
    permissions = data.get("permission_governance_matrix_v1.json", {})
    conflict = data.get("conflict_resolution_policy_v1.json", {})
    change = data.get("change_control_contract_v1.json", {})
    ownership = data.get("module_ownership_governance_v1.json", {})
    invariants = data.get("system_invariant_schema_v1.json", {})
    safety = data.get("safety_boundary_contract_v1.json", {})
    future = data.get("future_extension_boundary_v1.json", {})
    mapping = data.get("constitution_core_mapping_v1.json", {})

    principle_rows = principles.get("principles", [])
    names = [row.get("name") for row in principle_rows]
    expected_principles = {"System Stability Principle", "Evidence First Principle", "Boundary Respect Principle", "Unknown Preservation Principle", "State Ownership Principle", "Human Interaction Safety Principle"}
    check(expected_principles.issubset(set(names)), "constitution_principles_complete")
    check(len(names) == len(set(names)) and all(names), "constitution_principles_unique")
    check(all(row.get("priority") and row.get("description") and row.get("non_negotiable") is True for row in principle_rows), "constitution_principles_fields")
    check(principles.get("rules", {}).get("immutable_by_core") is True, "constitution_immutable")
    check(principles.get("rules", {}).get("ordinary_module_cannot_modify") is True, "constitution_no_core_edit")
    check(principles.get("rules", {}).get("unknown_cannot_be_suppressed") is True, "constitution_unknown_guard")

    layers = hierarchy.get("layers", [])
    layer_names = [row.get("layer") for row in layers]
    check(layer_names == ["L0 Constitution", "L1 Cognitive OS Governance", "L2 Cognitive Core", "L3 Capability Governance", "L4 Execution"], "authority_layers")
    check(len(layer_names) == len(set(layer_names)), "authority_layers_unique")
    check(all(row.get("owner") and row.get("scope") and row.get("cannot_be_overridden_by") is not None for row in layers), "authority_layers_complete")
    check(hierarchy.get("precedence") == layer_names, "authority_precedence")
    check(hierarchy.get("rules", {}).get("l0_immutable") is True, "authority_l0_immutable")
    check(hierarchy.get("rules", {}).get("no_reverse_authority") is True, "authority_no_reverse")
    check(hierarchy.get("rules", {}).get("execution_not_decision") is True, "authority_execution_boundary")

    permission_rows = permissions.get("rows", [])
    permission_names = [row.get("module") for row in permission_rows]
    check(len(permission_rows) >= 7, "permission_rows")
    check(len(permission_names) == len(set(permission_names)) and all(permission_names), "permission_modules_unique")
    check(all(row.get("layer") and row.get("allowed") is not None and row.get("forbidden") is not None for row in permission_rows), "permission_fields")
    brain = next((row for row in permission_rows if row.get("module") == "Brain"), {})
    self_reg = next((row for row in permission_rows if row.get("module") == "Self Regulation"), {})
    capability = next((row for row in permission_rows if row.get("module") == "Capability Governance"), {})
    runtime = next((row for row in permission_rows if row.get("module") == "Runtime"), {})
    check("Generate Decision Candidate" in brain.get("allowed", []) and "Modify Constitution" in brain.get("forbidden", []), "permission_brain")
    check("Assess Health" in self_reg.get("allowed", []) and "Modify Identity" in self_reg.get("forbidden", []), "permission_self_regulation")
    check("Manage Lifecycle" in capability.get("allowed", []) and "Generate Goal" in capability.get("forbidden", []), "permission_capability")
    check("Execute Admitted Request" in runtime.get("allowed", []) and "Make Decision" in runtime.get("forbidden", []), "permission_runtime")
    check(permissions.get("rules", {}).get("least_authority") is True, "permission_least_authority")
    check(permissions.get("rules", {}).get("execute_requires_admission") is True, "permission_admission_gate")

    check(conflict.get("precedence") == ["System Stability", "Core Cognitive Function", "Human Safety and Privacy", "Evidence Integrity", "User Goal", "Capability Improvement", "Performance Optimization"], "conflict_precedence")
    check(len(conflict.get("resolution_flow", [])) >= 6, "conflict_resolution_flow")
    check(len(conflict.get("cases", [])) >= 4, "conflict_cases")
    check(conflict.get("rules", {}).get("constitution_first") is True, "conflict_constitution_first")
    check(conflict.get("rules", {}).get("stability_over_optimization") is True, "conflict_stability_first")
    check(conflict.get("rules", {}).get("unknown_preserved") is True, "conflict_unknown")
    check(conflict.get("rules", {}).get("resolution_candidate_not_direct_action") is True, "conflict_candidate_only")

    check(change.get("lifecycle") == ["Proposal", "Evaluation", "Validation", "Admission", "Activation", "Monitoring"], "change_lifecycle")
    check(set(["New Module", "New Capability", "New Model", "New Provider", "Core Rule Adjustment"]).issubset(set(change.get("change_types", []))), "change_types")
    check(len(change.get("required_reviews", [])) >= 5, "change_reviews")
    check(set(["Constitution", "Identity", "Value", "Brain Rules"]).issubset(set(change.get("protected_changes", []))), "change_protected_surfaces")
    check(change.get("activation", {}).get("requires_admission") is True, "change_admission")
    check(change.get("activation", {}).get("automatic_activation") is False, "change_no_auto_activation")
    check(change.get("rules", {}).get("constitution_runtime_editing_forbidden") is True, "change_constitution_runtime_guard")

    owners = ownership.get("owners", [])
    concepts = [row.get("concept") for row in owners]
    check(len(owners) >= 8, "ownership_count")
    check(len(concepts) == len(set(concepts)) and all(concepts), "ownership_unique")
    check(all(row.get("owner") and row.get("writer") and row.get("readers") is not None for row in owners), "ownership_fields")
    check(ownership.get("rules", {}).get("unique_owner_required") is True, "ownership_unique_rule")
    check(ownership.get("rules", {}).get("reader_does_not_imply_write") is True, "ownership_reader_rule")

    invariant_rows = invariants.get("invariants", [])
    invariant_ids = [row.get("invariant_id") for row in invariant_rows]
    check(len(invariant_rows) >= 7, "invariant_count")
    check(len(invariant_ids) == len(set(invariant_ids)) and all(invariant_ids), "invariant_unique")
    check(all(row.get("description") and row.get("protected_by") for row in invariant_rows), "invariant_fields")
    check({"unique_state_owner", "decision_owner", "evidence_boundary", "action_boundary", "memory_boundary", "self_boundary"}.issubset(set(invariant_ids)), "invariant_core_coverage")
    check(invariants.get("rules", {}).get("invariant_violation_is_blocker") is True, "invariant_blocker")

    check(set(["User Safety", "Privacy", "Materially Consequential Action", "Sensitive Evidence"]).issubset(set(safety.get("protected_domains", []))), "safety_domains")
    check(len(safety.get("required_safeguards", [])) >= 5, "safety_safeguards")
    check(len(safety.get("escalation", [])) >= 4, "safety_escalation")
    check(safety.get("rules", {}).get("high_impact_requires_review") is True, "safety_review")
    check(safety.get("rules", {}).get("safety_over_task_completion") is True, "safety_priority")
    check(safety.get("rules", {}).get("action_authorization_required") is True, "safety_action_gate")

    extension_rows = future.get("extensions", [])
    extension_names = {row.get("extension") for row in extension_rows}
    check({"Emotion", "Social Identity", "World Model", "Embodiment"}.issubset(extension_names), "future_extensions")
    check(all(row.get("status") and row.get("allowed") and row.get("forbidden") for row in extension_rows), "future_extension_fields")
    check(len(future.get("entry_gates", [])) >= 5, "future_entry_gates")
    check(future.get("rules", {}).get("constitution_first") is True, "future_constitution_first")
    check(future.get("rules", {}).get("future_not_active") is True, "future_not_active")

    mappings = mapping.get("mappings", [])
    check(len(mappings) >= 6, "mapping_count")
    check(all(row.get("principle") and row.get("modules") and row.get("protected_invariant") for row in mappings), "mapping_fields")
    check(mapping.get("rules", {}).get("every_principle_mapped") is True, "mapping_principles")
    check(mapping.get("rules", {}).get("every_mapping_has_invariant") is True, "mapping_invariants")
    check(mapping.get("rules", {}).get("mapping_is_read_only") is True, "mapping_read_only")

    verifier_text = Path(__file__).read_text(encoding="utf-8")
    verifier_ast = ast.parse(verifier_text, filename=str(Path(__file__)))
    imports: set[str] = set()
    for node in ast.walk(verifier_ast):
        if isinstance(node, ast.Import):
            imports.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split(".")[0])
    check(not imports.intersection({"subprocess", "socket", "requests", "cv2", "torch"}), "planning_no_runtime_import")
    check(not imports.intersection({"runtime_edit", "emotion_runtime", "social_runtime", "auto_learning", "hardware_runtime"}), "planning_no_extension_import")
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
        print("READINESS: LUNA_SYSTEM_CONSTITUTION_GOVERNANCE_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_SYSTEM_CONSTITUTION_GOVERNANCE_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    sys.exit(main())
