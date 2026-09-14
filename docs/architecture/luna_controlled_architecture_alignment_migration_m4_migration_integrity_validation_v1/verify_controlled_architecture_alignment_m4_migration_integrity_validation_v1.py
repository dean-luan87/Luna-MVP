#!/usr/bin/env python3
"""Read-only final verifier for the M4 migration-integrity planning phase."""

from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any


BASE = Path(__file__).resolve().parent
REPO_ROOT = BASE.parents[2]

REQUIRED_FILES = {
    "cross_phase_consistency_matrix.json",
    "migration_integrity_checklist.json",
    "migration_safety_assessment.md",
    "validation_evidence_registry.json",
    "rollback_readiness_review.json",
    "migration_blocker_registry.json",
    "m4_migration_integrity_validation_summary.md",
    "m4_change_manifest.json",
    "phase_contract.json",
    "verify_controlled_architecture_alignment_m4_migration_integrity_validation_v1.py",
}

JSON_FILES = {
    "cross_phase_consistency_matrix.json",
    "migration_integrity_checklist.json",
    "validation_evidence_registry.json",
    "rollback_readiness_review.json",
    "migration_blocker_registry.json",
    "m4_change_manifest.json",
    "phase_contract.json",
}

MARKDOWN_FILES = {
    "migration_safety_assessment.md",
    "m4_migration_integrity_validation_summary.md",
}

REQUIRED_PHASE_LINKS = {
    ("M0 Documentation Alignment", "M1 Schema / Contract Alignment"),
    ("M1 Schema / Contract Alignment", "M2 Owner Metadata Alignment"),
    ("M2 Owner Metadata Alignment", "M3 Runtime Boundary Alignment"),
    ("M0 Documentation Alignment", "M3 Runtime Boundary Alignment"),
}

REQUIRED_INTEGRITY_CHECKS = {
    "Dynamic Architecture v2 positioning is correct",
    "Dynamic Architecture v2 does not replace Baseline",
    "Candidate contracts are not activated",
    "Fact and Candidate remain separated",
    "No second Writer is introduced",
    "Owner is unique",
    "Write Authority is unique",
    "Runtime does not own Cognition",
    "Runtime remains unmodified",
    "Legacy assets are preserved",
    "Rollback remains definable",
}

REQUIRED_BLOCKER_CATEGORIES = {
    "Owner conflict",
    "Contract conflict",
    "Runtime conflict",
    "Legacy conflict",
    "Missing dependency",
}

REQUIRED_ROLLBACK_ITEMS = {
    "Preserve active engineering Baseline",
    "Withdraw candidate mappings and contracts",
    "Preserve historical architecture documents",
    "Restore and preserve Owner boundaries",
}

ALLOWED_IMPORT_ROOTS = {"__future__", "ast", "json", "pathlib", "typing"}
FORBIDDEN_MUTATION_CALLS = {
    "write_text",
    "write_bytes",
    "unlink",
    "rename",
    "replace",
    "mkdir",
    "rmdir",
    "touch",
    "chmod",
}


def load_json(name: str) -> Any:
    return json.loads((BASE / name).read_text(encoding="utf-8"))


def main() -> int:
    checks: list[str] = []
    failed: list[str] = []

    def check(condition: bool, name: str) -> None:
        checks.append(name)
        if not condition:
            failed.append(name)

    actual_files = {path.name for path in BASE.iterdir() if path.is_file()}
    check(actual_files == REQUIRED_FILES, "exact_required_file_set")

    data: dict[str, Any] = {}
    for name in sorted(JSON_FILES):
        try:
            data[name] = load_json(name)
            check(True, f"json_parse:{name}")
        except (OSError, json.JSONDecodeError):
            data[name] = {}
            check(False, f"json_parse:{name}")

    for name in sorted(MARKDOWN_FILES):
        try:
            content = (BASE / name).read_text(encoding="utf-8")
            check(bool(content.strip()), f"markdown_nonempty:{name}")
        except OSError:
            check(False, f"markdown_nonempty:{name}")

    for name in sorted(JSON_FILES):
        check(data.get(name, {}).get("planning_status") == "PLANNING_CANDIDATE", f"planning_candidate:{name}")

    matrix = data.get("cross_phase_consistency_matrix.json", {})
    matrix_records = matrix.get("records", [])
    check(isinstance(matrix_records, list) and bool(matrix_records), "cross_phase_records_present")
    links = {
        (record.get("source_phase"), record.get("target_phase"))
        for record in matrix_records
        if isinstance(record, dict)
    }
    check(REQUIRED_PHASE_LINKS.issubset(links), "required_cross_phase_links")
    check(
        all(
            isinstance(record, dict)
            and all(
                key in record
                for key in (
                    "check_id",
                    "source_phase",
                    "target_phase",
                    "consistency_status",
                    "evidence_refs",
                    "conflict",
                    "resolution",
                )
            )
            for record in matrix_records
        ),
        "cross_phase_record_fields",
    )
    check(all(record.get("consistency_status") == "PASS" for record in matrix_records), "cross_phase_all_pass")
    check(all(record.get("conflict") == "" for record in matrix_records), "cross_phase_no_conflict")
    check(all(bool(record.get("resolution")) for record in matrix_records), "cross_phase_resolution_present")
    matrix_refs = [
        ref
        for record in matrix_records
        for ref in record.get("evidence_refs", [])
        if isinstance(ref, str)
    ]
    check(bool(matrix_refs), "cross_phase_evidence_refs_present")
    check(all((REPO_ROOT / ref).exists() for ref in matrix_refs), "cross_phase_evidence_refs_exist")
    check(matrix.get("conflict_count") == 0, "cross_phase_conflict_count_zero")
    check(matrix.get("blocked_count") == 0, "cross_phase_blocked_count_zero")
    check(matrix.get("migration_executed") is False, "cross_phase_no_migration")

    checklist = data.get("migration_integrity_checklist.json", {})
    checklist_records = checklist.get("records", [])
    checklist_names = {record.get("check") for record in checklist_records if isinstance(record, dict)}
    check(REQUIRED_INTEGRITY_CHECKS.issubset(checklist_names), "integrity_required_checks")
    check(
        all(
            isinstance(record, dict)
            and all(key in record for key in ("check", "status", "evidence", "blocker"))
            for record in checklist_records
        ),
        "integrity_record_fields",
    )
    check(all(record.get("status") == "PASS" for record in checklist_records), "integrity_all_pass")
    check(all(record.get("blocker") is False for record in checklist_records), "integrity_no_record_blocker")
    check(all(bool(record.get("evidence")) for record in checklist_records), "integrity_evidence_present")
    check(checklist.get("pass_count") == len(checklist_records), "integrity_pass_count")
    check(checklist.get("fail_count") == 0, "integrity_fail_count_zero")
    check(checklist.get("blocker_count") == 0, "integrity_blocker_count_zero")
    check(checklist.get("migration_executed") is False, "integrity_no_migration")

    safety = (BASE / "migration_safety_assessment.md").read_text(encoding="utf-8")
    for token, name in (
        ("PLANNING_CANDIDATE", "safety_planning_candidate"),
        ("Migration Executed: `false`", "safety_migration_false"),
        ("M5 Started: `false`", "safety_m5_false"),
        ("eligible for M5 architecture-freeze review only", "safety_condition_limited"),
        ("does **not** mean migration execution is approved", "safety_no_execution_authority"),
        ("Boundaries Ready to Freeze", "safety_frozen_boundaries"),
        ("Items That Remain Future Planning", "safety_future_planning"),
        ("Cannot Be Migrated in M4", "safety_cannot_migrate"),
    ):
        check(token in safety, name)

    evidence = data.get("validation_evidence_registry.json", {})
    evidence_records = evidence.get("records", [])
    evidence_phases = {record.get("source_phase") for record in evidence_records if isinstance(record, dict)}
    check(set(evidence.get("required_phase_coverage", [])) == evidence_phases, "evidence_phase_coverage")
    check(
        all(
            isinstance(record, dict)
            and all(key in record for key in ("validation_item", "source_phase", "source_file", "evidence_type", "verified"))
            for record in evidence_records
        ),
        "evidence_record_fields",
    )
    check(all(record.get("verified") is True for record in evidence_records), "evidence_all_verified")
    check(all((REPO_ROOT / record.get("source_file", "")).exists() for record in evidence_records), "evidence_source_files_exist")
    check(evidence.get("all_evidence_verified") is True, "evidence_registry_verified")
    check(evidence.get("migration_executed") is False, "evidence_no_migration")

    rollback = data.get("rollback_readiness_review.json", {})
    rollback_records = rollback.get("records", [])
    rollback_names = {record.get("rollback_item") for record in rollback_records if isinstance(record, dict)}
    check(REQUIRED_ROLLBACK_ITEMS.issubset(rollback_names), "rollback_required_items")
    check(
        all(
            isinstance(record, dict)
            and all(key in record for key in ("rollback_item", "available", "scope", "risk"))
            for record in rollback_records
        ),
        "rollback_record_fields",
    )
    check(all(record.get("available") is True for record in rollback_records), "rollback_all_available")
    check(all(bool(record.get("scope")) and bool(record.get("risk")) for record in rollback_records), "rollback_scope_and_risk")
    check(rollback.get("rollback_gaps") == [], "rollback_no_gap")
    check(rollback.get("migration_executed") is False, "rollback_no_migration")

    blocker = data.get("migration_blocker_registry.json", {})
    reviewed_categories = blocker.get("reviewed_categories", [])
    categories = {record.get("category") for record in reviewed_categories if isinstance(record, dict)}
    check(categories == REQUIRED_BLOCKER_CATEGORIES, "blocker_required_categories")
    check(all(record.get("status") == "CLEAR" and bool(record.get("evidence")) for record in reviewed_categories), "blocker_categories_clear")
    check(blocker.get("blockers") == [], "blocker_registry_empty")
    check(blocker.get("blocker_count") == 0, "blocker_count_zero")
    check(blocker.get("migration_executed") is False, "blocker_no_migration")
    check(blocker.get("m5_started") is False, "blocker_m5_not_started")

    summary = (BASE / "m4_migration_integrity_validation_summary.md").read_text(encoding="utf-8")
    for token, name in (
        ("M0 Documentation Alignment: completed", "summary_m0_complete"),
        ("M1 Schema / Contract Alignment: completed", "summary_m1_complete"),
        ("M2 Owner Metadata Alignment: completed", "summary_m2_complete"),
        ("M3 Runtime Boundary Alignment: completed", "summary_m3_complete"),
        ("Migration: `NOT_EXECUTED`", "summary_migration_not_executed"),
        ("M5 Started: `false`", "summary_m5_false"),
        ("M5 has not started", "summary_m5_not_started"),
        ("WAITING_FOR_USER_TERMINAL_VERIFICATION", "summary_waiting_status"),
    ):
        check(token in summary, name)

    manifest = data.get("m4_change_manifest.json", {})
    check(set(manifest.get("created_files", [])) == REQUIRED_FILES, "manifest_created_file_set")
    for field in (
        "modified_existing_files",
        "deleted_files",
        "moved_files",
        "renamed_files",
        "code_files_changed",
        "runtime_files_changed",
        "baseline_files_changed",
        "active_schema_files_changed",
        "active_contract_files_changed",
        "active_registry_files_changed",
        "active_owner_metadata_changed",
    ):
        check(manifest.get(field) == [], f"manifest_empty:{field}")
    for field in (
        "schema_changed",
        "contract_changed",
        "owner_metadata_changed",
        "candidate_contract_activated",
        "adapter_created",
        "cognitive_runtime_created",
        "migration_executed",
        "runtime_activated",
        "m5_started",
    ):
        check(manifest.get(field) is False, f"manifest_false:{field}")
    check(manifest.get("planning_candidate_only") is True, "manifest_planning_only")

    phase = data.get("phase_contract.json", {})
    check(phase.get("Execution Mode") == "Planning Only", "phase_execution_mode")
    check(phase.get("Execution Profile") == "Validation Planning Only", "phase_execution_profile")
    check(phase.get("Previous Phase Decision") == "LUNA_CONTROLLED_ARCHITECTURE_ALIGNMENT_M3_RUNTIME_BOUNDARY_ALIGNMENT_READY", "phase_previous_decision")
    check(set(phase.get("Required Final Files", [])) == REQUIRED_FILES, "phase_required_file_set")
    authority = phase.get("Verification Authority", {})
    check(authority.get("V0") == "Agent", "authority_v0")
    check(authority.get("V1") == "Not Authorized", "authority_v1")
    check(authority.get("V2") == "User Terminal Only", "authority_v2")
    check(authority.get("V3") == "ChatGPT Only", "authority_v3")
    check(phase.get("Migration") is False, "phase_migration_false")
    check(phase.get("Runtime Change") is False, "phase_runtime_false")
    check(phase.get("Schema Change") is False, "phase_schema_false")
    check(phase.get("Contract Change") is False, "phase_contract_false")
    check(phase.get("Owner Metadata Change") is False, "phase_owner_metadata_false")
    check(phase.get("M5 Started") is False, "phase_m5_false")
    check(phase.get("Agent Stop Point") == "WAITING_FOR_USER_TERMINAL_VERIFICATION", "phase_stop_point")
    expected_command = "python3 docs/architecture/luna_controlled_architecture_alignment_migration_m4_migration_integrity_validation_v1/verify_controlled_architecture_alignment_m4_migration_integrity_validation_v1.py"
    check(phase.get("User Terminal Commands") == [expected_command], "phase_terminal_command")
    check(phase.get("Expected Success Decision") == "V2_FINAL_VERIFICATION_PASSED", "phase_success_decision")
    check(phase.get("Expected Success Readiness") == "LUNA_CONTROLLED_ARCHITECTURE_ALIGNMENT_M4_MIGRATION_INTEGRITY_VALIDATION_READY", "phase_success_readiness")
    check(phase.get("Expected Failure Decision") == "BLOCKED_BY_VERIFIER_FAILURE", "phase_failure_decision")
    check(phase.get("Expected Failure Readiness") == "LUNA_CONTROLLED_ARCHITECTURE_ALIGNMENT_M4_MIGRATION_INTEGRITY_VALIDATION_REMEDIATION_REQUIRED", "phase_failure_readiness")

    verifier_path = BASE / "verify_controlled_architecture_alignment_m4_migration_integrity_validation_v1.py"
    try:
        tree = ast.parse(verifier_path.read_text(encoding="utf-8"))
        check(True, "verifier_ast_parse")
    except (OSError, SyntaxError):
        tree = ast.Module(body=[], type_ignores=[])
        check(False, "verifier_ast_parse")

    import_roots: set[str] = set()
    mutation_calls: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            import_roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            import_roots.add(node.module.split(".")[0])
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr in FORBIDDEN_MUTATION_CALLS:
                mutation_calls.add(node.func.attr)
    check(import_roots.issubset(ALLOWED_IMPORT_ROOTS), "verifier_standard_imports_only")
    check(not mutation_calls, "verifier_read_only_calls")

    print(f"CHECKS: {len(checks)}")
    print(f"FAILED_CHECKS: {failed}")
    print(f"PASSED_CHECK_COUNT: {len(checks) - len(failed)}")
    print(f"FAILED_CHECK_COUNT: {len(failed)}")
    print(f"BLOCKER_COUNT: {len(failed)}")
    if failed:
        print("FINAL_DECISION: BLOCKED_BY_VERIFIER_FAILURE")
        print("READINESS: LUNA_CONTROLLED_ARCHITECTURE_ALIGNMENT_M4_MIGRATION_INTEGRITY_VALIDATION_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1

    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_CONTROLLED_ARCHITECTURE_ALIGNMENT_M4_MIGRATION_INTEGRITY_VALIDATION_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
