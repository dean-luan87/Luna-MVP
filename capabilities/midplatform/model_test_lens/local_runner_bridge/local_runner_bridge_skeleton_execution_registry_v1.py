# -*- coding: utf-8 -*-
"""P1 Local Runner Bridge Service Skeleton Execution — registry v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

UPSTREAM_RUNNER_BRIDGE_PLANNING_EXPECTED_GO = (
    "P1_MIDPLATFORM_MODEL_TEST_LENS_LOCAL_RUNNER_BRIDGE_SERVICE_PLANNING_GO"
)
UPSTREAM_UI_PATCH_EXPECTED_GO = (
    "P1_MIDPLATFORM_MODEL_TEST_LENS_LOCAL_ASSET_IMPORT_UI_PATCH_EXECUTION_GO"
)

UPSTREAM_STAGE_REGISTRY: Tuple[Dict[str, Any], ...] = (
    {
        "phase_ref": "Phase-P1-Midplatform-Model-Test-Lens-Local-Runner-Bridge-Service-Planning-v1-001",
        "verify_flag": "local_runner_bridge_service_planning_go_verified",
        "expected_go": UPSTREAM_RUNNER_BRIDGE_PLANNING_EXPECTED_GO,
        "artifact_rel": (
            "_tmp_eval_out/p1_midplatform_model_test_lens_local_runner_bridge_service_planning_v1_smoke_v0/"
            "p1_midplatform_model_test_lens_local_runner_bridge_service_planning_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-P1-Midplatform-Model-Test-Lens-Local-Asset-Import-UI-Patch-Execution-And-Post-Review-v1-001",
        "verify_flag": "local_asset_import_ui_patch_go_verified",
        "expected_go": UPSTREAM_UI_PATCH_EXPECTED_GO,
        "artifact_rel": (
            "_tmp_eval_out/p1_midplatform_model_test_lens_local_asset_import_ui_patch_execution_v1_smoke_v0/"
            "p1_midplatform_model_test_lens_local_asset_import_ui_patch_execution_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-Test-Board-Protected-Artifact-Rule-v1-001",
        "verify_flag": "test_board_protocol_go_verified",
        "expected_go": "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO",
        "artifact_rel": "_tmp_eval_out/test_board_protocol_v1_smoke_v0/test_board_protocol_review_v1.json",
    },
)

REQUIRED_VERIFY_FLAGS: Tuple[str, ...] = tuple(e["verify_flag"] for e in UPSTREAM_STAGE_REGISTRY)
UPSTREAM_PRIMARY_PHASE_REF = UPSTREAM_STAGE_REGISTRY[0]["phase_ref"]
GOVERNANCE_TEMPLATE_STAGE_REF = "ControlledTrialGovernanceLifecycleTemplateV1"


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
        path = _resolve_file(repo_root, entry["artifact_rel"])
        if path is None:
            verify_flags[flag] = False
            warnings.append(f"upstream.review_missing={entry['artifact_rel']}")
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            decision = data.get("final_decision") or data.get("decision", {}).get("final_decision")
            ok = decision == entry["expected_go"]
            verify_flags[flag] = ok
            if not ok:
                issues.append(f"upstream.go_mismatch={entry['phase_ref']} got={decision}")
        except (OSError, json.JSONDecodeError) as exc:
            verify_flags[flag] = False
            issues.append(f"upstream.read_error={entry['artifact_rel']}: {exc}")
    return stage_refs, verify_flags, issues, warnings
