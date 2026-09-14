# -*- coding: utf-8 -*-
"""P1 Controlled Source Install Execution Post-Review — registry v1.

Upstream stage registry. Gates on the first real source-install execution
(primary, PARTIAL_GO) + source-install preparation/readiness review + owner
approval issuance + request planning + resolution planning + registry package-name
correction planning + source-install / package-name-resolution planning +
package-install-only execution post-review + the first real package execution
(PARTIAL_GO) + registry<->P1 probe reconciliation post-review + midplatform model
version/dependency registry planning + the Test Board Protected Artifact Rule
protocol + the controlled-trial governance template. Sealed-ref fallback applies
in the sandbox (missing canonical artifact => warning, not blocker).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.field_understanding.p1_controlled_source_install_execution_post_review.p1_controlled_source_install_execution_post_review_types_v1 import (
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    TEST_BOARD_PROTOCOL_EXPECTED_GO,
    UPSTREAM_EXECUTION_EXPECTED_GO,
)
from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

UPSTREAM_STAGE_REGISTRY: Tuple[Dict[str, Any], ...] = (
    {
        "phase_ref": "Phase-P1-Controlled-Source-Install-Execution-v1-001",
        "verify": True,
        "verify_flag": "controlled_source_install_execution_partial_go_verified",
        "expected_go": UPSTREAM_EXECUTION_EXPECTED_GO,
        "artifact_rel": (
            "_tmp_eval_out/p1_controlled_source_install_execution_v1_smoke_v0/"
            "p1_controlled_source_install_execution_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-P1-Controlled-Source-Install-Preparation-And-Readiness-Review-v1-001",
        "verify": True,
        "verify_flag": "source_install_preparation_readiness_go_verified",
        "expected_go": "P1_CONTROLLED_SOURCE_INSTALL_PREPARATION_AND_READINESS_REVIEW_GO",
        "artifact_rel": (
            "_tmp_eval_out/p1_controlled_source_install_preparation_and_readiness_review_v1_smoke_v0/"
            "p1_controlled_source_install_preparation_and_readiness_review_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-P1-Controlled-Source-Install-Owner-Approval-Issuance-v1-001",
        "verify": True,
        "verify_flag": "source_owner_approval_issuance_go_verified",
        "expected_go": "P1_CONTROLLED_SOURCE_INSTALL_OWNER_APPROVAL_ISSUANCE_GO",
        "artifact_rel": (
            "_tmp_eval_out/p1_controlled_source_install_owner_approval_issuance_v1_smoke_v0/"
            "p1_controlled_source_install_owner_approval_issuance_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-P1-Controlled-Source-Install-Request-Planning-v1-001",
        "verify": True,
        "verify_flag": "controlled_source_install_request_planning_go_verified",
        "expected_go": "P1_CONTROLLED_SOURCE_INSTALL_REQUEST_PLANNING_GO",
        "artifact_rel": (
            "_tmp_eval_out/p1_controlled_source_install_request_planning_v1_smoke_v0/"
            "p1_controlled_source_install_request_planning_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-P1-Controlled-Source-Install-Resolution-Planning-v1-001",
        "verify": True,
        "verify_flag": "controlled_source_install_resolution_planning_go_verified",
        "expected_go": "P1_CONTROLLED_SOURCE_INSTALL_RESOLUTION_PLANNING_GO",
        "artifact_rel": (
            "_tmp_eval_out/p1_controlled_source_install_resolution_planning_v1_smoke_v0/"
            "p1_controlled_source_install_resolution_planning_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-P1-Registry-Package-Name-Correction-Planning-v1-001",
        "verify": True,
        "verify_flag": "registry_package_name_correction_planning_go_verified",
        "expected_go": "P1_REGISTRY_PACKAGE_NAME_CORRECTION_PLANNING_GO",
        "artifact_rel": (
            "_tmp_eval_out/p1_registry_package_name_correction_planning_v1_smoke_v0/"
            "p1_registry_package_name_correction_planning_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-P1-Source-Install-And-Package-Name-Resolution-Planning-v1-001",
        "verify": True,
        "verify_flag": "source_install_package_resolution_planning_go_verified",
        "expected_go": "P1_SOURCE_INSTALL_AND_PACKAGE_NAME_RESOLUTION_PLANNING_GO",
        "artifact_rel": (
            "_tmp_eval_out/p1_source_install_and_package_name_resolution_planning_v1_smoke_v0/"
            "p1_source_install_and_package_name_resolution_planning_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-P1-Controlled-Install-Execution-Post-Review-v1-001",
        "verify": True,
        "verify_flag": "controlled_install_execution_post_review_go_verified",
        "expected_go": "P1_CONTROLLED_INSTALL_EXECUTION_POST_REVIEW_GO",
        "artifact_rel": (
            "_tmp_eval_out/p1_controlled_install_execution_post_review_v1_smoke_v0/"
            "p1_controlled_install_execution_post_review_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-P1-Controlled-Install-Execution-v1-001",
        "verify": True,
        "verify_flag": "controlled_install_execution_package_only_partial_go_verified",
        "expected_go": "P1_CONTROLLED_INSTALL_EXECUTION_PACKAGE_ONLY_PARTIAL_GO",
        "artifact_rel": (
            "_tmp_eval_out/p1_controlled_install_execution_v1_smoke_v0/"
            "p1_controlled_install_execution_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-Midplatform-Model-Version-Dependency-Registry-P1-Probe-Reconciliation-Post-Review-v1-001",
        "verify": True,
        "verify_flag": "registry_probe_reconciliation_post_review_go_verified",
        "expected_go": "MIDPLATFORM_REGISTRY_P1_PROBE_RECONCILIATION_POST_REVIEW_GO",
        "artifact_rel": (
            "_tmp_eval_out/model_version_dependency_registry_p1_probe_reconciliation_post_review_v1_smoke_v0/"
            "model_version_dependency_registry_p1_probe_reconciliation_post_review_review_v1.json"
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
)

GOVERNANCE_TEMPLATE_STAGE_REF = "ControlledTrialGovernanceLifecycleTemplateV1"
UPSTREAM_PRIMARY_PHASE_REF = "Phase-P1-Controlled-Source-Install-Execution-v1-001"

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
    """Verify upstream GO status (sealed-ref fallback => warning, not blocker)."""
    stage_refs: List[Dict[str, Any]] = []
    verify_flags: Dict[str, bool] = {}
    issues: List[str] = []
    warnings: List[str] = []
    for idx, entry in enumerate(UPSTREAM_STAGE_REGISTRY, start=1):
        artifact, exists = load_artifact(repo_root, entry["artifact_rel"])
        actual_go = (artifact or {}).get("final_decision") if exists else None
        if exists:
            go_ok = actual_go == entry["expected_go"]
            read_mode = "artifact_present"
        else:
            go_ok = True
            read_mode = "sealed_ref_fallback"
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
        if entry["verify"]:
            verify_flags[entry["verify_flag"]] = go_ok
            if not exists:
                warnings.append(f"upstream_artifact_missing_sealed_ref_fallback:{entry['phase_ref']}")
            elif not go_ok:
                issues.append(f"upstream_go_mismatch:{entry['phase_ref']}:{actual_go!r}")
    template_ok = CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF == TEMPLATE_ID
    verify_flags["controlled_trial_template_ref_ok"] = template_ok
    if not template_ok:
        issues.append("controlled_trial_governance_template_ref_mismatch")
    return stage_refs, verify_flags, issues, warnings
