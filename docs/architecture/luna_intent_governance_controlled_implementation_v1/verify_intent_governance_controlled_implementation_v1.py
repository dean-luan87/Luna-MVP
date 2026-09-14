#!/usr/bin/env python3
"""Read-only verifier for Intent Governance controlled implementation v1."""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path
from typing import Any, Dict


BASE = Path(__file__).resolve().parent
STATUS = "CONTROLLED_IMPLEMENTATION_CANDIDATE"
READY = "LUNA_INTENT_GOVERNANCE_CONTROLLED_IMPLEMENTATION_READY"
REMEDIATION = "LUNA_INTENT_GOVERNANCE_CONTROLLED_IMPLEMENTATION_REMEDIATION_REQUIRED"

CODE_FILES = {
    "__init__.py",
    "intent_error_types_v1.py",
    "intent_core_types_v1.py",
    "intent_io_types_v1.py",
    "intent_lifecycle_types_v1.py",
    "intent_interaction_types_v1.py",
    "intent_carryover_types_v1.py",
    "intent_resource_types_v1.py",
    "intent_trace_types_v1.py",
    "intent_handoff_types_v1.py",
    "intent_registry_v1.py",
    "intent_governance_protocol_v1.py",
    "intent_ownership_guard_v1.py",
    "intent_static_validators_v1.py",
    "intent_governance_fixture_v1.py",
    "intent_governance_skeleton_v1.py",
    "run_intent_governance_controlled_implementation_v1.py",
}

DOC_FILES = {
    "intent_governance_controlled_implementation_overview_v1.md",
    "intent_governance_controlled_execution_contract_v1.json",
    "intent_governance_negative_guards_v1.json",
    "intent_governance_planning_to_code_mapping_v1.json",
    "intent_governance_implementation_summary_v1.md",
    "intent_governance_controlled_change_manifest_v1.json",
    "phase_contract.json",
    "verify_intent_governance_controlled_implementation_v1.py",
}

JSON_FILES = {
    "intent_governance_controlled_execution_contract_v1.json",
    "intent_governance_negative_guards_v1.json",
    "intent_governance_planning_to_code_mapping_v1.json",
    "intent_governance_controlled_change_manifest_v1.json",
    "phase_contract.json",
}


def find_repo_root() -> Path:
    current = Path.cwd().resolve()
    for candidate in (current,) + tuple(current.parents):
        if (candidate / "capabilities/midplatform/core/intent_governance").is_dir():
            return candidate
    raise RuntimeError("repository_root_with_intent_governance_not_found")


def load_json(path: Path) -> Dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"{path.name} must contain a JSON object")
    return value


def emit(checks: list[str], failures: list[str]) -> None:
    print("CHECKS")
    for item in checks:
        print(item)

    print("FAILED_CHECKS")
    for item in failures:
        print(item)

    print("PASSED_CHECK_COUNT")
    print(max(0, len(checks) - len(failures)))

    print("FAILED_CHECK_COUNT")
    print(len(failures))

    print("FINAL_DECISION")
    print(READY if not failures else "BLOCKED_BY_VERIFIER_FAILURE")

    print("READINESS")
    print(READY if not failures else REMEDIATION)

    print("NEXT")
    print(
        "RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT"
        if not failures
        else "REMEDIATE_REPORTED_FAILURES_ONLY"
    )


def main() -> int:
    checks: list[str] = []
    failures: list[str] = []

    def check(condition: bool, check_id: str) -> None:
        checks.append(check_id)
        if not condition:
            failures.append(check_id)

    try:
        repo_root = find_repo_root()
        check(True, "repo_root_resolved")
    except RuntimeError:
        repo_root = Path.cwd().resolve()
        check(False, "repo_root_resolved")

    code_dir = repo_root / "capabilities/midplatform/core/intent_governance"
    actual_code_files = {path.name for path in code_dir.iterdir() if path.is_file()}
    actual_doc_files = {path.name for path in BASE.iterdir() if path.is_file()}
    check(actual_code_files == CODE_FILES, "exact_code_file_set")
    check(actual_doc_files == DOC_FILES, "exact_doc_file_set")

    docs: Dict[str, Dict[str, Any]] = {}
    for name in sorted(JSON_FILES):
        path = BASE / name
        try:
            docs[name] = load_json(path)
            check(True, f"json_parse:{name}")
        except (OSError, TypeError, json.JSONDecodeError):
            docs[name] = {}
            check(False, f"json_parse:{name}")

    contract = docs.get("intent_governance_controlled_execution_contract_v1.json", {})
    check(contract.get("candidate_only") is True, "contract_candidate_only")
    check(contract.get("synthetic_fixture_only") is True, "contract_synthetic_only")
    check(contract.get("runtime_execution") is False, "contract_no_runtime")
    check(
        contract.get("source_mutation_allowed") is False, "contract_no_source_mutation"
    )

    guards = docs.get("intent_governance_negative_guards_v1.json", {})
    check(guards.get("status") == STATUS, "guards_status")
    negative_guards = guards.get("negative_guards", [])
    check(
        "do not create parallel Intent owner" in negative_guards,
        "guards_parallel_owner",
    )

    mapping = docs.get("intent_governance_planning_to_code_mapping_v1.json", {})
    mapped = {Path(item).name for item in mapping.get("all_code_assets", [])}
    check(mapped == CODE_FILES, "mapping_code_completeness")
    check(
        mapping.get("planning_assets_modified") is False,
        "mapping_no_planning_modification",
    )
    check(
        mapping.get("parallel_implementation_created") is False, "mapping_no_parallel"
    )

    manifest = docs.get("intent_governance_controlled_change_manifest_v1.json", {})
    created_code = {Path(item).name for item in manifest.get("created_code_files", [])}
    created_doc = {
        Path(item).name for item in manifest.get("created_documentation_files", [])
    }
    check(created_code == CODE_FILES, "manifest_code_set")
    check(created_doc == DOC_FILES, "manifest_doc_set")
    check(manifest.get("modified_existing_files") == [], "manifest_no_modify")
    check(manifest.get("runtime_executed") is False, "manifest_runtime_false")
    check(manifest.get("runner_executed_by_agent") is False, "manifest_runner_false")
    check(
        manifest.get("verifier_executed_by_agent") is False, "manifest_verifier_false"
    )

    phase = docs.get("phase_contract.json", {})
    check(
        phase.get("phase")
        == "Phase-Luna-Intent-Governance-Controlled-Implementation-v1-001",
        "phase_id",
    )
    check(phase.get("status") == STATUS, "phase_status")
    check(
        phase.get("agent_stop_point") == "WAITING_FOR_USER_TERMINAL_VERIFICATION",
        "phase_waiting",
    )
    check(phase.get("runtime_executed") is False, "phase_runtime_false")

    overview = (
        BASE / "intent_governance_controlled_implementation_overview_v1.md"
    ).read_text(encoding="utf-8")
    for token, token_id in [
        ("candidate_only = true", "overview_candidate_only"),
        ("synthetic_fixture_only = true", "overview_synthetic_only"),
        ("runtime_executed = false", "overview_runtime_false"),
        ("no Decision/Action/Task/Causal truth output", "overview_no_decision_action"),
    ]:
        check(token in overview, token_id)

    summary = (BASE / "intent_governance_implementation_summary_v1.md").read_text(
        encoding="utf-8"
    )
    check("12-scenario synthetic fixture suite" in summary, "summary_fixture_coverage")

    for name in sorted(CODE_FILES):
        path = code_dir / name
        try:
            source = path.read_text(encoding="utf-8")
            ast.parse(source)
            check(True, f"ast_parse:{name}")
        except (SyntaxError, OSError):
            check(False, f"ast_parse:{name}")

    emit(checks, failures)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
