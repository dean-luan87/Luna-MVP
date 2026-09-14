from __future__ import annotations

import ast
import json
from pathlib import Path


CODE_DIR_REL = "capabilities/midplatform/field_perception_orchestrator/integration"
NEW_CODE_FILES = {
    "raw_camera_stream_types_v1.py",
    "raw_camera_stream_adapter_v1.py",
    "raw_camera_stream_fixture_v1.py",
    "run_a_route_s2_real_raw_camera_input_stream_controlled_replacement_v1.py",
}
DOC_FILES = {
    "s2_existing_asset_inventory_and_reuse_v1.json",
    "s2_controlled_execution_contract_v1.json",
    "s2_raw_frame_boundary_v1.json",
    "s2_bounded_stream_session_contract_v1.json",
    "s2_observation_perception_ingress_mapping_v1.json",
    "s2_differential_validation_contract_v1.json",
    "s2_privacy_raw_data_policy_v1.json",
    "s2_negative_guards_v1.json",
    "s2_scenario_mapping_v1.json",
    "s2_change_manifest_v1.json",
    "s2_implementation_summary_v1.md",
    "phase_contract.json",
    "verify_a_route_s2_real_raw_camera_input_stream_controlled_replacement_v1.py",
}
PARALLEL_OWNER_NAMES = {
    "camera_governance",
    "vision_governance",
    "perception_brain",
    "sensor_intelligence_governance",
}
S2_IDS = {f"S2-{index:02d}" for index in range(1, 25)}


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
    doc_dir = root / "docs/architecture/luna_a_route_s2_real_raw_camera_input_stream_controlled_replacement_v1"
    code_dir = root / CODE_DIR_REL
    eval_dir = root / "_eval_out/a_route_s2_real_raw_camera_input_stream_controlled_replacement_v1"

    actual_docs = {path.name for path in doc_dir.iterdir() if path.is_file()}
    require(actual_docs == DOC_FILES, "S2 documentation file set mismatch", failures)
    for path in sorted(doc_dir.glob("*.json")):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            failures.append(f"JSON parse failed: {path.name}: {exc}")
    for path in sorted(code_dir.glob("*.py")):
        if path.name in NEW_CODE_FILES:
            try:
                ast.parse(path.read_text(encoding="utf-8"))
            except (OSError, SyntaxError) as exc:
                failures.append(f"S2 AST parse failed: {path.name}: {exc}")
    require(all((code_dir / name).is_file() for name in NEW_CODE_FILES), "S2 code files missing", failures)

    manifest = json.loads((doc_dir / "s2_change_manifest_v1.json").read_text(encoding="utf-8"))
    require(manifest.get("new_semantic_owner") is False, "new semantic owner declared", failures)
    require(manifest.get("canonical_owner_reused") == "Field Perception Orchestrator", "canonical owner mismatch", failures)
    require(manifest.get("existing_owner_files_modified") is False, "existing owner modification declared", failures)
    require(manifest.get("s0_modified") is False and manifest.get("s1_modified") is False, "S0/S1 modification declared", failures)
    require(manifest.get("raw_payload_copied_to_eval_out") is False, "raw payload persistence declared", failures)
    require(manifest.get("provider_execution_added") is False and manifest.get("s3_plus_activated") is False, "S3+ activation declared", failures)

    contract = json.loads((doc_dir / "s2_controlled_execution_contract_v1.json").read_text(encoding="utf-8"))
    require(contract.get("canonical_owner") == "Field Perception Orchestrator", "S2 owner contract mismatch", failures)
    require(contract.get("real_component") == "RAW_CAMERA_INPUT_STREAM", "S2 real component mismatch", failures)
    require(contract.get("bounded") is True, "bounded session missing", failures)
    for key in ("provider_autonomous_continuous_execution", "provider_invocation", "semantic_interpretation", "semantic_compression", "candidate_only", "raw_only", "do_not_persist"):
        expected = True if key in {"bounded", "candidate_only", "raw_only", "do_not_persist"} else False
        require(contract.get(key) is expected, f"S2 contract guard mismatch: {key}", failures)
    require("Perception Evidence" in contract.get("not_output", []), "raw adapter output boundary missing", failures)

    inventory = json.loads((doc_dir / "s2_existing_asset_inventory_and_reuse_v1.json").read_text(encoding="utf-8"))
    require(inventory.get("s2_new_owner_required") is False, "inventory requires new owner", failures)
    require(inventory.get("bounded_session_contract_exists") is True, "existing bounded contract not recorded", failures)
    require(inventory.get("existing_assets_modified") is False, "inventory records existing asset modification", failures)

    frame = json.loads((doc_dir / "s2_raw_frame_boundary_v1.json").read_text(encoding="utf-8"))
    require(len(frame.get("inequalities", [])) >= 7, "raw-frame inequalities incomplete", failures)
    require(frame.get("raw_only") is True and frame.get("candidate_only") is True, "raw-frame boundary mismatch", failures)
    require(frame.get("evidence_created") is False and frame.get("observation_created") is False, "raw frame promoted downstream", failures)

    session = json.loads((doc_dir / "s2_bounded_stream_session_contract_v1.json").read_text(encoding="utf-8"))
    require(session.get("required", {}).get("bounded") is True, "session bounded flag missing", failures)
    require(session.get("required", {}).get("autonomous_continuous_execution") is False, "provider autonomy boundary violated", failures)
    require("camera available" in session.get("non_authorizers", []), "camera availability autonomy guard missing", failures)
    require("STOP" in session.get("controls", []) and "REVOKE" in session.get("controls", []), "session controls incomplete", failures)

    ingress = json.loads((doc_dir / "s2_observation_perception_ingress_mapping_v1.json").read_text(encoding="utf-8"))
    require(ingress.get("output") == "PerceptionIngressCandidateV1", "perception ingress type mismatch", failures)
    require(ingress.get("observation_demand_ref_required") is True, "observation demand requirement missing", failures)
    require(ingress.get("observation_gateway_direct_admission") is False, "Gateway admission boundary violated", failures)
    require(ingress.get("semantic_authority") is False, "ingress semantic authority violated", failures)

    differential = json.loads((doc_dir / "s2_differential_validation_contract_v1.json").read_text(encoding="utf-8"))
    require(differential.get("synthetic_source_retained") is True, "synthetic source retention missing", failures)
    require(differential.get("one_component_at_a_time") is True, "one-component replacement missing", failures)
    require(tuple(differential.get("comparison_dimensions", ())) == ("contract outputs", "trace/provenance", "state transitions", "negative guards", "unrelated module behavior"), "differential dimensions mismatch", failures)

    privacy = json.loads((doc_dir / "s2_privacy_raw_data_policy_v1.json").read_text(encoding="utf-8"))
    require(privacy.get("do_not_persist_candidate") is True, "raw privacy boundary missing", failures)
    require(privacy.get("cross_user_transfer") is False, "cross-user transfer guard missing", failures)
    require(privacy.get("raw_bytes_in_json_artifacts") is False, "raw bytes artifact boundary violated", failures)

    guards = json.loads((doc_dir / "s2_negative_guards_v1.json").read_text(encoding="utf-8"))
    false_guard_values = [key for key, value in guards.get("guards", {}).items() if key != "raw_camera_input_stream" and value is not False]
    require(not false_guard_values, f"S2 negative guard mismatch: {false_guard_values}", failures)
    require(guards.get("provider_autonomous_continuous_execution") is False, "provider autonomy guard mismatch", failures)
    require(guards.get("provenance_grants_authority") is False, "provenance authority boundary mismatch", failures)

    mapping = json.loads((doc_dir / "s2_scenario_mapping_v1.json").read_text(encoding="utf-8"))
    require(set(mapping.get("scenario_ids", [])) == S2_IDS, "S2 scenario mapping mismatch", failures)

    phase = json.loads((doc_dir / "phase_contract.json").read_text(encoding="utf-8"))
    require(phase.get("new_semantic_owner") is False, "phase owner boundary mismatch", failures)
    require(phase.get("real_component_scope") == ["RAW_CAMERA_INPUT_STREAM"], "phase real scope mismatch", failures)
    for key in ("provider_autonomous_continuous_execution", "vision_yolo_execution", "ocr_execution", "slam_execution", "vio_execution", "vlm_execution", "semantic_interpretation", "semantic_compression", "provider_semantic_authority", "field_state_direct_mutation", "current_world_truth_declaration", "intent_mutation", "decision_mutation", "task_mutation", "real_action_execution", "real_runtime_execution", "database_write", "vector_store_write", "embedding_execution", "model_call", "scheduler_execution", "cross_user_transfer", "emotion_engine_execution", "b_route_execution", "raw_content_persisted", "s0_modified", "s1_modified"):
        require(phase.get(key) is False, f"phase guard mismatch: {key}", failures)

    parallel_matches = tuple(
        path for base in (root / "capabilities/midplatform", root / "docs/architecture")
        for path in base.rglob("*")
        if path.is_dir() and path.name in PARALLEL_OWNER_NAMES
    )
    require(not parallel_matches, "parallel S2 semantic owner created", failures)

    forbidden_tokens = ("cv2.", "torch.", "pytesseract", "subprocess", "requests.", "YOLO(", "OCR(", "SLAM(", "VLM(")
    for name in NEW_CODE_FILES:
        source = (code_dir / name).read_text(encoding="utf-8")
        for token in forbidden_tokens:
            require(token not in source, f"S2 forbidden execution token in {name}: {token}", failures)

    artifacts = {
        "summary": eval_dir / "a_route_s2_real_raw_camera_stream_result_v1.json",
        "cases": eval_dir / "a_route_s2_real_raw_camera_stream_case_results_v1.json",
        "s0": eval_dir / "a_route_s2_s0_regression_case_results_v1.json",
        "s1": eval_dir / "a_route_s2_s1_regression_case_results_v1.json",
        "trace": eval_dir / "a_route_s2_raw_camera_trace_v1.json",
    }
    require(all(path.exists() for path in artifacts.values()), "S2 runner artifacts missing", failures)
    if all(path.exists() for path in artifacts.values()):
        summary = json.loads(artifacts["summary"].read_text(encoding="utf-8"))
        cases = json.loads(artifacts["cases"].read_text(encoding="utf-8"))
        s0_cases = json.loads(artifacts["s0"].read_text(encoding="utf-8"))
        s1_cases = json.loads(artifacts["s1"].read_text(encoding="utf-8"))
        trace = json.loads(artifacts["trace"].read_text(encoding="utf-8"))
        require(summary.get("s2_scenario_count", 0) >= 24, "S2 scenario count mismatch", failures)
        require(summary.get("s0_scenario_count") == 40 and summary.get("s1_scenario_count") == 20, "S0/S1 regression counts missing", failures)
        require(summary.get("s0_all_cases_passed") is True, "S0 regression failed", failures)
        require(summary.get("s1_all_cases_passed") is True, "S1 regression failed", failures)
        require(summary.get("s2_all_cases_passed") is True and summary.get("all_cases_passed") is True, "S2 cases did not pass", failures)
        require(summary.get("failed_case_ids") == [], "S2 runner reports failed cases", failures)
        require({item.get("scenario_id") for item in cases if item.get("scenario_id") in S2_IDS} == S2_IDS, "S2 case coverage missing", failures)
        require(all(item.get("all_checks_passed") is True for item in cases), "S2 case checks failed", failures)
        require({item.get("scenario_id") for item in s0_cases} == {f"L{index:02d}" for index in range(1, 41)}, "S0 regression coverage missing", failures)
        require(all(item.get("all_checks_passed") is True for item in s0_cases), "S0 regression case failed", failures)
        require({item.get("scenario_id") for item in s1_cases if item.get("scenario_id", "").startswith("S1-")} >= {f"S1-{index:02d}" for index in range(1, 21)}, "S1 regression coverage missing", failures)
        require(all(item.get("all_checks_passed") is True for item in s1_cases), "S1 regression case failed", failures)
        require(summary.get("provider_autonomous_continuous_execution") is False, "provider autonomy artifact mismatch", failures)
        require(summary.get("raw_content_persisted") is False, "raw persistence artifact mismatch", failures)
        require(trace.get("provenance_grants_authority") is False, "trace authority artifact mismatch", failures)

    print(f"FAILED_CHECK_COUNT={len(failures)}")
    for failure in failures:
        print(f"FAIL={failure}")
    print(f"BLOCKER_COUNT={len(failures)}")
    print(f"S2_STATUS={'PASS' if not failures else 'FAIL'}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
