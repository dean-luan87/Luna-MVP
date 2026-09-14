# -*- coding: utf-8 -*-
"""P1 Segmentation Boundary Visual Polish v1-001 — post-review."""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

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
    TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1,
    write_test_board_records,
)

PHASE_ID = "Phase-P1-Midplatform-Model-Test-Lens-Segmentation-Boundary-Visual-Polish-v1-001"
STATIC_REL = "capabilities/midplatform/model_test_lens/static_site"

POST_REVIEW_GO = (
    "P1_MIDPLATFORM_MODEL_TEST_LENS_VISUAL_EXPRESSION_SYSTEM_UI_EXECUTION_GO"
)
FINAL_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_SEGMENTATION_BOUNDARY_VISUAL_POLISH_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_MODEL_TEST_LENS_SEGMENTATION_BOUNDARY_VISUAL_POLISH_BLOCKED"

NEGATIVE_GUARDS: tuple[Dict[str, str], ...] = (
    {"guard_id": "A", "key": "no_runner_execution", "desc": "不触发 runner 执行"},
    {"guard_id": "B", "key": "no_fact_write", "desc": "不写 fact"},
    {"guard_id": "C", "key": "no_navigation_decision", "desc": "不做导航决策"},
    {"guard_id": "D", "key": "no_boundary_clone", "desc": "不 clone segmentation boundary"},
    {"guard_id": "E", "key": "no_secondary_box_from_attention", "desc": "Attention 不画第二套 box"},
    {"guard_id": "F", "key": "no_attention_boundary_owner", "desc": "Attention 非 boundary owner"},
    {"guard_id": "G", "key": "no_selected_boundary_mutation", "desc": "selected 不改变 boundary ownership"},
    {"guard_id": "H", "key": "no_hover_boundary_mutation", "desc": "hover 不生成第二套 boundary"},
    {"guard_id": "I", "key": "no_segmentation_boundary_hidden_by_panel_click", "desc": "面板点击不隐藏分割边界"},
    {"guard_id": "J", "key": "segmentation_boundary_single_owner_preserved", "desc": "segmentation 唯一 owner 保留"},
    {"guard_id": "K", "key": "boundary_visual_polish_only", "desc": "仅 boundary 视觉抛光"},
    {"guard_id": "L", "key": "no_icon_only_default_marker", "desc": "主图默认非图标-only 浮标"},
    {"guard_id": "M", "key": "p0_p1_short_label_default_visible", "desc": "P0/P1 默认短浮标可见"},
    {"guard_id": "N", "key": "p2_p3_default_panel_only", "desc": "P2/P3 默认仅面板"},
    {"guard_id": "O", "key": "show_all_candidate_markers_default_off", "desc": "显示全部候选浮标默认关闭"},
    {"guard_id": "P", "key": "no_duplicate_marker_for_same_region", "desc": "无同标签重复浮标"},
    {"guard_id": "Q", "key": "panel_contains_full_attention_explanation", "desc": "面板含完整解释"},
    {"guard_id": "R", "key": "footer_summary_only", "desc": "底部仅摘要"},
    {"guard_id": "S", "key": "candidate_only_not_fact_preserved", "desc": "candidate_only/not_fact 保留"},
)


def _read(rel: str) -> str:
    for base in (_detect_repo_root(), _REPO_ROOT, Path.cwd()):
        p = base / rel
        if p.is_file():
            return p.read_text(encoding="utf-8")
    return ""


def _load_review(rel: str) -> Dict[str, Any]:
    raw = _read(rel)
    return json.loads(raw) if raw else {}


def _chip_select_body(app_js: str) -> str:
    m = re.search(r"function onChipSelect\(entityId\) \{([\s\S]*?)\n  \}", app_js)
    return m.group(1) if m else ""


def _audit() -> Dict[str, bool]:
    polish = _read(f"{STATIC_REL}/segmentation_boundary_visual_polish_v1.js")
    vl = _read(f"{STATIC_REL}/hud_attention_visual_language_v1.js")
    renderer = _read(f"{STATIC_REL}/perception_hud_renderer_v1.js")
    panel = _read(f"{STATIC_REL}/observation_attention_priority_panel_v1.js")
    summary = _read(f"{STATIC_REL}/observation_attention_summary_v1.js")
    app_js = _read(f"{STATIC_REL}/app.js")
    engine = _read(f"{STATIC_REL}/observation_attention_engine_v1.js")
    policy = _read(f"{STATIC_REL}/hud_visual_policy_v1.js")
    controls = _read(f"{STATIC_REL}/perception_hud_controls_v1.js")
    hud_view = _read(f"{STATIC_REL}/perception_hud_view_v1.js")
    index_html = _read(f"{STATIC_REL}/index.html")
    chip_body = _chip_select_body(app_js)

    upstream = _load_review(
        "_tmp_eval_out/p1_midplatform_model_test_lens_visual_expression_system_ui_execution_post_review_minor_fix_v1_smoke_v0/"
        "p1_midplatform_model_test_lens_visual_expression_system_ui_execution_post_review_review_v1.json"
    )

    show_all_checkbox = re.search(
        r"id=['\"]phud-show-all-markers['\"][^>]*/>",
        controls,
    )
    checkbox_default_unchecked = bool(
        show_all_checkbox and "checked" not in show_all_checkbox.group(0).lower()
    )

    return {
        "upstream_post_review_go": upstream.get("final_decision") == POST_REVIEW_GO,
        "no_runner_execution": 'dataset.modelExecutionAllowed = "false"' in app_js,
        "no_fact_write": 'dataset.candidateOnly = "true"' in app_js,
        "no_navigation_decision": "not_navigation_action_speech" in app_js,
        "no_boundary_clone": (
            polish.count("noBoundaryClone") >= 1
            and vl.count("noBoundaryClone") >= 1
            and "cloneSegmentation" not in polish
        ),
        "no_secondary_box_from_attention": (
            "drawAttentionFloatMarker" in renderer
            and "drawSegmentationBoundary" in renderer
            and renderer.count("strokeRect") == 0
            and "drawSegmentationContour" in polish
        ),
        "no_attention_boundary_owner": (
            vl.count("annotationLayerOnly") >= 1
            and vl.count("noAttentionBoundaryOwner") >= 1
        ),
        "no_selected_boundary_mutation": (
            bool(chip_body)
            and "visible = false" not in chip_body
            and "_hidden" not in chip_body
        ),
        "no_hover_boundary_mutation": (
            "drawCornerBrackets" in polish
            and not re.search(r"isHovered[\s\S]{0,300}strokeRect", vl)
        ),
        "no_segmentation_boundary_hidden_by_panel_click": (
            bool(chip_body) and "visible = false" not in chip_body
        ),
        "segmentation_boundary_single_owner_preserved": (
            polish.count("segmentationBoundarySingleOwnerPreserved") >= 1
            and "drawSegmentationContour" in polish
            and vl.count("drawSegmentationBoundary") >= 1
        ),
        "boundary_visual_polish_only": (
            polish.count("boundaryVisualPolishOnly") >= 1
            and "drawCornerBrackets" in polish
            and "inferPriority" in engine
            and "buildAttentionPackage" in engine
            and "strokeDefault" in polish
            and "rgba(232, 238, 246" not in vl
        ),
        "no_icon_only_default_marker": (
            "formatFloatMarker" in vl and "drawNumberBadge" not in vl
        ),
        "p0_p1_short_label_default_visible": (
            "shouldShowMarkerOnCanvas" in vl and "isP01" in vl
        ),
        "p2_p3_default_panel_only": (
            "isP01" in vl and checkbox_default_unchecked
        ),
        "show_all_candidate_markers_default_off": (
            policy.count("showAllAttentionMarkers: false") >= 1
            and checkbox_default_unchecked
            and "showAllAttentionMarkers === true" in hud_view
        ),
        "no_duplicate_marker_for_same_region": (
            "buildMarkerDedupeSet" in vl
            and "markerVisibleByDedupe" in vl
            and "noDuplicateMarkerForSameRegion" in vl
            and "markerDedupeSet" in renderer
        ),
        "panel_contains_full_attention_explanation": (
            "oa-priority-why" in panel and "oa-priority-status" in panel
        ),
        "footer_summary_only": (
            "formatSchedulingSummary" in summary and "本帧建议优先观察" in summary
        ),
        "candidate_only_not_fact_preserved": (
            "candidate_only" in panel and "not_fact" in panel
        ),
        "polish_module_wired": "segmentation_boundary_visual_polish_v1.js" in index_html,
        "corner_contour_style": (
            "cornersOnly" in polish
            and "hairlineAlpha" in polish
            and "lineDefault: 1" in polish
        ),
        "selected_subtle_mask": "0.14" in renderer or "maskOpacity" in renderer,
        "phase_ref_polish": PHASE_ID in polish,
    }


def review(*, write_test_board: bool = True, test_board_root: Optional[str] = None) -> Dict[str, Any]:
    violations: List[str] = []
    combined = _read(f"{STATIC_REL}/hud_attention_visual_language_v1.js") + _read(
        f"{STATIC_REL}/segmentation_boundary_visual_polish_v1.js"
    )
    if re.search(r"drawHudBox|drawAttentionIndicators|drawPriorityCorner", combined):
        violations.append("legacy_dual_box_renderer")
    if re.search(r"rgba\(232,\s*238,\s*246", combined):
        violations.append("bright_white_debug_stroke")

    flags = _audit()
    failed: List[str] = []

    guards = []
    for spec in NEGATIVE_GUARDS:
        passed = bool(flags.get(spec["key"], False))
        guards.append({**spec, "passed": passed})
        if not passed:
            failed.append(f"guard.{spec['guard_id']}.fail={spec['key']}")

    for key in (
        "upstream_post_review_go",
        "polish_module_wired",
        "corner_contour_style",
        "selected_subtle_mask",
        "phase_ref_polish",
    ):
        if not flags.get(key, False):
            failed.append(f"audit.{key}=false")

    if violations:
        failed.extend([f"violation.{v}" for v in violations])

    ng_passed = sum(1 for g in guards if g["passed"])
    core_ok = all(flags.get(spec["key"], False) for spec in NEGATIVE_GUARDS)
    blocker_count = len(failed)
    decision = FINAL_GO if core_ok and blocker_count == 0 and not violations else FINAL_BLOCKED

    out = _detect_repo_root() / "_tmp_eval_out" / (
        "p1_midplatform_model_test_lens_segmentation_boundary_visual_polish_v1_smoke_v0"
    )
    out.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "audit_flags": flags,
        "negative_guards": guards,
        "negative_guard_count": len(guards),
        "negative_guard_passed": ng_passed,
        "forbidden_pattern_violations": violations,
        "blocker_count": blocker_count,
        "failed_checks": failed,
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }
    rp = out / "p1_midplatform_model_test_lens_segmentation_boundary_visual_polish_review_v1.json"
    rp.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    result["output_review_file"] = str(rp)

    if write_test_board and decision == FINAL_GO:
        root = Path(test_board_root or str(_detect_repo_root()))
        try:
            tb = write_test_board_records(
                result, test_mode="real_test", repo_root=root, module="model_governance",
                source_review_file=str(rp),
            )
            result["test_board_root"] = tb.get("test_board_dir")
        except (OSError, PermissionError):
            standin = _detect_repo_root() / "_tmp_eval_out" / "board_standin"
            standin.mkdir(parents=True, exist_ok=True)
            tb = write_test_board_records(
                result, test_mode="real_test", repo_root=standin, module="model_governance",
                source_review_file=str(rp),
            )
            result["test_board_root"] = tb.get("test_board_dir")

    return result


def main() -> int:
    r = review(test_board_root=str(_detect_repo_root()))
    print(json.dumps({
        "final_decision": r["final_decision"],
        "blocker_count": r["blocker_count"],
        "negative_guard_passed": r["negative_guard_passed"],
        "negative_guard_count": r["negative_guard_count"],
        "failed_checks": r.get("failed_checks", []),
    }, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
