# -*- coding: utf-8 -*-
"""Document Surface — Option B evidence chain post-reviewer v1."""

from __future__ import annotations

from typing import Any, Dict


def review_evidence_chain(*, evidence_results: Dict[str, Any]) -> Dict[str, Any]:
    records = evidence_results.get("records") or []
    checks = {
        "admission_refs_preserved": evidence_results.get("admission_refs_preserved") is True,
        "protocol_refs_preserved": evidence_results.get("protocol_refs_preserved") is True,
        "preservation_rate_1": evidence_results.get("evidence_chain_preservation_rate") == 1.0,
        "not_execution_result": all(r.get("admission_not_execution_result") is True for r in records),
        "active_false_preserved": all(r.get("active_status_preserved_false") is True for r in records),
        "trace_retained": all(r.get("trace_retained") is True for r in records),
    }
    failed = [k for k, v in checks.items() if not v]
    return {
        "review_id": "option_b_evidence_chain_post_review",
        "passed": len(failed) == 0,
        "review_passed_count": sum(1 for v in checks.values() if v),
        "review_failed_count": len(failed),
        "checks": checks,
        "failed_checks": failed,
        "candidate_only": True,
        "not_fact": True,
    }
