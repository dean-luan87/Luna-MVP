# -*- coding: utf-8 -*-
"""Model Governance Runtime Trial Planning — registry v1.

Upstream stage registry (integrated closure + 12 must-reference phases + governance
template) and the optional owner/record approval governance-reuse references.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.midplatform.model_governance_runtime_trial_planning.model_governance_runtime_trial_planning_types_v1 import (
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    INTEGRATED_CLOSURE_EXPECTED_GO,
    OPTIONAL_GOVERNANCE_REUSE_REFERENCES,
)
from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

# --------------------------------------------------------------------------- #
# Upstream stage registry. gated=True entries are required GO-verified.
# --------------------------------------------------------------------------- #
UPSTREAM_STAGE_REGISTRY: Tuple[Dict[str, Any], ...] = (
    {
        "phase_ref": "Phase-Recognition-Midplatform-Model-Governance-Integrated-Closure-v1-001",
        "verify": True,
        "verify_flag": "integrated_model_governance_closure_go_verified",
        "expected_go": INTEGRATED_CLOSURE_EXPECTED_GO,
        "artifact_rel": (
            "_tmp_eval_out/recognition_midplatform_model_governance_integrated_closure_v1_smoke_v0/"
            "recognition_midplatform_model_governance_integrated_closure_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-Midplatform-Model-Control-DryRun-v1-001",
        "verify": True,
        "verify_flag": "model_control_dryrun_go_verified",
        "expected_go": "MIDPLATFORM_MODEL_CONTROL_DRYRUN_GO",
        "artifact_rel": (
            "_tmp_eval_out/midplatform_model_control_dryrun_v1_smoke_v0/"
            "midplatform_model_control_dryrun_run_and_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-Midplatform-Model-Data-Handling-DryRun-v1-001",
        "verify": True,
        "verify_flag": "model_data_handling_dryrun_go_verified",
        "expected_go": "MIDPLATFORM_MODEL_DATA_HANDLING_DRYRUN_GO",
        "artifact_rel": (
            "_tmp_eval_out/midplatform_model_data_handling_dryrun_v1_smoke_v0/"
            "midplatform_model_data_handling_dryrun_run_and_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-Recognition-Model-Multi-Model-Interaction-DryRun-v1-001",
        "verify": True,
        "verify_flag": "multi_model_interaction_dryrun_go_verified",
        "expected_go": "RECOGNITION_MODEL_MULTI_MODEL_INTERACTION_DRYRUN_GO",
        "artifact_rel": (
            "_tmp_eval_out/recognition_model_multi_model_interaction_dryrun_v1_smoke_v0/"
            "recognition_model_multi_model_interaction_dryrun_run_and_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-Recognition-Model-P1-Output-Adapter-DryRun-v1-001",
        "verify": True,
        "verify_flag": "p1_output_adapter_dryrun_go_verified",
        "expected_go": "RECOGNITION_MODEL_P1_OUTPUT_ADAPTER_DRYRUN_GO",
        "artifact_rel": (
            "_tmp_eval_out/recognition_model_p1_output_adapter_dryrun_v1_smoke_v0/"
            "recognition_model_p1_output_adapter_dryrun_run_and_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-Recognition-Model-P0-Integration-Closure-v1-001",
        "verify": True,
        "verify_flag": "p0_integration_closure_go_verified",
        "expected_go": "RECOGNITION_MODEL_P0_INTEGRATION_CLOSURE_GO",
        "artifact_rel": (
            "_tmp_eval_out/recognition_model_p0_integration_closure_v1_smoke_v0/"
            "recognition_model_p0_integration_closure_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001",
        "verify": True,
        "verify_flag": "phase_one_evidence_main_chain_closure_go_verified",
        "expected_go": "PHASE_ONE_ENVIRONMENT_COGNITION_EVIDENCE_MAIN_CHAIN_CLOSURE_GO",
        "artifact_rel": (
            "_tmp_eval_out/phase_one_environment_cognition_evidence_main_chain_closure_v1_smoke_v0/"
            "phase_one_environment_cognition_evidence_main_chain_closure_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-RGB-Vision-Evidence-Chain-Integrated-Closure-v1-001",
        "verify": False,
        "verify_flag": None,
        "expected_go": "RGB_VISION_EVIDENCE_CHAIN_INTEGRATED_CLOSURE_GO",
        "artifact_rel": (
            "_tmp_eval_out/rgb_vision_evidence_chain_integrated_closure_v1_smoke_v0/"
            "rgb_vision_evidence_chain_integrated_closure_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-RGB-Vision-SLAM-Spatial-Evidence-Cross-Modal-Integrated-Closure-v1-001",
        "verify": False,
        "verify_flag": None,
        "expected_go": "RGB_VISION_SLAM_SPATIAL_EVIDENCE_CROSS_MODAL_INTEGRATED_CLOSURE_GO",
        "artifact_rel": (
            "_tmp_eval_out/rgb_vision_slam_spatial_evidence_cross_modal_integrated_closure_v1_smoke_v0/"
            "rgb_vision_slam_spatial_evidence_cross_modal_integrated_closure_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-Field-Task-Guidance-Safety-Chain-Closure-v1-001",
        "verify": True,
        "verify_flag": "field_task_guidance_safety_chain_verified",
        "expected_go": "FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_GO",
        "artifact_rel": (
            "_tmp_eval_out/field_task_guidance_safety_chain_closure_v1_smoke_v0/"
            "field_task_guidance_safety_chain_closure_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-PhaseOne-Environment-Cognition-Controlled-Runtime-Trial-Governance-Closure-v1-001",
        "verify": True,
        "verify_flag": "runtime_governance_closure_verified",
        "expected_go": "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_GOVERNANCE_CLOSURE_GO",
        "artifact_rel": (
            "_tmp_eval_out/phase_one_environment_cognition_runtime_trial_governance_closure_v1_smoke_v0/"
            "phase_one_environment_cognition_runtime_trial_governance_closure_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-Midplatform-Interface-Layer-Governance-Protocol-v1-001",
        "verify": True,
        "verify_flag": "interface_layer_governance_verified",
        "expected_go": "INTERFACE_LAYER_GOVERNANCE_PROTOCOL_BASELINE_READY_FOR_ADOPTION",
        "artifact_rel": (
            "_tmp_eval_out/interface_layer_governance_v1_smoke_v0/"
            "interface_layer_governance_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-Midplatform-Model-Admission-Governance-Standard-v1-001",
        "verify": True,
        "verify_flag": "model_admission_governance_verified",
        "expected_go": "MODEL_ADMISSION_GOVERNANCE_STANDARD_REVIEW_GO",
        "artifact_rel": (
            "_tmp_eval_out/model_admission_governance_v1_smoke_v0/"
            "model_admission_governance_run_and_review_v1.json"
        ),
    },
)

GOVERNANCE_TEMPLATE_STAGE_REF = "ControlledTrialGovernanceLifecycleTemplateV1"

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
) -> Tuple[List[Dict[str, Any]], Dict[str, bool], List[str]]:
    stage_refs: List[Dict[str, Any]] = []
    verify_flags: Dict[str, bool] = {}
    issues: List[str] = []
    for idx, entry in enumerate(UPSTREAM_STAGE_REGISTRY, start=1):
        artifact, exists = load_artifact(repo_root, entry["artifact_rel"])
        actual_go = (artifact or {}).get("final_decision") if exists else None
        go_ok = exists and actual_go == entry["expected_go"]
        stage_refs.append(
            {
                "stage_index": idx,
                "phase_ref": entry["phase_ref"],
                "expected_go": entry["expected_go"],
                "gated": entry["verify"],
                "go_verified": go_ok,
            }
        )
        if entry["verify"]:
            verify_flags[entry["verify_flag"]] = go_ok
            if not exists:
                issues.append(f"upstream_artifact_missing:{entry['phase_ref']}")
            elif not go_ok:
                issues.append(f"upstream_go_mismatch:{entry['phase_ref']}:{actual_go!r}")
    template_ok = CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF == TEMPLATE_ID
    verify_flags["controlled_trial_template_ref_ok"] = template_ok
    if not template_ok:
        issues.append("controlled_trial_governance_template_ref_mismatch")
    return stage_refs, verify_flags, issues


def resolve_optional_governance_refs(repo_root: Path) -> List[Dict[str, Any]]:
    """Record optional owner/record approval refs if present; never gating."""
    resolved: List[Dict[str, Any]] = []
    for ref in OPTIONAL_GOVERNANCE_REUSE_REFERENCES:
        _, exists = load_artifact(repo_root, ref["artifact_rel"])
        resolved.append(
            {
                "governance_asset": ref["governance_asset"],
                "usage": ref["usage"],
                "artifact_rel": ref["artifact_rel"],
                "present": exists,
                "optional": True,
                "reused": exists,
            }
        )
    return resolved
