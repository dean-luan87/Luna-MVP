from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.field_perception_orchestrator.integration.field_perception_handoff_diagnostics_v1 import (
    build_visual_handoff_diagnostics_v1,
)
from capabilities.midplatform.field_perception_orchestrator.integration.field_perception_handoff_trace_replay_v1 import (
    build_visual_handoff_trace_replay_v1,
)
from capabilities.midplatform.field_perception_orchestrator.integration.field_perception_invocation_budget_guard_v1 import (
    build_invocation_budget_guard_v1,
)
from capabilities.midplatform.field_perception_orchestrator.integration.field_perception_invocation_deduplication_v1 import (
    build_invocation_deduplication_v1,
)
from capabilities.midplatform.field_perception_orchestrator.integration.field_perception_invocation_history_resolver_v1 import (
    resolve_invocation_history_v1,
)
from capabilities.midplatform.field_perception_orchestrator.integration.field_perception_invocation_result_linker_v1 import (
    build_result_link_contract_v1,
)
from capabilities.midplatform.field_perception_orchestrator.integration.field_perception_model_candidate_binding_v1 import (
    build_model_candidate_binding_v1,
)
from capabilities.midplatform.field_perception_orchestrator.integration.field_perception_to_model_manager_requirement_adapter_v1 import (
    build_model_requirement_candidate_v1,
)
from capabilities.midplatform.field_perception_orchestrator.integration.field_perception_to_observation_request_adapter_v1 import (
    build_observation_request_candidate_v1,
)
from capabilities.midplatform.field_perception_orchestrator.integration.field_perception_to_vision_manager_adapter_v1 import (
    build_vision_request_candidate_v1,
)
from capabilities.midplatform.field_perception_orchestrator.integration.field_perception_visual_handoff_output_builder_v1 import (
    build_visual_handoff_result_v1,
    resolve_integration_status_v1,
)
from capabilities.midplatform.field_perception_orchestrator.integration.field_perception_visual_invocation_contract_v1 import (
    CAPABILITY_ID,
    not_fact,
)
from capabilities.midplatform.field_perception_orchestrator.integration.field_perception_visual_invocation_input_adapter_v1 import (
    adapt_field_perception_visual_handoff_input_v1,
)


def run_field_perception_visual_handoff_integration_v1(
    payload: Mapping[str, Any],
) -> Dict[str, Any]:
    try:
        input_candidate = adapt_field_perception_visual_handoff_input_v1(payload)
        history_resolution = resolve_invocation_history_v1(input_candidate)
        deduplication_result = build_invocation_deduplication_v1(history_resolution)
        budget_decision = build_invocation_budget_guard_v1(input_candidate)

        vision_request_candidate = None
        vision_manager_preview = None
        model_requirement_candidate = None
        eligible_model_candidates: tuple[Mapping[str, Any], ...] = tuple()
        rejected_model_candidates: tuple[Mapping[str, Any], ...] = tuple()
        fallback_model_candidates: tuple[Mapping[str, Any], ...] = tuple()
        model_manager_result = {}
        result_link_contract = None
        observation_request_candidate = None
        observation_manager_preview = None
        rejection_reasons: list[str] = list(
            input_candidate.get("rejection_reasons") or ()
        )

        handoff_id = (
            f"handoff::{input_candidate.get('handoff_request_id') or 'unknown'}"
        )
        integration_status = resolve_integration_status_v1(
            input_candidate,
            deduplication_result,
            budget_decision,
            eligible_model_candidates,
            observation_request_candidate,
        )

        if integration_status not in {
            "invalid_input",
            "permission_rejected",
            "conflicted",
            "no_visual_invocation_required",
            "duplicate_suppressed",
            "fresh_evidence_reused",
            "insufficient_plan",
        }:
            effective_caps = tuple(
                (budget_decision.get("budget_decision") or {}).get(
                    "effective_capability_plan"
                )
                or input_candidate.get("requested_visual_capabilities")
                or ()
            )
            input_runtime = dict(input_candidate)
            input_runtime["requested_visual_capabilities"] = effective_caps
            input_runtime["resolution_level"] = (
                budget_decision.get("budget_decision") or {}
            ).get("effective_resolution_level") or input_candidate.get(
                "resolution_level"
            )

            vr = build_vision_request_candidate_v1(input_runtime)
            vision_request_candidate = vr["vision_request_candidate"]
            vision_manager_preview = vr["vision_manager_preview"]

            model_requirement_candidate = build_model_requirement_candidate_v1(
                input_runtime
            )
            binding = build_model_candidate_binding_v1(
                input_runtime, model_requirement_candidate
            )
            eligible_model_candidates = tuple(
                binding.get("eligible_model_candidates") or ()
            )
            rejected_model_candidates = tuple(
                binding.get("rejected_model_candidates") or ()
            )
            fallback_model_candidates = tuple(
                binding.get("fallback_model_candidates") or ()
            )
            model_manager_result = dict(binding.get("model_manager_result") or {})

            trace_seed = build_visual_handoff_trace_replay_v1(
                input_candidate, "model_requirement_candidate_ready"
            )
            result_link_contract = build_result_link_contract_v1(
                input_candidate,
                handoff_id,
                str(
                    vision_request_candidate.get("vision_request_id")
                    if vision_request_candidate
                    else ""
                ),
                str(
                    model_requirement_candidate.get("requirement_id")
                    if model_requirement_candidate
                    else ""
                ),
                f"obs_req::{input_candidate.get('plan_id')}",
                str(trace_seed.get("trace_ref") or ""),
                str(trace_seed.get("replay_key") or ""),
            )

            if eligible_model_candidates:
                oa = build_observation_request_candidate_v1(
                    input_runtime,
                    vision_request_candidate,
                    model_requirement_candidate,
                    eligible_model_candidates,
                    result_link_contract,
                )
                observation_request_candidate = oa["observation_request_candidate"]
                observation_manager_preview = oa["observation_manager_preview"]
            else:
                rejection_reasons.append("no_eligible_model")

            integration_status = resolve_integration_status_v1(
                input_candidate,
                deduplication_result,
                budget_decision,
                eligible_model_candidates,
                observation_request_candidate,
            )

        trace = build_visual_handoff_trace_replay_v1(
            input_candidate, integration_status
        )
        if result_link_contract is None and integration_status in {
            "duplicate_suppressed",
            "fresh_evidence_reused",
            "no_visual_invocation_required",
        }:
            result_link_contract = build_result_link_contract_v1(
                input_candidate,
                handoff_id,
                "",
                "",
                "",
                str(trace.get("trace_ref") or ""),
                str(trace.get("replay_key") or ""),
            )

        diagnostics = build_visual_handoff_diagnostics_v1(
            input_candidate,
            integration_status,
            deduplication_result,
            budget_decision,
            eligible_model_candidates,
            rejected_model_candidates,
            tuple(rejection_reasons),
        )
        diagnostics.update(
            {
                "vision_manager_preview": vision_manager_preview,
                "model_manager_result": model_manager_result,
                "observation_manager_preview": observation_manager_preview,
                "fallback_model_candidates": fallback_model_candidates,
            }
        )

        output = build_visual_handoff_result_v1(
            integration_status,
            handoff_id,
            input_candidate,
            vision_request_candidate,
            model_requirement_candidate,
            eligible_model_candidates,
            rejected_model_candidates,
            observation_request_candidate,
            deduplication_result,
            budget_decision,
            result_link_contract,
            diagnostics,
            str(trace.get("trace_ref") or ""),
            str(trace.get("replay_key") or ""),
            tuple(dict.fromkeys(rejection_reasons)),
        )
        output.update(
            {
                "history_resolution": history_resolution,
                "unhandled_exception": False,
            }
        )
        return output
    except Exception:  # noqa: BLE001
        return {
            "capability_id": CAPABILITY_ID,
            "integration_status": "internal_error",
            "handoff_id": "",
            "plan_id": "",
            "task_id": "",
            "field_snapshot_ref": "",
            "information_gap_ref": "",
            "observation_goal": "",
            "vision_required": False,
            "vision_request_candidate": None,
            "model_requirement_candidate": None,
            "eligible_model_candidates": tuple(),
            "rejected_model_candidates": tuple(),
            "observation_request_candidate": None,
            "deduplication_result": {},
            "budget_decision": {},
            "result_link_contract": None,
            "diagnostics": {},
            "trace_ref": "",
            "replay_key": "",
            "rejection_reasons": ("internal_error",),
            "boundary_flags": {},
            "unhandled_exception": True,
            **not_fact(),
        }
