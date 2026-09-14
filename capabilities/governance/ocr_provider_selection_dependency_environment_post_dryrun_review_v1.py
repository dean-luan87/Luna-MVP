# -*- coding: utf-8 -*-
"""OCR Provider Selection / Dependency / Environment Post-DryRun Review v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.ocr_provider_selection_dependency_environment_dryrun_v1 import (
    BLOCKED_PATHS,
    FINAL_DECISION_GO as DRYRUN_FINAL_GO,
    HEALTH_BINDINGS,
    NEXT_PHASE_GO as DRYRUN_NEXT_PHASE,
    PHASE_ID as DRYRUN_PHASE,
    SCOPE as DRYRUN_SCOPE,
    SELECTION_CRITERIA,
)
from capabilities.governance.ocr_provider_selection_dependency_environment_planning_v1 import (
    SECURITY_CONFIRMATIONS,
)

PHASE_ID = "Phase-OCR-Provider-Selection-Dependency-Environment-Post-DryRun-Review-v1-001"
REVIEW_SCOPE = "ocr_provider_selection_dependency_environment_post_dryrun_review_only"
SOURCE_CHAIN = "ocr_provider_selection_dependency_environment_post_dryrun_review_v1"

UPSTREAM_REQUIRED_FINAL = DRYRUN_FINAL_GO
UPSTREAM_NEXT_PHASE = DRYRUN_NEXT_PHASE

FINAL_DECISION_GO = (
    "OCR_PROVIDER_SELECTION_DEPENDENCY_ENVIRONMENT_POST_DRYRUN_REVIEW_CLOSED_READY_FOR_REAL_DEPENDENCY_CHECK_PLANNING"
)
FINAL_DECISION_HOLD = (
    "OCR_PROVIDER_SELECTION_DEPENDENCY_ENVIRONMENT_POST_DRYRUN_REVIEW_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-OCR-Provider-Real-Dependency-Check-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-OCR-Provider-Selection-Dependency-Environment-Issue-Review-v1-001"

EXPECTED_PROVIDER_FAMILIES: Set[str] = {
    "mock_or_fixture",
    "paddleocr_later",
    "rapidocr_later",
    "external_ocr_later",
}

DEPENDENCY_PLANNED_FLAGS: Tuple[str, ...] = (
    "python_package_check_planned",
    "model_cache_check_planned",
    "model_file_hash_check_planned",
    "provider_import_check_planned",
    "runtime_smoke_check_planned",
    "sample_ocr_check_planned_later",
)

DEPENDENCY_EXECUTED_FLAGS: Tuple[str, ...] = (
    "python_package_check_executed_now",
    "model_cache_check_executed_now",
    "model_file_hash_check_executed_now",
    "provider_import_check_executed_now",
    "runtime_smoke_check_executed_now",
    "sample_ocr_check_executed_now",
)

BOUNDARY_FALSE_REVIEW: Tuple[str, ...] = (
    "new_provider_selection_candidate_generated_now",
    "new_dependency_readiness_candidate_generated_now",
    "new_environment_readiness_candidate_generated_now",
    "provider_selection_finalized_now",
    "provider_dependency_check_executed_now",
    "environment_readiness_check_executed_now",
    "dependency_install_executed_now",
    "model_download_executed_now",
    "provider_import_check_executed_now",
    "provider_smoke_check_executed_now",
    "sample_ocr_executed_now",
    "provider_authorization_started_now",
    "controlled_trial_started_now",
    "paddleocr_imported_now",
    "rapidocr_imported_now",
    "external_ocr_imported_now",
    "paddleocr_invoked_now",
    "rapidocr_invoked_now",
    "external_ocr_invoked_now",
    "real_ocr_provider_invoked_now",
    "ocr_request_submitted_now",
    "image_read_executed_now",
    "crop_executed_now",
    "ocr_fact_generated_now",
    "memory_written_now",
    "world_model_written_now",
    "user_facing_output_generated_now",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Post-DryRun Review GO ≠ provider selected",
    "provider_selection_candidate ≠ final provider selection",
    "dependency readiness candidate ≠ dependency check executed",
    "environment readiness candidate ≠ runtime ready",
    "provider comparison sample ≠ provider decision",
    "next real dependency check planning ≠ import/install allowed",
    "real dependency check planning ≠ provider invocation",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_provider_selection_dependency_environment_post_dryrun_review"
)


def _review_meta() -> Dict[str, Any]:
    meta = {
        "ocr_provider_selection_dependency_environment_post_dryrun_review_only": True,
        "review_only": True,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
    }
    for field in BOUNDARY_FALSE_REVIEW:
        meta[field] = False
    meta["new_provider_selection_candidate_generated_now"] = False
    meta["new_dependency_readiness_candidate_generated_now"] = False
    meta["new_environment_readiness_candidate_generated_now"] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def run_ocr_provider_selection_dependency_environment_post_dryrun_review_v1(
    *,
    ocr_provider_selection_dependency_environment_dryrun_root: str,
    review_output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    dryrun_root = Path(ocr_provider_selection_dependency_environment_dryrun_root).expanduser().resolve()
    dryrun_sm = _try_read_json(dryrun_root / "summary.json") or {}
    dryrun_vr = _try_read_json(dryrun_root / "verifier_report.json") or {}

    out_root = (
        Path(review_output_root).expanduser().resolve()
        if review_output_root
        else dryrun_root.parent / "ocr_provider_selection_dependency_environment_post_dryrun_review"
    )
    meta = {**_review_meta(), "upstream_dryrun_root": str(dryrun_root), "review_output_root": str(out_root)}

    selection = _try_read_json(dryrun_root / "provider_selection_candidate_v1.json") or {}
    dependency = _try_read_json(dryrun_root / "dependency_readiness_candidate_matrix_v1.json") or {}
    environment = _try_read_json(dryrun_root / "environment_readiness_candidate_v1.json") or {}
    comparison = _try_read_json(dryrun_root / "provider_comparison_matrix_sample_v1.json") or {}
    cost_latency = _try_read_json(dryrun_root / "provider_cost_latency_resource_sample_v1.json") or {}
    capability = _try_read_json(dryrun_root / "provider_capability_fit_sample_v1.json") or {}
    health = _try_read_json(dryrun_root / "provider_health_binding_dryrun_result_v1.json") or {}
    fallback = _try_read_json(dryrun_root / "provider_fallback_strategy_dryrun_result_v1.json") or {}
    security = _try_read_json(dryrun_root / "provider_security_boundary_dryrun_result_v1.json") or {}
    audit = _try_read_json(dryrun_root / "provider_no_import_no_install_audit_v1.json") or {}
    blocked = _try_read_json(dryrun_root / "provider_selection_blocked_path_result_v1.json") or {}

    dryrun_go = dryrun_vr.get("verifier") == "GO" and dryrun_vr.get("passed") is True
    if not dryrun_go:
        blockers.append("dryrun verifier must be GO")
    if dryrun_sm.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append("dryrun final_decision mismatch")
    if dryrun_sm.get("recommended_next_phase") != UPSTREAM_NEXT_PHASE:
        blockers.append("dryrun recommended_next_phase mismatch")
    if dryrun_sm.get("boundary_ok") is not True:
        blockers.append("dryrun boundary_ok must be true")
    if dryrun_sm.get("simulated") is not True:
        blockers.append("dryrun simulated must be true")

    for field in BOUNDARY_FALSE_REVIEW:
        if dryrun_sm.get(field) is True:
            blockers.append(f"dryrun {field} must be false")

    input_review = {
        "review_id": "provider_selection_dependency_environment_dryrun_input_review_v1",
        "upstream_root": str(dryrun_root),
        "upstream_phase": DRYRUN_PHASE,
        "upstream_scope": DRYRUN_SCOPE,
        "upstream_verifier_go": dryrun_go,
        "upstream_final_decision": dryrun_sm.get("final_decision"),
        "upstream_simulated": dryrun_sm.get("simulated"),
        "selection_candidate_count": selection.get("candidate_count"),
        "dependency_row_count": dependency.get("row_count"),
        "environment_candidate_present": bool(environment.get("artifact_id")),
        "comparison_sample_present": bool(comparison.get("matrix_id")),
        "review_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    selection_issues: List[Dict[str, Any]] = []
    candidates = selection.get("candidates") or []
    if selection.get("candidate_count") != 4 or len(candidates) != 4:
        selection_issues.append({"issue_id": "count", "detail": "expected 4 selection candidates"})
    families = {c.get("provider_family") for c in candidates}
    if families != EXPECTED_PROVIDER_FAMILIES:
        selection_issues.append({"issue_id": "families", "detail": f"expected {EXPECTED_PROVIDER_FAMILIES}"})
    if selection.get("selected_provider_for_execution") is not None:
        selection_issues.append({"issue_id": "not_finalized", "detail": "selected_provider_for_execution must be null"})
    if selection.get("provider_selection_finalized_now") is not False:
        selection_issues.append({"issue_id": "finalized_flag", "detail": "must be false"})
    for c in candidates:
        fam = c.get("provider_family")
        for flag, expected in (
            ("provider_status", "planned_candidate"),
            ("invocation_allowed", False),
            ("authorization_required", True),
            ("dependency_check_required", True),
            ("environment_check_required", True),
            ("controlled_trial_required", True),
        ):
            if c.get(flag) != expected:
                selection_issues.append({"issue_id": f"{fam}_{flag}", "detail": f"expected {expected}"})

    selection_review = {
        "review_id": "provider_selection_candidate_review_v1",
        "candidate_count": selection.get("candidate_count"),
        "selected_provider_for_execution": selection.get("selected_provider_for_execution"),
        "provider_selection_finalized_now": selection.get("provider_selection_finalized_now"),
        "issues": selection_issues,
        "review_pass": len(selection_issues) == 0,
        **meta,
    }

    dependency_issues: List[Dict[str, Any]] = []
    rows = dependency.get("rows") or []
    if dependency.get("row_count") != 4 or len(rows) != 4:
        dependency_issues.append({"issue_id": "count", "detail": "expected 4 dependency rows"})
    for row in rows:
        fam = row.get("provider_family", "unknown")
        for flag in DEPENDENCY_PLANNED_FLAGS:
            if row.get(flag) is not True:
                dependency_issues.append({"issue_id": f"{fam}_{flag}", "detail": "must be true"})
        for flag in DEPENDENCY_EXECUTED_FLAGS:
            if row.get(flag) is not False:
                dependency_issues.append({"issue_id": f"{fam}_{flag}", "detail": "must be false"})

    dependency_review = {
        "review_id": "dependency_readiness_candidate_review_v1",
        "row_count": dependency.get("row_count"),
        "issues": dependency_issues,
        "review_pass": len(dependency_issues) == 0,
        **meta,
    }

    environment_issues: List[Dict[str, Any]] = []
    checks = (
        ("virtualenv_isolation_required", True),
        ("model_cache_directory_planned", None),
        ("writable_output_directory_planned", None),
        ("readonly_fixture_directory_planned_later", None),
        ("cpu_memory_guard_planned", True),
        ("timeout_guard_planned", True),
        ("network_dependency_default", False),
        ("sandbox_boundary_required", True),
        ("production_path_write_allowed", False),
    )
    for key, expected in checks:
        val = environment.get(key)
        if expected is None:
            if not val:
                environment_issues.append({"issue_id": key, "detail": "must exist"})
        elif val != expected:
            environment_issues.append({"issue_id": key, "detail": f"expected {expected}"})
    if environment.get("environment_readiness_check_executed_now") is not False:
        environment_issues.append({"issue_id": "check_executed", "detail": "must be false"})

    environment_review = {
        "review_id": "environment_readiness_candidate_review_v1",
        "issues": environment_issues,
        "review_pass": len(environment_issues) == 0,
        **meta,
    }

    comparison_issues: List[Dict[str, Any]] = []
    if comparison.get("dimension_count") != len(SELECTION_CRITERIA):
        comparison_issues.append({"issue_id": "dimensions", "detail": f"expected {len(SELECTION_CRITERIA)}"})
    if len(comparison.get("rows") or []) != 4:
        comparison_issues.append({"issue_id": "rows", "detail": "expected 4 comparison rows"})
    if comparison.get("comparison_only_not_final_selection") is not True:
        comparison_issues.append({"issue_id": "sample_only", "detail": "must be true"})
    for row in comparison.get("rows") or []:
        if row.get("final_selection") is not False and row.get("sample_only") is not True:
            comparison_issues.append(
                {"issue_id": row.get("provider_family"), "detail": "comparison must be sample only"}
            )

    comparison_review = {
        "review_id": "provider_comparison_matrix_review_v1",
        "dimension_count": comparison.get("dimension_count"),
        "comparison_is_sample_only": comparison.get("comparison_only_not_final_selection"),
        "comparison_result_does_not_finalize_provider": selection.get("selected_provider_for_execution") is None,
        "provider_comparison_to_execution_selection_blocked": True,
        "issues": comparison_issues,
        "review_pass": len(comparison_issues) == 0,
        **meta,
    }

    cost_review = {
        "review_id": "provider_cost_latency_resource_review_v1",
        "sample_only": cost_latency.get("sample_only") is True,
        "row_count": len(cost_latency.get("rows") or []),
        "review_pass": cost_latency.get("sample_only") is True and len(cost_latency.get("rows") or []) == 4,
        **meta,
    }

    capability_review = {
        "review_id": "provider_capability_fit_review_v1",
        "sample_only": capability.get("sample_only") is True,
        "fit_count": len(capability.get("fit_notes") or []),
        "review_pass": capability.get("sample_only") is True and len(capability.get("fit_notes") or []) == 4,
        **meta,
    }

    health_issues: List[Dict[str, Any]] = []
    bindings = health.get("bindings") or []
    if len(bindings) != len(HEALTH_BINDINGS):
        health_issues.append({"issue_id": "count", "detail": f"expected {len(HEALTH_BINDINGS)} bindings"})
    binding_map = {(b.get("trigger"), b.get("target_candidate")) for b in bindings}
    for hb in HEALTH_BINDINGS:
        if (hb["trigger"], hb["target"]) not in binding_map:
            health_issues.append({"issue_id": hb["trigger"], "detail": "missing route"})
        for b in bindings:
            if b.get("trigger") == hb["trigger"] and b.get("executed_now") is not False:
                health_issues.append({"issue_id": f"{hb['trigger']}_executed", "detail": "must be false"})

    health_review = {
        "review_id": "provider_health_binding_review_v1",
        "binding_count": len(bindings),
        "issues": health_issues,
        "review_pass": len(health_issues) == 0,
        **meta,
    }

    fallback_issues: List[Dict[str, Any]] = []
    if fallback.get("no_automatic_switch_execution") is not True:
        fallback_issues.append({"issue_id": "no_auto", "detail": "must be true"})
    for flag in ("fallback_executed_now", "retry_executed_now", "provider_switch_executed_now"):
        if fallback.get(flag) is not False:
            fallback_issues.append({"issue_id": flag, "detail": "must be false"})

    fallback_review = {
        "review_id": "provider_fallback_strategy_review_v1",
        "issues": fallback_issues,
        "review_pass": len(fallback_issues) == 0,
        **meta,
    }

    security_issues: List[Dict[str, Any]] = []
    if security.get("boundary_pass") is not True:
        security_issues.append({"issue_id": "boundary_pass", "detail": "must be true"})
    for key in SECURITY_CONFIRMATIONS:
        if security.get("confirmations", {}).get(key) is not True:
            security_issues.append({"issue_id": key, "detail": "confirmation required"})

    security_review = {
        "review_id": "provider_security_boundary_review_v1",
        "issues": security_issues,
        "review_pass": len(security_issues) == 0,
        **meta,
    }

    no_import_issues: List[Dict[str, Any]] = []
    audit_flags = (
        "paddleocr_imported_now",
        "rapidocr_imported_now",
        "external_ocr_imported_now",
        "dependency_install_executed_now",
        "model_download_executed_now",
        "provider_import_check_executed_now",
        "provider_smoke_check_executed_now",
        "sample_ocr_executed_now",
        "paddleocr_invoked_now",
        "rapidocr_invoked_now",
        "external_ocr_invoked_now",
    )
    if audit.get("audit_pass") is not True:
        no_import_issues.append({"issue_id": "audit_pass", "detail": "must pass"})
    for flag in audit_flags:
        if audit.get(flag) is not False:
            no_import_issues.append({"issue_id": flag, "detail": "must be false"})
    if dryrun_sm.get("ocr_request_submitted_now") is True:
        no_import_issues.append({"issue_id": "ocr_request", "detail": "must not submit"})
    if dryrun_sm.get("image_read_executed_now") is True or dryrun_sm.get("crop_executed_now") is True:
        no_import_issues.append({"issue_id": "image_io", "detail": "no read/crop"})
    if dryrun_sm.get("ocr_fact_generated_now") is True:
        no_import_issues.append({"issue_id": "ocr_fact", "detail": "no fact"})

    no_import_review = {
        "review_id": "provider_no_import_no_install_review_v1",
        "no_dependency_install": audit.get("dependency_install_executed_now") is False,
        "no_model_download": audit.get("model_download_executed_now") is False,
        "no_provider_import": audit.get("paddleocr_imported_now") is False
        and audit.get("rapidocr_imported_now") is False,
        "no_provider_smoke": audit.get("provider_smoke_check_executed_now") is False,
        "no_sample_ocr": audit.get("sample_ocr_executed_now") is False,
        "issues": no_import_issues,
        "review_pass": len(no_import_issues) == 0,
        **meta,
    }

    blocked_issues: List[Dict[str, Any]] = []
    paths = {p.get("path_id"): p for p in blocked.get("paths") or []}
    if blocked.get("all_blocked") is not True or len(paths) != len(BLOCKED_PATHS):
        blocked_issues.append({"issue_id": "count", "detail": f"expected {len(BLOCKED_PATHS)} paths"})
    for pid in BLOCKED_PATHS:
        row = paths.get(pid)
        if not row or row.get("blocked") is not True:
            blocked_issues.append({"issue_id": pid, "detail": "must be blocked=true"})

    blocked_review = {
        "review_id": "provider_selection_blocked_path_review_v1",
        "paths_total": len(BLOCKED_PATHS),
        "all_blocked": blocked.get("all_blocked"),
        "issues": blocked_issues,
        "review_pass": len(blocked_issues) == 0,
        **meta,
    }

    reviews_pass = (
        len(blockers) == 0
        and input_review.get("review_pass")
        and selection_review.get("review_pass")
        and dependency_review.get("review_pass")
        and environment_review.get("review_pass")
        and comparison_review.get("review_pass")
        and cost_review.get("review_pass")
        and capability_review.get("review_pass")
        and health_review.get("review_pass")
        and fallback_review.get("review_pass")
        and security_review.get("review_pass")
        and no_import_review.get("review_pass")
        and blocked_review.get("review_pass")
    )
    boundary_ok = reviews_pass

    closure = {
        "closure_id": "provider_selection_dependency_environment_closure_decision_v1",
        "ocr_provider_selection_dependency_environment_dryrun_closed": boundary_ok,
        "provider_selection_candidate_trusted": boundary_ok,
        "dependency_readiness_candidate_trusted": boundary_ok,
        "environment_readiness_candidate_trusted": boundary_ok,
        "final_decision": FINAL_DECISION_GO if boundary_ok else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else NEXT_PHASE_HOLD,
        **meta,
    }

    next_readiness = {
        "readiness_id": "next_route_readiness_decision_v1",
        "ready_for_real_dependency_check_planning": boundary_ok,
        "do_not_import_provider_now": True,
        "do_not_install_dependency_now": True,
        "do_not_invoke_provider_now": True,
        "do_not_finalize_provider_selection_now": True,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else PHASE_ID,
        "final_decision": closure["final_decision"],
        "rationale": (
            "After dryrun closure, plan real dependency checks only — "
            "no import, install, download, or provider invocation"
        ),
        **meta,
    }

    non_claims = {
        "register_id": "non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    all_issue_ids = (
        [i["issue_id"] for i in selection_issues]
        + [i["issue_id"] for i in dependency_issues]
        + [i["issue_id"] for i in environment_issues]
        + [i["issue_id"] for i in comparison_issues]
        + [i["issue_id"] for i in blocked_issues]
        + [i["issue_id"] for i in no_import_issues]
    )

    summary = {
        "phase": PHASE_ID,
        "review_scope": REVIEW_SCOPE,
        "boundary_ok": boundary_ok,
        "violations": blockers + all_issue_ids,
        "final_decision": closure["final_decision"],
        "recommended_next_phase": closure["recommended_next_phase"],
        "high_risk_count": 0 if boundary_ok else 1,
        "ocr_provider_selection_dependency_environment_dryrun_closed": boundary_ok,
        "provider_selection_candidate_trusted": boundary_ok,
        **meta,
    }

    return {
        "provider_selection_dependency_environment_dryrun_input_review": input_review,
        "provider_selection_candidate_review": selection_review,
        "dependency_readiness_candidate_review": dependency_review,
        "environment_readiness_candidate_review": environment_review,
        "provider_comparison_matrix_review": comparison_review,
        "provider_cost_latency_resource_review": cost_review,
        "provider_capability_fit_review": capability_review,
        "provider_health_binding_review": health_review,
        "provider_fallback_strategy_review": fallback_review,
        "provider_security_boundary_review": security_review,
        "provider_no_import_no_install_review": no_import_review,
        "provider_selection_blocked_path_review": blocked_review,
        "provider_selection_dependency_environment_closure_decision": closure,
        "next_route_readiness_decision": next_readiness,
        "non_claims_register": non_claims,
        "summary": summary,
    }
