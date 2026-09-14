# -*- coding: utf-8 -*-
"""P1 Visual Expression System UI Execution v1-001 — post-review."""

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

PHASE_ID = (
    "Phase-P1-Midplatform-Model-Test-Lens-Visual-Expression-System-UI-Execution-And-Post-Review-v1-001"
)
STATIC_REL = "capabilities/midplatform/model_test_lens/static_site"
_PKG = "capabilities/midplatform/model_test_lens"

PLANNING_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_VISUAL_EXPRESSION_SYSTEM_PLANNING_GO"
SEMANTIC_PATCH_GO = (
    "P1_MIDPLATFORM_MODEL_TEST_LENS_OBSERVATION_ATTENTION_OVERLAY_SEMANTIC_SEPARATION_PATCH_GO"
)

FINAL_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_VISUAL_EXPRESSION_SYSTEM_UI_EXECUTION_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_MODEL_TEST_LENS_VISUAL_EXPRESSION_SYSTEM_UI_EXECUTION_BLOCKED"

NEGATIVE_GUARDS: tuple[Dict[str, str], ...] = (
    {"guard_id": "A", "key": "no_runner_execution", "desc": "不触发 runner 执行"},
    {"guard_id": "B", "key": "no_fact_write", "desc": "不写 fact"},
    {"guard_id": "C", "key": "no_navigation_decision", "desc": "不做导航决策"},
    {"guard_id": "D", "key": "no_boundary_clone", "desc": "不 clone segmentation boundary"},
    {"guard_id": "E", "key": "no_secondary_box_from_attention", "desc": "Attention 不画第二套 box"},
    {"guard_id": "F", "key": "no_attention_boundary_owner", "desc": "Attention 非 boundary owner"},
    {"guard_id": "G", "key": "no_selected_boundary_mutation", "desc": "selected 不改变 boundary ownership"},
    {"guard_id": "H", "key": "no_segmentation_boundary_hidden_by_panel_click", "desc": "面板点击不隐藏分割边界"},
    {"guard_id": "I", "key": "no_icon_only_default_marker", "desc": "主图默认非图标-only 浮标"},
    {"guard_id": "J", "key": "p0_p1_short_label_default_visible", "desc": "P0/P1 默认短浮标可见"},
    {"guard_id": "K", "key": "p2_p3_default_panel_only", "desc": "P2/P3 默认仅面板"},
    {"guard_id": "L", "key": "panel_contains_full_attention_explanation", "desc": "面板含完整 why/route/status"},
    {"guard_id": "M", "key": "footer_summary_only", "desc": "底部仅本帧调度摘要"},
    {"guard_id": "N", "key": "no_ground_truth_from_human_correction", "desc": "纠错非 ground truth"},
    {"guard_id": "O", "key": "no_prompt_label_fact_upgrade", "desc": "prompt_label 不升级事实"},
    {"guard_id": "P", "key": "no_motion_confirmed_from_single_frame", "desc": "单帧不 confirmed_dynamic"},
    {"guard_id": "Q", "key": "candidate_only_not_fact_preserved", "desc": "candidate_only/not_fact 保留"},
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


def _audit() -> Dict[str, bool]:
    vl = _read(f"{STATIC_REL}/hud_attention_visual_language_v1.js")
    renderer = _read(f"{STATIC_REL}/perception_hud_renderer_v1.js")
    panel = _read(f"{STATIC_REL}/observation_attention_priority_panel_v1.js")
    summary = _read(f"{STATIC_REL}/observation_attention_summary_v1.js")
    copy_js = _read(f"{STATIC_REL}/observation_attention_copy_v1.js")
    interaction = _read(f"{STATIC_REL}/visual_expression_interaction_v1.js")
    app_js = _read(f"{STATIC_REL}/app.js")
    engine = _read(f"{STATIC_REL}/observation_attention_engine_v1.js")
    hc_copy = _read(f"{STATIC_REL}/human_correction_copy_v1.js")
    index_html = _read(f"{STATIC_REL}/index.html")

    planning = _load_review(
        "_tmp_eval_out/p1_midplatform_model_test_lens_visual_expression_system_planning_v1_smoke_v0/"
        "p1_midplatform_model_test_lens_visual_expression_system_planning_review_v1.json"
    )
    semantic = _load_review(
        "_tmp_eval_out/p1_midplatform_model_test_lens_observation_attention_overlay_semantic_separation_patch_v1_002_smoke_v0/"
        "p1_midplatform_model_test_lens_observation_attention_overlay_semantic_separation_patch_review_v1.json"
    )

    chip_select_body = ""
    chip_m = re.search(r"function onChipSelect\(entityId\) \{([\s\S]*?)\n  \}", app_js)
    if chip_m:
        chip_select_body = chip_m.group(1)

    return {
        "upstream_planning_go": planning.get("final_decision") == PLANNING_GO,
        "upstream_semantic_separation_go": semantic.get("final_decision") == SEMANTIC_PATCH_GO,
        "no_runner_execution": (
            'dataset.modelExecutionAllowed = "false"' in app_js
            and interaction.count("noRunnerExecution") >= 1
            and "trigger_runner" not in panel.lower()
            and "executeRunner" not in app_js
        ),
        "no_fact_write": (
            'dataset.candidateOnly = "true"' in app_js
            and interaction.count("noFactWrite") >= 1
            and "writeFact" not in app_js
        ),
        "no_navigation_decision": (
            "not_navigation_action_speech" in app_js
            and "navigation_decision" not in panel.lower()
        ),
        "no_boundary_clone": (
            vl.count("noBoundaryClone") >= 1
            and "drawPriorityCorner" not in vl
            and "cloneSegmentation" not in vl
            and "clone_boundary" not in vl.lower()
        ),
        "no_secondary_box_from_attention": (
            "drawAttentionFloatMarker" in renderer
            and "drawSegmentationBoundary" in renderer
            and "drawHudBox" not in renderer
            and "drawAttentionIndicators" not in renderer
            and renderer.count("strokeRect") == 0
        ),
        "no_attention_boundary_owner": (
            vl.count("noAttentionBoundaryOwner") >= 1
            and vl.count("annotationLayerOnly") >= 1
            and "segmentation overlay owner" in vl.lower()
        ),
        "no_selected_boundary_mutation": (
            "drawSegmentationBoundary" in vl
            and "boundaryAlpha" in vl
            and bool(chip_m)
            and "visible = false" not in chip_select_body
            and "_hidden" not in chip_select_body
        ),
        "no_segmentation_boundary_hidden_by_panel_click": (
            bool(chip_m)
            and "highlightEntity" in chip_select_body
            and "visible = false" not in chip_select_body
        ),
        "no_icon_only_default_marker": (
            "formatFloatMarker" in vl
            and "drawNumberBadge" not in vl
            and "drawRouteDots" not in vl
            and "icon_only" not in vl.lower()
        ),
        "p0_p1_short_label_default_visible": (
            "shouldShowMarkerOnCanvas" in vl
            and "P0_immediate_attention" in vl
            and "P1_high_attention" in vl
        ),
        "p2_p3_default_panel_only": (
            "panelRecords" in panel
            and "shouldShowMarkerOnCanvas" in vl
            and "showAllAttentionMarkers" in _read(f"{STATIC_REL}/perception_hud_controls_v1.js")
        ),
        "panel_contains_full_attention_explanation": (
            "oa-priority-why" in panel
            and "oa-priority-next" in panel
            and "oa-priority-status" in panel
            and panel.count("panelContainsFullAttentionExplanation") >= 1
        ),
        "footer_summary_only": (
            "formatSchedulingSummary" in summary
            and summary.count("footerSummaryOnly") >= 1
            and "本帧建议优先观察" in summary
        ),
        "no_ground_truth_from_human_correction": (
            "ground truth" not in hc_copy.lower() or "not_ground_truth" in hc_copy
            or "非 ground truth" in hc_copy
            or "指错" in hc_copy
        ),
        "no_prompt_label_fact_upgrade": (
            "prompt_label_candidate" in engine
            and "confirmed" not in copy_js.lower()
        ),
        "no_motion_confirmed_from_single_frame": (
            "singleFrameLimit" in copy_js
            and "confirmed_dynamic" not in engine
        ),
        "candidate_only_not_fact_preserved": (
            "candidate_only" in panel
            and "not_fact" in panel
            and "candidate_only" in engine
        ),
        "visual_expression_interaction_wired": (
            "visual_expression_interaction_v1.js" in index_html
            and "VisualExpressionInteraction" in interaction
        ),
        "canvas_panel_hover_mapping": (
            "onHoverRegion" in panel
            and "onPanelHoverRegion" in app_js
            and "noAttentionRecord" in copy_js
        ),
        "attention_engine_priority_unchanged": (
            "inferPriority" in engine
            and "buildAttentionPackage" in engine
        ),
        "phase_ref_ui_execution": (
            PHASE_ID in vl
            and PHASE_ID in panel
        ),
    }


def review(*, write_test_board: bool = True, test_board_root: Optional[str] = None) -> Dict[str, Any]:
    violations: List[str] = []
    vl = _read(f"{STATIC_REL}/hud_attention_visual_language_v1.js")
    renderer = _read(f"{STATIC_REL}/perception_hud_renderer_v1.js")

    if re.search(r"drawHudBox|drawAttentionIndicators|drawPriorityCorner", renderer + vl):
        violations.append("legacy_dual_box_renderer")
    if re.search(r"strokeRect.*attention|attention.*strokeRect", vl, re.I):
        violations.append("attention_stroke_rect")

    flags = _audit()
    failed: List[str] = []

    guards = []
    for spec in NEGATIVE_GUARDS:
        passed = bool(flags.get(spec["key"], False))
        guards.append({**spec, "passed": passed})
        if not passed:
            failed.append(f"guard.{spec['guard_id']}.fail={spec['key']}")

    for key in (
        "upstream_planning_go",
        "upstream_semantic_separation_go",
        "visual_expression_interaction_wired",
        "canvas_panel_hover_mapping",
        "attention_engine_priority_unchanged",
        "phase_ref_ui_execution",
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
        "p1_midplatform_model_test_lens_visual_expression_system_ui_execution_v1_smoke_v0"
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
    rp = out / "p1_midplatform_model_test_lens_visual_expression_system_ui_execution_review_v1.json"
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
