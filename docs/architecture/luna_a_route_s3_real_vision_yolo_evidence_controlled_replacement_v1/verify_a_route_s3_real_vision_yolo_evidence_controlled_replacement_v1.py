from __future__ import annotations

import ast
import json
from pathlib import Path


CODE_DIR_REL = "capabilities/midplatform/field_perception_orchestrator/integration"
NEW_CODE_FILES = {
    "field_perception_real_vision_evidence_types_v1.py",
    "field_perception_real_vision_provider_adapter_v1.py",
    "field_perception_real_vision_fixture_v1.py",
    "run_a_route_s3_real_vision_yolo_evidence_controlled_replacement_v1.py",
}
DOC_FILES = {
    "s3_existing_asset_inventory_and_reuse_v1.json",
    "s3_owner_admission_mapping_v1.json",
    "s3_controlled_execution_contract_v1.json",
    "s3_provider_autonomy_boundary_v1.json",
    "s3_visual_evidence_contract_v1.json",
    "s3_attention_region_boundary_v1.json",
    "s3_model_admission_boundary_v1.json",
    "s3_evidence_sufficiency_mapping_v1.json",
    "s3_structured_evidence_inequalities_v1.json",
    "s3_differential_validation_contract_v1.json",
    "s3_privacy_raw_visual_data_policy_v1.json",
    "s3_negative_guards_v1.json",
    "s3_scenario_mapping_v1.json",
    "s3_change_manifest_v1.json",
    "s3_implementation_summary_v1.md",
    "phase_contract.json",
    "verify_a_route_s3_real_vision_yolo_evidence_controlled_replacement_v1.py",
}
S3_IDS = {f"S3-{index:02d}" for index in range(1, 29)}
PARALLEL_OWNER_NAMES = {
    "vision_governance",
    "perception_brain",
    "camera_governance",
    "sensor_intelligence_governance",
    "yolo_governance",
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
    root = repo_root_from(Path(__file__))
    doc_dir = root / "docs/architecture/luna_a_route_s3_real_vision_yolo_evidence_controlled_replacement_v1"
    code_dir = root / CODE_DIR_REL
    eval_dir = root / "_eval_out/a_route_s3_real_vision_yolo_evidence_controlled_replacement_v1"

    actual_docs = {path.name for path in doc_dir.iterdir() if path.is_file()}
    require(actual_docs == DOC_FILES, "S3 documentation file set mismatch", failures)
    for path in sorted(doc_dir.glob("*.json")):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            failures.append(f"JSON parse failed: {path.name}: {exc}")
    for name in NEW_CODE_FILES | {"verify_a_route_s3_real_vision_yolo_evidence_controlled_replacement_v1.py"}:
        path = code_dir / name if name in NEW_CODE_FILES else doc_dir / name
        require(path.is_file(), f"S3 file missing: {name}", failures)
        if path.is_file():
            try:
                ast.parse(path.read_text(encoding="utf-8"))
            except (OSError, SyntaxError) as exc:
                failures.append(f"S3 AST parse failed: {name}: {exc}")

    manifest = json.loads((doc_dir / "s3_change_manifest_v1.json").read_text(encoding="utf-8"))
    require(manifest.get("new_semantic_owner") is False, "new semantic owner declared", failures)
    require(manifest.get("canonical_owner_reused") == "Field Perception Orchestrator", "canonical owner mismatch", failures)
    require(manifest.get("reused_provider") == "capabilities/vision_runtime/yolo_candidate_adapter_v0.py", "existing YOLO provider not recorded", failures)
    for key in ("existing_owner_files_modified", "s0_modified", "s1_modified", "s2_modified", "observation_gateway_modified", "vision_provider_stack_duplicated", "ocr_activated", "slam_activated", "vlm_activated", "semantic_compression_added", "world_or_field_write_added"):
        require(manifest.get(key) is False, f"change manifest boundary mismatch: {key}", failures)

    inventory = json.loads((doc_dir / "s3_existing_asset_inventory_and_reuse_v1.json").read_text(encoding="utf-8"))
    require(inventory.get("new_semantic_owner_required") is False, "inventory requires new owner", failures)
    require(inventory.get("model_manager_admission_path_exists") is True, "model admission path missing", failures)
    require(inventory.get("detection_result_schema_exists") is True, "detection schema missing", failures)
    require(inventory.get("current_yolo_implementation") == "yolo_candidate_adapter_v0", "YOLO inventory mismatch", failures)

    contract = json.loads((doc_dir / "s3_controlled_execution_contract_v1.json").read_text(encoding="utf-8"))
    require(contract.get("canonical_owner") == "Field Perception Orchestrator", "S3 owner contract mismatch", failures)
    require("ObservationGatewayEvidenceHandoffCandidateV1" in contract.get("output", []), "Observation Gateway handoff candidate missing", failures)
    require(contract.get("candidate_only") is True and contract.get("truth_declared") is False, "candidate boundary mismatch", failures)
    for key in ("fact_admitted", "field_mutation", "current_world_mutation", "semantic_interpretation", "semantic_compression", "provider_autonomous_execution", "ocr_execution", "slam_execution", "vlm_execution", "raw_content_persisted"):
        require(contract.get(key) is False, f"S3 contract guard mismatch: {key}", failures)
    require(all(item in contract.get("required_authorization", []) for item in ("observation_demand", "observation_request", "VISION_DETECTION capability requirement", "bounded provider session", "model admission reference", "raw frame reference", "trace/provenance")), "authorization chain incomplete", failures)

    autonomy = json.loads((doc_dir / "s3_provider_autonomy_boundary_v1.json").read_text(encoding="utf-8"))
    require(autonomy.get("vision_provider_autonomous_execution") is False, "provider autonomy boundary violated", failures)
    require(len(autonomy.get("non_authorizers", [])) >= 7, "provider non-authorizer coverage incomplete", failures)
    require(autonomy.get("no_hidden_retry") is True and autonomy.get("no_hidden_continuation") is True, "hidden provider continuation guard missing", failures)

    attention = json.loads((doc_dir / "s3_attention_region_boundary_v1.json").read_text(encoding="utf-8"))
    require(attention.get("region_scope_enforced") is False and attention.get("region_scope_limitation_recorded") is True, "region execution limitation not explicit", failures)

    evidence = json.loads((doc_dir / "s3_visual_evidence_contract_v1.json").read_text(encoding="utf-8"))
    require(len(evidence.get("required_fields", [])) >= 14, "visual evidence fields incomplete", failures)
    require(len(evidence.get("inequalities", [])) >= 10, "visual evidence inequalities incomplete", failures)
    require(evidence.get("candidate_only") is True and evidence.get("truth_declared") is False and evidence.get("fact_admitted") is False, "visual evidence truth boundary violated", failures)
    require(evidence.get("natural_language_conclusion_generated") is False, "conclusion language boundary violated", failures)

    model = json.loads((doc_dir / "s3_model_admission_boundary_v1.json").read_text(encoding="utf-8"))
    require(model.get("capability_requirement") == "VISION_DETECTION", "vision capability requirement missing", failures)
    for key in ("provider_candidate_reference_required", "model_candidate_reference_required", "model_admission_reference_required"):
        require(model.get(key) is True, f"model admission reference missing: {key}", failures)
    require(model.get("model_availability_is_execution_authority") is False and model.get("provider_candidate_is_invocation") is False, "model/provider authority separation violated", failures)

    sufficiency = json.loads((doc_dir / "s3_evidence_sufficiency_mapping_v1.json").read_text(encoding="utf-8"))
    require(sufficiency.get("model_confidence_is_sufficiency") is False, "confidence/sufficiency boundary violated", failures)
    require(sufficiency.get("control_routes", {}).get("SUFFICIENT") == "STOP", "STOP route missing", failures)
    require(sufficiency.get("control_routes", {}).get("INSUFFICIENT") == "CONTINUE", "CONTINUE route missing", failures)
    require(sufficiency.get("control_routes", {}).get("CONTESTED") == "RECONSIDER", "RECONSIDER route missing", failures)

    inequalities = json.loads((doc_dir / "s3_structured_evidence_inequalities_v1.json").read_text(encoding="utf-8"))
    require(all(value is False for key, value in inequalities.items() if key != "semantic_compression"), "structured evidence inequality guard violated", failures)
    require(inequalities.get("semantic_compression") is False, "semantic compression activated", failures)

    differential = json.loads((doc_dir / "s3_differential_validation_contract_v1.json").read_text(encoding="utf-8"))
    require(differential.get("synthetic_provider_fixture_retained") is True, "synthetic provider fixture not retained", failures)
    require(differential.get("one_component_at_a_time") is True, "one component replacement missing", failures)
    require(tuple(differential.get("comparison_dimensions", ())) == ("contract outputs", "trace/provenance", "state transitions", "negative guards", "unrelated module behavior"), "differential dimensions mismatch", failures)

    privacy = json.loads((doc_dir / "s3_privacy_raw_visual_data_policy_v1.json").read_text(encoding="utf-8"))
    require(privacy.get("do_not_persist_raw_content") is True and privacy.get("cross_user_transfer") is False and privacy.get("training_use") is False, "visual privacy boundary mismatch", failures)

    guards = json.loads((doc_dir / "s3_negative_guards_v1.json").read_text(encoding="utf-8"))
    require(guards.get("guards", {}).get("vision_yolo_execution") == "authorized_bounded_real_only", "YOLO guard is not scoped", failures)
    require(all(value is False for key, value in guards.get("guards", {}).items() if key != "vision_yolo_execution"), "S3 negative guards contain an unexpected true value", failures)

    mapping = json.loads((doc_dir / "s3_scenario_mapping_v1.json").read_text(encoding="utf-8"))
    require(set(mapping.get("scenario_ids", [])) == S3_IDS, "S3 scenario mapping mismatch", failures)

    phase = json.loads((doc_dir / "phase_contract.json").read_text(encoding="utf-8"))
    require(phase.get("new_semantic_owner") is False, "phase owner boundary mismatch", failures)
    require(phase.get("real_component_scope") == ["VISION_YOLO_EVIDENCE"], "S3 real scope mismatch", failures)
    for key in ("provider_autonomous_execution", "ocr_execution", "slam_execution", "vio_execution", "vlm_execution", "semantic_interpretation", "semantic_compression", "provider_semantic_authority", "automatic_fact_admission", "field_state_direct_mutation", "current_world_truth_declaration", "intent_mutation", "decision_mutation", "task_mutation", "real_action_execution", "real_runtime_execution", "database_write", "vector_store_write", "embedding_execution", "scheduler_execution", "cross_user_transfer", "emotion_engine_execution", "b_route_execution", "raw_content_persisted", "training_use", "s0_modified", "s1_modified", "s2_modified"):
        require(phase.get(key) is False, f"phase guard mismatch: {key}", failures)

    parallel_matches = tuple(path for base in (root / "capabilities/midplatform", root / "docs/architecture") for path in base.rglob("*") if path.is_dir() and path.name in PARALLEL_OWNER_NAMES)
    require(not parallel_matches, "parallel S3 semantic owner created", failures)

    forbidden_tokens = ("from ultralytics import", "YOLO(", "OCR(", "SLAM(", "VLM(", "cv2.", "torch.", "pytesseract", "subprocess", "requests.")
    for name in NEW_CODE_FILES:
        source = (code_dir / name).read_text(encoding="utf-8")
        for token in forbidden_tokens:
            require(token not in source, f"S3 direct/forbidden execution token in {name}: {token}", failures)

    artifacts = {
        "summary": eval_dir / "a_route_s3_real_vision_yolo_result_v1.json",
        "cases": eval_dir / "a_route_s3_real_vision_yolo_case_results_v1.json",
        "s0": eval_dir / "a_route_s3_s0_regression_case_results_v1.json",
        "s1": eval_dir / "a_route_s3_s1_regression_case_results_v1.json",
        "s2": eval_dir / "a_route_s3_s2_regression_case_results_v1.json",
        "trace": eval_dir / "a_route_s3_real_vision_yolo_trace_v1.json",
    }
    require(all(path.exists() for path in artifacts.values()), "S3 runner artifacts missing", failures)
    if all(path.exists() for path in artifacts.values()):
        summary = json.loads(artifacts["summary"].read_text(encoding="utf-8"))
        cases = json.loads(artifacts["cases"].read_text(encoding="utf-8"))
        s0_cases = json.loads(artifacts["s0"].read_text(encoding="utf-8"))
        s1_cases = json.loads(artifacts["s1"].read_text(encoding="utf-8"))
        s2_cases = json.loads(artifacts["s2"].read_text(encoding="utf-8"))
        trace = json.loads(artifacts["trace"].read_text(encoding="utf-8"))
        require(summary.get("s3_scenario_count", 0) >= 28, "S3 scenario count mismatch", failures)
        require(summary.get("s0_scenario_count") == 40 and summary.get("s1_scenario_count") == 20 and summary.get("s2_scenario_count") == 24, "prior regression counts missing", failures)
        require(summary.get("s0_all_cases_passed") is True and summary.get("s1_all_cases_passed") is True and summary.get("s2_all_cases_passed") is True, "prior regression failed", failures)
        require(summary.get("s3_all_cases_passed") is True and summary.get("all_cases_passed") is True, "S3 controlled scenarios failed", failures)
        require(summary.get("failed_case_ids") == [], "S3 runner reports failed cases", failures)
        require({item.get("scenario_id") for item in cases if item.get("scenario_id") in S3_IDS} == S3_IDS, "S3 case coverage missing", failures)
        require(all(item.get("all_checks_passed") is True for item in cases), "S3 case checks failed", failures)
        require(all(item.get("all_checks_passed") is True for item in s0_cases), "S0 regression case failed", failures)
        require(all(item.get("all_checks_passed") is True for item in s1_cases), "S1 regression case failed", failures)
        require(all(item.get("all_checks_passed") is True for item in s2_cases), "S2 regression case failed", failures)
        require(trace.get("provenance_grants_authority") is False, "trace authority boundary mismatch", failures)
        require(summary.get("provider_autonomous_continuous_execution") is False, "provider autonomy artifact mismatch", failures)
        require(summary.get("ocr_execution") is False and summary.get("slam_execution") is False and summary.get("vlm_execution") is False, "S4+ execution artifact mismatch", failures)
        require(summary.get("semantic_compression") is False and summary.get("do_not_persist_raw_content") is True, "semantic/privacy artifact mismatch", failures)

    print(f"FAILED_CHECK_COUNT={len(failures)}")
    for failure in failures:
        print(f"FAIL={failure}")
    print(f"BLOCKER_COUNT={len(failures)}")
    print(f"S3_STATUS={'PASS' if not failures else 'FAIL'}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
