# -*- coding: utf-8 -*-
"""P1 Document Surface Detector — implementation planning review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Implementation-Planning-v1-001"
IP_REL = "capabilities/midplatform/model_manager/runtime/document_surface/implementation_planning"
DS_REL = "capabilities/midplatform/model_manager/runtime/document_surface"
MM_REL = "capabilities/midplatform/model_manager"
TB_REL = (
    "capabilities/test_board/model_governance/"
    "phase_p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_implementation_planning_v1_001"
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
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_LIGHTWEIGHT_VISION_RUNTIME_PLANNING_GO": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_lightweight_vision_runtime_planning_v1_review_v0/"
        "p1_midplatform_luna_model_manager_region_intelligence_ownership_lightweight_vision_runtime_planning_review_v1.json"
    ),
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_REAL_RUNTIME_INTEGRATION_DRYRUN_GO": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_real_runtime_integration_dryrun_v1_review_v0/"
        "p1_midplatform_luna_model_manager_region_intelligence_ownership_real_runtime_integration_dryrun_review_v1.json"
    ),
    "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_ATTENTION_GATED_REGION_INTELLIGENCE_DRYRUN_GO": (
        "_tmp_eval_out/p1_midplatform_luna_situation_understanding_attention_gated_ri_dryrun_v1_review_v0/"
        "p1_midplatform_luna_situation_understanding_attention_gated_ri_dryrun_review_v1.json"
    ),
}

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_IMPLEMENTATION_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_IMPLEMENTATION_PLANNING_BLOCKED"
RECOMMENDED_NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Implementation-DryRun-v1-001"
PARALLEL_NEXT_TRACK = "Phase-P1-Midplatform-Luna-Situation-Understanding-Field-Centric-Object-Role-DryRun-v1-001"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{IP_REL}/document_surface_real_runtime_implementation_plan_v1.md",
    f"{IP_REL}/document_surface_implementation_options_v1.py",
    f"{IP_REL}/document_surface_real_runtime_contract_v1.py",
    f"{IP_REL}/document_surface_real_runtime_failure_modes_v1.py",
    f"{IP_REL}/document_surface_real_runtime_benchmark_plan_v1.py",
    f"{IP_REL}/document_surface_real_runtime_test_image_registry_v1.py",
    f"{IP_REL}/document_surface_real_runtime_admission_policy_v1.json",
    f"{IP_REL}/document_surface_real_runtime_implementation_planning_adapter_v1.py",
    f"{MM_REL}/luna_model_manager_document_surface_detector_real_runtime_implementation_planning_types_v1.py",
    f"{MM_REL}/luna_model_manager_document_surface_detector_real_runtime_implementation_planning_processor_v1.py",
    f"{TB_REL}/luna_model_manager_document_surface_detector_real_runtime_implementation_planning_smoke_v1.py",
    f"{TB_REL}/run_luna_model_manager_document_surface_detector_real_runtime_implementation_planning_smoke_v1.py",
    f"{TB_REL}/review_model_test_lens_luna_model_manager_document_surface_detector_real_runtime_implementation_planning_v1.py",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = tuple(
    {"guard_id": f"{i:02d}", "key": k, "desc": d}
    for i, (k, d) in enumerate([
        ("plan_present", "Implementation Plan"),
        ("options_evaluated", "Option A/B/C/D 评估"),
        ("first_candidate", "first_real_implementation_candidate"),
        ("io_contract", "I/O Contract"),
        ("failure_modes", "Failure Modes"),
        ("benchmark_plan", "Benchmark Plan"),
        ("test_image_registry", "Test Image Registry"),
        ("no_real_model", "无真实模型执行"),
        ("no_segmentation", "无图像分割执行"),
        ("no_ocr", "无 OCR"),
        ("no_vlm", "无 VLM"),
        ("no_layout_parser", "无 layout parser"),
        ("mm_registry_aligned", "Model Manager Registry 对齐"),
        ("ownership_aligned", "Ownership Evidence Package 对齐"),
        ("no_direct_execution", "不直接真实执行"),
        ("case_a_path", "Case A 路径选择"),
        ("case_b_contract", "Case B Contract"),
        ("case_c_failure", "Case C Failure Modes"),
        ("case_d_images", "Case D Test Images"),
        ("case_e_benchmark", "Case E Benchmark"),
        ("case_f_attention", "Case F Attention Gate"),
        ("case_g_vlm", "Case G VLM 限制"),
        ("case_h_block", "Case H 执行阻断"),
        ("upstream_go", "上游 GO"),
        ("smoke_pass", "smoke 通过"),
        ("next_phase_ok", "recommended_next_phase 合理"),
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
    policy = _load_json(repo / f"{IP_REL}/document_surface_real_runtime_admission_policy_v1.json")
    plan = _read(f"{IP_REL}/document_surface_real_runtime_implementation_plan_v1.md")
    registry = _read(f"{DS_REL}/document_surface_detector_model_manager_registry_v1.py")

    smoke_result: Dict[str, Any] = {}
    planning: Dict[str, Any] = {}
    try:
        from capabilities.test_board.model_governance.phase_p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_implementation_planning_v1_001.luna_model_manager_document_surface_detector_real_runtime_implementation_planning_smoke_v1 import (  # noqa: WPS433
            run_smoke_cases,
        )
        from capabilities.midplatform.model_manager.runtime.document_surface.implementation_planning.document_surface_real_runtime_implementation_planning_adapter_v1 import (  # noqa: WPS433
            run_document_surface_implementation_planning,
        )
        smoke_result = run_smoke_cases()
        planning = run_document_surface_implementation_planning(repo_root=repo, write_outputs=True)
    except Exception:
        smoke_result = {"final_decision": FINAL_BLOCKED}

    cases = smoke_result.get("smoke_cases", [])
    upstream_ok = all(
        _load_json(repo / rel).get("final_decision") == go
        for go, rel in UPSTREAM_PATHS.items()
    )

    out_dir = repo / "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_implementation_planning_v1"
    outputs_ok = all(
        (out_dir / f).is_file()
        for f in (
            "implementation_planning_summary.json",
            "implementation_options_review.json",
            "real_runtime_contract_summary.json",
            "failure_modes_registry.json",
            "benchmark_plan_summary.json",
            "test_image_registry_plan.json",
        )
    )

    return {
        "plan_present": "option_a_classical_cv_boundary" in plan,
        "options_evaluated": "option_d_vlm_teacher_assisted" in _read(f"{IP_REL}/document_surface_implementation_options_v1.py"),
        "first_candidate": policy.get("first_real_implementation_candidate") == "option_a_classical_cv_boundary",
        "io_contract": "build_implementation_input_contract" in _read(f"{IP_REL}/document_surface_real_runtime_contract_v1.py"),
        "failure_modes": "FAILURE_MODES" in _read(f"{IP_REL}/document_surface_real_runtime_failure_modes_v1.py"),
        "benchmark_plan": "BENCHMARK_METRICS" in _read(f"{IP_REL}/document_surface_real_runtime_benchmark_plan_v1.py"),
        "test_image_registry": "TEST_IMAGE_CATEGORIES" in _read(f"{IP_REL}/document_surface_real_runtime_test_image_registry_v1.py"),
        "no_real_model": policy.get("real_execution_enabled") is False,
        "no_segmentation": planning.get("no_image_segmentation_execution") is True,
        "no_ocr": planning.get("no_ocr_execution") is True,
        "no_vlm": planning.get("no_vlm_call") is True,
        "no_layout_parser": "no_layout_parser_execution" in (policy.get("negative_guards") or []),
        "mm_registry_aligned": "document_surface_detector_v1" in registry and planning.get("model_manager_registry_aligned"),
        "ownership_aligned": planning.get("contract_aligned") is True,
        "no_direct_execution": policy.get("admission_gates", {}).get("no_direct_real_execution") is True,
        "case_a_path": _case(cases, "case_a_implementation_path_selection").get("passed") is True,
        "case_b_contract": _case(cases, "case_b_contract_alignment").get("passed") is True,
        "case_c_failure": _case(cases, "case_c_failure_modes_coverage").get("passed") is True,
        "case_d_images": _case(cases, "case_d_test_image_registry").get("passed") is True,
        "case_e_benchmark": _case(cases, "case_e_benchmark_metrics").get("passed") is True,
        "case_f_attention": _case(cases, "case_f_attention_gate_constraint").get("passed") is True,
        "case_g_vlm": _case(cases, "case_g_vlm_teacher_restriction").get("passed") is True,
        "case_h_block": _case(cases, "case_h_real_execution_block").get("passed") is True,
        "upstream_go": upstream_ok,
        "smoke_pass": smoke_result.get("final_decision", "").endswith("_GO"),
        "next_phase_ok": planning.get("recommended_next_phase") == RECOMMENDED_NEXT_PHASE and outputs_ok,
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
    out_review = _detect_repo_root() / "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_implementation_planning_v1_review_v0"
    out_review.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "runtime_id": "document_surface_detector_v1",
        "implementation_planning_only": True,
        "first_real_implementation_candidate": "option_a_classical_cv_boundary",
        "recommended_next_phase": RECOMMENDED_NEXT_PHASE if decision == FINAL_GO else None,
        "parallel_next_track": PARALLEL_NEXT_TRACK if decision == FINAL_GO else None,
        "real_execution_enabled": False,
        "audit_flags": flags,
        "negative_guards": guards,
        "negative_guard_passed": sum(1 for g in guards if g["passed"]),
        "smoke_cases_passed": flags.get("smoke_pass", False),
        "blocker_count": len(failed),
        "failed_checks": failed,
        "known_limits": ["implementation_planning_only", "no_real_model", "no_cv2", "no_real_images"],
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out_review / "p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_implementation_planning_review_v1.json"
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
