# -*- coding: utf-8 -*-
"""Document Surface — Option B route selection reviewer v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


ROUTES_REL = (
    "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_candidate_route_dryrun_v1/"
    "option_b_route_selection_summary.json"
)


def review_option_b_route_selection(*, repo_root: Path) -> Dict[str, Any]:
    routes: List[Dict[str, Any]] = json.loads((repo_root / ROUTES_REL).read_text(encoding="utf-8")) if (repo_root / ROUTES_REL).is_file() else []
    checks = {
        "no_execution_decision": all(r.get("execution_decision") is None for r in routes),
        "no_active_runtime_update": all(r.get("active_runtime_update") is None for r in routes),
        "no_direct_model_invocation": all(r.get("direct_model_invocation") is None for r in routes),
        "no_fallback_decision": all(r.get("fallback_decision") is None for r in routes),
        "route_reason_present": all(r.get("route_reason_candidate") for r in routes),
        "route_constraints_present": all(r.get("route_constraints") for r in routes),
        "not_silent_fallback": all((r.get("route_constraints") or {}).get("silent_fallback") is False for r in routes),
        "not_confidence_override": all((r.get("route_constraints") or {}).get("confidence_auto_override") is False for r in routes),
        "candidate_only": all(r.get("candidate_only") is True for r in routes),
    }
    failed = [k for k, v in checks.items() if not v]
    return {
        "review_id": "option_b_route_selection_review",
        "passed": len(failed) == 0,
        "review_passed_count": sum(1 for v in checks.values() if v),
        "review_failed_count": len(failed),
        "checks": checks,
        "failed_checks": failed,
        "candidate_only": True,
        "not_fact": True,
    }
