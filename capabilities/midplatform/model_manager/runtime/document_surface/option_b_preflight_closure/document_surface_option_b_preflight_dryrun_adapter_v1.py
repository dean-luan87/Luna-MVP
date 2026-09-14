# -*- coding: utf-8 -*-
"""Document Surface — Option B preflight dryrun adapter (closure) v1."""

from __future__ import annotations

import uuid
from pathlib import Path
from typing import Any, Dict, List

from capabilities.midplatform.model_manager.runtime.document_surface.option_b_preflight_closure.document_surface_option_b_candidate_schema_compliance_check_dryrun_v1 import (
    run_candidate_schema_compliance_check_dryrun,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_preflight_closure.document_surface_option_b_dependency_availability_check_dryrun_v1 import (
    run_dependency_availability_check_dryrun,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_preflight_closure.document_surface_option_b_input_boundary_check_dryrun_v1 import (
    run_input_boundary_check_dryrun,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_preflight_closure.document_surface_option_b_license_check_dryrun_v1 import (
    run_license_check_dryrun,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_preflight_closure.document_surface_option_b_model_weight_presence_check_dryrun_v1 import (
    run_model_weight_presence_check_dryrun,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_preflight_closure.document_surface_option_b_no_text_fact_leak_check_dryrun_v1 import (
    run_no_text_fact_leak_check_dryrun,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_preflight_closure.document_surface_option_b_output_boundary_check_dryrun_v1 import (
    run_output_boundary_check_dryrun,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_preflight_closure.document_surface_option_b_preflight_candidate_scope_v1 import (
    BLOCKED_REFERENCE_IDS,
    build_preflight_candidate_scope,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_preflight_closure.document_surface_option_b_preflight_dryrun_common_v1 import (
    ABORT_ROLLBACK,
    get_preflight_fixtures,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_preflight_closure.document_surface_option_b_raw_output_normalization_check_dryrun_v1 import (
    run_raw_output_normalization_check_dryrun,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_preflight_closure.document_surface_option_b_runtime_trace_check_dryrun_v1 import (
    run_runtime_trace_check_dryrun,
)

DRYRUN_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_PREFLIGHT_DRYRUN_GO"
DRYRUN_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_PREFLIGHT_DRYRUN_BLOCKED"


def _run_candidate_checks(*, fixture: Dict[str, Any], run_id: str) -> Dict[str, Any]:
    dep = run_dependency_availability_check_dryrun(fixture=fixture, run_id=run_id)
    weight = run_model_weight_presence_check_dryrun(fixture=fixture, run_id=run_id)
    lic = run_license_check_dryrun(fixture=fixture, run_id=run_id)
    inp = run_input_boundary_check_dryrun(fixture=fixture, run_id=run_id)
    out = run_output_boundary_check_dryrun(fixture=fixture, run_id=run_id)
    norm = run_raw_output_normalization_check_dryrun(fixture=fixture, run_id=run_id)
    schema = run_candidate_schema_compliance_check_dryrun(fixture=fixture, run_id=run_id)
    leak = run_no_text_fact_leak_check_dryrun(fixture=fixture, run_id=run_id)
    abort_reason = next(
        (r.get("abort_reason") for r in (dep, weight, lic, inp, out, norm, schema, leak) if r.get("abort_reason")),
        None,
    )
    trace = run_runtime_trace_check_dryrun(
        fixture=fixture,
        run_id=run_id,
        check_results={
            "dependency": dep.get("dependency_status_candidate"),
            "weight": weight.get("weight_status_candidate"),
            "license": lic.get("license_status_candidate"),
            "input": inp.get("input_boundary_check_candidate"),
            "output": out.get("output_boundary_check_candidate"),
            "normalization": norm.get("raw_output_normalization_check_candidate"),
            "schema": schema.get("candidate_schema_compliance_check_candidate"),
            "leak": leak.get("no_text_fact_leak_check_candidate"),
            "abort_reason": abort_reason,
        },
    )
    return {
        "dependency": dep,
        "weight": weight,
        "license": lic,
        "input": inp,
        "output": out,
        "normalization": norm,
        "schema": schema,
        "leak": leak,
        "trace": trace,
        "abort_rollback": {
            "abort_reason": abort_reason,
            "next_action": "return_to_preflight_planning_or_admission_review" if abort_reason else "proceed_to_post_review_only",
            "forbidden_workaround": "skip_preflight_or_force_execution",
            "rollback_action": ABORT_ROLLBACK["rollback_action"] if abort_reason else None,
            **ABORT_ROLLBACK,
        },
        "all_checks_passed": abort_reason is None,
    }


def run_preflight_dryrun_substage(*, repo_root: Path) -> Dict[str, Any]:
    run_id = f"preflight_dryrun_{uuid.uuid4().hex[:12]}"
    scope = build_preflight_candidate_scope()
    fixtures = get_preflight_fixtures(repo_root)
    per_candidate = [_run_candidate_checks(fixture=f, run_id=run_id) for f in fixtures]
    blocked_refs = [
        {"model_candidate_id": bid, "preflight_scope": False, "blocked_reference_only": True}
        for bid in BLOCKED_REFERENCE_IDS
    ]
    passed = (
        scope.get("preflight_candidate_count") == 2
        and len(fixtures) == 2
        and all(p.get("all_checks_passed") for p in per_candidate)
        and scope.get("active_model_selected") is False
    )
    decision = DRYRUN_GO if passed else DRYRUN_BLOCKED
    return {
        "substage": "preflight_dryrun",
        "preflight_dryrun_decision": decision,
        "passed": passed,
        "preflight_run_id": run_id,
        "scope_results": {**scope, "blocked_reference_records": blocked_refs},
        "per_candidate": per_candidate,
        "dependency_results": [p["dependency"] for p in per_candidate],
        "weight_results": [p["weight"] for p in per_candidate],
        "license_results": [p["license"] for p in per_candidate],
        "input_results": [p["input"] for p in per_candidate],
        "output_results": [p["output"] for p in per_candidate],
        "normalization_results": [p["normalization"] for p in per_candidate],
        "schema_results": [p["schema"] for p in per_candidate],
        "leak_results": [p["leak"] for p in per_candidate],
        "trace_results": [p["trace"] for p in per_candidate],
        "abort_rollback_results": [p["abort_rollback"] for p in per_candidate],
        "summary": {
            "phase_id": "Phase-P1-...-OptionB-Preflight-DryRun-v1-001",
            "preflight_dryrun_only": True,
            "preflight_execution_forbidden": True,
            "segmentation_execution_forbidden": True,
            "option_b_execution_allowed": False,
            "final_decision": decision,
            "candidate_only": True,
            "not_fact": True,
        },
        "candidate_only": True,
        "not_fact": True,
    }
