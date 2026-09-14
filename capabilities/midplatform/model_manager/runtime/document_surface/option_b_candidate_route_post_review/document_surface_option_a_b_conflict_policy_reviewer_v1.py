# -*- coding: utf-8 -*-
"""Document Surface — Option A/B conflict policy reviewer v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


CONFLICT_REL = (
    "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_candidate_route_dryrun_v1/"
    "option_a_b_conflict_policy_summary.json"
)


def review_option_ab_conflict_policy(*, repo_root: Path) -> Dict[str, Any]:
    conflicts: List[Dict[str, Any]] = json.loads((repo_root / CONFLICT_REL).read_text(encoding="utf-8")) if (repo_root / CONFLICT_REL).is_file() else []
    conflict_cases = [c for c in conflicts if c.get("conflict_detected")]
    checks = {
        "conflict_goes_validation_review": all(c.get("conflict_resolution") == "validation_review" for c in conflict_cases) if conflict_cases else True,
        "no_confidence_auto_override": all(c.get("confidence_auto_override") is False for c in conflicts),
        "no_silent_fallback": all(c.get("silent_fallback") is False for c in conflicts),
        "no_option_a_auto_replaced": all(c.get("option_a_auto_replaced") is False for c in conflicts),
        "no_option_b_silent_fallback": all(c.get("option_b_silent_fallback") is False for c in conflicts),
        "candidate_only": all(c.get("candidate_only") is True for c in conflicts),
    }
    failed = [k for k, v in checks.items() if not v]
    return {
        "review_id": "option_a_b_conflict_policy_review",
        "passed": len(failed) == 0,
        "review_passed_count": sum(1 for v in checks.values() if v),
        "review_failed_count": len(failed),
        "checks": checks,
        "failed_checks": failed,
        "candidate_only": True,
        "not_fact": True,
    }
