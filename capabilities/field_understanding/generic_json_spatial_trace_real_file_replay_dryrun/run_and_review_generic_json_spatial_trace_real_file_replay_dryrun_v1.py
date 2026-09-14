# -*- coding: utf-8 -*-
"""Generic JSON Spatial Trace Real File Controlled Replay DryRun — run + review v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)
from capabilities.midplatform.core.dryrun_lifecycle_template_v1 import write_json_file
from capabilities.field_understanding.generic_json_spatial_trace_real_file_replay_dryrun.generic_json_spatial_trace_real_file_replay_dryrun_cases_v1 import (
    build_negative_cases_v1,
    build_positive_cases_v1,
    run_all_cases_v1,
    samples_dir,
)
from capabilities.field_understanding.generic_json_spatial_trace_real_file_replay_dryrun.generic_json_spatial_trace_real_file_replay_dryrun_types_v1 import (
    CONTROLLED_RUNTIME_TRIAL_GOVERNANCE_STATUS,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    DRYRUN_PRINCIPLE_ZH,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    GENERIC_JSON_SPATIAL_TRACE_PARSER_REF,
    NEGATIVE_CASE_REFS,
    NON_EXECUTION_FLAGS,
    PHASE_ID,
    PHASE_ONE_CHAIN_STATUS,
    PLANNING_REF,
    POSITIVE_CASE_REFS,
    RUNTIME_TRIAL_MODE,
    SAMPLE_FILES,
    SAMPLES_REL_DIR,
    SOURCE_CHAIN,
    TARGET_ENTRYPOINT,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT
    / "_tmp_eval_out"
    / "generic_json_spatial_trace_real_file_replay_dryrun_v1_smoke_v0"
)
OUTPUT_FILENAME = "generic_json_spatial_trace_real_file_replay_dryrun_run_and_review_v1.json"

_UPSTREAM_ARTIFACTS: Tuple[Dict[str, Any], ...] = (
    {
        "phase_ref": PLANNING_REF,
        "artifact_rel": (
            "_tmp_eval_out/generic_json_spatial_trace_real_file_replay_planning_v1_smoke_v0/"
            "generic_json_spatial_trace_real_file_replay_planning_review_v1.json"
        ),
        "expected_go": "GENERIC_JSON_SPATIAL_TRACE_REAL_FILE_CONTROLLED_REPLAY_PLANNING_GO",
        "module_rel": (
            "capabilities/field_understanding/generic_json_spatial_trace_real_file_replay_planning/"
            "generic_json_spatial_trace_real_file_replay_planning_types_v1.py"
        ),
        "require_go": True,
        "require_planning_go": True,
    },
    {
        "phase_ref": GENERIC_JSON_SPATIAL_TRACE_PARSER_REF,
        "artifact_rel": (
            "_tmp_eval_out/generic_json_spatial_trace_parser_v1_smoke_v0/"
            "generic_json_spatial_trace_parser_run_and_review_v1.json"
        ),
        "expected_go": "GENERIC_JSON_SPATIAL_TRACE_PARSER_REVIEW_GO",
        "module_rel": (
            "capabilities/field_understanding/generic_json_spatial_trace_parser/"
            "generic_json_spatial_trace_parser_types_v1.py"
        ),
        "require_go": True,
        "require_parser_go": True,
    },
    {
        "phase_ref": "Phase-Field-Task-Guidance-Safety-Chain-Closure-v1-001",
        "artifact_rel": (
            "_tmp_eval_out/field_task_guidance_safety_chain_closure_v1_smoke_v0/"
            "field_task_guidance_safety_chain_closure_review_v1.json"
        ),
        "expected_go": "FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_GO",
        "module_rel": (
            "capabilities/field_understanding/field_task_guidance_safety_chain_closure/"
            "field_task_guidance_safety_chain_closure_types_v1.py"
        ),
        "require_go": True,
        "require_phase_one_chain_sealed": True,
    },
    {
        "phase_ref": "Phase-PhaseOne-Environment-Cognition-Controlled-Runtime-Trial-Governance-Closure-v1-001",
        "artifact_rel": (
            "_tmp_eval_out/phase_one_environment_cognition_runtime_trial_governance_closure_v1_smoke_v0/"
            "phase_one_environment_cognition_runtime_trial_governance_closure_review_v1.json"
        ),
        "expected_go": (
            "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_GOVERNANCE_CLOSURE_GO"
        ),
        "module_rel": (
            "capabilities/field_understanding/phase_one_environment_cognition_runtime_trial_governance_closure/"
            "phase_one_environment_cognition_runtime_trial_governance_closure_types_v1.py"
        ),
        "require_go": True,
        "require_governance_sealed": True,
    },
    {
        "phase_ref": "Phase-PhaseOne-Environment-Cognition-Controlled-Runtime-Trial-Issuance-Package-v1-001",
        "artifact_rel": (
            "_tmp_eval_out/phase_one_environment_cognition_runtime_trial_issuance_package_v1_smoke_v0/"
            "phase_one_environment_cognition_runtime_trial_issuance_package_review_v1.json"
        ),
        "expected_go": "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_ISSUANCE_PACKAGE_GO",
        "module_rel": (
            "capabilities/field_understanding/phase_one_environment_cognition_runtime_trial_issuance_package/"
            "phase_one_environment_cognition_runtime_trial_issuance_package_types_v1.py"
        ),
        "require_go": True,
    },
    {
        "phase_ref": "Phase-Midplatform-Interface-Layer-Governance-Protocol-v1-001",
        "artifact_rel": (
            "_tmp_eval_out/interface_layer_governance_v1_smoke_v0/"
            "interface_layer_governance_review_v1.json"
        ),
        "expected_go": "INTERFACE_LAYER_GOVERNANCE_PROTOCOL_BASELINE_READY_FOR_ADOPTION",
        "module_rel": (
            "capabilities/midplatform/interface_layer_governance/"
            "interface_layer_governance_types_v1.py"
        ),
        "require_go": True,
    },
    {
        "phase_ref": "Phase-Midplatform-Model-Admission-Governance-Standard-v1-001",
        "artifact_rel": (
            "_tmp_eval_out/model_admission_governance_v1_smoke_v0/"
            "model_admission_governance_run_and_review_v1.json"
        ),
        "expected_go": "MODEL_ADMISSION_GOVERNANCE_STANDARD_REVIEW_GO",
        "module_rel": (
            "capabilities/midplatform/model_admission_governance/"
            "model_admission_governance_types_v1.py"
        ),
        "require_go": True,
    },
)


def _load_upstream_artifact(artifact_rel: str) -> Tuple[Optional[Dict[str, Any]], bool]:
    path = _REPO_ROOT / artifact_rel
    if not path.is_file():
        return None, False
    try:
        return json.loads(path.read_text(encoding="utf-8")), True
    except (OSError, json.JSONDecodeError):
        return None, True


def review_upstream_artifacts() -> Tuple[Dict[str, bool], List[str]]:
    issues: List[str] = []
    checks: Dict[str, bool] = {}

    for entry in _UPSTREAM_ARTIFACTS:
        phase_ref = entry["phase_ref"]
        module_path = _REPO_ROOT / entry["module_rel"]
        checks[f"{phase_ref}.module_present"] = module_path.is_file()
        if not module_path.is_file():
            issues.append(f"upstream_module_missing:{phase_ref}")

        artifact, exists = _load_upstream_artifact(entry["artifact_rel"])
        checks[f"{phase_ref}.artifact_present"] = exists
        if not exists:
            issues.append(f"upstream_artifact_missing:{phase_ref}")
            continue

        actual_go = (artifact or {}).get("final_decision")
        expected_go = entry["expected_go"]
        go_ok = actual_go == expected_go
        checks[f"{phase_ref}.go_sealed"] = go_ok
        if not go_ok:
            issues.append(f"upstream_go_mismatch:{phase_ref}:{actual_go!r}")

        if entry.get("require_planning_go"):
            checks["planning_go_verified"] = go_ok
        if entry.get("require_parser_go"):
            checks["generic_json_spatial_trace_parser_go_verified"] = go_ok
        if entry.get("require_phase_one_chain_sealed") and artifact:
            sealed = (
                artifact.get("conclusions", {}).get("phase_one_environment_cognition_chain_status")
                == "sealed"
                or artifact.get("conclusions", {}).get("master_chain_sealed") is True
            )
            checks["phase_one_chain_sealed_verified"] = sealed
            if not sealed:
                issues.append("phase_one_chain_not_sealed")
        if entry.get("require_governance_sealed") and artifact:
            gov_sealed = (
                artifact.get("conclusions", {}).get("governance_closure_status") == "sealed"
                or artifact.get("final_decision")
                == "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_GOVERNANCE_CLOSURE_GO"
            )
            checks["controlled_runtime_trial_governance_sealed_verified"] = gov_sealed
            if not gov_sealed:
                issues.append("controlled_runtime_trial_governance_not_sealed")

    checks["controlled_trial_governance_template_ref_ok"] = (
        CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF == TEMPLATE_ID
    )
    if not checks.get("planning_go_verified", False):
        issues.append("planning_go_not_verified")
    if not checks.get("generic_json_spatial_trace_parser_go_verified", False):
        issues.append("parser_go_not_verified")
    if not checks.get("phase_one_chain_sealed_verified", False):
        issues.append("phase_one_chain_sealed_not_verified")
    if not checks.get("controlled_runtime_trial_governance_sealed_verified", False):
        issues.append("governance_sealed_not_verified")

    return checks, issues


def _aggregate_case_results(case_run: Dict[str, Any]) -> Dict[str, bool]:
    positive = case_run.get("positive_cases") or []
    negative = case_run.get("negative_cases") or []

    positive_pass = sum(1 for c in positive if c.get("passed"))
    negative_pass = sum(1 for c in negative if c.get("passed"))

    by_ref = {c["case_ref"]: c for c in positive + negative}

    pose = by_ref.get("real_file_pose_motion_low_risk_replay", {})
    health = by_ref.get("real_file_odometry_health_replay", {})
    anchor = by_ref.get("real_file_anchor_relocalization_drift_replay", {})
    fusion = by_ref.get("real_file_spatial_fusion_replay", {})
    guidance = by_ref.get("real_file_field_task_guidance_replay_path", {})
    missing = by_ref.get("invalid_missing_source_chain_rejected", {})
    unsupported = by_ref.get("invalid_unsupported_candidate_type_rejected", {})
    backend = by_ref.get("invalid_backend_native_direct_to_field_rejected", {})
    escalation = by_ref.get("invalid_runtime_escalation_rejected", {})

    sample_count = sum(1 for name in SAMPLE_FILES if (samples_dir() / name).is_file())

    return {
        "positive_case_count": len(positive),
        "negative_case_count": len(negative),
        "positive_pass_count": positive_pass,
        "invalid_expected_reject_count": negative_pass,
        "sample_file_count": sample_count,
        "local_file_read_used": any(
            (c.get("checks") or {}).get("local_file_read_used") for c in positive[:4]
        ),
        "file_source_admission_required": all(
            (c.get("admission") or {}).get("file_origin_metadata_present") is not False
            for c in positive[:4]
            if c.get("admission")
        ),
        "file_origin_metadata_required": all(
            (c.get("admission") or {}).get("file_origin_metadata_present") is True
            for c in positive[:4]
            if c.get("admission")
        ),
        "source_chain_required": all(
            not (c.get("parsed_result") or {}).get("parse_errors")
            for c in positive[:4]
            if c.get("passed")
        ),
        "generic_json_parser_reused": True,
        "candidate_bundle_mapping_ok": all(
            (c.get("bundle_result") or {}).get("candidate_bundle_mapping_ok") is True
            for c in positive[:4]
            if c.get("passed")
        ),
        "pose_motion_replay_ok": pose.get("passed") is True,
        "odometry_health_replay_ok": health.get("passed") is True,
        "anchor_relocalization_drift_replay_ok": anchor.get("passed") is True,
        "spatial_fusion_replay_ok": fusion.get("passed") is True,
        "field_task_guidance_replay_path_ok": guidance.get("passed") is True,
        "missing_source_chain_rejected": (missing.get("checks") or {}).get(
            "missing_source_chain_rejected"
        )
        is True,
        "unsupported_candidate_type_rejected": (unsupported.get("checks") or {}).get(
            "unsupported_candidate_type_rejected"
        )
        is True,
        "backend_native_output_direct_to_field_blocked": (backend.get("checks") or {}).get(
            "backend_native_output_direct_to_field_blocked"
        )
        is True,
        "relocalization_does_not_restore_runtime_trust": (anchor.get("checks") or {}).get(
            "relocalization_does_not_restore_runtime_trust"
        )
        is True,
        "gps_does_not_override_field_identity": (fusion.get("path_trace") or {}).get(
            "gps_does_not_override_field_identity"
        )
        is True,
        "candidate_only_replay_path_enforced": all(
            (c.get("path_trace") or {}).get("candidate_only") is True
            for c in positive
            if c.get("path_trace")
        ),
    }


def run_and_review_generic_json_spatial_trace_real_file_replay_dryrun_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
) -> Dict[str, Any]:
    case_run = run_all_cases_v1()
    upstream_checks, upstream_issues = review_upstream_artifacts()
    aggregate = _aggregate_case_results(case_run)

    failed_checks: List[str] = list(upstream_issues)
    passed_checks: List[str] = []

    go_conditions = {
        "positive_case_count_eq_5": aggregate["positive_case_count"] == 5,
        "negative_case_count_eq_4": aggregate["negative_case_count"] == 4,
        "positive_pass_count_eq_5": aggregate["positive_pass_count"] == 5,
        "invalid_expected_reject_count_eq_4": aggregate["invalid_expected_reject_count"] == 4,
        "planning_go_verified": upstream_checks.get("planning_go_verified") is True,
        "controlled_trial_governance_template_ref_ok": (
            upstream_checks.get("controlled_trial_governance_template_ref_ok") is True
        ),
        "phase_one_chain_sealed_verified": (
            upstream_checks.get("phase_one_chain_sealed_verified") is True
        ),
        "controlled_runtime_trial_governance_sealed_verified": (
            upstream_checks.get("controlled_runtime_trial_governance_sealed_verified") is True
        ),
        "generic_json_spatial_trace_parser_go_verified": (
            upstream_checks.get("generic_json_spatial_trace_parser_go_verified") is True
        ),
        "sample_file_count_gte_5": aggregate["sample_file_count"] >= 5,
        "local_file_read_used": aggregate["local_file_read_used"] is True,
        "file_source_admission_required": aggregate["file_source_admission_required"] is True,
        "file_origin_metadata_required": aggregate["file_origin_metadata_required"] is True,
        "source_chain_required": aggregate["source_chain_required"] is True,
        "generic_json_parser_reused": aggregate["generic_json_parser_reused"] is True,
        "candidate_bundle_mapping_ok": aggregate["candidate_bundle_mapping_ok"] is True,
        "pose_motion_replay_ok": aggregate["pose_motion_replay_ok"] is True,
        "odometry_health_replay_ok": aggregate["odometry_health_replay_ok"] is True,
        "anchor_relocalization_drift_replay_ok": (
            aggregate["anchor_relocalization_drift_replay_ok"] is True
        ),
        "spatial_fusion_replay_ok": aggregate["spatial_fusion_replay_ok"] is True,
        "field_task_guidance_replay_path_ok": aggregate["field_task_guidance_replay_path_ok"] is True,
        "backend_native_output_direct_to_field_blocked": (
            aggregate["backend_native_output_direct_to_field_blocked"] is True
        ),
        "unsupported_candidate_type_rejected": aggregate["unsupported_candidate_type_rejected"] is True,
        "missing_source_chain_rejected": aggregate["missing_source_chain_rejected"] is True,
        "relocalization_does_not_restore_runtime_trust": (
            aggregate["relocalization_does_not_restore_runtime_trust"] is True
        ),
        "gps_does_not_override_field_identity": (
            aggregate["gps_does_not_override_field_identity"] is True
        ),
        "candidate_only_replay_path_enforced": aggregate["candidate_only_replay_path_enforced"] is True,
        "real_file_replay_execution_allowed_true": NON_EXECUTION_FLAGS["real_file_replay_execution_allowed"] is True,
        "runtime_activation_allowed_false": NON_EXECUTION_FLAGS["runtime_activation_allowed"] is False,
        "live_sensor_connected_false": NON_EXECUTION_FLAGS["live_sensor_connected"] is False,
        "real_navigation_started_false": NON_EXECUTION_FLAGS["real_navigation_started"] is False,
        "real_map_api_connected_false": NON_EXECUTION_FLAGS["real_map_api_connected"] is False,
        "real_gps_connected_false": NON_EXECUTION_FLAGS["real_gps_connected"] is False,
        "ros_connected_false": NON_EXECUTION_FLAGS["ros_connected"] is False,
        "camera_connected_false": NON_EXECUTION_FLAGS["camera_connected"] is False,
        "imu_connected_false": NON_EXECUTION_FLAGS["imu_connected"] is False,
        "direct_action_allowed_false": NON_EXECUTION_FLAGS["direct_action_allowed"] is False,
        "direct_speech_allowed_false": NON_EXECUTION_FLAGS["direct_speech_allowed"] is False,
        "direct_fact_write_allowed_false": NON_EXECUTION_FLAGS["direct_fact_write_allowed"] is False,
        "commercial_runtime_approved_false": NON_EXECUTION_FLAGS["commercial_runtime_approved"] is False,
    }

    for key, ok in go_conditions.items():
        if ok:
            passed_checks.append(f"go.{key}=true")
        else:
            failed_checks.append(f"go.{key}=false")

    blocker_count = len(failed_checks)
    review_ok = blocker_count == 0

    review_checkpoints = {
        **aggregate,
        **upstream_checks,
        "runtime_trial_mode": RUNTIME_TRIAL_MODE,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "planning_ref": PLANNING_REF,
        "generic_json_spatial_trace_parser_ref": GENERIC_JSON_SPATIAL_TRACE_PARSER_REF,
        "target_entrypoint": TARGET_ENTRYPOINT,
        "phase_one_chain_status": PHASE_ONE_CHAIN_STATUS,
        "controlled_runtime_trial_governance_status": CONTROLLED_RUNTIME_TRIAL_GOVERNANCE_STATUS,
        "samples_rel_dir": SAMPLES_REL_DIR,
        **NON_EXECUTION_FLAGS,
    }

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    out_path = out_root / OUTPUT_FILENAME

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "Generic JSON Spatial Trace Real File Controlled Replay DryRun Run + Review",
        "lifecycle_variant": "compressed_real_file_replay_dryrun",
        "dryrun_principle_zh": DRYRUN_PRINCIPLE_ZH,
        "source_chain": SOURCE_CHAIN,
        "runtime_trial_mode": RUNTIME_TRIAL_MODE,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "planning_ref": PLANNING_REF,
        "generic_json_spatial_trace_parser_ref": GENERIC_JSON_SPATIAL_TRACE_PARSER_REF,
        "target_entrypoint": TARGET_ENTRYPOINT,
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "positive_case_refs": list(POSITIVE_CASE_REFS),
        "negative_case_refs": list(NEGATIVE_CASE_REFS),
        "sample_files": list(SAMPLE_FILES),
        "samples_rel_dir": SAMPLES_REL_DIR,
        "positive_cases": build_positive_cases_v1(),
        "negative_cases": build_negative_cases_v1(),
        "case_run": case_run,
        "upstream_sealed_phase_review": upstream_checks,
        "go_conditions": go_conditions,
        "review_checkpoints": review_checkpoints,
        "conclusions": {
            "real_file_replay_dryrun_status": "ready_for_export_loader_planning" if review_ok else "blocked",
            "real_file_replay_dryrun_not_live_runtime": True,
            "local_file_read_used": aggregate["local_file_read_used"],
            "generic_json_parser_reused": True,
            "trial_runtime_started": False,
            "next_phase_ref": "Phase-Generic-JSON-Spatial-Trace-Real-File-Export-Loader-Planning-v1-001",
            "transition_note": (
                "Completed first step from mock fixture to real offline file replay. "
                "Next: TUM / RTAB export loader or converter planning."
            ),
        },
        "output_root": str(out_root),
        "output_file": str(out_path),
        "blocker_count": blocker_count,
        "failed_checks": failed_checks,
        "passed_checks": passed_checks,
        "final_decision": FINAL_DECISION_GO if review_ok else FINAL_DECISION_BLOCKED,
    }

    # Serialize dataclass case definitions in result
    result["positive_cases"] = [
        {
            "case_ref": c.case_ref,
            "case_kind": c.case_kind,
            "sample_file": c.sample_file,
            "expected_outcome": c.expected_outcome,
            "source_chain": c.source_chain,
        }
        for c in build_positive_cases_v1()
    ]
    result["negative_cases"] = [
        {
            "case_ref": c.case_ref,
            "case_kind": c.case_kind,
            "sample_file": c.sample_file,
            "expected_outcome": c.expected_outcome,
            "source_chain": c.source_chain,
        }
        for c in build_negative_cases_v1()
    ]

    if write_file:
        write_json_file(out_path, result)

    return result


def main() -> int:
    result = run_and_review_generic_json_spatial_trace_real_file_replay_dryrun_v1()
    checkpoints = result["review_checkpoints"]
    print(
        json.dumps(
            {
                "output_file": result.get("output_file"),
                "positive_pass_count": checkpoints.get("positive_pass_count"),
                "invalid_expected_reject_count": checkpoints.get("invalid_expected_reject_count"),
                "sample_file_count": checkpoints.get("sample_file_count"),
                "candidate_bundle_mapping_ok": checkpoints.get("candidate_bundle_mapping_ok"),
                "real_file_replay_execution_allowed": checkpoints.get("real_file_replay_execution_allowed"),
                "runtime_activation_allowed": checkpoints.get("runtime_activation_allowed"),
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
