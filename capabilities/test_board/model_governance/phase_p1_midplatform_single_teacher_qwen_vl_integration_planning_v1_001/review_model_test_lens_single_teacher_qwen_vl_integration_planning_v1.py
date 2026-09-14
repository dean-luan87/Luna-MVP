# -*- coding: utf-8 -*-
"""P1 Single Teacher Qwen-VL Integration — planning review v1."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[4]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


def _detect_repo_root() -> Path:
    for base in (Path.cwd(), Path(__file__).resolve().parents[4]):
        if (base / "capabilities/test_board/test_board_protocol_v1.py").is_file():
            return base
    return _REPO_ROOT


from capabilities.test_board.test_board_protocol_v1 import (  # noqa: E402
    TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1,
    write_test_board_records,
)

PHASE_ID = "Phase-P1-Midplatform-Single-Teacher-QwenVL-Integration-Planning-v1-001"
QWEN_REL = "capabilities/midplatform/teacher_adapter/providers/qwen_vl"
TB_REL = (
    "capabilities/test_board/model_governance/"
    "phase_p1_midplatform_single_teacher_qwen_vl_integration_planning_v1_001"
)

UPSTREAM_PATHS = {
    "P1_MIDPLATFORM_THIRD_PARTY_TEACHER_ADAPTER_DRYRUN_GO": (
        "_tmp_eval_out/p1_midplatform_third_party_teacher_adapter_dryrun_v1_review_v0/"
        "p1_midplatform_third_party_teacher_adapter_dryrun_review_v1.json"
    ),
    "P1_MIDPLATFORM_THIRD_PARTY_TEACHER_ADAPTER_PLANNING_GO": (
        "_tmp_eval_out/p1_midplatform_third_party_teacher_adapter_planning_v1_review_v0/"
        "p1_midplatform_third_party_teacher_adapter_planning_review_v1.json"
    ),
    "P1_MIDPLATFORM_LUNA_DECISION_VALIDATION_LAYER_DRYRUN_GO": (
        "_tmp_eval_out/p1_midplatform_luna_decision_validation_layer_dryrun_v1_review_v0/"
        "p1_midplatform_luna_decision_validation_layer_dryrun_review_v1.json"
    ),
}

FINAL_GO = "P1_MIDPLATFORM_SINGLE_TEACHER_QWENVL_INTEGRATION_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_SINGLE_TEACHER_QWENVL_INTEGRATION_PLANNING_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Single-Teacher-QwenVL-Integration-DryRun-v1-001"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{QWEN_REL}/qwen_vl_teacher_adapter_plan_v1.md",
    f"{QWEN_REL}/qwen_vl_teacher_types_v1.py",
    f"{QWEN_REL}/qwen_vl_teacher_adapter_v1.py",
    f"{QWEN_REL}/__init__.py",
    f"{QWEN_REL}/schemas/qwen_vl_teacher_request_schema_v1.json",
    f"{QWEN_REL}/schemas/qwen_vl_teacher_evidence_candidate_schema_v1.json",
    f"{QWEN_REL}/governance/qwen_vl_teacher_governance_policy_v1.json",
    f"{TB_REL}/qwen_vl_integration_planning_smoke_v1.py",
    f"{TB_REL}/run_qwen_vl_integration_planning_smoke_v1.py",
    f"{TB_REL}/review_model_test_lens_single_teacher_qwen_vl_integration_planning_v1.py",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = tuple(
    {"guard_id": f"{i:02d}", "key": k, "desc": d}
    for i, (k, d) in enumerate([
        ("provider_adapter_exists", "QwenVLTeacherAdapter 存在"),
        ("teacher_role_defined", "perception_teacher 角色定义"),
        ("no_scene_ownership_transfer", "不转移 scene 所有权"),
        ("no_plan_override", "不覆盖 plan"),
        ("no_fact_write", "不写 fact"),
        ("no_tool_execution", "不执行工具"),
        ("evidence_only", "只输出 evidence candidate"),
        ("uncertainty_preserved", "保留 uncertainty"),
        ("validation_required", "必须经过 validation"),
        ("trace_complete", "trace 完整"),
        ("future_multi_teacher_ready", "预留多 Teacher 扩展"),
        ("governance_policy_present", "治理 policy 存在"),
        ("schemas_present", "schema 齐全"),
        ("no_real_api", "无真实 API"),
        ("no_network", "无网络"),
        ("case_a_possible_text_region", "Case A 店招 text region"),
        ("case_b_slam_rejected", "Case B SLAM 拒绝"),
        ("case_c_unknown_hypothesis", "Case C unknown 场景"),
        ("case_d_unsupported_claim", "Case D 幻觉拒绝"),
        ("case_e_navigate_clue_only", "Case E navigate 线索"),
        ("validation_processor_integrated", "接入 validation processor"),
        ("no_existing_runner_mutation", "未改 runner"),
        ("smoke_cases_passed", "smoke 通过"),
        ("upstream_gos_confirmed", "上游 GO 确认"),
    ], start=1)
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


def _load_json_path(path: Path) -> Dict[str, Any]:
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def _case(cases: List[Dict[str, Any]], case_id: str) -> Dict[str, Any]:
    return next((c for c in cases if c.get("case_id") == case_id), {})


def _audit() -> Dict[str, bool]:
    adapter_py = _read(f"{QWEN_REL}/qwen_vl_teacher_adapter_v1.py")
    types_py = _read(f"{QWEN_REL}/qwen_vl_teacher_types_v1.py")
    policy = _load_json(f"{QWEN_REL}/governance/qwen_vl_teacher_governance_policy_v1.json")
    validation_proc = _read("capabilities/midplatform/teacher_adapter/luna_teacher_validation_processor_v1.py")
    runner = _read(
        "capabilities/midplatform/model_test_lens/local_runner_bridge/runners/mobilesam_image_runner_v1.py"
    )
    flags = policy.get("boundary_flags", {})

    smoke_result: Dict[str, Any] = {}
    try:
        from capabilities.test_board.model_governance.phase_p1_midplatform_single_teacher_qwen_vl_integration_planning_v1_001.qwen_vl_integration_planning_smoke_v1 import (  # noqa: WPS433
            run_smoke_cases,
        )
        smoke_result = run_smoke_cases()
    except Exception:
        smoke_result = {"final_decision": FINAL_BLOCKED}

    cases = smoke_result.get("smoke_cases", [])

    upstream_ok = all(
        _load_json_path(_detect_repo_root() / rel).get("final_decision") == go
        for go, rel in UPSTREAM_PATHS.items()
    )

    return {
        "provider_adapter_exists": "class QwenVLTeacherAdapter" in adapter_py and "request_teacher_assistance" in adapter_py,
        "teacher_role_defined": "perception_teacher" in types_py and "TEACHER_ROLE" in types_py,
        "no_scene_ownership_transfer": flags.get("qwen_not_scene_owner") is True and "does_not_override_l1_scene" in adapter_py,
        "no_plan_override": flags.get("qwen_not_plan_owner") is True and "does_not_override_l2_selected_plan" in adapter_py,
        "no_fact_write": flags.get("no_fact_write") is True and "no_fact_write" in adapter_py,
        "no_tool_execution": flags.get("no_tool_execution") is True,
        "evidence_only": flags.get("evidence_only_output") is True and "teacher_evidence_candidate" in adapter_py,
        "uncertainty_preserved": flags.get("uncertainty_required") is True and '"uncertainty"' in adapter_py,
        "validation_required": flags.get("validation_required") is True and "review_teacher_evidence" in validation_proc,
        "trace_complete": flags.get("trace_required") is True and "trace_refs" in adapter_py,
        "future_multi_teacher_ready": flags.get("future_multi_teacher_ready") is True,
        "governance_policy_present": bool(policy.get("rules")),
        "schemas_present": bool(_read(f"{QWEN_REL}/schemas/qwen_vl_teacher_request_schema_v1.json"))
            and bool(_read(f"{QWEN_REL}/schemas/qwen_vl_teacher_evidence_candidate_schema_v1.json")),
        "no_real_api": flags.get("no_real_api") is True and "dashscope" not in adapter_py.lower() and "openai" not in adapter_py.lower(),
        "no_network": "requests." not in adapter_py and "urllib" not in adapter_py,
        "case_a_possible_text_region": _case(cases, "case_a_shopfront_possible_text_region").get("passed") is True,
        "case_b_slam_rejected": _case(cases, "case_b_slam_mapping_rejected").get("passed") is True,
        "case_c_unknown_hypothesis": _case(cases, "case_c_unknown_scene_hypothesis").get("passed") is True,
        "case_d_unsupported_claim": _case(cases, "case_d_unsupported_brand_claim").get("passed") is True,
        "case_e_navigate_clue_only": _case(cases, "case_e_navigate_task_clue_only").get("passed") is True,
        "validation_processor_integrated": "unsupported_claim" in validation_proc,
        "no_existing_runner_mutation": "qwen_vl" not in runner,
        "smoke_cases_passed": smoke_result.get("final_decision", "").endswith("_GO"),
        "upstream_gos_confirmed": upstream_ok,
    }


def review(
    *,
    write_file: bool = True,
    write_test_board: bool = True,
    test_board_root: Optional[str] = None,
) -> Dict[str, Any]:
    failed: List[str] = []
    generated_files = [rel for rel in REQUIRED_FILES if _read(rel)]
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

    out_review = _detect_repo_root() / "_tmp_eval_out/p1_midplatform_single_teacher_qwen_vl_integration_planning_v1_review_v0"
    out_review.mkdir(parents=True, exist_ok=True)

    smoke_result: Dict[str, Any] = {}
    try:
        from capabilities.test_board.model_governance.phase_p1_midplatform_single_teacher_qwen_vl_integration_planning_v1_001.qwen_vl_integration_planning_smoke_v1 import (  # noqa: WPS433
            run_smoke_cases,
        )
        smoke_result = run_smoke_cases()
    except Exception:
        pass

    known_limits = [
        "planning_only_no_real_qwen_api",
        "deterministic_mock_scenarios_only",
        "perception_teacher_only_no_planning_teacher",
        "no_network",
        "no_runner_invocation",
        "no_fact_write",
        "no_direct_training",
        "qwen_does_not_override_l1_scene",
        "qwen_does_not_override_l2_plan",
        "multi_teacher_arbitration_deferred",
    ]

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "layer_id": "Teacher_Adapter",
        "provider": "qwen_vl",
        "teacher_role": "perception_teacher",
        "planning_only": True,
        "execution": False,
        "fact_write": False,
        "plan_override": False,
        "recommended_next_phase": NEXT_PHASE,
        "audit_flags": flags,
        "negative_guards": guards,
        "negative_guard_count": len(guards),
        "negative_guard_passed": ng_passed,
        "smoke_cases_passed": flags.get("smoke_cases_passed", False),
        "review_guards_passed": ng_passed,
        "blocker_count": blocker_count,
        "failed_checks": failed,
        "generated_files": generated_files,
        "job_564f1aa93983_qwen_result": smoke_result.get("job_564f1aa93983_qwen_result"),
        "known_limits": known_limits,
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out_review / "p1_midplatform_single_teacher_qwen_vl_integration_planning_review_v1.json"
        rp.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(rp)

    if write_test_board and decision == FINAL_GO:
        root = Path(test_board_root or str(_detect_repo_root()))
        try:
            tb = write_test_board_records(
                result,
                test_mode="planning",
                repo_root=root,
                module="model_governance",
                source_review_file=result.get("output_review_file"),
            )
        except (OSError, PermissionError, TypeError):
            standin = _detect_repo_root() / "_tmp_eval_out" / "board_standin"
            standin.mkdir(parents=True, exist_ok=True)
            tb = write_test_board_records(
                result,
                test_mode="planning",
                repo_root=standin,
                module="model_governance",
                source_review_file=result.get("output_review_file"),
            )
        result["test_board_root"] = str(tb.get("test_board_dir", TB_REL))

    return result


def main() -> int:
    r = review(test_board_root=str(_detect_repo_root()))
    print(json.dumps({
        "final_decision": r["final_decision"],
        "provider": r.get("provider"),
        "teacher_role": r.get("teacher_role"),
        "execution": r.get("execution"),
        "fact_write": r.get("fact_write"),
        "plan_override": r.get("plan_override"),
        "blocker_count": r["blocker_count"],
        "smoke_cases_passed": r.get("smoke_cases_passed"),
        "review_guards_passed": r.get("review_guards_passed"),
        "job_564f1aa93983_qwen_result": r.get("job_564f1aa93983_qwen_result"),
        "recommended_next_phase": r.get("recommended_next_phase"),
        "failed_checks": r.get("failed_checks", []),
    }, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
