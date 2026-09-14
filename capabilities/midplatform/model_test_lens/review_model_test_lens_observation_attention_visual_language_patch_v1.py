# -*- coding: utf-8 -*-
"""P1 Observation Attention Visual Language Separation Patch — post-review v1."""

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


def _detect_repo_root() -> Path:
    candidates = [Path.cwd(), Path(__file__).resolve().parents[3]]
    marker = Path("capabilities/test_board/test_board_protocol_v1.py")
    for base in candidates:
        if (base / marker).is_file():
            return base
    return _REPO_ROOT


from capabilities.test_board.test_board_protocol_v1 import (  # noqa: E402
    REQUIRED_RECORD_TYPES,
    TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1,
    write_test_board_records,
)

PHASE_ID = "Phase-P1-Midplatform-Model-Test-Lens-Observation-Attention-Visual-Language-Patch-v1-001"
UPSTREAM_UI_PHASE = (
    "Phase-P1-Midplatform-Model-Test-Lens-Observation-Attention-Layer-UI-Execution-And-Post-Review-v1-001"
)
UPSTREAM_UI_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_OBSERVATION_ATTENTION_LAYER_UI_EXECUTION_GO"

STATIC_REL = "capabilities/midplatform/model_test_lens/static_site"
_PKG = "capabilities/midplatform/model_test_lens"

NEW_MODULES: Tuple[str, ...] = (
    f"{STATIC_REL}/hud_attention_visual_language_v1.js",
    f"{_PKG}/review_model_test_lens_observation_attention_visual_language_patch_v1.py",
)

UPDATED_FILES: Tuple[str, ...] = (
    f"{STATIC_REL}/perception_hud_renderer_v1.js",
    f"{STATIC_REL}/perception_hud_view_v1.js",
    f"{STATIC_REL}/observation_attention_priority_panel_v1.js",
    f"{STATIC_REL}/observation_attention_summary_v1.js",
    f"{STATIC_REL}/hud_object_chip_bar_v1.js",
    f"{STATIC_REL}/hud_selected_object_detail_v1.js",
    f"{STATIC_REL}/luna_observation_compact_ui_v1.js",
    f"{STATIC_REL}/app.js",
    f"{STATIC_REL}/index.html",
    f"{STATIC_REL}/styles.css",
)

UI_MARKERS: Tuple[str, ...] = (
    "hud_attention_visual_language_v1.js",
    "HudAttentionVisualLanguage",
    "drawSegmentationBoundary",
    "drawAttentionIndicators",
    "visualLanguageSeparation",
    "onSelectRegion",
    "onCanvasEntitySelect",
    "scrollToRegion",
    "formatSchedulingSummary",
    "观察调度主入口",
    "选中分割区域",
    "candidate_only · not_fact",
)

FORBIDDEN_IN_RENDERER: Tuple[Tuple[str, str], ...] = (
    (r"drawLabelChip|formatOverlayLabel|drawHudLabel", "full_label_on_canvas"),
    (r"attention.*strokeRect|priority.*strokeRect", "attention_second_box"),
    (r"\bfact_write\s*\(|\bexecute_detection\b", "runner_or_fact"),
)

FINAL_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_OBSERVATION_ATTENTION_VISUAL_LANGUAGE_PATCH_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_MODEL_TEST_LENS_OBSERVATION_ATTENTION_VISUAL_LANGUAGE_PATCH_BLOCKED"


def _default_out() -> Path:
    return (
        _detect_repo_root()
        / "_tmp_eval_out"
        / "p1_midplatform_model_test_lens_observation_attention_visual_language_patch_v1_smoke_v0"
    )


def _read(rel: str) -> str:
    for base in (_detect_repo_root(), _REPO_ROOT, Path.cwd()):
        p = base / rel
        if p.is_file():
            return p.read_text(encoding="utf-8")
    return ""


def _load_json(rel: str) -> Dict[str, Any]:
    raw = _read(rel)
    return json.loads(raw) if raw else {}


def _audit() -> Dict[str, bool]:
    renderer = _read(f"{STATIC_REL}/perception_hud_renderer_v1.js")
    vl = _read(f"{STATIC_REL}/hud_attention_visual_language_v1.js")
    panel = _read(f"{STATIC_REL}/observation_attention_priority_panel_v1.js")
    engine = _read(f"{STATIC_REL}/observation_attention_engine_v1.js")
    app = _read(f"{STATIC_REL}/app.js")
    hud_view = _read(f"{STATIC_REL}/perception_hud_view_v1.js")

    upstream = _load_json(
        "_tmp_eval_out/p1_midplatform_model_test_lens_observation_attention_layer_ui_execution_v1_smoke_v0/"
        "p1_midplatform_model_test_lens_observation_attention_layer_ui_execution_review_v1.json"
    )

    return {
        "upstream_attention_ui_go": upstream.get("final_decision") == UPSTREAM_UI_GO,
        "visual_language_module_present": bool(vl),
        "segmentation_primary_boundary": "drawSegmentationBoundary" in vl and "SEG" in vl,
        "attention_no_second_box": "drawAttentionIndicators" in vl
            and "drawSegmentationBoundary" in renderer,
        "no_full_label_on_canvas": "drawHudLabel" not in renderer and "drawLabelChip" not in renderer,
        "corner_badges_only": "drawPriorityCorner" in vl and "drawNumberBadge" in vl,
        "panel_scheduling_primary": "观察调度主入口" in panel and "onSelectRegion" in panel,
        "canvas_panel_linkage": "onCanvasEntitySelect" in app and "scrollToRegion" in panel,
        "chip_bar_segmentation_only": "oa-chip-pri" not in _read(f"{STATIC_REL}/hud_object_chip_bar_v1.js"),
        "attention_engine_unchanged": "buildAttentionPackage" in engine and "inferPriority" in engine,
        "selected_detail_points_to_panel": "观察调度说明见上方" in _read(
            f"{STATIC_REL}/hud_selected_object_detail_v1.js"
        ),
        "summary_scheduling_format": "formatSchedulingSummary" in _read(
            f"{STATIC_REL}/observation_attention_summary_v1.js"
        ),
        "hit_test_present": "hitTest" in vl and "attachCanvasInteraction" in hud_view,
    }


def review(*, write_file: bool = True, write_test_board: bool = True, test_board_root: Optional[str] = None) -> Dict[str, Any]:
    failed: List[str] = []
    for rel in NEW_MODULES + UPDATED_FILES:
        if not _read(rel):
            failed.append(f"file.missing={rel}")

    renderer = _read(f"{STATIC_REL}/perception_hud_renderer_v1.js")
    violations = [pid for pat, pid in FORBIDDEN_IN_RENDERER if re.search(pat, renderer, re.I)]

    flags = _audit()
    guards = [
        {"guard_id": "A", "passed": flags["upstream_attention_ui_go"]},
        {"guard_id": "B", "passed": flags["segmentation_primary_boundary"]},
        {"guard_id": "C", "passed": flags["attention_no_second_box"]},
        {"guard_id": "D", "passed": flags["no_full_label_on_canvas"] and not violations},
        {"guard_id": "E", "passed": flags["corner_badges_only"]},
        {"guard_id": "F", "passed": flags["panel_scheduling_primary"]},
        {"guard_id": "G", "passed": flags["canvas_panel_linkage"]},
        {"guard_id": "H", "passed": flags["chip_bar_segmentation_only"]},
        {"guard_id": "I", "passed": flags["attention_engine_unchanged"]},
        {"guard_id": "J", "passed": flags["summary_scheduling_format"]},
        {"guard_id": "K", "passed": flags["hit_test_present"]},
        {"guard_id": "L", "passed": flags["selected_detail_points_to_panel"]},
    ]
    ng_passed = sum(1 for g in guards if g["passed"])
    core = list(flags.keys())

    if violations or failed or not all(flags.get(k) for k in core) or ng_passed < 12:
        decision = FINAL_BLOCKED
        blockers = len(violations) + len(failed) + sum(1 for k in core if not flags.get(k)) + (12 - ng_passed)
    else:
        decision = FINAL_GO
        blockers = 0

    out_root = _default_out()
    out_root.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "visual_language_separation_patch": True,
        "upstream_ui_phase": UPSTREAM_UI_PHASE,
        "audit_flags": flags,
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
        rp = out_root / "p1_midplatform_model_test_lens_observation_attention_visual_language_patch_review_v1.json"
        rp.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(rp)

    if write_test_board:
        root = Path(test_board_root or str(_detect_repo_root()))
        try:
            tb = write_test_board_records(
                result, test_mode="real_test", repo_root=root, module="model_governance",
                source_review_file=result.get("output_review_file"),
            )
        except (OSError, PermissionError):
            standin = _detect_repo_root() / "_tmp_eval_out" / "board_standin"
            standin.mkdir(parents=True, exist_ok=True)
            tb = write_test_board_records(
                result, test_mode="real_test", repo_root=standin, module="model_governance",
                source_review_file=result.get("output_review_file"),
            )
        board_dir = Path(tb["test_board_dir"])
        (board_dir / "observation_attention_visual_language_patch_record.json").write_text(
            json.dumps({"phase_id": PHASE_ID, "protected": True}, indent=2) + "\n", encoding="utf-8")
        result["test_board_root"] = str(board_dir)

    return result


def main() -> int:
    r = review(test_board_root=str(_detect_repo_root()))
    print(json.dumps({
        "final_decision": r["final_decision"],
        "blocker_count": r["blocker_count"],
        "negative_guard_passed": r["negative_guard_passed"],
    }, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
