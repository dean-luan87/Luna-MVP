# -*- coding: utf-8 -*-
"""Luna Ownership Real Runtime Integration — dryrun fixtures v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.model_manager.luna_model_manager_region_intelligence_ownership_real_runtime_dryrun_processor_v1 import (
    run_attention_blocked,
    run_glass_reflection,
    run_occluded_missing,
    run_runtime_failure,
    run_shelf_price_tags,
    run_stacked_papers,
)
from capabilities.midplatform.model_manager.luna_model_manager_region_intelligence_ownership_real_runtime_dryrun_types_v1 import (
    DRYRUN_CASE_IDS,
    FINAL_BLOCKED,
    FINAL_GO,
)


def _wrap(case_id: str, result: Dict[str, Any], checks: Dict[str, bool]) -> Dict[str, Any]:
    return {"case_id": case_id, "passed": all(checks.values()), "result": result, "checks": checks}


def dryrun_case_a() -> Dict[str, Any]:
    r = run_stacked_papers()
    return _wrap("case_a_stacked_papers", r, {
        "paper_a": r.get("paper_a") is True,
        "paper_b": r.get("paper_b") is True,
        "per_owner": r.get("per_owner_assignments") is True,
        "owner_req": r.get("owner_required") is True,
    })


def dryrun_case_b() -> Dict[str, Any]:
    r = run_shelf_price_tags()
    return _wrap("case_b_shelf_price_tags", r, {
        "product": r.get("product") is True,
        "price": r.get("price_tag") is True,
        "ad": r.get("bg_ad") is True,
        "three": r.get("three_owners") is True,
    })


def dryrun_case_c() -> Dict[str, Any]:
    r = run_glass_reflection()
    return _wrap("case_c_glass_reflection", r, {
        "real": r.get("real_sign") is True,
        "reflection": r.get("reflection_entity") is True,
        "relation": r.get("reflection_relation") is True,
        "not_real": r.get("reflection_not_real_sign") is True,
    })


def dryrun_case_d() -> Dict[str, Any]:
    r = run_attention_blocked()
    return _wrap("case_d_attention_blocked", r, {
        "blocked": r.get("has_blocked") is True,
        "no_ad": r.get("bg_ad_not_entity") is True,
        "product": r.get("product_processed") is True,
    })


def dryrun_case_e() -> Dict[str, Any]:
    r = run_occluded_missing()
    return _wrap("case_e_occluded_missing", r, {
        "missing": r.get("has_missing") is True,
        "occluded": r.get("occluded_reason") is True,
        "not_absent": r.get("not_assume_absent") is True,
    })


def dryrun_case_f() -> Dict[str, Any]:
    r = run_runtime_failure()
    return _wrap("case_f_runtime_failure", r, {
        "error": r.get("runtime_error") is True,
        "replan": r.get("replan") is True,
        "no_fallback": r.get("no_fallback") is True,
    })


def run_all_dryrun_cases() -> Dict[str, Any]:
    cases = [dryrun_case_a(), dryrun_case_b(), dryrun_case_c(), dryrun_case_d(), dryrun_case_e(), dryrun_case_f()]
    failed = [c["case_id"] for c in cases if not c.get("passed")]
    return {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Real-Runtime-Integration-DryRun-v1-001",
        "dryrun_only": True,
        "dryrun_case_ids": list(DRYRUN_CASE_IDS),
        "dryrun_cases": cases,
        "dryrun_passed": sum(1 for c in cases if c.get("passed")),
        "dryrun_case_count": len(cases),
        "failed_checks": failed,
        "final_decision": FINAL_GO if not failed else FINAL_BLOCKED,
    }
