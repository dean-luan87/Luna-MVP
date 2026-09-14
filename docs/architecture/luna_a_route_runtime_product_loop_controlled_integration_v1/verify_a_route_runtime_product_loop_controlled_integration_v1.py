"""Static and artifact verifier for the controlled A Route product loop.

Run this only from the user terminal after the controlled Runner. The verifier
parses assets and reads generated JSON artifacts; it does not execute Luna
owners, providers, models, devices, or runtime code.
"""

from __future__ import annotations

import ast
import json
from pathlib import Path


CODE_FILES = {
    "__init__.py",
    "a_route_product_loop_integration_core_types_v1.py",
    "a_route_product_loop_integration_error_types_v1.py",
    "a_route_product_loop_integration_ownership_guard_v1.py",
    "a_route_product_loop_integration_engine_v1.py",
    "a_route_product_loop_integration_fixture_v1.py",
    "run_a_route_runtime_product_loop_controlled_integration_v1.py",
}
DOC_FILES = {
    "a_route_runtime_product_loop_controlled_integration_overview_v1.md",
    "a_route_runtime_product_loop_controlled_execution_contract_v1.json",
    "a_route_runtime_product_loop_owner_reuse_mapping_v1.json",
    "a_route_runtime_product_loop_state_contract_v1.json",
    "a_route_runtime_product_loop_handoff_mapping_v1.json",
    "a_route_runtime_product_loop_runtime_admission_contract_v1.json",
    "a_route_runtime_product_loop_feedback_routing_contract_v1.json",
    "a_route_runtime_product_loop_session_continuity_contract_v1.json",
    "a_route_runtime_product_loop_product_output_contract_v1.json",
    "a_route_runtime_product_loop_trace_provenance_contract_v1.json",
    "a_route_runtime_product_loop_idempotency_loop_guards_v1.json",
    "a_route_runtime_product_loop_negative_guards_v1.json",
    "a_route_runtime_product_loop_scenario_mapping_v1.json",
    "a_route_runtime_product_loop_change_manifest_v1.json",
    "a_route_runtime_product_loop_implementation_summary_v1.md",
    "phase_contract.json",
    "verify_a_route_runtime_product_loop_controlled_integration_v1.py",
}
L40_CHAIN = (
    "INPUT", "OBSERVATION_REQUIRED", "OBSERVING", "OBSERVATION_READY", "WORLD_CONTEXT_READY",
    "COGNITION_READY", "DECISION_READY", "TASK_READY", "ACTION_READY", "EXECUTION_PENDING",
    "EXECUTING", "RESULT_READY", "EVALUATING", "FEEDBACK", "COMPLETED",
)
PARALLEL_OWNER_DIRECTORY_NAMES = {
    "product_loop_governance",
    "a_route_runtime_governance",
    "runtime_brain",
    "cognitive_brain_governance",
    "product_orchestration_governance",
}


def repo_root_from(path: Path) -> Path:
    for candidate in (path.resolve(), *path.resolve().parents):
        if all((candidate / marker).exists() for marker in ("capabilities", "docs", "README.md")):
            return candidate
    raise RuntimeError("repository root sentinel not found")


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def main() -> int:
    failures: list[str] = []
    root = repo_root_from(Path(__file__).resolve())
    code_dir = root / "capabilities/midplatform/core/a_route_orchestration/integration"
    doc_dir = root / "docs/architecture/luna_a_route_runtime_product_loop_controlled_integration_v1"
    eval_dir = root / "_eval_out/a_route_runtime_product_loop_controlled_integration_v1"

    actual_code = {path.name for path in code_dir.iterdir() if path.is_file() and path.suffix == ".py"}
    require(actual_code == CODE_FILES, "exact implementation file set mismatch", failures)
    actual_docs = {path.name for path in doc_dir.iterdir() if path.is_file()}
    require(actual_docs == DOC_FILES, "exact documentation file set mismatch", failures)

    for path in sorted(code_dir.glob("*.py")):
        try:
            ast.parse(path.read_text(encoding="utf-8"))
        except (OSError, SyntaxError) as exc:
            failures.append(f"AST parse failed: {path.name}: {exc}")
    json_assets = [path for path in doc_dir.glob("*.json")]
    for path in json_assets:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            failures.append(f"JSON parse failed: {path.name}: {exc}")

    contract = json.loads((doc_dir / "phase_contract.json").read_text(encoding="utf-8"))
    for key in (
        "controlled_only", "synthetic_only", "real_runtime_execution", "provider_invocation", "model_call",
        "camera_execution", "ocr_execution", "slam_execution", "audio_execution", "database_write",
        "vector_store_write", "embedding_execution", "scheduler_execution", "device_control",
        "source_owner_mutation", "field_state_direct_mutation", "context_direct_mutation", "intent_mutation",
        "decision_mutation", "task_external_mutation", "memory_mutation", "learning_execution",
        "self_mutation", "personality_mutation", "emotion_engine_execution", "b_route_execution",
        "semantic_compression_execution", "cross_user_transfer", "real_side_effect", "persistence_execution",
        "user_delivery_executed",
    ):
        expected = True if key in {"controlled_only", "synthetic_only"} else False
        require(contract.get(key) is expected, f"phase guard mismatch: {key}", failures)

    owner = json.loads((doc_dir / "a_route_runtime_product_loop_owner_reuse_mapping_v1.json").read_text(encoding="utf-8"))
    change_manifest = json.loads((doc_dir / "a_route_runtime_product_loop_change_manifest_v1.json").read_text(encoding="utf-8"))
    require(owner.get("canonical_owner") == "A Route Orchestration Governance", "canonical owner mismatch", failures)
    parallel_owner_matches = tuple(
        path for base in (root / "capabilities/midplatform/core", root / "docs/architecture")
        for path in base.rglob("*")
        if path.is_dir() and path.name in PARALLEL_OWNER_DIRECTORY_NAMES
    )
    require(not parallel_owner_matches, "parallel semantic owner created", failures)
    require(change_manifest.get("new_semantic_owner") is False, "parallel semantic owner declared", failures)
    require(owner.get("existing_owner_files_modified") is False, "existing owner modification declared", failures)

    state = json.loads((doc_dir / "a_route_runtime_product_loop_state_contract_v1.json").read_text(encoding="utf-8"))
    for required_state in ("IDLE", "INPUT_RECEIVED", "OBSERVATION_REQUIRED", "OBSERVATION_READY", "WORLD_CONTEXT_READY", "COGNITION_READY", "DECISION_READY", "TASK_READY", "ACTION_READY", "EXECUTION_PENDING", "RESULT_READY", "EVALUATING", "REOBSERVATION_REQUIRED", "RECONSIDERING", "NEXT_CYCLE_READY", "COMPLETED", "DEFERRED", "FAILED", "ABORTED"):
        require(required_state in state.get("states", []), f"missing state: {required_state}", failures)

    scenario_map = json.loads((doc_dir / "a_route_runtime_product_loop_scenario_mapping_v1.json").read_text(encoding="utf-8"))
    require(set(scenario_map.get("scenario_ids", [])) == {f"L{i:02d}" for i in range(1, 41)}, "L01-L40 mapping mismatch", failures)
    require(tuple(scenario_map.get("L40_chain", ())) == L40_CHAIN, "L40 chain mapping mismatch", failures)

    negative = json.loads((doc_dir / "a_route_runtime_product_loop_negative_guards_v1.json").read_text(encoding="utf-8"))
    require(all(value is False for value in negative.get("guards", {}).values()), "negative guard is not false", failures)

    forbidden_source_tokens = ("subprocess", "os.system", "sqlite", "requests.", "cv2.", "pytesseract", "torch.")
    for path in code_dir.glob("*.py"):
        source = path.read_text(encoding="utf-8")
        for token in forbidden_source_tokens:
            require(token not in source, f"forbidden runtime token in {path.name}: {token}", failures)

    artifacts = {
        "summary": eval_dir / "a_route_runtime_product_loop_result_v1.json",
        "cases": eval_dir / "a_route_runtime_product_loop_case_results_v1.json",
        "trace": eval_dir / "a_route_runtime_product_loop_trace_v1.json",
    }
    require(all(path.exists() for path in artifacts.values()), "runner artifacts missing", failures)
    if all(path.exists() for path in artifacts.values()):
        summary = json.loads(artifacts["summary"].read_text(encoding="utf-8"))
        cases = json.loads(artifacts["cases"].read_text(encoding="utf-8"))
        trace = json.loads(artifacts["trace"].read_text(encoding="utf-8"))
        require(summary.get("scenario_count") == 40, "runner scenario count mismatch", failures)
        require(summary.get("all_cases_passed") is True, "controlled scenarios did not all pass", failures)
        require(summary.get("failed_case_ids") == [], "runner reports failed cases", failures)
        require({item.get("scenario_id") for item in cases} == {f"L{i:02d}" for i in range(1, 41)}, "runner case coverage mismatch", failures)
        require(all(item.get("all_checks_passed") is True for item in cases), "case checks did not all pass", failures)
        l40 = next((item for item in cases if item.get("scenario_id") == "L40"), {})
        l40_stages = tuple(l40.get("actual", {}).get("stage_ids", ()))
        require(all(stage in l40_stages for stage in L40_CHAIN), "L40 full-chain behavior missing", failures)
        require(len(trace) == 40, "trace artifact coverage mismatch", failures)
        require(all(item.get("provenance_grants_authority") is False for item in trace), "trace authority boundary violated", failures)

    print(f"FAILED_CHECK_COUNT={len(failures)}")
    for failure in failures:
        print(f"FAIL={failure}")
    print(f"BLOCKER_COUNT={len(failures)}")
    print(f"CONTROLLED_INTEGRATION_STATUS={'PASS' if not failures else 'FAIL'}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
