# -*- coding: utf-8
"""P1 Dual Route Perception Validation — execution post-review v1."""

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
    for base in (Path.cwd(), Path(__file__).resolve().parents[3]):
        if (base / "capabilities/test_board/test_board_protocol_v1.py").is_file():
            return base
    return _REPO_ROOT


from capabilities.test_board.test_board_protocol_v1 import (  # noqa: E402
    TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1,
    write_test_board_records,
)

PHASE_ID = "Phase-P1-Midplatform-Dual-Route-Perception-Validation-Execution-v1-001"
MM_REL = "capabilities/midplatform/model_test_lens/multi_model_interaction"
SCHEMA_REL = "capabilities/midplatform/model_test_lens/schemas/multi_model_interaction"
STATIC_REL = "capabilities/midplatform/model_test_lens/static_site"
_PKG = "capabilities/midplatform/model_test_lens"
RUNNER_REL = "capabilities/midplatform/model_test_lens/local_runner_bridge/runners"

UPSTREAM_DUAL_ROUTE_PLANNING_GO = "P1_MIDPLATFORM_DUAL_ROUTE_PERCEPTION_VALIDATION_PLANNING_GO"
UPSTREAM_SCENE_AWARE_EXEC_GO = "P1_MIDPLATFORM_SCENE_AWARE_SEGMENTATION_PROMPT_POLICY_EXECUTION_GO"
UPSTREAM_MOBILESAM_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_MOBILESAM_SINGLE_MODEL_EXECUTION_INTEGRATION_GO"
UPSTREAM_OCR_UI_GO = (
    "P1_MIDPLATFORM_MULTI_MODEL_INTERACTION_MOBILE_SAM_OCR_CONTROLLED_EXECUTION_UI_EXECUTION_GO"
)

FINAL_GO = "P1_MIDPLATFORM_DUAL_ROUTE_PERCEPTION_VALIDATION_EXECUTION_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_DUAL_ROUTE_PERCEPTION_VALIDATION_EXECUTION_BLOCKED"

NEW_MODULES: Tuple[str, ...] = (
    f"{MM_REL}/dual_route_perception_execution_types_v1.py",
    f"{MM_REL}/dual_route_perception_route_a_v1.py",
    f"{MM_REL}/dual_route_perception_route_b_v1.py",
    f"{MM_REL}/dual_route_comparison_processor_v1.py",
    f"{MM_REL}/dual_route_perception_validation_execution_smoke_v1.py",
    f"{_PKG}/run_dual_route_perception_validation_execution_smoke_v1.py",
    f"{_PKG}/review_model_test_lens_dual_route_perception_validation_execution_v1.py",
    f"{STATIC_REL}/dual_route_perception_copy_v1.js",
    f"{STATIC_REL}/dual_route_perception_state_v1.js",
    f"{STATIC_REL}/dual_route_perception_panel_v1.js",
    f"{STATIC_REL}/dual_route_perception_summary_v1.js",
)

UPDATED_FILES: Tuple[str, ...] = (
    f"{STATIC_REL}/app.js",
    f"{STATIC_REL}/index.html",
    f"{STATIC_REL}/luna_observation_compact_ui_v1.js",
    f"{STATIC_REL}/styles.css",
)

FORBIDDEN_UI: Tuple[Tuple[str, str], ...] = (
    (r"开始 OCR|立即识别|已识别文字|这是路牌|确认这是", "forbidden_fact_copy"),
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "A", "key": "no_slam_text_detection", "desc": "SLAM 不找文字"},
    {"guard_id": "B", "key": "no_slam_text_recognition", "desc": "SLAM 不识别文字"},
    {"guard_id": "C", "key": "no_slam_ocr_route_direct_generation", "desc": "SLAM 不直出 OCR route"},
    {"guard_id": "D", "key": "no_fact_write", "desc": "不写 fact"},
    {"guard_id": "E", "key": "no_navigation_decision", "desc": "不做导航决策"},
    {"guard_id": "F", "key": "no_ocr_execution", "desc": "不执行 OCR"},
    {"guard_id": "G", "key": "no_detection_execution", "desc": "不执行 Detection"},
    {"guard_id": "H", "key": "no_vlm_execution", "desc": "不执行 VLM"},
    {"guard_id": "I", "key": "no_grounding_real_model_call", "desc": "不调用真实 Grounding"},
    {"guard_id": "J", "key": "no_vlm_real_model_call", "desc": "不调用真实 VLM"},
    {"guard_id": "K", "key": "no_vlm_fact_generation", "desc": "VLM 不写 fact"},
    {"guard_id": "L", "key": "no_grounding_label_fact_upgrade", "desc": "Grounding label 不升级 fact"},
    {"guard_id": "M", "key": "no_sam_mask_fact_upgrade", "desc": "SAM mask 不升级 fact"},
    {"guard_id": "N", "key": "no_prompt_label_fact_upgrade", "desc": "prompt 不升级 fact"},
    {"guard_id": "O", "key": "route_a_candidate_only", "desc": "Route A candidate only"},
    {"guard_id": "P", "key": "route_b_candidate_only", "desc": "Route B candidate only"},
    {"guard_id": "Q", "key": "dual_route_comparison_not_fact", "desc": "comparison 非 fact"},
    {"guard_id": "R", "key": "dual_route_conflict_not_auto_fact", "desc": "conflict 不自动 fact"},
    {"guard_id": "S", "key": "route_a_miss_route_b_hit_requires_manual_review", "desc": "A 漏 B 命中须复核"},
    {"guard_id": "T", "key": "conflict_blocks_auto_admission", "desc": "冲突 block admission"},
    {"guard_id": "U", "key": "no_mobile_sam_direct_to_ocr", "desc": "SAM 不直连 OCR"},
    {"guard_id": "V", "key": "no_bypass_midplatform", "desc": "不绕过中台"},
    {"guard_id": "W", "key": "no_visual_expression_mutation", "desc": "不改 boundary owner"},
    {"guard_id": "X", "key": "no_boundary_clone", "desc": "不 clone boundary"},
    {"guard_id": "Y", "key": "human_correction_not_ground_truth", "desc": "纠错非 ground truth"},
    {"guard_id": "Z", "key": "browser_runtime_guard_inherited", "desc": "继承 browser guard"},
    {"guard_id": "AA", "key": "smoke_cases_pass", "desc": "smoke 通过"},
    {"guard_id": "AB", "key": "upstream_dual_route_planning_go", "desc": "上游 Dual Route Planning GO"},
    {"guard_id": "AC", "key": "upstream_scene_aware_execution_go", "desc": "上游 Scene-Aware Execution GO"},
    {"guard_id": "AD", "key": "upstream_mobilesam_go", "desc": "上游 MobileSAM GO"},
    {"guard_id": "AE", "key": "upstream_ocr_ui_go", "desc": "上游 OCR UI GO"},
)


def _read(rel: str) -> str:
    for base in (_detect_repo_root(), _REPO_ROOT, Path.cwd()):
        p = base / rel
        if p.is_file():
            return p.read_text(encoding="utf-8")
    return ""


def _load_json(rel: str) -> Dict[str, Any]:
    raw = _read(rel)
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {}


def _audit() -> Dict[str, bool]:
    route_a = _read(f"{MM_REL}/dual_route_perception_route_a_v1.py")
    route_b = _read(f"{MM_REL}/dual_route_perception_route_b_v1.py")
    processor = _read(f"{MM_REL}/dual_route_comparison_processor_v1.py")
    panel = _read(f"{STATIC_REL}/dual_route_perception_panel_v1.js")
    state = _read(f"{STATIC_REL}/dual_route_perception_state_v1.js")
    copy = _read(f"{STATIC_REL}/dual_route_perception_copy_v1.js")
    app = _read(f"{STATIC_REL}/app.js")
    compact = _read(f"{STATIC_REL}/luna_observation_compact_ui_v1.js")
    runner = _read(f"{RUNNER_REL}/mobilesam_image_runner_v1.py")
    browser = _read(f"{STATIC_REL}/browser_runtime_guard_v1.js")
    no_slam = _load_json(f"{SCHEMA_REL}/no_slam_for_text_policy_v1.json")
    prompt_display = _read(f"{STATIC_REL}/prompt_label_display_policy_v1.js")

    planning = _load_json(
        "_tmp_eval_out/p1_midplatform_dual_route_perception_validation_planning_v1_smoke_v0/"
        "p1_midplatform_dual_route_perception_validation_planning_review_v1.json"
    )
    scene_aware = _load_json(
        "_tmp_eval_out/p1_midplatform_scene_aware_segmentation_prompt_policy_execution_v1_smoke_v0/"
        "p1_midplatform_scene_aware_segmentation_prompt_policy_execution_review_v1.json"
    )
    mobilesam = _load_json(
        "_tmp_eval_out/p1_midplatform_model_test_lens_mobilesam_single_model_execution_integration_v1_002_smoke_v0/"
        "p1_midplatform_model_test_lens_mobilesam_single_model_execution_integration_v1_002_review.json"
    )
    ocr_ui = _load_json(
        "_tmp_eval_out/p1_midplatform_mobile_sam_ocr_controlled_execution_ui_execution_v1_smoke_v0/"
        "p1_midplatform_mobile_sam_ocr_controlled_execution_ui_execution_review_v1.json"
    )

    smoke_result: Dict[str, Any] = {}
    try:
        from capabilities.midplatform.model_test_lens.multi_model_interaction.dual_route_perception_validation_execution_smoke_v1 import (  # noqa: WPS433
            run_smoke_cases,
        )
        smoke_result = run_smoke_cases()
    except Exception:
        smoke_result = {"final_decision": FINAL_BLOCKED}

    ui_forbidden_ok = all(
        not re.search(pat, text, re.I)
        for pat, _ in FORBIDDEN_UI
        for text in (copy, app, compact)
        if text
    )

    return {
        "no_slam_text_detection": no_slam.get("boundary_flags", {}).get("no_slam_text_detection") is True,
        "no_slam_text_recognition": no_slam.get("boundary_flags", {}).get("no_slam_text_recognition") is True,
        "no_slam_ocr_route_direct_generation": "ocr_route_direct_generation" in json.dumps(no_slam)
            and "no_slam_ocr_route_direct_generation" in state,
        "no_fact_write": "no_fact_write" in processor and "no_fact_write" in panel,
        "no_navigation_decision": "must_not_trigger_navigation" not in processor
            and "no_navigation_decision" in processor,
        "no_ocr_execution": "no_ocr_execution" in panel and "ocr_runner" not in route_a,
        "no_detection_execution": "detection_runner" not in route_a and "no_detection_execution" in panel,
        "no_vlm_execution": "no_vlm_execution" in panel and "vlm_runner" not in route_b,
        "no_grounding_real_model_call": "no_grounding_real_model_call" in route_a
            and "planning_stub_v1" in route_a,
        "no_vlm_real_model_call": "no_vlm_real_model_call" in route_b,
        "no_vlm_fact_generation": "vlm_output_not_fact" in route_b and "no_vlm_fact_generation" in copy,
        "no_grounding_label_fact_upgrade": "detected_label_not_fact" in route_a,
        "no_sam_mask_fact_upgrade": "sam_mask_not_semantic_fact" in route_a,
        "no_prompt_label_fact_upgrade": "no_prompt_label_fact_upgrade" in prompt_display,
        "route_a_candidate_only": "route_a_candidate_only" in route_a,
        "route_b_candidate_only": "route_b_candidate_only" in route_b,
        "dual_route_comparison_not_fact": "dual_route_comparison_not_fact" in processor,
        "dual_route_conflict_not_auto_fact": "dual_route_conflict_not_auto_fact" in processor,
        "route_a_miss_route_b_hit_requires_manual_review": "manual_review" in processor
            and "route_a_miss_route_b_only" in processor,
        "conflict_blocks_auto_admission": "block_auto_admission" in processor,
        "no_mobile_sam_direct_to_ocr": "mask_ref_direct_ocr" not in processor
            and "direct_ocr" not in route_a.lower(),
        "no_bypass_midplatform": "midplatform_dual_route_comparison" in processor,
        "no_visual_expression_mutation": "segmentationSoleBoundaryOwner" in panel,
        "no_boundary_clone": "no_boundary_clone" in panel,
        "human_correction_not_ground_truth": "ground_truth" not in panel.lower()
            or "not_ground_truth" in _read(f"{STATIC_REL}/human_correction_copy_v1.js"),
        "browser_runtime_guard_inherited": "BrowserRuntimeGuard" in browser,
        "smoke_cases_pass": smoke_result.get("final_decision", "").endswith("_GO"),
        "upstream_dual_route_planning_go": planning.get("final_decision") == UPSTREAM_DUAL_ROUTE_PLANNING_GO,
        "upstream_scene_aware_execution_go": scene_aware.get("final_decision") == UPSTREAM_SCENE_AWARE_EXEC_GO,
        "upstream_mobilesam_go": mobilesam.get("final_decision") == UPSTREAM_MOBILESAM_GO,
        "upstream_ocr_ui_go": ocr_ui.get("final_decision") == UPSTREAM_OCR_UI_GO,
        "_ui_forbidden_ok": ui_forbidden_ok,
    }


def review(
    *,
    write_file: bool = True,
    write_test_board: bool = True,
    test_board_root: Optional[str] = None,
) -> Dict[str, Any]:
    failed: List[str] = []
    for rel in NEW_MODULES + UPDATED_FILES:
        if not _read(rel):
            failed.append(f"file.missing={rel}")

    flags = _audit()
    if not flags.pop("_ui_forbidden_ok", True):
        failed.append("ui.forbidden_copy_detected")

    guards = []
    for spec in NEGATIVE_GUARDS:
        passed = bool(flags.get(spec["key"], False))
        guards.append({**spec, "passed": passed})
        if not passed:
            failed.append(f"guard.{spec['guard_id']}.fail={spec['key']}")

    ng_passed = sum(1 for g in guards if g["passed"])
    blocker_count = len(failed)
    decision = FINAL_GO if blocker_count == 0 else FINAL_BLOCKED

    out = _detect_repo_root() / "_tmp_eval_out" / (
        "p1_midplatform_dual_route_perception_validation_execution_v1_smoke_v0"
    )
    out.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "execution_only": True,
        "no_model_call": True,
        "audit_flags": flags,
        "negative_guards": guards,
        "negative_guard_count": len(guards),
        "negative_guard_passed": ng_passed,
        "blocker_count": blocker_count,
        "failed_checks": failed,
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "test_board_dir": (
            "capabilities/test_board/model_governance/"
            "phase_p1_midplatform_dual_route_perception_validation_execution_v1_001"
        ),
    }

    if write_file:
        rp = out / "p1_midplatform_dual_route_perception_validation_execution_review_v1.json"
        rp.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(rp)

    if write_test_board and decision == FINAL_GO:
        root = Path(test_board_root or str(_detect_repo_root()))
        try:
            tb = write_test_board_records(
                result, test_mode="post_review", repo_root=root, module="model_governance",
                source_review_file=result.get("output_review_file"),
            )
        except (OSError, PermissionError):
            standin = _detect_repo_root() / "_tmp_eval_out" / "board_standin"
            standin.mkdir(parents=True, exist_ok=True)
            tb = write_test_board_records(
                result, test_mode="post_review", repo_root=standin, module="model_governance",
                source_review_file=result.get("output_review_file"),
            )
        result["test_board_root"] = str(tb.get("test_board_dir", ""))

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
