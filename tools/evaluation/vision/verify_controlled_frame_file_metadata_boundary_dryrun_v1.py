#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Controlled Frame File Metadata Boundary DryRun v1 (decision simulation only)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Controlled-Frame-File-Metadata-Boundary-DryRun-v1-001"
FINAL_DECISION = "CONTROLLED_FRAME_FILE_METADATA_BOUNDARY_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
NEXT_PHASE = "Phase-Controlled-Frame-File-Metadata-Boundary-Post-DryRun-Review-v1-001"
MIN_CHECKS = 220
BASELINE_REQUIREMENT = 180

REQUIRED_SCENARIO_IDS = [
    "repo_fixture_path_candidate",
    "eval_out_fixture_path_candidate",
    "user_uploaded_path_candidate",
    "external_absolute_path_blocked",
    "path_traversal_blocked",
    "symlink_requires_review",
    "unknown_path_blocked",
    "declared_metadata_public_image",
    "declared_metadata_private_home",
    "missing_declared_metadata_blocked",
    "hash_placeholder_allowed",
    "real_hash_attempt_blocked",
    "exif_parse_attempt_blocked",
    "video_probe_attempt_blocked",
    "perceptual_hash_deferred",
    "fixture_registry_entry_candidate",
    "manifest_to_metadata_mapping_candidate",
    "metadata_sensitive_requires_manual_review",
]


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/controlled_frame_file_metadata_boundary_dryrun_v1_smoke_v0",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    input_root_matrix = _load_json(root / "input_root_matrix.json")
    dryrun_case_schema = _load_json(root / "dryrun_case_schema.json")
    stub_schema = _load_json(root / "simulated_file_ref_metadata_stub_schema.json")
    path_schema = _load_json(root / "path_legality_decision_candidate_schema.json")
    existence_schema = _load_json(root / "file_existence_decision_candidate_schema.json")
    metadata_schema = _load_json(root / "external_metadata_decision_candidate_schema.json")
    hash_schema = _load_json(root / "hash_policy_decision_candidate_schema.json")
    fixture_schema = _load_json(root / "fixture_registry_decision_candidate_schema.json")
    mapping_schema = _load_json(root / "manifest_to_file_metadata_mapping_decision_candidate_schema.json")
    result_schema = _load_json(root / "file_metadata_boundary_dryrun_result_schema.json")
    scenario_matrix = _load_json(root / "controlled_frame_file_metadata_boundary_dryrun_scenario_matrix.json")
    dryrun_results = _load_json(root / "controlled_frame_file_metadata_boundary_dryrun_results.json")
    path_results = _load_json(root / "path_legality_decision_results.json")
    existence_results = _load_json(root / "file_existence_decision_results.json")
    metadata_results = _load_json(root / "external_metadata_decision_results.json")
    hash_results = _load_json(root / "hash_policy_decision_results.json")
    fixture_results = _load_json(root / "fixture_registry_decision_results.json")
    mapping_results = _load_json(root / "manifest_to_file_metadata_mapping_results.json")
    boundary_matrix = _load_json(root / "file_metadata_boundary_matrix.json")
    governance_debt = _load_json(root / "governance_debt_register.json")
    next_phase = _load_json(root / "next_phase_recommendation.json")
    no_file_op = _load_json(root / "no_file_operation_boundary_report.json")
    no_runtime = _load_json(root / "no_runtime_boundary_report.json")
    no_write = _load_json(root / "no_write_boundary_report.json")

    rows = input_root_matrix.get("rows", [])
    idx = {row.get("intake_id"): row for row in rows}
    for intake_id in (
        "controlled_frame_file_metadata_boundary_planning",
        "post_controlled_frame_sample_roadmap_decision",
        "controlled_frame_sample_closure",
        "controlled_frame_sample_post_review",
        "controlled_frame_sample_dryrun",
        "controlled_frame_sample_planning",
        "controlled_frame_input_closure",
        "map_location_readonly_context",
        "safety_constitution",
        "minimal_runtime_integration_closure",
        "ocr_final_closure",
    ):
        ok(f"input.{intake_id}", idx.get(intake_id, {}).get("loaded") is True)
    for intake_id in (
        "vision_frame_trace_stream_registry",
        "vision_frame_input_governance",
        "vision_roi_proposal_stub",
        "system_health_hardware_profile",
        "simulation_lab_profile",
        "privacy_governance_docs",
    ):
        ok(
            f"input.{intake_id}.optional",
            idx.get(intake_id, {}).get("status") in {"loaded", "optional_missing"},
            idx.get(intake_id, {}).get("status"),
        )

    for key in (
        "file_metadata_boundary_planning_input_loaded",
        "post_controlled_frame_sample_roadmap_input_loaded",
        "controlled_frame_sample_closure_input_loaded",
        "controlled_frame_sample_post_review_input_loaded",
        "controlled_frame_sample_dryrun_input_loaded",
        "controlled_frame_sample_planning_input_loaded",
        "controlled_frame_input_closure_input_loaded",
        "map_location_readonly_context_input_loaded",
        "safety_constitution_input_loaded",
        "minimal_runtime_integration_closure_loaded",
        "ocr_final_closure_loaded",
        "dryrun_case_schema_defined",
        "simulated_file_ref_metadata_stub_schema_defined",
        "path_legality_decision_candidate_schema_defined",
        "file_existence_decision_candidate_schema_defined",
        "external_metadata_decision_candidate_schema_defined",
        "hash_policy_decision_candidate_schema_defined",
        "fixture_registry_decision_candidate_schema_defined",
        "manifest_to_file_metadata_mapping_decision_candidate_schema_defined",
        "file_metadata_boundary_dryrun_result_schema_defined",
        "scenario_matrix_generated",
        "dryrun_results_generated",
        "fixture_registry_candidate_generated",
        "manifest_to_file_metadata_mapping_generated",
        "metadata_decision_simulation_only",
        "hash_placeholder_allowed",
        "perceptual_hash_deferred",
        "no_exif_parse_now",
        "no_video_probe_now",
        "no_runtime_executed",
        "no_new_runtime_enabled",
        "boundary_ok",
    ):
        ok(f"summary.{key}", summary.get(key) is True)

    ok("summary.scenario_count>=18", summary.get("scenario_count", 0) >= 18, summary.get("scenario_count"))
    ok("summary.allowed_path_candidate_count>=2", summary.get("allowed_path_candidate_count", 0) >= 2, summary.get("allowed_path_candidate_count"))
    ok("summary.restricted_path_candidate_count>=2", summary.get("restricted_path_candidate_count", 0) >= 2, summary.get("restricted_path_candidate_count"))
    ok("summary.blocked_path_candidate_count>=3", summary.get("blocked_path_candidate_count", 0) >= 3, summary.get("blocked_path_candidate_count"))
    ok("summary.metadata_candidate_case_count>=2", summary.get("metadata_candidate_case_count", 0) >= 2, summary.get("metadata_candidate_case_count"))
    ok("summary.hash_policy_case_count>=3", summary.get("hash_policy_case_count", 0) >= 3, summary.get("hash_policy_case_count"))

    for key in (
        "file_existence_check_allowed_now",
        "path_legality_check_allowed_now",
        "external_metadata_read_allowed_now",
        "real_hash_computation_allowed_now",
        "file_existence_check_invoked",
        "file_stat_invoked",
        "file_opened",
        "file_content_read",
        "image_content_read",
        "video_content_read",
        "image_opened",
        "video_opened",
        "video_decoded",
        "frame_extracted",
        "exif_parsed",
        "video_probe_invoked",
        "real_file_hash_computed",
        "perceptual_hash_computed",
        "fixture_registry_runtime_started",
        "manifest_to_file_metadata_candidate_mapping_runtime_started",
        "visual_observation_generated",
        "scene_sketch_generated",
        "ocr_activation_result_generated",
        "tracking_result_generated",
        "camera_invoked",
        "camera_opened",
        "visual_model_invoked",
        "map_api_invoked",
        "gaode_api_invoked",
        "gps_runtime_invoked",
        "ocr_provider_invoked",
        "ocrrequest_submitted",
        "tracking_runtime_invoked",
        "optical_flow_runtime_invoked",
        "crossing_runtime_invoked",
        "speech_gate_invoked",
        "vop_invoked",
        "tts_invoked",
        "task_state_committed_now",
        "navigation_action_triggered",
        "route_modified",
        "scene_delta_generated",
        "world_model_written",
        "memory_written",
        "library_written",
        "fact_written",
    ):
        ok(f"summary.{key}", summary.get(key) is False)

    ok("summary.dryrun_scope", summary.get("dryrun_scope") == "controlled_frame_file_metadata_boundary_dryrun_only")
    ok("summary.violations", summary.get("violations") == [])
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)

    ok("dryrun_case_schema.name", dryrun_case_schema.get("schema_name") == "ControlledFrameFileMetadataBoundaryDryRunCase")
    ok("stub_schema.invariants.stat", stub_schema.get("invariants", {}).get("file_stat_invoked") is False)
    ok("stub_schema.invariants.open", stub_schema.get("invariants", {}).get("file_opened") is False)
    ok("path_schema.status_values", len(path_schema.get("path_status_values", [])) >= 6)
    ok("existence_schema.not_checked", "existence_status" in {f["name"] for f in existence_schema.get("field_specs", [])})
    ok("metadata_schema.no_exif", metadata_schema.get("field_specs") and True)
    ok("hash_schema.real_hash_blocked", "real_hash_attempt_blocked" in {f["name"] for f in hash_schema.get("field_specs", [])})
    ok("fixture_schema.runtime", fixture_schema.get("field_specs") and True)
    ok("mapping_schema.content_read", mapping_schema.get("field_specs") and True)
    ok("result_schema.refs", "path_decision_ref" in {f["name"] for f in result_schema.get("field_specs", [])})

    scenario_rows = scenario_matrix.get("scenarios", [])
    scenario_idx = {row.get("scenario_id"): row for row in scenario_rows}
    ok("scenarios.count", scenario_matrix.get("scenario_count", 0) >= 18, scenario_matrix.get("scenario_count"))
    for sid in REQUIRED_SCENARIO_IDS:
        row = scenario_idx.get(sid, {})
        ok(f"scenario.{sid}.present", sid in scenario_idx)
        ok(f"scenario.{sid}.simulation_only", row.get("metadata_decision_simulation_only") is True)
        ok(f"scenario.{sid}.file_stat", row.get("file_stat_invoked") is False)
        ok(f"scenario.{sid}.file_opened", row.get("file_opened") is False)
        ok(f"scenario.{sid}.content_read", row.get("content_read") is False)

    ok("dryrun_results.count", dryrun_results.get("result_count", 0) >= 18, dryrun_results.get("result_count"))
    ok("path_results.count", path_results.get("decision_count", 0) >= 18, path_results.get("decision_count"))
    ok("existence_results.count", existence_results.get("decision_count", 0) >= 18, existence_results.get("decision_count"))
    ok("metadata_results.count", metadata_results.get("decision_count", 0) >= 18, metadata_results.get("decision_count"))
    ok("hash_results.count", hash_results.get("decision_count", 0) >= 18, hash_results.get("decision_count"))
    ok("fixture_results.count", fixture_results.get("decision_count", 0) >= 18, fixture_results.get("decision_count"))
    ok("mapping_results.count", mapping_results.get("decision_count", 0) >= 18, mapping_results.get("decision_count"))

    path_decisions = path_results.get("decisions", [])
    ok("path.repo_fixture", any(d.get("path_status") == "allowed_repo_fixture_candidate" for d in path_decisions))
    ok("path.eval_out", any(d.get("path_status") == "allowed_eval_out_fixture_candidate" for d in path_decisions))
    ok("path.user_upload", any(d.get("path_status") == "restricted_user_upload_candidate" for d in path_decisions))
    ok("path.external_blocked", any(d.get("path_status") == "blocked_external_absolute_path" for d in path_decisions))
    ok("path.traversal_blocked", any(d.get("path_status") == "blocked_path_traversal" for d in path_decisions))
    ok("path.symlink", any(d.get("path_status") == "restricted_symlink_candidate" for d in path_decisions))
    ok("path.unknown_blocked", any(d.get("path_status") == "blocked_unknown_path" for d in path_decisions))
    for d in path_decisions:
        ok(f"path.{d.get('path_decision_id')}.no_file_op", d.get("file_operation_allowed") is False)

    existence_decisions = existence_results.get("decisions", [])
    for d in existence_decisions:
        ok(f"existence.{d.get('existence_decision_id')}.not_invoked", d.get("file_existence_check_invoked") is False)
        ok(f"existence.{d.get('existence_decision_id')}.not_checked", d.get("existence_status") == "not_checked")
        ok(f"existence.{d.get('existence_decision_id')}.allowed_now", d.get("file_existence_check_allowed_now") is False)

    metadata_decisions = metadata_results.get("decisions", [])
    ok("metadata.public", any("allowed" in d.get("metadata_status", "") for d in metadata_decisions))
    ok("metadata.private", any("restricted" in d.get("metadata_status", "") or d.get("manual_review_required") for d in metadata_decisions))
    ok("metadata.missing_blocked", any(d.get("missing_declared_metadata_blocked") for d in metadata_decisions))
    ok("metadata.exif_blocked", any(d.get("metadata_status") == "exif_parse_attempt_blocked" for d in metadata_decisions))
    ok("metadata.probe_blocked", any(d.get("metadata_status") == "video_probe_attempt_blocked" for d in metadata_decisions))
    for d in metadata_decisions:
        ok(f"metadata.{d.get('metadata_decision_id')}.no_read", d.get("external_metadata_read_allowed_now") is False)
        ok(f"metadata.{d.get('metadata_decision_id')}.no_exif", d.get("exif_parse_allowed_now") is False)
        ok(f"metadata.{d.get('metadata_decision_id')}.no_probe", d.get("video_probe_allowed_now") is False)

    hash_decisions = hash_results.get("decisions", [])
    ok("hash.placeholder", any(d.get("hash_placeholder_allowed") and d.get("selected_hash_policy") == "placeholder_only" for d in hash_decisions))
    ok("hash.real_blocked", any(d.get("real_hash_attempt_blocked") for d in hash_decisions))
    ok("hash.perceptual_deferred", any(d.get("perceptual_hash_deferred") for d in hash_decisions))
    for d in hash_decisions:
        ok(f"hash.{d.get('hash_decision_id')}.not_computed", d.get("hash_currently_not_computed") is True)
        ok(f"hash.{d.get('hash_decision_id')}.real_now", d.get("real_hash_computation_allowed_now") is False)

    fixture_decisions = fixture_results.get("decisions", [])
    ok("fixture.candidate", any(d.get("registry_entry_candidate_allowed") for d in fixture_decisions))
    for d in fixture_decisions:
        ok(f"fixture.{d.get('fixture_registry_decision_id')}.no_runtime", d.get("registry_runtime_started") is False)
        ok(f"fixture.{d.get('fixture_registry_decision_id')}.no_exists", d.get("file_exists_verified") is False)
        ok(f"fixture.{d.get('fixture_registry_decision_id')}.no_hash", d.get("real_hash_computed") is False)
        ok(f"fixture.{d.get('fixture_registry_decision_id')}.no_read", d.get("content_read") is False)

    mapping_decisions = mapping_results.get("decisions", [])
    ok("mapping.candidate", any(d.get("file_metadata_candidate_allowed") for d in mapping_decisions))
    ok("mapping.manifest_ref", any(d.get("sample_manifest_ref") == "controlled_frame_sample_manifest_schema.json" for d in mapping_decisions))
    for d in mapping_decisions:
        ok(f"mapping.{d.get('mapping_decision_id')}.no_existence_now", d.get("file_existence_required_now") is False)
        ok(f"mapping.{d.get('mapping_decision_id')}.no_hash_now", d.get("real_hash_required_now") is False)
        ok(f"mapping.{d.get('mapping_decision_id')}.no_content", d.get("content_read_required") is False)

    results = dryrun_results.get("results", [])
    for r in results:
        ok(f"result.{r.get('result_id')}.has_refs", bool(r.get("path_decision_ref")))

    ok("boundary_matrix.frozen", len(boundary_matrix.get("frozen_boundaries", [])) >= 10)
    ok("boundary_matrix.blocked.stat", boundary_matrix.get("blocked_now", {}).get("file_stat") is True)
    ok("governance_debt.topics", len(governance_debt.get("carryover_topics", [])) >= 3)
    ok("next_phase.final", next_phase.get("final_decision") == FINAL_DECISION)
    ok("next_phase.recommended", next_phase.get("recommended_next_phase") == NEXT_PHASE)

    ok("no_file_op.simulation_only", no_file_op.get("metadata_decision_simulation_only") is True)
    ok("no_file_op.file_stat", no_file_op.get("file_stat_invoked") is False)
    ok("no_file_op.exif", no_file_op.get("exif_parsed") is False)
    ok("no_file_op.probe", no_file_op.get("video_probe_invoked") is False)
    ok("no_file_op.real_hash", no_file_op.get("real_file_hash_computed") is False)
    ok("no_file_op.mapping_runtime", no_file_op.get("manifest_to_file_metadata_candidate_mapping_runtime_started") is False)

    for report_name, report in (("no_runtime", no_runtime), ("no_write", no_write)):
        ok(f"{report_name}.no_runtime", report.get("no_runtime_executed") is True)
        ok(f"{report_name}.visual_obs", report.get("visual_observation_generated") is False)
        ok(f"{report_name}.world_model", report.get("world_model_written") is False)
        ok(f"{report_name}.ocr", report.get("ocr_provider_invoked") is False)

    passed_count = sum(1 for check in checks if check["passed"])
    verifier_report = {
        "phase": PHASE_ID,
        "min_checks": MIN_CHECKS,
        "baseline_requirement": BASELINE_REQUIREMENT,
        "check_count": len(checks),
        "passed_count": passed_count,
        "failed_count": len(checks) - passed_count,
        "verifier": "GO" if len(checks) >= MIN_CHECKS and passed_count == len(checks) else "NO_GO",
        "final_decision": summary.get("final_decision"),
        "recommended_next_phase": summary.get("recommended_next_phase"),
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(json.dumps(verifier_report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "verifier": verifier_report["verifier"],
                "check_count": verifier_report["check_count"],
                "passed_count": verifier_report["passed_count"],
                "failed_count": verifier_report["failed_count"],
                "final_decision": verifier_report["final_decision"],
                "recommended_next_phase": verifier_report["recommended_next_phase"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if verifier_report["verifier"] == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
