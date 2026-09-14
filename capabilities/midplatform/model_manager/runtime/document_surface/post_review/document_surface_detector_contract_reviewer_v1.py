# -*- coding: utf-8 -*-
"""Document Surface Detector — contract reviewer v1."""

from __future__ import annotations

from typing import Any, Dict, List

from capabilities.midplatform.model_manager.runtime.document_surface.document_surface_detector_request_builder_v1 import (
    build_document_surface_request,
)
from capabilities.midplatform.model_manager.runtime.document_surface.document_surface_detector_types_v1 import (
    RUNTIME_ID,
)
from capabilities.midplatform.model_manager.runtime.document_surface.dryrun.document_surface_detector_fixture_runtime_v1 import (
    run_document_surface_fixture_runtime,
)
from capabilities.midplatform.model_manager.runtime.document_surface.dryrun.document_surface_detector_dryrun_adapter_v1 import (
    run_document_surface_detector_dryrun,
)


REQUEST_REQUIRED = (
    "source_region_id",
    "attention_gate_status",
    "goal_context",
    "allowed_capabilities",
    "forbidden_capabilities",
    "candidate_only",
)

RESPONSE_REQUIRED = (
    "runtime_id",
    "execution_mode",
    "document_surface_candidates",
    "relation_hint_candidates",
    "runtime_status_candidate",
    "candidate_only",
    "not_fact",
)

SURFACE_CANDIDATE_REQUIRED = (
    "surface_id",
    "source_region_id",
    "visibility_status_candidate",
    "owner_entity_candidate_ref",
    "source_runtime",
    "candidate_only",
    "not_fact",
)

RELATION_REQUIRED = (
    "relation_id",
    "relation_type_candidate",
    "entity_a",
    "entity_b",
    "evidence_basis",
    "source_runtime",
    "candidate_only",
    "not_fact",
)

TEXT_OWNER_REQUIRED = (
    "text_region_id",
    "owner_entity_candidate_ref",
    "assignment_status_candidate",
    "assignment_basis",
    "candidate_only",
    "not_fact",
)


def _check_fields(obj: Dict[str, Any], required: tuple) -> List[str]:
    return [k for k in required if k not in obj or obj[k] is None]


def review_contracts() -> Dict[str, Any]:
    """Contract 完整性审查 — request / response / evidence / candidate."""
    checks: Dict[str, bool] = {}
    failures: List[str] = []

    request = build_document_surface_request(
        source_region_id="region_contract",
        attention_gate_status="allowed",
        goal_context={"task": "document_surface_dryrun"},
    )
    req_missing = _check_fields(request, REQUEST_REQUIRED)
    checks["request_schema_complete"] = not req_missing and request.get("candidate_only") is True
    if req_missing:
        failures.append(f"request.missing={req_missing}")

    runtime_out = run_document_surface_fixture_runtime(
        fixture_ref="stacked_papers",
        source_region_id="region_contract",
    )
    resp_missing = _check_fields(runtime_out, RESPONSE_REQUIRED)
    checks["response_schema_complete"] = (
        not resp_missing
        and runtime_out.get("runtime_id") == RUNTIME_ID
        and runtime_out.get("execution_mode") == "deterministic_fixture"
        and runtime_out.get("candidate_only") is True
        and runtime_out.get("not_fact") is True
    )
    if resp_missing:
        failures.append(f"response.missing={resp_missing}")

    surfaces = runtime_out.get("document_surface_candidates") or []
    surface_ok = bool(surfaces) and all(
        not _check_fields(s, SURFACE_CANDIDATE_REQUIRED)
        and (s.get("bbox_candidate") or s.get("polygon_candidate"))
        for s in surfaces
    )
    checks["surface_candidate_schema_complete"] = surface_ok

    relations = runtime_out.get("relation_hint_candidates") or []
    relation_ok = bool(relations) and all(not _check_fields(r, RELATION_REQUIRED) for r in relations)
    checks["relation_hint_schema_complete"] = relation_ok

    dryrun = run_document_surface_detector_dryrun(fixture_ref="stacked_papers")
    dr = dryrun.get("document_surface_dryrun_result") or {}
    pkg = dr.get("ownership_evidence_package") or {}
    assignments = dr.get("text_owner_assignment_candidates") or []

    checks["evidence_package_present"] = bool(pkg)
    checks["evidence_package_candidate_only"] = pkg.get("candidate_only") is True and pkg.get("not_fact") is True
    checks["surface_before_text_owner"] = pkg.get("surface_candidate_before_text_owner") is True
    checks["text_owner_schema_complete"] = bool(assignments) and all(
        not _check_fields(a, TEXT_OWNER_REQUIRED) and a.get("owner_entity_candidate_ref")
        for a in assignments
    )

    relation_types = {r.get("relation_type_candidate") for r in relations}
    checks["occlusion_overlap_attached_supported"] = "occludes" in relation_types

    passed = sum(1 for v in checks.values() if v)
    failed = sum(1 for v in checks.values() if not v)

    return {
        "review_id": "document_surface_detector_contract_review_v1",
        "runtime_id": RUNTIME_ID,
        "checks": checks,
        "review_passed_count": passed,
        "review_failed_count": failed,
        "failures": failures,
        "passed": failed == 0 and not failures,
        "candidate_only": True,
        "not_fact": True,
    }
