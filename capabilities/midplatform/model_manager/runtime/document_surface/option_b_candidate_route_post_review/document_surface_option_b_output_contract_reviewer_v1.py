# -*- coding: utf-8 -*-
"""Document Surface — Option B output contract reviewer v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

CONTRACT_REL = (
    "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_candidate_route_dryrun_v1/"
    "option_b_output_contract_summary.json"
)

EXPECTED_ALLOWED = {
    "surface_mask_candidate", "document_surface_candidate", "boundary_candidate",
    "partial_surface_candidate", "occlusion_surface_hint_candidate", "runtime_error_candidate",
}


def review_option_b_output_contract(*, repo_root: Path) -> Dict[str, Any]:
    contract = json.loads((repo_root / CONTRACT_REL).read_text(encoding="utf-8")) if (repo_root / CONTRACT_REL).is_file() else {}
    allowed = set(contract.get("allowed_output_types") or [])
    forbidden = set(contract.get("forbidden_output_types") or [])
    checks = {
        "allowed_types_complete": EXPECTED_ALLOWED.issubset(allowed),
        "forbidden_includes_ocr": "ocr_text" in forbidden,
        "forbidden_includes_fact": "final_owner_fact" in forbidden,
        "forbidden_includes_layout": "layout_semantic_fact" in forbidden,
        "forbidden_includes_relation_fact": "relation_fact" in forbidden,
        "contract_compliant": contract.get("contract_compliant") is True or bool(allowed),
    }
    failed = [k for k, v in checks.items() if not v]
    return {
        "review_id": "option_b_output_contract_review",
        "passed": len(failed) == 0,
        "review_passed_count": sum(1 for v in checks.values() if v),
        "review_failed_count": len(failed),
        "checks": checks,
        "failed_checks": failed,
        "candidate_only": True,
        "not_fact": True,
    }
