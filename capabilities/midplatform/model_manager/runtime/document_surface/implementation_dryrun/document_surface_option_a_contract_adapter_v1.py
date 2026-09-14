# -*- coding: utf-8 -*-
"""Option A — contract adapter v1."""

from __future__ import annotations

from typing import Any, Dict, Optional

from capabilities.midplatform.model_manager.runtime.document_surface.implementation_planning.document_surface_implementation_options_v1 import (
    FIRST_REAL_IMPLEMENTATION_CANDIDATE,
)
from capabilities.midplatform.model_manager.runtime.document_surface.implementation_planning.document_surface_real_runtime_contract_v1 import (
    build_implementation_input_contract,
    validate_contract_alignment,
)


def adapt_option_a_contract(
    *,
    source_region_id: str = "region_001",
    attention_gate_status: str = "allowed",
    goal_context: Optional[Dict[str, Any]] = None,
    field_context_candidate: Optional[Dict[str, Any]] = None,
    max_runtime_cost: str = "low",
) -> Dict[str, Any]:
    """Bridge implementation planning contract → Option A dryrun input."""
    contract = build_implementation_input_contract(
        source_region_id=source_region_id,
        attention_gate_status=attention_gate_status,
        goal_context=goal_context,
        field_context_candidate=field_context_candidate,
        max_runtime_cost=max_runtime_cost,
    )
    contract["implementation_option"] = FIRST_REAL_IMPLEMENTATION_CANDIDATE
    contract["implementation_mode_candidate"] = "classical_cv_boundary_v1"
    return contract


def verify_contract_for_dryrun(contract: Dict[str, Any]) -> Dict[str, Any]:
    """Verify contract fields required for dryrun."""
    required = (
        "source_region_id",
        "attention_gate_status",
        "goal_context",
        "allowed_capabilities",
        "forbidden_capabilities",
        "candidate_only",
    )
    missing = [k for k in required if k not in contract]
    return {
        "contract_usable": not missing,
        "missing_fields": missing,
        "candidate_only": contract.get("candidate_only") is True,
        "field_context_present": "field_context_candidate" in contract,
        "max_runtime_cost_present": "max_runtime_cost" in contract,
    }
