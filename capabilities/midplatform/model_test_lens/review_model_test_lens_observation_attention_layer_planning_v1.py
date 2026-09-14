# -*- coding: utf-8 -*-
"""P1 Observation Attention Layer — planning review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Model-Test-Lens-Observation-Attention-Layer-Planning-v1-001"
PLANNING_ONLY = True

OA_REL = "capabilities/midplatform/model_test_lens/observation_attention"
SCHEMA_REL = "capabilities/midplatform/model_test_lens/schemas/observation_attention"
GOV_REL = "capabilities/midplatform/governance_standards/model_test_lens_ui"
_PKG = "capabilities/midplatform/model_test_lens"
HC_PLAN = f"{_PKG}/human_correction/human_correction_layer_plan_v1.md"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{OA_REL}/observation_attention_layer_plan_v1.md",
    f"{OA_REL}/observation_attention_types_v1.py",
    f"{SCHEMA_REL}/observation_attention_record_schema_v1.json",
    f"{SCHEMA_REL}/region_priority_schema_v1.json",
    f"{SCHEMA_REL}/followup_model_route_schema_v1.json",
    f"{SCHEMA_REL}/observation_attention_policy_v1.json",
    f"{SCHEMA_REL}/static_dynamic_observation_policy_v1.json",
    f"{SCHEMA_REL}/observation_target_motion_state_schema_v1.json",
    f"{GOV_REL}/observation_attention_layer_governance_standard_v1.md",
    f"{_PKG}/review_model_test_lens_observation_attention_layer_planning_v1.py",
)

EXTRA_TEST_BOARD_RECORDS: Tuple[str, ...] = (
    "observation_attention_policy_record",
    "region_priority_schema_record",
    "followup_model_route_schema_record",
    "human_correction_linkage_record",
    "boundary_audit_record",
    "observation_attention_layer_plan_record",
    "static_dynamic_observation_policy_record",
    "motion_state_schema_record",
)

NEXT_EXECUTION = (
    "Phase-P1-Midplatform-Model-Test-Lens-Observation-Attention-Layer-UI-Execution-And-Post-Review-v1-001"
)

FINAL_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_OBSERVATION_ATTENTION_LAYER_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_MODEL_TEST_LENS_OBSERVATION_ATTENTION_LAYER_PLANNING_BLOCKED"

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "A", "key": "no_direct_model_execution", "desc": "不得直接调用后续模型"},
    {"guard_id": "B", "key": "no_fact_semantic_registry", "desc": "不得写 fact/semantic/registry"},
    {"guard_id": "C", "key": "no_navigation_speech", "desc": "不得生成导航或语音"},
    {"guard_id": "D", "key": "envelope_immutable", "desc": "不得修改 envelope/模型输出"},
    {"guard_id": "E", "key": "prompt_label_candidate_only", "desc": "prompt_label 不得当事实类别"},
    {"guard_id": "F", "key": "correction_not_ground_truth", "desc": "correction 不得当 ground truth"},
    {"guard_id": "G", "key": "route_not_execution", "desc": "route 不是立即执行"},
    {"guard_id": "H", "key": "region_priority_schema_defined_guard", "desc": "region priority schema 完整"},
    {"guard_id": "I", "key": "followup_route_schema_defined", "desc": "followup route schema 完整"},
    {"guard_id": "J", "key": "task_context_policy_defined", "desc": "task context policy 完整"},
    {"guard_id": "K", "key": "candidate_not_fact_boundaries", "desc": "candidate_only/not_fact 边界"},
    {"guard_id": "L", "key": "human_correction_linkage_defined", "desc": "Human Correction 联动"},
    {"guard_id": "M", "key": "testboard_required", "desc": "TestBoard 规划完整"},
    {"guard_id": "N", "key": "testboard_protected", "desc": "TestBoard protected"},
    {"guard_id": "O", "key": "no_confirmed_dynamic_single_frame", "desc": "单帧不得 confirmed_dynamic"},
    {"guard_id": "P", "key": "tracking_route_for_dynamic_defined", "desc": "动态候选含 tracking route"},
    {"guard_id": "Q", "key": "ocr_route_for_static_text_defined", "desc": "静态文字含 OCR route"},
    {"guard_id": "R", "key": "depth_slam_route_for_structure_defined", "desc": "结构候选含 Depth/SLAM route"},
    {"guard_id": "S", "key": "correction_not_motion_ground_truth", "desc": "Correction 非 motion ground truth"},
)


def _default_out_dir() -> Path:
    return (
        _detect_repo_root()
        / "_tmp_eval_out"
        / "p1_midplatform_model_test_lens_observation_attention_layer_planning_v1_smoke_v0"
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
    record = _load_json(f"{SCHEMA_REL}/observation_attention_record_schema_v1.json")
    priority = _load_json(f"{SCHEMA_REL}/region_priority_schema_v1.json")
    route = _load_json(f"{SCHEMA_REL}/followup_model_route_schema_v1.json")
    policy = _load_json(f"{SCHEMA_REL}/observation_attention_policy_v1.json")
    sd_policy = _load_json(f"{SCHEMA_REL}/static_dynamic_observation_policy_v1.json")
    motion = _load_json(f"{SCHEMA_REL}/observation_target_motion_state_schema_v1.json")
    types_py = _read(f"{OA_REL}/observation_attention_types_v1.py")
    plan = _read(f"{OA_REL}/observation_attention_layer_plan_v1.md")
    gov = _read(f"{GOV_REL}/observation_attention_layer_governance_standard_v1.md")

    record_req = set(record.get("required", []))
    priority_levels = priority.get("priority_levels", [])
    followup_models = [m.get("model_id", "") for m in route.get("recommended_followup_models", [])]
    task_contexts = policy.get("task_contexts", [])
    mobile_sam = policy.get("mobile_sam_region_strategy", {})
    hc_link = policy.get("human_correction_linkage", {})
    hc_motion = sd_policy.get("human_correction_motion_linkage", {})
    static_routes = sd_policy.get("static_observation_routes", {})
    dynamic_routes = sd_policy.get("dynamic_observation_routes", {})
    structure_routes = sd_policy.get("scene_structure_routes", {})
    single_frame_lim = sd_policy.get("single_frame_limitation", {})

    return {
        "observation_attention_record_schema_defined": record.get("schema_id") == "ObservationAttentionRecordSchemaV1",
        "region_priority_schema_defined": priority.get("schema_id") == "RegionPrioritySchemaV1",
        "region_priority_schema_defined_guard": len(priority_levels) >= 5,
        "followup_model_route_schema_defined": route.get("schema_id") == "FollowupModelRouteSchemaV1",
        "followup_route_schema_defined": route.get("schema_id") == "FollowupModelRouteSchemaV1",
        "observation_attention_policy_defined": policy.get("schema_id") == "ObservationAttentionPolicyV1",
        "motion_state_candidate_schema_defined": motion.get("schema_id") == "ObservationTargetMotionStateSchemaV1",
        "static_dynamic_observation_policy_defined": sd_policy.get("schema_id") == "StaticDynamicObservationPolicyV1",
        "task_context_policy_defined": len(task_contexts) >= 7 and "street_navigation_test" in task_contexts,
        "mobile_sam_region_strategy_defined": len(mobile_sam.get("strategies", [])) >= 5
            and mobile_sam.get("prompt_label_is_candidate_only") is True,
        "human_correction_linkage_defined": len(hc_link.get("rules", [])) >= 4
            and hc_link.get("not_ground_truth") is True,
        "human_correction_motion_linkage_defined": len(hc_motion.get("rules", [])) >= 4
            and hc_motion.get("not_motion_ground_truth") is True,
        "static_observation_routes_defined": bool(static_routes.get("rules")),
        "dynamic_observation_routes_defined": bool(dynamic_routes.get("rules")),
        "scene_structure_routes_defined": bool(structure_routes.get("rules")),
        "single_frame_motion_limitation_defined": single_frame_lim.get(
            "mobile_sam_single_frame_must_not_confirm_dynamic"
        ) is True,
        "tracking_route_for_dynamic_candidates_defined": "tracking" in json.dumps(dynamic_routes),
        "ocr_route_for_static_text_candidates_defined": "ocr" in json.dumps(static_routes),
        "depth_slam_route_for_scene_structure_defined": "depth" in json.dumps(structure_routes)
            and "slam" in json.dumps(structure_routes),
        "followup_routes_candidate_only": route.get("boundary_flags", {}).get("followup_model_route_candidate_only") is True,
        "observation_attention_candidate_only": record.get("properties", {}).get("candidate_only", {}).get("const") is True,
        "region_priority_candidate_only": priority.get("boundary_flags", {}).get("region_priority_candidate_only") is True,
        "no_direct_model_execution": "execute_detection" in record.get("forbidden_operations", [])
            and "must_not_execute_models" in json.dumps(policy),
        "no_fact_semantic_registry": all(
            x in record.get("forbidden_operations", []) for x in ("write_fact", "write_semantic", "mutate_registry")
        ),
        "no_navigation_speech": all(
            x in record.get("forbidden_operations", [])
            for x in ("trigger_navigation", "trigger_speech")
        ),
        "envelope_immutable": "modify_original_envelope" in record.get("forbidden_operations", [])
            and "must_not_modify_original_envelope" in types_py,
        "must_not_modify_original_envelope": "must_not_modify_original_envelope" in types_py,
        "must_not_modify_model_output": "overwrite_model_output" in types_py,
        "must_not_write_fact": "must_not_write_fact" in types_py,
        "must_not_write_semantic": "must_not_write_semantic" in types_py,
        "must_not_trigger_runtime": "must_not_trigger_runtime" in types_py,
        "must_not_trigger_navigation_action_speech": "must_not_trigger_navigation_action_speech" in types_py,
        "must_not_call_output_adapter": "must_not_call_output_adapter" in types_py,
        "must_not_mutate_registry": "must_not_mutate_registry" in types_py,
        "prompt_label_candidate_only": "prompt_label_candidate" in json.dumps(record)
            and "upgrade_prompt_label_to_fact" in record.get("forbidden_operations", []),
        "correction_not_ground_truth": "treat_correction_as_ground_truth" in record.get("forbidden_operations", [])
            and hc_link.get("correction_is_priority_signal_only") is True,
        "correction_not_motion_ground_truth": "treat_correction_as_motion_ground_truth" in record.get("forbidden_operations", [])
            and hc_motion.get("not_motion_ground_truth") is True,
        "route_not_execution": "execute_followup_route_immediately" in record.get("forbidden_operations", [])
            and route.get("boundary_flags", {}).get("not_execution_command") is True,
        "no_confirmed_dynamic_single_frame": "output_confirmed_dynamic_from_single_frame" in record.get("forbidden_operations", [])
            and motion.get("boundary_flags", {}).get("single_frame_no_confirmed_dynamic") is True,
        "tracking_route_for_dynamic_defined": "tracking" in followup_models
            and "tracking" in json.dumps(dynamic_routes),
        "ocr_route_for_static_text_defined": "ocr" in followup_models
            and "ocr" in json.dumps(static_routes),
        "depth_slam_route_for_structure_defined": "depth" in followup_models
            and "slam" in json.dumps(structure_routes),
        "followup_route_schema_defined_guard": len(followup_models) >= 10,
        "candidate_not_fact_boundaries": "candidate_only" in record_req and "not_fact" in record_req
            and "motion_state_candidate" in record_req,
        "testboard_required": "TestBoard" in plan or "test_board" in plan.lower(),
        "testboard_protected": REQUIRED_TEST_BOARD_FIELDS.get("test_artifact_protected") is True,
        "governance_standard_defined": "ObservationAttentionLayerGovernanceStandardV1" in gov,
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
        "observation_attention_layer_planning_profile_count_eq_1": True,
        "observation_attention_record_schema_defined": flags["observation_attention_record_schema_defined"],
        "region_priority_schema_defined": flags["region_priority_schema_defined"],
        "followup_model_route_schema_defined": flags["followup_model_route_schema_defined"],
        "observation_attention_policy_defined": flags["observation_attention_policy_defined"],
        "task_context_policy_defined": flags["task_context_policy_defined"],
        "mobile_sam_region_strategy_defined": flags["mobile_sam_region_strategy_defined"],
        "human_correction_linkage_defined": flags["human_correction_linkage_defined"],
        "human_correction_motion_linkage_defined": flags["human_correction_motion_linkage_defined"],
        "motion_state_candidate_schema_defined": flags["motion_state_candidate_schema_defined"],
        "static_dynamic_observation_policy_defined": flags["static_dynamic_observation_policy_defined"],
        "static_observation_routes_defined": flags["static_observation_routes_defined"],
        "dynamic_observation_routes_defined": flags["dynamic_observation_routes_defined"],
        "scene_structure_routes_defined": flags["scene_structure_routes_defined"],
        "single_frame_motion_limitation_defined": flags["single_frame_motion_limitation_defined"],
        "tracking_route_for_dynamic_candidates_defined": flags["tracking_route_for_dynamic_candidates_defined"],
        "ocr_route_for_static_text_candidates_defined": flags["ocr_route_for_static_text_candidates_defined"],
        "depth_slam_route_for_scene_structure_defined": flags["depth_slam_route_for_scene_structure_defined"],
        "followup_routes_candidate_only": flags["followup_routes_candidate_only"],
        "observation_attention_candidate_only": flags["observation_attention_candidate_only"],
        "region_priority_candidate_only": flags["region_priority_candidate_only"],
        "must_not_modify_original_envelope": flags["must_not_modify_original_envelope"],
        "must_not_modify_model_output": flags["must_not_modify_model_output"],
        "must_not_write_fact": flags["must_not_write_fact"],
        "must_not_write_semantic": flags["must_not_write_semantic"],
        "must_not_trigger_runtime": flags["must_not_trigger_runtime"],
        "must_not_trigger_navigation_action_speech": flags["must_not_trigger_navigation_action_speech"],
        "must_not_call_output_adapter": flags["must_not_call_output_adapter"],
        "must_not_mutate_registry": flags["must_not_mutate_registry"],
        "negative_guard_count_eq_19": len(guards) == 19,
        "negative_guard_passed_eq_19": sum(1 for g in guards if g["passed"]) == 19,
        "planning_only": PLANNING_ONLY,
        **{f"test_board.{k}": v is True for k, v in REQUIRED_TEST_BOARD_FIELDS.items()},
    }

    for key, ok in go_conditions.items():
        if not ok:
            failed.append(f"go.{key}=false")

    blocker_count = len(failed)
    final_decision = FINAL_GO if blocker_count == 0 else FINAL_BLOCKED

    record_schema = _load_json(f"{SCHEMA_REL}/observation_attention_record_schema_v1.json")
    priority_schema = _load_json(f"{SCHEMA_REL}/region_priority_schema_v1.json")
    route_schema = _load_json(f"{SCHEMA_REL}/followup_model_route_schema_v1.json")
    policy_schema = _load_json(f"{SCHEMA_REL}/observation_attention_policy_v1.json")

    sd_policy = _load_json(f"{SCHEMA_REL}/static_dynamic_observation_policy_v1.json")
    motion_schema = _load_json(f"{SCHEMA_REL}/observation_target_motion_state_schema_v1.json")

    linkage_plan = {
        "plan_id": "human_correction_linkage_plan_v1",
        "linkage": policy_schema.get("human_correction_linkage", {}),
        "motion_linkage": sd_policy.get("human_correction_motion_linkage", {}),
        "upstream": HC_PLAN,
    }

    boundary_audit = {
        "planning_only": PLANNING_ONLY,
        "forbidden_operations": record_schema.get("forbidden_operations", []),
        "failed_checks": failed,
    }

    out_root = _default_out_dir()
    out_root.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "planning_only": PLANNING_ONLY,
        "observation_attention_layer_planning": True,
        "observation_attention_layer_planning_profile_count": 1,
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
        rp = out_root / "p1_midplatform_model_test_lens_observation_attention_layer_planning_review_v1.json"
        rp.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(rp)
        (out_root / "observation_attention_record_schema_plan_v1.json").write_text(
            json.dumps({"plan_id": "observation_attention_record_schema_plan_v1", "schema": record_schema},
                       indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_root / "region_priority_schema_plan_v1.json").write_text(
            json.dumps({"plan_id": "region_priority_schema_plan_v1", "schema": priority_schema},
                       indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_root / "followup_model_route_schema_plan_v1.json").write_text(
            json.dumps({"plan_id": "followup_model_route_schema_plan_v1", "schema": route_schema},
                       indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_root / "observation_attention_policy_plan_v1.json").write_text(
            json.dumps({"plan_id": "observation_attention_policy_plan_v1", "schema": policy_schema},
                       indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_root / "static_dynamic_observation_policy_plan_v1.json").write_text(
            json.dumps({"plan_id": "static_dynamic_observation_policy_plan_v1", "schema": sd_policy},
                       indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_root / "motion_state_schema_plan_v1.json").write_text(
            json.dumps({"plan_id": "motion_state_schema_plan_v1", "schema": motion_schema},
                       indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_root / "human_correction_linkage_plan_v1.json").write_text(
            json.dumps(linkage_plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_root / "observation_attention_boundary_audit_v1.json").write_text(
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
            "observation_attention_policy_record": policy_schema,
            "region_priority_schema_record": priority_schema,
            "followup_model_route_schema_record": route_schema,
            "human_correction_linkage_record": linkage_plan,
            "boundary_audit_record": boundary_audit,
            "observation_attention_layer_plan_record": {"plan_ref": f"{OA_REL}/observation_attention_layer_plan_v1.md"},
            "static_dynamic_observation_policy_record": sd_policy,
            "motion_state_schema_record": motion_schema,
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
