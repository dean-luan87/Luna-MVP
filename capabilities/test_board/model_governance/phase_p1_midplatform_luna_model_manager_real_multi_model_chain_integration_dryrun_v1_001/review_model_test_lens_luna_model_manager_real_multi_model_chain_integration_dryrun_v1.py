# -*- coding: utf-8 -*-
"""P1 Luna Model Manager Real Multi-Model Chain — dryrun review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Luna-Model-Manager-Real-Multi-Model-Chain-Integration-DryRun-v1-001"
DRYRUN_REL = "capabilities/midplatform/model_manager/collaboration/real_chain/dryrun"
TB_REL = (
    "capabilities/test_board/model_governance/"
    "phase_p1_midplatform_luna_model_manager_real_multi_model_chain_integration_dryrun_v1_001"
)

UPSTREAM_PATHS = {
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REAL_MULTI_MODEL_CHAIN_INTEGRATION_PLANNING_GO": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_real_multi_model_chain_integration_planning_v1_review_v0/"
        "p1_midplatform_luna_model_manager_real_multi_model_chain_integration_planning_review_v1.json"
    ),
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_MULTI_MODEL_COLLABORATION_DRYRUN_GO": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_multi_model_collaboration_dryrun_v1_review_v0/"
        "p1_midplatform_luna_model_manager_multi_model_collaboration_dryrun_review_v1.json"
    ),
}

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REAL_MULTI_MODEL_CHAIN_INTEGRATION_DRYRUN_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REAL_MULTI_MODEL_CHAIN_INTEGRATION_DRYRUN_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Real-Runtime-Integration-Planning-v1-001"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{DRYRUN_REL}/real_chain_dryrun_adapter_v1.py",
    f"{DRYRUN_REL}/slot_execution_simulator_v1.py",
    f"{DRYRUN_REL}/provider_binding_dryrun_v1.py",
    f"{DRYRUN_REL}/evidence_package_builder_v1.py",
    f"{DRYRUN_REL}/fusion_validation_adapter_v1.py",
    f"{DRYRUN_REL}/execution_trace_graph_v1.py",
    f"{DRYRUN_REL}/real_chain_dryrun_policy_v1.json",
    f"{TB_REL}/luna_model_manager_real_multi_model_chain_integration_dryrun_fixtures_v1.py",
    f"{TB_REL}/run_luna_model_manager_real_multi_model_chain_integration_dryrun_v1.py",
    f"{TB_REL}/review_model_test_lens_luna_model_manager_real_multi_model_chain_integration_dryrun_v1.py",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = tuple(
    {"guard_id": f"{i:02d}", "key": k, "desc": d}
    for i, (k, d) in enumerate([
        ("dryrun_adapter_present", "dryrun adapter"),
        ("slot_simulator_present", "slot simulator"),
        ("binding_dryrun_present", "provider binding dryrun"),
        ("evidence_builder_present", "evidence package builder"),
        ("fusion_validation_present", "fusion validation adapter"),
        ("trace_graph_present", "Execution Trace Graph"),
        ("dryrun_policy_present", "dryrun policy"),
        ("slot_driven_orchestration", "Slot 驱动编排"),
        ("execution_trace_graph_flag", "trace graph 标志"),
        ("no_real_inference", "无真实推理"),
        ("case_a_shopfront", "Case A 标准店招"),
        ("case_b_upgrade", "Case B Provider 升级"),
        ("case_c_ocr_fail", "Case C OCR 失败"),
        ("case_d_context", "Case D Context Challenge"),
        ("case_e_conflict", "Case E Evidence Conflict"),
        ("case_f_trace", "Case F 完整 Trace"),
        ("upstream_gos_confirmed", "上游 GO"),
        ("dryrun_cases_pass", "dryrun 通过"),
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
    policy = _load_json(_detect_repo_root() / f"{DRYRUN_REL}/real_chain_dryrun_policy_v1.json")
    adapter = _read(f"{DRYRUN_REL}/real_chain_dryrun_adapter_v1.py")

    dryrun_result: Dict[str, Any] = {}
    try:
        from capabilities.test_board.model_governance.phase_p1_midplatform_luna_model_manager_real_multi_model_chain_integration_dryrun_v1_001.luna_model_manager_real_multi_model_chain_integration_dryrun_fixtures_v1 import (  # noqa: WPS433
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

    return {
        "dryrun_adapter_present": "run_standard_shopfront_dryrun" in adapter,
        "slot_simulator_present": "simulate_slot_execution" in _read(f"{DRYRUN_REL}/slot_execution_simulator_v1.py"),
        "binding_dryrun_present": "bind_providers_for_dryrun" in _read(f"{DRYRUN_REL}/provider_binding_dryrun_v1.py"),
        "evidence_builder_present": "build_packages_from_executions" in _read(f"{DRYRUN_REL}/evidence_package_builder_v1.py"),
        "fusion_validation_present": "run_fusion_and_validation" in _read(f"{DRYRUN_REL}/fusion_validation_adapter_v1.py"),
        "trace_graph_present": "build_execution_trace_graph" in _read(f"{DRYRUN_REL}/execution_trace_graph_v1.py"),
        "dryrun_policy_present": policy.get("schema_id") == "RealChainDryrunPolicyV1",
        "slot_driven_orchestration": policy.get("boundary_flags", {}).get("collaboration_slot_driven") is True,
        "execution_trace_graph_flag": policy.get("boundary_flags", {}).get("execution_trace_graph") is True,
        "no_real_inference": policy.get("boundary_flags", {}).get("dryrun_no_real_inference") is True,
        "case_a_shopfront": _case(cases, "case_a_standard_shopfront_chain").get("passed") is True,
        "case_b_upgrade": _case(cases, "case_b_slot_provider_upgrade").get("passed") is True,
        "case_c_ocr_fail": _case(cases, "case_c_ocr_failure_chain").get("passed") is True,
        "case_d_context": _case(cases, "case_d_context_challenge").get("passed") is True,
        "case_e_conflict": _case(cases, "case_e_evidence_conflict").get("passed") is True,
        "case_f_trace": _case(cases, "case_f_full_execution_trace").get("passed") is True,
        "upstream_gos_confirmed": upstream_ok,
        "dryrun_cases_pass": dryrun_result.get("final_decision", "").endswith("_GO"),
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

    decision = FINAL_GO if not failed else FINAL_BLOCKED
    out_review = _detect_repo_root() / "_tmp_eval_out/p1_midplatform_luna_model_manager_real_multi_model_chain_integration_dryrun_v1_review_v0"
    out_review.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "layer_id": "Model_Manager_Real_Chain_DryRun",
        "dryrun_only": True,
        "recommended_next_phase": NEXT_PHASE,
        "audit_flags": flags,
        "negative_guards": guards,
        "negative_guard_passed": sum(1 for g in guards if g["passed"]),
        "dryrun_cases_passed": flags.get("dryrun_cases_pass", False),
        "blocker_count": len(failed),
        "failed_checks": failed,
        "known_limits": [
            "deterministic_fixtures_only",
            "no_real_detector_ocr_qwen",
            "real_runtime_deferred",
        ],
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out_review / "p1_midplatform_luna_model_manager_real_multi_model_chain_integration_dryrun_review_v1.json"
        rp.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(rp)

    if write_test_board and decision == FINAL_GO:
        root = Path(test_board_root or str(_detect_repo_root()))
        try:
            tb = write_test_board_records(result, test_mode="dry_run", repo_root=root, module="model_governance", source_review_file=result.get("output_review_file"))
        except (OSError, PermissionError, TypeError):
            standin = _detect_repo_root() / "_tmp_eval_out" / "board_standin"
            standin.mkdir(parents=True, exist_ok=True)
            tb = write_test_board_records(result, test_mode="dry_run", repo_root=standin, module="model_governance", source_review_file=result.get("output_review_file"))
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
