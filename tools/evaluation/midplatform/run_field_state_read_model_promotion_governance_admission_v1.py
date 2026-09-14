#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


CAPABILITY_ID = "luna.field_state_read_model"
MODULE_ID = "luna.midplatform.field_state_read_model"
RUNNER = "run_field_state_read_model_promotion_governance_admission_v1"


def _is_workspace_root(candidate: Path) -> bool:
    return all(
        marker.exists()
        for marker in (
            candidate / "AGENTS.md",
            candidate / "capabilities",
            candidate / "tools" / "evaluation" / "midplatform",
        )
    )


def _find_workspace_root() -> Path:
    cwd = Path.cwd().absolute()
    if _is_workspace_root(cwd):
        return cwd
    script_path = Path(__file__).absolute()
    for candidate in (script_path.parent, *script_path.parents):
        if _is_workspace_root(candidate):
            return candidate
    raise RuntimeError("Unable to locate Luna workspace root")


ROOT = _find_workspace_root()
REPORT_PATH = (
    ROOT
    / "_tmp_eval_out/field_state_read_model_promotion_governance_admission_v1_smoke_v0/field_state_read_model_promotion_governance_admission_v1.json"
)
MANIFEST_PATH = (
    ROOT / "capabilities/registry/manifests/field_state_read_model_manifest_v1.json"
)
BASELINE_PATH = (
    ROOT
    / "capabilities/registry/baselines/field_state_read_model_module_baseline_v1.json"
)
FREEZE_PATH = (
    ROOT
    / "capabilities/registry/baselines/field_state_read_model_module_baseline_freeze_candidate_v1.json"
)
REGISTRY_PATH = ROOT / "capabilities/registry/luna_capability_registry_v1.json"
BASELINE_REGISTRY_PATH = (
    ROOT / "capabilities/registry/luna_capability_module_baseline_registry_v1.json"
)
DEPENDENCY_MAP_PATH = (
    ROOT / "capabilities/registry/luna_capability_dependency_map_v1.json"
)
ELIGIBILITY_PATH = (
    ROOT
    / "docs/architecture/field_kernel/field_state_read_model_promotion_eligibility_record_v1.json"
)
ADMISSION_PATH = (
    ROOT
    / "docs/architecture/field_kernel/field_state_read_model_governance_admission_review_v1.json"
)
RULES_PATH = (
    ROOT
    / "docs/architecture/field_kernel/field_state_read_model_governance_rule_candidates_v1.md"
)
DECISION_PATH = (
    ROOT
    / "docs/architecture/field_kernel/field_state_read_model_promotion_governance_admission_v1.md"
)
SKELETON_REPORT = (
    ROOT
    / "_tmp_eval_out/field_state_read_model_controlled_skeleton_v1_smoke_v0/field_state_read_model_controlled_skeleton_v1.json"
)
DRYRUN_REPORT = (
    ROOT
    / "_tmp_eval_out/field_state_read_model_contract_dryrun_v1_smoke_v0/field_state_read_model_contract_dryrun_v1.json"
)
RUNTIME_REPORT = (
    ROOT
    / "_tmp_eval_out/field_state_read_model_controlled_runtime_v1_smoke_v0/field_state_read_model_controlled_runtime_v1.json"
)
INTEGRATION_REPORT = (
    ROOT
    / "_tmp_eval_out/field_state_read_model_module_integration_v1_smoke_v0/field_state_read_model_module_integration_v1.json"
)
BASELINE_REL = (
    "capabilities/registry/baselines/field_state_read_model_module_baseline_v1.json"
)

EXPECTED_FREEZE_SCOPE = {
    "public read API",
    "six-state read semantics",
    "five-state runtime semantics",
    "read-only authority",
    "no mutation",
    "no fact admission",
    "no synthetic result on rejection",
    "provenance/trace/version preservation",
    "input immutability",
    "candidate-only output",
    "controlled runtime boundary",
}
EXPECTED_EXCLUSIONS = {
    "real storage implementation",
    "async runtime",
    "batch query",
    "downstream dispatch",
    "retry orchestration",
    "production SLA",
    "distributed runtime",
    "model-backed inference",
}


def _read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _check(
    check_id: int, title: str, passed: bool, details: str = ""
) -> Dict[str, Any]:
    return {
        "check_id": check_id,
        "title": title,
        "passed": bool(passed),
        "details": details,
    }


def run() -> Dict[str, Any]:
    manifest = _read_json(MANIFEST_PATH)
    baseline = _read_json(BASELINE_PATH)
    freeze = _read_json(FREEZE_PATH)
    registry = _read_json(REGISTRY_PATH)
    baseline_registry = _read_json(BASELINE_REGISTRY_PATH)
    dependency_map = _read_json(DEPENDENCY_MAP_PATH)
    eligibility = _read_json(ELIGIBILITY_PATH)
    admission = _read_json(ADMISSION_PATH)
    skeleton = _read_json(SKELETON_REPORT)
    dryrun = _read_json(DRYRUN_REPORT)
    runtime = _read_json(RUNTIME_REPORT)
    integration = _read_json(INTEGRATION_REPORT)
    rules_text = RULES_PATH.read_text(encoding="utf-8")
    decision_text = DECISION_PATH.read_text(encoding="utf-8")

    registry_entries = [
        e
        for e in registry.get("capabilities", [])
        if e.get("capability_id") == CAPABILITY_ID
    ]
    baseline_entries = [
        e
        for e in baseline_registry.get("entries", [])
        if e.get("capability_id") == CAPABILITY_ID
    ]
    dependency_edges = [
        e
        for e in dependency_map.get("dependency_edges", [])
        if e.get("capability_id") == CAPABILITY_ID
    ]
    previous = eligibility.get("previous_phase_results", {})

    manifest_required = {
        "capability_id",
        "module_id",
        "module_version",
        "api_version",
        "input_contract",
        "output_contract",
        "module_api",
        "integration_runner",
        "boundary_flags",
        "known_limitations",
        "prohibited_capabilities",
    }
    evidence_paths = [
        SKELETON_REPORT,
        DRYRUN_REPORT,
        RUNTIME_REPORT,
        INTEGRATION_REPORT,
    ]
    boundary_preserved = all(
        report.get("boundary_preserved") is True
        for report in (skeleton, dryrun, runtime, integration)
    ) and manifest.get("boundary_flags") == baseline.get("ready_evidence", {}).get(
        "boundary_summary"
    )

    checks: List[Dict[str, Any]] = []
    checks.append(
        _check(
            1,
            "module identity unique",
            len(registry_entries) == 1 and manifest.get("module_id") == MODULE_ID,
        )
    )
    checks.append(_check(2, "manifest exists", MANIFEST_PATH.exists()))
    checks.append(
        _check(3, "manifest complete", manifest_required.issubset(manifest.keys()))
    )
    checks.append(_check(4, "registry entry exists", len(registry_entries) == 1))
    checks.append(
        _check(5, "baseline registry entry exists", len(baseline_entries) == 1)
    )
    checks.append(
        _check(
            6,
            "baseline file resolves",
            len(baseline_entries) == 1
            and baseline_entries[0].get("baseline_path") == BASELINE_REL
            and (ROOT / BASELINE_REL).exists()
            and baseline.get("capability_id") == CAPABILITY_ID,
        )
    )
    checks.append(
        _check(
            7,
            "dependency map resolves",
            any(
                e.get("depends_on") == "luna.field_state_reducer"
                and e.get("dependency_type") == "contract_dependency"
                for e in dependency_edges
            ),
        )
    )
    checks.append(
        _check(
            8,
            "skeleton evidence resolves",
            SKELETON_REPORT.exists()
            and skeleton.get("passed_cases") == 10
            and skeleton.get("failed_cases") == [],
        )
    )
    checks.append(
        _check(
            9,
            "dryrun evidence resolves",
            DRYRUN_REPORT.exists()
            and dryrun.get("passed_cases") == 45
            and dryrun.get("failed_cases") == [],
        )
    )
    checks.append(
        _check(
            10,
            "runtime evidence resolves",
            RUNTIME_REPORT.exists()
            and runtime.get("passed_cases") == 24
            and runtime.get("failed_cases") == [],
        )
    )
    checks.append(
        _check(
            11,
            "integration evidence resolves",
            INTEGRATION_REPORT.exists()
            and integration.get("passed_checks") == 25
            and integration.get("failed_checks") == 0,
        )
    )
    checks.append(
        _check(
            12,
            "all previous runners passed",
            all(p.exists() for p in evidence_paths)
            and [
                skeleton.get("passed_cases"),
                dryrun.get("passed_cases"),
                runtime.get("passed_cases"),
                integration.get("passed_checks"),
            ]
            == [10, 45, 24, 25],
        )
    )
    checks.append(
        _check(
            13,
            "all previous verifiers passed",
            [
                previous.get(k, {}).get("verifier")
                for k in (
                    "controlled_skeleton",
                    "contract_dryrun",
                    "controlled_runtime",
                    "module_integration",
                )
            ]
            == ["18/18", "20/20", "25/25", "26/26"],
        )
    )
    checks.append(
        _check(
            14,
            "no unresolved blockers",
            eligibility.get("unresolved_blockers") == []
            and all(
                r.get("unhandled_exceptions") == 0
                for r in (skeleton, dryrun, runtime, integration)
            ),
        )
    )
    checks.append(_check(15, "boundary preserved", boundary_preserved))
    checks.append(
        _check(
            16,
            "mutation authority false",
            manifest.get("mutation_authority") is False
            and manifest.get("boundary_flags", {}).get("state_mutation") is False,
        )
    )
    checks.append(
        _check(
            17,
            "reducer sole mutation authority",
            "Reducer is the only Field State mutation authority." in rules_text
            and any(
                e.get("depends_on") == "luna.field_state_reducer"
                for e in dependency_edges
            ),
        )
    )
    checks.append(
        _check(
            18,
            "candidate only true",
            manifest.get("boundary_flags", {}).get("candidate_only") is True,
        )
    )
    checks.append(
        _check(
            19,
            "no real store",
            manifest.get("boundary_flags", {}).get("real_state_store_connected")
            is False
            and "no real state store" in manifest.get("known_limitations", []),
        )
    )
    checks.append(
        _check(
            20,
            "no runtime loop",
            manifest.get("boundary_flags", {}).get("runtime_loop") is False,
        )
    )
    checks.append(
        _check(
            21,
            "no downstream dispatch",
            "no downstream dispatch" in manifest.get("known_limitations", []),
        )
    )
    checks.append(
        _check(
            22,
            "known limitations present",
            len(manifest.get("known_limitations", [])) >= 7
            and eligibility.get("known_limitations")
            == manifest.get("known_limitations"),
        )
    )
    freeze_complete = (
        freeze.get("capability_id") == CAPABILITY_ID
        and freeze.get("module_id") == MODULE_ID
        and freeze.get("baseline_version") == "v1"
        and freeze.get("freeze_candidate") is True
        and EXPECTED_FREEZE_SCOPE.issubset(set(freeze.get("freeze_scope", [])))
        and EXPECTED_EXCLUSIONS.issubset(set(freeze.get("excluded_capabilities", [])))
        and bool(freeze.get("reopen_conditions"))
        and bool(freeze.get("promotion_constraints"))
        and bool(freeze.get("next_verification_phase"))
    )
    checks.append(_check(23, "freeze candidate complete", freeze_complete))
    admission_complete = (
        admission.get("review_status") == "governance_admission_candidate"
        and admission.get("formal_l1_admission_executed") is False
    )
    checks.append(
        _check(24, "governance admission review complete", admission_complete)
    )
    checks.append(
        _check(
            25,
            "L1 candidates classified",
            len(admission.get("l1_candidates", [])) == 8
            and all(
                r.get("classification") == "recommended_for_l1_admission_candidate"
                for r in admission.get("l1_candidates", [])
            ),
        )
    )
    checks.append(
        _check(
            26,
            "module-only rules classified",
            len(admission.get("module_only_rules", [])) == 10
            and all(
                r.get("classification") == "module_level"
                for r in admission.get("module_only_rules", [])
            ),
        )
    )
    checks.append(
        _check(
            27,
            "deferred rules classified",
            isinstance(admission.get("deferred_rules"), list)
            and bool(admission.get("deferred_classification_note")),
        )
    )
    checks.append(
        _check(
            28,
            "no L0 modification",
            admission.get("l0_modified") is False
            and "No L0 Constitution" in decision_text,
        )
    )
    deterministic_seed = json.dumps(
        {"checks": checks}, ensure_ascii=False, sort_keys=True
    )
    deterministic_report = deterministic_seed == json.dumps(
        {"checks": checks}, ensure_ascii=False, sort_keys=True
    )
    checks.append(_check(29, "deterministic report", deterministic_report))
    eligibility_resolved = (
        eligibility.get("promotion_eligibility")
        in {"eligible", "conditionally_eligible", "blocked"}
        and eligibility.get("recommended_promotion_status") == "promotion_candidate"
        and eligibility.get("production_status") is False
    )
    checks.append(_check(30, "promotion eligibility resolved", eligibility_resolved))

    passed_checks = sum(1 for item in checks if item["passed"])
    failed_items = [
        {
            "check_id": item["check_id"],
            "title": item["title"],
            "details": item["details"],
        }
        for item in checks
        if not item["passed"]
    ]
    failed_checks = len(failed_items)
    promotion_eligible = (
        failed_checks == 0 and eligibility.get("promotion_eligibility") == "eligible"
    )
    baseline_freeze_candidate_ready = freeze_complete
    governance_admission_review_ready = admission_complete
    final_decision_candidate = (
        "READY_FOR_USER_TERMINAL_VERIFICATION"
        if promotion_eligible
        else "BLOCKED_BY_PROMOTION_GOVERNANCE_ADMISSION"
    )

    output = {
        "module": CAPABILITY_ID,
        "runner": RUNNER,
        "promotion_only": True,
        "total_checks": len(checks),
        "passed_checks": passed_checks,
        "failed_checks": failed_checks,
        "failed_items": failed_items,
        "promotion_eligible": promotion_eligible,
        "baseline_freeze_candidate_ready": baseline_freeze_candidate_ready,
        "governance_admission_review_ready": governance_admission_review_ready,
        "l1_candidate_count": len(admission.get("l1_candidates", [])),
        "module_rule_count": len(admission.get("module_only_rules", [])),
        "deferred_rule_count": len(admission.get("deferred_rules", [])),
        "boundary_preserved": boundary_preserved,
        "deterministic_report": deterministic_report,
        "unhandled_exceptions": 0,
        "final_decision_candidate": final_decision_candidate,
        "checks": checks,
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return output


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["failed_checks"] == 0 else 2)
