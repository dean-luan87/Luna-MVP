# -*- coding: utf-8 -*-
"""P1 Luna Model Manager Lifecycle Sandbox — review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Luna-Model-Manager-Lifecycle-Sandbox-v1-001"
MM_REL = "capabilities/midplatform/model_manager"
LC_REL = f"{MM_REL}/lifecycle"
TB_REL = (
    "capabilities/test_board/model_governance/"
    "phase_p1_midplatform_luna_model_manager_lifecycle_sandbox_v1_001"
)

UPSTREAM_PATHS = {
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_FOUNDATION_DRYRUN_GO": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_foundation_dryrun_v1_review_v0/"
        "p1_midplatform_luna_model_manager_foundation_dryrun_review_v1.json"
    ),
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_FOUNDATION_PLANNING_GO": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_foundation_planning_v1_review_v0/"
        "p1_midplatform_luna_model_manager_foundation_planning_review_v1.json"
    ),
}

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_LIFECYCLE_SANDBOX_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_LIFECYCLE_SANDBOX_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-QwenVL-Real-Provider-Integration-DryRun-v1-001"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{LC_REL}/model_lifecycle_processor_v1.py",
    f"{LC_REL}/model_admission_processor_v1.py",
    f"{LC_REL}/model_registry_state_machine_v1.py",
    f"{LC_REL}/model_benchmark_record_schema_v1.json",
    f"{LC_REL}/model_activation_policy_v1.json",
    f"{LC_REL}/model_deprecation_policy_v1.json",
    f"{LC_REL}/luna_model_manager_lifecycle_sandbox_adapter_v1.py",
    f"{TB_REL}/luna_model_manager_lifecycle_sandbox_fixtures_v1.py",
    f"{TB_REL}/run_luna_model_manager_lifecycle_sandbox_v1.py",
    f"{TB_REL}/review_model_test_lens_luna_model_manager_lifecycle_sandbox_v1.py",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = tuple(
    {"guard_id": f"{i:02d}", "key": k, "desc": d}
    for i, (k, d) in enumerate([
        ("lifecycle_processor_present", "lifecycle processor 存在"),
        ("admission_processor_present", "admission processor 存在"),
        ("state_machine_present", "state machine 存在"),
        ("benchmark_schema_present", "benchmark schema 存在"),
        ("activation_policy_present", "activation policy 存在"),
        ("deprecation_policy_present", "deprecation policy 存在"),
        ("sandbox_adapter_present", "sandbox adapter 存在"),
        ("full_lifecycle_states", "完整生命周期状态机"),
        ("luna_owns_model", "Luna 拥有模型生命周期"),
        ("no_auto_admission", "不自动准入"),
        ("no_auto_activation", "不自动激活"),
        ("preserve_trace_on_deprecation", "退役保留 trace"),
        ("blocked_not_routing", "blocked 不参与路由"),
        ("sandbox_only_no_execution", "sandbox 不执行"),
        ("case_a_new_ocr", "Case A 新 OCR 模型"),
        ("case_b_eval_failed", "Case B 能力不足拒绝"),
        ("case_c_deprecation", "Case C 模型退役"),
        ("case_d_blocked", "Case D 恶意模型 blocked"),
        ("no_production_registry_mutation", "不修改生产 registry"),
        ("no_existing_runner_mutation", "未改 runner"),
        ("sandbox_cases_pass", "sandbox cases 通过"),
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
    lifecycle = _read(f"{LC_REL}/model_lifecycle_processor_v1.py")
    admission = _read(f"{LC_REL}/model_admission_processor_v1.py")
    sm = _read(f"{LC_REL}/model_registry_state_machine_v1.py")
    benchmark = _load_json(_detect_repo_root() / f"{LC_REL}/model_benchmark_record_schema_v1.json")
    activation = _load_json(_detect_repo_root() / f"{LC_REL}/model_activation_policy_v1.json")
    deprecation = _load_json(_detect_repo_root() / f"{LC_REL}/model_deprecation_policy_v1.json")
    adapter = _read(f"{LC_REL}/luna_model_manager_lifecycle_sandbox_adapter_v1.py")
    model_reg = _read(f"{MM_REL}/registries/model_registry_v1.json")
    runner = _read(
        "capabilities/midplatform/model_test_lens/local_runner_bridge/runners/mobilesam_image_runner_v1.py"
    )

    sandbox_result: Dict[str, Any] = {}
    try:
        from capabilities.test_board.model_governance.phase_p1_midplatform_luna_model_manager_lifecycle_sandbox_v1_001.luna_model_manager_lifecycle_sandbox_fixtures_v1 import (  # noqa: WPS433
            run_all_sandbox_cases,
        )
        sandbox_result = run_all_sandbox_cases()
    except Exception:
        sandbox_result = {"final_decision": FINAL_BLOCKED}

    cases = sandbox_result.get("sandbox_cases", [])
    upstream_ok = all(
        _load_json(_detect_repo_root() / rel).get("final_decision") == go
        for go, rel in UPSTREAM_PATHS.items()
    )

    return {
        "lifecycle_processor_present": "run_full_lifecycle_sandbox" in lifecycle,
        "admission_processor_present": "complete_admission" in admission,
        "state_machine_present": "transition_model_state" in sm and "discovered" in sm,
        "benchmark_schema_present": benchmark.get("schema_id") == "ModelBenchmarkRecordV1",
        "activation_policy_present": activation.get("schema_id") == "ModelActivationPolicyV1",
        "deprecation_policy_present": deprecation.get("schema_id") == "ModelDeprecationPolicyV1",
        "sandbox_adapter_present": "run_lifecycle_sandbox_case" in adapter,
        "full_lifecycle_states": all(s in sm for s in ("discovered", "candidate", "evaluating", "active", "deprecated", "blocked")),
        "luna_owns_model": "assert_luna_owns_model" in adapter and "_SANDBOX_REGISTRY" in lifecycle,
        "no_auto_admission": "no_auto_admission" in admission,
        "no_auto_activation": activation.get("boundary_flags", {}).get("no_auto_activation") is True,
        "preserve_trace_on_deprecation": deprecation.get("boundary_flags", {}).get("preserve_trace_on_deprecation") is True,
        "blocked_not_routing": "blocked" in sm and "ROUTING_ELIGIBLE" in sm,
        "sandbox_only_no_execution": "sandbox_only" in lifecycle and "no_auto_execution" in lifecycle,
        "case_a_new_ocr": _case(cases, "case_a_new_ocr_model_lifecycle").get("passed") is True,
        "case_b_eval_failed": _case(cases, "case_b_insufficient_capability_rejected").get("passed") is True,
        "case_c_deprecation": _case(cases, "case_c_ocr_v1_deprecation").get("passed") is True,
        "case_d_blocked": _case(cases, "case_d_malicious_model_blocked").get("passed") is True,
        "no_production_registry_mutation": "vision_teacher_bad" not in model_reg,
        "no_existing_runner_mutation": "lifecycle_sandbox" not in runner,
        "sandbox_cases_pass": sandbox_result.get("final_decision", "").endswith("_GO"),
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

    out_review = _detect_repo_root() / "_tmp_eval_out/p1_midplatform_luna_model_manager_lifecycle_sandbox_v1_review_v0"
    out_review.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "layer_id": "Model_Manager_Lifecycle",
        "sandbox_only": True,
        "recommended_next_phase": NEXT_PHASE,
        "audit_flags": flags,
        "negative_guards": guards,
        "negative_guard_count": len(guards),
        "negative_guard_passed": sum(1 for g in guards if g["passed"]),
        "sandbox_cases_passed": flags.get("sandbox_cases_pass", False),
        "blocker_count": blocker_count,
        "failed_checks": failed,
        "generated_files": generated_files,
        "lifecycle_states": [
            "discovered", "candidate", "evaluating", "admitted", "active", "deprecated", "blocked",
        ],
        "known_limits": [
            "sandbox_only_in_memory_registry",
            "no_real_provider_integration",
            "no_production_registry_mutation",
            "gemini_gpt_deferred_to_real_provider_phase",
        ],
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out_review / "p1_midplatform_luna_model_manager_lifecycle_sandbox_review_v1.json"
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
        "sandbox_cases_passed": r.get("sandbox_cases_passed"),
        "review_guards_passed": r.get("negative_guard_passed"),
        "recommended_next_phase": r.get("recommended_next_phase"),
        "failed_checks": r.get("failed_checks", []),
    }, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
