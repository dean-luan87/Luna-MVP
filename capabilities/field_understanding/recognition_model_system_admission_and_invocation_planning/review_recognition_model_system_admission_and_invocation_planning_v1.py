# -*- coding: utf-8 -*-
"""Recognition Model System Admission and Invocation Planning — review v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.recognition_model_system_admission_and_invocation_planning.recognition_model_system_admission_and_invocation_planning_registry_v1 import (
    REGISTRY_ID,
    build_recognition_model_system_admission_matrix_v1,
    validate_registry,
)
from capabilities.field_understanding.recognition_model_system_admission_and_invocation_planning.recognition_model_system_admission_and_invocation_planning_types_v1 import (
    ADMISSION_ORDER,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    INTERFACE_ADAPTER_REF,
    INVOCATION_FEASIBILITY_CHECK_ITEMS,
    MODEL_FAMILY_IDS,
    NEXT_PHASE_REF,
    NON_EXECUTION_FLAGS,
    ORDER_ENFORCEMENT_FLAGS,
    PHASE_ID,
    PLANNING_GOVERNANCE_RULES,
    PLANNING_PRINCIPLE_ZH,
    RUNTIME_TRIAL_MODE,
    SOURCE_CHAIN,
    TARGET_CHAIN_REF,
    TARGET_ENTRYPOINT,
)
from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT
    / "_tmp_eval_out"
    / "recognition_model_system_admission_and_invocation_planning_v1_smoke_v0"
)
REVIEW_FILENAME = "recognition_model_system_admission_and_invocation_planning_review_v1.json"

_PKG = (
    "capabilities/field_understanding/"
    "recognition_model_system_admission_and_invocation_planning"
)
STEP_FILES = (
    f"{_PKG}/recognition_model_system_admission_and_invocation_planning_types_v1.py",
    f"{_PKG}/recognition_model_system_admission_and_invocation_planning_registry_v1.py",
    f"{_PKG}/review_recognition_model_system_admission_and_invocation_planning_v1.py",
)

_REQUIRED_VERIFY_FLAGS: Tuple[str, ...] = (
    "phase_one_evidence_main_chain_closure_go_verified",
    "rgb_vision_evidence_chain_closure_go_verified",
    "slam_backend_evidence_chain_closure_go_verified",
    "rgb_slam_cross_modal_closure_go_verified",
    "field_task_guidance_safety_chain_closure_go_verified",
    "runtime_governance_closure_go_verified",
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


def review_recognition_model_system_admission_and_invocation_planning_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
) -> Dict[str, Any]:
    matrix = build_recognition_model_system_admission_matrix_v1()
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

    profile = matrix.get("planning_profile") or {}
    families = {p["model_family_id"]: p for p in matrix.get("family_admission_policies") or []}
    invocation = {
        p["model_family_id"]: p for p in matrix.get("invocation_feasibility_policies") or []
    }
    outputs = {p["model_family_id"]: p for p in matrix.get("output_requirement_policies") or []}
    adapters = {p["model_family_id"]: p for p in matrix.get("adapter_readiness_policies") or []}
    runtime_b = matrix.get("runtime_boundary_policy") or {}

    template_ok = profile.get("controlled_trial_governance_template_ref") == TEMPLATE_ID

    family_admission_planned = {
        f"{fid}_admission_planned": families.get(fid, {}).get("admission_planned") is True
        for fid in MODEL_FAMILY_IDS
    }

    # Invocation feasibility check items must hold across all families.
    def _all_families_true(policy_map: Dict[str, Dict[str, Any]], field: str) -> bool:
        return all(policy_map.get(fid, {}).get(field) is True for fid in MODEL_FAMILY_IDS)

    invocation_checks = {
        "callable_interface_required": _all_families_true(invocation, "callable_interface_defined"),
        "input_format_required": _all_families_true(invocation, "input_format_defined"),
        "output_schema_required": _all_families_true(invocation, "output_schema_defined"),
        "runtime_requirement_declared": _all_families_true(
            invocation, "local_or_target_runtime_requirement_declared"
        ),
        "license_ref_required": _all_families_true(invocation, "license_ref_required"),
        "model_origin_required": _all_families_true(invocation, "model_origin_required"),
        "dependency_boundary_declared": _all_families_true(
            invocation, "dependency_boundary_declared"
        ),
        "resource_requirement_declared": _all_families_true(
            invocation, "resource_requirement_declared"
        ),
        "offline_or_online_mode_declared": _all_families_true(
            invocation, "offline_or_online_mode_declared"
        ),
        "adapter_mapping_target_declared": _all_families_true(
            invocation, "adapter_mapping_target_declared"
        ),
    }

    output_checks = {
        "model_output_source_chain_required": _all_families_true(outputs, "source_chain_required"),
        "model_output_confidence_required": _all_families_true(outputs, "confidence_required"),
        "model_output_adapter_mapping_ref_required": _all_families_true(
            outputs, "adapter_mapping_ref_required"
        ),
        "model_output_allowed_use_required": _all_families_true(outputs, "allowed_use_required"),
        "model_output_commercial_use_status_required": _all_families_true(
            outputs, "commercial_use_status_required"
        ),
    }

    adapter_native_blocked = _all_families_true(
        adapters, "native_model_output_direct_to_field_blocked"
    )

    go_conditions = {
        "planning_profile_count_eq_1": True,
        "model_family_policy_count_gte_7": matrix.get("model_family_policy_count", 0) >= 7,
        "invocation_feasibility_policy_count_gte_7": (
            matrix.get("invocation_feasibility_policy_count", 0) >= 7
        ),
        "output_requirement_policy_count_gte_7": (
            matrix.get("output_requirement_policy_count", 0) >= 7
        ),
        "adapter_readiness_policy_count_gte_7": (
            matrix.get("adapter_readiness_policy_count", 0) >= 7
        ),
        "phase_one_evidence_main_chain_closure_go_verified": (
            upstream_checks.get("phase_one_evidence_main_chain_closure_go_verified") is True
        ),
        "rgb_vision_evidence_chain_closure_go_verified": (
            upstream_checks.get("rgb_vision_evidence_chain_closure_go_verified") is True
        ),
        "slam_backend_evidence_chain_closure_go_verified": (
            upstream_checks.get("slam_backend_evidence_chain_closure_go_verified") is True
        ),
        "rgb_slam_cross_modal_closure_go_verified": (
            upstream_checks.get("rgb_slam_cross_modal_closure_go_verified") is True
        ),
        "field_task_guidance_safety_chain_closure_go_verified": (
            upstream_checks.get("field_task_guidance_safety_chain_closure_go_verified") is True
        ),
        "runtime_governance_closure_go_verified": (
            upstream_checks.get("runtime_governance_closure_go_verified") is True
        ),
        "interface_layer_governance_verified": (
            upstream_checks.get("interface_layer_governance_verified") is True
        ),
        "model_admission_governance_verified": (
            upstream_checks.get("model_admission_governance_verified") is True
        ),
        "controlled_trial_governance_template_ref_ok": template_ok is True,
        **family_admission_planned,
        **invocation_checks,
        **output_checks,
        **{k: (v is True) for k, v in ORDER_ENFORCEMENT_FLAGS.items()},
        "model_system_admission_planning_only": (
            NON_EXECUTION_FLAGS["model_system_admission_planning_only"] is True
        ),
        "model_invocation_execution_allowed_false": (
            NON_EXECUTION_FLAGS["model_invocation_execution_allowed"] is False
        ),
        "model_output_adapter_dryrun_allowed_false": (
            NON_EXECUTION_FLAGS["model_output_adapter_dryrun_allowed"] is False
        ),
        "real_inference_allowed_false": NON_EXECUTION_FLAGS["real_inference_allowed"] is False,
        "model_tuning_allowed_false": NON_EXECUTION_FLAGS["model_tuning_allowed"] is False,
        "dataset_usage_allowed_false": NON_EXECUTION_FLAGS["dataset_usage_allowed"] is False,
        "training_use_allowed_false": NON_EXECUTION_FLAGS["training_use_allowed"] is False,
        "dataset_download_allowed_false": NON_EXECUTION_FLAGS["dataset_download_allowed"] is False,
        "runtime_activation_allowed_false": (
            NON_EXECUTION_FLAGS["runtime_activation_allowed"] is False
        ),
        "live_camera_connected_false": NON_EXECUTION_FLAGS["live_camera_connected"] is False,
        "live_sensor_connected_false": NON_EXECUTION_FLAGS["live_sensor_connected"] is False,
        "direct_action_allowed_false": NON_EXECUTION_FLAGS["direct_action_allowed"] is False,
        "direct_speech_allowed_false": NON_EXECUTION_FLAGS["direct_speech_allowed"] is False,
        "direct_fact_write_allowed_false": (
            NON_EXECUTION_FLAGS["direct_fact_write_allowed"] is False
        ),
        "commercial_runtime_approved_false": (
            NON_EXECUTION_FLAGS["commercial_runtime_approved"] is False
        ),
        "native_model_output_direct_to_field_blocked": adapter_native_blocked,
        "runtime_boundary_no_inference": (
            runtime_b.get("real_inference_allowed") is False
            and runtime_b.get("model_invocation_execution_allowed") is False
        ),
    }

    for key, ok in go_conditions.items():
        if ok:
            passed_checks.append(f"go.{key}=true")
        else:
            failed_checks.append(f"go.{key}=false")

    blocker_count = len(failed_checks)
    review_ok = registry_ok and blocker_count == 0

    review_checkpoints: Dict[str, Any] = {
        "planning_profile_count": 1,
        "model_family_policy_count": matrix.get("model_family_policy_count"),
        "invocation_feasibility_policy_count": matrix.get("invocation_feasibility_policy_count"),
        "output_requirement_policy_count": matrix.get("output_requirement_policy_count"),
        "adapter_readiness_policy_count": matrix.get("adapter_readiness_policy_count"),
        "model_family_ids": list(MODEL_FAMILY_IDS),
        "invocation_feasibility_check_items": list(INVOCATION_FEASIBILITY_CHECK_ITEMS),
        "admission_order": list(ADMISSION_ORDER),
        "runtime_trial_mode": RUNTIME_TRIAL_MODE,
        "target_chain_ref": TARGET_CHAIN_REF,
        "target_entrypoint": TARGET_ENTRYPOINT,
        "interface_adapter_ref": INTERFACE_ADAPTER_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        **upstream_checks,
        **ORDER_ENFORCEMENT_FLAGS,
        **NON_EXECUTION_FLAGS,
    }

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "Recognition Model System Admission and Invocation Planning Review",
        "lifecycle_variant": "recognition_model_system_admission_and_invocation_planning",
        "planning_principle_zh": PLANNING_PRINCIPLE_ZH,
        "registry_id": REGISTRY_ID,
        "source_chain": SOURCE_CHAIN,
        "runtime_trial_mode": RUNTIME_TRIAL_MODE,
        "target_chain_ref": TARGET_CHAIN_REF,
        "target_entrypoint": TARGET_ENTRYPOINT,
        "interface_adapter_ref": INTERFACE_ADAPTER_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "admission_order": list(ADMISSION_ORDER),
        "planning_governance_rules": list(PLANNING_GOVERNANCE_RULES),
        "order_enforcement_flags": dict(ORDER_ENFORCEMENT_FLAGS),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "registry_validation_ok": registry_ok,
        "upstream_sealed_phase_review": upstream_checks,
        "go_conditions": go_conditions,
        "review_checkpoints": review_checkpoints,
        "recognition_model_system_admission_matrix": matrix,
        "conclusions": {
            "recognition_model_system_admission_and_invocation_planning_status": (
                "recognition_model_system_admission_and_invocation_planning_ready"
                if review_ok
                else "blocked"
            ),
            "model_families_admission_planned": list(MODEL_FAMILY_IDS),
            "admission_order": list(ADMISSION_ORDER),
            "next_phase_ref": NEXT_PHASE_REF,
            "transition_note": (
                "Recognition-model system admission and invocation planned: which model families to "
                "admit, how to check invocation feasibility, what output schema is required, and the "
                "admission order (system admission -> invocation feasibility -> output adapter -> "
                "evidence main chain integration -> tuning -> data usage -> real recognition). No "
                "model download / invocation / inference / tuning / dataset usage. Next: "
                "Phase-Recognition-Model-Invocation-Feasibility-DryRun-v1-001 may start with "
                "lightweight stub / installed-check / command availability / import availability "
                "checks — not real image inference."
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
    result = review_recognition_model_system_admission_and_invocation_planning_v1()
    cp = result["review_checkpoints"]
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "model_family_policy_count": cp["model_family_policy_count"],
                "invocation_feasibility_policy_count": cp["invocation_feasibility_policy_count"],
                "output_requirement_policy_count": cp["output_requirement_policy_count"],
                "adapter_readiness_policy_count": cp["adapter_readiness_policy_count"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
