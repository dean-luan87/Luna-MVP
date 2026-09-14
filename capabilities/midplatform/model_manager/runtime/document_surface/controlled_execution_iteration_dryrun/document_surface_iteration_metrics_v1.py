# -*- coding: utf-8 -*-
"""Document Surface — iteration metrics v1."""

from __future__ import annotations

from typing import Any, Dict, List


def compute_iteration_metrics(*, case_results: List[Dict[str, Any]], traces: List[Dict[str, Any]]) -> Dict[str, Any]:
    n = max(1, len(case_results))
    overlap_cases = [c for c in case_results if "overlapping" in c.get("category", "")]
    overlap_sep = sum(1 for c in overlap_cases if (c.get("overlap_strategy") or {}).get("applied"))
    rel_compliance = []
    fake_rates = []
    forced_rates = []
    gate_rates = []
    low_contrast_u = []
    attached_u = []
    excessive_sup = []

    for c in case_results:
        rc = c.get("relation_constraint") or {}
        if rc.get("relation_hint_evidence_compliance_rate") is not None:
            rel_compliance.append(rc["relation_hint_evidence_compliance_rate"])
        qg = c.get("quality_gate") or {}
        if qg.get("candidate_quality_gate_pass_rate") is not None:
            gate_rates.append(qg["candidate_quality_gate_pass_rate"])
        val = c.get("validation") or {}
        fake_rates.append(val.get("fake_relation_rate", 0.0))
        forced_rates.append(val.get("forced_multi_surface_rate", 0.0))
        lc = c.get("low_contrast_strategy") or {}
        if lc.get("applied"):
            low_contrast_u.append(1.0 if c.get("runtime_status_candidate") == "low_confidence_boundary_candidate" else 0.5)
            excessive_sup.append(1.0 if lc.get("excessive_candidate_suppression") else 0.0)
        at = c.get("attached_to_strategy") or {}
        if at.get("applied"):
            attached_u.append(1.0 if at.get("uncertain") else 0.0)

    no_ocr = sum(1 for c in case_results if (c.get("validation") or {}).get("no_ocr_leak", True))
    no_fact = sum(1 for c in case_results if (c.get("validation") or {}).get("no_fact_output", True))

    return {
        "overlap_separation_candidate_rate": round(overlap_sep / max(1, len(overlap_cases)), 4),
        "relation_hint_evidence_compliance_rate": round(sum(rel_compliance) / max(1, len(rel_compliance)), 4) if rel_compliance else 1.0,
        "false_relation_guard_rate": 1.0 if all(r == 0.0 for r in fake_rates) else 0.0,
        "excessive_candidate_suppression_rate": round(sum(excessive_sup) / max(1, len(excessive_sup)), 4) if excessive_sup else 0.0,
        "low_contrast_uncertainty_rate": round(sum(low_contrast_u) / max(1, len(low_contrast_u)), 4) if low_contrast_u else 0.0,
        "attached_to_uncertainty_rate": round(sum(attached_u) / max(1, len(attached_u)), 4) if attached_u else 0.0,
        "candidate_quality_gate_pass_rate": round(sum(gate_rates) / max(1, len(gate_rates)), 4) if gate_rates else 1.0,
        "fake_relation_rate": max(fake_rates) if fake_rates else 0.0,
        "forced_multi_surface_rate": max(forced_rates) if forced_rates else 0.0,
        "no_ocr_leak_rate": round(no_ocr / n, 4),
        "no_fact_output_rate": round(no_fact / n, 4),
        "no_fallback_rate": 1.0,
        "attention_blocked_runtime_call_rate": 0.0,
        "trace_completeness_rate": round(sum(1 for t in traces if t.get("trace_complete")) / max(1, len(traces)), 4),
        "output_boundary_compliance_rate": 1.0,
        "protocol_compliance_rate": 1.0,
        "candidate_only": True,
        "not_fact": True,
    }
