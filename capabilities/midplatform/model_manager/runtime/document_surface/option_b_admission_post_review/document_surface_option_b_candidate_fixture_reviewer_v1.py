# -*- coding: utf-8 -*-
"""Document Surface — Option B candidate fixture reviewer v1."""

from __future__ import annotations

from typing import Any, Dict, List

REQUIRED_FIELDS = (
    "model_candidate_id",
    "family_type",
    "capability",
    "output_types_allowed",
    "output_types_forbidden",
    "dependency_profile",
    "weight_profile",
    "license_status_candidate",
    "execution_mode_candidate",
    "local_runtime_possible",
    "external_runtime_possible",
    "expected_input",
    "expected_output",
    "candidate_only",
    "not_fact",
    "active_status",
    "controlled_execution_required",
    "preflight_required",
    "validation_required",
)


def review_candidate_fixtures(*, registry: Dict[str, Any]) -> Dict[str, Any]:
    fixtures: List[Dict[str, Any]] = registry.get("fixtures") or []
    per_fixture: List[Dict[str, Any]] = []
    all_ok = True
    for f in fixtures:
        missing = [k for k in REQUIRED_FIELDS if f.get(k) is None]
        ok = (
            len(missing) == 0
            and f.get("capability") == "detect_document_surface_mask_candidate"
            and f.get("candidate_only") is True
            and f.get("not_fact") is True
            and f.get("active_status") is False
            and f.get("controlled_execution_required") is True
            and f.get("preflight_required") is True
            and f.get("validation_required") is True
        )
        if not ok:
            all_ok = False
        per_fixture.append({
            "model_candidate_id": f.get("model_candidate_id"),
            "complete": ok,
            "missing_fields": missing,
        })
    checks = {
        "fixture_count_8": len(fixtures) == 8,
        "all_fields_complete": all_ok,
        "all_active_status_false": all(f.get("active_status") is False for f in fixtures),
        "all_candidate_only": all(f.get("candidate_only") is True for f in fixtures),
        "all_not_fact": all(f.get("not_fact") is True for f in fixtures),
    }
    failed = [k for k, v in checks.items() if not v]
    return {
        "review_id": "option_b_candidate_fixture_review",
        "passed": len(failed) == 0,
        "review_passed_count": sum(1 for v in checks.values() if v),
        "review_failed_count": len(failed),
        "checks": checks,
        "failed_checks": failed,
        "per_fixture": per_fixture,
        "fixture_count": len(fixtures),
        "candidate_only": True,
        "not_fact": True,
    }
