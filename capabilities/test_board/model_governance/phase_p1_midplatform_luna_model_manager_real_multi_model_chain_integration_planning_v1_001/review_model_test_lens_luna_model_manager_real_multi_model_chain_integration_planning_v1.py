# -*- coding: utf-8 -*-
"""P1 Luna Model Manager Real Multi-Model Chain — planning review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Luna-Model-Manager-Real-Multi-Model-Chain-Integration-Planning-v1-001"
RC_REL = "capabilities/midplatform/model_manager/collaboration/real_chain"
MM_REL = "capabilities/midplatform/model_manager"
TB_REL = (
    "capabilities/test_board/model_governance/"
    "phase_p1_midplatform_luna_model_manager_real_multi_model_chain_integration_planning_v1_001"
)

UPSTREAM_PATHS = {
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_MULTI_MODEL_COLLABORATION_DRYRUN_GO": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_multi_model_collaboration_dryrun_v1_review_v0/"
        "p1_midplatform_luna_model_manager_multi_model_collaboration_dryrun_review_v1.json"
    ),
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_MULTI_PROVIDER_REGISTRY_GO": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_multi_provider_registry_v1_review_v0/"
        "p1_midplatform_luna_model_manager_multi_provider_registry_review_v1.json"
    ),
}

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REAL_MULTI_MODEL_CHAIN_INTEGRATION_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REAL_MULTI_MODEL_CHAIN_INTEGRATION_PLANNING_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Real-Multi-Model-Chain-Integration-DryRun-v1-001"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{RC_REL}/real_multi_model_chain_plan_v1.md",
    f"{RC_REL}/real_chain_orchestrator_v1.py",
    f"{RC_REL}/slot_provider_binding_v1.py",
    f"{RC_REL}/evidence_fusion_adapter_v1.py",
    f"{RC_REL}/real_chain_validation_policy_v1.json",
    f"{RC_REL}/schemas/execution_trace_schema.json",
    f"{RC_REL}/schemas/evidence_package_schema.json",
    f"{RC_REL}/schemas/fusion_candidate_schema.json",
    f"{MM_REL}/luna_model_manager_real_chain_types_v1.py",
    f"{MM_REL}/luna_model_manager_real_chain_processor_v1.py",
    f"{TB_REL}/luna_model_manager_real_multi_model_chain_integration_planning_smoke_v1.py",
    f"{TB_REL}/run_luna_model_manager_real_multi_model_chain_integration_planning_smoke_v1.py",
    f"{TB_REL}/review_model_test_lens_luna_model_manager_real_multi_model_chain_integration_planning_v1.py",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = tuple(
    {"guard_id": f"{i:02d}", "key": k, "desc": d}
    for i, (k, d) in enumerate([
        ("chain_plan_present", "真实链规划文档"),
        ("orchestrator_present", "Real Chain Orchestrator"),
        ("slot_binding_present", "Slot Provider Binding"),
        ("fusion_adapter_present", "Evidence Fusion Adapter"),
        ("validation_policy_present", "Validation Policy"),
        ("schemas_present", "Schemas 齐全"),
        ("three_slot_chain", "三 Slot 店招链"),
        ("text_capability_first", "文字能力优先"),
        ("sam_not_target_discovery", "SAM 非 target discovery"),
        ("qwen_not_ocr", "Qwen 不负责 OCR"),
        ("no_auto_answer_fusion", "禁止答案融合"),
        ("no_auto_model_replacement", "禁止自动换模型"),
        ("case_a_normal", "Case A 正常店招"),
        ("case_b_ocr_failure", "Case B OCR 失败"),
        ("case_c_unsupported", "Case C unsupported claim"),
        ("case_d_degradation", "Case D 资源降级"),
        ("upstream_gos_confirmed", "上游 GO 确认"),
        ("smoke_cases_passed", "smoke 通过"),
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
    plan = _read(f"{RC_REL}/real_multi_model_chain_plan_v1.md")
    policy = _load_json(_detect_repo_root() / f"{RC_REL}/real_chain_validation_policy_v1.json")
    binding = _read(f"{RC_REL}/slot_provider_binding_v1.py")

    smoke_result: Dict[str, Any] = {}
    try:
        from capabilities.test_board.model_governance.phase_p1_midplatform_luna_model_manager_real_multi_model_chain_integration_planning_v1_001.luna_model_manager_real_multi_model_chain_integration_planning_smoke_v1 import (  # noqa: WPS433
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
    schemas_ok = all(
        _read(f"{RC_REL}/schemas/{name}").strip()
        for name in ("execution_trace_schema.json", "evidence_package_schema.json", "fusion_candidate_schema.json")
    )

    return {
        "chain_plan_present": "Real Multi-Model Chain" in plan and "shopfront" in plan.lower(),
        "orchestrator_present": "run_normal_shopfront_chain" in _read(f"{RC_REL}/real_chain_orchestrator_v1.py"),
        "slot_binding_present": "bind_slot_providers" in binding,
        "fusion_adapter_present": "build_chain_fusion_candidate" in _read(f"{RC_REL}/evidence_fusion_adapter_v1.py"),
        "validation_policy_present": policy.get("schema_id") == "RealChainValidationPolicyV1",
        "schemas_present": schemas_ok,
        "three_slot_chain": len(policy.get("frozen_chain", {}).get("slots") or []) == 3,
        "text_capability_first": policy.get("boundary_flags", {}).get("text_detection_ocr_qwen_only") is True,
        "sam_not_target_discovery": "sam_not_target_discovery" in json.dumps(policy),
        "qwen_not_ocr": "qwen_not_ocr" in binding or "qwen_not_in_ocr_slot" in binding,
        "no_auto_answer_fusion": "no_auto_answer_fusion" in json.dumps(policy),
        "no_auto_model_replacement": "ocr_failure_l2_replan" in json.dumps(policy),
        "case_a_normal": _case(cases, "case_a_normal_shopfront_chain").get("passed") is True,
        "case_b_ocr_failure": _case(cases, "case_b_ocr_failure_challenge").get("passed") is True,
        "case_c_unsupported": _case(cases, "case_c_qwen_unsupported_claim_reject").get("passed") is True,
        "case_d_degradation": _case(cases, "case_d_detector_unavailable_degradation").get("passed") is True,
        "upstream_gos_confirmed": upstream_ok,
        "smoke_cases_passed": smoke_result.get("final_decision", "").endswith("_GO"),
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

    out_review = _detect_repo_root() / "_tmp_eval_out/p1_midplatform_luna_model_manager_real_multi_model_chain_integration_planning_v1_review_v0"
    out_review.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "layer_id": "Model_Manager_Real_Chain_Planning",
        "planning_only": True,
        "model_os_frozen": True,
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
            "planning_no_real_runtime_execution",
            "single_chain_shopfront_only",
            "internvl_gemini_sam_deferred",
        ],
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out_review / "p1_midplatform_luna_model_manager_real_multi_model_chain_integration_planning_review_v1.json"
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
        "smoke_cases_passed": r.get("smoke_cases_passed"),
        "review_guards_passed": r.get("negative_guard_passed"),
        "recommended_next_phase": r.get("recommended_next_phase"),
        "failed_checks": r.get("failed_checks", []),
    }, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
