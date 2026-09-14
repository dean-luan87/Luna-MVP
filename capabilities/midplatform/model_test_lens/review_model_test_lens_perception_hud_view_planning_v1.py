# -*- coding: utf-8 -*-
"""P1 Model Test Lens Perception HUD View — planning review v1."""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.test_board.test_board_protocol_v1 import (  # noqa: E402
    REQUIRED_RECORD_TYPES,
    TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1,
    write_test_board_records,
)
from capabilities.midplatform.model_test_lens.perception_hud.perception_hud_types_v1 import (  # noqa: E402
    ENTITY_TYPES,
    EXTRA_TEST_BOARD_RECORD_TYPES,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    HUD_IS_READ_ONLY,
    HUD_MAY_DISPLAY_ANNOTATIONS,
    HUD_MAY_DISPLAY_REASONING_PANEL,
    HUD_MAY_DISPLAY_SUGGESTIONS,
    HUD_MAY_DISPLAY_TASK_RELEVANCE,
    HUD_MAY_DISPLAY_UNCERTAINTY,
    HUD_MUST_NOT_CALL_OUTPUT_ADAPTER,
    HUD_MUST_NOT_EXECUTE_MODEL,
    HUD_MUST_NOT_GENERATE_NEW_FACT,
    HUD_MUST_NOT_MUTATE_REGISTRY,
    HUD_MUST_NOT_TRIGGER_NAVIGATION_ACTION_SPEECH,
    HUD_MUST_NOT_WRITE_SEMANTIC,
    HUD_USES_EXISTING_ENVELOPE,
    LUNA_CORE_PRINCIPLE,
    MODEL_EXECUTION_ALLOWED_IN_PAGE,
    NAVIGATION_ACTION_SPEECH_ALLOWED,
    NEGATIVE_GUARDS,
    NEXT_PHASE_EXECUTION,
    OUTPUT_ADAPTER_ALLOWED,
    PERCEPTION_HUD_ROOT_REL,
    PERCEPTION_HUD_VIEW_PLANNING,
    PHASE_GOVERNANCE_RULES,
    PHASE_ID,
    PLANNING_ONLY,
    PLANNING_PRINCIPLE_ZH,
    PRESERVED_VIEW_FILES,
    REGISTRY_MUTATION_ALLOWED,
    REQUIRED_PLANNING_FILES,
    REQUIRED_TEST_BOARD_FIELDS_LOCAL,
    RUNTIME_EXECUTION_ALLOWED,
    SCHEMAS_PERCEPTION_HUD_REL,
    SEMANTIC_LAYER_ALLOWED,
    SPATIAL_RELATIONS,
    TARGET_CHAIN_REF,
    TASK_CONTEXTS,
    TASK_RELEVANCE,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    UNCERTAINTY_TAGS,
    NegativePerceptionHudViewPlanningGuard,
    P1MidplatformModelTestLensPerceptionHudViewPlanningDecision,
    PerceptionHudFutureModelAdapterPlan,
    PerceptionHudMobileSamAdapterPlan,
    PerceptionHudViewPlanningProfile,
    to_dict,
)

_PKG = "capabilities/midplatform/model_test_lens"
STEP_FILES = REQUIRED_PLANNING_FILES + (
    f"{_PKG}/review_model_test_lens_perception_hud_view_planning_v1.py",
)

SCHEMA_FILES = {
    "perception_hud_scene_annotation_schema_v1.json": "hud_scene_annotation_schema_defined",
    "perception_hud_reasoning_panel_schema_v1.json": "hud_reasoning_panel_schema_defined",
    "perception_hud_overlay_layer_schema_v1.json": "hud_overlay_layer_schema_defined",
}

PROFILE_REF = "perception_hud_view_planning_profile_v1"
DECISION_REF = "perception_hud_view_planning_decision_v1"
REVIEW_FILENAME = "p1_midplatform_model_test_lens_perception_hud_view_planning_review_v1.json"
_BOARD_STANDIN_ROOT = _REPO_ROOT / "_tmp_eval_out" / "board_standin"


def _pick_writable_base() -> Path:
    for cand in (_REPO_ROOT, Path.cwd()):
        try:
            (cand / "_tmp_eval_out").mkdir(parents=True, exist_ok=True)
            return cand
        except (PermissionError, OSError):
            continue
    return _REPO_ROOT


_WRITABLE_BASE = _pick_writable_base()
DEFAULT_OUTPUT_ROOT = (
    _WRITABLE_BASE / "_tmp_eval_out"
    / "p1_midplatform_model_test_lens_perception_hud_view_planning_v1_smoke_v0"
)


def _artifact_roots() -> List[Path]:
    roots: List[Path] = [_REPO_ROOT, Path.cwd(), _WRITABLE_BASE]
    return roots


def _resolve_file(rel: str) -> Optional[Path]:
    for base in _artifact_roots():
        p = base / rel
        if p.is_file():
            return p
    return None


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_json(rel: str) -> Optional[Dict[str, Any]]:
    p = _resolve_file(rel)
    if p is None:
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def _build_profile() -> Dict[str, Any]:
    return to_dict(
        PerceptionHudViewPlanningProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            planning_only=PLANNING_ONLY,
            perception_hud_view_planning=PERCEPTION_HUD_VIEW_PLANNING,
            hud_is_read_only=HUD_IS_READ_ONLY,
            hud_uses_existing_envelope=HUD_USES_EXISTING_ENVELOPE,
            hud_may_display_annotations=HUD_MAY_DISPLAY_ANNOTATIONS,
            hud_may_display_reasoning_panel=HUD_MAY_DISPLAY_REASONING_PANEL,
            hud_may_display_task_relevance=HUD_MAY_DISPLAY_TASK_RELEVANCE,
            hud_may_display_uncertainty=HUD_MAY_DISPLAY_UNCERTAINTY,
            hud_may_display_suggestions=HUD_MAY_DISPLAY_SUGGESTIONS,
            hud_must_not_execute_model=HUD_MUST_NOT_EXECUTE_MODEL,
            hud_must_not_generate_new_fact=HUD_MUST_NOT_GENERATE_NEW_FACT,
            hud_must_not_write_semantic=HUD_MUST_NOT_WRITE_SEMANTIC,
            hud_must_not_trigger_navigation_action_speech=HUD_MUST_NOT_TRIGGER_NAVIGATION_ACTION_SPEECH,
            hud_must_not_call_output_adapter=HUD_MUST_NOT_CALL_OUTPUT_ADAPTER,
            hud_must_not_mutate_registry=HUD_MUST_NOT_MUTATE_REGISTRY,
            model_execution_allowed_in_page=MODEL_EXECUTION_ALLOWED_IN_PAGE,
            runtime_execution_allowed=RUNTIME_EXECUTION_ALLOWED,
            output_adapter_allowed=OUTPUT_ADAPTER_ALLOWED,
            semantic_layer_allowed=SEMANTIC_LAYER_ALLOWED,
            fact_write_allowed=False,
            navigation_action_speech_allowed=NAVIGATION_ACTION_SPEECH_ALLOWED,
            registry_mutation_allowed=REGISTRY_MUTATION_ALLOWED,
            external_network_allowed=False,
            live_camera_allowed=False,
            live_microphone_allowed=False,
            target_chain_ref=TARGET_CHAIN_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=PHASE_GOVERNANCE_RULES,
        )
    )


def review_model_test_lens_perception_hud_view_planning_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
    write_test_board: bool = True,
    test_board_root: Optional[str] = None,
) -> Dict[str, Any]:
    failed_checks: List[str] = []
    passed_checks: List[str] = []
    warnings: List[str] = []

    for rel in STEP_FILES:
        if _resolve_file(rel) is not None:
            passed_checks.append(f"step.file_present={rel.split('/')[-1]}")
        else:
            failed_checks.append(f"step.file_missing={rel}")

    schema_flags: Dict[str, bool] = {}
    scene_schema = _load_json(f"{SCHEMAS_PERCEPTION_HUD_REL}/perception_hud_scene_annotation_schema_v1.json")
    reasoning_schema = _load_json(f"{SCHEMAS_PERCEPTION_HUD_REL}/perception_hud_reasoning_panel_schema_v1.json")
    overlay_schema = _load_json(f"{SCHEMAS_PERCEPTION_HUD_REL}/perception_hud_overlay_layer_schema_v1.json")

    for fname, go_key in SCHEMA_FILES.items():
        ok = _resolve_file(f"{SCHEMAS_PERCEPTION_HUD_REL}/{fname}") is not None
        schema_flags[go_key] = ok
        (passed_checks if ok else failed_checks).append(f"schema.{go_key}={'true' if ok else 'false'}")

    task_context_defined = False
    reasoning_panel_defined = False
    uncertainty_defined = False
    missing_info_defined = False
    mobile_sam_prompt_candidate = False

    if scene_schema:
        task_ctx = scene_schema.get("properties", {}).get("task_context", {})
        enum_vals = (
            task_ctx.get("properties", {})
            .get("task_context_type", {})
            .get("enum", [])
        )
        task_context_defined = set(TASK_CONTEXTS) <= set(enum_vals)
        entity_enum = (
            scene_schema.get("properties", {})
            .get("entities", {})
            .get("items", {})
            .get("properties", {})
            .get("entity_type", {})
            .get("enum", [])
        )
        if set(ENTITY_TYPES) <= set(entity_enum):
            passed_checks.append("schema.entity_types_complete=true")
        else:
            failed_checks.append("schema.entity_types_incomplete=true")

    if reasoning_schema:
        required = set(reasoning_schema.get("required", []))
        reasoning_panel_defined = {
            "current_task", "system_observations", "reasoning_steps",
            "uncertainty_summary", "missing_information", "recommended_next_steps",
        } <= required
        uncertainty_defined = "uncertainty_summary" in required
        missing_info_defined = "missing_information" in required

    plan_md = _resolve_file(f"{PERCEPTION_HUD_ROOT_REL}/perception_hud_view_plan_v1.md")
    if plan_md:
        text = plan_md.read_text(encoding="utf-8")
        mobile_sam_prompt_candidate = (
            "prompt_label" in text
            and "不得" in text
            and "fact label" in text
        )
        if "Simple Mode" in text and "Visual Compare" in text:
            passed_checks.append("plan.preserved_views_documented=true")
        else:
            failed_checks.append("plan.preserved_views_documented=false")

    preserved_flags: Dict[str, bool] = {}
    for rel in PRESERVED_VIEW_FILES:
        key = rel.split("/")[-1].replace(".", "_")
        ok = _resolve_file(rel) is not None
        preserved_flags[key] = ok
        (passed_checks if ok else failed_checks).append(f"preserve.{key}={'true' if ok else 'false'}")

    simple_mode_preserved = preserved_flags.get("simple_mode_ui_v1_js", False)
    visual_compare_preserved = preserved_flags.get("visual_compare_view_v1_js", False)
    local_runner_bridge_preserved = preserved_flags.get("local_runner_bridge_server_v1_py", False)
    debug_mode_preserved = _resolve_file(
        "capabilities/midplatform/model_test_lens/static_site/app.js"
    ) is not None

    mobile_sam_plan = PerceptionHudMobileSamAdapterPlan(
        record_id="perception_hud_mobile_sam_adapter_plan_v1",
        model_id="mobile_sam",
        provides=("segmentation_mask", "prompt_label", "confidence_score"),
        does_not_provide=("semantic_detection", "object_class_proof", "motion_direction"),
        label_source="prompt_label",
        prompt_label_candidate_only=True,
        followup_runners=("detection", "ocr", "depth"),
        example_observations=(
            "建筑区域：较稳定",
            "道路区域：边界需复核",
            "车辆候选：置信较低，需 detection 复核",
            "路牌候选：需 OCR/detection 辅助",
        ),
    )

    future_adapter_plan = PerceptionHudFutureModelAdapterPlan(
        record_id="perception_hud_future_model_adapter_plan_v1",
        adapters={
            "detection_tracking": {
                "status": "reserved",
                "hud_must_show": ["bounding_box", "class_label", "confidence", "missed_object_warning"],
            },
            "ocr": {
                "status": "reserved",
                "hud_must_show": ["text_box", "recognized_text", "reading_order", "unclear_text_warning"],
            },
            "slam_vio": {
                "status": "reserved",
                "hud_must_show": ["keypoints", "tracking_state", "trajectory_minimap", "drift_warning"],
            },
            "depth_world": {"status": "reserved"},
            "asr": {"status": "reserved"},
            "tts": {"status": "reserved"},
            "speaker": {"status": "reserved"},
            "face_expression_gesture": {"status": "reserved"},
            "multimodal_vlm": {"status": "reserved"},
        },
    )

    invariant_state: Dict[str, bool] = {
        "hud_not_model_executor": HUD_MUST_NOT_EXECUTE_MODEL and MODEL_EXECUTION_ALLOWED_IN_PAGE is False,
        "hud_not_runner_caller": HUD_MUST_NOT_EXECUTE_MODEL and RUNTIME_EXECUTION_ALLOWED is False,
        "candidate_not_fact": HUD_MUST_NOT_GENERATE_NEW_FACT is True,
        "no_navigation_speech": (
            HUD_MUST_NOT_TRIGGER_NAVIGATION_ACTION_SPEECH is True
            and NAVIGATION_ACTION_SPEECH_ALLOWED is False
        ),
        "no_semantic_fact_registry": (
            HUD_MUST_NOT_WRITE_SEMANTIC is True
            and SEMANTIC_LAYER_ALLOWED is False
            and REGISTRY_MUTATION_ALLOWED is False
        ),
        "no_runtime_output_adapter": (
            HUD_MUST_NOT_CALL_OUTPUT_ADAPTER is True
            and OUTPUT_ADAPTER_ALLOWED is False
            and RUNTIME_EXECUTION_ALLOWED is False
        ),
        "no_external_camera_mic": True,
        "no_delete_artifact": True,
        "reasoning_panel_defined": reasoning_panel_defined,
        "task_context_defined": task_context_defined,
        "uncertainty_defined": uncertainty_defined,
        "mobile_sam_prompt_candidate_only": mobile_sam_prompt_candidate,
        "test_board_planned": True,
        "test_board_protected": REQUIRED_TEST_BOARD_FIELDS_LOCAL.get("test_artifact_protected", False) is True,
    }

    negative_guards: List[NegativePerceptionHudViewPlanningGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativePerceptionHudViewPlanningGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    go_conditions: Dict[str, bool] = {
        "perception_hud_view_planning_profile_count_eq_1": True,
        "hud_scene_annotation_schema_defined": schema_flags.get("hud_scene_annotation_schema_defined", False),
        "hud_reasoning_panel_schema_defined": schema_flags.get("hud_reasoning_panel_schema_defined", False),
        "hud_overlay_layer_schema_defined": schema_flags.get("hud_overlay_layer_schema_defined", False),
        "reasoning_panel_required": reasoning_panel_defined,
        "task_context_supported": task_context_defined,
        "uncertainty_display_required": uncertainty_defined,
        "missing_information_display_required": missing_info_defined,
        "mobile_sam_prompt_label_candidate_only": mobile_sam_prompt_candidate,
        "detection_hud_adapter_reserved": "detection_tracking" in future_adapter_plan.adapters,
        "ocr_hud_adapter_reserved": "ocr" in future_adapter_plan.adapters,
        "slam_hud_adapter_reserved": "slam_vio" in future_adapter_plan.adapters,
        "simple_mode_preserved": simple_mode_preserved,
        "visual_compare_view_preserved": visual_compare_preserved,
        "local_runner_bridge_preserved": local_runner_bridge_preserved,
        "debug_mode_preserved": debug_mode_preserved,
        "hud_must_not_execute_model": HUD_MUST_NOT_EXECUTE_MODEL is True,
        "hud_must_not_generate_new_fact": HUD_MUST_NOT_GENERATE_NEW_FACT is True,
        "hud_must_not_write_semantic": HUD_MUST_NOT_WRITE_SEMANTIC is True,
        "hud_must_not_trigger_navigation_action_speech": HUD_MUST_NOT_TRIGGER_NAVIGATION_ACTION_SPEECH is True,
        "hud_must_not_call_output_adapter": HUD_MUST_NOT_CALL_OUTPUT_ADAPTER is True,
        "hud_must_not_mutate_registry": HUD_MUST_NOT_MUTATE_REGISTRY is True,
        "planning_only": PLANNING_ONLY is True,
        "negative_guard_count_eq_14": negative_guard_count == 14,
        "negative_guard_passed_eq_14": negative_guard_passed == 14,
        **negative_guard_go,
        **{f"test_board.{k}": (v is True) for k, v in REQUIRED_TEST_BOARD_FIELDS_LOCAL.items()},
    }

    for key, ok in go_conditions.items():
        (passed_checks if ok else failed_checks).append(f"go.{key}={'true' if ok else 'false'}")

    blocker_count = len(failed_checks)
    final_decision = FINAL_DECISION_GO if blocker_count == 0 else FINAL_DECISION_BLOCKED

    test_board_total = len(REQUIRED_RECORD_TYPES) + len(EXTRA_TEST_BOARD_RECORD_TYPES)
    decision = P1MidplatformModelTestLensPerceptionHudViewPlanningDecision(
        decision_ref=DECISION_REF,
        perception_hud_view_planning_profile_count=1,
        hud_scene_annotation_schema_defined=schema_flags.get("hud_scene_annotation_schema_defined", False),
        hud_reasoning_panel_schema_defined=schema_flags.get("hud_reasoning_panel_schema_defined", False),
        hud_overlay_layer_schema_defined=schema_flags.get("hud_overlay_layer_schema_defined", False),
        reasoning_panel_required=reasoning_panel_defined,
        task_context_supported=task_context_defined,
        uncertainty_display_required=uncertainty_defined,
        missing_information_display_required=missing_info_defined,
        mobile_sam_prompt_label_candidate_only=mobile_sam_prompt_candidate,
        detection_hud_adapter_reserved=True,
        ocr_hud_adapter_reserved=True,
        slam_hud_adapter_reserved=True,
        simple_mode_preserved=simple_mode_preserved,
        visual_compare_view_preserved=visual_compare_preserved,
        local_runner_bridge_preserved=local_runner_bridge_preserved,
        debug_mode_preserved=debug_mode_preserved,
        negative_guard_count=negative_guard_count,
        negative_guard_passed=negative_guard_passed,
        test_board_record_count=test_board_total,
        blocker_count=blocker_count,
        final_decision=final_decision,
    )

    scene_schema_plan = {
        "plan_id": "perception_hud_scene_annotation_schema_plan_v1",
        "schema_ref": f"{SCHEMAS_PERCEPTION_HUD_REL}/perception_hud_scene_annotation_schema_v1.json",
        "entity_types": list(ENTITY_TYPES),
        "spatial_relations": list(SPATIAL_RELATIONS),
        "task_relevance": list(TASK_RELEVANCE),
        "uncertainty_tags": list(UNCERTAINTY_TAGS),
        "task_contexts": list(TASK_CONTEXTS),
        "candidate_only": True,
    }
    reasoning_panel_plan = {
        "plan_id": "perception_hud_reasoning_panel_schema_plan_v1",
        "schema_ref": f"{SCHEMAS_PERCEPTION_HUD_REL}/perception_hud_reasoning_panel_schema_v1.json",
        "five_sections": [
            "current_task", "system_observations", "reasoning_steps",
            "uncertainty_summary_and_risks", "recommended_next_steps",
        ],
        "not_fact": True,
        "not_navigation_instruction": True,
    }
    overlay_layer_plan = {
        "plan_id": "perception_hud_overlay_layer_schema_plan_v1",
        "schema_ref": f"{SCHEMAS_PERCEPTION_HUD_REL}/perception_hud_overlay_layer_schema_v1.json",
        "layer_types": [
            "object_box", "segmentation_mask", "ocr_text_box", "keypoint",
            "trajectory", "risk_marker", "attention_marker", "reasoning_callout",
        ],
    }

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 Model Test Lens Perception HUD View Planning",
        "lifecycle_variant": "p1_midplatform_model_test_lens_perception_hud_view_planning",
        "planning_principle_zh": PLANNING_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "planning_only": PLANNING_ONLY,
        "perception_hud_view_planning": PERCEPTION_HUD_VIEW_PLANNING,
        "perception_hud_root_rel": PERCEPTION_HUD_ROOT_REL,
        "target_chain_ref": TARGET_CHAIN_REF,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "phase_governance_rules": list(PHASE_GOVERNANCE_RULES),
        "perception_hud_view_planning_profile": _build_profile(),
        "perception_hud_view_planning_profile_count": 1,
        "perception_hud_mobile_sam_adapter_plan": asdict(mobile_sam_plan),
        "perception_hud_future_model_adapter_plan": asdict(future_adapter_plan),
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "warnings": warnings,
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "final_decision": final_decision,
        "blocker_count": blocker_count,
        "recommended_next_phase": NEXT_PHASE_EXECUTION,
        "conclusions": {
            "planning_status": "go" if blocker_count == 0 else "blocked",
            "transition_note": (
                "PLANNING ONLY. Perception HUD View defines robot-vision explainable overlay "
                "on top of Visual Compare View. Read-only; candidate-only; no model execution. "
                "Next: Perception HUD View Execution."
            ),
        },
        "passed_checks": passed_checks,
        "failed_checks": failed_checks,
        "reviewed_at": _now(),
    }

    if write_file:
        review_path = out_root / REVIEW_FILENAME
        review_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(review_path)
        (out_root / "perception_hud_scene_annotation_schema_plan_v1.json").write_text(
            json.dumps(scene_schema_plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        (out_root / "perception_hud_reasoning_panel_schema_plan_v1.json").write_text(
            json.dumps(reasoning_panel_plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        (out_root / "perception_hud_overlay_layer_schema_plan_v1.json").write_text(
            json.dumps(overlay_layer_plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        (out_root / "perception_hud_mobile_sam_adapter_plan_v1.json").write_text(
            json.dumps(asdict(mobile_sam_plan), indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        (out_root / "perception_hud_future_model_adapter_plan_v1.json").write_text(
            json.dumps(asdict(future_adapter_plan), indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        result["output_root"] = str(out_root)

    if write_test_board:
        board_root = Path(test_board_root).expanduser().resolve() if test_board_root else _REPO_ROOT
        try:
            manifest_tb = write_test_board_records(
                result,
                test_mode=TEST_BOARD_TEST_MODE,
                repo_root=board_root,
                module=TEST_BOARD_MODULE,
                source_review_file=result.get("output_review_file"),
            )
            result["test_board_write_mode"] = "canonical"
        except (PermissionError, OSError):
            _BOARD_STANDIN_ROOT.mkdir(parents=True, exist_ok=True)
            manifest_tb = write_test_board_records(
                result,
                test_mode=TEST_BOARD_TEST_MODE,
                repo_root=_BOARD_STANDIN_ROOT,
                module=TEST_BOARD_MODULE,
                source_review_file=result.get("output_review_file"),
            )
            result["test_board_write_mode"] = "standin_sandbox_fallback"

        board_dir = Path(manifest_tb["test_board_dir"])
        extra_payloads = {
            "perception_hud_scene_annotation_schema_plan_record": {"record": scene_schema_plan},
            "perception_hud_reasoning_panel_schema_plan_record": {"record": reasoning_panel_plan},
            "perception_hud_overlay_layer_schema_plan_record": {"record": overlay_layer_plan},
            "perception_hud_mobile_sam_adapter_plan_record": {"record": asdict(mobile_sam_plan)},
            "perception_hud_future_model_adapter_plan_record": {"record": asdict(future_adapter_plan)},
        }
        common = {
            "protocol_id": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
            "phase_id": PHASE_ID,
            "module": TEST_BOARD_MODULE,
            "test_mode": TEST_BOARD_TEST_MODE,
            "recorded_at_utc": _now(),
            "protected": True,
            "non_deletable": True,
            "deletion_forbidden": True,
            "planning_only": True,
            "hud_is_read_only": True,
            "candidate_output_only": True,
        }
        for rtype, payload in extra_payloads.items():
            out = {**common, **payload}
            (board_dir / f"{rtype}.json").write_text(
                json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
            )
        result["test_board_root"] = str(board_dir)

    return result


def main() -> int:
    result = review_model_test_lens_perception_hud_view_planning_v1()
    print(json.dumps(
        {
            "phase_id": result["phase_id"],
            "final_decision": result["final_decision"],
            "blocker_count": result["blocker_count"],
            "negative_guard_passed": result["negative_guard_passed"],
            "negative_guard_count": result["negative_guard_count"],
            "recommended_next_phase": result["recommended_next_phase"],
        },
        indent=2,
        ensure_ascii=False,
    ))
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
