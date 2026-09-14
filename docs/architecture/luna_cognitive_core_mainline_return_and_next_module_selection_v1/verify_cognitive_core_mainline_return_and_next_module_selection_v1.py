from __future__ import annotations

import ast
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Set

PHASE_DIR = Path(__file__).resolve().parent


@dataclass(frozen=True)
class CheckResult:
    check_id: str
    passed: bool
    detail: str


def _expect(condition: bool, check_id: str, ok: str, fail: str) -> CheckResult:
    return CheckResult(
        check_id=check_id, passed=condition, detail=ok if condition else fail
    )


def _required_files() -> Set[str]:
    return {
        "cognitive_core_current_module_inventory_v1.json",
        "cognitive_core_next_module_candidates_v1.json",
        "cognitive_core_next_module_selection_v1.json",
        "cognitive_core_mainline_return_summary_v1.md",
        "phase_contract.json",
        "verify_cognitive_core_mainline_return_and_next_module_selection_v1.py",
    }


def _load_json(name: str) -> Dict[str, Any]:
    obj = json.loads((PHASE_DIR / name).read_text(encoding="utf-8"))
    if not isinstance(obj, dict):
        raise TypeError(f"{name} must be a JSON object")
    return obj


def run_verification() -> Dict[str, Any]:
    results: List[CheckResult] = []

    actual = {p.name for p in PHASE_DIR.iterdir() if p.is_file()}
    required = _required_files()
    results.append(
        _expect(
            actual == required,
            "M01_exact_required_file_set",
            "Exact required file set present.",
            f"Mismatch missing={sorted(required - actual)} extra={sorted(actual - required)}",
        )
    )

    docs: Dict[str, Dict[str, Any]] = {}
    parse_fail: List[str] = []
    for name in [
        "cognitive_core_current_module_inventory_v1.json",
        "cognitive_core_next_module_candidates_v1.json",
        "cognitive_core_next_module_selection_v1.json",
        "phase_contract.json",
    ]:
        try:
            docs[name] = _load_json(name)
        except Exception as exc:
            docs[name] = {}
            parse_fail.append(f"{name}:{exc}")

    results.append(
        _expect(
            len(parse_fail) == 0,
            "M02_json_parse",
            "All JSON files parse.",
            f"JSON parse failures: {parse_fail}",
        )
    )

    ast_fail: List[str] = []
    try:
        ast.parse(
            (
                PHASE_DIR
                / "verify_cognitive_core_mainline_return_and_next_module_selection_v1.py"
            ).read_text(encoding="utf-8")
        )
    except Exception as exc:
        ast_fail.append(str(exc))

    results.append(
        _expect(
            len(ast_fail) == 0,
            "M03_ast_parse",
            "Verifier AST parse passed.",
            f"AST parse failures: {ast_fail}",
        )
    )

    inventory = docs.get("cognitive_core_current_module_inventory_v1.json", {})
    results.append(
        _expect(
            len(inventory.get("completed_and_frozen", [])) >= 7,
            "M04_inventory_completed_coverage",
            "Completed/frozen inventory coverage is sufficient.",
            f"completed_and_frozen size too small: {len(inventory.get('completed_and_frozen', []))}",
        )
    )

    candidates = docs.get("cognitive_core_next_module_candidates_v1.json", {}).get(
        "candidate_modules", []
    )
    results.append(
        _expect(
            len(candidates) >= 10,
            "M05_candidate_count",
            "Candidate module coverage complete.",
            f"candidate count too small: {len(candidates)}",
        )
    )

    required_candidate_fields = {
        "current_assets",
        "completion_level",
        "duplicate_implementation_risk",
        "cognitive_mainline_relation",
        "real_runtime_dependency",
        "core_differentiation_gain",
        "priority",
        "should_do_now",
        "stop_condition",
    }
    field_fail = []
    for item in candidates:
        if not isinstance(item, dict):
            field_fail.append("non-dict-candidate")
            continue
        missing = sorted(required_candidate_fields - set(item.keys()))
        if missing:
            field_fail.append(f"{item.get('candidate_id', 'unknown')}:{missing}")

    results.append(
        _expect(
            len(field_fail) == 0,
            "M06_candidate_field_completeness",
            "All candidates contain required evaluation fields.",
            f"Candidate field failures: {field_fail}",
        )
    )

    selection = docs.get("cognitive_core_next_module_selection_v1.json", {})
    required_selection_fields = [
        "selected_next_module",
        "selection_reason",
        "why_now",
        "why_not_other_candidates",
        "upstream_dependencies",
        "downstream_value",
        "implementation_scope",
        "stop_condition",
    ]
    missing_selection = [k for k in required_selection_fields if k not in selection]

    results.append(
        _expect(
            len(missing_selection) == 0,
            "M07_selection_fields",
            "Selection contains all mandatory decision fields.",
            f"Missing selection fields: {missing_selection}",
        )
    )

    should_do_now = [
        item
        for item in candidates
        if isinstance(item, dict) and item.get("should_do_now") is True
    ]
    results.append(
        _expect(
            len(should_do_now) == 1,
            "M08_single_now_candidate",
            "Exactly one candidate marked should_do_now=true.",
            f"should_do_now candidates: {[x.get('candidate_id') for x in should_do_now]}",
        )
    )

    phase = docs.get("phase_contract.json", {})
    b = phase.get("boundaries", {})
    results.append(
        _expect(
            b.get("audit_only") is True
            and b.get("planning_only") is True
            and b.get("runtime_executed") is False
            and b.get("database_write") is False
            and b.get("device_control") is False
            and b.get("scheduler_execution") is False
            and b.get("task_mutation") is False
            and b.get("source_module_mutation") is False,
            "M09_boundary_flags",
            "Boundary flags are correct.",
            f"Boundary mismatch: {b}",
        )
    )

    results.append(
        _expect(
            selection.get("selected_next_module")
            == "Context->PCN->Intent Pre-Cognitive Mainline Module",
            "M10_mainline_selection_target",
            "Selected module is set.",
            f"Selected module mismatch: {selection.get('selected_next_module')}",
        )
    )

    passed = [r for r in results if r.passed]
    failed = [r for r in results if not r.passed]

    return {
        "phase_id": "Phase-Luna-Cognitive-Core-Mainline-Return-And-Next-Module-Selection-v1-001",
        "checks": [
            {"check_id": r.check_id, "passed": r.passed, "detail": r.detail}
            for r in results
        ],
        "summary": {
            "total_checks": len(results),
            "passed_check_count": len(passed),
            "failed_check_count": len(failed),
            "blocker_count": len(failed),
        },
        "failed_checks": [{"check_id": r.check_id, "detail": r.detail} for r in failed],
        "final_decision_candidate": "LUNA_COGNITIVE_CORE_MAINLINE_RETURN_AND_NEXT_MODULE_SELECTION_READY_FOR_USER_V2_VERIFICATION"
        if not failed
        else "LUNA_COGNITIVE_CORE_MAINLINE_RETURN_AND_NEXT_MODULE_SELECTION_BLOCKED",
        "current_status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
        "next": "USER_TERMINAL_RUN_VERIFY_COGNITIVE_CORE_MAINLINE_RETURN_AND_NEXT_MODULE_SELECTION_V1",
        "note": "Agent must not declare GO. User terminal V2 verification and ChatGPT V3 audit are required.",
    }


if __name__ == "__main__":
    print(json.dumps(run_verification(), ensure_ascii=True, indent=2))
