from __future__ import annotations

from typing import Any, Dict, Iterable, Tuple


def build_module_diagnostics_v1(
    *,
    stage_reached: str,
    failed_stage: str,
    evaluation_status: str,
    selection_status: str,
    reduction_status: str,
    transition_status: str,
    conflict_status: str,
    overlay_status: str,
    missing_inputs: Iterable[str],
    rejection_reasons: Iterable[str],
    warnings: Iterable[str],
    invariant_violations: Iterable[str],
    component_versions: Dict[str, str],
) -> Dict[str, Any]:
    missing_inputs_t = tuple(dict.fromkeys(missing_inputs))
    rejection_reasons_t = tuple(dict.fromkeys(rejection_reasons))
    invariant_violations_t = tuple(dict.fromkeys(invariant_violations))

    return {
        "stage_reached": stage_reached,
        "failed_stage": failed_stage,
        "evaluation_status": evaluation_status,
        "selection_status": selection_status,
        "reduction_status": reduction_status,
        "transition_status": transition_status,
        "conflict_status": conflict_status,
        "overlay_status": overlay_status,
        "missing_inputs": list(missing_inputs_t),
        "rejection_reasons": list(rejection_reasons_t),
        "warnings": list(dict.fromkeys(warnings)),
        "invariant_violations": list(invariant_violations_t),
        "boundary_flags": {
            "candidate_only": True,
            "fact_admitted": False,
            "state_store_write_executed": False,
            "action_trigger_executed": False,
            "runtime_execution": False,
        },
        "component_versions": dict(component_versions),
    }
