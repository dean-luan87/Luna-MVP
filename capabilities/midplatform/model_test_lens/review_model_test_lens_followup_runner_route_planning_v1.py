# -*- coding: utf-8 -*-
"""P1 Followup Runner Route — planning review v1."""

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
    for base in (Path.cwd(), Path(__file__).resolve().parents[3]):
        if (base / "capabilities/test_board/test_board_protocol_v1.py").is_file():
            return base
    return _REPO_ROOT


from capabilities.test_board.test_board_protocol_v1 import (  # noqa: E402
    REQUIRED_RECORD_TYPES,
    REQUIRED_TEST_BOARD_FIELDS,
    TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1,
    write_test_board_records,
)

PHASE_ID = "Phase-P1-Midplatform-Model-Test-Lens-Followup-Runner-Route-Planning-v1-001"
PLANNING_ONLY = True
ROUTE_REL = "capabilities/midplatform/model_test_lens/followup_runner_route"
SCHEMA_REL = "capabilities/midplatform/model_test_lens/schemas/followup_runner_route"
GOV_REL = "capabilities/midplatform/governance_standards/model_test_lens_ui"
_PKG = "capabilities/midplatform/model_test_lens"
OA_SCHEMA = "capabilities/midplatform/model_test_lens/schemas/observation_attention"

CONTRAST_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_SEGMENTATION_BOUNDARY_CONTRAST_RESTORE_GO"
VE_PLANNING_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_VISUAL_EXPRESSION_SYSTEM_PLANNING_GO"
OA_UI_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_OBSERVATION_ATTENTION_LAYER_UI_EXECUTION_GO"

FINAL_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_FOLLOWUP_RUNNER_ROUTE_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_MODEL_TEST_LENS_FOLLOWUP_RUNNER_ROUTE_PLANNING_BLOCKED"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{ROUTE_REL}/followup_runner_route_plan_v1.md",
    f"{ROUTE_REL}/followup_runner_route_types_v1.py",
    f"{SCHEMA_REL}/followup_runner_task_candidate_schema_v1.json",
    f"{SCHEMA_REL}/runner_route_mapping_policy_v1.json",
    f"{SCHEMA_REL}/runner_route_admission_policy_v1.json",
    f"{GOV_REL}/followup_runner_route_governance_standard_v1.md",
    f"{_PKG}/review_model_test_lens_followup_runner_route_planning_v1.py",
)

EXTRA_TEST_BOARD_RECORDS: Tuple[str, ...] = (
    "followup_runner_task_candidate_schema_record",
    "runner_route_mapping_policy_record",
    "runner_route_admission_policy_record",
    "followup_runner_route_plan_record",
)

NEXT_EXECUTION = (
    "Phase-P1-Midplatform-Model-Test-Lens-Followup-Runner-Route-UI-Queue-Execution-And-Post-Review-v1-001"
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "A", "key": "no_runner_execution", "desc": "不触发 runner 执行"},
    {"guard_id": "B", "key": "no_model_call", "desc": "不调用模型"},
    {"guard_id": "C", "key": "no_fact_write", "desc": "不写 fact"},
    {"guard_id": "D", "key": "no_navigation_decision", "desc": "不做导航决策"},
    {"guard_id": "E", "key": "no_auto_runner_trigger", "desc": "不自动触发 runner"},
    {"guard_id": "F", "key": "no_human_correction_ground_truth", "desc": "纠错非 ground truth"},
    {"guard_id": "G", "key": "no_prompt_label_fact_upgrade", "desc": "prompt_label 不升级事实"},
    {"guard_id": "H", "key": "no_motion_confirmed_from_single_frame", "desc": "单帧不 confirmed_dynamic"},
    {"guard_id": "I", "key": "no_visual_expression_mutation", "desc": "不改变 Visual Expression System"},
    {"guard_id": "J", "key": "route_to_task_mapping_defined", "desc": "route→task 映射完整"},
    {"guard_id": "K", "key": "p0_p1_auto_eligible_defined", "desc": "P0/P1 默认可入队"},
    {"guard_id": "L", "key": "p2_p3_manual_only_defined", "desc": "P2/P3 默认 manual_only"},
    {"guard_id": "M", "key": "runner_task_candidate_not_execution", "desc": "task candidate ≠ 执行"},
    {"guard_id": "N", "key": "ocr_detection_tracking_depth_rules_defined", "desc": "模型路由规则完整"},
    {"guard_id": "O", "key": "planning_only", "desc": "仅规划不执行"},
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


def _load_review(rel: str) -> Dict[str, Any]:
    return _load_json(rel) if _read(rel) else {}


def _audit() -> Dict[str, bool]:
    plan = _read(f"{ROUTE_REL}/followup_runner_route_plan_v1.md")
    types_py = _read(f"{ROUTE_REL}/followup_runner_route_types_v1.py")
    task_schema = _load_json(f"{SCHEMA_REL}/followup_runner_task_candidate_schema_v1.json")
    mapping = _load_json(f"{SCHEMA_REL}/runner_route_mapping_policy_v1.json")
    admission = _load_json(f"{SCHEMA_REL}/runner_route_admission_policy_v1.json")
    gov = _read(f"{GOV_REL}/followup_runner_route_governance_standard_v1.md")
    upstream_route = _load_json(f"{OA_SCHEMA}/followup_model_route_schema_v1.json")

    contrast = _load_review(
        "_tmp_eval_out/p1_midplatform_model_test_lens_segmentation_boundary_contrast_restore_v1_smoke_v0/"
        "p1_midplatform_model_test_lens_segmentation_boundary_contrast_restore_review_v1.json"
    )
    ve_plan = _load_review(
        "_tmp_eval_out/p1_midplatform_model_test_lens_visual_expression_system_planning_v1_smoke_v0/"
        "p1_midplatform_model_test_lens_visual_expression_system_planning_review_v1.json"
    )

    p0 = admission.get("priority_admission", {}).get("P0_immediate_attention", {})
    p2 = admission.get("priority_admission", {}).get("P2_medium_attention", {})
    rules = mapping.get("model_routing_rules", {})

    return {
        "followup_runner_route_plan_defined": "runner_task_candidate" in plan and "核心链路" in plan,
        "followup_runner_route_types_defined": "FOLLOWUP_RUNNER_ROUTE_SYSTEM_ID" in types_py,
        "followup_runner_task_candidate_schema_defined": task_schema.get("schema_id") == "FollowupRunnerTaskCandidateSchemaV1",
        "runner_route_mapping_policy_defined": mapping.get("schema_id") == "RunnerRouteMappingPolicyV1",
        "runner_route_admission_policy_defined": admission.get("schema_id") == "RunnerRouteAdmissionPolicyV1",
        "governance_standard_defined": "FollowupRunnerRouteGovernanceStandardV1" in gov,
        "upstream_followup_route_schema_exists": upstream_route.get("schema_id") == "FollowupModelRouteSchemaV1",
        "upstream_contrast_restore_go": contrast.get("final_decision") == CONTRAST_GO,
        "upstream_visual_expression_planning_go": ve_plan.get("final_decision") == VE_PLANNING_GO,
        "no_runner_execution": (
            task_schema.get("boundary_flags", {}).get("not_runner_execution") is True
            and "no_runner_execution" in types_py
        ),
        "no_model_call": "model_call" in json.dumps(admission.get("forbidden_operations", [])),
        "no_fact_write": (
            task_schema.get("boundary_flags", {}).get("not_fact") is True
            and "not_fact_write" in json.dumps(admission)
        ),
        "no_navigation_decision": task_schema.get("boundary_flags", {}).get("not_navigation_instruction") is True,
        "no_auto_runner_trigger": admission.get("auto_runner_trigger_allowed") is False,
        "no_human_correction_ground_truth": (
            "ground truth" in gov.lower() or "ground_truth" in json.dumps(admission)
            or "treat_as_ground_truth" in json.dumps(admission)
        ),
        "no_prompt_label_fact_upgrade": (
            "prompt_label_as_ground_truth" in json.dumps(task_schema)
            or "prompt_label_as_detection_ground_truth" in json.dumps(mapping)
        ),
        "no_motion_confirmed_from_single_frame": (
            "confirmed_dynamic" in json.dumps(admission.get("frame_context_rules", {}))
            or "confirmed_dynamic_from_single_frame" in json.dumps(task_schema)
        ),
        "no_visual_expression_mutation": (
            admission.get("visual_expression_preservation", {}).get("canvas_frozen") is True
            and "visual_expression_system_frozen" in types_py
        ),
        "route_to_task_mapping_defined": (
            "field_mapping" in mapping and "runner_task_candidate_id" in json.dumps(mapping.get("field_mapping", {}))
        ),
        "p0_p1_auto_eligible_defined": (
            p0.get("queue_admission") == "auto_eligible"
            and admission.get("priority_admission", {}).get("P1_high_attention", {}).get("queue_admission") == "auto_eligible"
        ),
        "p2_p3_manual_only_defined": (
            p2.get("queue_admission") == "manual_only"
            and admission.get("priority_admission", {}).get("P3_low_attention", {}).get("queue_admission") == "manual_only"
        ),
        "runner_task_candidate_not_execution": (
            task_schema.get("boundary_flags", {}).get("runner_task_candidate_only") is True
            and task_schema.get("boundary_flags", {}).get("not_runner_execution") is True
        ),
        "ocr_detection_tracking_depth_rules_defined": (
            all(k in rules for k in ("detection", "ocr", "tracking", "depth", "slam"))
        ),
        "planning_only": PLANNING_ONLY and task_schema.get("boundary_flags", {}).get("planning_only") is True,
        "recommended_next_execution_defined": NEXT_EXECUTION in plan or NEXT_EXECUTION in json.dumps(admission),
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

    ng_passed = sum(1 for g in guards if g["passed"])
    blocker_count = len(failed)
    decision = FINAL_GO if blocker_count == 0 else FINAL_BLOCKED

    out = _detect_repo_root() / "_tmp_eval_out" / (
        "p1_midplatform_model_test_lens_followup_runner_route_planning_v1_smoke_v0"
    )
    out.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "planning_only": PLANNING_ONLY,
        "recommended_execution_phase": NEXT_EXECUTION,
        "audit_flags": flags,
        "negative_guards": guards,
        "negative_guard_count": len(guards),
        "negative_guard_passed": ng_passed,
        "blocker_count": blocker_count,
        "failed_checks": failed,
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out / "p1_midplatform_model_test_lens_followup_runner_route_planning_review_v1.json"
        rp.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(rp)

    if write_test_board and decision == FINAL_GO:
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
            "phase_id": PHASE_ID, "protected": True, "non_deletable": True,
            "deletion_forbidden": True, "test_artifact_protected": True,
            "test_mode": "planning", "planning_only": True,
        }
        payloads = {
            "followup_runner_task_candidate_schema_record": _load_json(f"{SCHEMA_REL}/followup_runner_task_candidate_schema_v1.json"),
            "runner_route_mapping_policy_record": _load_json(f"{SCHEMA_REL}/runner_route_mapping_policy_v1.json"),
            "runner_route_admission_policy_record": _load_json(f"{SCHEMA_REL}/runner_route_admission_policy_v1.json"),
            "followup_runner_route_plan_record": {"plan_ref": f"{ROUTE_REL}/followup_runner_route_plan_v1.md"},
        }
        for rtype in EXTRA_TEST_BOARD_RECORDS:
            (board_dir / f"{rtype}.json").write_text(
                json.dumps({**common, "record": payloads.get(rtype, {"id": rtype})},
                           indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
        result["test_board_root"] = str(board_dir)

    return result


def main() -> int:
    r = review(test_board_root=str(_detect_repo_root()))
    print(json.dumps({
        "final_decision": r["final_decision"],
        "blocker_count": r["blocker_count"],
        "negative_guard_passed": r["negative_guard_passed"],
        "negative_guard_count": r["negative_guard_count"],
        "recommended_execution_phase": r["recommended_execution_phase"],
        "failed_checks": r.get("failed_checks", []),
    }, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
