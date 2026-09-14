"""Static verifier for Outcome Evaluation Governance controlled implementation."""

from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any


def find_repo_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in (current, *current.parents):
        if all((candidate / marker).exists() for marker in ("capabilities", "docs", "README.md")):
            return candidate
    raise FileNotFoundError("repository root sentinel not found")


REPO_ROOT = find_repo_root(Path(__file__).resolve())
CODE_DIR = REPO_ROOT / "capabilities/midplatform/core/outcome_evaluation_governance"
DOC_DIR = REPO_ROOT / "docs/architecture/luna_a_route_result_comparison_outcome_evaluation_controlled_implementation_v1"
OUTPUT_DIR = REPO_ROOT / "_eval_out/outcome_evaluation_controlled_implementation_v1"

CODE_FILES = {
    "__init__.py",
    "outcome_evaluation_registry_v1.py",
    "outcome_evaluation_error_types_v1.py",
    "outcome_evaluation_core_types_v1.py",
    "outcome_evaluation_protocol_v1.py",
    "outcome_evaluation_ownership_guard_v1.py",
    "outcome_evaluation_static_validators_v1.py",
    "outcome_evaluation_engine_v1.py",
    "outcome_evaluation_fixture_v1.py",
    "run_outcome_evaluation_controlled_implementation_v1.py",
}
DOC_FILES = {
    "outcome_evaluation_controlled_implementation_overview_v1.md",
    "outcome_evaluation_controlled_execution_contract_v1.json",
    "outcome_evaluation_negative_guards_v1.json",
    "outcome_evaluation_planning_to_code_mapping_v1.json",
    "outcome_evaluation_controlled_change_manifest_v1.json",
    "outcome_evaluation_implementation_summary_v1.md",
    "phase_contract.json",
    "verify_outcome_evaluation_controlled_implementation_v1.py",
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def check(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def main() -> int:
    failures: list[str] = []
    check({item.name for item in CODE_DIR.iterdir() if item.is_file()} == CODE_FILES, "exact code file set", failures)
    check({item.name for item in DOC_DIR.iterdir() if item.is_file()} == DOC_FILES, "exact documentation file set", failures)

    for path in [CODE_DIR / name for name in CODE_FILES] + [DOC_DIR / name for name in DOC_FILES if name.endswith(".py")]:
        try:
            ast.parse(path.read_text(encoding="utf-8"))
        except (OSError, SyntaxError) as exc:
            failures.append(f"AST parse failed: {path.name}: {exc}")

    json_assets = [DOC_DIR / name for name in DOC_FILES if name.endswith(".json")]
    parsed: dict[str, Any] = {}
    for path in json_assets:
        try:
            parsed[path.name] = load(path)
        except (OSError, json.JSONDecodeError) as exc:
            failures.append(f"JSON parse failed: {path.name}: {exc}")

    contract = parsed.get("phase_contract.json", {})
    required_false = {
        "runtime_execution", "provider_invocation", "model_call", "database_write", "vector_store_write",
        "embedding_execution", "scheduler_execution", "device_control", "field_state_mutation", "context_mutation",
        "intent_mutation", "decision_mutation", "task_mutation", "action_execution", "memory_mutation",
        "learning_execution", "self_mutation", "personality_mutation", "dynamic_regulation_mutation",
        "emotion_engine_execution", "b_route_execution", "semantic_compression_execution", "cross_user_transfer", "real_side_effect",
    }
    check(contract.get("owner") == "Outcome Evaluation Governance", "canonical narrow owner", failures)
    check(contract.get("synthetic_only") is True and contract.get("candidate_only") is True, "synthetic/candidate boundary", failures)
    check(all(contract.get(key) is False for key in required_false), "execution and mutation guards", failures)
    check(contract.get("stop_status") == "WAITING_FOR_USER_TERMINAL_VERIFICATION", "stop status", failures)

    execution = parsed.get("outcome_evaluation_controlled_execution_contract_v1.json", {})
    check(execution.get("owner") == "Outcome Evaluation Governance", "execution owner", failures)
    check(execution.get("runtime_execution") is False and execution.get("candidate_only") is True, "execution contract boundary", failures)
    guards = parsed.get("outcome_evaluation_negative_guards_v1.json", {})
    check(all(value is False for value in guards.get("guards", {}).values()), "documentation negative guards", failures)
    check("Expected Outcome != Actual Result" in guards.get("semantic_inequalities", []), "semantic inequalities", failures)

    mapping = parsed.get("outcome_evaluation_planning_to_code_mapping_v1.json", {})
    check(len(mapping.get("mapping", [])) >= 12, "planning to code mapping", failures)
    check("Prediction Engine" in mapping.get("not_implemented", []), "prediction deferred", failures)

    manifest = parsed.get("outcome_evaluation_controlled_change_manifest_v1.json", {})
    check(manifest.get("modified_existing_files") == [], "existing owners unchanged", failures)
    check(len(manifest.get("scenario_ids", [])) == 36, "manifest scenario count", failures)

    fixture_text = (CODE_DIR / "outcome_evaluation_fixture_v1.py").read_text(encoding="utf-8")
    for scenario_id in [f"O{i:02d}" for i in range(1, 37)]:
        check(f'"{scenario_id}"' in fixture_text, f"fixture coverage {scenario_id}", failures)
    runner_text = (CODE_DIR / "run_outcome_evaluation_controlled_implementation_v1.py").read_text(encoding="utf-8")
    check("Path(__file__).resolve()" in runner_text and "sys.path.insert(0, str(REPO_ROOT))" in runner_text, "cwd-independent runner bootstrap", failures)

    if OUTPUT_DIR.is_dir():
        artifact_names = {
            "outcome_evaluation_result_v1.json",
            "outcome_evaluation_case_results_v1.json",
            "outcome_evaluation_trace_v1.json",
        }
        check({item.name for item in OUTPUT_DIR.iterdir() if item.is_file()} >= artifact_names, "runner artifacts exist", failures)
        try:
            result = load(OUTPUT_DIR / "outcome_evaluation_result_v1.json")
            cases = load(OUTPUT_DIR / "outcome_evaluation_case_results_v1.json")
            trace = load(OUTPUT_DIR / "outcome_evaluation_trace_v1.json")
            check(result.get("scenario_count") == 36, "runner scenario count", failures)
            check(result.get("all_cases_passed") is True, "all controlled scenarios passed", failures)
            check(len(cases) == 36 and {item.get("scenario_id") for item in cases} == {f"O{i:02d}" for i in range(1, 37)}, "runner scenario coverage", failures)
            check(all(item.get("all_checks_passed") is True for item in cases), "case checks pass", failures)
            check(len(trace) == 36, "trace scenario coverage", failures)
        except (OSError, json.JSONDecodeError) as exc:
            failures.append(f"runner artifact parse failed: {exc}")
    else:
        failures.append("runner artifacts missing; execute user-terminal Runner before Verifier")

    result = {"passed_check_count": 0 if failures else 1, "failed_check_count": len(failures), "blocker_count": len(failures), "failures": failures}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
