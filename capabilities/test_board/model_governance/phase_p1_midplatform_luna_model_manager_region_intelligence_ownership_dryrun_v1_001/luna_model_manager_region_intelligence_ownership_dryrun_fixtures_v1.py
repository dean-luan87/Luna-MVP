# -*- coding: utf-8 -*-
"""Luna Region Intelligence Ownership — dryrun smoke fixtures v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.model_manager.luna_model_manager_region_intelligence_ownership_dryrun_processor_v1 import (
    run_channel_conflict_same_region,
    run_missing_information_occlusion,
    run_ownership_first_stacked_menus,
    run_ownership_graph_structure,
    run_runtime_unavailable_replan,
    run_selective_channel_not_all_models,
)
from capabilities.midplatform.model_manager.luna_model_manager_region_intelligence_ownership_dryrun_types_v1 import (
    DRYRUN_CASE_IDS,
    FINAL_BLOCKED,
    FINAL_GO,
)


def _wrap(case_id: str, result: Dict[str, Any], checks: Dict[str, bool]) -> Dict[str, Any]:
    return {"case_id": case_id, "passed": all(checks.values()), "result": result, "checks": checks}


def dryrun_case_a() -> Dict[str, Any]:
    r = run_ownership_first_stacked_menus()
    return _wrap("case_a_ownership_first_stacked_menus", r, {
        "discovery_first": r.get("entity_discovery_first") is True,
        "two_entities": r.get("two_entities") is True,
        "per_entity_ocr": r.get("ocr_per_entity_only") is True,
        "not_global": r.get("not_global_ocr") is True,
    })


def dryrun_case_b() -> Dict[str, Any]:
    r = run_missing_information_occlusion()
    return _wrap("case_b_missing_information_occlusion", r, {
        "missing": r.get("has_missing_candidate") is True,
        "occluded": r.get("occluded_reason") is True,
        "not_absent": r.get("not_assume_absent") is True,
        "completeness": r.get("completeness_not_confidence") is True,
    })


def dryrun_case_c() -> Dict[str, Any]:
    r = run_channel_conflict_same_region()
    return _wrap("case_c_channel_conflict_same_region", r, {
        "conflict": r.get("semantic_conflict") is True,
        "not_merged": r.get("not_merged_answer") is True,
        "need_evidence": r.get("need_more_evidence") is True,
    })


def dryrun_case_d() -> Dict[str, Any]:
    r = run_selective_channel_not_all_models()
    return _wrap("case_d_selective_channel_not_all_models", r, {
        "selective": r.get("not_all_models_started") is True,
        "noop": r.get("noop_capabilities_exist") is True,
        "not_global": r.get("not_global_activation") is True,
    })


def dryrun_case_e() -> Dict[str, Any]:
    r = run_ownership_graph_structure()
    return _wrap("case_e_ownership_graph_structure", r, {
        "entities": r.get("has_entity_candidates") is True,
        "relations": r.get("has_relation_candidates") is True,
        "occlusion": r.get("occlusion_relation") is True,
        "structure": r.get("not_flat_structure") is True,
    })


def dryrun_case_f() -> Dict[str, Any]:
    r = run_runtime_unavailable_replan()
    return _wrap("case_f_runtime_unavailable_replan", r, {
        "unavailable": r.get("runtime_unavailable") is True,
        "no_fallback": r.get("not_global_fallback") is True,
        "validation": r.get("validation_error") is True,
    })


def run_all_dryrun_cases() -> Dict[str, Any]:
    cases = [dryrun_case_a(), dryrun_case_b(), dryrun_case_c(), dryrun_case_d(), dryrun_case_e(), dryrun_case_f()]
    failed = [c["case_id"] for c in cases if not c.get("passed")]
    return {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-DryRun-v1-001",
        "dryrun_only": True,
        "information_ownership_graph": True,
        "not_global_model_activation": True,
        "dryrun_case_ids": list(DRYRUN_CASE_IDS),
        "dryrun_cases": cases,
        "dryrun_passed": sum(1 for c in cases if c.get("passed")),
        "dryrun_case_count": len(cases),
        "failed_checks": failed,
        "final_decision": FINAL_GO if not failed else FINAL_BLOCKED,
    }
