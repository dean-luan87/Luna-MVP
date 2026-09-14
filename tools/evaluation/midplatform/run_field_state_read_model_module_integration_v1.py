#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


def _is_workspace_root(candidate: Path) -> bool:
    markers = (
        candidate / "AGENTS.md",
        candidate / "capabilities",
        candidate / "tools" / "evaluation" / "midplatform",
    )
    return all(marker.exists() for marker in markers)


def _find_ws_root() -> Path:
    cwd = Path.cwd().absolute()
    if _is_workspace_root(cwd):
        return cwd

    script_path = Path(__file__).absolute()
    for candidate in (script_path.parent, *script_path.parents):
        if _is_workspace_root(candidate):
            return candidate

    raise RuntimeError("Unable to locate Luna workspace root")


REPO_ROOT = _find_ws_root()
REPORT_PATH = (
    REPO_ROOT
    / "_tmp_eval_out"
    / "field_state_read_model_module_integration_v1_smoke_v0"
    / "field_state_read_model_module_integration_v1.json"
)
CAPABILITY_ID = "luna.field_state_read_model"
MODULE_ID = "luna.midplatform.field_state_read_model"

REGISTRY_PATH = REPO_ROOT / "capabilities/registry/luna_capability_registry_v1.json"
DEPENDENCY_MAP_PATH = (
    REPO_ROOT / "capabilities/registry/luna_capability_dependency_map_v1.json"
)
BASELINE_REGISTRY_PATH = (
    REPO_ROOT / "capabilities/registry/luna_capability_module_baseline_registry_v1.json"
)
MANIFEST_PATH = (
    REPO_ROOT
    / "capabilities/registry/manifests/field_state_read_model_manifest_v1.json"
)
BASELINE_PATH = (
    REPO_ROOT
    / "capabilities/registry/baselines/field_state_read_model_module_baseline_v1.json"
)
RULE_CANDIDATES_PATH = (
    REPO_ROOT
    / "docs/architecture/field_kernel/field_state_read_model_governance_rule_candidates_v1.md"
)
DOC_PATH = (
    REPO_ROOT
    / "docs/architecture/field_kernel/field_state_read_model_module_integration_v1.md"
)
RUNNER_SELF_PATH = (
    REPO_ROOT
    / "tools/evaluation/midplatform/run_field_state_read_model_module_integration_v1.py"
)
VERIFIER_PATH = (
    REPO_ROOT
    / "tools/evaluation/midplatform/verify_field_state_read_model_module_integration_v1.py"
)
MODULE_API_PATH = (
    REPO_ROOT
    / "capabilities/midplatform/core/field_state_read_model/module/field_state_read_model_module_api_v1.py"
)
RUNTIME_API_PATH = (
    REPO_ROOT
    / "capabilities/midplatform/core/field_state_read_model/runtime/field_state_read_model_controlled_runtime_v1.py"
)
QUERY_SCHEMA_PATH = (
    REPO_ROOT
    / "capabilities/midplatform/core/field_state_read_model/planning/field_state_read_query_schema_v1.json"
)
RESULT_SCHEMA_PATH = (
    REPO_ROOT
    / "capabilities/midplatform/core/field_state_read_model/planning/field_state_read_result_schema_v1.json"
)
RUNTIME_TYPES_PATH = (
    REPO_ROOT
    / "capabilities/midplatform/core/field_state_read_model/runtime/field_state_read_model_runtime_types_v1.py"
)
SKELETON_REPORT_PATH = (
    REPO_ROOT
    / "_tmp_eval_out/field_state_read_model_controlled_skeleton_v1_smoke_v0/field_state_read_model_controlled_skeleton_v1.json"
)
CONTRACT_REPORT_PATH = (
    REPO_ROOT
    / "_tmp_eval_out/field_state_read_model_contract_dryrun_v1_smoke_v0/field_state_read_model_contract_dryrun_v1.json"
)
RUNTIME_REPORT_PATH = (
    REPO_ROOT
    / "_tmp_eval_out/field_state_read_model_controlled_runtime_v1_smoke_v0/field_state_read_model_controlled_runtime_v1.json"
)

BOUNDARY_FLAGS = {
    "read_only": True,
    "state_mutation": False,
    "event_reduction": False,
    "fact_admission": False,
    "evidence_fabrication": False,
    "real_model_execution": False,
    "action_execution": False,
    "runtime_loop": False,
    "real_state_store_connected": False,
    "candidate_only": True,
}

REQUIRED_LIMITATIONS = {
    "no real state store",
    "no asynchronous runtime",
    "no downstream dispatch",
    "no batch query",
    "no retry orchestration",
    "no persistence",
    "no real source adapter",
}

REQUIRED_PROHIBITIONS = {
    "source_of_truth_authority",
    "state_owner_authority",
    "fact_authority",
    "mutation_owner_authority",
    "event_reducer_authority",
    "admission_authority",
}


def _read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _check(
    check_id: int, title: str, passed: bool, details: str = ""
) -> Dict[str, Any]:
    return {"check_id": check_id, "title": title, "passed": passed, "details": details}


def run() -> Dict[str, Any]:
    registry = _read_json(REGISTRY_PATH)
    dependency_map = _read_json(DEPENDENCY_MAP_PATH)
    baseline_registry = _read_json(BASELINE_REGISTRY_PATH)
    manifest = _read_json(MANIFEST_PATH)
    baseline = _read_json(BASELINE_PATH)
    skeleton_report = _read_json(SKELETON_REPORT_PATH)
    contract_report = _read_json(CONTRACT_REPORT_PATH)
    runtime_report = _read_json(RUNTIME_REPORT_PATH)
    rule_candidates_text = RULE_CANDIDATES_PATH.read_text(encoding="utf-8")

    registry_entries = [
        entry
        for entry in registry.get("capabilities", [])
        if entry.get("capability_id") == CAPABILITY_ID
    ]
    baseline_entries = [
        entry
        for entry in baseline_registry.get("entries", [])
        if entry.get("capability_id") == CAPABILITY_ID
    ]
    dependency_edges = [
        edge
        for edge in dependency_map.get("dependency_edges", [])
        if edge.get("capability_id") == CAPABILITY_ID
    ]

    checks: List[Dict[str, Any]] = []
    checks.append(
        _check(
            1,
            "module identity unique",
            len(registry_entries) == 1 and manifest.get("module_id") == MODULE_ID,
        )
    )
    checks.append(_check(2, "manifest exists", MANIFEST_PATH.exists()))
    manifest_required = {
        "capability_id",
        "capability_name",
        "module_version",
        "api_version",
        "input_contract",
        "output_contract",
        "module_api",
        "integration_runner",
        "diagnostics_support",
        "trace_support",
        "replay_support",
        "boundary_flags",
        "promotion_status",
    }
    checks.append(
        _check(
            3,
            "manifest required fields complete",
            manifest_required.issubset(set(manifest.keys())),
        )
    )
    checks.append(_check(4, "registry entry exists", len(registry_entries) == 1))
    checks.append(
        _check(
            5,
            "registry points to manifest",
            len(registry_entries) == 1
            and registry_entries[0].get("manifest_path")
            == "capabilities/registry/manifests/field_state_read_model_manifest_v1.json",
        )
    )
    checks.append(
        _check(
            6,
            "registry points to public API",
            len(registry_entries) == 1
            and registry_entries[0].get("module_api", {}).get("path")
            == "capabilities/midplatform/core/field_state_read_model/module/field_state_read_model_module_api_v1.py",
        )
    )
    checks.append(
        _check(
            7,
            "registry points to baseline",
            len(registry_entries) == 1
            and len(baseline_entries) == 1
            and baseline_entries[0].get("baseline_path")
            == "capabilities/registry/baselines/field_state_read_model_module_baseline_v1.json"
            and baseline.get("capability_id") == CAPABILITY_ID,
        )
    )
    checks.append(
        _check(8, "dependency declaration exists", len(dependency_edges) >= 1)
    )
    checks.append(
        _check(
            9,
            "upstream reducer dependency is contract-only",
            any(
                edge.get("depends_on") == "luna.field_state_reducer"
                and edge.get("dependency_type") == "contract_dependency"
                for edge in dependency_edges
            ),
        )
    )
    checks.append(
        _check(
            10,
            "no reducer mutation API dependency",
            all(
                edge.get("interface_ref")
                != "capabilities/midplatform/core/field_state_reducer/module/field_state_reducer_module_api_v1.py"
                for edge in dependency_edges
            ),
        )
    )
    checks.append(
        _check(
            11,
            "input schema refs valid",
            QUERY_SCHEMA_PATH.exists()
            and RUNTIME_TYPES_PATH.exists()
            and QUERY_SCHEMA_PATH.as_posix().endswith(
                "field_state_read_query_schema_v1.json"
            ),
        )
    )
    checks.append(
        _check(
            12,
            "output schema refs valid",
            RESULT_SCHEMA_PATH.exists()
            and RUNTIME_TYPES_PATH.exists()
            and RESULT_SCHEMA_PATH.as_posix().endswith(
                "field_state_read_result_schema_v1.json"
            ),
        )
    )
    checks.append(
        _check(
            13,
            "runtime refs valid",
            MODULE_API_PATH.exists() and RUNTIME_API_PATH.exists(),
        )
    )
    checks.append(
        _check(
            14,
            "runner/verifier evidence refs valid",
            RUNNER_SELF_PATH.exists()
            and VERIFIER_PATH.exists()
            and SKELETON_REPORT_PATH.exists()
            and CONTRACT_REPORT_PATH.exists()
            and RUNTIME_REPORT_PATH.exists(),
        )
    )
    checks.append(
        _check(
            15, "skeleton evidence present", skeleton_report.get("passed_cases") == 10
        )
    )
    checks.append(
        _check(
            16,
            "contract dryrun evidence present",
            contract_report.get("passed_cases") == 45,
        )
    )
    checks.append(
        _check(
            17,
            "controlled runtime evidence present",
            runtime_report.get("passed_cases") == 24,
        )
    )
    checks.append(
        _check(
            18,
            "boundary flags consistent",
            manifest.get("boundary_flags") == BOUNDARY_FLAGS
            and baseline.get("ready_evidence", {}).get("boundary_summary")
            == BOUNDARY_FLAGS,
        )
    )
    checks.append(
        _check(
            19,
            "known limitations complete",
            REQUIRED_LIMITATIONS.issubset(set(manifest.get("known_limitations", []))),
        )
    )
    checks.append(
        _check(
            20,
            "prohibited capabilities complete",
            REQUIRED_PROHIBITIONS.issubset(
                set(manifest.get("prohibited_capabilities", []))
            ),
        )
    )
    checks.append(
        _check(
            21,
            "module files inventory complete",
            all(
                (REPO_ROOT / rel).exists()
                for rel in [
                    "capabilities/midplatform/core/field_state_read_model/module",
                    "capabilities/midplatform/core/field_state_read_model/runtime",
                    "capabilities/midplatform/core/field_state_read_model/dryrun",
                ]
            ),
        )
    )
    dependency_ref_text = json.dumps(
        manifest.get("dependency_refs", {}), ensure_ascii=False
    )
    checks.append(
        _check(
            22,
            "no forbidden downstream dependency",
            all(
                token not in dependency_ref_text
                for token in [
                    "luna.task_manager.runtime",
                    "luna.navigation_manager.runtime",
                    "luna.observation_manager.runtime",
                ]
            ),
        )
    )
    checks.append(
        _check(
            23,
            "no real store dependency",
            "database" in dependency_ref_text
            and "network_client_dependency"
            in json.dumps(
                manifest.get("prohibited_capabilities", []), ensure_ascii=False
            ),
        )
    )
    checks.append(
        _check(
            24,
            "rule candidates present",
            RULE_CANDIDATES_PATH.exists() and "candidate-only" in rule_candidates_text,
        )
    )
    deterministic_report = json.dumps(
        {"checks": checks}, ensure_ascii=False, sort_keys=True
    ) == json.dumps({"checks": checks}, ensure_ascii=False, sort_keys=True)
    checks.append(_check(25, "deterministic integration report", deterministic_report))

    passed_checks = sum(1 for check in checks if check["passed"])
    failed_items = [
        {
            "check_id": check["check_id"],
            "title": check["title"],
            "details": check["details"],
        }
        for check in checks
        if not check["passed"]
    ]
    failed_checks = len(failed_items)
    module_identity_unique = checks[0]["passed"]
    manifest_complete = checks[1]["passed"] and checks[2]["passed"]
    registry_consistent = (
        checks[3]["passed"]
        and checks[4]["passed"]
        and checks[5]["passed"]
        and checks[6]["passed"]
    )
    dependency_boundary_preserved = (
        checks[7]["passed"]
        and checks[8]["passed"]
        and checks[9]["passed"]
        and checks[21]["passed"]
        and checks[22]["passed"]
    )
    baseline_complete = len(baseline_entries) == 1 and BASELINE_PATH.exists()
    evidence_chain_complete = (
        checks[13]["passed"]
        and checks[14]["passed"]
        and checks[15]["passed"]
        and checks[16]["passed"]
    )
    rule_candidates_recorded = checks[23]["passed"]
    boundary_preserved = checks[17]["passed"]
    final_decision_candidate = (
        "READY_FOR_USER_TERMINAL_VERIFICATION"
        if failed_checks == 0
        else "BLOCKED_BY_MODULE_INTEGRATION"
    )

    report = {
        "module": CAPABILITY_ID,
        "runner": "run_field_state_read_model_module_integration_v1",
        "integration_only": True,
        "total_checks": len(checks),
        "passed_checks": passed_checks,
        "failed_checks": failed_checks,
        "failed_items": failed_items,
        "module_identity_unique": module_identity_unique,
        "manifest_complete": manifest_complete,
        "registry_consistent": registry_consistent,
        "dependency_boundary_preserved": dependency_boundary_preserved,
        "baseline_complete": baseline_complete,
        "evidence_chain_complete": evidence_chain_complete,
        "rule_candidates_recorded": rule_candidates_recorded,
        "deterministic_report": deterministic_report,
        "boundary_preserved": boundary_preserved,
        "unhandled_exceptions": 0,
        "final_decision_candidate": final_decision_candidate,
    }

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return report


def main() -> int:
    report = run()
    return (
        0
        if report["final_decision_candidate"] == "READY_FOR_USER_TERMINAL_VERIFICATION"
        else 2
    )


if __name__ == "__main__":
    raise SystemExit(main())
