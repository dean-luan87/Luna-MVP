# -*- coding: utf-8 -*-
"""P1 Model Test Lens Simple Mode UX Patch Execution — registry v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.midplatform.model_test_lens.model_test_lens_simple_mode_ux_patch_execution_types_v1 import (
    UPSTREAM_RUNNER_BRIDGE_PLANNING_REF,
    UPSTREAM_RUNNER_BRIDGE_SKELETON_REF,
    UPSTREAM_UI_PATCH_REF,
)

UPSTREAM_UI_PATCH_EXPECTED_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_LOCAL_ASSET_IMPORT_UI_PATCH_EXECUTION_GO"
UPSTREAM_RUNNER_BRIDGE_SKELETON_EXPECTED_GO = (
    "P1_MIDPLATFORM_MODEL_TEST_LENS_LOCAL_RUNNER_BRIDGE_SERVICE_SKELETON_EXECUTION_GO"
)
UPSTREAM_RUNNER_BRIDGE_PLANNING_EXPECTED_GO = (
    "P1_MIDPLATFORM_MODEL_TEST_LENS_LOCAL_RUNNER_BRIDGE_SERVICE_PLANNING_GO"
)
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"

UPSTREAM_STAGE_REGISTRY: Tuple[Dict[str, Any], ...] = (
    {
        "phase_ref": UPSTREAM_UI_PATCH_REF,
        "verify": True,
        "verify_flag": "local_asset_import_ui_patch_go_verified",
        "expected_go": UPSTREAM_UI_PATCH_EXPECTED_GO,
        "artifact_rel": (
            "_tmp_eval_out/p1_midplatform_model_test_lens_local_asset_import_ui_patch_execution_v1_smoke_v0/"
            "p1_midplatform_model_test_lens_local_asset_import_ui_patch_execution_review_v1.json"
        ),
    },
    {
        "phase_ref": UPSTREAM_RUNNER_BRIDGE_SKELETON_REF,
        "verify": True,
        "verify_flag": "local_runner_bridge_skeleton_go_verified",
        "expected_go": UPSTREAM_RUNNER_BRIDGE_SKELETON_EXPECTED_GO,
        "artifact_rel": (
            "_tmp_eval_out/p1_midplatform_model_test_lens_local_runner_bridge_service_skeleton_execution_v1_smoke_v0/"
            "p1_midplatform_model_test_lens_local_runner_bridge_service_skeleton_execution_review_v1.json"
        ),
    },
    {
        "phase_ref": UPSTREAM_RUNNER_BRIDGE_PLANNING_REF,
        "verify": True,
        "verify_flag": "local_runner_bridge_planning_go_verified",
        "expected_go": UPSTREAM_RUNNER_BRIDGE_PLANNING_EXPECTED_GO,
        "artifact_rel": (
            "_tmp_eval_out/p1_midplatform_model_test_lens_local_runner_bridge_service_planning_v1_smoke_v0/"
            "p1_midplatform_model_test_lens_local_runner_bridge_service_planning_review_v1.json"
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
)

GOVERNANCE_TEMPLATE_STAGE_REF = "ControlledTrialGovernanceLifecycleTemplateV1"
UPSTREAM_PRIMARY_PHASE_REF = UPSTREAM_UI_PATCH_REF

REQUIRED_VERIFY_FLAGS: Tuple[str, ...] = tuple(
    entry["verify_flag"] for entry in UPSTREAM_STAGE_REGISTRY if entry.get("verify")
)


def verify_stages(artifact_roots: List[Path]) -> Dict[str, Any]:
    flags: Dict[str, bool] = {}
    details: List[Dict[str, Any]] = []
    for entry in UPSTREAM_STAGE_REGISTRY:
        flag = entry["verify_flag"]
        if not entry.get("verify"):
            flags[flag] = True
            continue
        artifact_rel = entry.get("artifact_rel", "")
        found = False
        go_ok = False
        for base in artifact_roots:
            p = base / artifact_rel
            if p.is_file():
                found = True
                try:
                    data = json.loads(p.read_text(encoding="utf-8"))
                    decision = data.get("final_decision") or data.get("decision", {}).get("final_decision")
                    expected = entry.get("expected_go")
                    if entry.get("verify_mode") == "file_exists":
                        go_ok = True
                    elif expected:
                        go_ok = decision == expected
                    else:
                        go_ok = True
                except (json.JSONDecodeError, OSError):
                    go_ok = False
                break
        flags[flag] = found and go_ok
        details.append({"phase_ref": entry["phase_ref"], "verify_flag": flag, "passed": flags[flag]})
    flags["upstream_go_verified"] = all(flags.get(e["verify_flag"], False) for e in UPSTREAM_STAGE_REGISTRY if e.get("verify"))
    return {"verify_flags": flags, "details": details}
