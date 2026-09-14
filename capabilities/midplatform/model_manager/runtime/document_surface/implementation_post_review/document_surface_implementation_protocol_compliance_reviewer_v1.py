# -*- coding: utf-8 -*-
"""Document Surface Implementation — protocol compliance reviewer v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from capabilities.midplatform.model_manager.runtime.document_surface.implementation_dryrun.document_surface_protocol_compliance_reviewer_v1 import (
    review_implementation_dryrun_protocol_compliance,
)

PROTOCOL_CHAIN = "capabilities/midplatform/protocols/region_intelligence_protocol_chain_v1.json"
PROTOCOL_PATCHES = "capabilities/midplatform/protocols/region_intelligence_protocol_patches_v1.json"
PROTOCOL_SUMMARY = (
    "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_implementation_dryrun_v1/"
    "option_a_protocol_compliance_summary.json"
)

LEGACY_CHECKS = (
    "candidate_fact_admission", "runtime_boundary_contract", "model_manager_registry",
    "attention_gate_protocol", "ownership_graph_protocol", "evidence_chain_traceability",
    "change_control_compliance",
)

PATCH_CHECKS = (
    "patch_field_understanding_patch", "patch_attention_gate_patch",
    "patch_ownership_graph_patch", "patch_lightweight_runtime_patch",
)


def review_protocol_compliance(*, repo_root: Path) -> Dict[str, Any]:
    chain = json.loads((repo_root / PROTOCOL_CHAIN).read_text(encoding="utf-8")) if (repo_root / PROTOCOL_CHAIN).is_file() else {}
    patches = json.loads((repo_root / PROTOCOL_PATCHES).read_text(encoding="utf-8")) if (repo_root / PROTOCOL_PATCHES).is_file() else {}
    summary_path = repo_root / PROTOCOL_SUMMARY
    saved_summary = json.loads(summary_path.read_text(encoding="utf-8")) if summary_path.is_file() else {}

    live = review_implementation_dryrun_protocol_compliance(repo_root=repo_root)
    sample_checks = (live.get("fixture_reviews") or [{}])[0].get("checks") or {}

    legacy_ok = all(sample_checks.get(k) for k in LEGACY_CHECKS)
    patch_ok = all(sample_checks.get(k) for k in PATCH_CHECKS)

    return {
        "review_id": "document_surface_implementation_protocol_compliance_review_v1",
        "protocol_compliance_check": "required",
        "existing_midplatform_protocol_chain_extension": True,
        "protocol_patch_not_new_branch": True,
        "governance_chain": chain.get("governance_chain"),
        "patch_count": len(patches.get("patches") or []),
        "saved_summary_passed": saved_summary.get("all_passed") is True,
        "live_review_passed": live.get("all_passed") is True,
        "legacy_protocol_checks_passed": legacy_ok,
        "patch_checks_passed": patch_ok,
        "protocol_compliance_passed": live.get("all_passed") is True and legacy_ok and patch_ok,
        "passed": live.get("all_passed") is True and legacy_ok and patch_ok,
    }
