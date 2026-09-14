# -*- coding: utf-8 -*-
"""Luna Model Manager Multi-Provider Registry — smoke fixtures v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.model_manager.luna_model_manager_multi_provider_registry_types_v1 import (
    FINAL_BLOCKED,
    FINAL_GO,
    SMOKE_CASE_IDS,
)
from capabilities.midplatform.model_manager.registry.dryrun.multi_provider_registry_dryrun_adapter_v1 import (
    run_capability_mismatch_ocr_dryrun,
    run_provider_conflict_dryrun,
    run_provider_deprecation_routing_dryrun,
    run_provider_version_replacement_dryrun,
    run_same_capability_three_providers_dryrun,
)


def smoke_case_a_same_capability_three_providers() -> Dict[str, Any]:
    """Case A: unknown_scene_reasoning — three providers, selection only."""
    case_id = "case_a_same_capability_three_providers"
    result = run_same_capability_three_providers_dryrun()
    selection = result.get("provider_selection") or {}
    passed = (
        result.get("three_providers_present") is True
        and result.get("provider_selection_candidate") is True
        and result.get("execution_performed") is True
        and result.get("not_voting") is True
        and selection.get("capability_first") is True
        and len(selection.get("provider_scores") or []) >= 3
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def smoke_case_b_capability_mismatch_ocr() -> Dict[str, Any]:
    """Case B: precise_ocr — OCR selected, Qwen excluded."""
    case_id = "case_b_capability_mismatch_ocr_selected"
    result = run_capability_mismatch_ocr_dryrun()
    passed = (
        result.get("ocr_selected") is True
        and result.get("qwen_excluded") is True
        and result.get("capability_first") is True
        and result.get("ocr_highest_score") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def smoke_case_c_provider_version_replacement() -> Dict[str, Any]:
    """Case C: Qwen v1→v2 replacement, L1/L2 unchanged."""
    case_id = "case_c_provider_version_replacement"
    result = run_provider_version_replacement_dryrun()
    passed = (
        result.get("v2_active") is True
        and result.get("v1_deprecated") is True
        and result.get("l1_l2_unchanged") is True
        and result.get("family_id") == "qwen_vl"
        and len(result.get("family_versions") or []) >= 2
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def smoke_case_d_provider_conflict() -> Dict[str, Any]:
    """Case D: provider conflict — not auto-resolved."""
    case_id = "case_d_provider_conflict_not_auto_resolve"
    result = run_provider_conflict_dryrun()
    review = result.get("validation_review") or {}
    passed = (
        result.get("conflict_detected") is True
        and result.get("not_auto_resolved") is True
        and result.get("requires_validation") is True
        and review.get("not_auto_resolved") is True
        and result.get("no_fact_admission") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def smoke_case_e_provider_deprecation() -> Dict[str, Any]:
    """Case E: deprecated provider removed from routing."""
    case_id = "case_e_provider_deprecation_routing_removal"
    result = run_provider_deprecation_routing_dryrun()
    passed = (
        result.get("routing_auto_removed") is True
        and result.get("internvl_removed_from_routing") is True
        and result.get("fallback_selection") is not None
        and result.get("fallback_selection") != "internvl2_5"
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def run_all_smoke_cases() -> Dict[str, Any]:
    runners = [
        smoke_case_a_same_capability_three_providers,
        smoke_case_b_capability_mismatch_ocr,
        smoke_case_c_provider_version_replacement,
        smoke_case_d_provider_conflict,
        smoke_case_e_provider_deprecation,
    ]
    cases = [fn() for fn in runners]
    failed = [c["case_id"] for c in cases if not c.get("passed")]
    return {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Multi-Provider-Registry-v1-001",
        "registry_only": True,
        "smoke_case_ids": list(SMOKE_CASE_IDS),
        "smoke_cases": cases,
        "smoke_passed": sum(1 for c in cases if c.get("passed")),
        "smoke_case_count": len(cases),
        "failed_checks": failed,
        "capability_marketplace": True,
        "final_decision": FINAL_GO if not failed else FINAL_BLOCKED,
    }
