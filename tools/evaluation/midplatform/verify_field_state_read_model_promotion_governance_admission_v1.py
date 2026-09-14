#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


MODULE = "luna.field_state_read_model"
VERIFIER = "verify_field_state_read_model_promotion_governance_admission_v1"


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
ELIGIBILITY_PATH = (
    ROOT
    / "docs/architecture/field_kernel/field_state_read_model_promotion_eligibility_record_v1.json"
)
FREEZE_PATH = (
    ROOT
    / "capabilities/registry/baselines/field_state_read_model_module_baseline_freeze_candidate_v1.json"
)
ADMISSION_PATH = (
    ROOT
    / "docs/architecture/field_kernel/field_state_read_model_governance_admission_review_v1.json"
)
DECISION_PATH = (
    ROOT
    / "docs/architecture/field_kernel/field_state_read_model_promotion_governance_admission_v1.md"
)
MANIFEST_PATH = (
    ROOT / "capabilities/registry/manifests/field_state_read_model_manifest_v1.json"
)
BASELINE_PATH = (
    ROOT
    / "capabilities/registry/baselines/field_state_read_model_module_baseline_v1.json"
)

EXPECTED_SCOPE = {
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
READ_STATES = [
    "query_rejected",
    "state_unavailable",
    "stale_state",
    "insufficient_state",
    "partial_projection",
    "read_ready",
]
RUNTIME_STATES = [
    "runtime_completed",
    "runtime_partial",
    "runtime_unavailable",
    "runtime_rejected",
    "runtime_error_contained",
]


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


def main() -> int:
    report = _read_json(REPORT_PATH)
    eligibility = _read_json(ELIGIBILITY_PATH)
    freeze = _read_json(FREEZE_PATH)
    admission = _read_json(ADMISSION_PATH)
    decision_text = DECISION_PATH.read_text(encoding="utf-8")
    manifest = _read_json(MANIFEST_PATH)
    baseline = _read_json(BASELINE_PATH)
    behavior = freeze.get("included_runtime_behavior", {})

    expected_files = [
        REPORT_PATH,
        ELIGIBILITY_PATH,
        FREEZE_PATH,
        ADMISSION_PATH,
        DECISION_PATH,
        MANIFEST_PATH,
        BASELINE_PATH,
    ]
    previous = eligibility.get("previous_phase_results", {})
    checks: List[Dict[str, Any]] = []
    checks.append(
        _check(1, "expected files exist", all(path.exists() for path in expected_files))
    )
    checks.append(
        _check(
            2,
            "promotion eligibility resolved",
            eligibility.get("promotion_eligibility") == "eligible"
            and report.get("promotion_eligible") is True,
        )
    )
    freeze_complete = (
        freeze.get("freeze_candidate") is True
        and freeze.get("freeze_status") == "candidate_only"
        and bool(freeze.get("included_contracts"))
        and bool(freeze.get("included_evidence"))
    )
    checks.append(
        _check(
            3,
            "baseline freeze candidate complete",
            freeze_complete and report.get("baseline_freeze_candidate_ready") is True,
        )
    )
    checks.append(
        _check(
            4,
            "freeze scope correct",
            EXPECTED_SCOPE.issubset(set(freeze.get("freeze_scope", []))),
        )
    )
    checks.append(
        _check(
            5,
            "excluded capabilities recorded",
            EXPECTED_EXCLUSIONS.issubset(set(freeze.get("excluded_capabilities", []))),
        )
    )
    checks.append(
        _check(
            6,
            "reopen conditions recorded",
            len(freeze.get("reopen_conditions", [])) >= 8,
        )
    )
    checks.append(
        _check(
            7,
            "evidence chain complete",
            len(freeze.get("included_evidence", [])) == 4
            and report.get("promotion_only") is True,
        )
    )
    checks.append(
        _check(
            8,
            "previous phase results correct",
            [
                previous.get(k, {}).get("runner")
                for k in (
                    "controlled_skeleton",
                    "contract_dryrun",
                    "controlled_runtime",
                    "module_integration",
                )
            ]
            == ["10/10", "45/45", "24/24", "25/25"],
        )
    )
    checks.append(
        _check(
            9,
            "previous runner and verifier results correct",
            [
                previous.get(k, {}).get("verifier")
                for k in (
                    "controlled_skeleton",
                    "contract_dryrun",
                    "controlled_runtime",
                    "module_integration",
                )
            ]
            == ["18/18", "20/20", "25/25", "26/26"]
            and report.get("failed_checks") == 0,
        )
    )
    checks.append(
        _check(
            10,
            "boundary preserved",
            report.get("boundary_preserved") is True
            and manifest.get("boundary_flags")
            == baseline.get("ready_evidence", {}).get("boundary_summary"),
        )
    )
    checks.append(
        _check(
            11,
            "mutation authority false",
            manifest.get("mutation_authority") is False
            and freeze.get("included_boundary_flags", {}).get("state_mutation")
            is False,
        )
    )
    checks.append(
        _check(
            12,
            "reducer sole mutation authority",
            any(
                r.get("rule_id") == "MODULE-01"
                for r in admission.get("module_only_rules", [])
            ),
        )
    )
    checks.append(
        _check(
            13,
            "six-state semantics unchanged",
            behavior.get("read_statuses") == READ_STATES,
        )
    )
    checks.append(
        _check(
            14,
            "five-state semantics unchanged",
            behavior.get("runtime_statuses") == RUNTIME_STATES,
        )
    )
    checks.append(
        _check(
            15,
            "no core implementation modified",
            freeze.get("core_implementation_modified") is False
            and "No Read Model module/runtime/dryrun implementation modification."
            in decision_text,
        )
    )
    checks.append(
        _check(
            16,
            "no real store",
            freeze.get("included_boundary_flags", {}).get("real_state_store_connected")
            is False
            and "real storage implementation"
            in freeze.get("excluded_capabilities", []),
        )
    )
    checks.append(
        _check(
            17,
            "no downstream dispatch",
            "downstream dispatch" in freeze.get("excluded_capabilities", []),
        )
    )
    checks.append(
        _check(
            18,
            "L1 candidates classified",
            len(admission.get("l1_candidates", [])) == 8
            and report.get("l1_candidate_count") == 8,
        )
    )
    checks.append(
        _check(
            19,
            "module-only rules classified",
            len(admission.get("module_only_rules", [])) == 10
            and report.get("module_rule_count") == 10,
        )
    )
    checks.append(
        _check(
            20,
            "deferred rules classified",
            isinstance(admission.get("deferred_rules"), list)
            and bool(admission.get("deferred_classification_note"))
            and report.get("deferred_rule_count")
            == len(admission.get("deferred_rules", [])),
        )
    )
    checks.append(
        _check(
            21,
            "no L0 modification",
            admission.get("l0_modified") is False
            and "No L0 Constitution" in decision_text,
        )
    )
    checks.append(
        _check(
            22,
            "no production status",
            eligibility.get("production_status") is False
            and freeze.get("production_status") is False
            and manifest.get("promotion_status") != "production",
        )
    )
    checks.append(
        _check(
            23, "deterministic report true", report.get("deterministic_report") is True
        )
    )
    checks.append(
        _check(
            24,
            "passed_checks equals total_checks",
            report.get("passed_checks") == report.get("total_checks") == 30,
        )
    )
    checks.append(
        _check(
            25,
            "failed checks empty",
            report.get("failed_checks") == 0 and report.get("failed_items") == [],
        )
    )
    checks.append(
        _check(26, "blocker count zero", eligibility.get("unresolved_blockers") == [])
    )
    checks.append(
        _check(27, "unhandled exceptions zero", report.get("unhandled_exceptions") == 0)
    )
    checks.append(
        _check(
            28,
            "promotion ready",
            report.get("final_decision_candidate")
            == "READY_FOR_USER_TERMINAL_VERIFICATION"
            and report.get("governance_admission_review_ready") is True,
        )
    )

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
    blocker_count = failed_checks
    promotion_ready = failed_checks == 0
    output = {
        "module": MODULE,
        "verifier": VERIFIER,
        "passed_checks": passed_checks,
        "failed_checks": failed_checks,
        "blocker_count": blocker_count,
        "failed_items": failed_items,
        "promotion_ready": promotion_ready,
        "baseline_freeze_candidate_ready": report.get("baseline_freeze_candidate_ready")
        is True,
        "governance_admission_candidate_ready": report.get(
            "governance_admission_review_ready"
        )
        is True,
        "boundary_preserved": report.get("boundary_preserved") is True,
        "final_decision_candidate": "READY_FOR_USER_TERMINAL_VERIFICATION"
        if promotion_ready
        else "BLOCKED_BY_PROMOTION_GOVERNANCE_ADMISSION",
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0 if promotion_ready else 2


if __name__ == "__main__":
    raise SystemExit(main())
