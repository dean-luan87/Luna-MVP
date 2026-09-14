"""Static verifier for the S0 Golden Synthetic Product Loop freeze.

This file is for user-terminal execution. It parses freeze assets and reads
prior evidence; it does not run prior code, runners, providers, or models.
"""

from __future__ import annotations

import ast
import json
from pathlib import Path


JSON_FILES = {
    "a_route_golden_synthetic_baseline_manifest_v1.json",
    "a_route_golden_synthetic_scenario_baseline_v1.json",
    "a_route_golden_synthetic_state_machine_freeze_v1.json",
    "a_route_golden_synthetic_trace_spine_freeze_v1.json",
    "a_route_golden_synthetic_negative_guards_freeze_v1.json",
    "a_route_golden_synthetic_provider_autonomy_freeze_v1.json",
    "a_route_synthetic_to_real_replacement_policy_v1.json",
    "a_route_synthetic_to_real_sequence_v1.json",
    "a_route_differential_validation_policy_v1.json",
    "a_route_golden_synthetic_deferred_registry_v1.json",
    "phase_contract.json",
}
EXPECTED_FILES = JSON_FILES | {
    "a_route_golden_synthetic_closure_summary_v1.md",
    "verify_a_route_golden_synthetic_product_loop_baseline_freeze_v1.py",
}
SCENARIOS = {f"L{i:02d}" for i in range(1, 41)}
STATES = {
    "IDLE", "INPUT_RECEIVED", "OBSERVATION_REQUIRED", "OBSERVING", "OBSERVATION_READY",
    "WORLD_CONTEXT_READY", "COGNITION_READY", "DECISION_READY", "TASK_READY", "ACTION_READY",
    "EXECUTION_PENDING", "EXECUTING", "RESULT_READY", "EVALUATING", "REOBSERVATION_REQUIRED",
    "RECONSIDERING", "NEXT_CYCLE_READY", "COMPLETED", "DEFERRED", "FAILED", "ABORTED",
}
NEGATIVE_GUARDS = {
    "real_runtime_execution", "provider_invocation", "model_call", "camera_execution", "ocr_execution",
    "slam_execution", "audio_execution", "database_write", "vector_store_write", "embedding_execution",
    "scheduler_execution", "device_control", "source_owner_mutation", "field_state_direct_mutation",
    "context_direct_mutation", "intent_mutation", "decision_mutation", "memory_mutation", "learning_mutation",
    "learning_execution", "self_mutation", "personality_mutation", "emotion_engine_execution", "b_route_execution",
    "semantic_compression_execution", "cross_user_transfer", "real_side_effect",
}


def repo_root_from(path: Path) -> Path:
    for candidate in (path.resolve(), *path.resolve().parents):
        if all((candidate / marker).exists() for marker in ("capabilities", "docs", "README.md")):
            return candidate
    raise RuntimeError("repository root sentinel not found")


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def main() -> int:
    failures: list[str] = []
    root = repo_root_from(Path(__file__).resolve())
    freeze_dir = root / "docs/architecture/luna_a_route_golden_synthetic_product_loop_baseline_freeze_v1"
    actual_files = {path.name for path in freeze_dir.iterdir() if path.is_file()}
    require(actual_files == EXPECTED_FILES, "exact freeze file set mismatch", failures)

    assets: dict[str, object] = {}
    for name in sorted(JSON_FILES):
        path = freeze_dir / name
        require(path.exists(), f"missing freeze asset: {name}", failures)
        if path.exists():
            try:
                assets[name] = load(path)
            except (OSError, json.JSONDecodeError) as exc:
                failures.append(f"invalid JSON {name}: {exc}")

    verifier_path = freeze_dir / "verify_a_route_golden_synthetic_product_loop_baseline_freeze_v1.py"
    try:
        ast.parse(verifier_path.read_text(encoding="utf-8"))
    except (OSError, SyntaxError) as exc:
        failures.append(f"verifier AST parse failed: {exc}")

    manifest = assets.get("a_route_golden_synthetic_baseline_manifest_v1.json", {})
    require(manifest.get("freeze_id") == "S0_GOLDEN_SYNTHETIC_BASELINE", "S0 freeze id missing", failures)
    require(manifest.get("freeze_status") == "FROZEN_V1", "freeze status missing", failures)
    require(manifest.get("canonical_loop_caller") == "A Route Orchestration Governance", "canonical owner mismatch", failures)
    evidence = manifest.get("required_evidence", {})
    for key, expected in (("scenario_count", 40), ("all_cases_passed", True), ("failed_case_ids", []), ("failed_check_count", 0), ("blocker_count", 0), ("controlled_integration_status", "PASS")):
        require(evidence.get(key) == expected, f"baseline evidence mismatch: {key}", failures)
    for ref_key in ("runner_evidence_ref", "case_evidence_ref", "trace_evidence_ref", "prior_verifier_ref"):
        require(Path(root / manifest.get(ref_key, "")).exists(), f"evidence reference missing: {ref_key}", failures)

    scenarios = assets.get("a_route_golden_synthetic_scenario_baseline_v1.json", {})
    require(scenarios.get("scenario_count") == 40, "scenario count is not 40", failures)
    require(set(scenarios.get("scenario_ids", [])) == SCENARIOS, "L01-L40 baseline coverage mismatch", failures)
    require(scenarios.get("all_scenarios_status") == "PASS", "scenario baseline is not PASS", failures)
    require(scenarios.get("L40_classification") == "FULL_SYNTHETIC_PRODUCT_LOOP_GOLDEN_PATH", "L40 golden classification missing", failures)
    require(scenarios.get("L40_preconstructed_terminal_result") is False, "L40 must not be preconstructed", failures)

    state = assets.get("a_route_golden_synthetic_state_machine_freeze_v1.json", {})
    require(set(state.get("states", [])) == STATES, "state vocabulary mismatch", failures)
    require(state.get("redesign_allowed_during_replacement") is False, "state redesign not frozen", failures)

    trace = assets.get("a_route_golden_synthetic_trace_spine_freeze_v1.json", {})
    require(trace.get("provenance_grants_authority") is False, "trace authority guard mismatch", failures)
    require(len(trace.get("reverse_trace", [])) == 12, "trace spine coverage mismatch", failures)

    provider = assets.get("a_route_golden_synthetic_provider_autonomy_freeze_v1.json", {})
    require(provider.get("provider_autonomous_continuous_execution") is False, "provider autonomy guard mismatch", failures)
    require(len(provider.get("required_control_chain", [])) == 8, "provider control chain incomplete", failures)

    replacement = assets.get("a_route_synthetic_to_real_replacement_policy_v1.json", {})
    differential_policy = assets.get("a_route_differential_validation_policy_v1.json", {})
    require(replacement.get("synthetic_adapters_permanent") is True, "synthetic adapter retention missing", failures)
    require(replacement.get("one_major_component_per_phase") is True, "single replacement rule missing", failures)
    require(
        differential_policy.get("differential_compare_fields") == [
            "contract outputs",
            "trace/provenance",
            "state transitions",
            "negative guards",
            "unrelated module behavior",
        ],
        "differential fields missing",
        failures,
    )

    sequence = assets.get("a_route_synthetic_to_real_sequence_v1.json", {})
    require([item.get("step") for item in sequence.get("default_sequence", [])] == [f"S{i}" for i in range(13)], "S0-S12 sequence mismatch", failures)
    require(sequence.get("architecture_law") is False, "replacement order incorrectly frozen as architecture law", failures)

    guards = assets.get("a_route_golden_synthetic_negative_guards_freeze_v1.json", {})
    require(set(guards.get("guards", {})) == NEGATIVE_GUARDS, "negative guard key set mismatch", failures)
    require(all(value is False for value in guards.get("guards", {}).values()), "negative guard is not false", failures)
    require(guards.get("synthetic_only") is True, "synthetic-only guard missing", failures)
    require(guards.get("controlled_integration_only") is True, "controlled-only guard missing", failures)

    deferred = assets.get("a_route_golden_synthetic_deferred_registry_v1.json", {})
    deferred_names = {item.get("name") for item in deferred.get("deferred", [])}
    for name in ("Emotion Engine", "Advanced Emotion Governance runtime", "B Route", "semantic compression", "affective memory compression", "emotion-memory summary generation", "personality-memory fusion", "cross-user transfer", "online model training", "automatic personality activation"):
        require(name in deferred_names, f"deferred workstream missing: {name}", failures)

    contract = assets.get("phase_contract.json", {})
    for key, expected in (("freeze_only", True), ("implementation_change", False), ("planning_asset_change", False), ("fixture_change", False), ("runner_change", False), ("prior_verifier_change", False), ("runtime_execution", False), ("provider_invocation", False), ("model_call", False), ("real_side_effect", False)):
        require(contract.get(key) == expected, f"freeze contract mismatch: {key}", failures)

    print(f"FAILED_CHECK_COUNT={len(failures)}")
    for failure in failures:
        print(f"FAIL={failure}")
    print(f"BLOCKER_COUNT={len(failures)}")
    print(f"FREEZE_STATUS={'FROZEN_V1' if not failures else 'FREEZE_BLOCKED'}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
