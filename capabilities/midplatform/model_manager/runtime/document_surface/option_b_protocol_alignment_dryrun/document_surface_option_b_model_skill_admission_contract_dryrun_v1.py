# -*- coding: utf-8 -*-
"""Document Surface — Option B Model/Skill Admission Contract dryrun v1."""

from __future__ import annotations

from typing import Any, Dict, List

PRIMARY_CONTRACT = "LUNA-PROTO-L1-MODEL-SKILL-ADMISSION-CONTRACT-V1"

PREFLIGHT_IDS = frozenset({
    "family_a_classical_helper_ok_candidate",
    "family_c_document_specific_surface_model_ok_for_preflight",
})


def _map_record(*, candidate: Dict[str, Any]) -> Dict[str, Any]:
    cid = candidate["model_candidate_id"]
    status = candidate.get("admission_status_candidate", "")
    abort = candidate.get("abort_rollback") or {}
    is_preflight = status == "admitted_for_preflight_candidate"
    is_blocked = status.startswith("blocked") or status == "blocked_or_requires_wrapper_candidate"

    model_record = {
        "record_type": "preflight_candidate" if is_preflight else "rejected_or_blocked_admission_record",
        "protocol_ref": PRIMARY_CONTRACT,
        "model_candidate_id": cid,
        "model_admitted": False,
        "skill_admitted": False,
        "runtime_admitted": False,
        "preflight_candidate": is_preflight,
        "candidate_only": True,
        "not_fact": True,
        "active_model": False,
        "active_skill": False,
        "active_registry_update_allowed": False,
        "preflight_required": True,
        "controlled_execution_required": True,
        "validation_required": True,
        "execution_allowed": False,
    }
    skill_record = {**model_record, "record_type": model_record["record_type"], "skill_candidate_id": cid}

    if is_blocked:
        model_record.update({
            "abort_reason": abort.get("abort_reason"),
            "next_action": abort.get("next_action"),
            "forbidden_workaround": abort.get("forbidden_workaround"),
            "rollback_action": abort.get("rollback_action"),
        })
        skill_record.update({
            "abort_reason": abort.get("abort_reason"),
            "next_action": abort.get("next_action"),
            "forbidden_workaround": abort.get("forbidden_workaround"),
            "rollback_action": abort.get("rollback_action"),
        })

    return {
        "model_candidate_id": cid,
        "admission_status_candidate": status,
        "model_candidate_admission_record": model_record,
        "skill_candidate_admission_record": skill_record,
        "mapping_valid": (
            model_record.get("model_admitted") is False
            and model_record.get("skill_admitted") is False
            and model_record.get("runtime_admitted") is False
            and model_record.get("active_registry_update_allowed") is False
            and (is_preflight == (cid in PREFLIGHT_IDS))
        ),
        "candidate_only": True,
        "not_fact": True,
    }


def run_model_skill_admission_contract_dryrun(*, admission_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    records = [_map_record(candidate=r) for r in admission_results]
    preflight = sum(1 for r in records if r["model_candidate_admission_record"].get("preflight_candidate"))
    blocked = sum(1 for r in records if r["model_candidate_admission_record"].get("record_type") == "rejected_or_blocked_admission_record")
    return {
        "dryrun_id": "option_b_model_skill_contract_mapping_dryrun_v1",
        "protocol_ref": PRIMARY_CONTRACT,
        "records": records,
        "candidate_count": len(records),
        "preflight_candidate_count": preflight,
        "blocked_admission_record_count": blocked,
        "all_mapped": len(records) == 8 and all(r.get("mapping_valid") for r in records),
        "candidate_only": True,
        "not_fact": True,
    }
