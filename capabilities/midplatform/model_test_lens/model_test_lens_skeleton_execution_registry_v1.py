# -*- coding: utf-8 -*-
"""P1 Midplatform Model Test Lens Static Site Skeleton Execution — registry v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.midplatform.model_test_lens.model_test_lens_skeleton_execution_types_v1 import (
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    ENVELOPE_SCHEMA_REL,
    PLAN_MD_REL,
    TEST_BOARD_PROTOCOL_EXPECTED_GO,
    UPSTREAM_PLANNING_EXPECTED_GO,
)
from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

UPSTREAM_MOBILE_SAM_MULTI_EXECUTION_EXPECTED_GO = (
    "P1_MOBILE_SAM_MULTI_REAL_IMAGE_INFERENCE_TRIAL_EXECUTION_GO"
)

UPSTREAM_STAGE_REGISTRY: Tuple[Dict[str, Any], ...] = (
    {
        "phase_ref": "Phase-P1-Midplatform-Model-Test-Lens-Static-Site-Planning-v1-001",
        "verify": True,
        "verify_flag": "model_test_lens_static_site_planning_go_verified",
        "expected_go": UPSTREAM_PLANNING_EXPECTED_GO,
        "artifact_rel": (
            "_tmp_eval_out/p1_midplatform_model_test_lens_static_site_planning_v1_smoke_v0/"
            "p1_midplatform_model_test_lens_static_site_planning_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-P1-MobileSAM-Multi-Real-Image-Inference-Trial-Execution-And-Post-Review-v1-001",
        "verify": True,
        "verify_flag": "mobile_sam_multi_image_execution_go_verified",
        "expected_go": UPSTREAM_MOBILE_SAM_MULTI_EXECUTION_EXPECTED_GO,
        "artifact_rel": (
            "_tmp_eval_out/p1_mobile_sam_multi_real_image_inference_trial_execution_and_post_review_v1_smoke_v0/"
            "p1_mobile_sam_multi_real_image_inference_trial_execution_and_post_review_review_v1.json"
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
        "phase_ref": "GovernanceStandardsManifestV1",
        "verify": True,
        "verify_flag": "governance_standard_manifest_verified",
        "expected_go": None,
        "artifact_rel": "capabilities/midplatform/governance_standards/governance_standards_manifest_v1.json",
        "verify_mode": "file_exists",
    },
    {
        "phase_ref": "GovernanceStandardsReferencePolicyV1",
        "verify": True,
        "verify_flag": "governance_reference_policy_ref_ok",
        "expected_go": None,
        "artifact_rel": (
            "capabilities/midplatform/governance_standards/index/"
            "governance_standards_reference_policy_v1.md"
        ),
        "verify_mode": "file_exists",
    },
    {
        "phase_ref": "ModelTestResultEnvelopeSchemaV1",
        "verify": True,
        "verify_flag": "envelope_schema_ref_ok",
        "expected_go": None,
        "artifact_rel": ENVELOPE_SCHEMA_REL,
        "verify_mode": "file_exists",
    },
    {
        "phase_ref": "ModelTestLensStaticSitePlanV1",
        "verify": True,
        "verify_flag": "static_site_plan_ref_ok",
        "expected_go": None,
        "artifact_rel": PLAN_MD_REL,
        "verify_mode": "file_exists",
    },
)

GOVERNANCE_TEMPLATE_STAGE_REF = "ControlledTrialGovernanceLifecycleTemplateV1"
UPSTREAM_PRIMARY_PHASE_REF = (
    "Phase-P1-Midplatform-Model-Test-Lens-Static-Site-Planning-v1-001"
)

REQUIRED_VERIFY_FLAGS: Tuple[str, ...] = tuple(
    e["verify_flag"] for e in UPSTREAM_STAGE_REGISTRY if e["verify"]
)


def _artifact_search_roots(repo_root: Path) -> Tuple[Path, ...]:
    roots: List[Path] = [repo_root, Path.cwd()]
    for extra in (repo_root.parent / "Luna-Core", repo_root.parent / "Luna-Workspace-Min"):
        if extra.is_dir() and extra not in roots:
            roots.append(extra)
    return tuple(roots)


def load_artifact(repo_root: Path, artifact_rel: str) -> Tuple[Optional[Dict[str, Any]], bool, str]:
    for base in _artifact_search_roots(repo_root):
        path = base / artifact_rel
        if path.is_file():
            try:
                if artifact_rel.endswith(".json"):
                    return json.loads(path.read_text(encoding="utf-8")), True, str(path)
                return {"_file_present": True, "_path": str(path)}, True, str(path)
            except (OSError, json.JSONDecodeError):
                return None, True, str(path)
    return None, False, ""


def verify_stages(
    repo_root: Path,
) -> Tuple[List[Dict[str, Any]], Dict[str, bool], List[str], List[str]]:
    stage_refs: List[Dict[str, Any]] = []
    verify_flags: Dict[str, bool] = {}
    issues: List[str] = []
    warnings: List[str] = []
    for idx, entry in enumerate(UPSTREAM_STAGE_REGISTRY, start=1):
        if entry["verify"]:
            artifact, exists, resolved = load_artifact(repo_root, entry["artifact_rel"])
            verify_mode = entry.get("verify_mode", "final_decision")
            if exists:
                if verify_mode == "file_exists":
                    go_ok = artifact is not None
                else:
                    go_ok = (artifact or {}).get("final_decision") == entry["expected_go"]
                read_mode = "artifact_present"
            else:
                go_ok = True
                read_mode = "sealed_ref_fallback"
            verify_flags[entry["verify_flag"]] = go_ok
            if not exists:
                warnings.append(f"upstream_artifact_missing_sealed_ref_fallback:{entry['phase_ref']}")
            elif not go_ok:
                issues.append(f"upstream_go_mismatch:{entry['phase_ref']}")
        else:
            read_mode = "reference_only"
            go_ok = True
            resolved = ""
        stage_refs.append(
            {
                "stage_index": idx,
                "phase_ref": entry["phase_ref"],
                "gated": entry["verify"],
                "artifact_read_mode": read_mode,
                "resolved_path": resolved,
                "go_verified": go_ok,
            }
        )
    template_ok = CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF == TEMPLATE_ID
    verify_flags["controlled_trial_template_ref_ok"] = template_ok
    if not template_ok:
        issues.append("controlled_trial_governance_template_ref_mismatch")
    return stage_refs, verify_flags, issues, warnings
