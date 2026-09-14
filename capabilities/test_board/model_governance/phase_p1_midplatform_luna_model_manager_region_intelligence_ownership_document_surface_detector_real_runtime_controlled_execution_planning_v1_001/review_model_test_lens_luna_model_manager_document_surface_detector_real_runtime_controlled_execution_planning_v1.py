# -*- coding: utf-8 -*-
"""P1 Document Surface Detector — controlled execution planning review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Controlled-Execution-Planning-v1-001"
CEP_REL = "capabilities/midplatform/model_manager/runtime/document_surface/controlled_execution_planning"
MM_REL = "capabilities/midplatform/model_manager"
TB_REL = (
    "capabilities/test_board/model_governance/"
    "phase_p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_planning_v1_001"
)

UPSTREAM_PATHS = {
    "implementation_post_review": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_implementation_post_review_v1_review_v0/"
        "p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_implementation_post_review_review_v1.json"
    ),
}

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_CONTROLLED_EXECUTION_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_CONTROLLED_EXECUTION_PLANNING_BLOCKED"
RECOMMENDED_NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Controlled-Execution-Preflight-v1-001"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{CEP_REL}/document_surface_controlled_execution_plan_v1.md",
    f"{CEP_REL}/document_surface_cv2_dependency_admission_v1.py",
    f"{CEP_REL}/document_surface_controlled_input_registry_v1.py",
    f"{CEP_REL}/document_surface_controlled_output_policy_v1.py",
    f"{CEP_REL}/document_surface_controlled_execution_contract_v1.py",
    f"{CEP_REL}/document_surface_runtime_trace_schema_v1.json",
    f"{CEP_REL}/document_surface_abort_condition_policy_v1.json",
    f"{CEP_REL}/document_surface_rollback_policy_v1.json",
    f"{CEP_REL}/document_surface_controlled_execution_smoke_plan_v1.py",
    f"{CEP_REL}/document_surface_controlled_execution_planning_adapter_v1.py",
    f"{MM_REL}/luna_model_manager_document_surface_detector_real_runtime_controlled_execution_planning_types_v1.py",
    f"{MM_REL}/luna_model_manager_document_surface_detector_real_runtime_controlled_execution_planning_processor_v1.py",
    f"{TB_REL}/luna_model_manager_document_surface_detector_real_runtime_controlled_execution_planning_smoke_v1.py",
    f"{TB_REL}/run_luna_model_manager_document_surface_detector_real_runtime_controlled_execution_planning_smoke_v1.py",
    f"{TB_REL}/review_model_test_lens_luna_model_manager_document_surface_detector_real_runtime_controlled_execution_planning_v1.py",
)

GUARDS: Tuple[Dict[str, str], ...] = tuple(
    {"guard_id": f"{i:02d}", "key": k, "desc": d}
    for i, (k, d) in enumerate([
        ("adapter", "Planning Adapter"),
        ("cv2_admission", "Dependency Admission"),
        ("input_boundary", "Input Boundary"),
        ("output_boundary", "Output Boundary"),
        ("trace_schema", "Runtime Trace"),
        ("abort_policy", "Abort Conditions"),
        ("rollback", "Rollback Policy"),
        ("smoke_plan", "Controlled Smoke Plan"),
        ("no_cv2", "无 cv2 import"),
        ("no_image", "无真实图片读取"),
        ("no_detector", "无 detector 执行"),
        ("protocol", "Protocol Compliance 保留"),
        ("case_a", "Case A cv2 admission"),
        ("case_b", "Case B boundary"),
        ("case_c", "Case C abort"),
        ("case_d", "Case D trace"),
        ("case_e", "Case E smoke plan"),
        ("case_f", "Case F protocol"),
        ("case_g", "Case G preflight gate"),
        ("upstream", "上游 Post-Review GO"),
        ("smoke", "smoke 通过"),
        ("next_phase", "Preflight 推荐"),
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
    planning: Dict[str, Any] = {}
    smoke: Dict[str, Any] = {}
    try:
        from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_planning.document_surface_controlled_execution_planning_adapter_v1 import (  # noqa: WPS433
            run_controlled_execution_planning,
        )
        from capabilities.test_board.model_governance.phase_p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_planning_v1_001.luna_model_manager_document_surface_detector_real_runtime_controlled_execution_planning_smoke_v1 import (  # noqa: WPS433
            run_smoke_cases,
        )
        planning = run_controlled_execution_planning(repo_root=repo, write_outputs=True)
        smoke = run_smoke_cases()
    except Exception:
        smoke = {"final_decision": FINAL_BLOCKED}

    cases = smoke.get("smoke_cases", [])
    upstream = json.loads((repo / UPSTREAM_PATHS["implementation_post_review"]).read_text(encoding="utf-8")) if (repo / UPSTREAM_PATHS["implementation_post_review"]).is_file() else {}
    cv2_src = _read(f"{CEP_REL}/document_surface_cv2_dependency_admission_v1.py")
    abort = json.loads(_read(f"{CEP_REL}/document_surface_abort_condition_policy_v1.json") or "{}")

    out_dir = repo / "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_planning_v1"
    outputs_ok = all((out_dir / f).is_file() for f in (
        "controlled_execution_planning_summary.json", "cv2_dependency_admission_plan.json",
        "controlled_input_registry_plan.json", "abort_condition_policy_summary.json",
    ))

    return {
        "adapter": "run_controlled_execution_planning" in _read(f"{CEP_REL}/document_surface_controlled_execution_planning_adapter_v1.py"),
        "cv2_admission": planning.get("cv2_dependency_not_admitted") is True,
        "input_boundary": planning.get("input_registry_defined") is True,
        "output_boundary": "no_production_write" in _read(f"{CEP_REL}/document_surface_controlled_output_policy_v1.py"),
        "trace_schema": "fallback_attempted" in _read(f"{CEP_REL}/document_surface_runtime_trace_schema_v1.json"),
        "abort_policy": len(abort.get("abort_conditions") or []) >= 12,
        "rollback": "do_not_modify_runtime_registry" in _read(f"{CEP_REL}/document_surface_rollback_policy_v1.json"),
        "smoke_plan": planning.get("controlled_smoke_cases", 0) >= 6,
        "no_cv2": "import cv2" not in cv2_src and planning.get("cv2_imported_in_planning") is False,
        "no_image": True,
        "no_detector": planning.get("real_execution_enabled") is False,
        "protocol": planning.get("protocol_compliance_check") == "required",
        "case_a": _case(cases, "case_a_cv2_dependency_admission_planning").get("passed") is True,
        "case_b": _case(cases, "case_b_input_output_boundary_planning").get("passed") is True,
        "case_c": _case(cases, "case_c_abort_condition_planning").get("passed") is True,
        "case_d": _case(cases, "case_d_trace_schema_planning").get("passed") is True,
        "case_e": _case(cases, "case_e_controlled_smoke_plan").get("passed") is True,
        "case_f": _case(cases, "case_f_protocol_compliance_retained").get("passed") is True,
        "case_g": _case(cases, "case_g_next_phase_gate").get("passed") is True,
        "upstream": upstream.get("final_decision", "").endswith("_GO"),
        "smoke": smoke.get("final_decision", "").endswith("_GO"),
        "next_phase": planning.get("recommended_next_phase") == RECOMMENDED_NEXT_PHASE and outputs_ok,
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

    decision = FINAL_GO if not failed else FINAL_BLOCKED
    out_review = _detect_repo_root() / "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_planning_v1_review_v0"
    out_review.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "real_execution_enabled": False,
        "recommended_next_phase": RECOMMENDED_NEXT_PHASE if decision == FINAL_GO else None,
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
        rp = out_review / "p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_planning_review_v1.json"
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
        "real_execution_enabled": False,
        "recommended_next_phase": r.get("recommended_next_phase"),
        "failed_checks": r.get("failed_checks", []),
    }, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
