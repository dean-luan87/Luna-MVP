from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any, Dict, Tuple

from .field_state_reducer_behavior_policy_trace_types_v1 import (
    BehaviorPolicyCompositionTraceStepV1,
    BehaviorPolicyEligibilityTraceStepV1,
    BehaviorPolicyPrecedenceTraceStepV1,
    BehaviorPolicyReplayKeyV1,
    BehaviorPolicyRejectionRefV1,
    BehaviorPolicyTraceV1,
)
from .field_state_reducer_behavior_policy_types_v1 import (
    BehaviorPolicyDecisionV1,
    BehaviorPolicyOutcomeV1,
    BehaviorPolicySelectionInputV1,
)
from .field_state_reducer_policy_composition_skeleton_v1 import (
    build_placeholder_composition_sequence,
)
from .field_state_reducer_policy_eligibility_skeleton_v1 import (
    build_placeholder_eligibility_results,
    list_candidate_policies,
)
from .field_state_reducer_policy_precedence_skeleton_v1 import (
    build_placeholder_precedence_sequence,
    load_precedence_rules,
)


def build_behavior_policy_replay_key(
    reducer_run_id: str,
    field_id: str,
    state_type: str,
    candidate_policy_ids: Tuple[str, ...],
) -> str:
    key = BehaviorPolicyReplayKeyV1(
        policy_registry_version="v1",
        eligibility_matrix_version="v1",
        precedence_matrix_version="v1",
        composition_contract_version="v1",
        stable_fingerprint="|".join(
            (reducer_run_id, field_id, state_type) + candidate_policy_ids
        ),
    )
    return hashlib.sha256(
        json.dumps(key.__dict__, sort_keys=True).encode("utf-8")
    ).hexdigest()


def build_behavior_policy_decision_skeleton(
    field_id: str,
    state_type: str,
    temporal_inputs: Dict[str, Any],
    confidence_inputs: Dict[str, Any],
    conflict_inputs: Dict[str, Any],
    owner_correction_inputs: Dict[str, Any],
    overlay_inputs: Dict[str, Any],
) -> Tuple[BehaviorPolicyDecisionV1, BehaviorPolicyTraceV1]:
    reducer_run_id = f"behavior_policy_skeleton_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
    candidate_policy_ids = list_candidate_policies(state_type)
    eligibility_rows = build_placeholder_eligibility_results(candidate_policy_ids)
    eligible_policy_ids = tuple(r.policy_id for r in eligibility_rows)
    rejected_policy_ids = tuple()

    precedence_sequence = build_placeholder_precedence_sequence(eligible_policy_ids)
    composition_sequence = build_placeholder_composition_sequence(precedence_sequence)

    replay_key = build_behavior_policy_replay_key(
        reducer_run_id,
        field_id,
        state_type,
        candidate_policy_ids,
    )

    outcome = (
        BehaviorPolicyOutcomeV1.NO_STATE_CHANGE.value
        if not candidate_policy_ids
        else BehaviorPolicyOutcomeV1.SKELETON_POLICY_DECISION.value
    )

    decision = BehaviorPolicyDecisionV1(
        decision_id=f"decision_{reducer_run_id}",
        reducer_run_id=reducer_run_id,
        field_id=field_id,
        state_type=state_type,
        candidate_policy_ids=candidate_policy_ids,
        eligible_policy_ids=eligible_policy_ids,
        rejected_policy_ids=rejected_policy_ids,
        selected_policy_ids=tuple(),
        precedence_steps=tuple(
            {
                "higher_policy": r.get("higher_policy"),
                "lower_policy": r.get("lower_policy"),
                "applied": False,
            }
            for r in load_precedence_rules()
        ),
        composition_sequence=composition_sequence,
        temporal_inputs=dict(temporal_inputs),
        confidence_inputs=dict(confidence_inputs),
        conflict_inputs=dict(conflict_inputs),
        owner_correction_inputs=dict(owner_correction_inputs),
        overlay_inputs=dict(overlay_inputs),
        decision_outcome=outcome,
        resulting_state_candidate=None,
        resulting_state_status_candidate="candidate",
        unresolved_conditions=tuple(),
        deterministic_replay_key=replay_key,
        skeleton_only=True,
        candidate_only=True,
        policy_execution_executed=False,
        state_mutation_executed=False,
        fact_promotion_executed=False,
        action_trigger_executed=False,
        runtime_execution=False,
    )

    trace = BehaviorPolicyTraceV1(
        trace_id=f"trace_{reducer_run_id}",
        reducer_run_id=reducer_run_id,
        field_id=field_id,
        state_type=state_type,
        candidate_policy_ids=candidate_policy_ids,
        eligible_policy_ids=eligible_policy_ids,
        rejected_policy_ids=rejected_policy_ids,
        selected_policy_ids=tuple(),
        precedence_steps=tuple(
            BehaviorPolicyPrecedenceTraceStepV1(
                step_id=f"precedence_{idx}",
                higher_policy=str(step.get("higher_policy", "")),
                lower_policy=str(step.get("lower_policy", "")),
                applied=False,
                reason="placeholder_precedence_only",
            )
            for idx, step in enumerate(load_precedence_rules(), start=1)
        ),
        composition_sequence=composition_sequence,
        temporal_inputs=dict(temporal_inputs),
        confidence_inputs=dict(confidence_inputs),
        conflict_inputs=dict(conflict_inputs),
        owner_correction_inputs=dict(owner_correction_inputs),
        overlay_inputs=dict(overlay_inputs),
        policy_versions={pid: "v1" for pid in candidate_policy_ids},
        replay_key=replay_key,
        eligibility_steps=tuple(
            BehaviorPolicyEligibilityTraceStepV1(
                step_id=f"eligibility_{idx}",
                policy_id=row.policy_id,
                status=row.status,
                notes="placeholder_only",
            )
            for idx, row in enumerate(eligibility_rows, start=1)
        ),
        composition_steps=(
            BehaviorPolicyCompositionTraceStepV1(
                step_id="composition_1",
                mode="sequential",
                sequence=composition_sequence,
                notes="placeholder_composition_only",
            ),
        ),
        rejection_refs=tuple(
            BehaviorPolicyRejectionRefV1(
                policy_id=pid, reason="placeholder_no_rejection"
            )
            for pid in rejected_policy_ids
        ),
        skeleton_only=True,
        candidate_only=True,
        policy_execution_executed=False,
        runtime_execution=False,
    )

    return decision, trace


def run_selection_input_skeleton(
    selection_input: BehaviorPolicySelectionInputV1,
) -> Tuple[BehaviorPolicyDecisionV1, BehaviorPolicyTraceV1]:
    return build_behavior_policy_decision_skeleton(
        field_id=selection_input.field_id,
        state_type=selection_input.state_type,
        temporal_inputs=selection_input.temporal_inputs,
        confidence_inputs=selection_input.confidence_inputs,
        conflict_inputs=selection_input.conflict_inputs,
        owner_correction_inputs=selection_input.owner_correction_inputs,
        overlay_inputs=selection_input.overlay_inputs,
    )
