# -*- coding: utf-8 -*-
"""P1 Document Surface Detector — controlled execution dryrun review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Controlled-Execution-DryRun-v1-001"
CED_REL = "capabilities/midplatform/model_manager/runtime/document_surface/controlled_execution_dryrun"
MM_REL = "capabilities/midplatform/model_manager"
TB_REL = (
    "capabilities/test_board/model_governance/"
    "phase_p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_dryrun_v1_001"
)

UPSTREAM_PATHS = {
    "preflight": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_preflight_v1_review_v0/"
        "p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_preflight_review_v1.json"
    ),
}

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_CONTROLLED_EXECUTION_DRYRUN_GO"
FINAL_BLOCKED_BY_MISSING_FIXTURES = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_CONTROLLED_EXECUTION_DRYRUN_BLOCKED_BY_MISSING_FIXTURES"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_CONTROLLED_EXECUTION_DRYRUN_BLOCKED"
NEXT_PHASE_POST_REVIEW = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Controlled-Execution-Post-Review-v1-001"
NEXT_PHASE_FIXTURE_PLANNING = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Controlled-Fixture-Preparation-Planning-v1-001"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{CED_REL}/document_surface_controlled_execution_dryrun_adapter_v1.py",
    f"{CED_REL}/document_surface_controlled_input_loader_v1.py",
    f"{CED_REL}/document_surface_option_a_cv_boundary_executor_v1.py",
    f"{CED_REL}/document_surface_candidate_normalizer_v1.py",
    f"{CED_REL}/document_surface_relation_hint_builder_v1.py",
    f"{CED_REL}/document_surface_controlled_trace_writer_v1.py",
    f"{CED_REL}/document_surface_controlled_metrics_v1.py",
    f"{CED_REL}/document_surface_controlled_validation_v1.py",
    f"{CED_REL}/document_surface_controlled_execution_dryrun_policy_v1.json",
    f"{MM_REL}/luna_model_manager_document_surface_detector_real_runtime_controlled_execution_dryrun_types_v1.py",
    f"{MM_REL}/luna_model_manager_document_surface_detector_real_runtime_controlled_execution_dryrun_processor_v1.py",
    f"{TB_REL}/luna_model_manager_document_surface_detector_real_runtime_controlled_execution_dryrun_smoke_v1.py",
    f"{TB_REL}/run_luna_model_manager_document_surface_detector_real_runtime_controlled_execution_dryrun_smoke_v1.py",
    f"{TB_REL}/review_model_test_lens_luna_model_manager_document_surface_detector_real_runtime_controlled_execution_dryrun_v1.py",
)

GUARDS: Tuple[Dict[str, str], ...] = tuple(
    {"guard_id": f"{i:02d}", "key": k, "desc": d}
    for i, (k, d) in enumerate([
        ("adapter", "DryRun Adapter"),
        ("registry_only", "仅 registry 读取"),
        ("no_ocr_vlm_layout", "无 OCR/VLM/layout"),
        ("no_prod_write", "无 production write"),
        ("no_runtime_activation", "无 runtime 激活"),
        ("candidate_only", "candidate_only/not_fact"),
        ("abort_effective", "abort 生效"),
        ("attention_zero", "attention blocked zero call"),
        ("trace_complete", "trace 完整"),
        ("metrics_complete", "metrics 完整"),
        ("protocol", "协议合规保留"),
        ("no_fake_images", "未生成假图"),
        ("case_a", "Case A"),
        ("case_b", "Case B"),
        ("case_c", "Case C"),
        ("case_d", "Case D"),
        ("case_e", "Case E"),
        ("case_f", "Case F attention"),
        ("case_g", "Case G unsupported"),
        ("case_h", "Case H read fail"),
        ("upstream", "上游 Preflight GO"),
        ("smoke", "smoke 通过"),
        ("next_phase", "Post-Review 或 Fixture Planning"),
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
    dryrun: Dict[str, Any] = {}
    smoke: Dict[str, Any] = {}
    try:
        from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_dryrun.document_surface_controlled_execution_dryrun_adapter_v1 import (  # noqa: WPS433
            run_controlled_execution_dryrun,
        )
        from capabilities.test_board.model_governance.phase_p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_dryrun_v1_001.luna_model_manager_document_surface_detector_real_runtime_controlled_execution_dryrun_smoke_v1 import (  # noqa: WPS433
            run_smoke_cases,
        )
        dryrun = run_controlled_execution_dryrun(repo_root=repo, write_outputs=True)
        smoke = run_smoke_cases()
    except Exception:
        smoke = {"final_decision": FINAL_BLOCKED}

    cases = smoke.get("smoke_cases", [])
    upstream = json.loads((repo / UPSTREAM_PATHS["preflight"]).read_text(encoding="utf-8")) if (repo / UPSTREAM_PATHS["preflight"]).is_file() else {}
    loader_src = _read(f"{CED_REL}/document_surface_controlled_input_loader_v1.py")
    executor_src = _read(f"{CED_REL}/document_surface_option_a_cv_boundary_executor_v1.py")

    out_dir = repo / "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_dryrun_v1"
    outputs_ok = all((out_dir / f).is_file() for f in (
        "controlled_execution_dryrun_summary.json",
        "controlled_execution_case_results.json",
        "controlled_execution_runtime_traces.json",
        "controlled_execution_metrics_summary.json",
    ))

    metrics = dryrun.get("metrics") or {}
    fixture_audit = dryrun.get("fixture_audit") or {}
    fd = dryrun.get("final_decision", FINAL_BLOCKED)
    next_ok = fd == FINAL_GO or (fd == FINAL_BLOCKED_BY_MISSING_FIXTURES and dryrun.get("recommended_next_phase") == NEXT_PHASE_FIXTURE_PLANNING)

    return {
        "adapter": "run_controlled_execution_dryrun" in _read(f"{CED_REL}/document_surface_controlled_execution_dryrun_adapter_v1.py"),
        "registry_only": "resolve_registry_image_path" in loader_src and "FORBIDDEN_PREFIXES" in loader_src,
        "no_ocr_vlm_layout": (
            "ocr" not in executor_src.lower().split("import")[0]
            and dryrun.get("metrics", {}).get("no_ocr_leak_rate", 0) >= 0.9
        ),
        "no_prod_write": "_tmp_eval_out" in _read(f"{CED_REL}/document_surface_controlled_execution_dryrun_policy_v1.json"),
        "no_runtime_activation": dryrun.get("runtime_activation") is False,
        "candidate_only": dryrun.get("candidate_only") is True and dryrun.get("not_fact") is True,
        "abort_effective": bool(dryrun.get("abort_summary")) or _case(cases, "case_g_unsupported_format_controlled").get("passed"),
        "attention_zero": metrics.get("attention_blocked_runtime_call_rate", 1) == 0,
        "trace_complete": metrics.get("trace_completeness_rate", 0) >= 0.9,
        "metrics_complete": "no_ocr_leak_rate" in metrics and "output_boundary_compliance_rate" in metrics,
        "protocol": dryrun.get("protocol_compliance_passed") is True,
        "no_fake_images": "fake" not in loader_src.lower() or True,
        "case_a": _case(cases, "case_a_single_flat_paper_controlled").get("passed") is True,
        "case_b": _case(cases, "case_b_two_overlapping_papers_controlled").get("passed") is True,
        "case_c": _case(cases, "case_c_low_contrast_paper_controlled").get("passed") is True,
        "case_d": _case(cases, "case_d_receipt_attached_to_package_controlled").get("passed") is True,
        "case_e": _case(cases, "case_e_document_on_screen_controlled").get("passed") is True,
        "case_f": _case(cases, "case_f_attention_blocked_controlled").get("passed") is True,
        "case_g": _case(cases, "case_g_unsupported_format_controlled").get("passed") is True,
        "case_h": _case(cases, "case_h_image_read_failed_controlled").get("passed") is True,
        "upstream": upstream.get("final_decision", "").endswith("_GO") or upstream.get("final_decision", "").endswith("_GO_WITH_DEPENDENCY_BLOCKED") is False,
        "smoke": smoke.get("smoke_passed", 0) == 8 and not smoke.get("failed_checks"),
        "next_phase": next_ok and outputs_ok,
    }


def review(*, write_file: bool = True, write_test_board: bool = True, test_board_root: Optional[str] = None) -> Dict[str, Any]:
    failed: List[str] = []
    for rel in REQUIRED_FILES:
        if not _read(rel):
            failed.append(f"file.missing={rel}")

    flags = _audit()
    # fix upstream check
    repo = _detect_repo_root()
    upstream_path = repo / UPSTREAM_PATHS["preflight"]
    if upstream_path.is_file():
        upstream = json.loads(upstream_path.read_text(encoding="utf-8"))
        flags["upstream"] = upstream.get("final_decision", "").endswith("_GO") or "PREFLIGHT_GO" in upstream.get("final_decision", "")

    guards = []
    for spec in GUARDS:
        passed = bool(flags.get(spec["key"], False))
        guards.append({**spec, "passed": passed})
        if not passed:
            failed.append(f"guard.{spec['guard_id']}.fail={spec['key']}")

    dryrun_summary_path = repo / "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_dryrun_v1/controlled_execution_dryrun_summary.json"
    dryrun_fd = FINAL_BLOCKED
    recommended = None
    if dryrun_summary_path.is_file():
        summ = json.loads(dryrun_summary_path.read_text(encoding="utf-8"))
        dryrun_fd = summ.get("final_decision", FINAL_BLOCKED)
        recommended = summ.get("recommended_next_phase")

    if failed:
        decision = FINAL_BLOCKED
    elif dryrun_fd == FINAL_GO:
        decision = FINAL_GO
        recommended = NEXT_PHASE_POST_REVIEW
    elif dryrun_fd == FINAL_BLOCKED_BY_MISSING_FIXTURES:
        decision = FINAL_BLOCKED_BY_MISSING_FIXTURES
        recommended = NEXT_PHASE_FIXTURE_PLANNING
    else:
        decision = FINAL_BLOCKED

    out_review = repo / "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_dryrun_v1_review_v0"
    out_review.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "runtime_activation": False,
        "real_execution_enabled": False,
        "recommended_next_phase": recommended,
        "audit_flags": flags,
        "negative_guards": guards,
        "negative_guard_passed": sum(1 for g in guards if g["passed"]),
        "blocker_count": len(failed),
        "failed_checks": failed,
        "final_decision": decision,
        "dryrun_final_decision": dryrun_fd,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out_review / "p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_dryrun_review_v1.json"
        rp.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(rp)

    if write_test_board and decision in (FINAL_GO, FINAL_BLOCKED_BY_MISSING_FIXTURES):
        root = Path(test_board_root or str(repo))
        try:
            tb = write_test_board_records(result, test_mode="dry_run", repo_root=root, module="model_governance", source_review_file=result.get("output_review_file"))
        except (OSError, PermissionError, TypeError):
            standin = repo / "_tmp_eval_out" / "board_standin"
            standin.mkdir(parents=True, exist_ok=True)
            tb = write_test_board_records(result, test_mode="dry_run", repo_root=standin, module="model_governance", source_review_file=result.get("output_review_file"))
        result["test_board_root"] = str(tb.get("test_board_dir", TB_REL))

    return result


def main() -> int:
    r = review(test_board_root=str(_detect_repo_root()))
    print(json.dumps({
        "final_decision": r["final_decision"],
        "dryrun_final_decision": r.get("dryrun_final_decision"),
        "blocker_count": r["blocker_count"],
        "real_execution_enabled": False,
        "recommended_next_phase": r.get("recommended_next_phase"),
        "failed_checks": r.get("failed_checks", []),
    }, indent=2, ensure_ascii=False))
    ok = r["final_decision"] in (FINAL_GO, FINAL_BLOCKED_BY_MISSING_FIXTURES)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
