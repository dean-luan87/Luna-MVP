# -*- coding: utf-8 -*-
"""Document Surface Option A — protocol compliance reviewer v1."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

from capabilities.midplatform.protocols.region_intelligence_protocol_compliance_checker_v1 import (
    check_region_intelligence_protocol_compliance,
)
from capabilities.midplatform.model_manager.runtime.document_surface.implementation_dryrun.document_surface_option_a_dryrun_adapter_v1 import (
    run_option_a_implementation_dryrun,
)


def review_implementation_dryrun_protocol_compliance(
    *,
    repo_root: Optional[Path] = None,
) -> Dict[str, Any]:
    """Run protocol compliance review against Option A implementation dryrun samples."""
    sample = run_option_a_implementation_dryrun(fixture_ref="single_flat_paper")
    overlap = run_option_a_implementation_dryrun(fixture_ref="two_overlapping_papers")
    screen = run_option_a_implementation_dryrun(fixture_ref="document_on_screen")
    blocked = run_option_a_implementation_dryrun(
        fixture_ref="single_flat_paper",
        attention_gate_status="blocked",
    )
    error = run_option_a_implementation_dryrun(
        fixture_ref="single_flat_paper",
        runtime_error_mode="runtime_dependency_missing",
    )

    reviews: List[Dict[str, Any]] = []
    for label, dr, blk in (
        ("single_flat_paper", sample, blocked),
        ("two_overlapping_papers", overlap, blocked),
        ("document_on_screen", screen, blocked),
    ):
        reviews.append({
            "fixture_ref": label,
            **check_region_intelligence_protocol_compliance(
                dryrun_result=dr,
                blocked_result=blocked,
                repo_root=repo_root,
            ),
        })

    error_review = check_region_intelligence_protocol_compliance(
        dryrun_result=error,
        blocked_result=blocked,
        repo_root=repo_root,
    )

    all_passed = all(r.get("passed") for r in reviews) and error_review.get("passed", False)

    return {
        "review_id": "document_surface_option_a_protocol_compliance_v1",
        "protocol_compliance_check": "required",
        "fixture_reviews": reviews,
        "error_path_review": error_review,
        "all_passed": all_passed,
        "candidate_only": True,
        "not_fact": True,
    }
