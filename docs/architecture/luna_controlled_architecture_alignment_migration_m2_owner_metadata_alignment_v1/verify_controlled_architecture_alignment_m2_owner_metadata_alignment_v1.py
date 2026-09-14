#!/usr/bin/env python3
"""Static final verifier for M2 Owner Metadata Alignment.

The verifier validates planning assets only. It does not import Luna business
modules, modify files, execute Runtime, call models, or execute migration.
"""

from __future__ import annotations

import ast
import json
from collections import Counter
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[3]

REQUIRED_JSON = [
    "owner_alignment_registry_candidate.json",
    "responsibility_boundary_matrix_candidate.json",
    "capability_registry_alignment_candidate.json",
    "owner_conflict_review.json",
    "m2_change_manifest.json",
    "phase_contract.json",
]
REQUIRED_MARKDOWN = ["owner_metadata_alignment_plan.md"]
VERIFIER_NAME = "verify_controlled_architecture_alignment_m2_owner_metadata_alignment_v1.py"
REQUIRED_FILES = [
    "owner_alignment_registry_candidate.json",
    "responsibility_boundary_matrix_candidate.json",
    "capability_registry_alignment_candidate.json",
    "owner_conflict_review.json",
    "owner_metadata_alignment_plan.md",
    "m2_change_manifest.json",
    "phase_contract.json",
    VERIFIER_NAME,
]

EXISTING_ASSETS = {
    "luna.field_state_reducer",
    "luna.field_state_read_model",
    "luna.observation_manager",
    "luna.task_manager",
    "luna.model_manager",
    "luna.protocol_manager",
    "luna.ocr_manager",
    "luna.vision_manager",
    "luna.memory_system",
}
FUTURE_ASSETS = {
    "luna.personal_cognitive_network",
    "luna.intent_architecture",
    "luna.causal_reasoning",
    "luna.experience_compression",
    "luna.a_b_route_boundary",
    "luna.decision_arbitration",
}
REQUIRED_MATRIX_OWNERS = {
    "Field State Reducer",
    "Field State Read Model",
    "Observation Manager",
    "Task Manager",
    "Capability Governance / Model Manager",
    "Protocol Manager",
    "Capability Governance / OCR Capability",
    "Capability Governance / Vision Capability",
    "Memory System",
    "Personal Cognitive Network Governance",
    "Intent Governance",
    "Causal Reasoning Governance",
    "Experience Governance",
    "A/B Route Boundary Governance",
    "Decision Arbitration",
}
ALLOWED_OWNER_STATUSES = {"ACTIVE_EXISTING", "PLANNING_CANDIDATE"}
ALLOWED_ALIGNMENT_TYPES = {"KEEP", "BOUNDARY_ALIGNMENT_ONLY", "FUTURE_REFERENCE", "BLOCKED"}


class Checks:
    def __init__(self) -> None:
        self.total = 0
        self.failed: list[str] = []

    def check(self, condition: bool, name: str) -> None:
        self.total += 1
        if not condition:
            self.failed.append(name)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def lower_join(values: list[str]) -> str:
    return " ".join(values).lower()


def main() -> int:
    checks = Checks()
    loaded: dict[str, Any] = {}

    for name in REQUIRED_FILES:
        checks.check((HERE / name).is_file(), f"required_file:{name}")
    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    checks.check(actual_files == set(REQUIRED_FILES), "target_directory_exact_file_set")
    checks.check({path.name for path in HERE.glob("*.py")} == {VERIFIER_NAME}, "final_verifier_only_python_file")

    for name in REQUIRED_JSON:
        try:
            loaded[name] = load_json(HERE / name)
            checks.check(bool(loaded[name]), f"json_nonempty:{name}")
        except (OSError, json.JSONDecodeError):
            loaded[name] = {}
            checks.check(False, f"json_parse:{name}")

    for name in REQUIRED_MARKDOWN:
        try:
            content = (HERE / name).read_text(encoding="utf-8")
        except OSError:
            content = ""
        checks.check(len(content.strip()) > 500, f"markdown_substantial:{name}")

    try:
        verifier_source = (HERE / VERIFIER_NAME).read_text(encoding="utf-8")
        verifier_tree = ast.parse(verifier_source)
        checks.check(True, "verifier_ast")
    except (OSError, SyntaxError):
        verifier_tree = ast.parse("pass")
        checks.check(False, "verifier_ast")

    owner_registry = loaded.get("owner_alignment_registry_candidate.json", {})
    owner_records = owner_registry.get("records", [])
    owner_by_asset = {item.get("asset_id"): item for item in owner_records}
    checks.check(owner_registry.get("planning_status") == "PLANNING_CANDIDATE", "owner_registry_planning_status")
    checks.check(owner_registry.get("candidate_only") is True, "owner_registry_candidate_only")
    checks.check(len(owner_records) == 15, "owner_registry_record_count")
    checks.check(len(owner_by_asset) == len(owner_records), "asset_ids_unique")
    checks.check(set(owner_by_asset) == EXISTING_ASSETS | FUTURE_ASSETS, "owner_registry_required_assets")
    checks.check(all(
        item.get("asset_type") and item.get("current_owner") and item.get("candidate_owner")
        and item.get("architecture_position") and item.get("owner_status") in ALLOWED_OWNER_STATUSES
        and item.get("write_authority") and item.get("read_consumers")
        and item.get("forbidden_responsibility") and item.get("source_refs")
        and item.get("compatibility_status") for item in owner_records
    ), "owner_records_complete")
    checks.check(all(owner_by_asset[item].get("owner_status") == "ACTIVE_EXISTING" for item in EXISTING_ASSETS), "existing_owner_statuses")
    checks.check(all(owner_by_asset[item].get("owner_status") == "PLANNING_CANDIDATE" for item in FUTURE_ASSETS), "future_owner_statuses")
    checks.check(all(item.get("current_owner") == item.get("candidate_owner") for item in owner_records), "no_owner_transfer")
    checks.check(len({item.get("write_authority") for item in owner_records}) == len(owner_records), "write_authority_descriptions_unique")
    for item in owner_records:
        for ref in item.get("source_refs", []):
            checks.check((ROOT / ref).exists(), f"owner_source_ref:{item.get('asset_id')}:{ref}")

    field_forbidden = lower_join(owner_by_asset.get("luna.field_state_reducer", {}).get("forbidden_responsibility", []))
    checks.check("user intent" in field_forbidden, "field_forbids_user_intent")
    checks.check("decision" in field_forbidden, "field_forbids_decision")
    observation_forbidden = lower_join(owner_by_asset.get("luna.observation_manager", {}).get("forbidden_responsibility", []))
    checks.check("cognition" in observation_forbidden, "observation_forbids_cognition")
    checks.check("decision" in observation_forbidden, "observation_forbids_decision")
    task_forbidden = lower_join(owner_by_asset.get("luna.task_manager", {}).get("forbidden_responsibility", []))
    checks.check("intent generation" in task_forbidden, "task_forbids_intent_generation")
    checks.check("causal reasoning" in task_forbidden, "task_forbids_causal_reasoning")
    memory_forbidden = lower_join(owner_by_asset.get("luna.memory_system", {}).get("forbidden_responsibility", []))
    checks.check("reality override" in memory_forbidden, "memory_forbids_reality_override")
    checks.check("decision" in memory_forbidden, "memory_forbids_decision")
    pcn_forbidden = lower_join(owner_by_asset.get("luna.personal_cognitive_network", {}).get("forbidden_responsibility", []))
    for phrase in ["source ownership", "source mutation", "source persistence", "self ownership", "role ownership", "relationship ownership", "memory ownership", "emotion ownership", "value ownership"]:
        checks.check(phrase in pcn_forbidden, f"pcn_forbidden:{phrase}")
    checks.check(owner_registry.get("active_metadata_change") is False, "owner_registry_no_active_metadata_change")
    checks.check(owner_registry.get("owner_transfer") is False, "owner_registry_no_owner_transfer_execution")
    checks.check(owner_registry.get("migration_executed") is False, "owner_registry_no_migration")

    boundary_matrix = loaded.get("responsibility_boundary_matrix_candidate.json", {})
    boundary_records = boundary_matrix.get("records", [])
    boundary_by_owner = {item.get("owner"): item for item in boundary_records}
    checks.check(boundary_matrix.get("planning_status") == "PLANNING_CANDIDATE", "boundary_matrix_planning_status")
    checks.check(len(boundary_records) == 15, "boundary_record_count")
    checks.check(len(boundary_by_owner) == len(boundary_records), "boundary_owners_unique")
    checks.check(set(boundary_by_owner) == REQUIRED_MATRIX_OWNERS, "boundary_required_owners")
    checks.check(all(item.get("responsibility") and item.get("forbidden_responsibility") and item.get("write_scope") and item.get("read_scope") for item in boundary_records), "boundary_records_complete")
    write_scopes = [scope for item in boundary_records for scope in item.get("write_scope", [])]
    checks.check(not [scope for scope, count in Counter(write_scopes).items() if count > 1], "no_duplicate_write_scope")
    checks.check(boundary_matrix.get("single_writer_per_scope") is True, "single_writer_declared")
    checks.check(boundary_matrix.get("active_metadata_modified") is False, "boundary_no_active_metadata_change")
    checks.check(boundary_matrix.get("migration_executed") is False, "boundary_no_migration")

    capability_registry = loaded.get("capability_registry_alignment_candidate.json", {})
    capability_records = capability_registry.get("records", [])
    capability_ids = {item.get("capability") for item in capability_records}
    checks.check(capability_registry.get("planning_status") == "PLANNING_CANDIDATE", "capability_alignment_planning_status")
    checks.check(len(capability_records) == 15, "capability_alignment_count")
    checks.check(capability_ids == EXISTING_ASSETS | FUTURE_ASSETS, "capability_alignment_required_assets")
    checks.check(all(
        item.get("architecture_position") and item.get("owner") and item.get("baseline_reference")
        and item.get("alignment_type") in ALLOWED_ALIGNMENT_TYPES
        and item.get("migration_required") is False and item.get("notes")
        for item in capability_records
    ), "capability_alignment_records_complete")
    for item in capability_records:
        checks.check((ROOT / item.get("baseline_reference", "")).exists(), f"capability_reference:{item.get('capability')}")
    checks.check(all(item.get("alignment_type") in {"KEEP", "BOUNDARY_ALIGNMENT_ONLY"} for item in capability_records if item.get("capability") in EXISTING_ASSETS), "existing_alignment_types")
    checks.check(all(item.get("alignment_type") == "FUTURE_REFERENCE" for item in capability_records if item.get("capability") in FUTURE_ASSETS), "future_alignment_types")
    checks.check(capability_registry.get("active_registry_change_required") is False, "no_active_registry_change")
    checks.check(capability_registry.get("active_baseline_change_required") is False, "no_active_baseline_change")
    checks.check(capability_registry.get("migration_executed") is False, "capability_registry_no_migration")

    conflict_review = loaded.get("owner_conflict_review.json", {})
    reviews = conflict_review.get("reviews", [])
    checks.check(conflict_review.get("planning_status") == "PLANNING_CANDIDATE", "conflict_review_planning_status")
    checks.check(len(reviews) == 15, "conflict_review_coverage")
    checks.check(all(item.get("asset") and item.get("resolution") for item in reviews), "conflict_review_records_complete")
    checks.check(all(item.get("conflict") is False for item in reviews), "review_no_conflicts")
    checks.check(all(item.get("blocker") is False for item in reviews), "review_no_blockers")
    checks.check(conflict_review.get("conflicts") == [], "conflict_list_empty")
    checks.check(conflict_review.get("blocker_count") == 0, "blocker_count_zero")
    for key in ["duplicate_owner_detected", "duplicate_writer_detected", "owner_drift_detected", "permission_conflict_detected", "active_metadata_modified", "migration_executed"]:
        checks.check(conflict_review.get(key) is False, f"conflict_flag_false:{key}")

    plan_text = (HERE / "owner_metadata_alignment_plan.md").read_text(encoding="utf-8")
    plan_lower = plan_text.lower()
    for stage in ["M2.0", "M2.1", "M2.2", "M2.3", "M2.4"]:
        checks.check(stage in plan_text, f"plan_stage:{stage}")
    for phrase, name in [
        ("architecture-domain placement is not ownership transfer", "plan_no_owner_transfer"),
        ("do not edit active owner metadata", "plan_no_active_metadata_edit"),
        ("do not create a second writer", "plan_no_second_writer"),
        ("do not start m3", "plan_no_m3"),
        ("waiting_for_user_terminal_verification", "plan_stop_status"),
    ]:
        checks.check(phrase in plan_lower, name)

    manifest = loaded.get("m2_change_manifest.json", {})
    checks.check(set(manifest.get("created_files", [])) == set(REQUIRED_FILES), "manifest_exact_created_files")
    for key in ["modified_existing_files", "deleted_files", "moved_files", "renamed_files", "code_files_changed", "runtime_files_changed", "baseline_files_changed", "active_schema_files_changed", "active_contract_files_changed", "registry_baseline_files_changed", "active_metadata_changed", "capability_implementation_changed"]:
        checks.check(manifest.get(key) == [], f"manifest_empty:{key}")
    for key in ["migration_executed", "runtime_activated", "owner_transfer_executed", "m3_started"]:
        checks.check(manifest.get(key) is False, f"manifest_false:{key}")
    checks.check(manifest.get("planning_candidate_only") is True, "manifest_planning_only")

    phase = loaded.get("phase_contract.json", {})
    required_phase_fields = {
        "Phase", "Stage", "Execution Mode", "Current Work Description", "Previous Phase",
        "Previous Phase Decision", "Input Assets", "Required Pre-Read", "Target Directory",
        "Scope", "Out Of Scope", "Required Final Files", "Implementation Principles",
        "Required Checks", "Negative Guards", "Verification Authority", "Allowed Agent Checks",
        "Allowed Agent Execution", "Prohibited Agent Execution", "Agent Stop Point",
        "User Terminal Commands", "Expected Success Decision", "Expected Next",
        "Expected Failure Decision", "Expected Failure Next", "Stop Condition",
        "Blocker Conditions", "Completion Report Format", "Current Status Contract"
    }
    checks.check(required_phase_fields.issubset(phase), "phase_required_fields")
    checks.check(phase.get("Phase") == "Phase-Luna-Controlled-Architecture-Alignment-Migration-M2-Owner-Metadata-Alignment-v1-001", "phase_identity")
    checks.check(phase.get("Execution Mode") == "Planning Only", "phase_execution_mode")
    checks.check(phase.get("Previous Phase Decision") == "LUNA_CONTROLLED_ARCHITECTURE_ALIGNMENT_M1_SCHEMA_CONTRACT_ALIGNMENT_READY", "previous_phase_decision")
    checks.check(phase.get("Required Final Files") == REQUIRED_FILES, "phase_required_file_order")
    authority = phase.get("Verification Authority", {})
    checks.check(authority.get("V0") == "Agent", "v0_authority")
    checks.check(authority.get("V1") == "Not Authorized", "v1_authority")
    checks.check(authority.get("V2") == "User Terminal Only", "v2_authority")
    checks.check(authority.get("V3") == "ChatGPT Only", "v3_authority")
    checks.check(phase.get("Agent Stop Point") == "WAITING_FOR_USER_TERMINAL_VERIFICATION", "agent_stop_point")
    checks.check(phase.get("Current Status Contract") == "WAITING_FOR_USER_TERMINAL_VERIFICATION", "current_status_contract")
    checks.check(phase.get("User Terminal Commands") == ["python3 docs/architecture/luna_controlled_architecture_alignment_migration_m2_owner_metadata_alignment_v1/verify_controlled_architecture_alignment_m2_owner_metadata_alignment_v1.py"], "exact_user_terminal_command")
    checks.check(phase.get("Migration") is False, "phase_migration_false")
    checks.check(phase.get("Runtime Change") is False, "phase_runtime_change_false")
    checks.check(phase.get("Active Metadata Change") is False, "phase_active_metadata_change_false")
    checks.check(phase.get("M3 Started") is False, "phase_m3_false")
    negative_guards = lower_join(phase.get("Negative Guards", []))
    for phrase in ["no-check-weaken", "no-hardcoded-pass", "no final phase verifier by agent", "no migration execution", "no m3 entry"]:
        checks.check(phrase in negative_guards, f"negative_guard:{phrase}")

    imported_roots: set[str] = set()
    for node in ast.walk(verifier_tree):
        if isinstance(node, ast.Import):
            imported_roots.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_roots.add(node.module.split(".", 1)[0])
    checks.check(imported_roots.issubset({"__future__", "ast", "json", "collections", "pathlib", "typing"}), "verifier_standard_library_import_boundary")

    failed = checks.failed
    passed_count = checks.total - len(failed)
    print(f"CHECKS: {checks.total}")
    print(f"FAILED_CHECKS: {failed}")
    print(f"PASSED_CHECK_COUNT: {passed_count}")
    print(f"FAILED_CHECK_COUNT: {len(failed)}")
    print(f"BLOCKER_COUNT: {len(failed)}")
    if failed:
        print("FINAL_DECISION: BLOCKED_BY_VERIFIER_FAILURE")
        print("READINESS: LUNA_CONTROLLED_ARCHITECTURE_ALIGNMENT_M2_OWNER_METADATA_ALIGNMENT_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_CONTROLLED_ARCHITECTURE_ALIGNMENT_M2_OWNER_METADATA_ALIGNMENT_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
