# -*- coding: utf-8 -*-
"""Document Surface — Option B runtime trace check plan v1."""

from __future__ import annotations

from typing import Any, Dict, List

TRACE_FIELDS = [
    "preflight_run_id",
    "candidate_id",
    "protocol_refs",
    "dependency_check_result",
    "weight_check_result",
    "license_check_result",
    "input_boundary_result",
    "output_boundary_result",
    "normalization_check_result",
    "schema_check_result",
    "leak_check_result",
    "abort_reason",
    "rollback_action",
    "execution_performed",
    "segmentation_performed",
    "active_model_selected",
    "active_registry_updated",
]


def build_runtime_trace_check_plan() -> Dict[str, Any]:
    return {
        "plan_id": "option_b_runtime_trace_check_plan_v1",
        "check_type": "runtime_trace_check",
        "output_type": "runtime_trace_check_candidate",
        "required_trace_fields": TRACE_FIELDS,
        "frozen_defaults": {
            "execution_performed": False,
            "segmentation_performed": False,
            "active_model_selected": False,
            "active_registry_updated": False,
        },
        "evidence_chain_contract": "LUNA-PROTO-L1-PROTOCOL-TRACEABILITY-GOVERNANCE-V1",
        "candidate_only": True,
        "not_fact": True,
    }
