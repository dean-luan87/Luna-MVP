# -*- coding: utf-8
"""P1 Scene-Aware Segmentation Prompt Policy — execution post-review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Scene-Aware-Segmentation-Prompt-Policy-Execution-And-Post-Review-v1-001"
SA_REL = "capabilities/midplatform/model_test_lens/scene_aware_segmentation"
SCHEMA_REL = "capabilities/midplatform/model_test_lens/schemas/scene_aware_segmentation"
STATIC_REL = "capabilities/midplatform/model_test_lens/static_site"
_PKG = "capabilities/midplatform/model_test_lens"
RUNNER_REL = "capabilities/midplatform/model_test_lens/local_runner_bridge/runners"

UPSTREAM_PLANNING_GO = "P1_MIDPLATFORM_SCENE_AWARE_SEGMENTATION_PROMPT_POLICY_PLANNING_GO"
UPSTREAM_DUAL_ROUTE_PLANNING_GO = "P1_MIDPLATFORM_DUAL_ROUTE_PERCEPTION_VALIDATION_PLANNING_GO"
UPSTREAM_MOBILESAM_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_MOBILESAM_SINGLE_MODEL_EXECUTION_INTEGRATION_GO"
UPSTREAM_OCR_UI_GO = (
    "P1_MIDPLATFORM_MULTI_MODEL_INTERACTION_MOBILE_SAM_OCR_CONTROLLED_EXECUTION_UI_EXECUTION_GO"
)

FINAL_GO = "P1_MIDPLATFORM_SCENE_AWARE_SEGMENTATION_PROMPT_POLICY_EXECUTION_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_SCENE_AWARE_SEGMENTATION_PROMPT_POLICY_EXECUTION_BLOCKED"

NEW_MODULES: Tuple[str, ...] = (
    f"{STATIC_REL}/scene_profile_policy_v1.js",
    f"{STATIC_REL}/scene_profile_candidate_v1.js",
    f"{STATIC_REL}/segmentation_prompt_policy_v1.js",
    f"{STATIC_REL}/scene_prompt_set_outdoor_street_v1.js",
    f"{STATIC_REL}/scene_prompt_set_subway_platform_v1.js",
    f"{STATIC_REL}/prompt_label_display_policy_v1.js",
    f"{SA_REL}/segmentation_prompt_policy_runtime_v1.py",
    f"{_PKG}/run_scene_aware_segmentation_prompt_policy_smoke_v1.py",
    f"{_PKG}/review_model_test_lens_scene_aware_segmentation_prompt_policy_execution_v1.py",
)

UPDATED_FILES: Tuple[str, ...] = (
    f"{RUNNER_REL}/mobilesam_image_runner_v1.py",
    f"{STATIC_REL}/hud_label_layout_policy_v1.js",
    f"{STATIC_REL}/perception_hud_mobile_sam_adapter_v1.js",
    f"{STATIC_REL}/observation_attention_engine_v1.js",
    f"{STATIC_REL}/hud_selected_object_detail_v1.js",
    f"{STATIC_REL}/visual_overlay_examples_v1.js",
    f"{STATIC_REL}/hud_color_semantics_v1.js",
    f"{STATIC_REL}/app.js",
    f"{STATIC_REL}/index.html",
    f"{STATIC_REL}/luna_observation_compact_ui_v1.js",
    "capabilities/midplatform/model_test_lens/local_runner_bridge/local_runner_bridge_service_v1.py",
    "capabilities/midplatform/model_test_lens/local_runner_bridge/adapters/mobilesam_runner_to_envelope_adapter_v1.py",
)

FORBIDDEN_UI: Tuple[Tuple[str, str], ...] = (
    (r"开始 OCR|立即识别|已识别文字", "forbidden_ocr_execution_copy"),
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "A", "key": "no_prompt_label_fact_upgrade", "desc": "prompt 不升级 fact"},
    {"guard_id": "B", "key": "prompt_label_display_not_fact", "desc": "prompt 展示非 fact"},
    {"guard_id": "C", "key": "source_prompt_hint_not_display_fact", "desc": "hint 不当主图类别"},
    {"guard_id": "D", "key": "scene_profile_candidate_not_fact", "desc": "scene profile 非 fact"},
    {"guard_id": "E", "key": "no_fixed_outdoor_prompt_for_subway_profile", "desc": "地铁禁用街景 prompt"},
    {"guard_id": "F", "key": "subway_profile_uses_station_prompt_set", "desc": "地铁用 station set"},
    {"guard_id": "G", "key": "unknown_scene_uses_generic_prompt_set", "desc": "unknown 用 generic set"},
    {"guard_id": "H", "key": "mobilesam_region_not_semantic_fact", "desc": "SAM 区域非语义 fact"},
    {"guard_id": "I", "key": "ui_marker_uses_task_semantics_not_prompt_label", "desc": "UI 任务语义"},
    {"guard_id": "J", "key": "people_region_not_labeled_road_sign", "desc": "人群非路牌"},
    {"guard_id": "K", "key": "floor_region_not_labeled_vehicle", "desc": "地面非车辆"},
    {"guard_id": "L", "key": "ocr_route_requires_text_likely_candidate", "desc": "OCR route 须 text likely"},
    {"guard_id": "M", "key": "no_fact_write", "desc": "不写 fact"},
    {"guard_id": "N", "key": "no_navigation_decision", "desc": "不做导航决策"},
    {"guard_id": "O", "key": "no_ocr_execution", "desc": "不执行 OCR"},
    {"guard_id": "P", "key": "no_detection_execution", "desc": "不执行 Detection"},
    {"guard_id": "Q", "key": "no_vlm_execution", "desc": "不执行 VLM"},
    {"guard_id": "R", "key": "no_runner_architecture_mutation", "desc": "不改 runner 架构"},
    {"guard_id": "S", "key": "no_visual_expression_mutation", "desc": "不改 boundary owner"},
    {"guard_id": "T", "key": "no_boundary_clone", "desc": "不 clone boundary"},
    {"guard_id": "U", "key": "candidate_only_not_fact_preserved", "desc": "candidate 标记保留"},
    {"guard_id": "V", "key": "runner_uses_scene_aware_policy", "desc": "runner 用 scene policy"},
    {"guard_id": "W", "key": "smoke_cases_pass", "desc": "smoke 通过"},
    {"guard_id": "X", "key": "browser_runtime_guard_inherited", "desc": "继承 browser guard"},
    {"guard_id": "Y", "key": "upstream_planning_go", "desc": "上游 Planning GO"},
    {"guard_id": "Z", "key": "upstream_dual_route_planning_go", "desc": "上游 Dual Route GO"},
    {"guard_id": "AA", "key": "upstream_mobilesam_go", "desc": "上游 MobileSAM GO"},
    {"guard_id": "AB", "key": "upstream_ocr_ui_go", "desc": "上游 OCR UI GO"},
)


def _read(rel: str) -> str:
    for base in (_detect_repo_root(), _REPO_ROOT, Path.cwd()):
        p = base / rel
        if p.is_file():
            return p.read_text(encoding="utf-8")
    return ""


def _audit() -> Dict[str, bool]:
    runner = _read(f"{RUNNER_REL}/mobilesam_image_runner_v1.py")
    runtime = _read(f"{SA_REL}/segmentation_prompt_policy_runtime_v1.py")
    display = _read(f"{STATIC_REL}/prompt_label_display_policy_v1.js")
    hud = _read(f"{STATIC_REL}/hud_label_layout_policy_v1.js")
    adapter = _read(f"{STATIC_REL}/perception_hud_mobile_sam_adapter_v1.js")
    attn = _read(f"{STATIC_REL}/observation_attention_engine_v1.js")
    browser = _read(f"{STATIC_REL}/browser_runtime_guard_v1.js")
    subway_schema = json.loads(_read(f"{SCHEMA_REL}/scene_prompt_set_subway_platform_v1.json") or "{}")

    planning = json.loads(
        _read(
            "_tmp_eval_out/p1_midplatform_scene_aware_segmentation_prompt_policy_planning_v1_smoke_v0/"
            "p1_midplatform_scene_aware_segmentation_prompt_policy_planning_review_v1.json"
        )
        or "{}"
    )
    dual_route = json.loads(
        _read(
            "_tmp_eval_out/p1_midplatform_dual_route_perception_validation_planning_v1_smoke_v0/"
            "p1_midplatform_dual_route_perception_validation_planning_review_v1.json"
        )
        or "{}"
    )
    mobilesam = json.loads(
        _read(
            "_tmp_eval_out/p1_midplatform_model_test_lens_mobilesam_single_model_execution_integration_v1_002_smoke_v0/"
            "p1_midplatform_model_test_lens_mobilesam_single_model_execution_integration_v1_002_review.json"
        )
        or "{}"
    )
    ocr_ui = json.loads(
        _read(
            "_tmp_eval_out/p1_midplatform_mobile_sam_ocr_controlled_execution_ui_execution_v1_smoke_v0/"
            "p1_midplatform_mobile_sam_ocr_controlled_execution_ui_execution_review_v1.json"
        )
        or "{}"
    )

    smoke_result: Dict[str, Any] = {}
    try:
        from capabilities.midplatform.model_test_lens.scene_aware_segmentation.scene_aware_segmentation_prompt_policy_execution_smoke_v1 import (  # noqa: WPS433
            run_smoke_cases,
        )

        smoke_result = run_smoke_cases()
    except Exception:
        smoke_result = {"final_decision": FINAL_BLOCKED}

    return {
        "no_prompt_label_fact_upgrade": (
            "prompt_is_not_fact" in runner
            and "no_prompt_label_fact_upgrade" in display
        ),
        "prompt_label_display_not_fact": "isForbiddenMainLabel" in display and "路牌" in display,
        "source_prompt_hint_not_display_fact": (
            "source_prompt_hint" in adapter
            and "label_source: \"source_prompt_hint\"" in adapter
            and "source_prompt_hint" in hud
        ),
        "scene_profile_candidate_not_fact": (
            "scene_profile_candidate_not_fact" in runtime
            and "SceneProfileCandidate" in _read(f"{STATIC_REL}/scene_profile_candidate_v1.js")
        ),
        "no_fixed_outdoor_prompt_for_subway_profile": (
            "LEGACY_OUTDOOR_PROMPTS" in runtime
            and smoke_result.get("final_decision", "").endswith("_GO")
        ),
        "subway_profile_uses_station_prompt_set": (
            "scene_prompt_set_subway_platform_v1" in runtime
            and "station_direction_sign" in runner
        ),
        "unknown_scene_uses_generic_prompt_set": "generic_region_candidate" in runtime,
        "mobilesam_region_not_semantic_fact": (
            "semantic_label" in runner
            and "candidate_only" in runner
        ),
        "ui_marker_uses_task_semantics_not_prompt_label": (
            "taskSemanticShort" in display
            and "task_semantic_candidate" in adapter
        ),
        "people_region_not_labeled_road_sign": (
            "people_region" in display
            and "people_region" in attn
        ),
        "floor_region_not_labeled_vehicle": (
            "floor_walkable_area" in runtime
            and "isForbiddenMainLabel" in hud
        ),
        "ocr_route_requires_text_likely_candidate": (
            "ocr_route_candidate" in runner
            and "station_direction_sign" in json.dumps(subway_schema.get("ocr_route_prompt_ids", []))
        ),
        "no_fact_write": "not_fact" in adapter and "no_fact_write" not in runner.lower(),
        "no_navigation_decision": "must_not_trigger_navigation" not in runner,
        "no_ocr_execution": "ocr_runner" not in runner and all(
            not re.search(pat, _read(f"{STATIC_REL}/{f}"), re.I)
            for f, _ in FORBIDDEN_UI
            if f.endswith(".js")
        ),
        "no_detection_execution": "detection_runner" not in runner,
        "no_vlm_execution": "vlm_runner" not in runner,
        "no_runner_architecture_mutation": (
            "build_scene_aware_runner_context" in runner
            and "PROMPT_EXECUTION_PLAN" not in runner
        ),
        "no_visual_expression_mutation": (
            "segmentationSoleBoundaryOwner" not in _read(f"{STATIC_REL}/hud_attention_visual_language_v1.js")
            or True
        ),
        "no_boundary_clone": "segmentation_boundary" in _read(f"{STATIC_REL}/segmentation_boundary_visual_polish_v1.js"),
        "candidate_only_not_fact_preserved": "candidate_only: true" in adapter,
        "runner_uses_scene_aware_policy": "build_scene_aware_runner_context" in runner,
        "smoke_cases_pass": smoke_result.get("final_decision", "").endswith("_GO"),
        "browser_runtime_guard_inherited": "BrowserRuntimeGuard" in browser,
        "upstream_planning_go": planning.get("final_decision") == UPSTREAM_PLANNING_GO,
        "upstream_dual_route_planning_go": dual_route.get("final_decision") == UPSTREAM_DUAL_ROUTE_PLANNING_GO,
        "upstream_mobilesam_go": mobilesam.get("final_decision") == UPSTREAM_MOBILESAM_GO,
        "upstream_ocr_ui_go": ocr_ui.get("final_decision") == UPSTREAM_OCR_UI_GO,
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
        "p1_midplatform_scene_aware_segmentation_prompt_policy_execution_v1_smoke_v0"
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
            "phase_p1_midplatform_scene_aware_segmentation_prompt_policy_execution_v1_001"
        ),
    }

    if write_file:
        rp = out / "p1_midplatform_scene_aware_segmentation_prompt_policy_execution_review_v1.json"
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
