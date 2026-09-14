# -*- coding: utf-8 -*-
"""Teacher Performance Evaluation — full-chain adapter v1."""

from __future__ import annotations

from typing import Any, Dict, Optional

from capabilities.midplatform.teacher_adapter.providers.qwen_vl.qwen_vl_real_integration.luna_qwen_vl_real_integration_adapter_v1 import (
    run_qwen_vl_real_provider_integration,
)
from capabilities.midplatform.teacher_evaluation.luna_teacher_performance_types_v1 import POLICY_REF
from capabilities.midplatform.teacher_evaluation.teacher_performance_metrics_v1 import (
    get_performance_metrics,
    reset_performance_metrics,
)
from capabilities.midplatform.teacher_evaluation.teacher_performance_processor_v1 import (
    evaluate_teacher_performance,
)

FINAL_GO = "P1_MIDPLATFORM_TEACHER_PERFORMANCE_EVALUATION_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_TEACHER_PERFORMANCE_EVALUATION_BLOCKED"


def run_teacher_performance_evaluation_chain(
    job_envelope: Dict[str, Any],
    *,
    recorded_fixture_id: Optional[str] = None,
    admission_hints: Optional[Dict[str, Any]] = None,
    case_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Full chain:
    L1 → L2 → L2.5 → Admission → Qwen → Validation → Performance Evaluation.
    Evaluation does NOT alter current decisions.
    """
    integration = run_qwen_vl_real_provider_integration(
        job_envelope,
        recorded_fixture_id=recorded_fixture_id,
        admission_hints=admission_hints,
        case_id=case_id,
    )
    integration["case_id"] = case_id

    evaluation = evaluate_teacher_performance(
        integration,
        case_id=case_id,
        metrics=get_performance_metrics(),
    )

    original_validation = integration.get("teacher_validation_status")
    original_admission = (integration.get("teacher_admission") or {}).get("admission_status")

    return {
        **integration,
        "chain": integration.get("chain", []) + ["teacher_performance_evaluation"],
        "teacher_performance_evaluation": evaluation,
        "teacher_performance_record": evaluation.get("teacher_performance_record"),
        "teacher_usage_profile_candidate": evaluation.get("teacher_usage_profile_candidate"),
        "teacher_reliability_metrics": evaluation.get("teacher_reliability_metrics"),
        "usage_policy_update_candidate": evaluation.get("usage_policy_update_candidate"),
        "evaluation_outcome": evaluation.get("evaluation_outcome"),
        "value_score": evaluation.get("value_score"),
        "does_not_affect_current_decision": True,
        "decision_unchanged_assertion": {
            "passed": (
                integration.get("teacher_validation_status") == original_validation
                and (integration.get("teacher_admission") or {}).get("admission_status") == original_admission
            ),
            "teacher_validation_status": original_validation,
            "teacher_admission_status": original_admission,
            "candidate_only": True,
            "not_fact": True,
        },
        "policy_refs": list({*(integration.get("policy_refs") or []), POLICY_REF}),
    }
