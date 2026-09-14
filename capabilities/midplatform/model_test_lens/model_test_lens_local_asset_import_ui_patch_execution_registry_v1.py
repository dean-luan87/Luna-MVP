# -*- coding: utf-8 -*-
"""P1 Model Test Lens Local Asset Import UI Patch Execution — registry v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.midplatform.model_test_lens.model_test_lens_local_asset_import_ui_patch_execution_types_v1 import (
    UPSTREAM_LENS_PLANNING_REF,
    UPSTREAM_LOCAL_ASSET_IMPORT_PLANNING_REF,
    UPSTREAM_SKELETON_EXECUTION_REF,
)

UPSTREAM_LOCAL_ASSET_IMPORT_PLANNING_EXPECTED_GO = (
    "P1_MIDPLATFORM_MODEL_TEST_LENS_LOCAL_ASSET_IMPORT_RUNNER_BRIDGE_PLANNING_GO"
)
UPSTREAM_SKELETON_EXECUTION_EXPECTED_GO = (
    "P1_MIDPLATFORM_MODEL_TEST_LENS_STATIC_SITE_SKELETON_EXECUTION_GO"
)
UPSTREAM_LENS_PLANNING_EXPECTED_GO = (
    "P1_MIDPLATFORM_MODEL_TEST_LENS_STATIC_SITE_PLANNING_GO"
)
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"

UPSTREAM_STAGE_REGISTRY: Tuple[Dict[str, Any], ...] = (
    {
        "phase_ref": UPSTREAM_LOCAL_ASSET_IMPORT_PLANNING_REF,
        "verify": True,
        "verify_flag": "local_asset_import_runner_bridge_planning_go_verified",
        "expected_go": UPSTREAM_LOCAL_ASSET_IMPORT_PLANNING_EXPECTED_GO,
        "artifact_rel": (
            "_tmp_eval_out/p1_midplatform_model_test_lens_local_asset_import_runner_bridge_planning_v1_smoke_v0/"
            "p1_midplatform_model_test_lens_local_asset_import_runner_bridge_planning_review_v1.json"
        ),
    },
    {
        "phase_ref": UPSTREAM_SKELETON_EXECUTION_REF,
        "verify": True,
        "verify_flag": "model_test_lens_skeleton_execution_go_verified",
        "expected_go": UPSTREAM_SKELETON_EXECUTION_EXPECTED_GO,
        "artifact_rel": (
            "_tmp_eval_out/p1_midplatform_model_test_lens_static_site_skeleton_execution_v1_smoke_v0/"
            "p1_midplatform_model_test_lens_static_site_skeleton_execution_review_v1.json"
        ),
    },
    {
        "phase_ref": UPSTREAM_LENS_PLANNING_REF,
        "verify": True,
        "verify_flag": "model_test_lens_static_site_planning_go_verified",
        "expected_go": UPSTREAM_LENS_PLANNING_EXPECTED_GO,
        "artifact_rel": (
            "_tmp_eval_out/p1_midplatform_model_test_lens_static_site_planning_v1_smoke_v0/"
            "p1_midplatform_model_test_lens_static_site_planning_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-Test-Board-Protected-Artifact-Rule-v1-001",
        "verify": True,
        "verify_flag": "test_board_protocol_go_verified",
        "expected_go": TEST_BOARD_PROTOCOL_EXPECTED_GO,
        "artifact_rel": (
            "_tmp_eval_out/test_board_protocol_v1_smoke_v0/test_board_protocol_review_v1.json"
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
)

GOVERNANCE_TEMPLATE_STAGE_REF = "ControlledTrialGovernanceLifecycleTemplateV1"
UPSTREAM_PRIMARY_PHASE_REF = UPSTREAM_LOCAL_ASSET_IMPORT_PLANNING_REF

REQUIRED_VERIFY_FLAGS: Tuple[str, ...] = tuple(
    e["verify_flag"] for e in UPSTREAM_STAGE_REGISTRY if e["verify"]
)

GOVERNANCE_CANONICAL_REFS: Tuple[str, ...] = (
    "capabilities/midplatform/governance_standards/governance_standards_manifest_v1.json",
    "capabilities/midplatform/governance_standards/index/governance_standards_reference_policy_v1.md",
    "capabilities/midplatform/model_test_lens/schemas/local_asset_import/local_test_asset_manifest_schema_v1.json",
    "capabilities/midplatform/model_test_lens/schemas/local_asset_import/model_test_job_request_schema_v1.json",
    "capabilities/midplatform/model_test_lens/schemas/local_asset_import/runner_bridge_request_schema_v1.json",
    "capabilities/midplatform/model_test_lens/schemas/local_asset_import/asset_to_envelope_route_schema_v1.json",
)


def _artifact_roots(repo_root: Path) -> List[Path]:
    roots: List[Path] = [repo_root, Path.cwd()]
    for extra in (repo_root.parent / "Luna-Core", repo_root.parent / "Luna-Workspace-Min"):
        if extra.is_dir() and extra not in roots:
            roots.append(extra)
    return roots


def _resolve_file(repo_root: Path, rel: str) -> Optional[Path]:
    for base in _artifact_roots(repo_root):
        p = base / rel
        if p.is_file():
            return p
    return None


def verify_stages(repo_root: Path) -> Tuple[List[str], Dict[str, bool], List[str], List[str]]:
    stage_refs: List[str] = []
    verify_flags: Dict[str, bool] = {}
    issues: List[str] = []
    warnings: List[str] = []

    for entry in UPSTREAM_STAGE_REGISTRY:
        stage_refs.append(entry["phase_ref"])
        flag = entry["verify_flag"]
        if not entry.get("verify"):
            verify_flags[flag] = True
            continue
        mode = entry.get("verify_mode", "review_go")
        artifact = entry.get("artifact_rel", "")
        if mode == "file_exists":
            ok = _resolve_file(repo_root, artifact) is not None
            verify_flags[flag] = ok
            if not ok:
                issues.append(f"upstream.file_missing={artifact}")
            continue
        path = _resolve_file(repo_root, artifact)
        if path is None:
            verify_flags[flag] = False
            warnings.append(f"upstream.review_missing={artifact}")
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            decision = data.get("final_decision") or data.get("decision", {}).get("final_decision")
            expected = entry.get("expected_go")
            ok = expected is None or decision == expected
            verify_flags[flag] = ok
            if not ok:
                issues.append(f"upstream.go_mismatch={entry['phase_ref']} got={decision}")
        except (json.JSONDecodeError, OSError) as exc:
            verify_flags[flag] = False
            issues.append(f"upstream.read_error={artifact}: {exc}")

    return stage_refs, verify_flags, issues, warnings
