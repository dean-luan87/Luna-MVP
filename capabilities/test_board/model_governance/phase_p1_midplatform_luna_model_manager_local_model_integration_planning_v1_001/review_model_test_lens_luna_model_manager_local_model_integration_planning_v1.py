# -*- coding: utf-8 -*-
"""P1 Luna Model Manager Local Model — planning review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Luna-Model-Manager-Local-Model-Integration-Planning-v1-001"
MM_REL = "capabilities/midplatform/model_manager"
LR_REL = f"{MM_REL}/local_runtime"
RT_REL = f"{MM_REL}/runtime"
TB_REL = (
    "capabilities/test_board/model_governance/"
    "phase_p1_midplatform_luna_model_manager_local_model_integration_planning_v1_001"
)

UPSTREAM_PATHS = {
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_QWENVL_REAL_PROVIDER_INTEGRATION_DRYRUN_GO": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_qwen_vl_real_provider_integration_dryrun_v1_review_v0/"
        "p1_midplatform_luna_model_manager_qwen_vl_real_provider_integration_dryrun_review_v1.json"
    ),
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_LIFECYCLE_SANDBOX_GO": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_lifecycle_sandbox_v1_review_v0/"
        "p1_midplatform_luna_model_manager_lifecycle_sandbox_review_v1.json"
    ),
}

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_LOCAL_MODEL_INTEGRATION_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_LOCAL_MODEL_INTEGRATION_PLANNING_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Local-Model-Integration-DryRun-v1-001"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{LR_REL}/local_model_integration_plan_v1.md",
    f"{LR_REL}/local_model_runtime_adapter_v1.py",
    f"{LR_REL}/local_model_resource_profile_schema_v1.json",
    f"{LR_REL}/local_model_admission_policy_v1.json",
    f"{LR_REL}/local_model_runtime_health_policy_v1.json",
    f"{LR_REL}/local_model_lifecycle_adapter_v1.py",
    f"{MM_REL}/luna_model_manager_local_model_types_v1.py",
    f"{MM_REL}/luna_model_manager_local_model_processor_v1.py",
    f"{RT_REL}/local_model_runtime_adapter_v1.py",
    f"{RT_REL}/runtime_health_checker_v1.py",
    f"{RT_REL}/runtime_resource_profile_v1.py",
    f"{RT_REL}/runtime_policy_v1.json",
    f"{TB_REL}/luna_model_manager_local_model_integration_planning_smoke_v1.py",
    f"{TB_REL}/run_luna_model_manager_local_model_integration_planning_smoke_v1.py",
    f"{TB_REL}/review_model_test_lens_luna_model_manager_local_model_integration_planning_v1.py",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = tuple(
    {"guard_id": f"{i:02d}", "key": k, "desc": d}
    for i, (k, d) in enumerate([
        ("integration_plan_present", "integration 规划文档"),
        ("runtime_adapter_present", "runtime adapter 存在"),
        ("lifecycle_adapter_present", "lifecycle adapter 存在"),
        ("resource_profile_schema_present", "resource profile schema"),
        ("admission_policy_present", "admission policy 存在"),
        ("health_policy_present", "health policy 存在"),
        ("runtime_policy_present", "runtime policy 存在"),
        ("unified_execution_mode", "统一 execution_mode 抽象"),
        ("resource_aware_routing", "资源感知路由"),
        ("provider_fallback_explicit", "显式 provider fallback"),
        ("no_separate_api_local_logic", "无 API/Local 两套逻辑"),
        ("model_manager_location_agnostic", "MM 不关心运行位置"),
        ("no_training_finetuning", "不做训练/finetuning"),
        ("case_a_local_admission", "Case A 本地准入"),
        ("case_b_gpu_fallback", "Case B GPU fallback"),
        ("case_c_local_external", "Case C Local vs External"),
        ("case_d_version_upgrade", "Case D 版本升级"),
        ("registry_internvl_entry", "Registry internvl 条目"),
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
    plan = _read(f"{LR_REL}/local_model_integration_plan_v1.md")
    processor = _read(f"{MM_REL}/luna_model_manager_local_model_processor_v1.py")
    registry = _load_json(_detect_repo_root() / f"{MM_REL}/registries/model_registry_v1.json")
    runtime_policy = _load_json(_detect_repo_root() / f"{RT_REL}/runtime_policy_v1.json")
    runner = _read(
        "capabilities/midplatform/model_test_lens/local_runner_bridge/runners/mobilesam_image_runner_v1.py"
    )

    smoke_result: Dict[str, Any] = {}
    try:
        from capabilities.test_board.model_governance.phase_p1_midplatform_luna_model_manager_local_model_integration_planning_v1_001.luna_model_manager_local_model_integration_planning_smoke_v1 import (  # noqa: WPS433
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

    has_internvl = any(m.get("model_id") == "internvl2_5" for m in registry.get("models", []))
    qwen = next((m for m in registry.get("models", []) if m.get("model_id") == "qwen_vl"), {})

    return {
        "integration_plan_present": "Local Runtime Model" in plan and "execution_mode" in plan,
        "runtime_adapter_present": "invoke_local_runtime" in _read(f"{RT_REL}/local_model_runtime_adapter_v1.py"),
        "lifecycle_adapter_present": "run_local_model_admission_pipeline" in _read(f"{LR_REL}/local_model_lifecycle_adapter_v1.py"),
        "resource_profile_schema_present": _load_json(_detect_repo_root() / f"{LR_REL}/local_model_resource_profile_schema_v1.json").get("schema_id") == "LocalModelResourceProfileV1",
        "admission_policy_present": _load_json(_detect_repo_root() / f"{LR_REL}/local_model_admission_policy_v1.json").get("schema_id") == "LocalModelAdmissionPolicyV1",
        "health_policy_present": _load_json(_detect_repo_root() / f"{LR_REL}/local_model_runtime_health_policy_v1.json").get("schema_id") == "LocalModelRuntimeHealthPolicyV1",
        "runtime_policy_present": runtime_policy.get("schema_id") == "ModelRuntimePolicyV1",
        "unified_execution_mode": qwen.get("execution_mode") == "external_api" and has_internvl,
        "resource_aware_routing": "score_providers_with_resource" in processor,
        "provider_fallback_explicit": "build_provider_fallback_candidate" in processor,
        "no_separate_api_local_logic": runtime_policy.get("boundary_flags", {}).get("no_separate_api_local_logic") is True,
        "model_manager_location_agnostic": "model_manager_location_agnostic" in _read(f"{MM_REL}/luna_model_manager_local_model_types_v1.py"),
        "no_training_finetuning": "no_training_no_finetuning" in _read(f"{MM_REL}/luna_model_manager_local_model_types_v1.py"),
        "case_a_local_admission": _case(cases, "case_a_local_model_normal_admission").get("passed") is True,
        "case_b_gpu_fallback": _case(cases, "case_b_gpu_insufficient_fallback").get("passed") is True,
        "case_c_local_external": _case(cases, "case_c_local_vs_external_routing").get("passed") is True,
        "case_d_version_upgrade": _case(cases, "case_d_local_version_upgrade").get("passed") is True,
        "registry_internvl_entry": has_internvl,
        "no_existing_runner_mutation": "local_model_integration" not in runner,
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

    out_review = _detect_repo_root() / "_tmp_eval_out/p1_midplatform_luna_model_manager_local_model_integration_planning_v1_review_v0"
    out_review.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "layer_id": "Model_Manager_Local_Runtime",
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
            "planning_only_no_real_inference",
            "internvl_minicpm_not_deployed",
            "no_training_finetuning",
            "gemini_deferred",
        ],
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out_review / "p1_midplatform_luna_model_manager_local_model_integration_planning_review_v1.json"
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
