"""Static verifier for the A Route Cognitive Brain audit package.

This verifier parses audit assets and checks declarations only. It does not
import or execute any existing capability, runner, provider, model, or runtime.
"""

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
PHASE_DIR = REPO_ROOT / "docs/architecture/luna_a_route_cognitive_brain_computational_runtime_loop_audit_v1"

REQUIRED_FILES = {
    "cognitive_brain_computational_audit_v1.md",
    "cognitive_brain_module_inventory_v1.json",
    "cognitive_brain_maturity_matrix_v1.json",
    "cognitive_brain_algorithm_inventory_v1.json",
    "cognitive_brain_mathematical_object_registry_v1.json",
    "cognitive_brain_runtime_handoff_matrix_v1.json",
    "cognitive_brain_attention_audit_v1.json",
    "cognitive_brain_hypothesis_expectation_prediction_audit_v1.json",
    "cognitive_brain_state_vector_audit_v1.json",
    "cognitive_brain_dynamic_function_audit_v1.json",
    "cognitive_brain_dynamic_regulation_audit_v1.json",
    "cognitive_brain_parameter_genome_audit_v1.json",
    "cognitive_brain_decision_algorithm_audit_v1.json",
    "cognitive_brain_result_comparison_error_audit_v1.json",
    "cognitive_brain_learning_boundary_audit_v1.json",
    "cognitive_brain_p0_p1_p2_gap_registry_v1.json",
    "cognitive_brain_owner_reuse_matrix_v1.json",
    "cognitive_brain_future_build_sequence_v1.json",
    "cognitive_brain_deferred_registry_v1.json",
    "phase_contract.json",
    "verify_cognitive_brain_computational_runtime_loop_audit_v1.py",
}

JSON_FILES = {name for name in REQUIRED_FILES if name.endswith(".json")}
LEVELS = {
    "M0_MISSING",
    "M1_CONCEPT_ONLY",
    "M2_SCHEMA_OR_TYPES",
    "M3_GOVERNANCE_CONTRACT",
    "M4_CONTROLLED_SKELETON",
    "M5_DETERMINISTIC_CONTROLLED_ALGORITHM",
    "M6_COMPUTABLE_MODEL_NOT_RUNTIME_INTEGRATED",
    "M7_CONTROLLED_RUNTIME_INTEGRATED",
    "M8_REAL_RUNTIME_INTEGRATED",
    "M9_REAL_DATA_VALIDATED",
}
HANDOFF_STATUS = {
    "CONTRACT_ONLY",
    "ADAPTER_EXISTS",
    "CONTROLLED_HANDOFF",
    "COMPUTABLE",
    "RUNTIME_CONNECTED",
    "REAL_DATA_PROVEN",
    "MISSING",
}
ALGORITHM_CLASSES = {
    "RULE_BASED",
    "STATE_MACHINE",
    "WEIGHTED_SCORE",
    "HEURISTIC",
    "PROBABILISTIC",
    "OPTIMIZATION",
    "GRAPH",
    "VECTOR_DYNAMICS",
    "LEARNED_MODEL",
    "DETERMINISTIC_PLACEHOLDER",
    "UNKNOWN",
}


def load(name: str) -> Any:
    return json.loads((PHASE_DIR / name).read_text(encoding="utf-8"))


def check(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def main() -> int:
    failures: list[str] = []
    actual_files = {item.name for item in PHASE_DIR.iterdir() if item.is_file()}
    check(actual_files == REQUIRED_FILES, "exact required audit file set", failures)

    assets: dict[str, Any] = {}
    for name in JSON_FILES:
        try:
            assets[name] = load(name)
        except (OSError, json.JSONDecodeError) as exc:
            failures.append(f"invalid JSON {name}: {exc}")

    try:
        ast.parse((PHASE_DIR / "verify_cognitive_brain_computational_runtime_loop_audit_v1.py").read_text(encoding="utf-8"))
    except (OSError, SyntaxError) as exc:
        failures.append(f"verifier AST parse: {exc}")

    contract = assets.get("phase_contract.json", {})
    required_false = {
        "implementation_allowed", "runtime_execution", "model_call", "provider_invocation",
        "database_write", "vector_store_write", "scheduler_execution", "device_control",
        "source_owner_mutation", "field_state_mutation", "context_mutation", "intent_mutation",
        "attention_mutation", "hypothesis_mutation", "cognitive_state_mutation",
        "regulation_parameter_mutation", "parameter_genome_activation", "decision_execution",
        "task_mutation", "action_execution", "learning_execution", "memory_mutation",
        "self_mutation", "personality_mutation", "emotion_engine_execution", "b_route_execution",
        "semantic_compression_execution", "real_side_effect",
    }
    check(contract.get("audit_only") is True, "audit_only", failures)
    check(contract.get("planning_only") is True, "planning_only", failures)
    check(all(contract.get(key) is False for key in required_false), "all audit mutation/runtime guards false", failures)
    check(contract.get("stop_status") == "WAITING_FOR_USER_TERMINAL_VERIFICATION", "stop status", failures)

    inventory = assets.get("cognitive_brain_module_inventory_v1.json", {})
    modules = inventory.get("modules", [])
    expected_ids = set("ABCDEFGHIJ KLMNOPQRSTUVWXYZ".replace(" ", "")) | {"AA", "AB"}
    check({item.get("id") for item in modules} == expected_ids, "A-Z plus AA/AB mechanism coverage", failures)
    check(all(item.get("maturity") in LEVELS for item in modules), "module maturity values", failures)
    check(all(item.get("evidence_refs") for item in modules), "module evidence refs", failures)

    maturity = assets.get("cognitive_brain_maturity_matrix_v1.json", {})
    entries = maturity.get("entries", [])
    check({item.get("id") for item in entries} == expected_ids, "maturity matrix coverage", failures)
    check(all(item.get("primary") in LEVELS for item in entries), "maturity matrix levels", failures)
    check(all(maturity.get("distribution", {}).get(level, 0) >= 0 for level in LEVELS), "maturity distribution", failures)

    algorithms = assets.get("cognitive_brain_algorithm_inventory_v1.json", {}).get("algorithms", [])
    required_algorithm_fields = {"algorithm_id", "name", "owner", "location", "purpose", "inputs", "outputs", "mathematical_form", "algorithm_class", "parameters", "parameter_source", "stateful", "temporal", "uncertainty_support", "runtime_called", "real_data_tested", "maturity", "evidence_refs", "known_limitations"}
    check(bool(algorithms), "algorithm inventory nonempty", failures)
    check(all(required_algorithm_fields <= set(item) for item in algorithms), "algorithm inventory fields", failures)
    check(all(item.get("algorithm_class") in ALGORITHM_CLASSES for item in algorithms), "algorithm classes", failures)
    check(all(item.get("maturity") in LEVELS for item in algorithms), "algorithm maturity", failures)
    check(all(item.get("runtime_called") is False and item.get("real_data_tested") is False for item in algorithms), "algorithm runtime/data evidence boundary", failures)

    objects = assets.get("cognitive_brain_mathematical_object_registry_v1.json", {}).get("objects", [])
    allowed_object_types = {"scalar", "vector", "tensor", "graph", "distribution", "set", "ordered_set", "state_machine", "transition_system", "function", "utility_function", "cost_function", "probability", "confidence_interval", "constraint_set", "optimization_problem"}
    object_fields = {"object_id", "name", "owner", "object_type", "dimensions", "domain", "range", "units", "normalization", "update_function", "parameter_refs", "uncertainty_representation", "temporal_semantics", "runtime_status", "evidence_refs"}
    check(all(object_fields <= set(item) for item in objects), "mathematical object fields", failures)
    check(all(item.get("object_type") in allowed_object_types for item in objects), "mathematical object types", failures)
    check(all(item.get("runtime_status") != "REAL_DATA_VALIDATED" for item in objects), "no fabricated real-data mathematical object", failures)

    handoffs = assets.get("cognitive_brain_runtime_handoff_matrix_v1.json", {}).get("handoffs", [])
    check(len(handoffs) >= 10, "runtime handoff coverage", failures)
    check(all(item.get("status") in HANDOFF_STATUS for item in handoffs), "handoff statuses", failures)
    check(any(item.get("from") == "Result" and item.get("to") == "Comparison/Error" for item in handoffs), "result comparison arrow", failures)
    check(any(item.get("from") == "Comparison/Error" and item.get("to") == "Learning Signal" for item in handoffs), "error learning arrow", failures)
    check(not any(item.get("runtime_connected") == "yes" or item.get("real_data_proven") == "yes" for item in handoffs), "no runtime/real-data claim", failures)

    for name in {
        "cognitive_brain_attention_audit_v1.json",
        "cognitive_brain_hypothesis_expectation_prediction_audit_v1.json",
        "cognitive_brain_state_vector_audit_v1.json",
        "cognitive_brain_dynamic_function_audit_v1.json",
        "cognitive_brain_dynamic_regulation_audit_v1.json",
        "cognitive_brain_parameter_genome_audit_v1.json",
        "cognitive_brain_decision_algorithm_audit_v1.json",
        "cognitive_brain_result_comparison_error_audit_v1.json",
        "cognitive_brain_learning_boundary_audit_v1.json",
    }:
        check(isinstance(assets.get(name), dict), f"specialized audit present: {name}", failures)

    gaps = assets.get("cognitive_brain_p0_p1_p2_gap_registry_v1.json", {}).get("gaps", [])
    check(bool(gaps), "genuine gap registry", failures)
    check(all(item.get("priority") in {"P0", "P1", "P2"} for item in gaps), "gap priorities", failures)
    check(any(item.get("priority") == "P0" and "Result Comparison" in item.get("capability", "") for item in gaps), "P0 result comparison gap", failures)

    owner = assets.get("cognitive_brain_owner_reuse_matrix_v1.json", {})
    check(owner.get("owner_decision"), "owner reuse decision", failures)
    check(not any("new cognitive owner" in str(item).lower() and "create" in str(item).lower() for item in owner.get("decisions", [])), "no parallel cognitive owner", failures)

    future = assets.get("cognitive_brain_future_build_sequence_v1.json", {})
    check(len(future.get("sequence", [])) >= 4, "future module sequence", failures)
    deferred = assets.get("cognitive_brain_deferred_registry_v1.json", {})
    deferred_text = json.dumps(deferred, ensure_ascii=False).lower()
    for token in ("emotion", "b route", "semantic compression"):
        check(token in deferred_text, f"deferred boundary: {token}", failures)

    result = {"passed_check_count": 0 if failures else 1, "failed_check_count": len(failures), "blocker_count": len(failures), "failures": failures}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
