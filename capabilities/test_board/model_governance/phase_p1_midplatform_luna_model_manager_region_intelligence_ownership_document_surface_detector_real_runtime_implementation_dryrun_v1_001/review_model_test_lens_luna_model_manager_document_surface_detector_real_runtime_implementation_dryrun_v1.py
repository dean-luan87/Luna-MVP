# -*- coding: utf-8 -*-
"""P1 Document Surface Detector — implementation dryrun review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Implementation-DryRun-v1-001"
ID_REL = "capabilities/midplatform/model_manager/runtime/document_surface/implementation_dryrun"
MM_REL = "capabilities/midplatform/model_manager"
TB_REL = (
    "capabilities/test_board/model_governance/"
    "phase_p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_implementation_dryrun_v1_001"
)

UPSTREAM_PATHS = {
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_INTEGRATION_PLANNING_GO": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_integration_planning_v1_review_v0/"
        "p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_integration_planning_review_v1.json"
    ),
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_INTEGRATION_DRYRUN_GO": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_integration_dryrun_v1_review_v0/"
        "p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_integration_dryrun_review_v1.json"
    ),
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_INTEGRATION_POST_REVIEW_GO": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_integration_post_review_v1_review_v0/"
        "p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_integration_post_review_review_v1.json"
    ),
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_IMPLEMENTATION_PLANNING_GO": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_implementation_planning_v1_review_v0/"
        "p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_implementation_planning_review_v1.json"
    ),
}

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_IMPLEMENTATION_DRYRUN_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_IMPLEMENTATION_DRYRUN_BLOCKED"
RECOMMENDED_NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Implementation-Post-Review-v1-001"
PARALLEL_NEXT_TRACK = "Phase-P1-Midplatform-Luna-Situation-Understanding-Field-Centric-Object-Role-DryRun-v1-001"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{ID_REL}/document_surface_option_a_dryrun_policy_v1.json",
    f"{ID_REL}/document_surface_option_a_dryrun_adapter_v1.py",
    f"{ID_REL}/classical_boundary_candidate_pipeline_v1.py",
    f"{ID_REL}/document_surface_option_a_fixture_v1.py",
    f"{ID_REL}/document_surface_option_a_contract_adapter_v1.py",
    f"{ID_REL}/document_surface_option_a_failure_mode_simulator_v1.py",
    f"{ID_REL}/document_surface_option_a_benchmark_dryrun_v1.py",
    f"{ID_REL}/document_surface_protocol_compliance_reviewer_v1.py",
    f"capabilities/midplatform/protocols/region_intelligence_protocol_chain_v1.json",
    f"capabilities/midplatform/protocols/region_intelligence_protocol_patches_v1.json",
    f"capabilities/midplatform/protocols/region_intelligence_protocol_compliance_checker_v1.py",
    f"{MM_REL}/luna_model_manager_document_surface_detector_real_runtime_implementation_dryrun_types_v1.py",
    f"{MM_REL}/luna_model_manager_document_surface_detector_real_runtime_implementation_dryrun_processor_v1.py",
    f"{TB_REL}/luna_model_manager_document_surface_detector_real_runtime_implementation_dryrun_smoke_v1.py",
    f"{TB_REL}/run_luna_model_manager_document_surface_detector_real_runtime_implementation_dryrun_smoke_v1.py",
    f"{TB_REL}/review_model_test_lens_luna_model_manager_document_surface_detector_real_runtime_implementation_dryrun_v1.py",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = tuple(
    {"guard_id": f"{i:02d}", "key": k, "desc": d}
    for i, (k, d) in enumerate([
        ("option_a_adapter", "Option A DryRun Adapter"),
        ("classical_pipeline", "Classical Boundary Pipeline"),
        ("contract_adapter", "Contract Adapter"),
        ("failure_simulator", "Failure Mode Simulator"),
        ("benchmark_dryrun", "Benchmark DryRun"),
        ("no_cv2_import", "未导入 cv2"),
        ("no_real_image", "未读取真实图片"),
        ("no_real_processing", "未执行真实图像处理"),
        ("contract_aligned", "Contract 与 planning 对齐"),
        ("failure_modes_11", "11 failure modes 可模拟"),
        ("benchmark_complete", "Benchmark 指标完整"),
        ("ownership_compat", "Ownership Package 兼容"),
        ("no_ocr_vlm_layout", "无 OCR/VLM/layout 越界"),
        ("attention_zero_call", "Attention blocked zero call"),
        ("candidate_only", "candidate_only/not_fact"),
        ("case_a_flat", "Case A single_flat_paper"),
        ("case_b_overlap", "Case B two_overlapping_papers"),
        ("case_c_folded", "Case C folded_or_curved_paper"),
        ("case_d_receipt", "Case D receipt_attached"),
        ("case_e_screen", "Case E document_on_screen"),
        ("case_f_contrast", "Case F low_contrast"),
        ("case_g_blocked", "Case G attention_blocked"),
        ("case_h_error", "Case H runtime_error"),
        ("upstream_go", "上游 GO"),
        ("smoke_pass", "smoke 通过"),
        ("next_phase_ok", "next phase 不直接真实执行"),
        ("protocol_compliance", "Protocol Compliance Check"),
        ("protocol_chain", "协议治理链对齐"),
        ("protocol_patches", "4 项 Protocol Patch"),
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
    repo = _detect_repo_root()
    policy = _load_json(repo / f"{ID_REL}/document_surface_option_a_dryrun_policy_v1.json")
    pipeline_src = _read(f"{ID_REL}/classical_boundary_candidate_pipeline_v1.py")

    smoke_result: Dict[str, Any] = {}
    full: Dict[str, Any] = {}
    try:
        from capabilities.test_board.model_governance.phase_p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_implementation_dryrun_v1_001.luna_model_manager_document_surface_detector_real_runtime_implementation_dryrun_smoke_v1 import (  # noqa: WPS433
            run_smoke_cases,
        )
        from capabilities.midplatform.model_manager.runtime.document_surface.implementation_dryrun.document_surface_option_a_dryrun_adapter_v1 import (  # noqa: WPS433
            run_full_implementation_dryrun,
        )
        from capabilities.midplatform.model_manager.runtime.document_surface.implementation_dryrun.document_surface_option_a_failure_mode_simulator_v1 import (  # noqa: WPS433
            simulate_all_failure_modes,
        )
        from capabilities.midplatform.model_manager.runtime.document_surface.implementation_dryrun.document_surface_protocol_compliance_reviewer_v1 import (  # noqa: WPS433
            review_implementation_dryrun_protocol_compliance,
        )
        smoke_result = run_smoke_cases()
        full = run_full_implementation_dryrun(repo_root=repo, write_outputs=True)
        failures = simulate_all_failure_modes()
        protocol = review_implementation_dryrun_protocol_compliance(repo_root=repo)
    except Exception:
        smoke_result = {"final_decision": FINAL_BLOCKED}
        failures = {"all_modes_simulated": False}
        protocol = {"all_passed": False}

    cases = smoke_result.get("smoke_cases", [])
    upstream_ok = all(
        _load_json(repo / rel).get("final_decision") == go
        for go, rel in UPSTREAM_PATHS.items()
    )

    out_dir = repo / "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_implementation_dryrun_v1"
    outputs_ok = all(
        (out_dir / f).is_file()
        for f in (
            "implementation_dryrun_summary.json",
            "option_a_contract_dryrun_summary.json",
            "option_a_failure_mode_dryrun_summary.json",
            "option_a_benchmark_dryrun_summary.json",
            "option_a_ownership_package_compatibility_summary.json",
            "option_a_protocol_compliance_summary.json",
        )
    )

    chain = _load_json(repo / "capabilities/midplatform/protocols/region_intelligence_protocol_chain_v1.json")
    patches = _load_json(repo / "capabilities/midplatform/protocols/region_intelligence_protocol_patches_v1.json")

    sample = next((r for r in full.get("dryrun_results", []) if r.get("fixture_ref") == "single_flat_paper"), {})

    return {
        "option_a_adapter": "run_option_a_implementation_dryrun" in _read(f"{ID_REL}/document_surface_option_a_dryrun_adapter_v1.py"),
        "classical_pipeline": "run_classical_boundary_candidate_pipeline" in pipeline_src,
        "contract_adapter": "adapt_option_a_contract" in _read(f"{ID_REL}/document_surface_option_a_contract_adapter_v1.py"),
        "failure_simulator": "simulate_all_failure_modes" in _read(f"{ID_REL}/document_surface_option_a_failure_mode_simulator_v1.py"),
        "benchmark_dryrun": "compute_benchmark_dryrun_metrics" in _read(f"{ID_REL}/document_surface_option_a_benchmark_dryrun_v1.py"),
        "no_cv2_import": "import cv2" not in pipeline_src and "CV2_IMPORTED = False" in pipeline_src,
        "no_real_image": sample.get("no_real_image_read") is True,
        "no_real_processing": sample.get("no_cv2_import") is True,
        "contract_aligned": (sample.get("contract_check") or {}).get("contract_usable") is True,
        "failure_modes_11": failures.get("all_modes_simulated") is True,
        "benchmark_complete": full.get("benchmark_targets_met") is True,
        "ownership_compat": full.get("ownership_summary", {}).get("surface_before_text_owner") is True,
        "no_ocr_vlm_layout": sample.get("no_ocr_text") is True and "no_vlm_call" in (policy.get("negative_guards") or []),
        "attention_zero_call": (full.get("attention_blocked_result") or {}).get("runtime_call_count") == 0,
        "candidate_only": sample.get("candidate_only") is True and sample.get("not_fact") is True,
        "case_a_flat": _case(cases, "case_a_single_flat_paper").get("passed") is True,
        "case_b_overlap": _case(cases, "case_b_two_overlapping_papers").get("passed") is True,
        "case_c_folded": _case(cases, "case_c_folded_or_curved_paper").get("passed") is True,
        "case_d_receipt": _case(cases, "case_d_receipt_attached_to_package").get("passed") is True,
        "case_e_screen": _case(cases, "case_e_document_on_screen").get("passed") is True,
        "case_f_contrast": _case(cases, "case_f_low_contrast_paper_on_desk").get("passed") is True,
        "case_g_blocked": _case(cases, "case_g_attention_blocked").get("passed") is True,
        "case_h_error": _case(cases, "case_h_runtime_error").get("passed") is True,
        "upstream_go": upstream_ok,
        "smoke_pass": smoke_result.get("final_decision", "").endswith("_GO"),
        "next_phase_ok": full.get("recommended_next_phase") == RECOMMENDED_NEXT_PHASE and outputs_ok,
        "protocol_compliance": protocol.get("all_passed") is True and full.get("protocol_compliance_passed") is True,
        "protocol_chain": bool(chain.get("governance_chain")),
        "protocol_patches": len(patches.get("patches") or []) >= 4,
    }


def review(*, write_file: bool = True, write_test_board: bool = True, test_board_root: Optional[str] = None) -> Dict[str, Any]:
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
    out_review = _detect_repo_root() / "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_implementation_dryrun_v1_review_v0"
    out_review.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "runtime_id": "document_surface_detector_v1",
        "implementation_mode_candidate": "classical_cv_boundary_v1",
        "implementation_dryrun_only": True,
        "recommended_next_phase": RECOMMENDED_NEXT_PHASE if decision == FINAL_GO else None,
        "parallel_next_track": PARALLEL_NEXT_TRACK if decision == FINAL_GO else None,
        "audit_flags": flags,
        "negative_guards": guards,
        "negative_guard_passed": sum(1 for g in guards if g["passed"]),
        "smoke_cases_passed": flags.get("smoke_pass", False),
        "blocker_count": len(failed),
        "failed_checks": failed,
        "known_limits": ["implementation_dryrun_only", "no_cv2", "no_real_images"],
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out_review / "p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_implementation_dryrun_review_v1.json"
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
        "smoke_cases_passed": r.get("smoke_cases_passed"),
        "review_guards_passed": r.get("negative_guard_passed"),
        "recommended_next_phase": r.get("recommended_next_phase"),
        "parallel_next_track": r.get("parallel_next_track"),
        "failed_checks": r.get("failed_checks", []),
    }, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
