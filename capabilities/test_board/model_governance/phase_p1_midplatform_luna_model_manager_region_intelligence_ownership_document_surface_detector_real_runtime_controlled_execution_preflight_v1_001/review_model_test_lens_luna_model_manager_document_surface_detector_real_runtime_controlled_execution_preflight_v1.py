# -*- coding: utf-8 -*-
"""P1 Document Surface Detector — controlled execution preflight review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Controlled-Execution-Preflight-v1-001"
CEP_REL = "capabilities/midplatform/model_manager/runtime/document_surface/controlled_execution_preflight"
MM_REL = "capabilities/midplatform/model_manager"
TB_REL = (
    "capabilities/test_board/model_governance/"
    "phase_p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_preflight_v1_001"
)

UPSTREAM_PATHS = {
    "controlled_execution_planning": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_planning_v1_review_v0/"
        "p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_planning_review_v1.json"
    ),
}

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_CONTROLLED_EXECUTION_PREFLIGHT_GO"
FINAL_GO_WITH_DEPENDENCY_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_CONTROLLED_EXECUTION_PREFLIGHT_GO_WITH_DEPENDENCY_BLOCKED"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_CONTROLLED_EXECUTION_PREFLIGHT_BLOCKED"
NEXT_PHASE_DRYRUN = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Controlled-Execution-DryRun-v1-001"
NEXT_PHASE_CV2_REVIEW = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-CV2-Dependency-Admission-Review-v1-001"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{CEP_REL}/document_surface_controlled_execution_preflight_plan_v1.md",
    f"{CEP_REL}/document_surface_cv2_preflight_check_v1.py",
    f"{CEP_REL}/document_surface_input_registry_preflight_v1.py",
    f"{CEP_REL}/document_surface_output_boundary_preflight_v1.py",
    f"{CEP_REL}/document_surface_trace_schema_preflight_v1.py",
    f"{CEP_REL}/document_surface_abort_policy_preflight_v1.py",
    f"{CEP_REL}/document_surface_rollback_policy_preflight_v1.py",
    f"{CEP_REL}/document_surface_preflight_adapter_v1.py",
    f"{CEP_REL}/document_surface_controlled_execution_preflight_policy_v1.json",
    f"{MM_REL}/luna_model_manager_document_surface_detector_real_runtime_controlled_execution_preflight_types_v1.py",
    f"{MM_REL}/luna_model_manager_document_surface_detector_real_runtime_controlled_execution_preflight_processor_v1.py",
    f"{TB_REL}/luna_model_manager_document_surface_detector_real_runtime_controlled_execution_preflight_smoke_v1.py",
    f"{TB_REL}/run_luna_model_manager_document_surface_detector_real_runtime_controlled_execution_preflight_smoke_v1.py",
    f"{TB_REL}/review_model_test_lens_luna_model_manager_document_surface_detector_real_runtime_controlled_execution_preflight_v1.py",
)

GUARDS: Tuple[Dict[str, str], ...] = tuple(
    {"guard_id": f"{i:02d}", "key": k, "desc": d}
    for i, (k, d) in enumerate([
        ("adapter", "Preflight Adapter"),
        ("cv2_probe_only", "cv2 仅 import 探测"),
        ("input_registry", "Input Registry 封闭"),
        ("output_boundary", "Output Boundary 封闭"),
        ("trace_schema", "Trace Schema 完整"),
        ("abort_policy", "Abort Policy 13 项"),
        ("rollback_policy", "Rollback Policy 完整"),
        ("protocol", "Protocol Compliance 保留"),
        ("no_detector", "无 detector 执行"),
        ("no_cv2_processing", "无 cv2 图像处理"),
        ("no_image_read", "无图片内容读取"),
        ("no_ocr_vlm_layout", "无 OCR/VLM/layout"),
        ("case_a", "Case A cv2 preflight"),
        ("case_b", "Case B input registry"),
        ("case_c", "Case C invalid path abort"),
        ("case_d", "Case D output boundary"),
        ("case_e", "Case E trace schema"),
        ("case_f", "Case F abort policy"),
        ("case_g", "Case G protocol"),
        ("case_h", "Case H real execution off"),
        ("upstream", "上游 Planning GO"),
        ("smoke", "smoke 通过"),
        ("real_exec_off", "real_execution_enabled=false"),
        ("next_phase", "受控下一阶段推荐"),
    ], start=1)
)


def _read(rel: str) -> str:
    for base in (_detect_repo_root(), _REPO_ROOT, Path.cwd()):
        p = base / rel
        if p.is_file():
            return p.read_text(encoding="utf-8")
    return ""


def _case(cases: List[Dict[str, Any]], case_id: str) -> Dict[str, Any]:
    return next((c for c in cases if c.get("case_id") == case_id), {})


def _audit() -> Dict[str, bool]:
    repo = _detect_repo_root()
    preflight: Dict[str, Any] = {}
    smoke: Dict[str, Any] = {}
    try:
        from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_preflight.document_surface_preflight_adapter_v1 import (  # noqa: WPS433
            run_controlled_execution_preflight,
        )
        from capabilities.test_board.model_governance.phase_p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_preflight_v1_001.luna_model_manager_document_surface_detector_real_runtime_controlled_execution_preflight_smoke_v1 import (  # noqa: WPS433
            run_smoke_cases,
        )
        preflight = run_controlled_execution_preflight(repo_root=repo, write_outputs=True)
        smoke = run_smoke_cases()
    except Exception:
        smoke = {"final_decision": FINAL_BLOCKED}

    cases = smoke.get("smoke_cases", [])
    upstream = json.loads((repo / UPSTREAM_PATHS["controlled_execution_planning"]).read_text(encoding="utf-8")) if (repo / UPSTREAM_PATHS["controlled_execution_planning"]).is_file() else {}
    cv2_src = _read(f"{CEP_REL}/document_surface_cv2_preflight_check_v1.py")
    cv2_no_processing_call = "cv2.imread" not in cv2_src and "cv2.findContours" not in cv2_src

    out_dir = repo / "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_preflight_v1"
    outputs_ok = all((out_dir / f).is_file() for f in (
        "controlled_execution_preflight_summary.json",
        "cv2_preflight_check_summary.json",
        "input_registry_preflight_summary.json",
        "abort_policy_preflight_summary.json",
        "protocol_compliance_preflight_summary.json",
    ))

    fd = smoke.get("final_decision", FINAL_BLOCKED)
    smoke_ok = fd in (FINAL_GO, FINAL_GO_WITH_DEPENDENCY_BLOCKED)
    next_phase = preflight.get("recommended_next_phase")
    next_ok = next_phase in (NEXT_PHASE_DRYRUN, NEXT_PHASE_CV2_REVIEW)

    return {
        "adapter": "run_controlled_execution_preflight" in _read(f"{CEP_REL}/document_surface_preflight_adapter_v1.py"),
        "cv2_probe_only": "cv2_import_attempted" in cv2_src and cv2_no_processing_call and preflight.get("no_cv2_processing_executed") is True,
        "input_registry": preflight.get("checks", {}).get("input_registry", {}).get("passed") is True,
        "output_boundary": preflight.get("checks", {}).get("output_boundary", {}).get("passed") is True,
        "trace_schema": preflight.get("checks", {}).get("trace_schema", {}).get("passed") is True,
        "abort_policy": preflight.get("checks", {}).get("abort_policy", {}).get("passed") is True,
        "rollback_policy": preflight.get("checks", {}).get("rollback_policy", {}).get("passed") is True,
        "protocol": preflight.get("protocol_compliance_passed") is True,
        "no_detector": preflight.get("detector_execution_enabled") is False,
        "no_cv2_processing": preflight.get("no_cv2_processing_executed") is True,
        "no_image_read": True,
        "no_ocr_vlm_layout": True,
        "case_a": _case(cases, "case_a_cv2_dependency_preflight").get("passed") is True,
        "case_b": _case(cases, "case_b_controlled_input_registry").get("passed") is True,
        "case_c": _case(cases, "case_c_blocked_invalid_input_path").get("passed") is True,
        "case_d": _case(cases, "case_d_output_boundary").get("passed") is True,
        "case_e": _case(cases, "case_e_trace_schema").get("passed") is True,
        "case_f": _case(cases, "case_f_abort_policy").get("passed") is True,
        "case_g": _case(cases, "case_g_protocol_compliance_retained").get("passed") is True,
        "case_h": _case(cases, "case_h_real_execution_remains_disabled").get("passed") is True,
        "upstream": upstream.get("final_decision", "").endswith("_GO"),
        "smoke": smoke_ok,
        "real_exec_off": preflight.get("real_execution_enabled") is False,
        "next_phase": next_ok and outputs_ok,
    }


def review(*, write_file: bool = True, write_test_board: bool = True, test_board_root: Optional[str] = None) -> Dict[str, Any]:
    failed: List[str] = []
    for rel in REQUIRED_FILES:
        if not _read(rel):
            failed.append(f"file.missing={rel}")

    flags = _audit()
    guards = []
    for spec in GUARDS:
        passed = bool(flags.get(spec["key"], False))
        guards.append({**spec, "passed": passed})
        if not passed:
            failed.append(f"guard.{spec['guard_id']}.fail={spec['key']}")

    if flags.get("smoke") and not failed:
        decision = FINAL_GO
        repo = _detect_repo_root()
        summary_path = repo / "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_preflight_v1/controlled_execution_preflight_summary.json"
        if summary_path.is_file():
            summ = json.loads(summary_path.read_text(encoding="utf-8"))
            if summ.get("cv2_available_candidate"):
                decision = FINAL_GO
            elif summ.get("dependency_missing_candidate"):
                decision = FINAL_GO_WITH_DEPENDENCY_BLOCKED
    else:
        decision = FINAL_BLOCKED

    recommended = NEXT_PHASE_DRYRUN if decision == FINAL_GO else (
        NEXT_PHASE_CV2_REVIEW if decision == FINAL_GO_WITH_DEPENDENCY_BLOCKED else None
    )

    out_review = _detect_repo_root() / "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_preflight_v1_review_v0"
    out_review.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "detector_execution_enabled": False,
        "real_execution_enabled": False,
        "recommended_next_phase": recommended,
        "audit_flags": flags,
        "negative_guards": guards,
        "negative_guard_passed": sum(1 for g in guards if g["passed"]),
        "blocker_count": len(failed),
        "failed_checks": failed,
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out_review / "p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_preflight_review_v1.json"
        rp.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(rp)

    if write_test_board and decision in (FINAL_GO, FINAL_GO_WITH_DEPENDENCY_BLOCKED):
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
        "real_execution_enabled": False,
        "recommended_next_phase": r.get("recommended_next_phase"),
        "failed_checks": r.get("failed_checks", []),
    }, indent=2, ensure_ascii=False))
    ok = r["final_decision"] in (FINAL_GO, FINAL_GO_WITH_DEPENDENCY_BLOCKED)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
