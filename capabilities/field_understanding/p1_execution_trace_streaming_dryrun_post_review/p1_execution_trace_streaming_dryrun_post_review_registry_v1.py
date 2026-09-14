# -*- coding: utf-8 -*-
"""P1 Execution Trace Streaming DryRun Post-Review — registry v1.

Upstream stage registry: the streaming dry-run (under review) + P1 execution
foundation, P1 download/license planning, runtime-trial-planning, integrated
governance closure + post-review, midplatform model control / data handling /
multi-model interaction / P1 output adapter dry-runs, P0 integration closure, the
Test Board Protected Artifact Rule protocol, and the controlled-trial governance
template. All gated entries must be GO-verified.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.field_understanding.p1_execution_trace_streaming_dryrun_post_review.p1_execution_trace_streaming_dryrun_post_review_types_v1 import (
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    STREAMING_DRYRUN_EXPECTED_GO,
    TEST_BOARD_PROTOCOL_EXPECTED_GO,
)
from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

# --------------------------------------------------------------------------- #
# Upstream stage registry. gated=True entries are required GO-verified.
# --------------------------------------------------------------------------- #
UPSTREAM_STAGE_REGISTRY: Tuple[Dict[str, Any], ...] = (
    {
        "phase_ref": "Phase-P1-Execution-Trace-Streaming-DryRun-v1-001",
        "verify": True,
        "verify_flag": "p1_execution_trace_streaming_dryrun_go_verified",
        "expected_go": STREAMING_DRYRUN_EXPECTED_GO,
        "artifact_rel": (
            "_tmp_eval_out/p1_execution_trace_streaming_dryrun_v1_smoke_v0/"
            "p1_execution_trace_streaming_dryrun_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-P1-Execution-DryRun-Foundation-v1-001",
        "verify": True,
        "verify_flag": "p1_execution_dryrun_foundation_go_verified",
        "expected_go": "P1_EXECUTION_DRYRUN_FOUNDATION_GO",
        "artifact_rel": (
            "_tmp_eval_out/p1_execution_dryrun_foundation_v1_smoke_v0/"
            "p1_execution_dryrun_foundation_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-Recognition-Model-P1-Download-License-Planning-v1-001",
        "verify": True,
        "verify_flag": "p1_download_license_planning_go_verified",
        "expected_go": "RECOGNITION_MODEL_P1_DOWNLOAD_LICENSE_PLANNING_GO",
        "artifact_rel": (
            "_tmp_eval_out/recognition_model_p1_download_license_planning_v1_smoke_v0/"
            "recognition_model_p1_download_license_planning_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-Model-Governance-Runtime-Trial-Planning-v1-001",
        "verify": True,
        "verify_flag": "runtime_trial_planning_go_verified",
        "expected_go": "MODEL_GOVERNANCE_RUNTIME_TRIAL_PLANNING_GO",
        "artifact_rel": (
            "_tmp_eval_out/model_governance_runtime_trial_planning_v1_smoke_v0/"
            "model_governance_runtime_trial_planning_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-Recognition-Midplatform-Model-Governance-Integrated-Closure-Post-Review-v1-001",
        "verify": True,
        "verify_flag": "integrated_closure_post_review_go_verified",
        "expected_go": "RECOGNITION_MIDPLATFORM_MODEL_GOVERNANCE_INTEGRATED_CLOSURE_POST_REVIEW_GO",
        "artifact_rel": (
            "_tmp_eval_out/recognition_midplatform_model_governance_integrated_closure_post_review_v1_smoke_v0/"
            "recognition_midplatform_model_governance_integrated_closure_post_review_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-Recognition-Midplatform-Model-Governance-Integrated-Closure-v1-001",
        "verify": True,
        "verify_flag": "integrated_closure_go_verified",
        "expected_go": "RECOGNITION_MIDPLATFORM_MODEL_GOVERNANCE_INTEGRATED_CLOSURE_GO",
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
        "phase_ref": "Phase-Test-Board-Protected-Artifact-Rule-v1-001",
        "verify": True,
        "verify_flag": "test_board_protocol_go_verified",
        "expected_go": TEST_BOARD_PROTOCOL_EXPECTED_GO,
        "artifact_rel": (
            "_tmp_eval_out/test_board_protocol_v1_smoke_v0/"
            "test_board_protocol_review_v1.json"
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
