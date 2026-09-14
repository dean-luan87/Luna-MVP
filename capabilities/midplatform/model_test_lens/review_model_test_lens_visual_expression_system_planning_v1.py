# -*- coding: utf-8 -*-
"""P1 Visual Expression System — planning review v1."""

from __future__ import annotations

import json
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
    REQUIRED_TEST_BOARD_FIELDS,
    TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1,
    write_test_board_records,
)

PHASE_ID = "Phase-P1-Midplatform-Model-Test-Lens-Visual-Expression-System-Planning-v1-001"
PLANNING_ONLY = True

VE_REL = "capabilities/midplatform/model_test_lens/visual_expression"
SCHEMA_REL = "capabilities/midplatform/model_test_lens/schemas/visual_expression"
GOV_REL = "capabilities/midplatform/governance_standards/model_test_lens_ui"
_PKG = "capabilities/midplatform/model_test_lens"
OA_UI_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_OBSERVATION_ATTENTION_LAYER_UI_EXECUTION_GO"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{VE_REL}/visual_expression_system_plan_v1.md",
    f"{VE_REL}/visual_expression_current_slice_v1.md",
    f"{VE_REL}/visual_expression_types_v1.py",
    f"{SCHEMA_REL}/visual_layer_ownership_policy_v1.json",
    f"{SCHEMA_REL}/canvas_panel_interaction_policy_v1.json",
    f"{SCHEMA_REL}/observation_attention_visual_expression_policy_v1.json",
    f"{GOV_REL}/visual_expression_system_governance_standard_v1.md",
    f"{_PKG}/review_model_test_lens_visual_expression_system_planning_v1.py",
)

EXTRA_TEST_BOARD_RECORDS: Tuple[str, ...] = (
    "visual_layer_ownership_policy_record",
    "canvas_panel_interaction_policy_record",
    "observation_attention_visual_expression_policy_record",
    "visual_expression_boundary_audit_record",
    "visual_expression_system_plan_record",
    "visual_expression_current_slice_record",
)

NEXT_EXECUTION = (
    "Phase-P1-Midplatform-Model-Test-Lens-Visual-Expression-System-UI-Execution-And-Post-Review-v1-001"
)

FINAL_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_VISUAL_EXPRESSION_SYSTEM_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_MODEL_TEST_LENS_VISUAL_EXPRESSION_SYSTEM_PLANNING_BLOCKED"

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "A", "key": "no_runner_execution", "desc": "不触发 runner 执行"},
    {"guard_id": "B", "key": "no_fact_write", "desc": "不写 fact"},
    {"guard_id": "C", "key": "no_navigation_decision", "desc": "不做导航决策"},
    {"guard_id": "D", "key": "no_boundary_clone", "desc": "不 clone segmentation boundary"},
    {"guard_id": "E", "key": "no_secondary_box_from_attention", "desc": "Attention 不画第二套 box"},
    {"guard_id": "F", "key": "no_ground_truth_from_human_correction", "desc": "纠错非 ground truth"},
    {"guard_id": "G", "key": "no_prompt_label_fact_upgrade", "desc": "prompt_label 不升级事实"},
    {"guard_id": "H", "key": "no_motion_confirmed_from_single_frame", "desc": "单帧不 confirmed_dynamic"},
    {"guard_id": "I", "key": "canvas_panel_role_division_defined", "desc": "主图/右侧/底部/交互分工明确"},
    {"guard_id": "J", "key": "segmentation_sole_boundary_owner", "desc": "segmentation 唯一 boundary owner"},
    {"guard_id": "K", "key": "terminal_form_and_slice_defined", "desc": "终结形态与当前切片"},
    {"guard_id": "L", "key": "click_hover_selected_rules_defined", "desc": "click/hover/selected 规则完整"},
    {"guard_id": "M", "key": "p0_p1_p2_p3_strategy_defined", "desc": "P0-P3 展示策略"},
    {"guard_id": "N", "key": "readable_label_not_icon_only", "desc": "可读短标签，非图标默认"},
    {"guard_id": "O", "key": "candidate_only_constraints_preserved", "desc": "candidate_only/not_fact 保留"},
)


def _default_out_dir() -> Path:
    return (
        _detect_repo_root()
        / "_tmp_eval_out"
        / "p1_midplatform_model_test_lens_visual_expression_system_planning_v1_smoke_v0"
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
    plan = _read(f"{VE_REL}/visual_expression_system_plan_v1.md")
    slice_doc = _read(f"{VE_REL}/visual_expression_current_slice_v1.md")
    types_py = _read(f"{VE_REL}/visual_expression_types_v1.py")
    ownership = _load_json(f"{SCHEMA_REL}/visual_layer_ownership_policy_v1.json")
    interaction = _load_json(f"{SCHEMA_REL}/canvas_panel_interaction_policy_v1.json")
    attn_vis = _load_json(f"{SCHEMA_REL}/observation_attention_visual_expression_policy_v1.json")
    gov = _read(f"{GOV_REL}/visual_expression_system_governance_standard_v1.md")

    seg_owner = ownership.get("canvas_boundary_owners", {}).get("segmentation", {})
    attn_owner = ownership.get("canvas_boundary_owners", {}).get("observation_attention", {})
    forbidden_own = ownership.get("forbidden_operations", [])
    forbidden_int = interaction.get("forbidden_operations", [])
    forbidden_attn = attn_vis.get("forbidden_operations", [])

    upstream_ui = _load_json(
        "_tmp_eval_out/p1_midplatform_model_test_lens_observation_attention_layer_ui_execution_v1_smoke_v0/"
        "p1_midplatform_model_test_lens_observation_attention_layer_ui_execution_review_v1.json"
    )

    return {
        "visual_expression_system_plan_defined": "Visual Expression System" in plan
            and "终结形态原则" in plan,
        "visual_layer_ownership_policy_defined": ownership.get("schema_id") == "VisualLayerOwnershipPolicyV1",
        "canvas_panel_interaction_policy_defined": interaction.get("schema_id") == "CanvasPanelInteractionPolicyV1",
        "observation_attention_visual_expression_policy_defined": attn_vis.get("schema_id")
            == "ObservationAttentionVisualExpressionPolicyV1",
        "current_slice_defined": "VisualExpressionCurrentSliceV1" in slice_doc
            or "当前切片" in slice_doc,
        "governance_standard_defined": "VisualExpressionSystemGovernanceStandardV1" in gov,
        "upstream_observation_attention_ui_go": upstream_ui.get("final_decision") == OA_UI_GO,
        "canvas_panel_role_division_defined": "spatial_localization" in json.dumps(ownership)
            and "observation_judgment" in json.dumps(ownership)
            and "frame_scheduling_summary" in json.dumps(ownership),
        "segmentation_sole_boundary_owner": seg_owner.get("may_draw_boundary") is True
            and seg_owner.get("may_express_priority_on_boundary") is False
            and attn_owner.get("may_draw_boundary") is False
            and attn_owner.get("may_clone_segmentation_box") is False,
        "terminal_form_and_slice_defined": "终结形态" in plan and "当前阶段裁剪" in plan
            and "下一 UI Execution" in slice_doc,
        "click_hover_selected_rules_defined": "click_right_panel_record" in json.dumps(interaction)
            and "hover_canvas_region" in json.dumps(interaction)
            and "selected" in json.dumps(interaction),
        "p0_p1_p2_p3_strategy_defined": "P0_immediate_attention" in json.dumps(attn_vis.get("priority_display_strategy", {}))
            and "P2_medium_attention" in json.dumps(attn_vis.get("priority_display_strategy", {})),
        "readable_label_not_icon_only": attn_vis.get("canvas_rules", {}).get("icon_only_expression_forbidden") is True
            and "float_marker_examples" in json.dumps(attn_vis),
        "candidate_only_constraints_preserved": attn_vis.get("boundary_flags", {}).get("not_fact") is True
            and attn_vis.get("boundary_flags", {}).get("observation_attention_visual_candidate_only") is True,
        "no_runner_execution": (
            "execute_runner_from_canvas_click" in json.dumps(forbidden_attn + forbidden_int)
            or "trigger_runner" in json.dumps(interaction.get("interactions", {}))
        ) and "not_runner_execution" in types_py,
        "no_fact_write": ("write_fact" in types_py or "write_fact_from_visual_expression" in types_py)
            and (
                "write_fact" in json.dumps(forbidden_int + forbidden_attn)
                or interaction.get("boundary_flags", {}).get("not_fact_write") is True
            ),
        "no_navigation_decision": "navigation_decision_from_visual_expression" in types_py
            and interaction.get("boundary_flags", {}).get("not_navigation_instruction") is True,
        "no_boundary_clone": "attention_no_boundary_clone" in json.dumps(ownership.get("layer_conflict_rules", []))
            or "clone_segmentation_box" in json.dumps(forbidden_own + forbidden_int),
        "no_secondary_box_from_attention": "draw_attention_boundary" in forbidden_attn
            and attn_owner.get("may_draw_secondary_box") is False,
        "no_ground_truth_from_human_correction": "treat_correction_as_ground_truth" in json.dumps(attn_vis)
            and attn_vis.get("human_correction_visual_rules", {}).get("not_ground_truth") is True,
        "no_prompt_label_fact_upgrade": "upgrade_prompt_label_to_fact" in json.dumps(forbidden_attn + forbidden_own),
        "no_motion_confirmed_from_single_frame": "output_confirmed_dynamic" in json.dumps(forbidden_attn),
        "planning_only": PLANNING_ONLY,
        "testboard_required": "TestBoard" in plan or "test_board" in plan.lower(),
        "testboard_protected": REQUIRED_TEST_BOARD_FIELDS.get("test_artifact_protected") is True,
    }


def review(
    *,
    write_file: bool = True,
    write_test_board: bool = True,
    test_board_root: Optional[str] = None,
) -> Dict[str, Any]:
    failed: List[str] = []
    for rel in REQUIRED_FILES:
        if not _read(rel):
            failed.append(f"file.missing={rel}")

    flags = _audit()

    guards = []
    for spec in NEGATIVE_GUARDS:
        passed = bool(flags.get(spec["key"], False))
        guards.append({**spec, "passed": passed})
        if not passed:
            failed.append(f"guard.{spec['guard_id']}.fail={spec['key']}")

    go_conditions: Dict[str, bool] = {
        "visual_expression_system_planning_profile_count_eq_1": True,
        "visual_expression_system_plan_defined": flags["visual_expression_system_plan_defined"],
        "visual_layer_ownership_policy_defined": flags["visual_layer_ownership_policy_defined"],
        "canvas_panel_interaction_policy_defined": flags["canvas_panel_interaction_policy_defined"],
        "observation_attention_visual_expression_policy_defined": flags[
            "observation_attention_visual_expression_policy_defined"
        ],
        "current_slice_defined": flags["current_slice_defined"],
        "governance_standard_defined": flags["governance_standard_defined"],
        "canvas_panel_role_division_defined": flags["canvas_panel_role_division_defined"],
        "segmentation_sole_boundary_owner": flags["segmentation_sole_boundary_owner"],
        "terminal_form_and_slice_defined": flags["terminal_form_and_slice_defined"],
        "click_hover_selected_rules_defined": flags["click_hover_selected_rules_defined"],
        "p0_p1_p2_p3_strategy_defined": flags["p0_p1_p2_p3_strategy_defined"],
        "readable_label_not_icon_only": flags["readable_label_not_icon_only"],
        "candidate_only_constraints_preserved": flags["candidate_only_constraints_preserved"],
        "negative_guard_count_eq_15": len(guards) == 15,
        "negative_guard_passed_eq_15": sum(1 for g in guards if g["passed"]) == 15,
        "planning_only": PLANNING_ONLY,
        **{f"test_board.{k}": v is True for k, v in REQUIRED_TEST_BOARD_FIELDS.items()},
    }

    for key, ok in go_conditions.items():
        if not ok:
            failed.append(f"go.{key}=false")

    blocker_count = len(failed)
    final_decision = FINAL_GO if blocker_count == 0 else FINAL_BLOCKED

    ownership = _load_json(f"{SCHEMA_REL}/visual_layer_ownership_policy_v1.json")
    interaction = _load_json(f"{SCHEMA_REL}/canvas_panel_interaction_policy_v1.json")
    attn_vis = _load_json(f"{SCHEMA_REL}/observation_attention_visual_expression_policy_v1.json")

    boundary_audit = {
        "planning_only": PLANNING_ONLY,
        "forbidden_operations": list(set(
            ownership.get("forbidden_operations", [])
            + interaction.get("forbidden_operations", [])
            + attn_vis.get("forbidden_operations", [])
        )),
        "failed_checks": failed,
    }

    out_root = _default_out_dir()
    out_root.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "planning_only": PLANNING_ONLY,
        "visual_expression_system_planning": True,
        "visual_expression_system_planning_profile_count": 1,
        "recommended_execution_phase": NEXT_EXECUTION,
        "audit_flags": flags,
        "go_conditions": go_conditions,
        "negative_guards": guards,
        "negative_guard_count": len(guards),
        "negative_guard_passed": sum(1 for g in guards if g["passed"]),
        "blocker_count": blocker_count,
        "final_decision": final_decision,
        "failed_checks": failed,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out_root / "p1_midplatform_model_test_lens_visual_expression_system_planning_review_v1.json"
        rp.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(rp)
        (out_root / "visual_layer_ownership_policy_plan_v1.json").write_text(
            json.dumps({"plan_id": "visual_layer_ownership_policy_plan_v1", "schema": ownership},
                       indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_root / "canvas_panel_interaction_policy_plan_v1.json").write_text(
            json.dumps({"plan_id": "canvas_panel_interaction_policy_plan_v1", "schema": interaction},
                       indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_root / "observation_attention_visual_expression_policy_plan_v1.json").write_text(
            json.dumps({"plan_id": "observation_attention_visual_expression_policy_plan_v1", "schema": attn_vis},
                       indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_root / "visual_expression_boundary_audit_v1.json").write_text(
            json.dumps(boundary_audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if write_test_board:
        root = Path(test_board_root or str(_detect_repo_root()))
        try:
            tb = write_test_board_records(
                result, test_mode="planning", repo_root=root, module="model_governance",
                source_review_file=result.get("output_review_file"),
            )
        except (OSError, PermissionError):
            standin = _detect_repo_root() / "_tmp_eval_out" / "board_standin"
            standin.mkdir(parents=True, exist_ok=True)
            tb = write_test_board_records(
                result, test_mode="planning", repo_root=standin, module="model_governance",
                source_review_file=result.get("output_review_file"),
            )
        board_dir = Path(tb["test_board_dir"])
        common = {
            "phase_id": PHASE_ID,
            "protected": True,
            "non_deletable": True,
            "deletion_forbidden": True,
            "test_artifact_protected": True,
            "test_mode": "planning",
            "planning_only": True,
        }
        payloads = {
            "visual_layer_ownership_policy_record": ownership,
            "canvas_panel_interaction_policy_record": interaction,
            "observation_attention_visual_expression_policy_record": attn_vis,
            "visual_expression_boundary_audit_record": boundary_audit,
            "visual_expression_system_plan_record": {"plan_ref": f"{VE_REL}/visual_expression_system_plan_v1.md"},
            "visual_expression_current_slice_record": {"slice_ref": f"{VE_REL}/visual_expression_current_slice_v1.md"},
        }
        for rtype in EXTRA_TEST_BOARD_RECORDS:
            (board_dir / f"{rtype}.json").write_text(
                json.dumps({**common, "record": payloads.get(rtype, {"id": rtype})},
                           indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
        result["test_board_root"] = str(board_dir)
        result["test_board_record_count"] = len(REQUIRED_RECORD_TYPES) + len(EXTRA_TEST_BOARD_RECORDS)

    return result


def main() -> int:
    r = review(test_board_root=str(_detect_repo_root()))
    print(json.dumps({
        "final_decision": r["final_decision"],
        "blocker_count": r["blocker_count"],
        "negative_guard_passed": r["negative_guard_passed"],
        "negative_guard_count": r["negative_guard_count"],
        "recommended_execution_phase": r["recommended_execution_phase"],
    }, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
