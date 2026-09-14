# -*- coding: utf-8 -*-
"""Document Surface — controlled execution metrics v1."""

from __future__ import annotations

from typing import Any, Dict, List


def compute_controlled_execution_metrics(
    *,
    case_results: List[Dict[str, Any]],
    traces: List[Dict[str, Any]],
    fixture_audit: Dict[str, Any],
) -> Dict[str, Any]:
    total = len(case_results)
    executed = sum(1 for c in case_results if c.get("executed") is True)
    aborted = sum(1 for c in case_results if c.get("abort_status") == "aborted")
    surface_count = sum(len((c.get("candidate_outputs") or {}).get("document_surface_candidates") or []) for c in case_results)
    low_conf = sum(
        1 for c in case_results
        for s in ((c.get("candidate_outputs") or {}).get("document_surface_candidates") or [])
        if s.get("low_confidence_boundary_candidate")
    )
    relation_count = sum(len((c.get("candidate_outputs") or {}).get("relation_hint_candidates") or []) for c in case_results)

    schema_pass = sum(1 for c in case_results if c.get("validation", {}).get("schema_compliant") is True)
    no_ocr = sum(1 for c in case_results if c.get("validation", {}).get("no_ocr_leak") is True)
    no_fact = sum(1 for c in case_results if c.get("validation", {}).get("no_fact_output") is True)
    no_fallback = sum(1 for c in case_results if c.get("validation", {}).get("no_fallback") is True)

    attention_blocked = [c for c in case_results if c.get("case_id") == "case_f_attention_blocked_controlled"]
    attn_zero = all(c.get("runtime_call_count", 1) == 0 for c in attention_blocked) if attention_blocked else True

    trace_complete = sum(1 for t in traces if t.get("trace_complete") is True)
    output_boundary_ok = all(t.get("output_boundary_status") == "controlled_tmp_only" for t in traces) if traces else True
    protocol_ok = all(c.get("protocol_compliance_passed", True) for c in case_results)

    denom = max(1, total)
    return {
        "total_registry_cases": fixture_audit.get("total_registry_entries", 0),
        "executed_case_count": executed,
        "aborted_case_count": aborted,
        "surface_candidate_count": surface_count,
        "low_confidence_candidate_count": low_conf,
        "relation_hint_candidate_count": relation_count,
        "candidate_schema_compliance_rate": round(schema_pass / denom, 4),
        "no_ocr_leak_rate": round(no_ocr / denom, 4),
        "no_fact_output_rate": round(no_fact / denom, 4),
        "no_fallback_rate": round(no_fallback / denom, 4),
        "attention_blocked_runtime_call_rate": 0.0 if attn_zero else 1.0,
        "trace_completeness_rate": round(trace_complete / max(1, len(traces)), 4),
        "output_boundary_compliance_rate": 1.0 if output_boundary_ok else 0.0,
        "protocol_compliance_rate": round(sum(1 for c in case_results if c.get("protocol_compliance_passed", True)) / denom, 4),
        "fixture_execution_ready": fixture_audit.get("execution_fixtures_ready") is True,
        "blocked_by_missing_fixtures": fixture_audit.get("blocked_by_missing_fixtures") is True,
        "candidate_only": True,
        "not_fact": True,
    }
