# -*- coding: utf-8 -*-
"""Field State Reducer controlled skeleton implementation v1."""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from typing import Any, Dict, List, Tuple

from capabilities.midplatform.core.field_state_reducer.field_state_reducer_protocol_v1 import (
    FieldStateReducerProtocolV1,
)
from capabilities.midplatform.core.field_state_reducer.field_state_reducer_trace_types_v1 import (
    FieldStateReducerDecisionStepV1,
    FieldStateReducerTraceV1,
)
from capabilities.midplatform.core.field_state_reducer.field_state_reducer_types_v1 import (
    FieldStateReducerInputV1,
    FieldStateReducerOutputV1,
    ReductionDecisionTypeV1,
    StateChangeTypeV1,
)
from capabilities.midplatform.core.field_state_reducer.field_state_reducer_static_validators_v1 import (
    validate_admitted_events_only,
    validate_no_direct_mutation_request,
    validate_no_raw_observation,
    validate_reducer_input_contract,
    validate_replay_boundary,
    validate_stable_event_ids,
    validate_temporal_snapshot_present,
    validate_version_snapshot_present,
)


class FieldStateReducerSkeletonV1(FieldStateReducerProtocolV1):
    reducer_is_single_mutation_authority = True
    skeleton_only = True
    runtime_implemented = False
    production_enabled = False
    database_access_allowed = False
    scheduler_access_allowed = False
    provider_recall_allowed = False
    external_lookup_allowed = False
    action_trigger_allowed = False
    direct_state_write_allowed = False
    event_mutation_allowed = False

    def validate_input(
        self, reducer_input: FieldStateReducerInputV1
    ) -> Tuple[bool, Tuple[str, ...]]:
        issues: List[str] = []
        checks = [
            validate_reducer_input_contract(reducer_input),
            validate_admitted_events_only(reducer_input.admitted_field_events),
            validate_no_raw_observation(reducer_input.admitted_field_events),
            validate_temporal_snapshot_present(
                reducer_input.temporal_validity_snapshot
            ),
            validate_version_snapshot_present(reducer_input.reducer_version_snapshot),
            validate_stable_event_ids(reducer_input.admitted_field_events),
            validate_no_direct_mutation_request(reducer_input),
            validate_replay_boundary(reducer_input),
        ]
        for ok, errs in checks:
            if not ok:
                issues.extend(errs)
        return len(issues) == 0, tuple(issues)

    def order_events(
        self, reducer_input: FieldStateReducerInputV1
    ) -> Tuple[Dict[str, Any], ...]:
        # Deterministic placeholder ordering by stable event_id only.
        events = list(reducer_input.admitted_field_events)
        events.sort(key=lambda e: str(e.get("event_id", "")))
        return tuple(events)

    def build_replay_key(
        self,
        reducer_input: FieldStateReducerInputV1,
        ordered_events: Tuple[Dict[str, Any], ...],
    ) -> str:
        fingerprint = "|".join(str(e.get("event_id", "")) for e in ordered_events)
        key_raw = (
            f"{reducer_input.reducer_version_snapshot.reducer_version}|"
            f"{reducer_input.reducer_version_snapshot.reduction_policy_version}|"
            f"{reducer_input.reducer_config_snapshot.deterministic_evaluation_timestamp}|"
            f"{fingerprint}"
        )
        return hashlib.sha256(key_raw.encode("utf-8")).hexdigest()

    def build_trace(
        self,
        reducer_input: FieldStateReducerInputV1,
        ordered_events: Tuple[Dict[str, Any], ...],
        issues: Tuple[str, ...],
    ) -> FieldStateReducerTraceV1:
        run_id = (
            f"fsr_skeleton_run_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
        )
        decision_steps = (
            FieldStateReducerDecisionStepV1(
                step_id="s1",
                step_name="validate_input",
                step_result="ok" if not issues else "blocked",
                notes=",".join(issues)
                if issues
                else "controlled_skeleton_validation_pass",
            ),
            FieldStateReducerDecisionStepV1(
                step_id="s2",
                step_name="order_events",
                step_result="placeholder_only",
                notes="deterministic_order_by_event_id",
            ),
            FieldStateReducerDecisionStepV1(
                step_id="s3",
                step_name="reduce",
                step_result="no_state_change",
                notes="skeleton_no_state_change",
            ),
        )
        return FieldStateReducerTraceV1(
            trace_id=f"trace_{run_id}",
            state_id="state_placeholder_none",
            reducer_run_id=run_id,
            reducer_version=reducer_input.reducer_version_snapshot.reducer_version,
            policy_version=reducer_input.reducer_version_snapshot.reduction_policy_version,
            input_event_ids=tuple(
                str(e.get("event_id", "")) for e in reducer_input.admitted_field_events
            ),
            ordered_event_ids=tuple(str(e.get("event_id", "")) for e in ordered_events),
            accepted_event_ids=tuple(
                str(e.get("event_id", "")) for e in ordered_events
            ),
            rejected_event_ids=tuple(),
            ignored_event_ids=tuple(),
            conflict_ids=tuple(),
            temporal_snapshot=dict(reducer_input.temporal_validity_snapshot),
            decision_steps=decision_steps,
            resulting_state_hash="state_placeholder_none",
            replay_key=self.build_replay_key(reducer_input, ordered_events),
            created_at=datetime.now(timezone.utc).isoformat(),
        )

    def reduce(
        self, reducer_input: FieldStateReducerInputV1
    ) -> FieldStateReducerOutputV1:
        ok, issues = self.validate_input(reducer_input)
        ordered = self.order_events(reducer_input)
        trace = self.build_trace(reducer_input, ordered, issues)
        decision = (
            ReductionDecisionTypeV1.SKELETON_NO_STATE_CHANGE.value
            if ok
            else ReductionDecisionTypeV1.SKELETON_VALIDATION_BLOCKED.value
        )
        return FieldStateReducerOutputV1(
            resulting_state=None,
            reduction_decision=decision,
            applied_event_ids=tuple(str(e.get("event_id", "")) for e in ordered)
            if ok
            else tuple(),
            rejected_event_ids=tuple()
            if ok
            else tuple(str(e.get("event_id", "")) for e in ordered),
            ignored_event_ids=tuple(),
            conflict_ids=tuple(),
            unresolved_conditions=issues,
            reducer_trace={
                "trace_id": trace.trace_id,
                "reducer_run_id": trace.reducer_run_id,
                "ordered_event_ids": trace.ordered_event_ids,
                "decision_steps": [
                    {
                        "step_id": s.step_id,
                        "step_name": s.step_name,
                        "step_result": s.step_result,
                        "notes": s.notes,
                    }
                    for s in trace.decision_steps
                ],
                "skeleton_only": True,
                "deterministic_placeholder_supported": True,
            },
            deterministic_replay_key=trace.replay_key,
            state_change_type=StateChangeTypeV1.NO_STATE_CHANGE.value,
            mutation_allowed_only_by_reducer=True,
            skeleton_only=True,
            candidate_only=True,
            runtime_executed=False,
            state_mutation_executed=False,
        )
