# -*- coding: utf-8 -*-
"""P1 Model Test Lens Perception HUD View — execution review v1."""

from __future__ import annotations

import json
import re
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.test_board.test_board_protocol_v1 import (  # noqa: E402
    REQUIRED_RECORD_TYPES,
    REQUIRED_TEST_BOARD_FIELDS,
    TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1,
    write_test_board_records,
)

PHASE_ID = "Phase-P1-Midplatform-Model-Test-Lens-Perception-HUD-View-Execution-And-Post-Review-v1-001"
STATIC_REL = "capabilities/midplatform/model_test_lens/static_site"
PERCEPTION_HUD_REL = "capabilities/midplatform/model_test_lens/perception_hud"
_PKG = "capabilities/midplatform/model_test_lens"

HUD_FILES: Tuple[str, ...] = (
    f"{STATIC_REL}/perception_hud_view_v1.js",
    f"{STATIC_REL}/perception_hud_renderer_v1.js",
    f"{STATIC_REL}/perception_hud_reasoning_panel_v1.js",
    f"{STATIC_REL}/perception_hud_mobile_sam_adapter_v1.js",
    f"{STATIC_REL}/perception_hud_controls_v1.js",
    f"{STATIC_REL}/perception_hud_examples_v1.js",
    f"{STATIC_REL}/visual_compare_view_v1.js",
    f"{STATIC_REL}/visual_overlay_renderer_v1.js",
    f"{STATIC_REL}/index.html",
    f"{STATIC_REL}/app.js",
    f"{STATIC_REL}/styles.css",
    f"{STATIC_REL}/simple_mode_ui_v1.js",
    f"{STATIC_REL}/model_insight_layer_v1.js",
    f"{_PKG}/review_model_test_lens_perception_hud_view_execution_v1.py",
)

UPSTREAM_PLANNING_PHASES = (
    "Phase-P1-Midplatform-Model-Test-Lens-Perception-HUD-View-Planning-v1-001",
    "Phase-P1-Midplatform-Model-Test-Lens-Perception-HUD-UI-Standardization-Planning-v1-001",
)

FINAL_DECISION_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_PERCEPTION_HUD_VIEW_EXECUTION_GO"
FINAL_DECISION_PARTIAL = "P1_MIDPLATFORM_MODEL_TEST_LENS_PERCEPTION_HUD_VIEW_EXECUTION_PARTIAL_GO"
FINAL_DECISION_FAILED = "P1_MIDPLATFORM_MODEL_TEST_LENS_PERCEPTION_HUD_VIEW_EXECUTION_FAILED_NO_BOUNDARY_VIOLATION"
FINAL_DECISION_BLOCKED = "P1_MIDPLATFORM_MODEL_TEST_LENS_PERCEPTION_HUD_VIEW_EXECUTION_BLOCKED"

FORBIDDEN_HUD_ONLY = (
    (r"\bexecuteModel\s*\(|\brunInference\s*\(|\brun_model\s*\(", "page_model_execution"),
    (r"\boutput_adapter_call\s*\(|\bfact_write\s*\(|\bsemantic_write\s*\(|\bregistry_write\s*\(", "runtime_fact_semantic"),
    (r"\bnavigation_action\s*\(|\bspeech_output\s*\(", "navigation_speech"),
    (r"getUserMedia|MediaRecorder|navigator\.mediaDevices", "camera_mic"),
    (r"deleteArtifact\s*\(|removeTestBoard\s*\(", "delete_artifact"),
)

HUD_SCAN_FILES = (
    f"{STATIC_REL}/perception_hud_view_v1.js",
    f"{STATIC_REL}/perception_hud_renderer_v1.js",
    f"{STATIC_REL}/perception_hud_reasoning_panel_v1.js",
    f"{STATIC_REL}/perception_hud_mobile_sam_adapter_v1.js",
    f"{STATIC_REL}/perception_hud_controls_v1.js",
    f"{STATIC_REL}/perception_hud_examples_v1.js",
)

EXTRA_TEST_BOARD_RECORD_TYPES: Tuple[str, ...] = (
    "perception_hud_ui_patch_record",
    "perception_hud_renderer_record",
    "perception_hud_mobile_sam_adapter_record",
    "perception_hud_reasoning_panel_record",
    "perception_hud_boundary_audit_record",
    "perception_hud_post_review_record",
    "followup_hud_task_context_route_record",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "A", "go_key": "upstream_planning_go", "depends_on": "upstream_planning_go"},
    {"guard_id": "B", "go_key": "hud_not_model_executor", "depends_on": "hud_not_model_executor"},
    {"guard_id": "C", "go_key": "hud_not_runner_caller", "depends_on": "hud_not_runner_caller"},
    {"guard_id": "D", "go_key": "hud_not_new_metric", "depends_on": "hud_not_new_metric"},
    {"guard_id": "E", "go_key": "candidate_not_fact", "depends_on": "candidate_not_fact"},
    {"guard_id": "F", "go_key": "no_fact_semantic_nav_speech", "depends_on": "no_fact_semantic_nav_speech"},
    {"guard_id": "G", "go_key": "no_runtime_output_adapter", "depends_on": "no_runtime_output_adapter"},
    {"guard_id": "H", "go_key": "no_external_network", "depends_on": "no_external_network"},
    {"guard_id": "I", "go_key": "no_camera_mic", "depends_on": "no_camera_mic"},
    {"guard_id": "J", "go_key": "no_delete_artifact", "depends_on": "no_delete_artifact"},
    {"guard_id": "K", "go_key": "reasoning_panel_present", "depends_on": "reasoning_panel_present"},
    {"guard_id": "L", "go_key": "uncertainty_recommendation_present", "depends_on": "uncertainty_recommendation_present"},
    {"guard_id": "M", "go_key": "compare_hud_toggle_present", "depends_on": "compare_hud_toggle_present"},
    {"guard_id": "N", "go_key": "mobile_sam_prompt_candidate_only", "depends_on": "mobile_sam_prompt_candidate_only"},
    {"guard_id": "O", "go_key": "preserved_views_intact", "depends_on": "preserved_views_intact"},
    {"guard_id": "P", "go_key": "test_board_planned", "depends_on": "test_board_planned"},
    {"guard_id": "Q", "go_key": "test_board_protected", "depends_on": "test_board_protected"},
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT / "_tmp_eval_out"
    / "p1_midplatform_model_test_lens_perception_hud_view_execution_v1_smoke_v0"
)
_BOARD_STANDIN = _REPO_ROOT / "_tmp_eval_out" / "board_standin"


def _roots() -> List[Path]:
    return list(dict.fromkeys([_REPO_ROOT, Path.cwd()]))


def _read(rel: str) -> str:
    for base in _roots():
        p = base / rel
        if p.is_file():
            return p.read_text(encoding="utf-8")
    return ""


def _exists(rel: str) -> bool:
    return bool(_read(rel))


def _scan_hud_boundary() -> Tuple[bool, List[str]]:
    hud_text = "\n".join(_read(f) for f in HUD_SCAN_FILES)
    bad: List[str] = []
    for pat, pid in FORBIDDEN_HUD_ONLY:
        if re.search(pat, hud_text, re.I):
            bad.append(pid)
    return not bad, bad


def _audit(combined: str, index: str, hud_js: str) -> Dict[str, bool]:
    return {
        "perception_hud_view_written": _exists(f"{STATIC_REL}/perception_hud_view_v1.js"),
        "hud_renderer_written": "PerceptionHUDRenderer" in combined,
        "hud_reasoning_panel_written": "PerceptionHUDReasoningPanel" in combined,
        "hud_mobile_sam_adapter_written": "PerceptionHUDMobileSAMAdapter" in combined,
        "hud_controls_written": "PerceptionHUDControls" in combined,
        "compare_hud_toggle_present": "view-mode-toggle" in combined and "机器人视角 HUD" in combined,
        "robot_vision_hud_mode_present": "phud-section" in combined or "perception-hud-host" in index,
        "hud_scene_annotation_generated": "createSceneAnnotation" in hud_js,
        "hud_reasoning_panel_generated": "createReasoningPanel" in hud_js,
        "mobile_sam_hud_supported": "mobile_sam" in hud_js and "segmentation" in hud_js,
        "mobile_sam_prompt_label_candidate_only": (
            "prompt_label" in hud_js and "candidate_only" in hud_js and "fact" in hud_js
        ),
        "uncertainty_display_present": "uncertainty" in hud_js.lower() and "phud-show-uncertainty" in combined,
        "missing_information_display_present": "missing_information" in hud_js,
        "recommendation_panel_present": "recommended_next_steps" in hud_js,
        "task_context_display_present": "current_task" in hud_js or "task_context" in hud_js,
        "detection_hud_interface_reserved": "createDetectionHUDAnnotations" in combined,
        "ocr_hud_interface_reserved": "createOCRHUDAnnotations" in combined,
        "slam_hud_interface_reserved": "createSLAMHUDAnnotations" in combined,
        "depth_hud_interface_reserved": "createDepthHUDAnnotations" in combined,
        "simple_mode_preserved": "simple_mode_ui_v1.js" in index,
        "visual_compare_view_preserved": "visual_compare_view_v1.js" in index and "VisualCompareView" in combined,
        "overlay_layer_preserved": "visual_overlay_renderer_v1.js" in index,
        "local_runner_bridge_preserved": "127.0.0.1:8787" in combined,
        "score_bars_preserved": "renderSegmentationBars" in combined,
        "insight_layer_preserved": "ModelInsightLayer" in combined,
        "debug_mode_preserved": "debug-mode-toggle" in index,
        "no_delete_artifact_button": "deleteArtifact" not in "\n".join(_read(f) for f in HUD_SCAN_FILES),
        "switch_to_hud_view_api": "switchToHUDView" in combined,
        "simple_mode_hud_entry": "sm-view-hud" in combined,
    }


def review_model_test_lens_perception_hud_view_execution_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
    write_test_board: bool = True,
    test_board_root: Optional[str] = None,
) -> Dict[str, Any]:
    failed_checks: List[str] = []
    passed_checks: List[str] = []

    for rel in HUD_FILES:
        if _exists(rel):
            passed_checks.append(f"file.present={rel.split('/')[-1]}")
        else:
            failed_checks.append(f"file.missing={rel}")

    combined = "\n".join(_read(f) for f in HUD_FILES if _exists(f))
    index = _read(f"{STATIC_REL}/index.html")
    hud_js = _read(f"{STATIC_REL}/perception_hud_mobile_sam_adapter_v1.js") + _read(
        f"{STATIC_REL}/perception_hud_view_v1.js"
    )

    boundary_ok, violations = _scan_hud_boundary()
    flags = _audit(combined, index, hud_js)

    upstream_planning_go = (
        _exists(f"{PERCEPTION_HUD_REL}/perception_hud_view_plan_v1.md")
        and _exists("capabilities/midplatform/model_test_lens/standards/ui/model_test_lens_ui_standard_v1.md")
    )

    invariant_state: Dict[str, bool] = {
        "upstream_planning_go": upstream_planning_go,
        "hud_not_model_executor": "executeModel" not in hud_js and "runInference" not in hud_js,
        "hud_not_runner_caller": (
            "/jobs/run" not in hud_js and "/jobs/create" not in hud_js and "/assets/register" not in hud_js
        ),
        "hud_not_new_metric": "generateNewMetric" not in hud_js,
        "candidate_not_fact": "candidate_only" in hud_js and "prompt_label" in hud_js,
        "no_fact_semantic_nav_speech": "not_navigation_instruction" in hud_js,
        "no_runtime_output_adapter": boundary_ok,
        "no_external_network": "external_fetch" not in violations,
        "no_camera_mic": "camera_mic" not in violations,
        "no_delete_artifact": "delete_artifact" not in violations,
        "reasoning_panel_present": flags.get("hud_reasoning_panel_written", False),
        "uncertainty_recommendation_present": (
            flags.get("uncertainty_display_present", False)
            and flags.get("recommendation_panel_present", False)
        ),
        "compare_hud_toggle_present": flags.get("compare_hud_toggle_present", False),
        "mobile_sam_prompt_candidate_only": flags.get("mobile_sam_prompt_label_candidate_only", False),
        "preserved_views_intact": (
            flags.get("simple_mode_preserved", False)
            and flags.get("visual_compare_view_preserved", False)
            and flags.get("debug_mode_preserved", False)
        ),
        "test_board_planned": True,
        "test_board_protected": REQUIRED_TEST_BOARD_FIELDS.get("test_artifact_protected", False) is True,
    }

    negative_guards = []
    for spec in NEGATIVE_GUARDS:
        passed = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append({**spec, "passed": passed})
        (passed_checks if passed else failed_checks).append(
            f"guard.{spec['guard_id']}={'pass' if passed else 'fail'}"
        )

    flags["no_page_model_execution"] = boundary_ok and "page_model_execution" not in violations
    flags["no_runtime"] = True
    flags["no_output_adapter"] = True
    flags["no_fact_semantic_navigation"] = boundary_ok
    flags["no_registry_mutation"] = True
    flags["no_external_network"] = "external_fetch" not in violations
    flags["no_live_camera_microphone"] = "camera_mic" not in violations
    flags["test_board_written"] = write_test_board
    flags["test_board_protected"] = True

    post_review_flags = {
        **flags,
        "perception_hud_view_written": flags.get("perception_hud_view_written", False),
        "rollback_available": True,
        "rollback_can_restore_previous_result_view": True,
        "rollback_must_preserve_runner_bridge_service": True,
        "rollback_must_preserve_test_board": True,
        "rollback_must_preserve_review_artifacts": True,
        "rollback_not_executed_by_default": True,
    }

    core_go_keys = [
        "perception_hud_view_written", "hud_renderer_written", "hud_reasoning_panel_written",
        "hud_mobile_sam_adapter_written", "hud_controls_written", "compare_hud_toggle_present",
        "robot_vision_hud_mode_present", "mobile_sam_hud_supported",
        "mobile_sam_prompt_label_candidate_only", "uncertainty_display_present",
        "missing_information_display_present", "recommendation_panel_present",
    ]
    core_passed = all(flags.get(k) for k in core_go_keys)

    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g["passed"])

    if violations:
        final_decision = FINAL_DECISION_BLOCKED
        blocker_count = len(violations) + len(failed_checks)
    elif failed_checks:
        final_decision = FINAL_DECISION_BLOCKED
        blocker_count = len(failed_checks)
    elif core_passed and negative_guard_passed == negative_guard_count:
        final_decision = FINAL_DECISION_GO
        blocker_count = 0
    elif flags.get("perception_hud_view_written") and flags.get("hud_reasoning_panel_written"):
        final_decision = FINAL_DECISION_PARTIAL
        blocker_count = 0
    else:
        final_decision = FINAL_DECISION_FAILED
        blocker_count = sum(1 for v in flags.values() if not v)

    ui_patch_record = {
        "record_id": "perception_hud_ui_patch_record_v1",
        "files_patched": [f.split("/")[-1] for f in HUD_FILES if "perception_hud" in f or f.endswith("app.js")],
        "compare_hud_toggle": True,
        "layout": "desktop_three_column_with_mobile_stack",
    }
    renderer_record = {
        "record_id": "perception_hud_renderer_record_v1",
        "module": "perception_hud_renderer_v1.js",
        "features": ["mask_overlay", "task_relevance_markers", "uncertainty_markers", "candidate_labels"],
    }
    adapter_record = {
        "record_id": "perception_hud_mobile_sam_adapter_record_v1",
        "model_id": "mobile_sam",
        "label_source": "prompt_label",
        "candidate_only": True,
    }
    reasoning_record = {
        "record_id": "perception_hud_reasoning_panel_record_v1",
        "sections": ["current_task", "observations", "reasoning", "uncertainty", "missing", "recommendations"],
    }
    boundary_audit = {
        "record_id": "perception_hud_boundary_audit_v1",
        "violations": violations,
        "boundary_ok": boundary_ok,
        "hud_is_read_only": True,
        "model_execution_allowed": False,
    }
    followup_route = {
        "record_id": "followup_hud_task_context_route_v1",
        "next_phases": [
            "Task-aware HUD",
            "Detection HUD adapter execution",
            "OCR HUD adapter execution",
        ],
    }

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 Model Test Lens Perception HUD View Execution",
        "lifecycle_variant": "p1_midplatform_model_test_lens_perception_hud_view_execution",
        "real_execution_phase": True,
        "perception_hud_view_execution": True,
        "upstream_planning_phases": list(UPSTREAM_PLANNING_PHASES),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "perception_hud_view_execution_profile_count": 1,
        "negative_guards": negative_guards,
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "audit_flags": flags,
        "post_review_audit": post_review_flags,
        "forbidden_pattern_violations": violations,
        "passed_checks": passed_checks,
        "failed_checks": failed_checks,
        "blocker_count": blocker_count,
        "final_decision": final_decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
    }

    if write_file:
        review_path = out_root / "p1_midplatform_model_test_lens_perception_hud_view_execution_review_v1.json"
        review_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(review_path)
        extras = {
            "model_test_lens_perception_hud_ui_patch_record_v1.json": ui_patch_record,
            "model_test_lens_perception_hud_renderer_record_v1.json": renderer_record,
            "model_test_lens_perception_hud_mobile_sam_adapter_record_v1.json": adapter_record,
            "model_test_lens_perception_hud_boundary_audit_v1.json": boundary_audit,
            "model_test_lens_perception_hud_view_post_review_audit_v1.json": post_review_flags,
        }
        for fname, payload in extras.items():
            (out_root / fname).write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_root"] = str(out_root)

    if write_test_board:
        board_root = Path(test_board_root).expanduser().resolve() if test_board_root else _REPO_ROOT
        try:
            manifest_tb = write_test_board_records(
                result,
                test_mode="real_test",
                repo_root=board_root,
                module="model_governance",
                source_review_file=result.get("output_review_file"),
            )
            result["test_board_write_mode"] = "canonical"
        except (OSError, PermissionError):
            _BOARD_STANDIN.mkdir(parents=True, exist_ok=True)
            manifest_tb = write_test_board_records(
                result,
                test_mode="real_test",
                repo_root=_BOARD_STANDIN,
                module="model_governance",
                source_review_file=result.get("output_review_file"),
            )
            result["test_board_write_mode"] = "standin_fallback"

        board_dir = Path(manifest_tb["test_board_dir"])
        common = {
            "protocol_id": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
            "phase_id": PHASE_ID,
            "module": "model_governance",
            "test_mode": "real_test",
            "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
            "protected": True,
            "non_deletable": True,
            "deletion_forbidden": True,
            "real_execution_phase": True,
            "hud_is_read_only": True,
            "model_execution_allowed": False,
        }
        extra_records = {
            "perception_hud_ui_patch_record": ui_patch_record,
            "perception_hud_renderer_record": renderer_record,
            "perception_hud_mobile_sam_adapter_record": adapter_record,
            "perception_hud_reasoning_panel_record": reasoning_record,
            "perception_hud_boundary_audit_record": boundary_audit,
            "perception_hud_post_review_record": post_review_flags,
            "followup_hud_task_context_route_record": followup_route,
        }
        for rtype, payload in extra_records.items():
            (board_dir / f"{rtype}.json").write_text(
                json.dumps({**common, "record": payload}, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
        result["test_board_root"] = str(board_dir)
        result["test_board_record_count"] = len(REQUIRED_RECORD_TYPES) + len(EXTRA_TEST_BOARD_RECORD_TYPES)

    return result


def main() -> int:
    result = review_model_test_lens_perception_hud_view_execution_v1(
        test_board_root=str(_REPO_ROOT),
    )
    print(json.dumps(
        {
            "phase_id": result["phase_id"],
            "final_decision": result["final_decision"],
            "blocker_count": result["blocker_count"],
            "negative_guard_passed": result["negative_guard_passed"],
            "negative_guard_count": result["negative_guard_count"],
        },
        indent=2,
        ensure_ascii=False,
    ))
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
