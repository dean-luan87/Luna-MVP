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
        "cognitive_state_formation_current_inventory_v1.json",
        "cognitive_state_formation_candidate_modules_v1.json",
        "cognitive_state_formation_boundary_risk_matrix_v1.json",
        "cognitive_state_formation_next_module_selection_v1.json",
        "phase_contract.json",
        "verify_cognitive_state_formation_next_module_selection_v1.py",
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
            "S01_exact_required_file_set",
            "Exact required file set present.",
            f"Mismatch missing={sorted(required - actual)} extra={sorted(actual - required)}",
        )
    )

    parse_fail: List[str] = []
    docs: Dict[str, Dict[str, Any]] = {}
    for name in [
        "cognitive_state_formation_current_inventory_v1.json",
        "cognitive_state_formation_candidate_modules_v1.json",
        "cognitive_state_formation_boundary_risk_matrix_v1.json",
        "cognitive_state_formation_next_module_selection_v1.json",
        "phase_contract.json",
    ]:
        try:
            docs[name] = _load_json(name)
        except Exception as exc:
            parse_fail.append(f"{name}:{exc}")
            docs[name] = {}

    results.append(
        _expect(
            len(parse_fail) == 0,
            "S02_json_parse",
            "All JSON files parse.",
            f"JSON parse failures: {parse_fail}",
        )
    )

    ast_fail: List[str] = []
    try:
        ast.parse(
            (
                PHASE_DIR
                / "verify_cognitive_state_formation_next_module_selection_v1.py"
            ).read_text(encoding="utf-8")
        )
    except Exception as exc:
        ast_fail.append(str(exc))

    results.append(
        _expect(
            len(ast_fail) == 0,
            "S03_ast_parse",
            "Verifier AST parse passed.",
            f"AST parse failures: {ast_fail}",
        )
    )

    cand = docs.get("cognitive_state_formation_candidate_modules_v1.json", {}).get(
        "candidates", []
    )
    cand_ids = {item.get("candidate_id") for item in cand if isinstance(item, dict)}
    results.append(
        _expect(
            cand_ids == {"A", "B", "C"},
            "S04_candidate_set_abc",
            "Candidate set A/B/C complete.",
            f"candidate_ids mismatch: {sorted(x for x in cand_ids if x is not None)}",
        )
    )

    selection = docs.get("cognitive_state_formation_next_module_selection_v1.json", {})
    required_selection_fields = [
        "selected_next_module",
        "selection_reason",
        "why_now",
        "why_not_others",
        "relationship_to_field_state",
        "relationship_to_causal_governance",
        "relationship_to_context_intent_chain",
        "upstream_dependencies",
        "downstream_value",
        "implementation_scope",
        "stop_condition",
    ]
    missing_selection = [k for k in required_selection_fields if k not in selection]
    results.append(
        _expect(
            len(missing_selection) == 0,
            "S05_selection_fields",
            "Selection fields complete.",
            f"Missing fields: {missing_selection}",
        )
    )

    results.append(
        _expect(
            selection.get("selected_next_module")
            == "Attention -> Hypothesis -> Current World Cognitive State Formation Module",
            "S06_selected_module_target",
            "Selected module is expected A-module.",
            f"selected_next_module={selection.get('selected_next_module')}",
        )
    )

    matrix = docs.get("cognitive_state_formation_boundary_risk_matrix_v1.json", {}).get(
        "focus_judgements", {}
    )
    results.append(
        _expect(
            all(
                key in matrix
                for key in (
                    "J1_attention_hypothesis_current_world_single_module",
                    "J2_hypothesis_vs_causal_governance_boundary",
                    "J3_current_world_vs_field_state_reducer_boundary",
                    "J4_dynamic_function_start_readiness",
                    "J5_learning_dependency_on_memory_experience",
                )
            ),
            "S07_focus_judgements_complete",
            "All five required focus judgements are present.",
            "Missing one or more focus judgement entries.",
        )
    )

    inv = docs.get("cognitive_state_formation_current_inventory_v1.json", {})
    status = inv.get("upstream_mainline_status", {}).get("context_pcn_intent_chain")
    results.append(
        _expect(
            status == "GO",
            "S08_upstream_status_go",
            "Upstream context-pcn-intent chain status recorded as GO.",
            f"upstream status mismatch: {status}",
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
            "S09_boundary_flags",
            "Boundary flags are correct.",
            f"Boundary mismatch: {b}",
        )
    )

    results.append(
        _expect(
            phase.get("verification", {}).get("agent_stop_status")
            == "WAITING_FOR_USER_TERMINAL_VERIFICATION",
            "S10_agent_stop_status",
            "Agent stop status is correct.",
            f"agent_stop_status={phase.get('verification', {}).get('agent_stop_status')}",
        )
    )

    passed = [r for r in results if r.passed]
    failed = [r for r in results if not r.passed]

    return {
        "phase_id": "Phase-Luna-Cognitive-State-Formation-Next-Module-Selection-v1-001",
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
        "final_decision_candidate": "LUNA_COGNITIVE_STATE_FORMATION_NEXT_MODULE_SELECTION_READY_FOR_USER_V2_VERIFICATION"
        if not failed
        else "LUNA_COGNITIVE_STATE_FORMATION_NEXT_MODULE_SELECTION_BLOCKED",
        "current_status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
        "next": "USER_TERMINAL_RUN_VERIFY_COGNITIVE_STATE_FORMATION_NEXT_MODULE_SELECTION_V1",
        "note": "Agent must not declare GO. User terminal V2 verification and ChatGPT V3 audit are required.",
    }


if __name__ == "__main__":
    print(json.dumps(run_verification(), ensure_ascii=True, indent=2))
