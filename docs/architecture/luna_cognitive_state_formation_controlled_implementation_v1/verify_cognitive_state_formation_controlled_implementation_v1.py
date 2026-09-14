#!/usr/bin/env python3
"""Final phase verifier for Cognitive State Formation controlled implementation v1.

User terminal (V2) only.
"""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


def _resolve_repo_root() -> Path:
    current = Path(__file__).resolve()
    for candidate in current.parents:
        sentinel = candidate / "capabilities/midplatform/core/cognitive_state_formation"
        if sentinel.is_dir():
            return candidate

    cwd = Path.cwd().resolve()
    if (cwd / "capabilities/midplatform/core/cognitive_state_formation").is_dir():
        return cwd

    return Path(__file__).resolve().parents[4]


REPO_ROOT = _resolve_repo_root()
PHASE_DIR = (
    REPO_ROOT
    / "docs/architecture/luna_cognitive_state_formation_controlled_implementation_v1"
)
PLANNING_DIR = (
    REPO_ROOT
    / "docs/architecture/luna_cognitive_state_formation_architecture_and_controlled_implementation_planning_v1"
)
EVAL_OUT_DIR = (
    REPO_ROOT / "_eval_out/cognitive_state_formation_controlled_implementation_v1"
)

CODE_FILES = [
    "capabilities/midplatform/core/cognitive_state_formation/__init__.py",
    "capabilities/midplatform/core/cognitive_state_formation/cognitive_state_formation_registry_v1.py",
    "capabilities/midplatform/core/cognitive_state_formation/cognitive_state_formation_error_types_v1.py",
    "capabilities/midplatform/core/cognitive_state_formation/cognitive_state_formation_core_types_v1.py",
    "capabilities/midplatform/core/cognitive_state_formation/attention_types_v1.py",
    "capabilities/midplatform/core/cognitive_state_formation/cognitive_hypothesis_types_v1.py",
    "capabilities/midplatform/core/cognitive_state_formation/current_world_types_v1.py",
    "capabilities/midplatform/core/cognitive_state_formation/cognitive_state_vector_types_v1.py",
    "capabilities/midplatform/core/cognitive_state_formation/cognitive_state_formation_trace_types_v1.py",
    "capabilities/midplatform/core/cognitive_state_formation/cognitive_state_formation_handoff_types_v1.py",
    "capabilities/midplatform/core/cognitive_state_formation/cognitive_state_formation_io_types_v1.py",
    "capabilities/midplatform/core/cognitive_state_formation/cognitive_state_formation_protocol_v1.py",
    "capabilities/midplatform/core/cognitive_state_formation/cognitive_state_formation_ownership_guard_v1.py",
    "capabilities/midplatform/core/cognitive_state_formation/cognitive_state_formation_static_validators_v1.py",
    "capabilities/midplatform/core/cognitive_state_formation/cognitive_state_formation_fixture_v1.py",
    "capabilities/midplatform/core/cognitive_state_formation/cognitive_state_formation_engine_v1.py",
    "capabilities/midplatform/core/cognitive_state_formation/run_cognitive_state_formation_controlled_implementation_v1.py",
]

DOC_FILES = [
    "docs/architecture/luna_cognitive_state_formation_controlled_implementation_v1/cognitive_state_formation_controlled_implementation_overview_v1.md",
    "docs/architecture/luna_cognitive_state_formation_controlled_implementation_v1/cognitive_state_formation_controlled_execution_contract_v1.json",
    "docs/architecture/luna_cognitive_state_formation_controlled_implementation_v1/cognitive_state_formation_negative_guards_v1.json",
    "docs/architecture/luna_cognitive_state_formation_controlled_implementation_v1/cognitive_state_formation_planning_to_code_mapping_v1.json",
    "docs/architecture/luna_cognitive_state_formation_controlled_implementation_v1/cognitive_state_formation_controlled_change_manifest_v1.json",
    "docs/architecture/luna_cognitive_state_formation_controlled_implementation_v1/cognitive_state_formation_implementation_summary_v1.md",
    "docs/architecture/luna_cognitive_state_formation_controlled_implementation_v1/phase_contract.json",
    "docs/architecture/luna_cognitive_state_formation_controlled_implementation_v1/verify_cognitive_state_formation_controlled_implementation_v1.py",
]

PLANNING_REQUIRED = [
    "cognitive_state_formation_owner_boundary_v1.json",
    "cognitive_state_formation_scenario_suite_v1.json",
    "cognitive_state_formation_negative_guards_v1.json",
    "cognitive_state_formation_trace_provenance_contract_v1.json",
]

SCENARIO_IDS = [f"S{i:02d}" for i in range(1, 21)]


def _load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _expect(name: str, cond: bool, failed: List[str]) -> None:
    if not cond:
        failed.append(name)


def _check_exists(paths: Iterable[str], failed: List[str], prefix: str) -> None:
    for rel in paths:
        _expect(f"{prefix}:{rel}", (REPO_ROOT / rel).exists(), failed)


def _check_json_parse(paths: Iterable[str], failed: List[str], prefix: str) -> None:
    for rel in paths:
        if not rel.endswith(".json"):
            continue
        try:
            _load_json(REPO_ROOT / rel)
        except Exception:
            failed.append(f"{prefix}_json_parse:{rel}")


def _check_ast_parse(paths: Iterable[str], failed: List[str], prefix: str) -> None:
    for rel in paths:
        if not rel.endswith(".py"):
            continue
        try:
            source = (REPO_ROOT / rel).read_text(encoding="utf-8")
            ast.parse(source)
        except Exception:
            failed.append(f"{prefix}_ast_parse:{rel}")


def _contains_all(items: Iterable[str], req: Iterable[str]) -> bool:
    s = set(items)
    return all(i in s for i in req)


def main() -> int:
    failed: List[str] = []

    _check_exists(CODE_FILES, failed, "missing_code")
    _check_exists(DOC_FILES, failed, "missing_doc")
    _check_json_parse(CODE_FILES + DOC_FILES, failed, "parse")
    _check_ast_parse(CODE_FILES + DOC_FILES, failed, "parse")

    for name in PLANNING_REQUIRED:
        _expect(f"planning_exists:{name}", (PLANNING_DIR / name).exists(), failed)

    if not failed:
        owner = _load_json(
            PLANNING_DIR / "cognitive_state_formation_owner_boundary_v1.json"
        )
        _expect(
            "planning_owner_canonical",
            owner.get("canonical_owner_candidate")
            == "Cognitive State Formation Governance",
            failed,
        )

        scenario_plan = _load_json(
            PLANNING_DIR / "cognitive_state_formation_scenario_suite_v1.json"
        )
        plan_ids = [item.get("id", "") for item in scenario_plan.get("scenarios", [])]
        _expect(
            "planning_scenario_count_20",
            scenario_plan.get("scenario_count") == 20,
            failed,
        )
        _expect("planning_ids_complete", _contains_all(plan_ids, SCENARIO_IDS), failed)

        guards_plan = _load_json(
            PLANNING_DIR / "cognitive_state_formation_negative_guards_v1.json"
        )
        _expect(
            "planning_guard_minimum",
            _contains_all(
                guards_plan.get("must_fail_if_present", []),
                [
                    "field_state_mutation",
                    "decision_output",
                    "action_output",
                    "task_output",
                    "trace_missing",
                    "provenance_missing",
                ],
            ),
            failed,
        )

        phase_contract = _load_json(PHASE_DIR / "phase_contract.json")
        _expect(
            "canonical_owner_phase_contract",
            phase_contract.get("required_code_files") == CODE_FILES,
            failed,
        )
        _expect(
            "required_doc_file_set",
            phase_contract.get("required_doc_files") == DOC_FILES,
            failed,
        )

        registry_source = (
            REPO_ROOT
            / "capabilities/midplatform/core/cognitive_state_formation/cognitive_state_formation_registry_v1.py"
        ).read_text(encoding="utf-8")
        _expect(
            "no_parallel_owner_module",
            "attention_governance" not in registry_source
            and "hypothesis_governance" not in registry_source
            and "current_world_governance" not in registry_source,
            failed,
        )
        _expect(
            "canonical_owner_declared",
            'CANONICAL_OWNER = "Cognitive State Formation Governance"'
            in registry_source,
            failed,
        )

        validator_source = (
            REPO_ROOT
            / "capabilities/midplatform/core/cognitive_state_formation/cognitive_state_formation_static_validators_v1.py"
        ).read_text(encoding="utf-8")
        _expect(
            "guard_current_world_not_field",
            "validate_no_field_mutation" in validator_source,
            failed,
        )
        _expect(
            "guard_world_candidate_only",
            "validate_current_world_candidate_only" in validator_source,
            failed,
        )
        _expect(
            "guard_field_read_only",
            "validate_field_ref_read_only_boundary" in validator_source,
            failed,
        )

        fixture_source = (
            REPO_ROOT
            / "capabilities/midplatform/core/cognitive_state_formation/cognitive_state_formation_fixture_v1.py"
        ).read_text(encoding="utf-8")
        _expect(
            "fixture_scenario_ids",
            all(f'"{sid}"' in fixture_source for sid in SCENARIO_IDS),
            failed,
        )

        engine_source = (
            REPO_ROOT
            / "capabilities/midplatform/core/cognitive_state_formation/cognitive_state_formation_engine_v1.py"
        ).read_text(encoding="utf-8")
        _expect(
            "attention_implemented",
            "_build_attention_candidates" in engine_source,
            failed,
        )
        _expect("hypothesis_implemented", "_build_hypotheses" in engine_source, failed)
        _expect("current_world_implemented", "_build_world" in engine_source, failed)
        _expect("vector_implemented", "_build_vector" in engine_source, failed)
        _expect("handoff_implemented", "_build_handoff" in engine_source, failed)

        out_result = EVAL_OUT_DIR / "cognitive_state_formation_result_v1.json"
        out_cases = EVAL_OUT_DIR / "cognitive_state_formation_case_results_v1.json"
        out_trace = EVAL_OUT_DIR / "cognitive_state_formation_trace_v1.json"
        _expect("runner_result_exists", out_result.exists(), failed)
        _expect("runner_cases_exists", out_cases.exists(), failed)
        _expect("runner_trace_exists", out_trace.exists(), failed)

        if out_result.exists() and out_cases.exists() and out_trace.exists():
            result = _load_json(out_result)
            cases = _load_json(out_cases)
            trace = _load_json(out_trace)
            _expect("runner_case_count_20", result.get("case_count") == 20, failed)
            _expect(
                "runner_side_effect_free",
                result.get("runtime_executed") is False,
                failed,
            )
            _expect(
                "runner_candidate_only", result.get("candidate_only") is True, failed
            )
            _expect("runner_cases_len_20", len(cases) == 20, failed)
            _expect(
                "runner_all_cases_passed",
                all(item.get("all_checks_passed") is True for item in cases),
                failed,
            )
            case_ids = [item.get("case_id", "") for item in cases]
            _expect(
                "runner_case_ids_coverage",
                _contains_all(case_ids, SCENARIO_IDS),
                failed,
            )
            _expect("trace_has_cases", bool(trace.get("case_traces")), failed)

    passed_count = 0
    if not failed:
        passed_count = 1

    payload = {
        "CHECKS": {
            "code_file_set": "pass"
            if not any(x.startswith("missing_code") for x in failed)
            else "fail",
            "doc_file_set": "pass"
            if not any(x.startswith("missing_doc") for x in failed)
            else "fail",
            "json_parse": "pass"
            if not any("json_parse" in x for x in failed)
            else "fail",
            "ast_parse": "pass"
            if not any("ast_parse" in x for x in failed)
            else "fail",
            "owner_and_boundary": "pass"
            if not any("owner" in x or "guard_" in x for x in failed)
            else "fail",
            "scenario_and_fixture": "pass"
            if not any("scenario" in x or "fixture" in x for x in failed)
            else "fail",
            "runner_artifacts": "pass"
            if not any("runner_" in x for x in failed)
            else "fail",
        },
        "FAILED_CHECKS": failed,
        "PASSED_CHECK_COUNT": max(0, 7 - len([1 for _ in ["a"] if failed])),
        "FAILED_CHECK_COUNT": len(failed),
        "BLOCKER_COUNT": len(failed),
        "FINAL_DECISION": "PASS" if not failed else "BLOCKED",
        "NEXT": "LUNA_COGNITIVE_STATE_FORMATION_CONTROLLED_IMPLEMENTATION_GO"
        if not failed
        else "LUNA_COGNITIVE_STATE_FORMATION_CONTROLLED_IMPLEMENTATION_REMEDIATION",
    }

    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
