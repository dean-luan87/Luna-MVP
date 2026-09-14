# -*- coding: utf-8 -*-
"""Recognition Midplatform Model Governance Integrated Closure — registry v1.

Upstream stage registry (16 phase refs + governance template = 17 stage refs) and
the four-layer artifact registry that the closure verifies and seals.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.midplatform.model_governance_integrated_closure.model_governance_integrated_closure_types_v1 import (
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
)
from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

# --------------------------------------------------------------------------- #
# Upstream stage registry (16 phases). gated=True entries must be GO-verified.
# --------------------------------------------------------------------------- #
UPSTREAM_STAGE_REGISTRY: Tuple[Dict[str, Any], ...] = (
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
        "phase_ref": "Phase-Midplatform-Model-Data-Handling-DryRun-v1-001",
        "verify": True,
        "verify_flag": "midplatform_model_data_handling_dryrun_go_verified",
        "expected_go": "MIDPLATFORM_MODEL_DATA_HANDLING_DRYRUN_GO",
        "artifact_rel": (
            "_tmp_eval_out/midplatform_model_data_handling_dryrun_v1_smoke_v0/"
            "midplatform_model_data_handling_dryrun_run_and_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-Midplatform-Model-Control-DryRun-v1-001",
        "verify": True,
        "verify_flag": "midplatform_model_control_dryrun_go_verified",
        "expected_go": "MIDPLATFORM_MODEL_CONTROL_DRYRUN_GO",
        "artifact_rel": (
            "_tmp_eval_out/midplatform_model_control_dryrun_v1_smoke_v0/"
            "midplatform_model_control_dryrun_run_and_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-Recognition-Model-P1-Invocation-And-Local-Availability-DryRun-v1-001",
        "verify": True,
        "verify_flag": "p1_invocation_local_availability_dryrun_go_verified",
        "expected_go": "RECOGNITION_MODEL_P1_INVOCATION_AND_LOCAL_AVAILABILITY_DRYRUN_GO",
        "artifact_rel": (
            "_tmp_eval_out/recognition_model_p1_invocation_and_local_availability_dryrun_v1_smoke_v0/"
            "recognition_model_p1_invocation_and_local_availability_dryrun_run_and_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-Recognition-Model-P1-Family-Expansion-Planning-v1-001",
        "verify": True,
        "verify_flag": "p1_family_expansion_planning_go_verified",
        "expected_go": "RECOGNITION_MODEL_P1_FAMILY_EXPANSION_PLANNING_GO",
        "artifact_rel": (
            "_tmp_eval_out/recognition_model_p1_family_expansion_planning_v1_smoke_v0/"
            "recognition_model_p1_family_expansion_planning_review_v1.json"
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
        "phase_ref": "Phase-Recognition-Model-Evidence-Main-Chain-Integration-DryRun-v1-001",
        "verify": False,
        "verify_flag": None,
        "expected_go": "RECOGNITION_MODEL_EVIDENCE_MAIN_CHAIN_INTEGRATION_DRYRUN_GO",
        "artifact_rel": (
            "_tmp_eval_out/recognition_model_evidence_main_chain_integration_dryrun_v1_smoke_v0/"
            "recognition_model_evidence_main_chain_integration_dryrun_run_and_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-Recognition-Model-Real-Output-Adapter-DryRun-v1-001",
        "verify": False,
        "verify_flag": None,
        "expected_go": "RECOGNITION_MODEL_REAL_OUTPUT_ADAPTER_DRYRUN_GO",
        "artifact_rel": (
            "_tmp_eval_out/recognition_model_real_output_adapter_dryrun_v1_smoke_v0/"
            "recognition_model_real_output_adapter_dryrun_run_and_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-Recognition-Model-Output-Adapter-DryRun-v1-001",
        "verify": False,
        "verify_flag": None,
        "expected_go": "RECOGNITION_MODEL_OUTPUT_ADAPTER_DRYRUN_GO",
        "artifact_rel": (
            "_tmp_eval_out/recognition_model_output_adapter_dryrun_v1_smoke_v0/"
            "recognition_model_output_adapter_dryrun_run_and_review_v1.json"
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
        "verify": True,
        "verify_flag": "rgb_vision_evidence_chain_closure_go_verified",
        "expected_go": "RGB_VISION_EVIDENCE_CHAIN_INTEGRATED_CLOSURE_GO",
        "artifact_rel": (
            "_tmp_eval_out/rgb_vision_evidence_chain_integrated_closure_v1_smoke_v0/"
            "rgb_vision_evidence_chain_integrated_closure_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-RGB-Vision-SLAM-Spatial-Evidence-Cross-Modal-Integrated-Closure-v1-001",
        "verify": True,
        "verify_flag": "rgb_slam_cross_modal_closure_go_verified",
        "expected_go": "RGB_VISION_SLAM_SPATIAL_EVIDENCE_CROSS_MODAL_INTEGRATED_CLOSURE_GO",
        "artifact_rel": (
            "_tmp_eval_out/rgb_vision_slam_spatial_evidence_cross_modal_integrated_closure_v1_smoke_v0/"
            "rgb_vision_slam_spatial_evidence_cross_modal_integrated_closure_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-Field-Task-Guidance-Safety-Chain-Closure-v1-001",
        "verify": True,
        "verify_flag": "field_task_guidance_safety_chain_closure_go_verified",
        "expected_go": "FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_GO",
        "artifact_rel": (
            "_tmp_eval_out/field_task_guidance_safety_chain_closure_v1_smoke_v0/"
            "field_task_guidance_safety_chain_closure_review_v1.json"
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

# --------------------------------------------------------------------------- #
# Four-layer artifact registry (sealed baseline artifacts).
# --------------------------------------------------------------------------- #
LAYER_ARTIFACT_REGISTRY: Tuple[Dict[str, str], ...] = (
    {
        "layer": "p1_p2_output_adapter",
        "phase_ref": "Phase-Recognition-Model-P1-Output-Adapter-DryRun-v1-001",
        "expected_go": "RECOGNITION_MODEL_P1_OUTPUT_ADAPTER_DRYRUN_GO",
        "artifact_rel": (
            "_tmp_eval_out/recognition_model_p1_output_adapter_dryrun_v1_smoke_v0/"
            "recognition_model_p1_output_adapter_dryrun_run_and_review_v1.json"
        ),
    },
    {
        "layer": "multi_model_interaction",
        "phase_ref": "Phase-Recognition-Model-Multi-Model-Interaction-DryRun-v1-001",
        "expected_go": "RECOGNITION_MODEL_MULTI_MODEL_INTERACTION_DRYRUN_GO",
        "artifact_rel": (
            "_tmp_eval_out/recognition_model_multi_model_interaction_dryrun_v1_smoke_v0/"
            "recognition_model_multi_model_interaction_dryrun_run_and_review_v1.json"
        ),
    },
    {
        "layer": "midplatform_model_data_handling",
        "phase_ref": "Phase-Midplatform-Model-Data-Handling-DryRun-v1-001",
        "expected_go": "MIDPLATFORM_MODEL_DATA_HANDLING_DRYRUN_GO",
        "artifact_rel": (
            "_tmp_eval_out/midplatform_model_data_handling_dryrun_v1_smoke_v0/"
            "midplatform_model_data_handling_dryrun_run_and_review_v1.json"
        ),
    },
    {
        "layer": "midplatform_model_control",
        "phase_ref": "Phase-Midplatform-Model-Control-DryRun-v1-001",
        "expected_go": "MIDPLATFORM_MODEL_CONTROL_DRYRUN_GO",
        "artifact_rel": (
            "_tmp_eval_out/midplatform_model_control_dryrun_v1_smoke_v0/"
            "midplatform_model_control_dryrun_run_and_review_v1.json"
        ),
    },
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
    verify_flags["controlled_trial_governance_template_ref_ok"] = template_ok
    if not template_ok:
        issues.append("controlled_trial_governance_template_ref_mismatch")
    return stage_refs, verify_flags, issues


def verify_layer_artifacts(repo_root: Path) -> Tuple[List[Dict[str, Any]], List[str]]:
    artifact_refs: List[Dict[str, Any]] = []
    issues: List[str] = []
    for entry in LAYER_ARTIFACT_REGISTRY:
        artifact, exists = load_artifact(repo_root, entry["artifact_rel"])
        actual_go = (artifact or {}).get("final_decision") if exists else None
        ok = exists and actual_go == entry["expected_go"]
        artifact_refs.append(
            {
                "layer": entry["layer"],
                "phase_ref": entry["phase_ref"],
                "artifact_rel": entry["artifact_rel"],
                "final_decision": actual_go,
                "present": ok,
            }
        )
        if not ok:
            issues.append(f"layer_artifact_not_sealed:{entry['layer']}:{actual_go!r}")
    return artifact_refs, issues
