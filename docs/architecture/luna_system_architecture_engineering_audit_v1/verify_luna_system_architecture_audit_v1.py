"""V0/V1 static verifier for the Luna system architecture audit.

This verifier is deliberately read-only with respect to Luna runtime code.  It
validates audit assets, source syntax, and the declared boundary model; it does
not import, execute, or activate capability/runtime modules.
"""

from __future__ import annotations

import json
import ast
import sys
from pathlib import Path


BASE = Path(__file__).resolve().parent
REPO_ROOT = BASE.parents[2]
ARCH_ROOT = REPO_ROOT / "docs" / "architecture"

REQUIRED_JSON = (
    "luna_module_inventory_v1.json",
    "luna_dependency_graph_v1.json",
    "luna_information_flow_audit_v1.json",
    "luna_authority_matrix_v1.json",
    "luna_state_ownership_audit_v1.json",
    "luna_code_health_report_v1.json",
    "luna_orphan_module_registry_v1.json",
    "luna_duplicate_asset_registry_v1.json",
    "luna_runtime_readiness_check_v1.json",
    "luna_missing_capability_analysis_v1.json",
)
REQUIRED_MD = (
    "luna_system_architecture_audit_report_v1.md",
    "luna_architecture_audit_go_no_go_v1.md",
)


def _source_compile(root: Path) -> tuple[bool, list[str]]:
    """Compile source in memory, avoiding pycache writes and imports."""

    failures: list[str] = []
    for path in root.rglob("*.py"):
        try:
            compile(path.read_text(encoding="utf-8", errors="replace"), str(path), "exec")
        except (OSError, SyntaxError, ValueError) as exc:
            failures.append(f"{path}: {exc}")
    return not failures, failures


def _check(condition: bool, name: str, failures: list[str]) -> None:
    if not condition:
        failures.append(name)


def main() -> int:
    failures: list[str] = []
    checks = 0

    def check(condition: bool, name: str) -> None:
        nonlocal checks
        checks += 1
        _check(condition, name, failures)

    for name in REQUIRED_JSON:
        path = BASE / name
        check(path.is_file(), f"missing_json:{name}")
        if path.is_file():
            try:
                json.loads(path.read_text(encoding="utf-8"))
                check(True, f"json_parse:{name}")
            except (OSError, json.JSONDecodeError):
                check(False, f"json_parse:{name}")

    for name in REQUIRED_MD:
        path = BASE / name
        check(path.is_file(), f"missing_md:{name}")
        if path.is_file():
            text = path.read_text(encoding="utf-8", errors="replace")
            check(len(text.strip()) > 0, f"nonempty_md:{name}")

    inventory = json.loads((BASE / "luna_module_inventory_v1.json").read_text())
    graph = json.loads((BASE / "luna_dependency_graph_v1.json").read_text())
    authority = json.loads((BASE / "luna_authority_matrix_v1.json").read_text())
    code_health = json.loads((BASE / "luna_code_health_report_v1.json").read_text())
    runtime = json.loads((BASE / "luna_runtime_readiness_check_v1.json").read_text())
    duplicates = json.loads((BASE / "luna_duplicate_asset_registry_v1.json").read_text())
    missing = json.loads((BASE / "luna_missing_capability_analysis_v1.json").read_text())
    information = json.loads((BASE / "luna_information_flow_audit_v1.json").read_text())

    expected_statuses = {"Active", "Skeleton", "Deprecated", "Duplicate", "Orphan", "Planning Only"}
    check(set(inventory.get("status_values", [])) == expected_statuses, "inventory_status_values")
    check(set(inventory.get("inventory_scope", [])) == {"capabilities/", "docs/architecture/", "tools/"}, "inventory_scope")
    check(len(inventory.get("module_domains", [])) >= 5, "inventory_module_domains")

    layer_names = [item.get("name") for item in graph.get("layers", [])]
    check(layer_names == [
        "Constitution",
        "Governance Plane",
        "Cognitive Core",
        "Cognitive Runtime",
        "Capability Runtime",
        "Hardware / Model / Provider",
    ], "canonical_layer_order")
    required_edges = set(graph.get("required_edges", []))
    forbidden_edges = set(graph.get("forbidden_edges", []))
    check(len(required_edges) >= 8, "dependency_required_edges")
    check({"Capability → Brain", "Model → Goal", "Provider → Reality"}.issubset(forbidden_edges), "dependency_forbidden_edges")
    check(graph.get("rules", {}).get("no_reverse_layer_dependency") is True, "dependency_no_reverse_rule")

    authority_modules = {row.get("module") for row in authority.get("rows", [])}
    check({"Brain", "Attention", "Memory", "Learning", "Value", "Reflex", "Capability", "Action Boundary"}.issubset(authority_modules), "authority_core_modules")
    check(authority.get("rules", {}).get("no_circular_authority") is True, "authority_no_cycle_rule")
    check(authority.get("rules", {}).get("reader_does_not_gain_write") is True, "authority_reader_writer_rule")

    check(code_health.get("line_thresholds", {}).get("blocker_candidate_over") == 1200, "code_health_threshold")
    check(code_health.get("large_file_count_over_1200", 0) == 20, "code_health_large_file_inventory")
    check(any(item.get("file", "").endswith("voice_final_text_dispatcher.py") for item in code_health.get("priority_files", [])), "code_health_priority_file")

    runtime_dimensions = {item.get("dimension") for item in runtime.get("readiness_dimensions", [])}
    check({"State", "Event", "Trace", "Failure", "Retry", "Degrade", "Recovery", "Scheduler Policy", "State Persistence"}.issubset(runtime_dimensions), "runtime_dimensions")
    check(runtime.get("runtime_active") is False, "runtime_not_active")
    boundary = runtime.get("boundary", {})
    check(all(boundary.get(key) is True for key in ("no_runtime_execution", "no_model_calls", "no_hardware_calls", "no_action_execution")), "runtime_boundary")

    duplicate_entries = duplicates.get("duplicate_groups", duplicates.get("groups", []))
    check(len(duplicate_entries) == 7, "duplicate_group_count")
    check(all(item.get("canonical_owner") for item in duplicate_entries), "duplicate_canonical_owners")
    check(all(item.get("resolution") for item in duplicate_entries), "duplicate_resolution_values")

    missing_caps = {item.get("capability"): item.get("status") for item in missing.get("capability_checks", [])}
    check(missing_caps.get("Capability Discovery") == "partial", "missing_capability_discovery_is_explicit")
    check(missing_caps.get("Social / Emotion") == "boundary_only", "social_emotion_boundary_only")
    check(missing.get("rules", {}).get("no_auto_create") is True, "missing_capability_no_auto_create")

    check(len(information.get("canonical_flow", [])) >= 10, "information_canonical_flow")
    check(len(information.get("forbidden_flows", [])) >= 4, "information_forbidden_flows")

    # Dynamic asset accounting is intentionally narrow: it audits phase
    # directories without attempting to classify every historical artifact.
    phase_dirs = [path for path in ARCH_ROOT.iterdir() if path.is_dir() and path.name.startswith("cognitive_")]
    active = verification_only = missing_candidate = 0
    for path in phase_dirs:
        has_md = any(path.glob("*.md"))
        has_json = any(path.glob("*.json"))
        has_verifier = any(path.glob("verify_*.py"))
        if has_md or has_json:
            active += 1
        elif has_verifier:
            verification_only += 1
        else:
            missing_candidate += 1
    observed = inventory.get("phase_directory_status", {})
    check(observed.get("active") == active, "phase_active_count")
    check(observed.get("verification_only") == verification_only, "phase_verification_only_count")
    check(observed.get("missing_asset_candidate") == missing_candidate, "phase_missing_candidate_count")

    capabilities_ok, capability_failures = _source_compile(REPO_ROOT / "capabilities")
    tools_ok, tools_failures = _source_compile(REPO_ROOT / "tools")
    check(capabilities_ok, "capabilities_source_compile")
    check(tools_ok, "tools_source_compile")
    check(not capability_failures and not tools_failures, "source_compile_failure_details")

    # The audit phase itself must remain a static, non-activating asset.
    verifier_text = Path(__file__).read_text(encoding="utf-8")
    verifier_tree = ast.parse(verifier_text, filename=str(Path(__file__)))
    imported_modules = set()
    for node in ast.walk(verifier_tree):
        if isinstance(node, ast.Import):
            imported_modules.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_modules.add(node.module.split(".")[0])
    check(not imported_modules.intersection({"subprocess", "socket"}), "verifier_no_runtime_activation")
    check("no_runtime_execution" in json.dumps(runtime), "runtime_execution_guard_present")

    passed = checks - len(failures)
    remediation_signals = []
    if any(item.get("status") == "Orphan" and item.get("priority") in {"P0", "P1"} for item in inventory.get("known_findings", [])):
        remediation_signals.append("registered_orphan_candidate")
    if any(item.get("status") == "partial" and item.get("priority") == "P1" for item in runtime.get("readiness_dimensions", [])):
        remediation_signals.append("runtime_readiness_partial_before_runtime")
    if any(item.get("status") == "partial" and item.get("priority") == "P1" for item in missing.get("capability_checks", [])):
        remediation_signals.append("capability_gap_before_runtime")
    if code_health.get("large_file_count_over_1200", 0) > 0:
        remediation_signals.append("large_file_governance_risk")
    print(f"CHECKS: {checks}")
    print(f"FAILED_CHECKS: {failures}")
    print(f"PASSED_CHECK_COUNT: {passed}")
    print(f"FAILED_CHECK_COUNT: {len(failures)}")
    print(f"BLOCKER_COUNT: {len(failures)}")
    if failures:
        print("FINAL_DECISION: BLOCKED_BY_VERIFIER_FAILURE")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    if remediation_signals:
        print(f"REMEDIATION_SIGNALS: {remediation_signals}")
        print("READINESS: LUNA_SYSTEM_ARCHITECTURE_REMEDIATION_REQUIRED")
    else:
        print("READINESS: LUNA_SYSTEM_ARCHITECTURE_HEALTHY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    sys.exit(main())
