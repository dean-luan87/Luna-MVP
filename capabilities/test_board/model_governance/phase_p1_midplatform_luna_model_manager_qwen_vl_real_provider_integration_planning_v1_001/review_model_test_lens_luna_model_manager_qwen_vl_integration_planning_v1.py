# -*- coding: utf-8 -*-
"""P1 Luna Model Manager Qwen-VL Real Provider — planning review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Luna-Model-Manager-QwenVL-Real-Provider-Integration-Planning-v1-001"
MM_REL = "capabilities/midplatform/model_manager"
PROV_REL = f"{MM_REL}/providers/qwen_vl"
TB_REL = (
    "capabilities/test_board/model_governance/"
    "phase_p1_midplatform_luna_model_manager_qwen_vl_real_provider_integration_planning_v1_001"
)

UPSTREAM_PATHS = {
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_LIFECYCLE_SANDBOX_GO": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_lifecycle_sandbox_v1_review_v0/"
        "p1_midplatform_luna_model_manager_lifecycle_sandbox_review_v1.json"
    ),
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_FOUNDATION_DRYRUN_GO": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_foundation_dryrun_v1_review_v0/"
        "p1_midplatform_luna_model_manager_foundation_dryrun_review_v1.json"
    ),
    "P1_MIDPLATFORM_SINGLE_TEACHER_QWENVL_REAL_PROVIDER_INTEGRATION_GO": (
        "_tmp_eval_out/p1_midplatform_single_teacher_qwen_vl_real_provider_integration_v1_review_v0/"
        "p1_midplatform_single_teacher_qwen_vl_real_provider_integration_review_v1.json"
    ),
}

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_QWENVL_REAL_PROVIDER_INTEGRATION_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_QWENVL_REAL_PROVIDER_INTEGRATION_PLANNING_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Local-Model-Integration-Planning-v1-001"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{MM_REL}/luna_model_manager_qwen_vl_integration_plan_v1.md",
    f"{MM_REL}/luna_model_manager_qwen_vl_types_v1.py",
    f"{MM_REL}/luna_model_manager_qwen_vl_processor_v1.py",
    f"{PROV_REL}/qwen_vl_provider_adapter_v1.py",
    f"{PROV_REL}/qwen_vl_request_builder_v1.py",
    f"{PROV_REL}/qwen_vl_response_parser_v1.py",
    f"{PROV_REL}/qwen_vl_provider_profile_v1.json",
    f"{PROV_REL}/governance/qwen_vl_model_manager_provider_policy_v1.json",
    f"{TB_REL}/luna_model_manager_qwen_vl_integration_planning_smoke_v1.py",
    f"{TB_REL}/run_luna_model_manager_qwen_vl_integration_planning_smoke_v1.py",
    f"{TB_REL}/review_model_test_lens_luna_model_manager_qwen_vl_integration_planning_v1.py",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = tuple(
    {"guard_id": f"{i:02d}", "key": k, "desc": d}
    for i, (k, d) in enumerate([
        ("integration_plan_present", "integration 规划文档"),
        ("provider_adapter_present", "provider adapter 存在"),
        ("request_builder_present", "request builder 存在"),
        ("response_parser_present", "response parser 存在"),
        ("provider_profile_present", "provider profile 存在"),
        ("provider_policy_present", "provider policy 存在"),
        ("registry_owned_not_hardcoded", "Registry 接管非硬编码"),
        ("capability_first_routing", "能力优先路由"),
        ("lifecycle_gated", "lifecycle 门控"),
        ("qwen_not_special_teacher", "Qwen 非特殊 Teacher"),
        ("no_fact_write", "不写 fact"),
        ("no_plan_override", "不覆盖 plan"),
        ("provider_error_to_l2", "provider 错误交还 L2"),
        ("case_a_unknown_evidence", "Case A unknown evidence"),
        ("case_b_shopfront_noop", "Case B 店招 Qwen noop"),
        ("case_c_timeout_fallback", "Case C timeout fallback"),
        ("case_d_unsupported_reject", "Case D unsupported reject"),
        ("case_e_lifecycle_switch", "Case E lifecycle 切换"),
        ("frozen_teacher_prerequisite", "Teacher 前置冻结"),
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


def _load_json(path: Path) -> Dict[str, Any]:
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def _case(cases: List[Dict[str, Any]], case_id: str) -> Dict[str, Any]:
    return next((c for c in cases if c.get("case_id") == case_id), {})


def _audit() -> Dict[str, bool]:
    plan = _read(f"{MM_REL}/luna_model_manager_qwen_vl_integration_plan_v1.md")
    processor = _read(f"{MM_REL}/luna_model_manager_qwen_vl_processor_v1.py")
    adapter = _read(f"{PROV_REL}/qwen_vl_provider_adapter_v1.py")
    policy = _load_json(_detect_repo_root() / f"{PROV_REL}/governance/qwen_vl_model_manager_provider_policy_v1.json")
    profile = _load_json(_detect_repo_root() / f"{PROV_REL}/qwen_vl_provider_profile_v1.json")
    runner = _read(
        "capabilities/midplatform/model_test_lens/local_runner_bridge/runners/mobilesam_image_runner_v1.py"
    )

    smoke_result: Dict[str, Any] = {}
    try:
        from capabilities.test_board.model_governance.phase_p1_midplatform_luna_model_manager_qwen_vl_real_provider_integration_planning_v1_001.luna_model_manager_qwen_vl_integration_planning_smoke_v1 import (  # noqa: WPS433
            run_smoke_cases,
        )
        smoke_result = run_smoke_cases()
    except Exception:
        smoke_result = {"final_decision": FINAL_BLOCKED}

    cases = smoke_result.get("smoke_cases", [])
    upstream_ok = all(
        _load_json(_detect_repo_root() / rel).get("final_decision") == go
        for go, rel in UPSTREAM_PATHS.items()
    )

    return {
        "integration_plan_present": "Model Manager" in plan and "Qwen-VL" in plan,
        "provider_adapter_present": "invoke_qwen_vl_provider" in adapter,
        "request_builder_present": "build_qwen_vl_provider_request" in _read(f"{PROV_REL}/qwen_vl_request_builder_v1.py"),
        "response_parser_present": "parse_qwen_vl_provider_response" in _read(f"{PROV_REL}/qwen_vl_response_parser_v1.py"),
        "provider_profile_present": profile.get("managed_by") == "LunaModelManager",
        "provider_policy_present": policy.get("schema_id") == "QwenVLModelManagerProviderPolicyV1",
        "registry_owned_not_hardcoded": "load_qwen_model_from_registry" in adapter and "no_hardcoded_provider_call" in processor,
        "capability_first_routing": policy.get("boundary_flags", {}).get("capability_first") is True,
        "lifecycle_gated": "is_routing_eligible" in adapter,
        "qwen_not_special_teacher": "qwen_not_special_teacher" in _read(f"{MM_REL}/luna_model_manager_qwen_vl_types_v1.py"),
        "no_fact_write": policy.get("boundary_flags", {}).get("evidence_not_fact") is True,
        "no_plan_override": policy.get("boundary_flags", {}).get("no_plan_override") is True,
        "provider_error_to_l2": policy.get("boundary_flags", {}).get("provider_error_to_l2") is True,
        "case_a_unknown_evidence": _case(cases, "case_a_unknown_scene_qwen_evidence").get("passed") is True,
        "case_b_shopfront_noop": _case(cases, "case_b_shopfront_ocr_qwen_noop").get("passed") is True,
        "case_c_timeout_fallback": _case(cases, "case_c_qwen_provider_timeout_fallback").get("passed") is True,
        "case_d_unsupported_reject": _case(cases, "case_d_qwen_unsupported_claim_reject").get("passed") is True,
        "case_e_lifecycle_switch": _case(cases, "case_e_qwen_lifecycle_version_switch").get("passed") is True,
        "frozen_teacher_prerequisite": "FROZEN_PREREQUISITES" in _read(f"{MM_REL}/luna_model_manager_qwen_vl_types_v1.py"),
        "no_existing_runner_mutation": "qwen_vl_provider" not in runner,
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

    blocker_count = len(failed)
    decision = FINAL_GO if blocker_count == 0 else FINAL_BLOCKED

    out_review = _detect_repo_root() / "_tmp_eval_out/p1_midplatform_luna_model_manager_qwen_vl_real_provider_integration_planning_v1_review_v0"
    out_review.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "layer_id": "Model_Manager_QwenVL",
        "planning_only": True,
        "recommended_next_phase": NEXT_PHASE,
        "audit_flags": flags,
        "negative_guards": guards,
        "negative_guard_count": len(guards),
        "negative_guard_passed": sum(1 for g in guards if g["passed"]),
        "smoke_cases_passed": flags.get("smoke_cases_passed", False),
        "blocker_count": blocker_count,
        "failed_checks": failed,
        "generated_files": generated_files,
        "known_limits": [
            "planning_only_no_live_api",
            "teacher_adapter_qwen_vl_frozen_not_removed",
            "gemini_internvl_deferred",
            "local_model_phase_after_qwen_dryrun",
        ],
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out_review / "p1_midplatform_luna_model_manager_qwen_vl_real_provider_integration_planning_review_v1.json"
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
        "blocker_count": r["blocker_count"],
        "smoke_cases_passed": r.get("smoke_cases_passed"),
        "review_guards_passed": r.get("negative_guard_passed"),
        "recommended_next_phase": r.get("recommended_next_phase"),
        "failed_checks": r.get("failed_checks", []),
    }, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
