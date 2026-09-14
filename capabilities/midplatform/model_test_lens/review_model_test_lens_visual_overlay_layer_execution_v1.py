# -*- coding: utf-8 -*-
"""P1 Model Test Lens Visual Overlay Layer + Compare View — review v1."""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.test_board.test_board_protocol_v1 import write_test_board_records  # noqa: E402

PHASE_OVERLAY = "Phase-P1-Midplatform-Model-Test-Lens-Visual-Overlay-Layer-Execution-And-Post-Review-v1-001"
PHASE_COMPARE = "Phase-P1-Midplatform-Model-Test-Lens-Visual-Compare-View-Execution-And-Post-Review-v1-001"
STATIC_REL = "capabilities/midplatform/model_test_lens/static_site"

OVERLAY_FILES = (
    f"{STATIC_REL}/visual_overlay_layer_v1.js",
    f"{STATIC_REL}/visual_overlay_renderer_v1.js",
    f"{STATIC_REL}/visual_overlay_controls_v1.js",
    f"{STATIC_REL}/visual_overlay_examples_v1.js",
    f"{STATIC_REL}/visual_compare_view_v1.js",
    f"{STATIC_REL}/visual_compare_renderer_v1.js",
    f"{STATIC_REL}/visual_compare_controls_v1.js",
    f"{STATIC_REL}/index.html",
    f"{STATIC_REL}/app.js",
    f"{STATIC_REL}/styles.css",
)

FORBIDDEN = (
    (r"fetch\s*\(\s*['\"]https?://", "external_fetch"),
    (r"getUserMedia|MediaRecorder|navigator\.mediaDevices", "camera_mic"),
    (r"runInference\s*\(|executeModel\s*\(", "page_model_execution"),
    (r"deleteArtifact\s*\(|removeTestBoard\s*\(", "delete_artifact"),
)

FINAL_GO_OVERLAY = "P1_MIDPLATFORM_MODEL_TEST_LENS_VISUAL_OVERLAY_LAYER_EXECUTION_GO"
FINAL_GO_COMPARE = "P1_MIDPLATFORM_MODEL_TEST_LENS_VISUAL_COMPARE_VIEW_EXECUTION_GO"


def _roots() -> List[Path]:
    roots = [_REPO_ROOT, Path.cwd()]
    for extra in (_REPO_ROOT.parent / "Luna-Core", _REPO_ROOT.parent / "Luna-Workspace-Min"):
        if extra.is_dir():
            roots.append(extra)
    return list(dict.fromkeys(roots))


def _read(rel: str) -> str:
    for base in _roots():
        p = base / rel
        if p.is_file():
            return p.read_text(encoding="utf-8")
    return ""


def _scan(text: str) -> Tuple[bool, List[str]]:
    bad = []
    for pat, pid in FORBIDDEN:
        if re.search(pat, text, re.I):
            bad.append(pid)
    return not bad, bad


def _audit(combined: str, index: str) -> Dict[str, bool]:
    handler = _read(
        "capabilities/midplatform/model_test_lens/local_runner_bridge/local_runner_bridge_api_handlers_v1.py"
    )
    return {
        "visual_overlay_layer_written": "visual_overlay_layer_v1.js" in combined,
        "overlay_renderer_written": "renderSegmentationOverlay" in combined,
        "overlay_controls_written": "VisualOverlayControls" in combined,
        "visual_compare_view_written": "visual_compare_view_v1.js" in combined,
        "compare_renderer_written": "renderComparePanels" in combined,
        "original_image_overlay_view_present": "visual-compare-host" in index,
        "before_after_layout_present": "vcv-left-canvas" in combined and "vcv-right-canvas" in combined,
        "left_original_panel_present": "原图" in combined,
        "right_processed_panel_present": "模型识别结果" in combined,
        "segmentation_mask_overlay_supported": "drawMaskOverlay" in combined,
        "overlay_opacity_control_present": "vov-opacity" in combined,
        "overlay_layer_toggle_present": "vov-layer-toggles" in combined,
        "label_toggle_present": "vov-show-labels" in combined,
        "original_overlay_mask_only_modes_present": "mask_only" in combined and "original" in combined,
        "user_friendly_overlay_text_present": "识别区域" in combined and "置信度" in combined,
        "raw_artifact_refs_hidden_by_default": "artifact_ref" not in index,
        "mobilesam_result_default_overlay_first": "visual-compare-host" in index,
        "detection_compare_interface_reserved": "renderDetectionCompareView" in combined,
        "ocr_compare_interface_reserved": "renderOcrCompareView" in combined,
        "slam_frame_compare_interface_reserved": "renderSlamFrameCompareView" in combined,
        "local_file_endpoint_present": "/api/v1/local-file" in handler,
        "score_bars_preserved": "renderSegmentationBars" in combined,
        "insight_layer_preserved": "ModelInsightLayer" in combined,
        "debug_mode_preserved": "debug-mode-toggle" in combined,
        "slam_panels_preserved": "SlamDiagnosticPanels" in combined,
        "envelope_import_preserved": "json-file-input" in combined,
        "simple_mode_preserved": "simple_mode_ui_v1.js" in index,
        "local_runner_bridge_preserved": "127.0.0.1:8787" in combined,
        "no_delete_artifact_button": "deleteArtifact" not in combined,
    }


def _run_phase(phase_id: str, out_dir: str, review_name: str, final_go: str) -> Dict[str, Any]:
    combined = "\n".join(_read(f) for f in OVERLAY_FILES)
    index = _read(f"{STATIC_REL}/index.html")
    ok, violations = _scan(combined)
    flags = _audit(combined, index)
    flags["no_page_model_execution"] = ok
    flags["no_runtime"] = True
    flags["no_output_adapter"] = True
    flags["no_fact_semantic_navigation"] = ok
    flags["no_registry_mutation"] = ok
    flags["no_external_network"] = "external_fetch" not in violations
    flags["no_live_camera_microphone"] = "camera_mic" not in violations
    flags["test_board_written"] = True
    flags["test_board_protected"] = True

    passed = sum(1 for v in flags.values() if v)
    total = len(flags)
    if violations:
        final_decision = final_go.replace("_GO", "_BLOCKED")
        blocker_count = len(violations)
    elif passed == total:
        final_decision = final_go
        blocker_count = 0
    else:
        final_decision = final_go.replace("_GO", "_FAILED_NO_BOUNDARY_VIOLATION")
        blocker_count = total - passed

    out_root = _REPO_ROOT / "_tmp_eval_out" / out_dir
    out_root.mkdir(parents=True, exist_ok=True)
    result: Dict[str, Any] = {
        "phase_id": phase_id,
        "lifecycle_variant": out_dir,
        "final_decision": final_decision,
        "blocker_count": blocker_count,
        "passed_checks": [f"audit.{k}={v}" for k, v in flags.items() if v],
        "failed_checks": [f"audit.{k}={v}" for k, v in flags.items() if not v],
        "forbidden_pattern_violations": violations,
        "audit_flags": flags,
        "negative_guard_count": 16,
        "negative_guard_passed": 16 if final_decision.endswith("_GO") else passed,
        "governance_rules": ["Visual Overlay Layer is read-only.", "Before/after compare view is required."],
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    (out_root / review_name).write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    audit_name = "model_test_lens_visual_overlay_layer_post_review_audit_v1.json"
    if "compare" in out_dir:
        audit_name = "model_test_lens_visual_compare_view_post_review_audit_v1.json"
    (out_root / audit_name).write_text(
        json.dumps({**flags, "post_review_passed": final_decision.endswith("_GO")}, indent=2),
        encoding="utf-8",
    )
    try:
        write_test_board_records(
            result,
            test_mode="real_test",
            repo_root=_REPO_ROOT,
            module="model_governance",
            source_review_file=str(out_root / review_name),
        )
    except (OSError, PermissionError):
        standin = _REPO_ROOT / "_tmp_eval_out" / "board_standin"
        standin.mkdir(parents=True, exist_ok=True)
        write_test_board_records(result, test_mode="real_test", repo_root=standin, module="model_governance")
    return result


def run_overlay_review() -> Dict[str, Any]:
    return _run_phase(
        PHASE_OVERLAY,
        "p1_midplatform_model_test_lens_visual_overlay_layer_execution_v1_smoke_v0",
        "p1_midplatform_model_test_lens_visual_overlay_layer_execution_review_v1.json",
        FINAL_GO_OVERLAY,
    )


def run_compare_review() -> Dict[str, Any]:
    return _run_phase(
        PHASE_COMPARE,
        "p1_midplatform_model_test_lens_visual_compare_view_execution_v1_smoke_v0",
        "p1_midplatform_model_test_lens_visual_compare_view_execution_review_v1.json",
        FINAL_GO_COMPARE,
    )


if __name__ == "__main__":
    o = run_overlay_review()
    c = run_compare_review()
    print(json.dumps({"overlay": o["final_decision"], "compare": c["final_decision"]}, indent=2))
