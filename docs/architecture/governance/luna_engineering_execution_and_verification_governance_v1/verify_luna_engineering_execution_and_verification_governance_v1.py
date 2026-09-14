from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

BASE_DIR = Path(__file__).resolve().parent

REQUIRED_FILES = [
    "luna_engineering_phase_execution_role_standard_v1.md",
    "luna_phase_verification_execution_authority_standard_v1.md",
    "luna_execution_mode_verification_authority_matrix_v1.json",
    "luna_phase_instruction_required_fields_standard_v1.json",
    "luna_phase_instruction_template_v1.md",
    "luna_runner_and_verifier_naming_standard_v1.md",
    "luna_verification_status_registry_v1.json",
    "luna_verification_failure_classification_and_remediation_standard_v1.json",
    "luna_agent_product_development_compliance_contract_v1.json",
    "luna_engineering_execution_and_verification_governance_summary_v1.json",
    "verify_luna_engineering_execution_and_verification_governance_v1.py",
]

JSON_FILES = [f for f in REQUIRED_FILES if f.endswith(".json")]

EXPECTED_DECISION = (
    "LUNA_ENGINEERING_EXECUTION_AND_VERIFICATION_GOVERNANCE_STANDARDIZATION_GO"
)
EXPECTED_NEXT = "RETURN_TO_CURRENT_LUNA_PRODUCT_PHASE"

EXPECTED_MODES = {
    "Planning Only",
    "Controlled Skeleton Implementation",
    "Controlled DryRun",
    "Smoke Test",
    "Runtime Execution",
    "Audit",
    "Post Review",
    "Remediation",
    "Migration",
    "Production Activation",
}

EXPECTED_STATUSES = {
    "NOT_STARTED",
    "IN_AGENT_EXECUTION",
    "STATIC_CHECK_READY",
    "COMPONENT_VALIDATION_PASSED",
    "WAITING_FOR_USER_TERMINAL_VERIFICATION",
    "BLOCKED_BEFORE_USER_TERMINAL_VERIFICATION",
    "BLOCKED_BY_VERIFIER_FAILURE",
    "BLOCKED_BY_OUTPUT_CONTRACT_DEVIATION",
    "BLOCKED_BY_BOUNDARY_VIOLATION",
    "GO",
}

EXPECTED_FAILURE_CLASSES = {
    "MISSING_ARTIFACT",
    "OUTPUT_CONTRACT_DRIFT",
    "STATIC_IMPORT_OR_SYNTAX_FAILURE",
    "FIXTURE_CONTRACT_FAILURE",
    "RUNTIME_BOUNDARY_VIOLATION",
    "VERIFIER_DEFECT",
    "REAL_IMPLEMENTATION_DEFECT",
    "ARCHITECTURE_BLOCKER",
}


def _load_json(name: str) -> Dict[str, Any]:
    with open(BASE_DIR / name, "r", encoding="utf-8") as f:
        return json.load(f)


def _load_md(name: str) -> str:
    return (BASE_DIR / name).read_text(encoding="utf-8")


def main() -> int:
    checks: List[Dict[str, Any]] = []

    def add(name: str, passed: bool, detail: str = "") -> None:
        checks.append({"name": name, "passed": bool(passed), "detail": detail})

    missing = [f for f in REQUIRED_FILES if not (BASE_DIR / f).exists()]
    add(
        "required_files_exist",
        len(missing) == 0,
        ",".join(missing) if missing else "ok",
    )

    invalid_json = []
    for jf in JSON_FILES:
        try:
            _load_json(jf)
        except Exception as exc:
            invalid_json.append(f"{jf}:{exc}")
    add(
        "all_json_valid",
        len(invalid_json) == 0,
        ";".join(invalid_json) if invalid_json else "ok",
    )

    if missing or invalid_json:
        failed = [c for c in checks if not c["passed"]]
        print("CHECKS")
        for c in checks:
            print(f"- [{'PASS' if c['passed'] else 'FAIL'}] {c['name']}")
        print("FAILED_CHECKS")
        if failed:
            for c in failed:
                print(
                    f"- {c['name']}: {c['detail'] if c['detail'] else 'condition_not_met'}"
                )
        else:
            print("- NONE")
        print("PASSED_CHECK_COUNT")
        print(sum(1 for c in checks if c["passed"]))
        print("FAILED_CHECK_COUNT")
        print(len(failed))
        print("BLOCKER_COUNT")
        print(len(failed))
        print("FINAL_DECISION")
        print(
            "LUNA_ENGINEERING_EXECUTION_AND_VERIFICATION_GOVERNANCE_STANDARDIZATION_BLOCKED"
        )
        print("NEXT")
        print(
            "Phase-Luna-Engineering-Execution-And-Verification-Governance-Standardization-Output-Contract-Correction-v1-001"
        )
        return 1

    role_std = _load_md("luna_engineering_phase_execution_role_standard_v1.md")
    auth_std = _load_md("luna_phase_verification_execution_authority_standard_v1.md")
    template_md = _load_md("luna_phase_instruction_template_v1.md")
    naming_md = _load_md("luna_runner_and_verifier_naming_standard_v1.md")

    mode_matrix = _load_json(
        "luna_execution_mode_verification_authority_matrix_v1.json"
    )
    field_std = _load_json("luna_phase_instruction_required_fields_standard_v1.json")
    status_reg = _load_json("luna_verification_status_registry_v1.json")
    remediation = _load_json(
        "luna_verification_failure_classification_and_remediation_standard_v1.json"
    )
    compliance = _load_json(
        "luna_agent_product_development_compliance_contract_v1.json"
    )
    summary = _load_json(
        "luna_engineering_execution_and_verification_governance_summary_v1.json"
    )

    add(
        "role_standard_has_three_roles",
        "Role A: Agent" in role_std
        and "Role B: User Terminal" in role_std
        and "Role C: ChatGPT" in role_std,
    )
    add("role_standard_has_stop_point", "Agent Stop Point" in role_std)
    add(
        "role_standard_has_unverified_no_go_rule",
        "Without complete V2 output and V3 audit" in role_std,
    )

    add(
        "authority_standard_has_v0_v1_v2_v3",
        all(x in auth_std for x in ["## V0", "## V1", "## V2", "## V3"]),
    )
    add("authority_standard_v2_user_only", "User Terminal Only" in auth_std)
    add("authority_standard_v3_chatgpt_only", "ChatGPT Only" in auth_std)
    add(
        "authority_standard_only_v2_v3_can_grant_go",
        "Only user-executed V2 plus ChatGPT V3 audit can grant GO." in auth_std,
    )

    modes = mode_matrix.get("modes", [])
    mode_ids = {m.get("mode_id") for m in modes if isinstance(m, dict)}
    add(
        "execution_mode_matrix_complete_true",
        mode_matrix.get("matrix_complete") is True,
    )
    add("execution_mode_matrix_contains_required_modes", mode_ids == EXPECTED_MODES)
    add(
        "planning_only_v0_only",
        any(
            m.get("mode_id") == "Planning Only"
            and m.get("agent_v0_allowed") is True
            and m.get("agent_v1_allowed") is False
            and m.get("final_phase_verifier_user_only") is True
            for m in modes
        ),
    )
    add(
        "controlled_dryrun_permissions_correct",
        any(
            m.get("mode_id") == "Controlled DryRun"
            and m.get("agent_v0_allowed") is True
            and m.get("agent_v1_allowed") is True
            and m.get("runtime_permission") is False
            and m.get("final_phase_verifier_user_only") is True
            for m in modes
        ),
    )
    add(
        "runtime_migration_production_default_restricted",
        all(
            any(
                m.get("mode_id") == target and m.get("runtime_permission") is False
                for m in modes
            )
            for target in ["Runtime Execution", "Migration", "Production Activation"]
        ),
    )

    req_fields = field_std.get("required_fields", {})
    needed = {
        "Phase",
        "Stage",
        "Execution Mode",
        "Current Work Description",
        "Previous Phase",
        "Previous Phase Decision",
        "Input Assets",
        "Required Pre-Read",
        "Target Directory",
        "Scope",
        "Out Of Scope",
        "Required Final Files",
        "Implementation Principles",
        "Required Checks",
        "Negative Guards",
        "Verification Authority",
        "Allowed Agent Checks",
        "Allowed Agent Execution",
        "Prohibited Agent Execution",
        "Agent Stop Point",
        "User Terminal Commands",
        "Expected Success Decision",
        "Expected Next",
        "Expected Failure Decision",
        "Expected Failure Next",
        "Stop Condition",
        "Blocker Conditions",
        "Completion Report Format",
        "Current Status Contract",
    }
    add("required_fields_complete_set", set(req_fields.keys()) == needed)
    add(
        "required_fields_have_required_description_validation",
        all(
            isinstance(v, dict)
            and {"required", "description", "validation_rule"}.issubset(set(v.keys()))
            for v in req_fields.values()
        ),
    )
    add(
        "required_fields_complete_true",
        field_std.get("required_fields_complete") is True,
    )

    add(
        "template_has_required_structure",
        all(
            x in template_md
            for x in [
                "## 当前阶段判断",
                "## 当前工作内容描述",
                "## 适可而止条件",
                "## 🟢 Agent 执行",
                "## 🟡 用户终端执行",
                "## 🔵 ChatGPT 审核与最终裁决",
            ]
        ),
    )
    add(
        "template_has_verification_authority_section",
        "Verification Authority:" in template_md,
    )
    add(
        "template_has_validation_result_authority_rules",
        "V0 does not grant GO." in template_md
        and "Only user-executed V2 plus ChatGPT V3 audit can grant GO." in template_md,
    )
    add(
        "template_has_four_examples",
        all(
            x in template_md
            for x in [
                "Example A: Planning Only",
                "Example B: Controlled Skeleton",
                "Example C: Controlled DryRun",
                "Example D: Remediation",
            ]
        ),
    )

    add(
        "naming_standard_has_runner_result_final_split",
        all(
            x in naming_md
            for x in [
                "## A. Phase Runner",
                "## B. Result Verifier",
                "## C. Final Phase Verifier",
            ]
        ),
    )
    add(
        "naming_standard_forbids_result_verifier_impersonation",
        "Result Verifier pretending to be Final Phase Verifier." in naming_md,
    )
    add(
        "naming_standard_forbids_runner_go_output",
        "Runner output claiming GO." in naming_md,
    )

    statuses = status_reg.get("statuses", [])
    status_names = {s.get("status") for s in statuses if isinstance(s, dict)}
    add(
        "status_registry_complete_true",
        status_reg.get("status_registry_complete") is True,
    )
    add("status_registry_contains_required_statuses", status_names == EXPECTED_STATUSES)
    add(
        "status_registry_agent_may_not_emit_go_true",
        status_reg.get("agent_may_not_emit_go") is True,
    )
    add(
        "status_registry_agent_max_waiting_status",
        status_reg.get("agent_highest_normal_completion_status")
        == "WAITING_FOR_USER_TERMINAL_VERIFICATION",
    )
    add(
        "status_registry_go_requires_v2_v3_true",
        status_reg.get("go_requires_user_v2_plus_chatgpt_v3") is True,
    )

    classes = remediation.get("failure_classes", {})
    add(
        "remediation_classes_complete_set",
        set(classes.keys()) == EXPECTED_FAILURE_CLASSES,
    )
    add(
        "remediation_each_class_has_required_keys",
        all(
            isinstance(v, dict)
            and {
                "description",
                "remediation_scope",
                "allowed_files",
                "prohibited_shortcuts",
                "rerun_requirement",
                "next_status",
            }.issubset(set(v.keys()))
            for v in classes.values()
        ),
    )
    principles = remediation.get("remediation_principles", {})
    add(
        "remediation_principles_no_shortcuts",
        all(
            principles.get(k) is True
            for k in [
                "fix_failed_items_only",
                "do_not_modify_passed_assets",
                "do_not_delete_checks",
                "do_not_hide_failure_by_renaming",
                "do_not_hardcode_pass",
                "do_not_reduce_check_count",
                "do_not_change_success_conditions",
                "user_must_rerun_original_final_phase_verifier",
            ]
        ),
    )
    add(
        "remediation_standard_complete_true",
        remediation.get("failure_classification_complete") is True,
    )

    add(
        "compliance_contract_complete_true",
        compliance.get("compliance_contract_complete") is True,
    )
    add(
        "agent_not_run_final_phase_verifier_true",
        compliance.get("must_not_run_final_phase_verifier") is True,
    )
    add("agent_not_declare_go_true", compliance.get("must_not_declare_go") is True)
    add(
        "repo_governance_source_true",
        compliance.get("must_use_repository_governance_assets") is True,
    )
    add(
        "private_memory_not_only_source_true",
        compliance.get("must_not_use_private_editor_memory_as_only_source") is True,
    )

    add(
        "summary_repository_governance_created_true",
        summary.get("repository_governance_created") is True,
    )
    add(
        "summary_role_standard_created_true",
        summary.get("role_standard_created") is True,
    )
    add(
        "summary_verification_authority_standard_created_true",
        summary.get("verification_authority_standard_created") is True,
    )
    add(
        "summary_execution_mode_matrix_created_true",
        summary.get("execution_mode_matrix_created") is True,
    )
    add(
        "summary_phase_template_created_true",
        summary.get("phase_template_created") is True,
    )
    add(
        "summary_runner_verifier_naming_standard_created_true",
        summary.get("runner_verifier_naming_standard_created") is True,
    )
    add(
        "summary_status_registry_created_true",
        summary.get("verification_status_registry_created") is True,
    )
    add(
        "summary_remediation_standard_created_true",
        summary.get("remediation_standard_created") is True,
    )
    add(
        "summary_agent_compliance_contract_created_true",
        summary.get("agent_compliance_contract_created") is True,
    )
    add(
        "summary_user_terminal_final_verifier_executor_true",
        summary.get("user_terminal_is_final_phase_verifier_executor") is True,
    )
    add(
        "summary_chatgpt_final_audit_authority_true",
        summary.get("chatgpt_is_final_audit_and_decision_authority") is True,
    )
    add(
        "summary_agent_may_not_declare_go_true",
        summary.get("agent_may_not_declare_go") is True,
    )
    add(
        "summary_repository_source_of_truth_true",
        summary.get("repository_is_source_of_truth") is True,
    )
    add(
        "summary_vscode_private_memory_source_of_truth_false",
        summary.get("vscode_private_memory_is_source_of_truth") is False,
    )
    add(
        "summary_product_runtime_modified_false",
        summary.get("product_runtime_modified") is False,
    )
    add(
        "summary_existing_phase_decisions_modified_false",
        summary.get("existing_phase_decisions_modified") is False,
    )
    add("summary_blocker_count_zero", summary.get("blocker_count") == 0)
    add(
        "summary_final_decision_exact",
        summary.get("final_decision") == EXPECTED_DECISION,
    )
    add("summary_next_exact", summary.get("recommended_next_phase") == EXPECTED_NEXT)

    failed = [c for c in checks if not c["passed"]]
    passed_count = sum(1 for c in checks if c["passed"])
    failed_count = len(failed)
    blocker_count = failed_count

    final_decision = (
        EXPECTED_DECISION
        if blocker_count == 0
        else "LUNA_ENGINEERING_EXECUTION_AND_VERIFICATION_GOVERNANCE_STANDARDIZATION_BLOCKED"
    )
    next_phase = (
        EXPECTED_NEXT
        if blocker_count == 0
        else "Phase-Luna-Engineering-Execution-And-Verification-Governance-Standardization-Output-Contract-Correction-v1-001"
    )

    print("CHECKS")
    for c in checks:
        print(f"- [{'PASS' if c['passed'] else 'FAIL'}] {c['name']}")
    print("FAILED_CHECKS")
    if failed:
        for c in failed:
            print(
                f"- {c['name']}: {c['detail'] if c['detail'] else 'condition_not_met'}"
            )
    else:
        print("- NONE")
    print("PASSED_CHECK_COUNT")
    print(passed_count)
    print("FAILED_CHECK_COUNT")
    print(failed_count)
    print("BLOCKER_COUNT")
    print(blocker_count)
    print("FINAL_DECISION")
    print(final_decision)
    print("NEXT")
    print(next_phase)

    return 0 if blocker_count == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
