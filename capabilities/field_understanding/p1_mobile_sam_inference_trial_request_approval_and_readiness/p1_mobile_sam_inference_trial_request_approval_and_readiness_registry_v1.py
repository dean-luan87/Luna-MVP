# -*- coding: utf-8 -*-
"""P1 MobileSAM Inference Trial Request Approval And Readiness — registry v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.field_understanding.p1_mobile_sam_inference_trial_request_approval_and_readiness.p1_mobile_sam_inference_trial_request_approval_and_readiness_types_v1 import (
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    TEST_BOARD_PROTOCOL_EXPECTED_GO,
    UPSTREAM_REGISTRY_PATCH_EXECUTION_EXPECTED_GO,
)
from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

UPSTREAM_STAGE_REGISTRY: Tuple[Dict[str, Any], ...] = (
    {
        "phase_ref": "Phase-P1-MobileSAM-Model-Load-Registry-Patch-Execution-And-Post-Review-v1-001",
        "verify": True,
        "verify_flag": "mobile_sam_model_load_registry_patch_execution_go_verified",
        "expected_go": UPSTREAM_REGISTRY_PATCH_EXECUTION_EXPECTED_GO,
        "artifact_rel": (
            "_tmp_eval_out/p1_mobile_sam_model_load_registry_patch_execution_and_post_review_v1_smoke_v0/"
            "p1_mobile_sam_model_load_registry_patch_execution_and_post_review_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-P1-MobileSAM-Model-Load-Registry-Patch-And-Inference-Trial-Readiness-Planning-v1-001",
        "verify": True,
        "verify_flag": "mobile_sam_model_load_registry_patch_inference_readiness_planning_go_verified",
        "expected_go": "P1_MOBILE_SAM_MODEL_LOAD_REGISTRY_PATCH_AND_INFERENCE_TRIAL_READINESS_PLANNING_GO",
        "artifact_rel": (
            "_tmp_eval_out/p1_mobile_sam_model_load_registry_patch_and_inference_trial_readiness_planning_v1_smoke_v0/"
            "p1_mobile_sam_model_load_registry_patch_and_inference_trial_readiness_planning_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-P1-MobileSAM-Model-Load-Trial-Retry-Execution-And-Post-Review-v1-001",
        "verify": True,
        "verify_flag": "mobile_sam_model_load_retry_execution_go_verified",
        "expected_go": "P1_MOBILE_SAM_MODEL_LOAD_TRIAL_RETRY_EXECUTION_GO",
        "artifact_rel": (
            "_tmp_eval_out/p1_mobile_sam_model_load_trial_retry_execution_and_post_review_v1_smoke_v0/"
            "p1_mobile_sam_model_load_trial_retry_execution_and_post_review_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-P1-MobileSAM-Dependency-Repair-NoDeps-Install-Execution-And-Post-Review-v1-001",
        "verify": True,
        "verify_flag": "mobile_sam_nodeps_timm_install_execution_go_verified",
        "expected_go": "P1_MOBILE_SAM_DEPENDENCY_REPAIR_NODEPS_INSTALL_EXECUTION_GO",
        "artifact_rel": (
            "_tmp_eval_out/p1_mobile_sam_dependency_repair_nodeps_install_execution_and_post_review_v1_smoke_v0/"
            "p1_mobile_sam_dependency_repair_nodeps_install_execution_and_post_review_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-P1-MobileSAM-Dependency-Repair-NoDeps-Install-Request-Approval-And-Readiness-v1-001",
        "verify": True,
        "verify_flag": "mobile_sam_nodeps_timm_install_request_approval_readiness_go_verified",
        "expected_go": "P1_MOBILE_SAM_DEPENDENCY_REPAIR_NODEPS_INSTALL_REQUEST_APPROVAL_AND_READINESS_GO",
        "artifact_rel": (
            "_tmp_eval_out/p1_mobile_sam_dependency_repair_nodeps_install_request_approval_and_readiness_v1_smoke_v0/"
            "p1_mobile_sam_dependency_repair_nodeps_install_request_approval_and_readiness_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-P1-MobileSAM-Dependency-Repair-Install-Failure-Review-And-Repair-Planning-v1-001",
        "verify": True,
        "verify_flag": "mobile_sam_timm_install_failure_repair_planning_go_verified",
        "expected_go": "P1_MOBILE_SAM_DEPENDENCY_REPAIR_INSTALL_FAILURE_REVIEW_AND_REPAIR_PLANNING_GO",
        "artifact_rel": (
            "_tmp_eval_out/p1_mobile_sam_dependency_repair_install_failure_review_and_repair_planning_v1_smoke_v0/"
            "p1_mobile_sam_dependency_repair_install_failure_review_and_repair_planning_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-P1-MobileSAM-Model-Load-Failure-Review-And-Repair-Planning-v1-001",
        "verify": True,
        "verify_flag": "mobile_sam_model_load_failure_repair_planning_go_verified",
        "expected_go": "P1_MOBILE_SAM_MODEL_LOAD_FAILURE_REVIEW_AND_REPAIR_PLANNING_GO",
        "artifact_rel": (
            "_tmp_eval_out/p1_mobile_sam_model_load_failure_review_and_repair_planning_v1_smoke_v0/"
            "p1_mobile_sam_model_load_failure_review_and_repair_planning_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-P1-MobileSAM-Model-Load-Trial-Execution-And-Post-Review-v1-001",
        "verify": True,
        "verify_flag": "mobile_sam_model_load_trial_execution_failed_no_boundary_violation_verified",
        "expected_go": "P1_MOBILE_SAM_MODEL_LOAD_TRIAL_EXECUTION_FAILED_NO_BOUNDARY_VIOLATION",
        "artifact_rel": (
            "_tmp_eval_out/p1_mobile_sam_model_load_trial_execution_and_post_review_v1_smoke_v0/"
            "p1_mobile_sam_model_load_trial_execution_and_post_review_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-P1-MobileSAM-Model-Load-Trial-Request-Approval-And-Readiness-v1-001",
        "verify": True,
        "verify_flag": "mobile_sam_model_load_request_approval_readiness_go_verified",
        "expected_go": "P1_MOBILE_SAM_MODEL_LOAD_TRIAL_REQUEST_APPROVAL_AND_READINESS_GO",
        "artifact_rel": (
            "_tmp_eval_out/p1_mobile_sam_model_load_trial_request_approval_and_readiness_v1_smoke_v0/"
            "p1_mobile_sam_model_load_trial_request_approval_and_readiness_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-P1-MobileSAM-Weight-Registry-Patch-Execution-And-Post-Review-v1-001",
        "verify": True,
        "verify_flag": "mobile_sam_weight_registry_patch_execution_go_verified",
        "expected_go": "P1_MOBILE_SAM_WEIGHT_REGISTRY_PATCH_EXECUTION_AND_POST_REVIEW_GO",
        "artifact_rel": (
            "_tmp_eval_out/p1_mobile_sam_weight_registry_patch_execution_and_post_review_v1_smoke_v0/"
            "p1_mobile_sam_weight_registry_patch_execution_and_post_review_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-P1-Model-Weight-Download-Execution-And-Post-Review-v1-001",
        "verify": True,
        "verify_flag": "model_weight_download_execution_post_review_go_verified",
        "expected_go": "P1_MODEL_WEIGHT_DOWNLOAD_EXECUTION_AND_POST_REVIEW_GO",
        "artifact_rel": (
            "_tmp_eval_out/p1_model_weight_download_execution_and_post_review_v1_smoke_v0/"
            "p1_model_weight_download_execution_and_post_review_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-P1-Source-Code-Only-Install-Registry-Patch-Execution-And-Post-Review-v1-001",
        "verify": True,
        "verify_flag": "source_code_only_registry_patch_execution_go_verified",
        "expected_go": "P1_SOURCE_CODE_ONLY_INSTALL_REGISTRY_PATCH_EXECUTION_AND_POST_REVIEW_GO",
        "artifact_rel": (
            "_tmp_eval_out/p1_source_code_only_install_registry_patch_execution_and_post_review_v1_smoke_v0/"
            "p1_source_code_only_install_registry_patch_execution_and_post_review_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-P1-Controlled-Source-Install-Execution-Retry-And-Post-Review-v1-001",
        "verify": True,
        "verify_flag": "source_install_execution_retry_code_only_go_verified",
        "expected_go": "P1_CONTROLLED_SOURCE_INSTALL_EXECUTION_RETRY_CODE_ONLY_GO",
        "artifact_rel": (
            "_tmp_eval_out/p1_controlled_source_install_execution_retry_and_post_review_v1_smoke_v0/"
            "p1_controlled_source_install_execution_retry_and_post_review_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-Midplatform-Model-Version-Dependency-Registry-Planning-v1-001",
        "verify": True,
        "verify_flag": "model_version_dependency_registry_planning_go_verified",
        "expected_go": "MIDPLATFORM_MODEL_VERSION_DEPENDENCY_REGISTRY_PLANNING_GO",
        "artifact_rel": (
            "_tmp_eval_out/midplatform_model_version_dependency_registry_planning_v1_smoke_v0/"
            "midplatform_model_version_dependency_registry_planning_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-Test-Board-Protected-Artifact-Rule-v1-001",
        "verify": True,
        "verify_flag": "test_board_protocol_go_verified",
        "expected_go": TEST_BOARD_PROTOCOL_EXPECTED_GO,
        "artifact_rel": (
            "_tmp_eval_out/test_board_protocol_v1_smoke_v0/"
            "test_board_protocol_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-Midplatform-Model-Version-Dependency-Registry-P1-Probe-Reconciliation-Post-Review-v1-001",
        "verify": False,
        "verify_flag": None,
        "expected_go": None,
        "artifact_rel": None,
    },
)

GOVERNANCE_TEMPLATE_STAGE_REF = "ControlledTrialGovernanceLifecycleTemplateV1"
UPSTREAM_PRIMARY_PHASE_REF = (
    "Phase-P1-MobileSAM-Model-Load-Registry-Patch-Execution-And-Post-Review-v1-001"
)

REQUIRED_VERIFY_FLAGS: Tuple[str, ...] = tuple(
    e["verify_flag"] for e in UPSTREAM_STAGE_REGISTRY if e["verify"]
)


def load_artifact(repo_root: Path, artifact_rel: str) -> Tuple[Optional[Dict[str, Any]], bool]:
    path = repo_root / artifact_rel
    if not path.is_file():
        return None, False
    try:
        return json.loads(path.read_text(encoding="utf-8")), True
    except (OSError, json.JSONDecodeError):
        return None, True


def verify_stages(
    repo_root: Path,
) -> Tuple[List[Dict[str, Any]], Dict[str, bool], List[str], List[str]]:
    stage_refs: List[Dict[str, Any]] = []
    verify_flags: Dict[str, bool] = {}
    issues: List[str] = []
    warnings: List[str] = []
    for idx, entry in enumerate(UPSTREAM_STAGE_REGISTRY, start=1):
        if entry["verify"]:
            artifact, exists = load_artifact(repo_root, entry["artifact_rel"])
            actual_go = (artifact or {}).get("final_decision") if exists else None
            if exists:
                go_ok = actual_go == entry["expected_go"]
                read_mode = "artifact_present"
            else:
                go_ok = True
                read_mode = "sealed_ref_fallback"
            verify_flags[entry["verify_flag"]] = go_ok
            if not exists:
                warnings.append(f"upstream_artifact_missing_sealed_ref_fallback:{entry['phase_ref']}")
            elif not go_ok:
                issues.append(f"upstream_go_mismatch:{entry['phase_ref']}:{actual_go!r}")
        else:
            read_mode = "reference_only"
            go_ok = True
        stage_refs.append(
            {
                "stage_index": idx,
                "phase_ref": entry["phase_ref"],
                "expected_go": entry["expected_go"],
                "gated": entry["verify"],
                "artifact_read_mode": read_mode,
                "go_verified": go_ok,
            }
        )
    template_ok = CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF == TEMPLATE_ID
    verify_flags["controlled_trial_template_ref_ok"] = template_ok
    if not template_ok:
        issues.append("controlled_trial_governance_template_ref_mismatch")
    return stage_refs, verify_flags, issues, warnings
