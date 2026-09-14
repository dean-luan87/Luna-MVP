# -*- coding: utf-8 -*-
"""P1 Document Surface Detector — real runtime integration planning review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Integration-Planning-v1-001"
DS_REL = "capabilities/midplatform/model_manager/runtime/document_surface"
MM_REL = "capabilities/midplatform/model_manager"
TB_REL = (
    "capabilities/test_board/model_governance/"
    "phase_p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_integration_planning_v1_001"
)

UPSTREAM_PATHS = {
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_LIGHTWEIGHT_VISION_RUNTIME_PLANNING_GO": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_lightweight_vision_runtime_planning_v1_review_v0/"
        "p1_midplatform_luna_model_manager_region_intelligence_ownership_lightweight_vision_runtime_planning_review_v1.json"
    ),
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_REAL_RUNTIME_INTEGRATION_DRYRUN_GO": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_real_runtime_integration_dryrun_v1_review_v0/"
        "p1_midplatform_luna_model_manager_region_intelligence_ownership_real_runtime_integration_dryrun_review_v1.json"
    ),
}

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_INTEGRATION_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_INTEGRATION_PLANNING_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Integration-DryRun-v1-001"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{DS_REL}/document_surface_detector_runtime_plan_v1.md",
    f"{DS_REL}/document_surface_detector_types_v1.py",
    f"{DS_REL}/document_surface_detector_request_builder_v1.py",
    f"{DS_REL}/document_surface_detector_response_parser_v1.py",
    f"{DS_REL}/document_surface_detector_evidence_normalizer_v1.py",
    f"{DS_REL}/document_surface_detector_runtime_policy_v1.json",
    f"{DS_REL}/document_surface_detector_model_manager_registry_v1.py",
    f"{DS_REL}/document_surface_planning_adapter_v1.py",
    f"{DS_REL}/schemas/document_surface_candidate_schema_v1.json",
    f"{DS_REL}/schemas/document_surface_runtime_request_schema_v1.json",
    f"{DS_REL}/schemas/document_surface_runtime_response_schema_v1.json",
    f"{DS_REL}/schemas/document_surface_evidence_package_schema_v1.json",
    f"{MM_REL}/luna_model_manager_document_surface_detector_real_runtime_planning_types_v1.py",
    f"{MM_REL}/luna_model_manager_document_surface_detector_real_runtime_planning_processor_v1.py",
    f"{TB_REL}/luna_model_manager_document_surface_detector_real_runtime_planning_smoke_v1.py",
    f"{TB_REL}/run_luna_model_manager_document_surface_detector_real_runtime_planning_smoke_v1.py",
    f"{TB_REL}/review_model_test_lens_luna_model_manager_document_surface_detector_real_runtime_planning_v1.py",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = tuple(
    {"guard_id": f"{i:02d}", "key": k, "desc": d}
    for i, (k, d) in enumerate([
        ("plan_present", "Document Surface 规划"),
        ("request_builder", "Request Builder"),
        ("response_parser", "Response Parser"),
        ("evidence_normalizer", "Evidence Normalizer"),
        ("mm_registry", "Model Manager Registry"),
        ("adapter", "Planning Adapter"),
        ("schemas", "JSON Schemas"),
        ("policy", "Runtime Policy"),
        ("no_real_model", "无真实模型执行"),
        ("no_ocr_execution", "无 OCR 执行"),
        ("no_ocr_text_output", "no_ocr_text_output"),
        ("attention_gate_required", "attention_gate_required"),
        ("candidate_only_not_fact", "candidate_only_not_fact"),
        ("mm_registry_entry", "registry 含 document_surface_detector_v1"),
        ("case_a_papers", "Case A 叠放纸张"),
        ("case_b_menus", "Case B 菜单叠放"),
        ("case_c_receipt", "Case C 票据附着"),
        ("case_d_blocked", "Case D Attention Blocked"),
        ("case_e_uncertain", "Case E 边界不清晰"),
        ("case_f_runtime", "Case F Runtime 故障"),
        ("case_g_conflict", "Case G Layout 冲突"),
        ("case_h_screen", "Case H 屏幕文档混淆"),
        ("upstream_go", "上游 GO"),
        ("smoke_pass", "smoke 通过"),
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
    plan = _read(f"{DS_REL}/document_surface_detector_runtime_plan_v1.md")
    policy = _load_json(_detect_repo_root() / f"{DS_REL}/document_surface_detector_runtime_policy_v1.json")
    registry = _read(f"{DS_REL}/document_surface_detector_model_manager_registry_v1.py")

    smoke_result: Dict[str, Any] = {}
    sample: Dict[str, Any] = {}
    try:
        from capabilities.test_board.model_governance.phase_p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_integration_planning_v1_001.luna_model_manager_document_surface_detector_real_runtime_planning_smoke_v1 import (  # noqa: WPS433
            run_smoke_cases,
        )
        from capabilities.midplatform.model_manager.runtime.document_surface.document_surface_planning_adapter_v1 import (  # noqa: WPS433
            run_document_surface_detector_planning,
        )
        smoke_result = run_smoke_cases()
        sample = run_document_surface_detector_planning(fixture_ref="stacked_papers")
    except Exception:
        smoke_result = {"final_decision": FINAL_BLOCKED}

    cases = smoke_result.get("smoke_cases", [])
    upstream_ok = all(
        _load_json(_detect_repo_root() / rel).get("final_decision") == go
        for go, rel in UPSTREAM_PATHS.items()
    )

    schemas_ok = all(
        _read(f"{DS_REL}/schemas/{name}").strip()
        for name in (
            "document_surface_candidate_schema_v1.json",
            "document_surface_runtime_request_schema_v1.json",
            "document_surface_runtime_response_schema_v1.json",
            "document_surface_evidence_package_schema_v1.json",
        )
    )

    return {
        "plan_present": "document_surface_detector_v1" in plan,
        "request_builder": "build_document_surface_request" in _read(f"{DS_REL}/document_surface_detector_request_builder_v1.py"),
        "response_parser": "parse_document_surface_response" in _read(f"{DS_REL}/document_surface_detector_response_parser_v1.py"),
        "evidence_normalizer": "normalize_document_surface_evidence" in _read(f"{DS_REL}/document_surface_detector_evidence_normalizer_v1.py"),
        "mm_registry": "DOCUMENT_SURFACE_RUNTIME_REGISTRY" in registry,
        "adapter": "run_document_surface_detector_planning" in _read(f"{DS_REL}/document_surface_planning_adapter_v1.py"),
        "schemas": schemas_ok,
        "policy": policy.get("schema_id") == "DocumentSurfaceDetectorRuntimePolicyV1",
        "no_real_model": policy.get("boundary_flags", {}).get("no_real_model_execution") is True,
        "no_ocr_execution": policy.get("boundary_flags", {}).get("no_ocr_execution") is True,
        "no_ocr_text_output": sample.get("no_ocr_text_output") is True,
        "attention_gate_required": sample.get("attention_gate_required") is True,
        "candidate_only_not_fact": sample.get("candidate_only") is True and sample.get("not_fact") is True,
        "mm_registry_entry": "document_surface_detector_v1" in registry,
        "case_a_papers": _case(cases, "case_a_stacked_papers_occlusion").get("passed") is True,
        "case_b_menus": _case(cases, "case_b_stacked_menus_no_ocr").get("passed") is True,
        "case_c_receipt": _case(cases, "case_c_receipt_attached_to_package").get("passed") is True,
        "case_d_blocked": _case(cases, "case_d_attention_blocked_skip").get("passed") is True,
        "case_e_uncertain": _case(cases, "case_e_uncertain_boundary").get("passed") is True,
        "case_f_runtime": _case(cases, "case_f_runtime_unavailable").get("passed") is True,
        "case_g_conflict": _case(cases, "case_g_layout_detector_conflict").get("passed") is True,
        "case_h_screen": _case(cases, "case_h_screen_document_confusion").get("passed") is True,
        "upstream_go": upstream_ok,
        "smoke_pass": smoke_result.get("final_decision", "").endswith("_GO"),
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
    out_review = _detect_repo_root() / "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_integration_planning_v1_review_v0"
    out_review.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "runtime_id": "document_surface_detector_v1",
        "planning_only": True,
        "first_real_lightweight_runtime": True,
        "recommended_next_phase": NEXT_PHASE,
        "audit_flags": flags,
        "negative_guards": guards,
        "negative_guard_passed": sum(1 for g in guards if g["passed"]),
        "smoke_cases_passed": flags.get("smoke_pass", False),
        "blocker_count": len(failed),
        "failed_checks": failed,
        "known_limits": ["planning_fixture_only", "no_real_segmentation", "no_ocr"],
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out_review / "p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_integration_planning_review_v1.json"
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
        "failed_checks": r.get("failed_checks", []),
    }, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
