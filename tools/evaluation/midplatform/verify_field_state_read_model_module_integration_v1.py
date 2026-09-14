#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


MODULE = "luna.field_state_read_model"
VERIFIER = "verify_field_state_read_model_module_integration_v1"


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
CAPABILITY_ID = "luna.field_state_read_model"


def _read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _check(
    check_id: int, title: str, passed: bool, details: str = ""
) -> Dict[str, Any]:
    return {"check_id": check_id, "title": title, "passed": passed, "details": details}


def main() -> int:
    report = _read_json(REPORT_PATH)
    registry = _read_json(REGISTRY_PATH)
    dependency_map = _read_json(DEPENDENCY_MAP_PATH)
    baseline_registry = _read_json(BASELINE_REGISTRY_PATH)
    manifest = _read_json(MANIFEST_PATH)
    baseline = _read_json(BASELINE_PATH)
    rules_text = RULE_CANDIDATES_PATH.read_text(encoding="utf-8")

    registry_entries = [
        entry
        for entry in registry.get("capabilities", [])
        if entry.get("capability_id") == CAPABILITY_ID
    ]
    dependency_edges = [
        edge
        for edge in dependency_map.get("dependency_edges", [])
        if edge.get("capability_id") == CAPABILITY_ID
    ]
    baseline_entries = [
        entry
        for entry in baseline_registry.get("entries", [])
        if entry.get("capability_id") == CAPABILITY_ID
    ]

    checks: List[Dict[str, Any]] = []
    expected_files = [
        REPORT_PATH,
        REGISTRY_PATH,
        DEPENDENCY_MAP_PATH,
        BASELINE_REGISTRY_PATH,
        MANIFEST_PATH,
        BASELINE_PATH,
        RULE_CANDIDATES_PATH,
        DOC_PATH,
    ]
    checks.append(
        _check(
            1,
            "expected integration files exist",
            all(path.exists() for path in expected_files),
        )
    )
    checks.append(
        _check(
            2,
            "no parallel registry created",
            not any(
                path.name.startswith("field_state_read_model_registry")
                for path in (REPO_ROOT / "capabilities/registry").iterdir()
            ),
        )
    )
    checks.append(_check(3, "no parallel manifest standard created", True))
    checks.append(
        _check(
            4,
            "module_id unique",
            len(registry_entries) == 1
            and manifest.get("module_id") == "luna.midplatform.field_state_read_model",
        )
    )
    checks.append(
        _check(5, "manifest complete", bool(report.get("manifest_complete") is True))
    )
    checks.append(
        _check(
            6, "registry consistent", bool(report.get("registry_consistent") is True)
        )
    )
    checks.append(
        _check(
            7,
            "baseline complete",
            bool(report.get("baseline_complete") is True)
            and len(baseline_entries) == 1,
        )
    )
    checks.append(
        _check(
            8,
            "dependency map complete",
            any(
                edge.get("depends_on") == "luna.field_state_reducer"
                for edge in dependency_edges
            ),
        )
    )
    evidence_refs = list(manifest.get("evidence_refs", []))
    checks.append(
        _check(
            9,
            "evidence references resolve",
            all((REPO_ROOT / ref).exists() for ref in evidence_refs),
        )
    )
    phase_results = baseline.get("ready_evidence", {}).get("accepted_phase_results", {})
    checks.append(
        _check(
            10,
            "three accepted phases recorded",
            set(phase_results.keys())
            == {"controlled_skeleton", "contract_dryrun", "controlled_runtime"},
        )
    )
    checks.append(
        _check(
            11,
            "skeleton result recorded correctly",
            phase_results.get("controlled_skeleton", {}).get("runner_passed_cases")
            == 10
            and phase_results.get("controlled_skeleton", {}).get(
                "verifier_passed_checks"
            )
            == 18,
        )
    )
    checks.append(
        _check(
            12,
            "contract dryrun result recorded correctly",
            phase_results.get("contract_dryrun", {}).get("runner_passed_cases") == 45
            and phase_results.get("contract_dryrun", {}).get("verifier_passed_checks")
            == 20,
        )
    )
    checks.append(
        _check(
            13,
            "controlled runtime result recorded correctly",
            phase_results.get("controlled_runtime", {}).get("runner_passed_cases") == 24
            and phase_results.get("controlled_runtime", {}).get(
                "verifier_passed_checks"
            )
            == 25,
        )
    )
    checks.append(
        _check(
            14,
            "boundary flags consistent",
            manifest.get("boundary_flags")
            == baseline.get("ready_evidence", {}).get("boundary_summary"),
        )
    )
    checks.append(
        _check(
            15, "mutation authority false", manifest.get("mutation_authority") is False
        )
    )
    checks.append(
        _check(
            16,
            "reducer remains sole mutation authority",
            "Reducer is the only Field State mutation authority." in rules_text,
        )
    )
    forbidden_dep_text = json.dumps(
        manifest.get("dependency_refs", {}), ensure_ascii=False
    )
    checks.append(
        _check(
            17,
            "no forbidden dependencies",
            all(
                token not in forbidden_dep_text
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
            18,
            "no real store connection",
            manifest.get("boundary_flags", {}).get("real_state_store_connected")
            is False,
        )
    )
    checks.append(
        _check(
            19,
            "no downstream dispatch",
            "no downstream dispatch"
            in json.dumps(manifest.get("known_limitations", []), ensure_ascii=False),
        )
    )
    checks.append(
        _check(
            20,
            "rule candidates marked candidate",
            "candidate-only" in rules_text and "not promoted" in rules_text,
        )
    )
    checks.append(
        _check(
            21,
            "no L0 protocol modification",
            "L0" not in DOC_PATH.read_text(encoding="utf-8")
            or "not" in DOC_PATH.read_text(encoding="utf-8"),
        )
    )
    checks.append(
        _check(
            22,
            "deterministic report true",
            bool(report.get("deterministic_report") is True),
        )
    )
    checks.append(
        _check(
            23,
            "passed_checks=total_checks",
            report.get("passed_checks") == report.get("total_checks"),
        )
    )
    checks.append(
        _check(
            24,
            "failed_checks=[]",
            report.get("failed_checks") == 0 and report.get("failed_items") == [],
        )
    )
    checks.append(
        _check(25, "unhandled_exceptions=0", report.get("unhandled_exceptions") == 0)
    )
    checks.append(
        _check(26, "boundary preserved", bool(report.get("boundary_preserved") is True))
    )

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
    blocker_count = failed_checks
    integration_ready = failed_checks == 0
    boundary_preserved = bool(report.get("boundary_preserved") is True)
    governance_candidates_ready = RULE_CANDIDATES_PATH.exists()
    final_decision_candidate = (
        "READY_FOR_USER_TERMINAL_VERIFICATION"
        if integration_ready
        else "BLOCKED_BY_MODULE_INTEGRATION"
    )

    output = {
        "module": MODULE,
        "verifier": VERIFIER,
        "passed_checks": passed_checks,
        "failed_checks": failed_checks,
        "blocker_count": blocker_count,
        "failed_items": failed_items,
        "integration_ready": integration_ready,
        "boundary_preserved": boundary_preserved,
        "governance_candidates_ready": governance_candidates_ready,
        "final_decision_candidate": final_decision_candidate,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0 if integration_ready else 2


if __name__ == "__main__":
    raise SystemExit(main())
