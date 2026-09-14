# -*- coding: utf-8 -*-
"""Option A — failure mode simulator v1."""

from __future__ import annotations

from typing import Any, Dict, List

from capabilities.midplatform.model_manager.runtime.document_surface.implementation_planning.document_surface_real_runtime_failure_modes_v1 import (
    FAILURE_MODES,
)

FAILURE_MODE_MAP = {fm["failure_mode_id"]: fm for fm in FAILURE_MODES}


def simulate_failure_mode(failure_mode_id: str) -> Dict[str, Any]:
    """Simulate a single failure mode from implementation planning registry."""
    fm = FAILURE_MODE_MAP.get(failure_mode_id)
    if not fm:
        return {
            "failure_mode_id": failure_mode_id,
            "simulated": False,
            "candidate_only": True,
        }
    return {
        "failure_mode_id": failure_mode_id,
        "simulated": True,
        "error_or_uncertainty_candidate": fm.get("output_candidate"),
        "validation_status_candidate": fm.get("validation_status"),
        "next_action_candidate": fm.get("next_action"),
        "forbidden_fallbacks": fm.get("forbidden_fallback"),
        "candidate_only": True,
        "not_fact": True,
    }


def simulate_all_failure_modes() -> Dict[str, Any]:
    """Simulate all 11 failure modes from implementation planning."""
    results = [simulate_failure_mode(fm["failure_mode_id"]) for fm in FAILURE_MODES]
    complete = all(r.get("simulated") and r.get("error_or_uncertainty_candidate") for r in results)
    return {
        "simulator_id": "option_a_failure_mode_simulator_v1",
        "failure_mode_count": len(FAILURE_MODES),
        "simulated_count": sum(1 for r in results if r.get("simulated")),
        "all_modes_simulated": complete and len(results) >= 11,
        "simulations": results,
        "candidate_only": True,
        "not_fact": True,
    }
