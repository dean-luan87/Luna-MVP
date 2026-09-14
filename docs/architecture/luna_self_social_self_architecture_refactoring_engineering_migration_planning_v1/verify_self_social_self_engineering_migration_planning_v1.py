"""V0 static verifier for Self/Social Self Refactoring and Migration Planning.

Planning Only: validates inventories and migration contracts without moving,
deleting, refactoring, or executing any Runtime or social/emotion behavior.
"""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
JSON_ASSETS = (
    "architecture_refactoring_delta_v1.json", "existing_module_impact_inventory_v1.json",
    "ownership_migration_map_v1.json", "code_impact_registry_v1.json",
    "runtime_impact_review_v1.json", "module_ownership_registry_update_process_v1.json",
    "architecture_change_governance_v1.json", "future_development_workflow_v1.json",
    "engineering_migration_risk_registry_v1.json", "self_social_asset_mapping_v1.json",
    "migration_non_goals_v1.json",
)
MD_ASSETS = (
    "luna_self_social_self_architecture_refactoring_and_engineering_migration_planning_v1.md",
    "self_social_engineering_migration_whitebox_v1.md",
    "self_social_engineering_migration_go_no_go_v1.md",
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

    delta = data.get("architecture_refactoring_delta_v1.json", {})
    inventory = data.get("existing_module_impact_inventory_v1.json", {})
    ownership = data.get("ownership_migration_map_v1.json", {})
    code = data.get("code_impact_registry_v1.json", {})
    runtime = data.get("runtime_impact_review_v1.json", {})
    owner_process = data.get("module_ownership_registry_update_process_v1.json", {})
    change = data.get("architecture_change_governance_v1.json", {})
    workflow = data.get("future_development_workflow_v1.json", {})
    risks = data.get("engineering_migration_risk_registry_v1.json", {})
    assets = data.get("self_social_asset_mapping_v1.json", {})
    non_goals = data.get("migration_non_goals_v1.json", {})

    check(delta.get("new_layers") == ["Self Layer", "Social Self Layer", "Integration Layer"], "delta_layers")
    check(delta.get("previous_decision") == "LUNA_SELF_SOCIAL_SELF_ARCHITECTURE_READY", "delta_previous_decision")
    check(len(delta.get("delta", [])) >= 4, "delta_entries")
    check(delta.get("rules", {}).get("mapping_before_move") is True, "delta_mapping_first")
    check(delta.get("rules", {}).get("owner_before_implementation") is True, "delta_owner_first")
    check(delta.get("rules", {}).get("no_code_change") is True, "delta_no_code")

    inventory_rows = inventory.get("observed_assets", [])
    check(inventory.get("scan_scope") == ["capabilities/", "docs/architecture/", "tools/"], "inventory_scope")
    check(len(inventory_rows) >= 8, "inventory_rows")
    check(all(row.get("asset_id") and row.get("path") and row.get("current_owner") and row.get("target_owner") and row.get("status") and row.get("impact") for row in inventory_rows), "inventory_fields")
    check(inventory.get("rules", {}).get("inventory_is_read_only") is True, "inventory_read_only")
    check(inventory.get("rules", {}).get("no_automatic_migration") is True, "inventory_no_auto_migration")

    ownership_rows = ownership.get("mappings", [])
    objects = {row.get("object") for row in ownership_rows}
    check({"Self Model", "Role", "Relationship", "Emotion Context", "Constitution"}.issubset(objects), "ownership_objects")
    check(len(ownership_rows) >= 9, "ownership_rows")
    check(all(row.get("old_owner") and row.get("new_owner") and row.get("migration_action") and row.get("stage") and row.get("code_change") is False for row in ownership_rows), "ownership_mapping_fields")
    check(ownership.get("mapping_principle") == "No Move First; Mapping First; Owner First; Migration Later", "ownership_principle")
    check(ownership.get("rules", {}).get("no_file_move") is True, "ownership_no_move")
    check(ownership.get("rules", {}).get("implementation_after_plan") is True, "ownership_implementation_after_plan")

    code_rows = code.get("entries", [])
    check(len(code_rows) >= 8, "code_impact_rows")
    check(all(row.get("path") and row.get("object") and row.get("impact") and row.get("priority") and row.get("action") and row.get("code_change") is False for row in code_rows), "code_impact_fields")
    check(code.get("rules", {}).get("registry_is_plan_only") is True, "code_registry_plan_only")
    check(code.get("rules", {}).get("no_direct_edit") is True, "code_registry_no_edit")

    check(runtime.get("status") == "planning_only_no_runtime_change", "runtime_review_status")
    check(set(["Self State", "Social State", "Integration Context"]).issubset(set(runtime.get("state_contracts", []))), "runtime_state_contracts")
    check(set(["Self Observation Event", "Social Context Event", "Role Transition Event"]).issubset(set(runtime.get("events", []))), "runtime_events")
    check(set(["Runtime Owns Self Identity", "Runtime Owns Role", "Runtime Constitution Edit"]).issubset(set(runtime.get("runtime_forbidden", []))), "runtime_forbidden")
    check(runtime.get("rules", {}).get("runtime_not_modified") is True, "runtime_not_modified")
    check(runtime.get("rules", {}).get("state_owner_preserved") is True, "runtime_state_owner")

    check(owner_process.get("ownership_classes") == ["Self", "Social Self", "Cognitive Core", "Capability", "Action", "Governance"], "owner_process_classes")
    check(owner_process.get("process") == ["Proposal", "Subject Ownership Classification", "Cognitive Object Definition", "Permission Definition", "Interface Definition", "Ownership Review", "Registry Update", "Implementation Planning", "Validation"], "owner_process_flow")
    check(len(owner_process.get("required_questions", [])) >= 6, "owner_process_questions")
    check(owner_process.get("rules", {}).get("owner_before_code") is True, "owner_process_owner_first")
    check(owner_process.get("rules", {}).get("registry_update_required") is True, "owner_process_registry")

    check(change.get("lifecycle") == ["Proposal", "Impact Analysis", "Ownership Review", "Migration Plan", "Implementation", "Validation"], "change_governance_flow")
    check(len(change.get("change_inputs", [])) >= 5, "change_governance_inputs")
    check(len(change.get("required_outputs", [])) >= 5, "change_governance_outputs")
    check(change.get("approval", {}).get("constitution_check") is True, "change_constitution_check")
    check(change.get("approval", {}).get("implementation_admission") is True, "change_implementation_admission")
    check(change.get("rules", {}).get("proposal_before_code") is True, "change_proposal_first")
    check(change.get("rules", {}).get("migration_plan_required") is True, "change_migration_required")

    workflow_steps = workflow.get("steps", [])
    check([row.get("name") for row in workflow_steps] == ["Subject Ownership Classification", "Cognitive Object Definition", "Permission Definition", "Interface Definition", "Engineering Implementation"], "workflow_steps")
    check(all(row.get("step") and row.get("question") and row.get("output") for row in workflow_steps), "workflow_fields")
    check(workflow.get("example", {}).get("owner") == "Social Self", "workflow_example_owner")
    check(workflow.get("rules", {}).get("implementation_is_last") is True, "workflow_implementation_last")
    check(workflow.get("rules", {}).get("governance_admission_required") is True, "workflow_admission")

    risk_rows = risks.get("risks", [])
    check(len(risk_rows) >= 7, "risk_rows")
    check(all(row.get("risk_id") and row.get("risk") and row.get("impact") and row.get("mitigation") and row.get("priority") for row in risk_rows), "risk_fields")
    check(any(row.get("priority") == "P0" for row in risk_rows), "risk_p0")
    check(risks.get("rules", {}).get("p0_requires_resolution_before_implementation") is True, "risk_p0_gate")
    check(risks.get("rules", {}).get("no_silent_migration") is True, "risk_no_silent")

    check(assets.get("mapping_only") is True, "asset_mapping_only")
    asset_classes = {row.get("class") for row in assets.get("asset_classes", [])}
    check({"Self Layer", "Social Self Layer", "Integration Layer", "Governance"}.issubset(asset_classes), "asset_classes")
    check(assets.get("rules", {}).get("no_move") is True, "asset_no_move")
    check(assets.get("rules", {}).get("reference_existing_assets") is True, "asset_reference_existing")

    forbidden = set(non_goals.get("forbidden_actions", []))
    check({"Runtime Implementation", "Emotion Runtime", "Role Runtime", "Social Runtime", "Memory Migration", "Code Refactor", "Module Deletion", "File Move"}.issubset(forbidden), "non_goals_complete")
    check(set(["Read-only Scan", "Impact Inventory", "Ownership Mapping", "Code Impact Registration"]).issubset(set(non_goals.get("allowed_actions", []))), "non_goals_allowed")
    check(non_goals.get("rules", {}).get("plan_only") is True, "non_goals_plan_only")
    check(non_goals.get("rules", {}).get("no_code_refactor") is True, "non_goals_no_refactor")

    verifier_text = Path(__file__).read_text(encoding="utf-8")
    verifier_ast = ast.parse(verifier_text, filename=str(Path(__file__)))
    imports: set[str] = set()
    for node in ast.walk(verifier_ast):
        if isinstance(node, ast.Import):
            imports.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split(".")[0])
    check(not imports.intersection({"subprocess", "socket", "requests", "cv2", "torch"}), "planning_no_runtime_import")
    check(not imports.intersection({"runtime_migration", "emotion_runtime", "role_runtime", "social_runtime", "memory_migration"}), "planning_no_migration_import")
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
        print("READINESS: LUNA_SELF_SOCIAL_SELF_ENGINEERING_MIGRATION_PLAN_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_SELF_SOCIAL_SELF_ENGINEERING_MIGRATION_PLAN_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    sys.exit(main())
