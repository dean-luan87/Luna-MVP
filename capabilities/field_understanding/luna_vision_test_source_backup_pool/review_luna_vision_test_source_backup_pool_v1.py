# -*- coding: utf-8 -*-
"""Luna Vision Test Source Backup Pool — review v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.luna_vision_test_source_backup_pool.luna_vision_test_source_backup_pool_registry_v1 import (
    REGISTRY_ID,
    build_backup_pool_matrix_v1,
    validate_registry,
)
from capabilities.field_understanding.luna_vision_test_source_backup_pool.luna_vision_test_source_backup_pool_types_v1 import (
    COMMERCIAL_USE_DEFAULT,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    INTERFACE_ADAPTER_REF,
    NEXT_PHASE_REF,
    NON_EXECUTION_FLAGS,
    PHASE_ID,
    POOL_GOVERNANCE_RULES,
    POOL_PRINCIPLE_ZH,
    SOURCE_REGISTERED_GO_KEYS,
    SYSTEM_OBJECTIVE,
    TARGET_ENTRYPOINT,
    TARGET_INTERNAL_FORMAT,
    TEST_SOURCE_POOL_MODE,
    VISION_HARDWARE_BASELINE,
)
from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT / "_tmp_eval_out" / "luna_vision_test_source_backup_pool_v1_smoke_v0"
)
REVIEW_FILENAME = "luna_vision_test_source_backup_pool_review_v1.json"

_PKG = "capabilities/field_understanding/luna_vision_test_source_backup_pool"
STEP_FILES = (
    f"{_PKG}/luna_vision_test_source_backup_pool_types_v1.py",
    f"{_PKG}/luna_vision_test_source_backup_pool_registry_v1.py",
    f"{_PKG}/review_luna_vision_test_source_backup_pool_v1.py",
)

_REQUIRED_VERIFY_FLAGS: Tuple[str, ...] = (
    "rgb_vision_planning_go_verified",
    "rtab_multi_export_spatial_evidence_replay_closure_go_verified",
    "field_task_guidance_safety_chain_closure_go_verified",
    "interface_layer_governance_verified",
    "model_admission_governance_verified",
)


def _load_upstream_artifact(artifact_rel: str) -> Tuple[Optional[Dict[str, Any]], bool]:
    path = _REPO_ROOT / artifact_rel
    if not path.is_file():
        return None, False
    try:
        return json.loads(path.read_text(encoding="utf-8")), True
    except (OSError, json.JSONDecodeError):
        return None, True


def review_sealed_upstream_artifacts(matrix: Dict[str, Any]) -> Tuple[Dict[str, bool], List[str]]:
    issues: List[str] = []
    checks: Dict[str, bool] = {}

    for entry in matrix.get("sealed_upstream_go_artifacts") or []:
        phase_ref = entry["phase_ref"]
        module_path = _REPO_ROOT / entry["module_rel"]
        checks[f"{phase_ref}.module_present"] = module_path.is_file()
        if not module_path.is_file():
            issues.append(f"upstream_module_missing:{phase_ref}")

        artifact, exists = _load_upstream_artifact(entry["artifact_rel"])
        checks[f"{phase_ref}.artifact_present"] = exists
        if not exists:
            if entry.get("require_go", True):
                issues.append(f"upstream_artifact_missing:{phase_ref}")
            continue

        actual_go = (artifact or {}).get("final_decision")
        go_ok = actual_go == entry["expected_go"]
        checks[f"{phase_ref}.go_sealed"] = go_ok
        if not go_ok:
            issues.append(f"upstream_go_mismatch:{phase_ref}:{actual_go!r}")

        verify_flag = entry.get("verify_flag")
        if verify_flag:
            checks[verify_flag] = go_ok

    checks["controlled_trial_governance_template_ref_ok"] = (
        CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF == TEMPLATE_ID
    )
    for required in _REQUIRED_VERIFY_FLAGS:
        if not checks.get(required, False):
            issues.append(f"{required}_not_verified")

    return checks, issues


def review_luna_vision_test_source_backup_pool_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
) -> Dict[str, Any]:
    matrix = build_backup_pool_matrix_v1()
    registry_ok, registry_issues = validate_registry()

    failed_checks: List[str] = []
    passed_checks: List[str] = []

    for rel in STEP_FILES:
        if (_REPO_ROOT / rel).is_file():
            passed_checks.append(f"step.file_present={rel.split('/')[-1]}")
        else:
            failed_checks.append(f"step.file_missing={rel}")

    if registry_ok:
        passed_checks.append("registry_validation_ok=true")
    else:
        failed_checks.extend(registry_issues)

    upstream_checks, upstream_issues = review_sealed_upstream_artifacts(matrix)
    failed_checks.extend(upstream_issues)

    profile = matrix.get("backup_pool_profile") or {}
    license_policy = matrix.get("license_admission_policy") or {}
    annotation_policy = matrix.get("annotation_format_policy") or {}
    mapping_policy = matrix.get("evidence_candidate_mapping_policy") or {}
    risk_policy = matrix.get("risk_policy") or {}
    source_registered = matrix.get("source_registered_map") or {}

    template_ok = profile.get("controlled_trial_governance_template_ref") == TEMPLATE_ID

    review_checkpoints: Dict[str, Any] = {
        "backup_pool_profile_count": 1,
        "registry_item_count": matrix.get("registry_item_count", 0),
        "p0_source_count": matrix.get("p0_source_count", 0),
        "p1_source_count": matrix.get("p1_source_count", 0),
        "p2_source_count": matrix.get("p2_source_count", 0),
        "rgb_vision_planning_go_verified": upstream_checks.get(
            "rgb_vision_planning_go_verified", False
        ),
        "rtab_multi_export_spatial_evidence_replay_closure_go_verified": upstream_checks.get(
            "rtab_multi_export_spatial_evidence_replay_closure_go_verified", False
        ),
        "field_task_guidance_safety_chain_closure_go_verified": upstream_checks.get(
            "field_task_guidance_safety_chain_closure_go_verified", False
        ),
        "interface_layer_governance_verified": upstream_checks.get(
            "interface_layer_governance_verified", False
        ),
        "model_admission_governance_verified": upstream_checks.get(
            "model_admission_governance_verified", False
        ),
        "controlled_trial_governance_template_ref_ok": template_ok,
        "license_ref_required_for_all": license_policy.get("license_ref_required") is True,
        "source_chain_required_for_all": license_policy.get("source_chain_required") is True,
        "annotation_origin_required_for_all": license_policy.get("annotation_origin_required")
        is True,
        "sample_origin_required_for_all": license_policy.get("sample_origin_required") is True,
        "commercial_use_unknown_until_verified": (
            license_policy.get("commercial_use_unknown_until_verified") is True
            and COMMERCIAL_USE_DEFAULT == "unknown_until_license_verified"
        ),
        "non_commercial_sources_marked_research_test_only": (
            license_policy.get("non_commercial_marked_research_test_only") is True
        ),
        "roboflow_per_dataset_license_required": (
            license_policy.get("per_dataset_license_required_for_roboflow") is True
        ),
        "dataset_label_not_fact": annotation_policy.get("dataset_label_not_fact") is True,
        "annotation_as_evidence_candidate": (
            annotation_policy.get("annotation_as_evidence_candidate") is True
        ),
        "interface_adapter_required": mapping_policy.get("interface_adapter_required") is True,
        "native_output_direct_to_field_blocked": (
            mapping_policy.get("native_output_direct_to_field_blocked") is True
        ),
        "integrated_replay_compatible_for_all": (
            mapping_policy.get("integrated_replay_compatible_for_all") is True
        ),
        "rgb_first_hardware_baseline_preserved": (
            risk_policy.get("rgb_first_hardware_baseline_preserved") is True
            and VISION_HARDWARE_BASELINE == "rgb_first_first_person_camera"
        ),
        "backup_pool_not_training_admission": (
            risk_policy.get("backup_pool_not_training_admission") is True
        ),
        "backup_pool_not_runtime_admission": (
            risk_policy.get("backup_pool_not_runtime_admission") is True
        ),
        **source_registered,
        "test_source_pool_mode_locked": TEST_SOURCE_POOL_MODE,
        "vision_hardware_baseline_locked": VISION_HARDWARE_BASELINE,
        "system_objective_locked": SYSTEM_OBJECTIVE,
        **NON_EXECUTION_FLAGS,
    }

    go_conditions = {
        "backup_pool_profile_count_eq_1": review_checkpoints["backup_pool_profile_count"] == 1,
        "registry_item_count_gte_14": review_checkpoints["registry_item_count"] >= 14,
        "p0_source_count_gte_7": review_checkpoints["p0_source_count"] >= 7,
        "p1_source_count_gte_3": review_checkpoints["p1_source_count"] >= 3,
        "p2_source_count_gte_4": review_checkpoints["p2_source_count"] >= 4,
        "rgb_vision_planning_go_verified": (
            review_checkpoints["rgb_vision_planning_go_verified"] is True
        ),
        "rtab_multi_export_spatial_evidence_replay_closure_go_verified": (
            review_checkpoints["rtab_multi_export_spatial_evidence_replay_closure_go_verified"]
            is True
        ),
        "field_task_guidance_safety_chain_closure_go_verified": (
            review_checkpoints["field_task_guidance_safety_chain_closure_go_verified"] is True
        ),
        "interface_layer_governance_verified": (
            review_checkpoints["interface_layer_governance_verified"] is True
        ),
        "model_admission_governance_verified": (
            review_checkpoints["model_admission_governance_verified"] is True
        ),
        "controlled_trial_governance_template_ref_ok": template_ok is True,
        **{key: source_registered.get(key) is True for key in SOURCE_REGISTERED_GO_KEYS},
        "license_ref_required_for_all": (
            review_checkpoints["license_ref_required_for_all"] is True
        ),
        "source_chain_required_for_all": (
            review_checkpoints["source_chain_required_for_all"] is True
        ),
        "annotation_origin_required_for_all": (
            review_checkpoints["annotation_origin_required_for_all"] is True
        ),
        "sample_origin_required_for_all": (
            review_checkpoints["sample_origin_required_for_all"] is True
        ),
        "commercial_use_unknown_until_verified": (
            review_checkpoints["commercial_use_unknown_until_verified"] is True
        ),
        "non_commercial_sources_marked_research_test_only": (
            review_checkpoints["non_commercial_sources_marked_research_test_only"] is True
        ),
        "roboflow_per_dataset_license_required": (
            review_checkpoints["roboflow_per_dataset_license_required"] is True
        ),
        "dataset_label_not_fact": review_checkpoints["dataset_label_not_fact"] is True,
        "annotation_as_evidence_candidate": (
            review_checkpoints["annotation_as_evidence_candidate"] is True
        ),
        "interface_adapter_required": review_checkpoints["interface_adapter_required"] is True,
        "integrated_replay_compatible_for_all": (
            review_checkpoints["integrated_replay_compatible_for_all"] is True
        ),
        "rgb_first_hardware_baseline_preserved": (
            review_checkpoints["rgb_first_hardware_baseline_preserved"] is True
        ),
        "backup_pool_not_training_admission": (
            review_checkpoints["backup_pool_not_training_admission"] is True
        ),
        "backup_pool_not_runtime_admission": (
            review_checkpoints["backup_pool_not_runtime_admission"] is True
        ),
        "integrated_validation_mode_required": (
            review_checkpoints["integrated_validation_mode_required"] is True
        ),
        "single_loader_validation_not_used": (
            review_checkpoints["single_loader_validation_not_used"] is True
        ),
        "training_use_allowed_false": review_checkpoints["training_use_allowed"] is False,
        "dataset_download_allowed_false": review_checkpoints["dataset_download_allowed"] is False,
        "runtime_activation_allowed_false": (
            review_checkpoints["runtime_activation_allowed"] is False
        ),
        "live_camera_connected_false": review_checkpoints["live_camera_connected"] is False,
        "live_sensor_connected_false": review_checkpoints["live_sensor_connected"] is False,
        "real_map_api_connected_false": review_checkpoints["real_map_api_connected"] is False,
        "real_gps_connected_false": review_checkpoints["real_gps_connected"] is False,
        "ros_connected_false": review_checkpoints["ros_connected"] is False,
        "real_navigation_started_false": review_checkpoints["real_navigation_started"] is False,
        "direct_action_allowed_false": review_checkpoints["direct_action_allowed"] is False,
        "direct_speech_allowed_false": review_checkpoints["direct_speech_allowed"] is False,
        "direct_fact_write_allowed_false": (
            review_checkpoints["direct_fact_write_allowed"] is False
        ),
        "commercial_runtime_approved_false": (
            review_checkpoints["commercial_runtime_approved"] is False
        ),
    }

    for key, ok in go_conditions.items():
        if ok:
            passed_checks.append(f"go.{key}=true")
        else:
            failed_checks.append(f"go.{key}=false")

    blocker_count = len(failed_checks)
    review_ok = registry_ok and blocker_count == 0

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "Luna Vision Test Source Backup Pool Review",
        "lifecycle_variant": "rgb_first_vision_test_source_backup_pool_review",
        "pool_principle_zh": POOL_PRINCIPLE_ZH,
        "registry_id": REGISTRY_ID,
        "test_source_pool_mode": TEST_SOURCE_POOL_MODE,
        "vision_hardware_baseline": VISION_HARDWARE_BASELINE,
        "system_objective": SYSTEM_OBJECTIVE,
        "commercial_use_default": COMMERCIAL_USE_DEFAULT,
        "target_internal_format": TARGET_INTERNAL_FORMAT,
        "target_entrypoint": TARGET_ENTRYPOINT,
        "interface_adapter_ref": INTERFACE_ADAPTER_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "pool_governance_rules": list(POOL_GOVERNANCE_RULES),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "registry_validation_ok": registry_ok,
        "upstream_sealed_phase_review": upstream_checks,
        "go_conditions": go_conditions,
        "review_checkpoints": review_checkpoints,
        "backup_pool_matrix": matrix,
        "conclusions": {
            "luna_vision_test_source_backup_pool_status": (
                "vision_test_source_backup_pool_sealed" if review_ok else "blocked"
            ),
            "backup_pool_is_test_source_only": True,
            "backup_pool_not_training_main_data": True,
            "backup_pool_not_fact_source": True,
            "rgb_first_baseline_preserved": True,
            "integrated_validation_mode_required": True,
            "next_phase_ref": NEXT_PHASE_REF,
            "pipeline_summary": {
                "input": "open_public_research_vision_datasets",
                "admission": "license_source_admission_per_dataset",
                "adapter": INTERFACE_ADAPTER_REF,
                "internal_format": TARGET_INTERNAL_FORMAT,
                "bundle": "luna_evidence_candidate_sample",
                "path": "field_task_guidance_candidate_replay_path",
            },
            "transition_note": (
                "Vision test-source backup pool sealed (Roboflow + COCO/Open Images/LVIS/ADE20K/"
                "TextOCR/Visual Genome + BDD100K/Cityscapes/Mapillary Vistas + Ego4D/EPIC-KITCHENS/"
                "EgoTracks/RefEgo) as test/replay/benchmark sources only. Next: pick 3-5 lightweight "
                "sample sources for the integrated evidence replay dry-run."
            ),
        },
        "blocker_count": blocker_count,
        "failed_checks": failed_checks,
        "passed_checks": passed_checks,
        "final_decision": FINAL_DECISION_GO if review_ok else FINAL_DECISION_BLOCKED,
    }

    if write_file:
        out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
        out_root.mkdir(parents=True, exist_ok=True)
        out_path = out_root / REVIEW_FILENAME
        out_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        result["output_review_file"] = str(out_path)

    return result


def main() -> int:
    result = review_luna_vision_test_source_backup_pool_v1()
    cp = result["review_checkpoints"]
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "registry_item_count": cp["registry_item_count"],
                "p0_source_count": cp["p0_source_count"],
                "p1_source_count": cp["p1_source_count"],
                "p2_source_count": cp["p2_source_count"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
