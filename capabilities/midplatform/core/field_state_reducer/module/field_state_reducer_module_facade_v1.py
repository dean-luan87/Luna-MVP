from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict, List, Tuple

from ..behavior_policy.field_state_reducer_behavior_policy_registry_skeleton_v1 import (
    FIELD_STATE_REDUCER_BEHAVIOR_POLICY_REGISTRY_SKELETON_V1,
    policy_ids_v1,
)
from ..behavior_policy.policy_evaluation import (
    EvaluationInput,
    evaluate_single_policy_v1,
)
from ..behavior_policy.policy_selection import PolicySelectionInput, select_policy_v1
from ..state_reduction import (
    build_handoff_input_from_selection_result,
    reduce_selected_policy_to_state_candidate_v1,
)
from .field_state_reducer_module_diagnostics_v1 import build_module_diagnostics_v1
from .field_state_reducer_module_input_adapter_v1 import adapt_module_input_v1
from .field_state_reducer_module_output_builder_v1 import build_module_output_surface_v1
from .field_state_reducer_module_types_v1 import (
    FieldStateReducerModuleRequestV1,
    FieldStateReducerModuleResultV1,
)
from .field_state_reducer_read_projection_candidate_v1 import (
    build_read_projection_candidate_v1,
)


class FieldStateReducerModuleV1:
    @staticmethod
    def reduce(
        request: FieldStateReducerModuleRequestV1,
    ) -> FieldStateReducerModuleResultV1:
        stage_reached = "adapt_input"
        failed_stage = ""
        warnings: List[str] = []
        invariant_violations: List[str] = []

        adapted, missing_inputs, adapter_rejections = adapt_module_input_v1(request)
        if adapted is None:
            diagnostics = build_module_diagnostics_v1(
                stage_reached=stage_reached,
                failed_stage="adapt_input",
                evaluation_status="not_started",
                selection_status="not_started",
                reduction_status="not_started",
                transition_status="not_started",
                conflict_status="not_started",
                overlay_status="not_started",
                missing_inputs=missing_inputs,
                rejection_reasons=adapter_rejections,
                warnings=warnings,
                invariant_violations=invariant_violations,
                component_versions=dict(request.version_snapshots),
            )
            return build_module_output_surface_v1(
                reducer_request_id=request.reducer_request_id,
                reducer_run_id=request.reducer_run_id,
                field_id=request.field_id,
                state_type=request.requested_state_type,
                adapted_input_ok=False,
                evaluation_summary={"evaluation_statuses": []},
                selection_summary={"selection_status": "not_started"},
                reduction_summary={
                    "reduction_status": "not_started",
                    "conflict_status": "not_started",
                },
                transition_summary={
                    "transition_allowed": False,
                    "transition_status": "not_started",
                },
                field_state_candidate=None,
                read_model_projection_candidate=None,
                unresolved_items=tuple(),
                rejection_reasons=tuple(adapter_rejections),
                diagnostics=diagnostics,
                trace_ref="",
                replay_key="",
                contract_versions=dict(request.version_snapshots),
            )

        try:
            # 2) evaluate_policies
            stage_reached = "evaluate_policies"
            policy_metadata = {
                str(row.get("policy_id", "")): row
                for row in FIELD_STATE_REDUCER_BEHAVIOR_POLICY_REGISTRY_SKELETON_V1
            }
            evaluation_rows: List[Dict[str, Any]] = []
            evaluation_refs: List[str] = []

            for policy_id in policy_ids_v1():
                evaluation_input = EvaluationInput(
                    evaluation_id=f"eval_{adapted.reducer_run_id}_{policy_id}",
                    reducer_run_id=adapted.reducer_run_id,
                    field_id=adapted.field_id,
                    state_type=adapted.state_type,
                    policy_id=policy_id,
                    admitted_events=tuple(adapted.admitted_events),
                    existing_state_snapshot=dict(adapted.existing_state_snapshot),
                    temporal_snapshot=dict(adapted.temporal_snapshot),
                    confidence_policy_snapshot=dict(
                        adapted.provenance_snapshot.get(
                            "confidence_policy_snapshot", {"measured_confidence": 0.9}
                        )
                    ),
                    conflict_snapshot=dict(adapted.conflict_snapshot),
                    owner_correction_snapshot=dict(adapted.owner_correction_snapshot),
                    overlay_snapshot=dict(adapted.overlay_snapshot),
                    provenance_snapshot=dict(adapted.provenance_snapshot),
                    governance_snapshot=dict(
                        adapted.provenance_snapshot.get(
                            "governance_snapshot",
                            {
                                "owner_correction_review": True,
                                "fact_admission_dependency": True,
                                "permission_admission_dependency": True,
                                "human_review_dependency": True,
                                "protocol_version_dependency": True,
                                "provenance_dependency": True,
                                "change_control_dependency": True,
                                "runtime_boundary_dependency": True,
                            },
                        )
                    ),
                    policy_registry_version=str(
                        adapted.version_snapshots.get("policy_registry_version", "v1")
                    ),
                    eligibility_matrix_version=str(
                        adapted.version_snapshots.get(
                            "eligibility_matrix_version", "v1"
                        )
                    ),
                    evaluation_contract_version=str(
                        adapted.version_snapshots.get(
                            "evaluation_contract_version", "v1"
                        )
                    ),
                    evaluation_requested_at=str(
                        adapted.provenance_snapshot.get(
                            "evaluation_requested_at", "1970-01-01T00:00:00+00:00"
                        )
                    ),
                    runtime_state_dependency_requested=False,
                    provider_recall_requested=False,
                    external_lookup_requested=False,
                    model_call_requested=False,
                    state_write_requested=False,
                    action_trigger_requested=False,
                )
                eval_result = evaluate_single_policy_v1(evaluation_input)
                row = {
                    "evaluation_id": eval_result.evaluation_id,
                    "policy_id": eval_result.policy_id,
                    "state_type": eval_result.state_type,
                    "evaluation_status": eval_result.evaluation_status,
                    "selection_candidate_allowed": eval_result.selection_candidate_allowed,
                    "evaluation_trace_ref": eval_result.evaluation_trace_ref,
                    "replay_key": eval_result.replay_key,
                    "rejection_reasons": list(eval_result.rejection_reasons),
                }
                evaluation_rows.append(row)
                evaluation_refs.append(eval_result.evaluation_trace_ref)

            evaluation_statuses = [
                str(r.get("evaluation_status", "")) for r in evaluation_rows
            ]
            evaluation_summary = {
                "total_policies": len(evaluation_rows),
                "eligible_candidates": [
                    str(r.get("policy_id", ""))
                    for r in evaluation_rows
                    if str(r.get("evaluation_status", "")) == "eligible_candidate"
                    and bool(r.get("selection_candidate_allowed", False))
                ],
                "evaluation_statuses": evaluation_statuses,
            }

            # 3) select_policies
            stage_reached = "select_policies"
            selection_input = PolicySelectionInput(
                selection_id=f"selection_{adapted.reducer_run_id}",
                reducer_run_id=adapted.reducer_run_id,
                field_id=adapted.field_id,
                state_type=adapted.state_type,
                evaluation_results=tuple(evaluation_rows),
                policy_registry_version=str(
                    adapted.version_snapshots.get("policy_registry_version", "v1")
                ),
                eligibility_matrix_version=str(
                    adapted.version_snapshots.get("eligibility_matrix_version", "v1")
                ),
                precedence_matrix_version=str(
                    adapted.version_snapshots.get("precedence_matrix_version", "v1")
                ),
                composition_contract_version=str(
                    adapted.version_snapshots.get("composition_contract_version", "v1")
                ),
                replay_contract_version=str(
                    adapted.version_snapshots.get("replay_contract_version", "v1")
                ),
            )
            selection_result, _ = select_policy_v1(selection_input)
            selection_dict = asdict(selection_result)
            selection_summary = {
                "selection_status": selection_result.selection_status,
                "selected_policy_ids": list(selection_result.selected_policy_ids),
                "eligible_policy_ids": list(selection_result.eligible_policy_ids),
                "rejected_policy_ids": list(selection_result.rejected_policy_ids),
            }

            # 4-9) reduction chain
            stage_reached = "reduce_state"
            selected_policy_metadata = {
                pid: {
                    "policy_version": str(
                        policy_metadata.get(pid, {}).get("policy_version", "v1")
                    )
                }
                for pid in selection_result.selected_policy_ids
            }
            handoff_input = build_handoff_input_from_selection_result(
                selection_dict,
                existing_state_snapshot=dict(adapted.existing_state_snapshot),
                admitted_event_refs=tuple(adapted.admitted_event_refs),
                temporal_snapshot=dict(adapted.temporal_snapshot),
                conflict_snapshot=dict(adapted.conflict_snapshot),
                overlay_snapshot=dict(adapted.overlay_snapshot),
                owner_correction_snapshot=dict(adapted.owner_correction_snapshot),
                policy_evaluation_refs=tuple(evaluation_refs),
                selected_policy_metadata=selected_policy_metadata,
                direct_state_write_requested=False,
                action_trigger_requested=False,
                admitted_events=tuple(adapted.admitted_events),
            )

            reduction_result, reduction_trace = (
                reduce_selected_policy_to_state_candidate_v1(handoff_input)
            )
            reduction_dict = asdict(reduction_result)
            reduction_summary = {
                "reduction_status": reduction_result.reduction_status,
                "handoff_status": reduction_result.handoff_status,
                "conflict_status": reduction_result.conflict_result.conflict_status,
                "overlay_status": reduction_result.overlay_result.overlay_status,
                "rejection_reasons": list(reduction_result.rejection_reasons),
                "trace": reduction_trace,
                "overlay_result": reduction_dict.get("overlay_result", {}),
            }

            transition_summary = {
                "transition_allowed": reduction_result.transition_result.transition_allowed,
                "transition_status": reduction_result.transition_result.transition_status,
                "requested_transition": reduction_result.transition_result.requested_transition,
                "rejection_reasons": list(
                    reduction_result.transition_result.rejection_reasons
                ),
            }

            candidate_dict = reduction_dict.get("state_candidate")
            projection_candidate = build_read_projection_candidate_v1(
                reducer_run_id=adapted.reducer_run_id,
                field_id=adapted.field_id,
                state_type=adapted.state_type,
                state_candidate=candidate_dict,
                reduction_summary=reduction_summary,
                conflict_status=reduction_result.conflict_result.conflict_status,
                overlay_status=reduction_result.overlay_result.overlay_status,
            )

            unresolved_items = tuple(
                dict.fromkeys(
                    list(reduction_result.rejection_reasons)
                    + (
                        ["unresolved"]
                        if reduction_result.conflict_result.conflict_status
                        == "unresolved"
                        else []
                    )
                )
            )

            stage_reached = "build_output"
            diagnostics = build_module_diagnostics_v1(
                stage_reached=stage_reached,
                failed_stage=failed_stage,
                evaluation_status=",".join(sorted(set(evaluation_statuses))) or "none",
                selection_status=selection_result.selection_status,
                reduction_status=reduction_result.reduction_status,
                transition_status=reduction_result.transition_result.transition_status,
                conflict_status=reduction_result.conflict_result.conflict_status,
                overlay_status=reduction_result.overlay_result.overlay_status,
                missing_inputs=tuple(),
                rejection_reasons=tuple(reduction_result.rejection_reasons),
                warnings=warnings,
                invariant_violations=invariant_violations,
                component_versions=dict(adapted.version_snapshots),
            )

            return build_module_output_surface_v1(
                reducer_request_id=adapted.reducer_request_id,
                reducer_run_id=adapted.reducer_run_id,
                field_id=adapted.field_id,
                state_type=adapted.state_type,
                adapted_input_ok=True,
                evaluation_summary=evaluation_summary,
                selection_summary=selection_summary,
                reduction_summary=reduction_summary,
                transition_summary=transition_summary,
                field_state_candidate=candidate_dict,
                read_model_projection_candidate=projection_candidate,
                unresolved_items=unresolved_items,
                rejection_reasons=tuple(reduction_result.rejection_reasons),
                diagnostics=diagnostics,
                trace_ref=str(reduction_result.trace_ref),
                replay_key=str(reduction_result.replay_key),
                contract_versions=dict(adapted.version_snapshots),
            )

        except Exception as exc:
            failed_stage = stage_reached
            diagnostics = build_module_diagnostics_v1(
                stage_reached=stage_reached,
                failed_stage=failed_stage,
                evaluation_status="error",
                selection_status="error",
                reduction_status="error",
                transition_status="error",
                conflict_status="error",
                overlay_status="error",
                missing_inputs=tuple(),
                rejection_reasons=("internal_error", str(exc)),
                warnings=warnings,
                invariant_violations=("facade_exception",),
                component_versions=dict(request.version_snapshots),
            )
            return build_module_output_surface_v1(
                reducer_request_id=request.reducer_request_id,
                reducer_run_id=request.reducer_run_id,
                field_id=request.field_id,
                state_type=request.requested_state_type,
                adapted_input_ok=True,
                evaluation_summary={"evaluation_statuses": []},
                selection_summary={"selection_status": "internal_error"},
                reduction_summary={
                    "reduction_status": "internal_error",
                    "conflict_status": "internal_error",
                },
                transition_summary={
                    "transition_allowed": False,
                    "transition_status": "internal_error",
                },
                field_state_candidate=None,
                read_model_projection_candidate=None,
                unresolved_items=("internal_error",),
                rejection_reasons=("internal_error",),
                diagnostics=diagnostics,
                trace_ref="",
                replay_key="",
                contract_versions=dict(request.version_snapshots),
            )
