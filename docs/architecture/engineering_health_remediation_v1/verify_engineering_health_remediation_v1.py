#!/usr/bin/env python3
"""V2 verifier for Engineering Health Remediation.

The verifier is intentionally user-terminal oriented. It validates the phase
contracts, rechecks the bounded syntax remediation, scans architecture
directory status, and runs compileall as a health gate. It does not invoke a
model, provider, hardware, action, migration, or runtime path.
"""
import compileall
import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent
REPO_ROOT = BASE.parents[2]
ARCH_ROOT = REPO_ROOT / "docs" / "architecture"

MD_REQ = {
    "engineering_health_remediation_plan_v1.md": [
        "Engineering Health Remediation v1", "Phase-Engineering-Health-Remediation-v1-001", "Remediation",
        "Previous Phase Decision", "BLOCKED_BEFORE_USER_TERMINAL_VERIFICATION", "R1", "Python syntax",
        "R2", "Architecture inventory", "R3", "Canonical Schema Registry", "R4", "Large-file governance",
        "BOUNDARY_FLAGS", "RECOMMENDED_NEXT_PHASE", "active", "historical", "verification_only",
        "missing_asset_candidate", "V0 Agent checks", "python3 -m compileall capabilities/", "V2 Final Phase Verification",
        "V3 is ChatGPT Only", "No new Capability", "no Model Runtime", "no Hardware Runtime", "no Action execution",
        "no automatic Learning", "no schema redesign", "no historical asset deletion", "no hardcoded pass"
    ],
    "engineering_health_report_v1.md": [
        "Engineering Health Report v1", "53 `active` directories", "46 `verification_only` historical/validation directories",
        "1 `missing_asset_candidate` directory", "cognitive_flow", "confirmed syntax issue", "BOUNDARY_FLAGS",
        "RECOMMENDED_NEXT_PHASE", "No provider invocation", "no model call", "no hardware call", "No asset is deleted",
        "compileall", "does not approve Runtime integration", "V3 audit"
    ],
    "engineering_health_go_no_go_v1.md": [
        "Engineering Health Remediation Go / No-Go v1", "compileall", "active", "historical", "verification_only",
        "missing_asset_candidate", "Canonical IDs", "aliases", "Duplicate groups", "Large files", "V0", "V1",
        "V2 Final Phase Verification", "V3 Final Audit", "WAITING_FOR_USER_TERMINAL_VERIFICATION", "No new Capability",
        "no Model", "no Hardware", "no Provider invocation", "no Runtime implementation", "no Action execution",
        "no OCR/SLAM/VLM call", "no automatic Learning", "no historical deletion", "no hardcoded pass"
    ]
}

JSON_REQ = {
    "python_compile_issue_registry_v1.json": [
        "Python Compile Issue Registry v1", "capabilities/", "python3 -m compileall capabilities/",
        "mobile_sam_ocr_controlled_execution_types_v1.py", "STATIC_IMPORT_OR_SYNTAX_FAILURE", "RECOMMENDED_NEXT_PHASE",
        "BOUNDARY_FLAGS", "remediated", "protocol_changed", "capability_behavior_changed", "model_or_hardware_called",
        "fix_failed_items_only", "preserve_interface_meaning", "no_protocol_redesign", "no_new_capability",
        "no_model_runtime", "no_hardware_runtime", "no_action_execution", "unknowns_are_preserved", "provenance_is_preserved"
    ],
    "architecture_asset_inventory_v1.json": [
        "Architecture Asset Inventory v1", "docs/architecture/", "policy plus repository snapshot", "active", "historical",
        "verification_only", "missing_asset_candidate", "md", "json", "verifier", "cognitive_directory_count", "100",
        "active_count", "53", "verification_only_count", "46", "missing_asset_candidate_count", "1", "cognitive_flow",
        "every_cognitive_directory_receives_status", "historical_assets_are_not_deleted", "missing_assets_are_registered_only",
        "inventory_is_not_runtime_input", "rescan_required_after_asset_change", "unknowns_are_preserved", "provenance_is_preserved"
    ],
    "architecture_asset_status_matrix_v1.json": [
        "Architecture Asset Status Matrix v1", "Category A", "Category B", "Category C", "Category D", "active", "historical",
        "verification_only", "missing_asset_candidate", "architecture.md", "contract/schema json", "verifier", "status metadata",
        "all_architecture_assets_have_status", "historical_assets_are_retained", "missing_assets_are_not_auto_created",
        "status_change_requires_review", "no_runtime_behavior", "unknowns_are_preserved"
    ],
    "canonical_schema_registry_v1.json": [
        "Canonical Schema Registry v1", "canonical_schema_and_contract_registry", "active", "alias", "deprecated", "historical",
        "canonical_id", "aliases", "status", "owner", "migration_rule", "cognitive_field_brain_interface_v1",
        "cognitive_field_a_route_interface_v1", "capability_attention_interface_v1", "decision_revision_contract_v1",
        "attention_capability_feedback_contract_v1", "relationship_context_schema_v1", "capability_admission_contract_v1",
        "canonical_reference_required_for_new_code", "aliases_remain_compatible", "direct_delete_forbidden",
        "overwrite_forbidden", "migration_requires_review", "unknowns_are_preserved", "provenance_is_preserved"
    ],
    "duplicate_asset_resolution_map_v1.json": [
        "Duplicate Asset Resolution Map v1", "duplicate_groups", "duplicate_group", "canonical_asset", "legacy_assets", "decision",
        "merge", "alias", "historical", "keep_parallel", "no_delete", "no_overwrite", "canonical_registry_binding_required",
        "semantic_review_required_before_merge", "unknowns_are_preserved", "provenance_is_preserved"
    ],
    "large_file_governance_registry_v1.json": [
        "Large File Governance Registry v1", "normal_max_lines", "warning_over_lines", "blocker_candidate_over_lines", "file",
        "line_count", "category", "action", "priority", "Active Code", "Frozen Compatibility", "Registry / Generated",
        "voice_final_text_dispatcher.py", "5161", "no_direct_split_in_this_phase", "blocker_candidate_requires_owner",
        "generated_files_need_special_handling", "frozen_compatibility_is_not_deleted", "unknowns_are_preserved", "provenance_is_preserved"
    ],
    "engineering_health_validation_strategy_v1.json": [
        "Engineering Health Validation Strategy v1", "python_compile", "json_parse", "asset_inventory", "canonical_registry",
        "duplicate_map", "large_file_registry", "boundary_scan", "final_phase_verification", "final_audit",
        "python3 -m compileall capabilities/", "Agent V0", "User Terminal V2", "ChatGPT V3", "compile_failure_blocks",
        "missing_asset_is_registered_not_auto_created", "duplicate_without_decision_blocks", "large_file_without_action_blocks",
        "v0_does_not_grant_go", "unknowns_are_preserved"
    ]
}


def _architecture_status(path: Path) -> str:
    files = [p for p in path.iterdir() if p.is_file()]
    has_md = any(p.suffix == ".md" for p in files)
    has_json = any(p.suffix == ".json" for p in files)
    has_verifier = (path / f"verify_{path.name}.py").is_file()
    if has_md and has_json and has_verifier:
        return "active"
    if has_verifier and not (has_md or has_json):
        return "verification_only"
    return "missing_asset_candidate"


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

    # Confirm the bounded remediation without importing the capability module.
    checks += 3
    repaired = REPO_ROOT / "capabilities/midplatform/model_test_lens/multi_model_interaction/mobile_sam_ocr_controlled_execution_types_v1.py"
    repaired_text = repaired.read_text()
    if "BOUNDARY_FLAGS = {" not in repaired_text:
        failures.append("syntax remediation missing BOUNDARY_FLAGS mapping")
    if repaired_text.count("RECOMMENDED_NEXT_PHASE =") != 1:
        failures.append("RECOMMENDED_NEXT_PHASE is not defined exactly once")
    if "RECOMMENDED_NEXT_PHASE = (\n    \"Phase-" not in repaired_text:
        failures.append("RECOMMENDED_NEXT_PHASE interface value is not preserved")

    # Dynamic architecture inventory consistency.
    dirs = [p for p in ARCH_ROOT.iterdir() if p.is_dir() and p.name.startswith("cognitive_")]
    checks += 4
    statuses = [_architecture_status(p) for p in dirs]
    if len(dirs) != 100:
        failures.append(f"architecture cognitive directory count drifted: {len(dirs)}")
    if statuses.count("active") != 53:
        failures.append(f"active directory count drifted: {statuses.count('active')}")
    if statuses.count("verification_only") != 46:
        failures.append(f"verification_only directory count drifted: {statuses.count('verification_only')}")
    if statuses.count("missing_asset_candidate") != 1:
        failures.append(f"missing_asset_candidate count drifted: {statuses.count('missing_asset_candidate')}")

    # Compileall is a V2 user-terminal health gate; keep output quiet and report only status.
    checks += 1
    if not compileall.compile_dir(str(REPO_ROOT / "capabilities"), quiet=1, maxlevels=99):
        failures.append("python3 -m compileall capabilities/ failed")

    # Phase assets must not introduce active runtime or provider execution.
    checks += 1
    phase_text = "\n".join(p.read_text(errors="ignore") for p in BASE.iterdir() if p.is_file())
    runtime_hits = re.findall(r"(?m)^\s*(?:import|from)\s+(subprocess|socket|requests|cv2|torch|onnx)\b", phase_text)
    # The phase verifier imports only compileall/json/re/Path; actual runtime imports are forbidden.
    if runtime_hits:
        failures.append(f"forbidden runtime implementation terms: {runtime_hits}")

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
    print("READINESS: ENGINEERING_HEALTH_REMEDIATION_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
