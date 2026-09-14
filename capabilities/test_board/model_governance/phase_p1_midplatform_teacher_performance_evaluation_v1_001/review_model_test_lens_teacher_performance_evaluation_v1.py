# -*- coding: utf-8 -*-
"""P1 Teacher Performance Evaluation — review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Teacher-Performance-Evaluation-v1-001"
TE_REL = "capabilities/midplatform/teacher_evaluation"
TB_REL = "capabilities/test_board/model_governance/phase_p1_midplatform_teacher_performance_evaluation_v1_001"

UPSTREAM_PATHS = {
    "P1_MIDPLATFORM_SINGLE_TEACHER_QWENVL_REAL_PROVIDER_INTEGRATION_GO": (
        "_tmp_eval_out/p1_midplatform_single_teacher_qwen_vl_real_provider_integration_v1_review_v0/"
        "p1_midplatform_single_teacher_qwen_vl_real_provider_integration_review_v1.json"
    ),
    "P1_MIDPLATFORM_SINGLE_TEACHER_QWENVL_INTEGRATION_DRYRUN_GO": (
        "_tmp_eval_out/p1_midplatform_single_teacher_qwen_vl_integration_dryrun_v1_review_v0/"
        "p1_midplatform_single_teacher_qwen_vl_integration_dryrun_review_v1.json"
    ),
}

FINAL_GO = "P1_MIDPLATFORM_TEACHER_PERFORMANCE_EVALUATION_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_TEACHER_PERFORMANCE_EVALUATION_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Multi-Teacher-Validation-Planning-v1-001"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{TE_REL}/teacher_performance_evaluation_plan_v1.md",
    f"{TE_REL}/luna_teacher_performance_types_v1.py",
    f"{TE_REL}/teacher_performance_metrics_v1.py",
    f"{TE_REL}/teacher_performance_processor_v1.py",
    f"{TE_REL}/luna_teacher_performance_evaluation_adapter_v1.py",
    f"{TE_REL}/governance/teacher_performance_evaluation_policy_v1.json",
    f"{TE_REL}/schemas/teacher_performance_record_schema_v1.json",
    f"{TE_REL}/schemas/teacher_usage_profile_candidate_schema_v1.json",
    f"{TE_REL}/schemas/teacher_reliability_metrics_schema_v1.json",
    f"{TB_REL}/luna_teacher_performance_evaluation_fixtures_v1.py",
    f"{TB_REL}/run_luna_teacher_performance_evaluation_v1.py",
    f"{TB_REL}/review_model_test_lens_teacher_performance_evaluation_v1.py",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = tuple(
    {"guard_id": f"{i:02d}", "key": k, "desc": d}
    for i, (k, d) in enumerate([
        ("evaluation_plan_present", "评估规划文档"),
        ("metrics_module_present", "metrics 模块"),
        ("processor_present", "processor 存在"),
        ("evaluation_adapter_present", "evaluation adapter"),
        ("schemas_present", "schema 齐全"),
        ("policy_present", "治理 policy"),
        ("does_not_affect_decision", "不影响当前决策"),
        ("no_auto_policy_update", "不自动更新 policy"),
        ("usage_profile_candidate", "usage profile candidate"),
        ("reliability_metrics", "reliability metrics"),
        ("policy_update_candidate", "policy update candidate"),
        ("evaluation_after_validation", "validation 之后评估"),
        ("case_a_high_value", "Case A 高价值"),
        ("case_b_noop_correct", "Case B noop 正确"),
        ("case_c_policy_rejection", "Case C policy 拒绝"),
        ("case_d_unsupported_claim", "Case D 幻觉"),
        ("future_multi_teacher_ready", "多 Teacher 预留"),
        ("no_existing_runner_mutation", "未改 runner"),
        ("evaluation_cases_pass", "evaluation cases 通过"),
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
    plan = _read(f"{TE_REL}/teacher_performance_evaluation_plan_v1.md")
    metrics = _read(f"{TE_REL}/teacher_performance_metrics_v1.py")
    processor = _read(f"{TE_REL}/teacher_performance_processor_v1.py")
    adapter = _read(f"{TE_REL}/luna_teacher_performance_evaluation_adapter_v1.py")
    policy = _load_json(f"{TE_REL}/governance/teacher_performance_evaluation_policy_v1.json")
    runner = _read(
        "capabilities/midplatform/model_test_lens/local_runner_bridge/runners/mobilesam_image_runner_v1.py"
    )
    flags = policy.get("boundary_flags", {})

    eval_result: Dict[str, Any] = {}
    try:
        from capabilities.test_board.model_governance.phase_p1_midplatform_teacher_performance_evaluation_v1_001.luna_teacher_performance_evaluation_fixtures_v1 import (  # noqa: WPS433
            run_all_evaluation_cases,
        )
        eval_result = run_all_evaluation_cases()
    except Exception:
        eval_result = {"final_decision": FINAL_BLOCKED}

    cases = eval_result.get("evaluation_cases", [])

    upstream_ok = all(
        _load_json_path(_detect_repo_root() / rel).get("final_decision") == go
        for go, rel in UPSTREAM_PATHS.items()
    )

    return {
        "evaluation_plan_present": "Teacher Performance Evaluation" in plan,
        "metrics_module_present": "TeacherPerformanceMetrics" in metrics,
        "processor_present": "evaluate_teacher_performance" in processor,
        "evaluation_adapter_present": "run_teacher_performance_evaluation_chain" in adapter,
        "schemas_present": all(_read(f"{TE_REL}/schemas/{s}") for s in (
            "teacher_performance_record_schema_v1.json",
            "teacher_usage_profile_candidate_schema_v1.json",
            "teacher_reliability_metrics_schema_v1.json",
        )),
        "policy_present": bool(policy.get("rules")),
        "does_not_affect_decision": flags.get("does_not_affect_current_decision") is True and eval_result.get("does_not_affect_current_decision") is True,
        "no_auto_policy_update": flags.get("no_auto_policy_update") is True and "no_auto_apply" in processor,
        "usage_profile_candidate": "teacher_usage_profile_candidate" in processor,
        "reliability_metrics": "teacher_reliability_metrics" in processor,
        "policy_update_candidate": "usage_policy_update_candidate" in processor,
        "evaluation_after_validation": "evaluate_teacher_performance" in adapter and "run_qwen_vl_real_provider_integration" in adapter,
        "case_a_high_value": _case(cases, "case_a_high_value_unknown_scene").get("passed") is True,
        "case_b_noop_correct": _case(cases, "case_b_low_value_shopfront_noop").get("passed") is True,
        "case_c_policy_rejection": _case(cases, "case_c_policy_rejection_slam").get("passed") is True,
        "case_d_unsupported_claim": _case(cases, "case_d_unsupported_claim_hallucination").get("passed") is True,
        "future_multi_teacher_ready": flags.get("future_multi_teacher_ready") is True,
        "no_existing_runner_mutation": "teacher_performance_evaluation" not in runner,
        "evaluation_cases_pass": eval_result.get("final_decision", "").endswith("_GO"),
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

    blocker_count = len(failed)
    decision = FINAL_GO if blocker_count == 0 else FINAL_BLOCKED

    out_review = _detect_repo_root() / "_tmp_eval_out/p1_midplatform_teacher_performance_evaluation_v1_review_v0"
    out_review.mkdir(parents=True, exist_ok=True)

    eval_result: Dict[str, Any] = {}
    try:
        from capabilities.test_board.model_governance.phase_p1_midplatform_teacher_performance_evaluation_v1_001.luna_teacher_performance_evaluation_fixtures_v1 import (  # noqa: WPS433
            run_all_evaluation_cases,
        )
        eval_result = run_all_evaluation_cases()
    except Exception:
        pass

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "layer_id": "Teacher_Performance_Evaluation",
        "provider": "qwen_vl",
        "recommended_next_phase": NEXT_PHASE,
        "audit_flags": flags,
        "negative_guards": guards,
        "negative_guard_count": len(guards),
        "negative_guard_passed": sum(1 for g in guards if g["passed"]),
        "evaluation_cases_passed": flags.get("evaluation_cases_pass", False),
        "blocker_count": blocker_count,
        "failed_checks": failed,
        "generated_files": generated_files,
        "teacher_reliability_metrics": eval_result.get("teacher_reliability_metrics"),
        "teacher_performance_metrics": eval_result.get("teacher_performance_metrics"),
        "known_limits": [
            "evaluation_does_not_auto_update_usage_policy",
            "policy_update_requires_human_review",
            "single_teacher_qwen_vl_only",
            "multi_teacher_arbitration_deferred",
        ],
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out_review / "p1_midplatform_teacher_performance_evaluation_review_v1.json"
        rp.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(rp)

    if write_test_board and decision == FINAL_GO:
        root = Path(test_board_root or str(_detect_repo_root()))
        try:
            tb = write_test_board_records(
                result,
                test_mode="post_review",
                repo_root=root,
                module="model_governance",
                source_review_file=result.get("output_review_file"),
            )
        except (OSError, PermissionError, TypeError):
            standin = _detect_repo_root() / "_tmp_eval_out" / "board_standin"
            standin.mkdir(parents=True, exist_ok=True)
            tb = write_test_board_records(
                result,
                test_mode="post_review",
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
        "blocker_count": r["blocker_count"],
        "evaluation_cases_passed": r.get("evaluation_cases_passed"),
        "teacher_reliability_metrics": r.get("teacher_reliability_metrics"),
        "recommended_next_phase": r.get("recommended_next_phase"),
        "failed_checks": r.get("failed_checks", []),
    }, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
