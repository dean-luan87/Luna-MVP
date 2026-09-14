"""V0 static verifier for read-only governance asset discovery.

Audit / Planning Only: validates discovery manifests and mapping candidates.
It does not modify, import, execute, move, rename, delete, or consolidate
existing capabilities, architecture assets, tools, providers, models, or
hardware.
"""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path


BASE = Path(__file__).resolve().parent
JSON_ASSETS = (
    "architecture_asset_inventory_v1.json",
    "model_management_asset_inventory_v1.json",
    "capability_governance_asset_inventory_v1.json",
    "admission_asset_inventory_v1.json",
    "provider_asset_inventory_v1.json",
    "calibration_asset_inventory_v1.json",
    "ownership_mapping_candidate_v1.json",
    "duplicate_asset_candidate_registry_v1.json",
    "core_architecture_mapping_candidate_v1.json",
)
MD_ASSETS = (
    "luna_governance_asset_discovery_report_v1.md",
    "governance_discovery_whitebox_v1.md",
    "governance_discovery_go_no_go_v1.md",
)
SCAN_ROOTS = ("capabilities/", "docs/architecture/", "tools/")


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

    inventory = data.get("architecture_asset_inventory_v1.json", {})
    model = data.get("model_management_asset_inventory_v1.json", {})
    capability = data.get("capability_governance_asset_inventory_v1.json", {})
    admission = data.get("admission_asset_inventory_v1.json", {})
    provider = data.get("provider_asset_inventory_v1.json", {})
    calibration = data.get("calibration_asset_inventory_v1.json", {})
    ownership = data.get("ownership_mapping_candidate_v1.json", {})
    duplicate = data.get("duplicate_asset_candidate_registry_v1.json", {})
    mapping = data.get("core_architecture_mapping_candidate_v1.json", {})

    check(inventory.get("scan_scope") == list(SCAN_ROOTS), "scan_scope")
    policy = inventory.get("scan_policy", {})
    check(policy.get("read_only") is True, "scan_read_only")
    check(set(policy.get("exclude", [])) >= {"__pycache__", "*.pyc"}, "scan_exclusions")
    snapshot = inventory.get("scan_snapshot", {})
    check(snapshot.get("total_files") == snapshot.get("capabilities_files", 0) + snapshot.get("architecture_files", 0) + snapshot.get("tools_files", 0), "scan_total_integrity")
    check(all(snapshot.get(key, 0) > 0 for key in ("capabilities_files", "architecture_files", "tools_files")), "scan_root_counts")
    entries = inventory.get("entries", [])
    check(len(entries) >= 10, "inventory_entries")
    check(all({"asset_id", "path", "type", "layer_candidate", "current_owner", "description", "status"}.issubset(entry) for entry in entries), "inventory_entry_schema")
    check({"Active Asset", "Historical Asset", "Verification Only", "Duplicate Candidate", "Missing Ownership"}.issubset({entry.get("status") for entry in entries}), "inventory_status_categories")
    check(all(entry.get("path") for entry in entries), "inventory_paths")

    model_summary = model.get("summary", {})
    check(model.get("status") == "present_distributed", "model_status")
    check(model_summary.get("model_manager_files_excluding_cache", 0) > 0, "model_manager_present")
    for key in ("model_registry_assets", "model_manager_baseline_present", "model_lifecycle_present", "model_admission_present", "model_health_present", "benchmark_record_present"):
        check(bool(model_summary.get(key)), f"model_feature:{key}")
    check(any(entry.get("path") == "capabilities/midplatform/model_manager/" for entry in model.get("entries", [])), "model_manager_inventory_entry")
    check(any(entry.get("status") == "Duplicate Candidate" for entry in model.get("entries", [])), "model_duplicate_candidate")

    cap_summary = capability.get("summary", {})
    check(capability.get("status") == "present_distributed", "capability_status")
    for key in ("canonical_registry_present", "lifecycle_present", "manifest_present", "dependency_map_present", "calibration_standard_present"):
        check(cap_summary.get(key) is True, f"capability_feature:{key}")
    check(any(entry.get("status") == "Duplicate Candidate" for entry in capability.get("entries", [])), "capability_duplicate_candidate")

    check(set(admission.get("admission_classes", [])) == {"Model Admission", "Capability Admission", "Provider Admission", "Runtime Admission"}, "admission_classes")
    check(len(admission.get("entries", [])) >= 5, "admission_entries")
    check(all(entry.get("class") in admission.get("admission_classes", []) for entry in admission.get("entries", [])), "admission_mapping_classes")
    check(any(entry.get("status") == "Verification Only" for entry in admission.get("entries", [])), "admission_verification_only")

    provider_findings = provider.get("boundary_findings", {})
    check(provider.get("status") == "present_distributed", "provider_status")
    check(len(provider.get("entries", [])) >= 5, "provider_entries")
    check(provider_findings.get("provider_to_brain_authority") is False, "provider_no_brain_authority")
    check(provider_findings.get("provider_to_reality_authority") is False, "provider_no_reality_authority")
    check(provider_findings.get("provider_to_memory_authority") is False, "provider_no_memory_authority")

    check(calibration.get("status") == "present_distributed", "calibration_status")
    check(len(calibration.get("entries", [])) >= 5, "calibration_entries")
    check(any(entry.get("type") == "benchmark_schema" for entry in calibration.get("entries", [])), "calibration_benchmark")
    check(any(entry.get("type") == "module_baseline_family" for entry in calibration.get("entries", [])), "calibration_baseline")
    check(any(entry.get("type") == "provider_benchmark_registry" for entry in calibration.get("entries", [])), "calibration_provider_benchmark")

    mapping_entries = ownership.get("entries", [])
    check(ownership.get("mapping_status") == "candidate_only", "ownership_candidate_only")
    check(len(mapping_entries) >= 8, "ownership_entries")
    check(all({"asset", "current_location", "target_owner", "migration_needed", "reason"}.issubset(entry) for entry in mapping_entries), "ownership_schema")
    check(ownership.get("rules", {}).get("no_move") is True, "ownership_no_move")
    check(ownership.get("rules", {}).get("no_delete") is True, "ownership_no_delete")
    check(ownership.get("rules", {}).get("requires_separate_migration_phase") is True, "ownership_migration_boundary")

    duplicate_groups = duplicate.get("groups", [])
    check(len(duplicate_groups) >= 4, "duplicate_groups")
    check(all(group.get("duplicate_group") and group.get("canonical_candidate") and group.get("others") and group.get("decision") for group in duplicate_groups), "duplicate_schema")
    check(duplicate.get("rules", {}).get("no_delete") is True, "duplicate_no_delete")
    check(duplicate.get("rules", {}).get("no_merge_in_discovery") is True, "duplicate_no_merge")
    check(duplicate.get("rules", {}).get("canonical_candidate_not_final") is True, "duplicate_candidate_not_final")

    target_tree = set(mapping.get("target_tree", []))
    check({"L0 Constitution", "L1 Cognitive OS Governance", "L2 Cognitive Core", "L4 Capability Governance", "L4 Model Management", "L4 Admission", "L4 Calibration", "L4 Provider Adapter", "L4 Capability Runtime", "L5 Hardware / External Implementation"}.issubset(target_tree), "mapping_target_tree")
    mapping_rows = mapping.get("mappings", [])
    check(len(mapping_rows) >= 8, "mapping_rows")
    check(all({"asset", "current_location", "target_owner", "migration_needed", "reason"}.issubset(entry) for entry in mapping_rows), "mapping_schema")
    check(mapping.get("rules", {}).get("candidate_only") is True, "mapping_candidate_only")
    check(mapping.get("rules", {}).get("no_directory_change") is True, "mapping_no_directory_change")
    check(mapping.get("rules", {}).get("no_asset_merge") is True, "mapping_no_merge")

    verifier_text = Path(__file__).read_text(encoding="utf-8")
    verifier_ast = ast.parse(verifier_text, filename=str(Path(__file__)))
    imports: set[str] = set()
    for node in ast.walk(verifier_ast):
        if isinstance(node, ast.Import):
            imports.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split(".")[0])
    check(not imports.intersection({"subprocess", "socket", "requests", "cv2", "torch"}), "discovery_no_runtime_import")
    check(not imports.intersection({"shutil", "os"}), "discovery_no_mutation_import")
    compile(verifier_text, str(Path(__file__)), "exec")
    check(True, "discovery_verifier_compile")

    passed = checks - len(failures)
    print(f"CHECKS: {checks}")
    print(f"FAILED_CHECKS: {failures}")
    print(f"PASSED_CHECK_COUNT: {passed}")
    print(f"FAILED_CHECK_COUNT: {len(failures)}")
    print(f"BLOCKER_COUNT: {len(failures)}")
    if failures:
        print("FINAL_DECISION: BLOCKED_BY_VERIFIER_FAILURE")
        print("READINESS: LUNA_GOVERNANCE_ASSET_DISCOVERY_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_GOVERNANCE_ASSET_DISCOVERY_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    sys.exit(main())
