"""Static verifier for Result Comparison / Outcome Evaluation planning.

It parses planning declarations only. It does not import or execute existing
capabilities, runners, verifiers, providers, models, or runtime code.
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
PHASE_DIR = REPO_ROOT / "docs/architecture/luna_a_route_result_comparison_outcome_evaluation_architecture_planning_v1"

REQUIRED_FILES = {
    "result_comparison_outcome_evaluation_architecture_plan_v1.md",
    "existing_asset_inventory_v1.json",
    "owner_decision_v1.json",
    "expected_outcome_input_model_v1.json",
    "actual_result_input_model_v1.json",
    "comparability_gate_v1.json",
    "deviation_model_v1.json",
    "outcome_evaluation_candidate_schema_v1.json",
    "attribution_taxonomy_v1.json",
    "multi_cause_uncertainty_model_v1.json",
    "reconsideration_handoff_v1.json",
    "learning_signal_handoff_v1.json",
    "observation_feedback_handoff_v1.json",
    "temporal_comparison_model_v1.json",
    "correction_revision_model_v1.json",
    "trace_provenance_model_v1.json",
    "idempotency_guards_v1.json",
    "scenario_suite_v1.json",
    "abcd_gap_registry_v1.json",
    "deferred_registry_v1.json",
    "negative_guards_v1.json",
    "phase_contract.json",
    "verify_result_comparison_outcome_evaluation_architecture_planning_v1.py",
}

JSON_FILES = {name for name in REQUIRED_FILES if name.endswith(".json")}


def load(name: str) -> Any:
    return json.loads((PHASE_DIR / name).read_text(encoding="utf-8"))


def check(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def main() -> int:
    failures: list[str] = []
    if not PHASE_DIR.is_dir():
        failures.append("phase directory missing")
        print(json.dumps({"failures": failures}, indent=2))
        return 1

    actual_files = {item.name for item in PHASE_DIR.iterdir() if item.is_file()}
    check(actual_files == REQUIRED_FILES, "exact planning file set", failures)

    assets: dict[str, Any] = {}
    for name in JSON_FILES:
        try:
            assets[name] = load(name)
        except (OSError, json.JSONDecodeError) as exc:
            failures.append(f"invalid JSON {name}: {exc}")

    verifier_path = PHASE_DIR / "verify_result_comparison_outcome_evaluation_architecture_planning_v1.py"
    try:
        ast.parse(verifier_path.read_text(encoding="utf-8"))
    except (OSError, SyntaxError) as exc:
        failures.append(f"verifier AST parse: {exc}")

    contract = assets.get("phase_contract.json", {})
    false_flags = {
        "implementation_allowed", "runtime_execution", "provider_invocation", "model_call",
        "database_write", "vector_store_write", "embedding_execution", "scheduler_execution",
        "device_control", "field_state_mutation", "context_mutation", "intent_mutation",
        "decision_mutation", "task_mutation", "action_execution", "memory_mutation",
        "learning_execution", "self_mutation", "personality_mutation", "emotion_engine_execution",
        "b_route_execution", "semantic_compression_execution", "cross_user_transfer", "real_side_effect",
    }
    check(contract.get("audit_only") is True, "audit_only=true", failures)
    check(contract.get("planning_only") is True, "planning_only=true", failures)
    check(all(contract.get(flag) is False for flag in false_flags), "phase negative execution/mutation guards", failures)
    check(contract.get("stop_status") == "WAITING_FOR_USER_TERMINAL_VERIFICATION", "stop status", failures)

    owner = assets.get("owner_decision_v1.json", {})
    check(owner.get("classification") == "D_NO_CANONICAL_OWNER_FOUND", "owner classification", failures)
    check(owner.get("canonical_owner_exists") is False, "no existing canonical owner", failures)
    check(owner.get("recommended_future_owner") == "Outcome Evaluation Governance", "narrow future owner", failures)
    prohibited = set(owner.get("parallel_super_owner_prohibited", []))
    check({"Cognitive Brain Governance", "Cognitive Feedback Governance", "Intelligence Governance", "Cognitive Supervision Governance"} <= prohibited, "super-owner names remain prohibited", failures)

    inventory = assets.get("existing_asset_inventory_v1.json", {})
    entries = inventory.get("assets", [])
    check(bool(entries), "existing asset inventory", failures)
    check(all(item.get("classification") in {"A", "B", "C", "D"} for item in entries), "A/B/C/D classifications", failures)
    check(any(item.get("classification") == "A" for item in entries), "A reusable assets", failures)
    check(any(item.get("classification") == "B" for item in entries), "B adapter assets", failures)
    check(any(item.get("classification") == "C" for item in entries), "C conflicting assets", failures)
    check(any(item.get("classification") == "D" for item in entries), "D deferred assets", failures)

    expected = assets.get("expected_outcome_input_model_v1.json", {})
    actual = assets.get("actual_result_input_model_v1.json", {})
    check(expected.get("candidate_only") is True and expected.get("truth_declared") is False, "expected candidate boundary", failures)
    check(actual.get("candidate_only") is True and actual.get("truth_declared") is False, "actual candidate boundary", failures)
    check(len(expected.get("inputs", [])) >= 8, "expected input coverage", failures)
    check(len(actual.get("sources", [])) >= 8, "actual source coverage", failures)
    check(all(token in expected.get("non_equivalence", []) for token in ["Declared Expectation != Predicted Outcome", "Predicted Outcome != Task Completion Criterion"]), "expectation distinctions", failures)

    gate = assets.get("comparability_gate_v1.json", {})
    required_gate_states = {"COMPARABLE", "PARTIALLY_COMPARABLE", "NOT_COMPARABLE", "INSUFFICIENT_EVIDENCE", "STALE_ACTUAL", "STALE_EXPECTATION", "CONTESTED", "NEEDS_CONFIRMATION"}
    check(required_gate_states <= set(gate.get("states", [])), "comparability gate states", failures)
    check(len(gate.get("checks", [])) >= 8, "comparability checks", failures)
    check("No deviation calculation" in gate.get("rule", ""), "comparability blocks forced deviation", failures)

    deviation = assets.get("deviation_model_v1.json", {})
    check({"MATCH", "PARTIAL_MATCH", "MISMATCH", "UNKNOWN", "CONTESTED"} <= set(deviation.get("statuses", [])), "deviation statuses", failures)
    check(deviation.get("no_single_score") is True, "no opaque deviation score", failures)

    evaluation = assets.get("outcome_evaluation_candidate_schema_v1.json", {})
    required_eval = {"evaluation_id", "expected_outcome_refs", "actual_result_refs", "comparability_ref", "deviation_refs", "attribution_candidate_refs", "reconsideration_candidate_refs", "learning_signal_candidate_refs", "trace_ref", "provenance_refs"}
    check(required_eval <= set(evaluation.get("required_fields", [])), "evaluation schema fields", failures)
    check(evaluation.get("candidate_only") is True and evaluation.get("truth_declared") is False and evaluation.get("mutation_authority") is False, "evaluation boundary", failures)

    attribution = assets.get("attribution_taxonomy_v1.json", {})
    required_attribution = {"OBSERVATION_ERROR_CANDIDATE", "WORLD_MODEL_ERROR_CANDIDATE", "PREDICTION_ERROR_CANDIDATE", "DECISION_ERROR_CANDIDATE", "TASK_PLANNING_ERROR_CANDIDATE", "EXECUTION_ERROR_CANDIDATE", "CAPABILITY_ERROR_CANDIDATE", "TEMPORAL_VALIDITY_ERROR_CANDIDATE", "STALE_INFORMATION_CANDIDATE", "EXTERNAL_WORLD_CHANGE_CANDIDATE", "USER_CORRECTION_CANDIDATE", "INSUFFICIENT_EVIDENCE", "UNRESOLVED_ATTRIBUTION"}
    check(required_attribution <= set(attribution.get("types", [])), "attribution taxonomy", failures)
    check("multiple causes may coexist" in attribution.get("rules", []), "multi-cause attribution", failures)

    multi = assets.get("multi_cause_uncertainty_model_v1.json", {})
    check(multi.get("single_root_cause_forced") is False, "multi-cause not flattened", failures)
    check(len(multi.get("supports", [])) >= 6, "uncertainty/multi-cause coverage", failures)

    reconsider = assets.get("reconsideration_handoff_v1.json", {})
    check("REOBSERVE" in reconsider.get("recommendations", []) and "RECONSIDER_DECISION" in reconsider.get("recommendations", []), "reconsideration recommendations", failures)
    check(reconsider.get("candidate_only") is True, "reconsideration candidate boundary", failures)
    learning = assets.get("learning_signal_handoff_v1.json", {})
    check(learning.get("candidate_only") is True, "learning handoff candidate boundary", failures)
    check(any("no Learning state mutation" == item for item in learning.get("prohibitions", [])), "learning mutation guard", failures)
    observation = assets.get("observation_feedback_handoff_v1.json", {})
    check("Field Perception Orchestrator" in observation.get("flow", ""), "observation feedback owner", failures)
    check(len(observation.get("provider_boundary", [])) >= 4, "provider autonomy boundary", failures)

    temporal = assets.get("temporal_comparison_model_v1.json", {})
    check(len(temporal.get("temporal_cases", [])) >= 8, "temporal comparison cases", failures)
    check(temporal.get("scheduler_execution") is False, "no scheduler execution", failures)
    correction = assets.get("correction_revision_model_v1.json", {})
    check("never silently overwrite" in correction.get("rules", []), "correction lineage", failures)
    trace = assets.get("trace_provenance_model_v1.json", {})
    check(len(trace.get("reverse_routes", [])) >= 3 and trace.get("provenance_authority") is False, "trace/provenance reverse lookup", failures)
    idem = assets.get("idempotency_guards_v1.json", {})
    check(len(idem.get("guards", [])) >= 9 and idem.get("completed_immutable") is True, "idempotency guards", failures)

    scenarios = assets.get("scenario_suite_v1.json", {})
    scenario_ids = [item.get("id") for item in scenarios.get("scenarios", [])]
    check(scenarios.get("scenario_count") == 36 and scenario_ids == [f"O{i:02d}" for i in range(1, 37)], "O01-O36 scenario coverage", failures)
    check(scenarios.get("synthetic_only") is True, "synthetic scenarios", failures)

    abcd = assets.get("abcd_gap_registry_v1.json", {})
    check(all(item.get("classification") in {"A", "B", "C", "D"} for item in abcd.get("entries", [])), "gap A/B/C/D registry", failures)
    deferred = assets.get("deferred_registry_v1.json", {})
    deferred_text = json.dumps(deferred, ensure_ascii=False).lower()
    for token in ("emotion", "b route", "semantic compression", "affective memory", "personality-memory", "cross-user"):
        check(token in deferred_text, f"deferred registry includes {token}", failures)

    guards = assets.get("negative_guards_v1.json", {})
    check(guards.get("planning_only") is True and guards.get("candidate_only") is True, "negative guard phase flags", failures)
    check(all(value is False for value in guards.get("guards", {}).values()), "negative guards all false", failures)
    semantic = set(guards.get("semantic_guards", []))
    check("comparison_is_not_decision" in semantic and "confidence_is_not_correctness" in semantic, "semantic inequalities", failures)

    result = {"passed_check_count": 0 if failures else 1, "failed_check_count": len(failures), "blocker_count": len(failures), "failures": failures}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
