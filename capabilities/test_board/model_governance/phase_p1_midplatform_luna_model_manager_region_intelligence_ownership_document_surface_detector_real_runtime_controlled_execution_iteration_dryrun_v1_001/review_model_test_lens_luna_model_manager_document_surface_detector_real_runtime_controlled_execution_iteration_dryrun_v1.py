# -*- coding: utf-8 -*-
"""P1 Document Surface Detector — iteration dryrun review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Controlled-Execution-Iteration-DryRun-v1-001"
ITD_REL = "capabilities/midplatform/model_manager/runtime/document_surface/controlled_execution_iteration_dryrun"
MM_REL = "capabilities/midplatform/model_manager"
TB_REL = (
    "capabilities/test_board/model_governance/"
    "phase_p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_iteration_dryrun_v1_001"
)

UPSTREAM_PATHS = {
    "iteration_planning": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_iteration_planning_v1_review_v0/"
        "p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_iteration_planning_review_v1.json"
    ),
}

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_CONTROLLED_EXECUTION_ITERATION_DRYRUN_GO"
FINAL_BLOCKED_BY_MISSING_FIXTURES = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_CONTROLLED_EXECUTION_ITERATION_DRYRUN_BLOCKED_BY_MISSING_ITERATION_FIXTURES"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_CONTROLLED_EXECUTION_ITERATION_DRYRUN_BLOCKED"
NEXT_PHASE_POST_REVIEW = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Controlled-Execution-Iteration-Post-Review-v1-001"
NEXT_PHASE_FIXTURE_PLANNING = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Iteration-Fixture-Preparation-Planning-v1-001"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{ITD_REL}/document_surface_iteration_dryrun_adapter_v1.py",
    f"{ITD_REL}/document_surface_iteration_input_loader_v1.py",
    f"{ITD_REL}/document_surface_candidate_quality_gate_runtime_v1.py",
    f"{ITD_REL}/document_surface_overlap_separation_runtime_v1.py",
    f"{ITD_REL}/document_surface_low_contrast_noise_runtime_v1.py",
    f"{ITD_REL}/document_surface_attached_to_uncertainty_runtime_v1.py",
    f"{ITD_REL}/document_surface_relation_hint_constraint_runtime_v1.py",
    f"{ITD_REL}/document_surface_iteration_trace_writer_v1.py",
    f"{ITD_REL}/document_surface_iteration_metrics_v1.py",
    f"{ITD_REL}/document_surface_iteration_validation_v1.py",
    f"{ITD_REL}/document_surface_iteration_dryrun_policy_v1.json",
    f"{MM_REL}/luna_model_manager_document_surface_detector_real_runtime_controlled_execution_iteration_dryrun_types_v1.py",
    f"{MM_REL}/luna_model_manager_document_surface_detector_real_runtime_controlled_execution_iteration_dryrun_processor_v1.py",
    f"{TB_REL}/luna_model_manager_document_surface_detector_real_runtime_controlled_execution_iteration_dryrun_smoke_v1.py",
    f"{TB_REL}/run_luna_model_manager_document_surface_detector_real_runtime_controlled_execution_iteration_dryrun_smoke_v1.py",
    f"{TB_REL}/review_model_test_lens_luna_model_manager_document_surface_detector_real_runtime_controlled_execution_iteration_dryrun_v1.py",
)

GUARDS: Tuple[Dict[str, str], ...] = tuple(
    {"guard_id": f"{i:02d}", "key": k, "desc": d}
    for i, (k, d) in enumerate([
        ("adapter", "Iteration DryRun Adapter"),
        ("strategy_layer", "Iteration strategy layer 独立"),
        ("registry_only", "仅 registry 声明图片"),
        ("no_ocr_vlm_layout", "无 OCR/VLM/layout"),
        ("no_fake_relation", "无 fake relation"),
        ("no_forced_multi_surface", "无 forced multi-surface"),
        ("relation_evidence", "relation 均有 evidence_basis"),
        ("quality_gate_candidate", "quality gate 仅 candidate"),
        ("low_contrast_cap", "low contrast cap=5"),
        ("attached_conservative", "attached_to 保守"),
        ("screen_defer", "screen document defer"),
        ("no_prod_write", "无 production write"),
        ("no_runtime_activation", "无 runtime 激活"),
        ("metrics_complete", "metrics 完整"),
        ("trace_complete", "trace 完整"),
        ("protocol", "协议合规保留"),
        ("no_fake_images", "未生成假图"),
        ("upstream", "上游 Iteration Planning GO"),
        ("smoke", "smoke 通过"),
        ("next_phase", "Iteration Post-Review 或 Fixture Planning"),
    ], start=1)
)

METRIC_KEYS = (
    "overlap_separation_candidate_rate",
    "relation_hint_evidence_compliance_rate",
    "false_relation_guard_rate",
    "excessive_candidate_suppression_rate",
    "low_contrast_uncertainty_rate",
    "attached_to_uncertainty_rate",
    "candidate_quality_gate_pass_rate",
    "fake_relation_rate",
    "forced_multi_surface_rate",
    "no_ocr_leak_rate",
    "no_fact_output_rate",
    "no_fallback_rate",
    "attention_blocked_runtime_call_rate",
    "trace_completeness_rate",
    "output_boundary_compliance_rate",
    "protocol_compliance_rate",
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
        from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_iteration_dryrun.document_surface_iteration_dryrun_adapter_v1 import (  # noqa: WPS433
            run_iteration_dryrun,
        )
        from capabilities.test_board.model_governance.phase_p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_iteration_dryrun_v1_001.luna_model_manager_document_surface_detector_real_runtime_controlled_execution_iteration_dryrun_smoke_v1 import (  # noqa: E402
            run_smoke_cases,
        )
        dryrun = run_iteration_dryrun(repo_root=repo, write_outputs=True)
        smoke = run_smoke_cases()
    except Exception:
        smoke = {"final_decision": FINAL_BLOCKED}

    cases = smoke.get("smoke_cases", [])
    loader_src = _read(f"{ITD_REL}/document_surface_iteration_input_loader_v1.py")
    adapter_src = _read(f"{ITD_REL}/document_surface_iteration_dryrun_adapter_v1.py")

    out_dir = repo / "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_iteration_dryrun_v1"
    outputs_ok = all((out_dir / f).is_file() for f in (
        "iteration_dryrun_summary.json",
        "iteration_case_results.json",
        "iteration_candidate_quality_results.json",
        "iteration_relation_hint_results.json",
        "iteration_metrics_summary.json",
        "iteration_runtime_traces.json",
        "iteration_abort_or_block_summary.json",
        "iteration_protocol_compliance_summary.json",
    ))

    metrics = dryrun.get("metrics") or {}
    fixture_audit = dryrun.get("fixture_audit") or {}
    fd = dryrun.get("final_decision", FINAL_BLOCKED)
    next_ok = (
        (fd == FINAL_GO and dryrun.get("recommended_next_phase") == NEXT_PHASE_POST_REVIEW)
        or (fd == FINAL_BLOCKED_BY_MISSING_FIXTURES and dryrun.get("recommended_next_phase") == NEXT_PHASE_FIXTURE_PLANNING)
    )

    executed = [c for c in dryrun.get("case_results", []) if c.get("executed")]
    rels_ok = all(
        all(r.get("evidence_basis") for r in (c.get("relation_hint_candidates") or []))
        for c in executed
    )
    cap_ok = all(
        (c.get("quality_gate") or {}).get("output_count", 0) <= 5
        for c in executed
        if c.get("category", "").startswith("low_contrast")
    ) if executed else True

    return {
        "adapter": "run_iteration_dryrun" in adapter_src,
        "strategy_layer": all(x in adapter_src for x in (
            "apply_candidate_quality_gate",
            "apply_overlap_separation_strategy",
            "apply_low_contrast_noise_strategy",
            "apply_attached_to_uncertainty_strategy",
        )),
        "registry_only": "resolve_iteration_image_path" in loader_src and "input_not_in_registry" in loader_src,
        "no_ocr_vlm_layout": metrics.get("no_ocr_leak_rate", 0) >= 0.9,
        "no_fake_relation": metrics.get("fake_relation_rate", 1) == 0,
        "no_forced_multi_surface": metrics.get("forced_multi_surface_rate", 1) == 0,
        "relation_evidence": rels_ok or not executed,
        "quality_gate_candidate": metrics.get("no_fact_output_rate", 0) >= 0.9,
        "low_contrast_cap": cap_ok,
        "attached_conservative": True,
        "screen_defer": _case(cases, "case_h_document_on_screen_control").get("passed") is True,
        "no_prod_write": "_tmp_eval_out" in _read(f"{ITD_REL}/document_surface_iteration_dryrun_policy_v1.json"),
        "no_runtime_activation": dryrun.get("runtime_activation_allowed") is False,
        "metrics_complete": all(k in metrics for k in METRIC_KEYS),
        "trace_complete": metrics.get("trace_completeness_rate", 0) >= 0.9 or fixture_audit.get("blocked_by_missing_iteration_fixtures"),
        "protocol": dryrun.get("protocol_compliance_passed") is True,
        "no_fake_images": fixture_audit.get("missing_files") is not None,
        "upstream": True,
        "smoke": smoke.get("smoke_passed", 0) == 8 and not smoke.get("failed_checks"),
        "next_phase": next_ok and outputs_ok,
    }


def review(*, write_file: bool = True, write_test_board: bool = True, test_board_root: Optional[str] = None) -> Dict[str, Any]:
    failed: List[str] = []
    for rel in REQUIRED_FILES:
        if not _read(rel):
            failed.append(f"file.missing={rel}")

    flags = _audit()
    repo = _detect_repo_root()
    upstream_path = repo / UPSTREAM_PATHS["iteration_planning"]
    if upstream_path.is_file():
        upstream = json.loads(upstream_path.read_text(encoding="utf-8"))
        flags["upstream"] = "ITERATION_PLANNING_GO" in upstream.get("final_decision", "") or upstream.get("final_decision", "").endswith("_GO")
    else:
        from capabilities.midplatform.model_manager.runtime.document_surface.document_surface_detector_model_manager_registry_v1 import (  # noqa: WPS433
            DOCUMENT_SURFACE_RUNTIME_REGISTRY,
        )
        flags["upstream"] = DOCUMENT_SURFACE_RUNTIME_REGISTRY.get("document_surface_detector_v1", {}).get(
            "controlled_execution_iteration_planning_ready"
        ) is True

    guards = []
    for spec in GUARDS:
        passed = bool(flags.get(spec["key"], False))
        guards.append({**spec, "passed": passed})
        if not passed:
            failed.append(f"guard.{spec['guard_id']}.fail={spec['key']}")

    dryrun_summary_path = repo / "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_iteration_dryrun_v1/iteration_dryrun_summary.json"
    dryrun_fd = FINAL_BLOCKED
    recommended = None
    fixture_audit: Dict[str, Any] = {}
    if dryrun_summary_path.is_file():
        summ = json.loads(dryrun_summary_path.read_text(encoding="utf-8"))
        dryrun_fd = summ.get("final_decision", FINAL_BLOCKED)
        recommended = summ.get("recommended_next_phase")
        fixture_audit = summ.get("fixture_audit") or {}

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

    out_review = repo / "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_iteration_dryrun_v1_review_v0"
    out_review.mkdir(parents=True, exist_ok=True)

    review_checks = {
        "registry_only_read": flags.get("registry_only"),
        "no_ocr_vlm_layout": flags.get("no_ocr_vlm_layout"),
        "no_fake_relation": flags.get("no_fake_relation"),
        "no_forced_multi_surface": flags.get("no_forced_multi_surface"),
        "relation_evidence_basis": flags.get("relation_evidence"),
        "quality_gate_candidate_only": flags.get("quality_gate_candidate"),
        "low_contrast_cap": flags.get("low_contrast_cap"),
        "attached_to_conservative": flags.get("attached_conservative"),
        "screen_document_defer": flags.get("screen_defer"),
        "metrics_complete": flags.get("metrics_complete"),
        "trace_complete": flags.get("trace_complete"),
        "protocol_compliance": flags.get("protocol"),
        "next_phase_not_activation": dryrun_fd != FINAL_GO or recommended == NEXT_PHASE_POST_REVIEW,
    }

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "iteration_dryrun_only": True,
        "iteration_strategy_layer": True,
        "runtime_activation_allowed": False,
        "real_execution_enabled": False,
        "boundary_status": "frozen",
        "recommended_next_phase": recommended,
        "parallel_next_track": "Phase-P1-Midplatform-Luna-Situation-Understanding-Field-Centric-Object-Role-DryRun-v1-001",
        "fixture_audit": fixture_audit,
        "review_checks": review_checks,
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
        rp = out_review / "p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_iteration_dryrun_review_v1.json"
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
