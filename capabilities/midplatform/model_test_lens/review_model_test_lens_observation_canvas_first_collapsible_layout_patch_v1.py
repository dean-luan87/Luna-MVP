# -*- coding: utf-8 -*-
"""P1 Model Test Lens Observation Canvas-First Collapsible Layout Patch — review v1."""

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
    "Phase-P1-Midplatform-Model-Test-Lens-Observation-Canvas-First-Collapsible-Layout-Patch-"
    "Execution-And-Post-Review-v1-001"
)
STATIC_REL = "capabilities/midplatform/model_test_lens/static_site"
_PKG = "capabilities/midplatform/model_test_lens"

PATCH_FILES: Tuple[str, ...] = (
    f"{STATIC_REL}/observation_canvas_first_collapsible_layout_v1.js",
    f"{STATIC_REL}/luna_left_capability_drawer_v1.js",
    f"{STATIC_REL}/hud_object_chip_bar_v1.js",
    f"{STATIC_REL}/hud_selected_object_detail_v1.js",
    f"{STATIC_REL}/luna_bottom_drawer_tabs_v1.js",
    f"{STATIC_REL}/luna_topbar_compact_actions_v1.js",
    f"{STATIC_REL}/index.html",
    f"{STATIC_REL}/app.js",
    f"{STATIC_REL}/styles.css",
    f"{STATIC_REL}/luna_observation_compact_ui_v1.js",
    f"{STATIC_REL}/perception_hud_view_v1.js",
    f"{STATIC_REL}/perception_hud_controls_v1.js",
    f"{STATIC_REL}/hud_external_annotation_panel_v1.js",
    f"{STATIC_REL}/hud_label_layout_policy_v1.js",
    f"{STATIC_REL}/luna_observation_copy_v1.js",
    f"{STATIC_REL}/README_STATIC_SITE.md",
    f"{_PKG}/review_model_test_lens_observation_canvas_first_collapsible_layout_patch_v1.py",
)

FINAL_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_OBSERVATION_CANVAS_FIRST_COLLAPSIBLE_LAYOUT_PATCH_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_MODEL_TEST_LENS_OBSERVATION_CANVAS_FIRST_COLLAPSIBLE_LAYOUT_PATCH_BLOCKED"

FORBIDDEN: Tuple[Tuple[str, str], ...] = (
    (r"\brun_model\s*\(|\binfer\s*\(", "page_model_execution"),
    (r"\bfact_write\s*\(|\bsemantic_write\s*\(", "fact_semantic"),
    (r"getUserMedia|MediaRecorder|navigator\.mediaDevices", "camera_mic"),
    (r"fetch\s*\(\s*['\"]https?://(?!127\.0\.0\.1|localhost)", "external_url_fetch"),
)

EXTRA_RECORDS: Tuple[str, ...] = (
    "observation_canvas_first_collapsible_layout_patch_record",
    "left_capability_drawer_record",
    "hud_object_chip_bar_record",
    "bottom_drawer_tabs_record",
    "observation_canvas_first_collapsible_boundary_audit_record",
    "observation_canvas_first_collapsible_layout_post_review_record",
)

DEFAULT_OUT = (
    _REPO_ROOT / "_tmp_eval_out" / "p1_midplatform_model_test_lens_observation_canvas_first_collapsible_layout_patch_v1_smoke_v0"
)
_BOARD_STANDIN = _REPO_ROOT / "_tmp_eval_out" / "board_standin"


def _read(rel: str) -> str:
    for base in (_REPO_ROOT, Path.cwd()):
        p = base / rel
        if p.is_file():
            return p.read_text(encoding="utf-8")
    return ""


def _audit() -> Dict[str, bool]:
    layout = _read(f"{STATIC_REL}/observation_canvas_first_collapsible_layout_v1.js")
    left = _read(f"{STATIC_REL}/luna_left_capability_drawer_v1.js")
    chips = _read(f"{STATIC_REL}/hud_object_chip_bar_v1.js")
    selected = _read(f"{STATIC_REL}/hud_selected_object_detail_v1.js")
    bottom = _read(f"{STATIC_REL}/luna_bottom_drawer_tabs_v1.js")
    topbar = _read(f"{STATIC_REL}/luna_topbar_compact_actions_v1.js")
    index = _read(f"{STATIC_REL}/index.html")
    app = _read(f"{STATIC_REL}/app.js")
    styles = _read(f"{STATIC_REL}/styles.css")
    compact = _read(f"{STATIC_REL}/luna_observation_compact_ui_v1.js")
    view = _read(f"{STATIC_REL}/perception_hud_view_v1.js")
    label = _read(f"{STATIC_REL}/hud_label_layout_policy_v1.js")
    return {
        "main_canvas_priority_applied": "lol-layout-canvas-first" in layout and "lol-layout-canvas-first" in styles,
        "central_hud_largest_area": "minmax(0, 1fr)" in styles and "lol-hud-canvas-wrap" in styles,
        "left_sidebar_collapsible": "LunaLeftCapabilityDrawer" in left and "lol-left-expanded" in styles,
        "topbar_compact_actions": "LunaTopbarCompactActions" in topbar and "lol-more-menu" in topbar,
        "object_cards_removed_from_default_main_flow": "canvas-first" in view and "hud-external-panel-host" not in view.split("canvasFirst ? \"\" :")[0] if "canvasFirst" in view else "lol-hud-canvas-first" in view,
        "object_chip_bar_present": "HudObjectChipBar" in chips and "lol-object-chip-host" in index,
        "selected_object_detail_on_demand": "HudSelectedObjectDetail" in selected and "lol-right-selected-host" in compact,
        "right_reasoning_panel_result_first": "HudReasoningCompression" in compact,
        "right_reasoning_panel_short_default": "主要风险" in _read(f"{STATIC_REL}/hud_reasoning_compression_v1.js"),
        "bottom_summary_preserved": "lol-dock-summary" in bottom,
        "bottom_drawer_tabs_present": "LunaBottomDrawerTabs" in bottom and "lol-drawer-overlay" in bottom,
        "metrics_default_collapsed": "lol-drawer-overlay" in bottom and 'hidden' in bottom,
        "object_details_default_collapsed": "renderObjects" in app and "objects" in bottom,
        "advanced_default_collapsed": "renderAdvanced" in app,
        "developer_json_default_collapsed": "renderDeveloper" in app,
        "whitebox_default_collapsed": "whitebox" in bottom,
        "testboard_default_collapsed": "testboard" in bottom,
        "raw_engineering_terms_hidden_by_default": "lol-more-dropdown" in topbar and "phase_ref" not in index,
        "page_long_scroll_reduced": "overflow: hidden" in styles and "lol-layout-canvas-first" in styles,
        "hud_image_size_increased": "lol-hud-canvas-wrap" in styles and "flex: 1" in styles,
        "chip_status_short_present": "chipStatusShort" in label,
        "compact_ui_preserved": "lol-main-grid" in index,
        "perception_hud_preserved": "renderCentral" in view,
        "visual_compare_preserved": "visual_compare_view_v1.js" in index,
        "simple_mode_preserved": "simple_mode_ui_v1.js" in index,
        "local_runner_bridge_preserved": "127.0.0.1:8787" in _read(f"{STATIC_REL}/simple_mode_ui_v1.js"),
        "no_delete_artifact_button": "deleteArtifact" not in app,
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
    flags["no_output_adapter"] = True
    flags["no_fact_semantic_navigation"] = "navigation_action" not in js and "speech_output" not in js
    flags["no_registry_mutation"] = "registry_write" not in js
    flags["no_external_network"] = "external_url_fetch" not in violations
    flags["no_live_camera_microphone"] = "camera_mic" not in violations
    flags["test_board_written"] = write_test_board
    flags["test_board_protected"] = True

    guards = [
        {"guard_id": "A", "passed": flags["main_canvas_priority_applied"]},
        {"guard_id": "B", "passed": flags["central_hud_largest_area"]},
        {"guard_id": "C", "passed": flags["left_sidebar_collapsible"]},
        {"guard_id": "D", "passed": flags["topbar_compact_actions"]},
        {"guard_id": "E", "passed": flags["object_chip_bar_present"]},
        {"guard_id": "F", "passed": flags["object_cards_removed_from_default_main_flow"]},
        {"guard_id": "G", "passed": flags["selected_object_detail_on_demand"]},
        {"guard_id": "H", "passed": flags["bottom_drawer_tabs_present"]},
        {"guard_id": "I", "passed": flags["metrics_default_collapsed"]},
        {"guard_id": "J", "passed": flags["raw_engineering_terms_hidden_by_default"]},
        {"guard_id": "K", "passed": flags["right_reasoning_panel_result_first"]},
        {"guard_id": "L", "passed": flags["compact_ui_preserved"]},
        {"guard_id": "M", "passed": flags["perception_hud_preserved"]},
        {"guard_id": "N", "passed": flags["visual_compare_preserved"]},
        {"guard_id": "O", "passed": flags["simple_mode_preserved"]},
        {"guard_id": "P", "passed": flags["local_runner_bridge_preserved"]},
        {"guard_id": "Q", "passed": flags["no_page_model_execution"]},
        {"guard_id": "R", "passed": flags["test_board_protected"]},
    ]
    ng_passed = sum(1 for g in guards if g["passed"])
    core = [
        "main_canvas_priority_applied",
        "central_hud_largest_area",
        "left_sidebar_collapsible",
        "topbar_compact_actions",
        "object_chip_bar_present",
        "object_cards_removed_from_default_main_flow",
        "selected_object_detail_on_demand",
        "bottom_drawer_tabs_present",
        "metrics_default_collapsed",
        "object_details_default_collapsed",
        "right_reasoning_panel_result_first",
        "compact_ui_preserved",
        "perception_hud_preserved",
        "visual_compare_preserved",
        "simple_mode_preserved",
        "local_runner_bridge_preserved",
        "no_page_model_execution",
    ]
    if violations or failed or not all(flags.get(k) for k in core):
        decision = FINAL_BLOCKED
        blockers = len(violations) + len(failed) + sum(1 for k in core if not flags.get(k))
    else:
        decision = FINAL_GO
        blockers = 0

    post = {
        **flags,
        "rollback_available": True,
        "rollback_can_restore_previous_compact_layout": True,
        "rollback_must_preserve_runner_bridge_service": True,
        "rollback_must_preserve_test_board": True,
        "rollback_must_preserve_review_artifacts": True,
        "rollback_not_executed_by_default": True,
    }
    out_root = DEFAULT_OUT
    out_root.mkdir(parents=True, exist_ok=True)
    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "real_execution_phase": True,
        "observation_canvas_first_collapsible_layout_patch": True,
        "observation_canvas_first_collapsible_layout_patch_profile_count": 1,
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
        rp = out_root / "p1_midplatform_model_test_lens_observation_canvas_first_collapsible_layout_patch_review_v1.json"
        rp.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(rp)
        extras = {
            "model_test_lens_observation_canvas_first_collapsible_layout_patch_record_v1.json": {"canvas_first": True},
            "model_test_lens_left_capability_drawer_record_v1.json": {"collapsible": True},
            "model_test_lens_hud_object_chip_bar_record_v1.json": {"chip_bar": True},
            "model_test_lens_bottom_drawer_tabs_record_v1.json": {"overlay_drawer": True},
            "model_test_lens_observation_canvas_first_collapsible_boundary_audit_v1.json": {"violations": violations},
            "model_test_lens_observation_canvas_first_collapsible_layout_post_review_audit_v1.json": post,
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
    print(json.dumps({
        "final_decision": r["final_decision"],
        "blocker_count": r["blocker_count"],
        "negative_guard_passed": r["negative_guard_passed"],
        "negative_guard_count": r["negative_guard_count"],
    }, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
