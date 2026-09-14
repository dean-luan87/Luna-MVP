from __future__ import annotations

from typing import Any, Dict, Iterable, Mapping, Sequence, Tuple


def build_task_manager_diagnostics_v1(
    *,
    step_results: Sequence[Mapping[str, Any]],
    rejection_reasons: Iterable[str],
    current_blocking_reasons: Iterable[str],
    historical_blocking_reasons: Iterable[str],
    trace_ref: str,
    replay_key: str,
) -> Dict[str, Any]:
    rejection = tuple(str(x) for x in rejection_reasons)
    current_blocking = tuple(str(x) for x in current_blocking_reasons)
    historical_blocking = tuple(str(x) for x in historical_blocking_reasons)
    return {
        "trace_ref": trace_ref,
        "replay_key": replay_key,
        "step_results": tuple(dict(x) for x in step_results),
        "rejection_reasons": rejection,
        "current_blocking_reasons": current_blocking,
        "historical_blocking_reasons": historical_blocking,
        "blocking_reasons": current_blocking,
        "diagnostic_status": "ok"
        if not rejection and not current_blocking
        else "attention_required",
        "candidate_only_processing": True,
        "action_execution_executed": False,
        "model_call_executed": False,
        "state_mutation_executed": False,
        "fact_promotion_executed": False,
        "runtime_dispatch_executed": False,
    }
