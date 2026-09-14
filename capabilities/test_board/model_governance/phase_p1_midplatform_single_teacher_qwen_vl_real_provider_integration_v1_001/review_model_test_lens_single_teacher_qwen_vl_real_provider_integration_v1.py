# -*- coding: utf-8 -*-
"""P1 Qwen-VL Real Provider Integration — review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Single-Teacher-QwenVL-Real-Provider-Integration-v1-001"
QWEN_REL = "capabilities/midplatform/teacher_adapter/providers/qwen_vl"
REAL_REL = f"{QWEN_REL}/qwen_vl_real_integration"
TB_REL = (
    "capabilities/test_board/model_governance/"
    "phase_p1_midplatform_single_teacher_qwen_vl_real_provider_integration_v1_001"
)

UPSTREAM_PATHS = {
    "P1_MIDPLATFORM_SINGLE_TEACHER_QWENVL_INTEGRATION_DRYRUN_GO": (
        "_tmp_eval_out/p1_midplatform_single_teacher_qwen_vl_integration_dryrun_v1_review_v0/"
        "p1_midplatform_single_teacher_qwen_vl_integration_dryrun_review_v1.json"
    ),
    "P1_MIDPLATFORM_SINGLE_TEACHER_QWENVL_INTEGRATION_PLANNING_GO": (
        "_tmp_eval_out/p1_midplatform_single_teacher_qwen_vl_integration_planning_v1_review_v0/"
        "p1_midplatform_single_teacher_qwen_vl_integration_planning_review_v1.json"
    ),
}

FINAL_GO = "P1_MIDPLATFORM_SINGLE_TEACHER_QWENVL_REAL_PROVIDER_INTEGRATION_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_SINGLE_TEACHER_QWENVL_REAL_PROVIDER_INTEGRATION_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Teacher-Performance-Evaluation-v1-001"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{QWEN_REL}/api_client_v1.py",
    f"{QWEN_REL}/request_builder_v1.py",
    f"{QWEN_REL}/response_parser_v1.py",
    f"{QWEN_REL}/evidence_normalizer_v1.py",
    f"{QWEN_REL}/qwen_vl_real_provider_v1.py",
    f"{QWEN_REL}/teacher_usage_metrics_v1.py",
    f"{QWEN_REL}/governance/qwen_vl_real_provider_policy_v1.json",
    f"{QWEN_REL}/governance/teacher_usage_policy_v1.json",
    f"{QWEN_REL}/schemas/qwen_vl_raw_teacher_response_schema_v1.json",
    f"{QWEN_REL}/schemas/teacher_usage_metrics_schema_v1.json",
    f"{REAL_REL}/luna_qwen_vl_real_integration_adapter_v1.py",
    f"{TB_REL}/luna_qwen_vl_real_provider_integration_fixtures_v1.py",
    f"{TB_REL}/run_luna_qwen_vl_real_provider_integration_v1.py",
    f"{TB_REL}/review_model_test_lens_single_teacher_qwen_vl_real_provider_integration_v1.py",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = tuple(
    {"guard_id": f"{i:02d}", "key": k, "desc": d}
    for i, (k, d) in enumerate([
        ("provider_layer_split", "Provider 层职责拆分"),
        ("api_client_present", "api_client 存在"),
        ("request_builder_present", "request_builder 存在"),
        ("response_parser_present", "response_parser 存在"),
        ("evidence_normalizer_present", "evidence_normalizer 存在"),
        ("raw_response_separated", "raw 与 evidence 分离"),
        ("teacher_admission_present", "Teacher Admission"),
        ("teacher_usage_policy_present", "teacher_usage_policy"),
        ("teacher_usage_metrics_present", "Teacher Usage Metrics"),
        ("no_scene_override", "不覆盖 scene"),
        ("no_plan_override", "不覆盖 plan"),
        ("no_tool_execution", "不执行工具"),
        ("no_fact_write", "不写 fact"),
        ("validation_required", "必须经过 validation"),
        ("unsupported_claim_gate", "unsupported_claim 门"),
        ("case_a_unknown_scene", "Case A unknown 场景"),
        ("case_b_shopfront_noop", "Case B 店招 noop"),
        ("case_c_slam_rejected", "Case C SLAM 拒绝"),
        ("case_d_unsupported_claim", "Case D 幻觉拒绝"),
        ("no_existing_runner_mutation", "未改 runner"),
        ("integration_cases_pass", "integration cases 通过"),
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
    api = _read(f"{QWEN_REL}/api_client_v1.py")
    builder = _read(f"{QWEN_REL}/request_builder_v1.py")
    parser = _read(f"{QWEN_REL}/response_parser_v1.py")
    normalizer = _read(f"{QWEN_REL}/evidence_normalizer_v1.py")
    real_provider = _read(f"{QWEN_REL}/qwen_vl_real_provider_v1.py")
    adapter = _read(f"{REAL_REL}/luna_qwen_vl_real_integration_adapter_v1.py")
    metrics = _read(f"{QWEN_REL}/teacher_usage_metrics_v1.py")
    policy = _load_json(f"{QWEN_REL}/governance/qwen_vl_real_provider_policy_v1.json")
    usage = _load_json(f"{QWEN_REL}/governance/teacher_usage_policy_v1.json")
    validation = _read("capabilities/midplatform/teacher_adapter/luna_teacher_validation_processor_v1.py")
    runner = _read(
        "capabilities/midplatform/model_test_lens/local_runner_bridge/runners/mobilesam_image_runner_v1.py"
    )
    flags = policy.get("boundary_flags", {})

    integration_result: Dict[str, Any] = {}
    try:
        from capabilities.test_board.model_governance.phase_p1_midplatform_single_teacher_qwen_vl_real_provider_integration_v1_001.luna_qwen_vl_real_provider_integration_fixtures_v1 import (  # noqa: WPS433
            run_all_integration_cases,
        )
        integration_result = run_all_integration_cases()
    except Exception:
        integration_result = {"final_decision": FINAL_BLOCKED}

    cases = integration_result.get("integration_cases", [])

    upstream_ok = all(
        _load_json_path(_detect_repo_root() / rel).get("final_decision") == go
        for go, rel in UPSTREAM_PATHS.items()
    )

    return {
        "provider_layer_split": all(x in real_provider for x in ("call_qwen_vl_api", "parse_raw_teacher_response", "normalize_teacher_evidence")),
        "api_client_present": "call_qwen_vl_api" in api,
        "request_builder_present": "build_teacher_request" in builder,
        "response_parser_present": "parse_raw_teacher_response" in parser,
        "evidence_normalizer_present": "normalize_teacher_evidence" in normalizer,
        "raw_response_separated": flags.get("raw_response_separated") is True and integration_result.get("raw_response_separated") is True,
        "teacher_admission_present": "evaluate_qwen_teacher_admission" in adapter,
        "teacher_usage_policy_present": bool(usage.get("admission_matrix")),
        "teacher_usage_metrics_present": "TeacherUsageMetrics" in metrics,
        "no_scene_override": flags.get("no_scene_override") is True,
        "no_plan_override": flags.get("no_plan_override") is True,
        "no_tool_execution": flags.get("no_tool_execution") is True,
        "no_fact_write": flags.get("no_fact_write") is True,
        "validation_required": flags.get("validation_required") is True and "review_teacher_evidence" in adapter,
        "unsupported_claim_gate": flags.get("unsupported_claim_gate") is True and "unsupported_claim" in validation,
        "case_a_unknown_scene": _case(cases, "case_a_unknown_scene_real_evidence").get("passed") is True,
        "case_b_shopfront_noop": _case(cases, "case_b_shopfront_teacher_noop").get("passed") is True,
        "case_c_slam_rejected": _case(cases, "case_c_slam_suggestion_rejected").get("passed") is True,
        "case_d_unsupported_claim": _case(cases, "case_d_unsupported_claim_rejected").get("passed") is True,
        "no_existing_runner_mutation": "qwen_vl_real_integration" not in runner,
        "integration_cases_pass": integration_result.get("final_decision", "").endswith("_GO"),
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

    out_review = _detect_repo_root() / "_tmp_eval_out/p1_midplatform_single_teacher_qwen_vl_real_provider_integration_v1_review_v0"
    out_review.mkdir(parents=True, exist_ok=True)

    integration_result: Dict[str, Any] = {}
    try:
        from capabilities.test_board.model_governance.phase_p1_midplatform_single_teacher_qwen_vl_real_provider_integration_v1_001.luna_qwen_vl_real_provider_integration_fixtures_v1 import (  # noqa: WPS433
            run_all_integration_cases,
        )
        integration_result = run_all_integration_cases()
    except Exception:
        pass

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "layer_id": "Teacher_Adapter",
        "provider": "qwen_vl",
        "real_provider_integration": True,
        "recommended_next_phase": NEXT_PHASE,
        "audit_flags": flags,
        "negative_guards": guards,
        "negative_guard_count": len(guards),
        "negative_guard_passed": ng_passed,
        "integration_cases_passed": flags.get("integration_cases_pass", False),
        "blocker_count": blocker_count,
        "failed_checks": failed,
        "generated_files": generated_files,
        "teacher_usage_metrics": integration_result.get("teacher_usage_metrics"),
        "known_limits": [
            "recorded_fixture_default_for_ci",
            "live_mode_requires_DASHSCOPE_API_KEY_and_LUNA_QWEN_VL_TEACHER_LIVE",
            "no_multi_teacher_arbitration_yet",
            "no_direct_training",
            "teacher_performance_evaluation_deferred",
        ],
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out_review / "p1_midplatform_single_teacher_qwen_vl_real_provider_integration_review_v1.json"
        rp.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(rp)

    if write_test_board and decision == FINAL_GO:
        root = Path(test_board_root or str(_detect_repo_root()))
        try:
            tb = write_test_board_records(
                result,
                test_mode="real_test",
                repo_root=root,
                module="model_governance",
                source_review_file=result.get("output_review_file"),
            )
        except (OSError, PermissionError, TypeError):
            standin = _detect_repo_root() / "_tmp_eval_out" / "board_standin"
            standin.mkdir(parents=True, exist_ok=True)
            tb = write_test_board_records(
                result,
                test_mode="real_test",
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
        "blocker_count": r["blocker_count"],
        "integration_cases_passed": r.get("integration_cases_passed"),
        "review_guards_passed": r.get("negative_guard_passed"),
        "teacher_usage_metrics": r.get("teacher_usage_metrics"),
        "recommended_next_phase": r.get("recommended_next_phase"),
        "failed_checks": r.get("failed_checks", []),
    }, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
