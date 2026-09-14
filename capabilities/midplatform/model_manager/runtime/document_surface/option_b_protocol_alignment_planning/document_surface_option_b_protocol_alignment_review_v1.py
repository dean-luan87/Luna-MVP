# -*- coding: utf-8 -*-
"""Document Surface — Option B protocol alignment review v1."""

from __future__ import annotations

from typing import Any, Dict


def build_protocol_alignment_review(*, mappings: Dict[str, Any]) -> Dict[str, Any]:
    contract = mappings.get("contract_mapping") or {}
    registry = mappings.get("registry_alignment") or {}
    dep = mappings.get("dependency_mapping") or {}
    output = mappings.get("output_mapping") or {}
    boundary = mappings.get("boundary_mapping") or {}
    change = mappings.get("change_control_mapping") or {}

    checks = {
        "primary_contract_mapped": contract.get("primary_contract") is not None,
        "chain_extension_not_new_branch": contract.get("existing_midplatform_protocol_chain_extension") is True
        and contract.get("protocol_patch_not_new_branch") is True,
        "local_admission_mounted_not_replaced": contract.get("local_admission_mounted") is True
        and contract.get("local_admission_replaces_contract") is False,
        "active_model_false": contract.get("option_b_status_under_contract", {}).get("active_model") is False,
        "active_skill_false": contract.get("option_b_status_under_contract", {}).get("active_skill") is False,
        "model_skill_admission_required": contract.get("option_b_status_under_contract", {}).get("model_skill_admission_required") is True,
        "registry_no_active_update": registry.get("active_registry_update_allowed") is False,
        "preflight_not_equal_admitted": registry.get("admitted_for_preflight_not_equal_model_admitted") is True,
        "dependency_gates_blocked": dep.get("all_install_blocked") is True and dep.get("all_execution_blocked") is True,
        "output_no_fact_promotion": output.get("no_fact_promotion") is True,
        "runtime_activation_blocked": (boundary.get("option_b_frozen_state") or {}).get("runtime_activation_allowed") is False,
        "boundary_frozen": change.get("boundary_status") == "frozen",
        "pipeline_includes_protocol_alignment": "Model / Skill Admission Protocol Alignment" in (change.get("adjusted_pipeline") or []),
    }
    failed = [k for k, v in checks.items() if not v]
    return {
        "review_id": "option_b_protocol_alignment_review_v1",
        "passed": len(failed) == 0,
        "review_passed_count": sum(1 for v in checks.values() if v),
        "review_failed_count": len(failed),
        "checks": checks,
        "failed_checks": failed,
        "candidate_only": True,
        "not_fact": True,
    }
