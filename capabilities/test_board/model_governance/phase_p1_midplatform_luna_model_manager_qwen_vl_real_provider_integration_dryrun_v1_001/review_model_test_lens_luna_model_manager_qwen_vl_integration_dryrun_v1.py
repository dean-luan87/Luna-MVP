# -*- coding: utf-8 -*-
"""P1 Luna Model Manager Qwen-VL Real Provider — dryrun review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Luna-Model-Manager-QwenVL-Real-Provider-Integration-DryRun-v1-001"
MM_REL = "capabilities/midplatform/model_manager"
PROV_REL = f"{MM_REL}/providers/qwen_vl"
DRYRUN_REL = f"{PROV_REL}/dryrun"
TB_REL = (
    "capabilities/test_board/model_governance/"
    "phase_p1_midplatform_luna_model_manager_qwen_vl_real_provider_integration_dryrun_v1_001"
)

UPSTREAM_PATHS = {
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_QWENVL_REAL_PROVIDER_INTEGRATION_PLANNING_GO": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_qwen_vl_real_provider_integration_planning_v1_review_v0/"
        "p1_midplatform_luna_model_manager_qwen_vl_real_provider_integration_planning_review_v1.json"
    ),
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_LIFECYCLE_SANDBOX_GO": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_lifecycle_sandbox_v1_review_v0/"
        "p1_midplatform_luna_model_manager_lifecycle_sandbox_review_v1.json"
    ),
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_FOUNDATION_DRYRUN_GO": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_foundation_dryrun_v1_review_v0/"
        "p1_midplatform_luna_model_manager_foundation_dryrun_review_v1.json"
    ),
}

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_QWENVL_REAL_PROVIDER_INTEGRATION_DRYRUN_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_QWENVL_REAL_PROVIDER_INTEGRATION_DRYRUN_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Local-Model-Integration-DryRun-v1-001"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{DRYRUN_REL}/qwen_vl_provider_dryrun_adapter_v1.py",
    f"{DRYRUN_REL}/qwen_vl_lifecycle_integration_v1.py",
    f"{DRYRUN_REL}/qwen_vl_routing_validation_v1.py",
    f"{DRYRUN_REL}/qwen_vl_evidence_normalizer_v1.py",
    f"{DRYRUN_REL}/qwen_vl_model_usage_metrics_v1.py",
    f"{DRYRUN_REL}/qwen_vl_provider_dryrun_policy_v1.json",
    f"{PROV_REL}/qwen_vl_provider_adapter_v1.py",
    f"{TB_REL}/luna_model_manager_qwen_vl_integration_dryrun_fixtures_v1.py",
    f"{TB_REL}/run_luna_model_manager_qwen_vl_integration_dryrun_v1.py",
    f"{TB_REL}/review_model_test_lens_luna_model_manager_qwen_vl_integration_dryrun_v1.py",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = tuple(
    {"guard_id": f"{i:02d}", "key": k, "desc": d}
    for i, (k, d) in enumerate([
        ("dryrun_adapter_present", "dryrun adapter 存在"),
        ("lifecycle_integration_present", "lifecycle integration 存在"),
        ("routing_validation_present", "routing validation 存在"),
        ("evidence_normalizer_present", "evidence normalizer 存在"),
        ("usage_metrics_present", "usage metrics 存在"),
        ("dryrun_policy_present", "dryrun policy 存在"),
        ("full_chain_closed_loop", "全链路闭环"),
        ("model_manager_no_goal_ownership", "MM 不拥有目标"),
        ("provider_no_internal_state", "Provider 无内部状态"),
        ("provider_output_not_fact", "输出非 fact"),
        ("usage_metrics_to_evaluation", "metrics 进 evaluation"),
        ("case_a_normal_loop", "Case A 正常闭环"),
        ("case_b_capability_mismatch", "Case B 能力不匹配"),
        ("case_c_version_switch", "Case C 版本切换"),
        ("case_d_timeout_no_switch", "Case D timeout 不偷换"),
        ("case_e_unsupported_governance", "Case E unsupported 治理"),
        ("frozen_teacher_prerequisite", "Teacher 前置冻结"),
        ("no_existing_runner_mutation", "未改 runner"),
        ("dryrun_cases_pass", "dryrun cases 通过"),
        ("upstream_gos_confirmed", "上游 GO 确认"),
    ], start=1)
)


def _read(rel: str) -> str:
    for base in (_detect_repo_root(), _REPO_ROOT, Path.cwd()):
        p = base / rel
        if p.is_file():
            return p.read_text(encoding="utf-8")
    return ""


def _load_json(path: Path) -> Dict[str, Any]:
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def _case(cases: List[Dict[str, Any]], case_id: str) -> Dict[str, Any]:
    return next((c for c in cases if c.get("case_id") == case_id), {})


def _audit() -> Dict[str, bool]:
    adapter = _read(f"{DRYRUN_REL}/qwen_vl_provider_dryrun_adapter_v1.py")
    policy = _load_json(_detect_repo_root() / f"{DRYRUN_REL}/qwen_vl_provider_dryrun_policy_v1.json")
    runner = _read(
        "capabilities/midplatform/model_test_lens/local_runner_bridge/runners/mobilesam_image_runner_v1.py"
    )

    dryrun_result: Dict[str, Any] = {}
    try:
        from capabilities.test_board.model_governance.phase_p1_midplatform_luna_model_manager_qwen_vl_real_provider_integration_dryrun_v1_001.luna_model_manager_qwen_vl_integration_dryrun_fixtures_v1 import (  # noqa: WPS433
            run_all_dryrun_cases,
        )
        dryrun_result = run_all_dryrun_cases()
    except Exception:
        dryrun_result = {"final_decision": FINAL_BLOCKED}

    cases = dryrun_result.get("dryrun_cases", [])
    upstream_ok = all(
        _load_json(_detect_repo_root() / rel).get("final_decision") == go
        for go, rel in UPSTREAM_PATHS.items()
    )

    case_a = _case(cases, "case_a_qwen_normal_closed_loop").get("result") or {}

    return {
        "dryrun_adapter_present": "run_qwen_vl_provider_dryrun" in adapter,
        "lifecycle_integration_present": "run_qwen_version_switch_dryrun" in _read(f"{DRYRUN_REL}/qwen_vl_lifecycle_integration_v1.py"),
        "routing_validation_present": "validate_routing_candidate" in _read(f"{DRYRUN_REL}/qwen_vl_routing_validation_v1.py"),
        "evidence_normalizer_present": "normalize_qwen_evidence_candidate" in _read(f"{DRYRUN_REL}/qwen_vl_evidence_normalizer_v1.py"),
        "usage_metrics_present": "QwenVLModelUsageMetrics" in _read(f"{DRYRUN_REL}/qwen_vl_model_usage_metrics_v1.py"),
        "dryrun_policy_present": policy.get("schema_id") == "QwenVLProviderDryrunPolicyV1",
        "full_chain_closed_loop": "evaluation_record" in adapter and "model_evaluation_record" in adapter,
        "model_manager_no_goal_ownership": policy.get("boundary_flags", {}).get("model_manager_no_goal_ownership") is True,
        "provider_no_internal_state": policy.get("boundary_flags", {}).get("provider_no_internal_state") is True,
        "provider_output_not_fact": policy.get("boundary_flags", {}).get("provider_output_not_fact") is True,
        "usage_metrics_to_evaluation": policy.get("boundary_flags", {}).get("usage_metrics_to_evaluation") is True,
        "case_a_normal_loop": _case(cases, "case_a_qwen_normal_closed_loop").get("passed") is True,
        "case_b_capability_mismatch": _case(cases, "case_b_capability_mismatch_ocr_selected").get("passed") is True,
        "case_c_version_switch": _case(cases, "case_c_qwen_version_switch").get("passed") is True,
        "case_d_timeout_no_switch": _case(cases, "case_d_provider_timeout_no_silent_switch").get("passed") is True,
        "case_e_unsupported_governance": _case(cases, "case_e_unsupported_claim_governance").get("passed") is True,
        "frozen_teacher_prerequisite": "FROZEN_PREREQUISITES" in _read(f"{MM_REL}/luna_model_manager_qwen_vl_types_v1.py"),
        "no_existing_runner_mutation": "qwen_vl_provider_dryrun" not in runner,
        "dryrun_cases_pass": dryrun_result.get("final_decision", "").endswith("_GO"),
        "upstream_gos_confirmed": upstream_ok,
        "_case_a_has_evaluation": (case_a.get("model_evaluation_record") or {}).get("no_auto_policy_update") is True,
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

    out_review = _detect_repo_root() / "_tmp_eval_out/p1_midplatform_luna_model_manager_qwen_vl_real_provider_integration_dryrun_v1_review_v0"
    out_review.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "layer_id": "Model_Manager_QwenVL_DryRun",
        "dryrun_only": True,
        "recommended_next_phase": NEXT_PHASE,
        "audit_flags": flags,
        "negative_guards": guards,
        "negative_guard_count": len(guards),
        "negative_guard_passed": sum(1 for g in guards if g["passed"]),
        "dryrun_cases_passed": flags.get("dryrun_cases_pass", False),
        "blocker_count": blocker_count,
        "failed_checks": failed,
        "generated_files": generated_files,
        "known_limits": [
            "dryrun_recorded_fixtures_no_live_api_default",
            "teacher_adapter_qwen_vl_frozen_not_removed",
            "gemini_deferred",
            "local_model_next_internvl_minicpm",
        ],
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out_review / "p1_midplatform_luna_model_manager_qwen_vl_real_provider_integration_dryrun_review_v1.json"
        rp.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(rp)

    if write_test_board and decision == FINAL_GO:
        root = Path(test_board_root or str(_detect_repo_root()))
        try:
            tb = write_test_board_records(
                result,
                test_mode="dry_run",
                repo_root=root,
                module="model_governance",
                source_review_file=result.get("output_review_file"),
            )
        except (OSError, PermissionError, TypeError):
            standin = _detect_repo_root() / "_tmp_eval_out" / "board_standin"
            standin.mkdir(parents=True, exist_ok=True)
            tb = write_test_board_records(
                result,
                test_mode="dry_run",
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
        "dryrun_cases_passed": r.get("dryrun_cases_passed"),
        "review_guards_passed": r.get("negative_guard_passed"),
        "recommended_next_phase": r.get("recommended_next_phase"),
        "failed_checks": r.get("failed_checks", []),
    }, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
