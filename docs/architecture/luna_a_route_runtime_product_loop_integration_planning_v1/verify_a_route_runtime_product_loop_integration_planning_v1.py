"""Static verifier for A Route runtime product-loop planning.

This verifier is intended for user-terminal execution. It only parses planning
assets and checks declared planning boundaries; it does not execute any Luna
runtime, provider, model, or prior-phase runner.
"""

from __future__ import annotations

import ast
import json
from pathlib import Path


REQUIRED_JSON = {
    "a_route_runtime_product_loop_existing_asset_inventory_v1.json",
    "a_route_runtime_product_loop_maturity_matrix_v1.json",
    "a_route_runtime_product_loop_owner_decision_v1.json",
    "a_route_runtime_product_loop_state_model_v1.json",
    "a_route_runtime_product_loop_handoff_matrix_v1.json",
    "a_route_runtime_product_loop_runtime_boundary_v1.json",
    "a_route_runtime_product_loop_feedback_control_v1.json",
    "a_route_runtime_product_loop_observation_reentry_v1.json",
    "a_route_runtime_product_loop_reconsideration_v1.json",
    "a_route_runtime_product_loop_execution_result_contract_v1.json",
    "a_route_runtime_product_loop_persistence_continuity_audit_v1.json",
    "a_route_runtime_product_loop_user_input_output_audit_v1.json",
    "a_route_runtime_product_loop_error_namespace_matrix_v1.json",
    "a_route_runtime_product_loop_trace_provenance_contract_v1.json",
    "a_route_runtime_product_loop_idempotency_contract_v1.json",
    "a_route_runtime_product_loop_negative_guards_v1.json",
    "a_route_runtime_product_loop_gap_registry_v1.json",
    "a_route_runtime_product_loop_deferred_registry_v1.json",
    "a_route_runtime_product_loop_minimum_scenario_suite_v1.json",
    "a_route_runtime_product_loop_implementation_sequence_v1.json",
    "phase_contract.json",
}


def repo_root_from(path: Path) -> Path:
    for candidate in (path, *path.parents):
        if all((candidate / marker).exists() for marker in ("capabilities", "docs", "README.md")):
            return candidate
    raise RuntimeError("repository root sentinel not found")


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def main() -> int:
    failures: list[str] = []
    root = repo_root_from(Path(__file__).resolve())
    directory = root / "docs/architecture/luna_a_route_runtime_product_loop_integration_planning_v1"
    actual = {path.name for path in directory.iterdir() if path.is_file()}
    expected = set(REQUIRED_JSON) | {
        "a_route_runtime_product_loop_architecture_plan_v1.md",
        "verify_a_route_runtime_product_loop_integration_planning_v1.py",
    }
    require(actual == expected, "exact planning file set mismatch", failures)

    parsed: dict[str, object] = {}
    for name in sorted(REQUIRED_JSON):
        path = directory / name
        require(path.exists(), f"missing required file: {name}", failures)
        if path.exists():
            try:
                parsed[name] = load_json(path)
            except (OSError, json.JSONDecodeError) as exc:
                failures.append(f"invalid JSON {name}: {exc}")

    verifier_path = directory / "verify_a_route_runtime_product_loop_integration_planning_v1.py"
    try:
        ast.parse(verifier_path.read_text(encoding="utf-8"))
    except (OSError, SyntaxError) as exc:
        failures.append(f"verifier AST parse failed: {exc}")

    contract = parsed.get("phase_contract.json", {})
    require(contract.get("audit_only") is True, "audit_only must be true", failures)
    require(contract.get("planning_only") is True, "planning_only must be true", failures)
    for key in (
        "implementation_allowed", "runtime_execution", "model_call", "provider_invocation",
        "database_write", "vector_store_write", "scheduler_execution", "device_control",
        "source_owner_mutation", "field_state_mutation", "context_mutation", "intent_mutation",
        "attention_mutation", "hypothesis_mutation", "cognitive_state_mutation",
        "regulation_parameter_mutation", "parameter_genome_activation", "decision_execution",
        "task_mutation", "action_execution", "learning_execution", "memory_mutation",
        "self_mutation", "personality_mutation", "emotion_engine_execution", "b_route_execution",
        "semantic_compression_execution", "real_side_effect",
    ):
        require(contract.get(key) is False, f"planning guard is not false: {key}", failures)

    owner = parsed.get("a_route_runtime_product_loop_owner_decision_v1.json", {})
    require(owner.get("decision_class") == "A_EXISTING_CANONICAL_OWNER", "canonical owner decision missing", failures)
    require(owner.get("new_super_owner_required") is False, "new super-owner must remain false", failures)

    maturity = parsed.get("a_route_runtime_product_loop_maturity_matrix_v1.json", {})
    node_ids = {item.get("id") for item in maturity.get("nodes", [])}
    require(node_ids == {f"N{i:02d}" for i in range(1, 13)}, "maturity node coverage mismatch", failures)
    require(maturity.get("distribution", {}).get("M7") == 0, "M7 must not be claimed", failures)
    require(maturity.get("distribution", {}).get("M8") == 0, "M8 must not be claimed", failures)
    require(maturity.get("distribution", {}).get("M9") == 0, "M9 must not be claimed", failures)

    handoffs = parsed.get("a_route_runtime_product_loop_handoff_matrix_v1.json", {}).get("handoffs", [])
    require({item.get("id") for item in handoffs} == {f"H{i:02d}" for i in range(1, 18)}, "H01-H17 coverage mismatch", failures)
    require(all(item.get("runtime_status") == "absent" for item in handoffs), "runtime handoff must remain absent", failures)

    scenarios = parsed.get("a_route_runtime_product_loop_minimum_scenario_suite_v1.json", {})
    require(scenarios.get("scenario_count") == 40, "scenario count must be 40", failures)
    require({item.get("id") for item in scenarios.get("scenarios", [])} == {f"L{i:02d}" for i in range(1, 41)}, "L01-L40 coverage mismatch", failures)

    guards = parsed.get("a_route_runtime_product_loop_negative_guards_v1.json", {}).get("guards", {})
    require(all(value is False for value in guards.values()), "negative guards must be false", failures)
    deferred = parsed.get("a_route_runtime_product_loop_deferred_registry_v1.json", {}).get("deferred", [])
    deferred_text = json.dumps(deferred, ensure_ascii=False)
    for token in ("Emotion Engine", "B Route", "semantic compression", "cross-user transfer"):
        require(token in deferred_text, f"deferred boundary missing: {token}", failures)

    print(f"FAILED_CHECK_COUNT={len(failures)}")
    for failure in failures:
        print(f"FAIL={failure}")
    print(f"PLANNING_STATUS={'PASS' if not failures else 'FAIL'}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
