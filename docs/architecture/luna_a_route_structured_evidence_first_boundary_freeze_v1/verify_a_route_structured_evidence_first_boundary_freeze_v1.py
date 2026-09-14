from __future__ import annotations

import ast
import json
from pathlib import Path


DOC_FILES = {
    "structured_evidence_first_manifest_v1.json",
    "human_language_vs_sensor_semantics_boundary_v1.json",
    "sensor_ingress_canonical_flow_v1.json",
    "provider_evidence_semantic_inequality_v1.json",
    "product_loop_input_sensor_boundary_v1.json",
    "s1_semantic_scope_closure_v1.json",
    "s2_s5_corrected_replacement_definition_v1.json",
    "semantic_compression_deferred_freeze_v1.json",
    "structured_evidence_negative_guards_v1.json",
    "closure_summary_v1.md",
    "phase_contract.json",
    "verify_a_route_structured_evidence_first_boundary_freeze_v1.py",
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
    doc_dir = root / "docs/architecture/luna_a_route_structured_evidence_first_boundary_freeze_v1"

    actual_files = {path.name for path in doc_dir.iterdir() if path.is_file()}
    require(actual_files == DOC_FILES, "exact boundary-freeze file set mismatch", failures)
    for path in sorted(doc_dir.glob("*.json")):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            failures.append(f"JSON parse failed: {path.name}: {exc}")
    try:
        ast.parse((doc_dir / "verify_a_route_structured_evidence_first_boundary_freeze_v1.py").read_text(encoding="utf-8"))
    except (OSError, SyntaxError) as exc:
        failures.append(f"verifier AST parse failed: {exc}")
    implementation_files = {path.name for path in doc_dir.glob("*.py")}
    require(implementation_files == {"verify_a_route_structured_evidence_first_boundary_freeze_v1.py"}, "implementation file created in freeze package", failures)

    manifest = json.loads((doc_dir / "structured_evidence_first_manifest_v1.json").read_text(encoding="utf-8"))
    require(manifest.get("freeze_id") == "STRUCTURED_EVIDENCE_FIRST_BOUNDARY_FREEZE_V1", "freeze identity mismatch", failures)
    require(manifest.get("freeze_status") == "FROZEN_V1", "freeze status mismatch", failures)
    require(manifest.get("principle") == "STRUCTURED_EVIDENCE_FIRST", "structured evidence principle missing", failures)
    require(manifest.get("semantic_compression_status") == "DEFERRED", "semantic compression not deferred", failures)
    require(manifest.get("s0_baseline_ref") == "S0_GOLDEN_SYNTHETIC_BASELINE:FROZEN_V1", "S0 reference mismatch", failures)
    require(manifest.get("s0_assets_modified") is False and manifest.get("s1_implementation_modified") is False, "prior assets marked modified", failures)
    require(manifest.get("implementation_files_created") == [], "freeze implementation expansion declared", failures)

    s0 = json.loads((root / "docs/architecture/luna_a_route_golden_synthetic_product_loop_baseline_freeze_v1/a_route_golden_synthetic_baseline_manifest_v1.json").read_text(encoding="utf-8"))
    require(s0.get("freeze_status") == "FROZEN_V1" and s0.get("freeze_id") == "S0_GOLDEN_SYNTHETIC_BASELINE", "S0 freeze evidence missing", failures)
    s1 = json.loads((root / "docs/architecture/luna_a_route_s1_real_user_input_controlled_replacement_v1/s1_real_user_input_controlled_execution_contract_v1.json").read_text(encoding="utf-8"))
    require(s1.get("output") == "ProductLoopInputV1", "S1 ProductLoopInput boundary missing", failures)
    require(s1.get("real_component") == "USER_INPUT", "S1 scope expanded beyond USER_INPUT", failures)
    require("semantic interpretation" in s1.get("not_performed", []), "S1 semantic interpretation boundary missing", failures)
    require(s1.get("truth_declared") is False, "S1 truth boundary violated", failures)

    human = json.loads((doc_dir / "human_language_vs_sensor_semantics_boundary_v1.json").read_text(encoding="utf-8"))
    require(human.get("human_authored_language", {}).get("is_luna_semantic_compression") is False, "human language incorrectly classified as compression", failures)
    require(human.get("human_authored_language", {}).get("becomes_external_reality_truth") is False, "user statement truth boundary violated", failures)
    require(human.get("machine_sensor_input", {}).get("must_remain") == "structured provider-native evidence", "sensor evidence structure missing", failures)
    require("conclusion-level natural-language sentence" in human.get("machine_sensor_input", {}).get("must_not_become", ""), "sensor conclusion shortcut not forbidden", failures)

    flow = json.loads((doc_dir / "sensor_ingress_canonical_flow_v1.json").read_text(encoding="utf-8"))
    require(flow.get("canonical_flow", [])[0:3] == ["Raw Sensor Data", "Provider-Native Evidence", "Perception Evidence"], "canonical sensor flow mismatch", failures)
    require(flow.get("opaque_conclusion_conversion") is False, "opaque sensor conclusion conversion allowed", failures)
    require(flow.get("automatic_fact_admission") is False, "automatic fact admission allowed", failures)

    sensor_boundary = json.loads((doc_dir / "product_loop_input_sensor_boundary_v1.json").read_text(encoding="utf-8"))
    require("raw camera frames" in sensor_boundary.get("ProductLoopInputV1_must_not_be_sensor_sink_for", []), "raw camera boundary missing", failures)
    require(sensor_boundary.get("raw_sensor_to_product_loop_language_conversion") is False, "ProductLoopInput sensor sink allowed", failures)

    replacement = json.loads((doc_dir / "s2_s5_corrected_replacement_definition_v1.json").read_text(encoding="utf-8"))
    require(replacement.get("S2", {}).get("name") == "REAL_RAW_CAMERA_INPUT_STREAM_INGESTION", "corrected S2 definition missing", failures)
    require(replacement.get("S2", {}).get("does_not_execute") == ["YOLO", "OCR", "SLAM", "VLM", "semantic interpretation", "semantic compression"], "S2 scope expanded", failures)
    require(replacement.get("S3", {}).get("name") == "REAL_VISION_YOLO_EVIDENCE_REPLACEMENT", "S3 definition missing", failures)
    require(replacement.get("S4", {}).get("name") == "REAL_OCR_EVIDENCE_REPLACEMENT", "S4 definition missing", failures)
    require(replacement.get("S5", {}).get("name") == "REAL_SLAM_VIO_SPATIAL_EVIDENCE_REPLACEMENT", "S5 definition missing", failures)
    require(replacement.get("S3", {}).get("output_authoritative_world_language") is False, "S3 authority boundary violated", failures)
    require(replacement.get("S4", {}).get("output_authoritative_world_language") is False, "S4 authority boundary violated", failures)
    require(replacement.get("S5", {}).get("output_authoritative_world_language") is False, "S5 authority boundary violated", failures)

    deferred = json.loads((doc_dir / "semantic_compression_deferred_freeze_v1.json").read_text(encoding="utf-8"))
    require(deferred.get("semantic_compression_status") == "DEFERRED" and deferred.get("execution") is False, "deferred semantic compression boundary mismatch", failures)
    guards = json.loads((doc_dir / "structured_evidence_negative_guards_v1.json").read_text(encoding="utf-8"))
    require(all(value is False for value in guards.get("guards", {}).values()), "structured evidence negative guard is not false", failures)
    require(guards.get("provenance_grants_authority") is False, "provenance authority boundary violated", failures)

    contract = json.loads((doc_dir / "phase_contract.json").read_text(encoding="utf-8"))
    for key in ("implementation_change", "s0_modified", "s1_modified", "product_loop_input_modified", "observation_gateway_modified", "field_perception_orchestrator_modified", "emotion_engine_execution", "b_route_execution", "semantic_compression_execution", "database_write", "runtime_execution", "model_call", "provider_execution", "real_side_effect"):
        require(contract.get(key) is False, f"phase boundary mismatch: {key}", failures)
    require(contract.get("structured_evidence_first") is True, "phase principle missing", failures)
    require(contract.get("semantic_compression_status") == "DEFERRED", "phase compression status mismatch", failures)

    print(f"FAILED_CHECK_COUNT={len(failures)}")
    for failure in failures:
        print(f"FAIL={failure}")
    print(f"BLOCKER_COUNT={len(failures)}")
    print(f"FREEZE_STATUS={'FROZEN_V1' if not failures else 'FREEZE_BLOCKED'}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
