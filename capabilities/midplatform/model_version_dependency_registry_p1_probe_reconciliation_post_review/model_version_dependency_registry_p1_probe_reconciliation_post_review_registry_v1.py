# -*- coding: utf-8 -*-
"""Midplatform Registry <-> P1 Probe Reconciliation Post-Review — registry v1.

Upstream stage registry: the midplatform model version/dependency registry
planning phase (the registry under reconciliation) + the P1 real-install local
availability dry-run (the probe results under reconciliation) + the test board
planning-mode protocol patch + the Test Board Protected Artifact Rule protocol.
All gated entries must be GO-verified.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.midplatform.model_version_dependency_registry_p1_probe_reconciliation_post_review.model_version_dependency_registry_p1_probe_reconciliation_post_review_types_v1 import (
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    TEST_BOARD_PROTOCOL_EXPECTED_GO,
)
from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

UPSTREAM_STAGE_REGISTRY: Tuple[Dict[str, Any], ...] = (
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
        "phase_ref": "Phase-P1-Real-Install-Local-Availability-DryRun-v1-001",
        "verify": True,
        "verify_flag": "p1_real_install_local_availability_dryrun_go_verified",
        "expected_go": "P1_REAL_INSTALL_LOCAL_AVAILABILITY_DRYRUN_GO",
        "artifact_rel": (
            "_tmp_eval_out/p1_real_install_local_availability_dryrun_v1_smoke_v0/"
            "p1_real_install_local_availability_dryrun_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-TestBoard-Planning-Mode-Protocol-Patch-v1-001",
        "verify": True,
        "verify_flag": "planning_mode_protocol_patch_go_verified",
        "expected_go": "TEST_BOARD_PLANNING_MODE_PROTOCOL_PATCH_GO",
        "artifact_rel": (
            "_tmp_eval_out/test_board_planning_mode_protocol_patch_v1_smoke_v0/"
            "test_board_planning_mode_protocol_patch_review_v1.json"
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

# Convenience: upstream artifact relative paths for the reconciliation review.
REGISTRY_PLANNING_ARTIFACT_REL = UPSTREAM_STAGE_REGISTRY[0]["artifact_rel"]
P1_PROBE_ARTIFACT_REL = UPSTREAM_STAGE_REGISTRY[1]["artifact_rel"]


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
