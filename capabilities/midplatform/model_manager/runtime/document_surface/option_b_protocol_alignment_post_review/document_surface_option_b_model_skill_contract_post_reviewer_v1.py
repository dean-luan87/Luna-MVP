# -*- coding: utf-8 -*-
"""Document Surface — Option B Model/Skill contract post-reviewer v1."""

from __future__ import annotations

from typing import Any, Dict, List

PRIMARY = "LUNA-PROTO-L1-MODEL-SKILL-ADMISSION-CONTRACT-V1"
PREFLIGHT_IDS = frozenset({
    "family_a_classical_helper_ok_candidate",
    "family_c_document_specific_surface_model_ok_for_preflight",
})
REQUIRED_RECORD_FIELDS = (
    "protocol_ref", "model_admitted", "skill_admitted", "candidate_only", "not_fact",
    "active_model", "active_skill", "active_registry_update_allowed",
    "preflight_required", "controlled_execution_required", "validation_required",
)


def review_model_skill_contract(*, contract_results: Dict[str, Any]) -> Dict[str, Any]:
    records: List[Dict[str, Any]] = contract_results.get("records") or []
    per: List[Dict[str, Any]] = []
    all_ok = True
    for rec in records:
        cid = rec.get("model_candidate_id")
        model = rec.get("model_candidate_admission_record") or {}
        skill = rec.get("skill_candidate_admission_record") or {}
        is_preflight = cid in PREFLIGHT_IDS
        is_blocked = model.get("record_type") == "rejected_or_blocked_admission_record"
        ok = (
            len(records) == 8
            and model.get("protocol_ref") == PRIMARY
            and skill.get("protocol_ref") == PRIMARY
            and all(model.get(f) is not None for f in REQUIRED_RECORD_FIELDS if f in model)
            and model.get("model_admitted") is False
            and model.get("skill_admitted") is False
            and model.get("active_model") is False
            and model.get("active_skill") is False
            and (is_preflight == (model.get("record_type") == "preflight_candidate"))
            and (not is_preflight or not is_blocked)
        )
        if is_blocked:
            ok = ok and all([
                model.get("abort_reason"), model.get("next_action"),
                model.get("forbidden_workaround"), model.get("rollback_action"),
            ])
        if not ok:
            all_ok = False
        per.append({"model_candidate_id": cid, "passed": ok, "record_type": model.get("record_type")})
    checks = {
        "count_8": len(records) == 8,
        "all_records_valid": all_ok,
        "preflight_2": sum(1 for p in per if p.get("record_type") == "preflight_candidate") == 2,
        "blocked_6": sum(1 for p in per if p.get("record_type") == "rejected_or_blocked_admission_record") == 6,
        "not_model_admitted": all(
            (r.get("model_candidate_admission_record") or {}).get("model_admitted") is False for r in records
        ),
    }
    failed = [k for k, v in checks.items() if not v]
    return {
        "review_id": "option_b_model_skill_contract_post_review",
        "passed": len(failed) == 0,
        "review_passed_count": sum(1 for v in checks.values() if v),
        "review_failed_count": len(failed),
        "checks": checks,
        "failed_checks": failed,
        "per_candidate": per,
        "interpretation": "A1/C1 preflight_candidate only; not model/skill/runtime admitted",
        "candidate_only": True,
        "not_fact": True,
    }
