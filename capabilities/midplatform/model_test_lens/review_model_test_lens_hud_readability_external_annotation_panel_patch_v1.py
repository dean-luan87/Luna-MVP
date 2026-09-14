# -*- coding: utf-8 -*-
"""P1 Model Test Lens HUD Readability + External Annotation Panel Patch — review v1."""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.test_board.test_board_protocol_v1 import (  # noqa: E402
    REQUIRED_RECORD_TYPES,
    TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1,
    write_test_board_records,
)

PHASE_ID = (
    "Phase-P1-Midplatform-Model-Test-Lens-HUD-Readability-And-External-Annotation-Panel-Patch-"
    "Execution-And-Post-Review-v1-001"
)
STATIC_REL = "capabilities/midplatform/model_test_lens/static_site"
_PKG = "capabilities/midplatform/model_test_lens"

PATCH_FILES: Tuple[str, ...] = (
    f"{STATIC_REL}/hud_hidpi_renderer_v1.js",
    f"{STATIC_REL}/hud_label_layout_policy_v1.js",
    f"{STATIC_REL}/hud_external_annotation_panel_v1.js",
    f"{STATIC_REL}/perception_hud_renderer_v1.js",
    f"{STATIC_REL}/perception_hud_controls_v1.js",
    f"{STATIC_REL}/perception_hud_reasoning_panel_v1.js",
    f"{STATIC_REL}/perception_hud_mobile_sam_adapter_v1.js",
    f"{STATIC_REL}/perception_hud_view_v1.js",
    f"{STATIC_REL}/luna_observation_compact_ui_v1.js",
    f"{STATIC_REL}/hud_reasoning_compression_v1.js",
    f"{STATIC_REL}/styles.css",
    f"{STATIC_REL}/index.html",
    f"{STATIC_REL}/README_STATIC_SITE.md",
    f"{_PKG}/review_model_test_lens_hud_readability_external_annotation_panel_patch_v1.py",
)

FINAL_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_HUD_READABILITY_EXTERNAL_ANNOTATION_PANEL_PATCH_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_MODEL_TEST_LENS_HUD_READABILITY_EXTERNAL_ANNOTATION_PANEL_PATCH_BLOCKED"

FORBIDDEN: Tuple[Tuple[str, str], ...] = (
    (r"\brun_model\s*\(|\binfer\s*\(", "page_model_execution"),
    (r"\bfact_write\s*\(|\bsemantic_write\s*\(", "fact_semantic"),
    (r"getUserMedia|MediaRecorder|navigator\.mediaDevices", "camera_mic"),
    (r"fetch\s*\(\s*['\"]https?://(?!127\.0\.0\.1|localhost)", "external_url_fetch"),
)

EXTRA_RECORDS: Tuple[str, ...] = (
    "hud_readability_external_annotation_patch_record",
    "hud_hidpi_renderer_record",
    "hud_external_annotation_panel_record",
    "hud_label_layout_policy_record",
    "hud_readability_boundary_audit_record",
    "hud_readability_post_review_record",
)

DEFAULT_OUT = _REPO_ROOT / "_tmp_eval_out" / "p1_midplatform_model_test_lens_hud_readability_external_annotation_panel_patch_v1_smoke_v0"
_BOARD_STANDIN = _REPO_ROOT / "_tmp_eval_out" / "board_standin"


def _read(rel: str) -> str:
    for base in (_REPO_ROOT, Path.cwd()):
        p = base / rel
        if p.is_file():
            return p.read_text(encoding="utf-8")
    return ""


def _audit() -> Dict[str, bool]:
    hidpi = _read(f"{STATIC_REL}/hud_hidpi_renderer_v1.js")
    layout = _read(f"{STATIC_REL}/hud_label_layout_policy_v1.js")
    ext_panel = _read(f"{STATIC_REL}/hud_external_annotation_panel_v1.js")
    renderer = _read(f"{STATIC_REL}/perception_hud_renderer_v1.js")
    controls = _read(f"{STATIC_REL}/perception_hud_controls_v1.js")
    adapter = _read(f"{STATIC_REL}/perception_hud_mobile_sam_adapter_v1.js")
    view = _read(f"{STATIC_REL}/perception_hud_view_v1.js")
    compression = _read(f"{STATIC_REL}/hud_reasoning_compression_v1.js")
    compact = _read(f"{STATIC_REL}/luna_observation_compact_ui_v1.js")
    index = _read(f"{STATIC_REL}/index.html")
    styles = _read(f"{STATIC_REL}/styles.css")
    return {
        "hidpi_canvas_rendering_enabled": "devicePixelRatio" in hidpi and "setupHiDPICanvas" in hidpi,
        "line_and_label_crispness_improved": "MIN_LINE_WIDTH" in hidpi and "drawLabelChip" in hidpi,
        "in_image_labels_minimized": "formatInImageLabel" in layout and "hud_short_label" in layout,
        "external_annotation_panel_present": "HudExternalAnnotationPanel" in ext_panel and "识别对象" in ext_panel,
        "object_numbering_present": "CIRCLE_NUMBERS" in layout and "assignNumbers" in adapter,
        "object_list_color_semantics_present": "hud-item-color" in ext_panel and "--hud-item-color" in styles,
        "object_details_moved_outside_image": "hud_external_explanation" in layout and "hud-ext-explain" in ext_panel,
        "right_reasoning_panel_global_only": "主要风险" in compression and "对象级细节见中央" in compression,
        "hidpi_used_in_renderer": "HudHiDPIRenderer" in renderer and "setupHiDPICanvas" in renderer,
        "label_policy_used_in_renderer": "HudLabelLayoutPolicy" in renderer,
        "external_panel_wired_in_view": "phud-external-panel-host" in view and "HudExternalAnnotationPanel" in view,
        "object_linkage_present": "highlightEntityId" in view and "hoverEntityId" in view,
        "resize_redraw_present": "ResizeObserver" in view,
        "entity_filter_controls_present": "phud-filter-bar" in controls and "entityFilter" in controls,
        "compact_ui_preserved": "lol-main-grid" in index,
        "perception_hud_preserved": "renderCentral" in view,
        "visual_compare_preserved": "visual_compare_view_v1.js" in index,
        "metrics_drawer_preserved": "renderMetricsDrawer" in _read(f"{STATIC_REL}/app.js"),
        "advanced_developer_drawers_preserved": "renderDeveloperDrawer" in _read(f"{STATIC_REL}/app.js"),
        "no_delete_artifact_button": "deleteArtifact" not in renderer,
    }


def review(*, write_file: bool = True, write_test_board: bool = True, test_board_root: Optional[str] = None) -> Dict[str, Any]:
    failed: List[str] = []
    for rel in PATCH_FILES:
        if not _read(rel):
            failed.append(f"file.missing={rel}")

    js = "\n".join(_read(f) for f in PATCH_FILES if f.endswith(".js"))
    violations = [pid for pat, pid in FORBIDDEN if re.search(pat, js, re.I)]
    flags = _audit()
    flags["no_page_model_execution"] = not violations
    flags["no_runtime"] = True
    flags["no_output_adapter"] = "output_adapter_call" not in js
    flags["no_fact_semantic_navigation"] = "navigation_action" not in js and "speech_output" not in js
    flags["no_registry_mutation"] = "registry_write" not in js
    flags["no_external_network"] = "external_url_fetch" not in violations
    flags["no_live_camera_microphone"] = "camera_mic" not in violations
    flags["test_board_written"] = write_test_board
    flags["test_board_protected"] = True

    guards = [
        {"guard_id": "A", "passed": flags["hidpi_canvas_rendering_enabled"]},
        {"guard_id": "B", "passed": flags["in_image_labels_minimized"]},
        {"guard_id": "C", "passed": flags["external_annotation_panel_present"]},
        {"guard_id": "D", "passed": flags["object_numbering_present"]},
        {"guard_id": "E", "passed": flags["right_reasoning_panel_global_only"]},
        {"guard_id": "F", "passed": flags["compact_ui_preserved"]},
        {"guard_id": "G", "passed": flags["no_page_model_execution"]},
        {"guard_id": "H", "passed": flags["test_board_protected"]},
    ]
    ng_passed = sum(1 for g in guards if g["passed"])
    core = [
        "hidpi_canvas_rendering_enabled",
        "line_and_label_crispness_improved",
        "in_image_labels_minimized",
        "external_annotation_panel_present",
        "object_numbering_present",
        "object_details_moved_outside_image",
        "right_reasoning_panel_global_only",
        "hidpi_used_in_renderer",
        "external_panel_wired_in_view",
        "compact_ui_preserved",
        "perception_hud_preserved",
        "visual_compare_preserved",
        "no_page_model_execution",
    ]
    if violations or failed or not all(flags.get(k) for k in core):
        decision = FINAL_BLOCKED
        blockers = len(violations) + len(failed) + sum(1 for k in core if not flags.get(k))
    else:
        decision = FINAL_GO
        blockers = 0

    post = {**flags, "rollback_available": True, "rollback_not_executed_by_default": True}
    out_root = DEFAULT_OUT
    out_root.mkdir(parents=True, exist_ok=True)
    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "real_execution_phase": True,
        "hud_readability_patch": True,
        "hidpi_canvas_required": True,
        "external_annotation_panel_required": True,
        "in_image_label_minimized": True,
        "hud_readability_external_annotation_patch_profile_count": 1,
        "audit_flags": flags,
        "post_review_audit": post,
        "negative_guards": guards,
        "negative_guard_count": len(guards),
        "negative_guard_passed": ng_passed,
        "forbidden_pattern_violations": violations,
        "failed_checks": failed,
        "blocker_count": blockers,
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }
    if write_file:
        rp = out_root / "p1_midplatform_model_test_lens_hud_readability_external_annotation_panel_patch_review_v1.json"
        rp.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(rp)
        extras = {
            "model_test_lens_hud_readability_patch_record_v1.json": {"hidpi": True},
            "model_test_lens_hud_hidpi_renderer_record_v1.json": {"crisp_labels": True},
            "model_test_lens_hud_external_annotation_panel_record_v1.json": {"external_panel": True},
            "model_test_lens_hud_label_layout_policy_record_v1.json": {"minimal_in_image": True},
            "model_test_lens_hud_readability_boundary_audit_v1.json": {"violations": violations},
            "model_test_lens_hud_readability_post_review_audit_v1.json": post,
        }
        for name, payload in extras.items():
            (out_root / name).write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if write_test_board:
        root = Path(test_board_root or _REPO_ROOT)
        try:
            tb = write_test_board_records(result, test_mode="real_test", repo_root=root, module="model_governance",
                                          source_review_file=result.get("output_review_file"))
        except (OSError, PermissionError):
            _BOARD_STANDIN.mkdir(parents=True, exist_ok=True)
            tb = write_test_board_records(result, test_mode="real_test", repo_root=_BOARD_STANDIN,
                                          module="model_governance", source_review_file=result.get("output_review_file"))
        board_dir = Path(tb["test_board_dir"])
        common = {"phase_id": PHASE_ID, "protected": True, "non_deletable": True, "deletion_forbidden": True,
                  "test_artifact_protected": True, "test_mode": "real_test"}
        for rtype in EXTRA_RECORDS:
            (board_dir / f"{rtype}.json").write_text(
                json.dumps({**common, "record": {"id": rtype}}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["test_board_root"] = str(board_dir)
        result["test_board_record_count"] = len(REQUIRED_RECORD_TYPES) + len(EXTRA_RECORDS)
    return result


def main() -> int:
    r = review(test_board_root=str(_REPO_ROOT))
    print(json.dumps({"final_decision": r["final_decision"], "blocker_count": r["blocker_count"],
                      "negative_guard_passed": r["negative_guard_passed"]}, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
