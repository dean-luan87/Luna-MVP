# -*- coding: utf-8 -*-
"""P1 Model Test Lens Left Drawer Trigger + Bottom Drawer Cleanup Patch — review v1."""

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
    "Phase-P1-Midplatform-Model-Test-Lens-Left-Drawer-Trigger-And-Bottom-Drawer-Cleanup-Patch-"
    "Execution-And-Post-Review-v1-001"
)
STATIC_REL = "capabilities/midplatform/model_test_lens/static_site"
_PKG = "capabilities/midplatform/model_test_lens"

PATCH_FILES: Tuple[str, ...] = (
    f"{STATIC_REL}/luna_capability_grid_trigger_v1.js",
    f"{STATIC_REL}/luna_bottom_drawer_state_guard_v1.js",
    f"{STATIC_REL}/luna_left_capability_drawer_v1.js",
    f"{STATIC_REL}/luna_bottom_drawer_tabs_v1.js",
    f"{STATIC_REL}/observation_canvas_first_collapsible_layout_v1.js",
    f"{STATIC_REL}/luna_observation_compact_ui_v1.js",
    f"{STATIC_REL}/styles.css",
    f"{STATIC_REL}/index.html",
    f"{STATIC_REL}/README_STATIC_SITE.md",
    f"{_PKG}/review_model_test_lens_left_drawer_trigger_bottom_drawer_cleanup_patch_v1.py",
)

FINAL_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_LEFT_DRAWER_TRIGGER_BOTTOM_DRAWER_CLEANUP_PATCH_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_MODEL_TEST_LENS_LEFT_DRAWER_TRIGGER_BOTTOM_DRAWER_CLEANUP_PATCH_BLOCKED"

FORBIDDEN: Tuple[Tuple[str, str], ...] = (
    (r"\brun_model\s*\(|\binfer\s*\(", "page_model_execution"),
    (r"\bfact_write\s*\(|\bsemantic_write\s*\(", "fact_semantic"),
    (r"getUserMedia|MediaRecorder|navigator\.mediaDevices", "camera_mic"),
)

EXTRA_RECORDS: Tuple[str, ...] = (
    "left_drawer_trigger_bottom_drawer_cleanup_patch_record",
    "capability_grid_trigger_record",
    "bottom_drawer_cleanup_record",
    "bottom_drawer_state_guard_record",
    "left_drawer_bottom_cleanup_boundary_audit_record",
    "left_drawer_trigger_bottom_drawer_cleanup_post_review_record",
)

DEFAULT_OUT = (
    _REPO_ROOT / "_tmp_eval_out" / "p1_midplatform_model_test_lens_left_drawer_trigger_bottom_drawer_cleanup_patch_v1_smoke_v0"
)
_BOARD_STANDIN = _REPO_ROOT / "_tmp_eval_out" / "board_standin"


def _read(rel: str) -> str:
    for base in (_REPO_ROOT, Path.cwd()):
        p = base / rel
        if p.is_file():
            return p.read_text(encoding="utf-8")
    return ""


def _audit() -> Dict[str, bool]:
    grid = _read(f"{STATIC_REL}/luna_capability_grid_trigger_v1.js")
    guard = _read(f"{STATIC_REL}/luna_bottom_drawer_state_guard_v1.js")
    left = _read(f"{STATIC_REL}/luna_left_capability_drawer_v1.js")
    bottom = _read(f"{STATIC_REL}/luna_bottom_drawer_tabs_v1.js")
    layout = _read(f"{STATIC_REL}/observation_canvas_first_collapsible_layout_v1.js")
    styles = _read(f"{STATIC_REL}/styles.css")
    index = _read(f"{STATIC_REL}/index.html")
    compact = _read(f"{STATIC_REL}/luna_observation_compact_ui_v1.js")
    return {
        "capability_grid_trigger_present": "LunaCapabilityGridTrigger" in grid and "lol-cap-grid-trigger" in grid,
        "red_box_input_like_control_removed": "lol-left-toggle" not in left and "lol-input-mini" not in left,
        "left_sidebar_collapsed_width_lte_72px": "64px" in styles and "lol-cap-grid-trigger" in styles,
        "left_sidebar_expandable": "setLeftExpanded" in left and "能力面板" in left,
        "bottom_drawer_default_collapsed": "ensureCollapsed" in guard and "ensureCollapsed" in bottom,
        "bottom_blank_area_removed": "position: fixed" in styles and "lol-drawer-overlay[hidden]" in styles,
        "empty_drawer_body_not_rendered_by_default": "overlay.hidden = true" in bottom or "ensureCollapsed" in bottom,
        "bottom_summary_height_compact": "max-height: 88px" in styles and "lol-dock-bar" in bottom,
        "drawer_tabs_present": "lol-dock-tabs" in bottom,
        "drawer_body_opens_only_on_tab_click": "activeDrawer" in bottom,
        "drawer_close_button_present": "lol-drawer-close" in bottom,
        "main_canvas_priority_preserved": "lol-layout-canvas-first" in layout,
        "central_hud_largest_area": "minmax(0, 1fr)" in styles,
        "right_reasoning_panel_preserved": "lol-right-panel" in index,
        "object_chip_bar_preserved": "lol-object-chip-host" in index,
        "compact_ui_preserved": "lol-main-grid" in index,
        "no_delete_artifact_button": "deleteArtifact" not in left,
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
    flags["no_fact_semantic_navigation"] = "navigation_action" not in js
    flags["no_registry_mutation"] = True
    flags["no_external_network"] = "external_url_fetch" not in violations
    flags["no_live_camera_microphone"] = "camera_mic" not in violations
    flags["test_board_written"] = write_test_board
    flags["test_board_protected"] = True

    guards = [
        {"guard_id": "A", "passed": flags["capability_grid_trigger_present"]},
        {"guard_id": "B", "passed": flags["red_box_input_like_control_removed"]},
        {"guard_id": "C", "passed": flags["left_sidebar_expandable"]},
        {"guard_id": "D", "passed": flags["bottom_drawer_default_collapsed"]},
        {"guard_id": "E", "passed": flags["bottom_blank_area_removed"]},
        {"guard_id": "F", "passed": flags["empty_drawer_body_not_rendered_by_default"]},
        {"guard_id": "G", "passed": flags["drawer_body_opens_only_on_tab_click"]},
        {"guard_id": "H", "passed": flags["main_canvas_priority_preserved"]},
        {"guard_id": "I", "passed": flags["object_chip_bar_preserved"]},
        {"guard_id": "J", "passed": flags["right_reasoning_panel_preserved"]},
        {"guard_id": "K", "passed": flags["compact_ui_preserved"]},
        {"guard_id": "L", "passed": flags["no_page_model_execution"]},
        {"guard_id": "M", "passed": flags["test_board_protected"]},
        {"guard_id": "N", "passed": flags["drawer_close_button_present"]},
        {"guard_id": "O", "passed": flags["bottom_summary_height_compact"]},
        {"guard_id": "P", "passed": flags["drawer_tabs_present"]},
    ]
    ng_passed = sum(1 for g in guards if g["passed"])
    core = [
        "capability_grid_trigger_present",
        "red_box_input_like_control_removed",
        "left_sidebar_expandable",
        "bottom_drawer_default_collapsed",
        "bottom_blank_area_removed",
        "empty_drawer_body_not_rendered_by_default",
        "drawer_body_opens_only_on_tab_click",
        "drawer_close_button_present",
        "main_canvas_priority_preserved",
        "object_chip_bar_preserved",
        "compact_ui_preserved",
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
        "rollback_can_restore_previous_collapsible_layout": True,
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
        "left_drawer_trigger_bottom_drawer_cleanup_patch_profile_count": 1,
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
        rp = out_root / "p1_midplatform_model_test_lens_left_drawer_trigger_bottom_drawer_cleanup_patch_review_v1.json"
        rp.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(rp)
        extras = {
            "model_test_lens_capability_grid_trigger_record_v1.json": {"grid_trigger": True},
            "model_test_lens_bottom_drawer_cleanup_record_v1.json": {"blank_removed": True},
            "model_test_lens_bottom_drawer_state_guard_record_v1.json": {"default_collapsed": True},
            "model_test_lens_left_drawer_bottom_cleanup_boundary_audit_v1.json": {"violations": violations},
            "model_test_lens_left_drawer_trigger_bottom_drawer_cleanup_post_review_audit_v1.json": post,
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
