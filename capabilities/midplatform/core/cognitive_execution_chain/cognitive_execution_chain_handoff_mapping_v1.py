from __future__ import annotations

from datetime import datetime, timezone
from typing import Tuple

from capabilities.midplatform.core.action_governance.action_confirmation_types_v1 import (
    ConfirmationStatusV1,
)
from capabilities.midplatform.core.action_governance.action_core_types_v1 import (
    SourceRefV1 as ActionSourceRefV1,
)
from capabilities.midplatform.core.action_governance.action_dependency_types_v1 import (
    ActionDependencyCandidateV1,
)
from capabilities.midplatform.core.action_governance.action_failure_types_v1 import (
    FailureResultReferenceV1,
)
from capabilities.midplatform.core.action_governance.action_io_types_v1 import (
    ActionGovernanceInputV1,
)
from capabilities.midplatform.core.action_governance.action_precondition_types_v1 import (
    ActionPreconditionCandidateV1,
)
from capabilities.midplatform.core.causal_governance.causal_core_types_v1 import (
    SourceRefV1 as CausalSourceRefV1,
)
from capabilities.midplatform.core.causal_governance.causal_io_types_v1 import (
    CausalGovernanceInputV1,
)
from capabilities.midplatform.core.cognitive_execution_chain.cognitive_execution_chain_compatibility_v1 import (
    HopVersionV1,
)
from capabilities.midplatform.core.cognitive_execution_chain.cognitive_execution_chain_types_v1 import (
    HandoffEnvelopeV1,
    IntegrationScenarioDirectiveV1,
)
from capabilities.midplatform.core.decision_governance.decision_core_types_v1 import (
    DecisionOptionCandidateV1,
    RiskCandidateV1,
    SourceRefV1 as DecisionSourceRefV1,
    UtilityCandidateV1,
)
from capabilities.midplatform.core.decision_governance.decision_io_types_v1 import (
    DecisionGovernanceInputV1,
)
from capabilities.midplatform.core.intent_governance.intent_core_types_v1 import (
    SourceRefV1 as IntentSourceRefV1,
)
from capabilities.midplatform.core.intent_governance.intent_io_types_v1 import (
    IntentGovernanceInputV1,
    IntentGovernanceOutputV1,
)
from capabilities.midplatform.core.runtime_executor.execution_request_types_v1 import (
    ExecutionRequestCandidateV1,
)
from capabilities.midplatform.core.runtime_executor.runtime_executor_core_types_v1 import (
    SourceRefV1 as RuntimeSourceRefV1,
)
from capabilities.midplatform.core.runtime_executor.runtime_executor_io_types_v1 import (
    RuntimeExecutorInputV1,
)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _iref(owner: str, ref_id: str, ref_type: str) -> IntentSourceRefV1:
    return IntentSourceRefV1(owner=owner, ref_id=ref_id, ref_type=ref_type)


def _cref(owner: str, ref_id: str, ref_type: str) -> CausalSourceRefV1:
    return CausalSourceRefV1(owner=owner, ref_id=ref_id, ref_type=ref_type)


def _dref(owner: str, ref_id: str, ref_type: str) -> DecisionSourceRefV1:
    return DecisionSourceRefV1(owner=owner, ref_id=ref_id, ref_type=ref_type)


def _aref(owner: str, ref_id: str, ref_type: str) -> ActionSourceRefV1:
    return ActionSourceRefV1(owner=owner, ref_id=ref_id, ref_type=ref_type)


def _rref(owner: str, ref_id: str, ref_type: str) -> RuntimeSourceRefV1:
    return RuntimeSourceRefV1(owner=owner, ref_id=ref_id, ref_type=ref_type)


def build_intent_input(scenario_id: str) -> IntentGovernanceInputV1:
    return IntentGovernanceInputV1(
        scenario_id=scenario_id,
        context_refs=(_iref("Context Governance", f"ctx:{scenario_id}", "CONTEXT"),),
        pcn_refs=(
            _iref(
                "Personal Cognitive Network Governance",
                f"pcn:{scenario_id}",
                "PCN",
            ),
        ),
        source_refs=(
            _iref("External Request Source", f"request:{scenario_id}", "REQUEST"),
            _iref("Cognitive Field", f"field:{scenario_id}", "FIELD"),
        ),
        self_refs=(
            _iref("Self Layer / Self Governance", f"self:{scenario_id}", "SELF"),
        ),
        field_refs=(_iref("Cognitive Field", f"field:{scenario_id}", "FIELD"),),
        role_refs=(
            _iref(
                "Social Self / Role Governance",
                f"role:{scenario_id}",
                "ROLE",
            ),
        ),
        relationship_refs=(
            _iref(
                "Social Self / Relationship Governance",
                f"rel:{scenario_id}",
                "RELATIONSHIP",
            ),
        ),
        memory_refs=(_iref("Memory Governance", f"mem:{scenario_id}", "MEMORY"),),
        experience_refs=(
            _iref("Experience Governance", f"exp:{scenario_id}", "EXPERIENCE"),
        ),
        emotion_refs=(
            _iref("Emotion / Integration Governance", f"emo:{scenario_id}", "EMOTION"),
        ),
        unknowns=("unknown:confidence",),
        synthetic_only=True,
        candidate_only=True,
    )


def map_intent_to_causal(
    scenario_id: str,
    intent_output: IntentGovernanceOutputV1,
    directive: IntegrationScenarioDirectiveV1,
    envelope_version: HopVersionV1,
) -> tuple[CausalGovernanceInputV1, HandoffEnvelopeV1]:
    handoff = intent_output.handoff_candidate
    hypothesis = ("intent-driven-causal-path",)
    support = (_cref("Observation Governance", f"support:{scenario_id}:1", "EVIDENCE"),)
    oppose: Tuple[CausalSourceRefV1, ...] = ()
    confounders: Tuple[CausalSourceRefV1, ...] = ()

    if directive.force_causal_uncertainty_high:
        support = ()
        oppose = (
            _cref("Observation Governance", f"oppose:{scenario_id}:1", "EVIDENCE"),
        )
        confounders = (
            _cref("Context Governance", f"confounder:{scenario_id}:1", "CONFOUNDER"),
        )

    causal_input = CausalGovernanceInputV1(
        scenario_id=scenario_id,
        hypothesis_candidates=hypothesis,
        target_event_refs=(
            _cref("Observation Governance", f"event:{scenario_id}:1", "EVENT"),
        ),
        cause_candidate_refs=(
            _cref("Observation Governance", f"cause:{scenario_id}:1", "CAUSE"),
        ),
        supporting_evidence_refs=support,
        opposing_evidence_refs=oppose,
        confounder_refs=confounders,
        temporal_order_refs=(
            _cref("Context Governance", f"temporal:{scenario_id}:1", "TEMPORAL"),
        ),
        context_refs=tuple(
            _cref("Context Governance", ref, "CONTEXT") for ref in handoff.context_refs
        ),
        prior_refs=(_cref("Memory Governance", f"prior:{scenario_id}:1", "PRIOR"),),
        intent_refs=tuple(
            _cref("Intent Governance", ref, "INTENT")
            for ref in handoff.intent_candidate_refs
        ),
        influence_refs=tuple(
            _cref("Cognitive Field", ref, "FIELD_INFLUENCE")
            for ref in handoff.field_refs
        ),
        correlation_signal_refs=(
            _cref("Observation Governance", f"corr:{scenario_id}:1", "CORRELATION"),
        ),
        unknowns=handoff.uncertainty,
        counterfactual_requested=False,
        synthetic_only=True,
        candidate_only=True,
    )

    envelope = HandoffEnvelopeV1(
        handoff_id=handoff.handoff_id,
        source_owner=handoff.producer_owner,
        target_owner=handoff.consumer_owner,
        source_candidate_ref=handoff.intent_candidate_refs[0]
        if handoff.intent_candidate_refs
        else handoff.potential_intent_refs[0],
        required_refs=handoff.intent_candidate_refs + handoff.context_refs,
        trace_ref=f"intent:{intent_output.trace_candidate.trace_id}",
        provenance_ref=handoff.provenance[0],
        schema_version=envelope_version.schema_version,
        contract_version=envelope_version.contract_version,
    )
    return causal_input, envelope


def map_causal_to_decision(
    scenario_id: str,
    causal_output,
    directive: IntegrationScenarioDirectiveV1,
    envelope_version: HopVersionV1,
) -> tuple[DecisionGovernanceInputV1, HandoffEnvelopeV1]:
    handoff = causal_output.handoff_candidate

    option_permission_allowed = not directive.force_decision_permission_veto
    option_hard_ok = not directive.force_decision_abstain

    options = (
        DecisionOptionCandidateV1(
            option_id=f"opt:{scenario_id}:1",
            option_statement="option candidate",
            utility=UtilityCandidateV1(
                utility_ref_id=f"utility:{scenario_id}:1",
                expected_benefit=92,
                tradeoff_notes=("candidate_only",),
                uncertainty=("utility_not_authority",),
                provenance=(f"prov:{scenario_id}:utility",),
            ),
            risk=RiskCandidateV1(
                risk_ref_id=f"risk:{scenario_id}:1",
                severity=1,
                likelihood=1,
                unknowns=("risk_not_safety_authority",),
                provenance=(f"prov:{scenario_id}:risk",),
            ),
            cost=2,
            hard_constraints_ok=option_hard_ok,
            permission_allowed=option_permission_allowed,
            safety_allowed=True,
            role_allowed=True,
            reversibility="REVERSIBLE",
            intent_alignment=3,
            evidence_ready=not directive.force_causal_uncertainty_high,
        ),
    )

    decision_input = DecisionGovernanceInputV1(
        scenario_id=scenario_id,
        intent_refs=(
            _dref("Intent Governance", f"intent-ref:{scenario_id}:1", "INTENT"),
        ),
        causal_refs=tuple(
            _dref("Causal Governance", ref, "CAUSAL")
            for ref in handoff.causal_hypothesis_refs
        ),
        context_refs=(_dref("Context Governance", f"ctx:{scenario_id}:1", "CONTEXT"),),
        field_refs=(_dref("Cognitive Field", f"field:{scenario_id}:1", "FIELD"),),
        role_refs=(_dref("Role Governance", f"role:{scenario_id}:1", "ROLE"),),
        permission_refs=(
            _dref("Permission Governance", f"permission:{scenario_id}:1", "PERMISSION"),
        ),
        safety_refs=(_dref("Safety Governance", f"safety:{scenario_id}:1", "SAFETY"),),
        resource_refs=(
            _dref("Resource Governance", f"resource:{scenario_id}:1", "RESOURCE"),
        ),
        constraint_refs=(
            _dref("Constraint Governance", f"constraint:{scenario_id}:1", "CONSTRAINT"),
        ),
        evidence_refs=tuple(
            _dref("Observation Governance", ref, "EVIDENCE")
            for ref in handoff.supporting_evidence_refs + handoff.opposing_evidence_refs
        ),
        options=options,
        intent_preferred_option_ids=(options[0].option_id,),
        causal_uncertainty_level="HIGH"
        if directive.force_causal_uncertainty_high
        else "LOW",
        competing_causal_hypotheses=False,
        resource_pressure_level="NORMAL",
        human_confirmation_available=False,
        synthetic_only=True,
        candidate_only=True,
    )

    envelope = HandoffEnvelopeV1(
        handoff_id=handoff.handoff_id,
        source_owner=handoff.producer_owner,
        target_owner="Decision Governance",
        source_candidate_ref=handoff.causal_hypothesis_refs[0],
        required_refs=handoff.causal_hypothesis_refs
        + handoff.supporting_evidence_refs
        + handoff.opposing_evidence_refs,
        trace_ref=handoff.trace_ref,
        provenance_ref=handoff.provenance[0],
        schema_version=envelope_version.schema_version,
        contract_version=envelope_version.contract_version,
    )
    return decision_input, envelope


def map_decision_to_action(
    scenario_id: str,
    decision_output,
    directive: IntegrationScenarioDirectiveV1,
    envelope_version: HopVersionV1,
) -> tuple[ActionGovernanceInputV1, HandoffEnvelopeV1]:
    handoff = decision_output.handoff_candidate
    selected = handoff.selected_candidate_ref or f"decision:{scenario_id}:none"

    precondition_status = "satisfied"
    if directive.force_action_stale_confirmation:
        precondition_status = "satisfied"

    action_input = ActionGovernanceInputV1(
        scenario_id=scenario_id,
        selected_decision_refs=(
            _aref("Decision Governance", selected, "DECISION_CANDIDATE"),
        ),
        intent_refs=(
            _aref("Intent Governance", f"intent-ref:{scenario_id}:1", "INTENT"),
        ),
        causal_refs=(
            _aref("Causal Governance", f"causal-ref:{scenario_id}:1", "CAUSAL"),
        ),
        target_refs=(_aref("Target Governance", f"target:{scenario_id}:1", "TARGET"),),
        context_refs=(_aref("Context Governance", f"ctx:{scenario_id}:1", "CONTEXT"),),
        field_refs=(_aref("Cognitive Field", f"field:{scenario_id}:1", "FIELD"),),
        permission_refs=(
            _aref("Permission Governance", f"permission:{scenario_id}:1", "PERMISSION"),
        ),
        safety_refs=(_aref("Safety Governance", f"safety:{scenario_id}:1", "SAFETY"),),
        confirmation_refs=(
            _aref("Human Oversight", f"confirmation:{scenario_id}:1", "CONFIRMATION"),
        ),
        preconditions=(
            ActionPreconditionCandidateV1(
                precondition_id=f"precondition:{scenario_id}:1",
                domain="environment",
                status=precondition_status,
                required=True,
                provenance_refs=(f"prov:{scenario_id}:precondition",),
            ),
        ),
        dependencies=(
            ActionDependencyCandidateV1(
                dependency_id=f"dependency:{scenario_id}:1",
                dependency_type="resource",
                status="satisfied",
                blocking=True,
                provenance_refs=(f"prov:{scenario_id}:dependency",),
            ),
        ),
        resource_refs=(
            _aref("Resource Governance", f"resource:{scenario_id}:1", "RESOURCE"),
        ),
        resource_state="available",
        permission_valid=not directive.force_action_permission_revoked,
        safety_valid=True,
        confirmation=ConfirmationStatusV1(
            state="confirmed",
            is_stale=directive.force_action_stale_confirmation,
            is_fabricated=False,
            strong_confirmation=True,
        ),
        reversibility="reversible",
        target_valid=not directive.force_action_cancelled,
        cancellation_requested=directive.force_action_cancelled,
        rollback_required=False,
        failure_result=None,
        revision_requested=False,
        prefer_eligible_state=True,
        task_reference_context_refs=(
            _aref("Task Context", f"task-context:{scenario_id}:1", "TASK_CONTEXT"),
        ),
        synthetic_only=True,
        candidate_only=True,
    )

    envelope = HandoffEnvelopeV1(
        handoff_id=handoff.handoff_id,
        source_owner=handoff.producer_owner,
        target_owner="Action Governance",
        source_candidate_ref=selected,
        required_refs=(selected,)
        + handoff.permission_status_refs
        + handoff.safety_status_refs,
        trace_ref=decision_output.trace_candidate.trace_id,
        provenance_ref=handoff.provenance[0],
        schema_version=envelope_version.schema_version,
        contract_version=envelope_version.contract_version,
    )
    return action_input, envelope


def map_action_to_runtime(
    scenario_id: str,
    action_output,
    directive: IntegrationScenarioDirectiveV1,
    envelope_version: HopVersionV1,
) -> tuple[RuntimeExecutorInputV1, HandoffEnvelopeV1]:
    handoff = action_output.runtime_handoff

    execution_request = ExecutionRequestCandidateV1(
        execution_request_id=f"execution-request:{scenario_id}",
        action_candidate_ref=_rref(
            "Action Governance", handoff.action_candidate_ref, "ACTION_CANDIDATE"
        ),
        execution_readiness_ref=_rref(
            "Action Governance",
            f"readiness:{scenario_id}:{handoff.execution_readiness}",
            "EXECUTION_READINESS",
        ),
        permission_recheck_ref=_rref(
            "Permission Governance", f"permission:{scenario_id}:1", "PERMISSION_RECHECK"
        ),
        safety_recheck_ref=_rref(
            "Safety Governance", f"safety:{scenario_id}:1", "SAFETY_RECHECK"
        ),
        confirmation_ref=_rref(
            "Human Oversight", f"confirmation:{scenario_id}:1", "CONFIRMATION"
        ),
        resource_constraint_ref=_rref(
            "Resource Governance", f"resource:{scenario_id}:1", "RESOURCE_CONSTRAINT"
        ),
        reversibility=handoff.reversibility,
        request_time=_now_iso(),
        idempotency_key=f"idem:{scenario_id}",
        scope_key=f"scope:{scenario_id}",
        provenance_ref=_rref(
            "Runtime Executor", f"prov:{scenario_id}:request", "PROVENANCE"
        ),
        scheduler_refs=(
            _rref("Scheduler", f"scheduler:{scenario_id}:1", "SCHEDULER_REFERENCE"),
        ),
        task_refs=(_rref("Task Manager", f"task:{scenario_id}:1", "TASK_REFERENCE"),),
        adapter_refs=(
            _rref("Execution Adapter", f"adapter:{scenario_id}:1", "ADAPTER_REFERENCE"),
        ),
        candidate_only=True,
        planning_only=True,
    )

    runtime_input = RuntimeExecutorInputV1(
        scenario_id=scenario_id,
        request=execution_request,
        readiness_fresh=handoff.execution_readiness == "candidate_ready",
        permission_valid=not directive.force_action_permission_revoked,
        safety_valid=True,
        confirmation_valid=not directive.force_action_stale_confirmation,
        final_scope_valid=not directive.force_runtime_admission_reject,
        final_time_window_valid=True,
        scheduler_delay=directive.force_runtime_timeout,
        start_requested=True,
        force_failure=directive.force_runtime_failure,
        force_timeout=directive.force_runtime_timeout,
        cancel_requested=False,
        force_partial=directive.force_runtime_partial,
        rollback_required=directive.force_runtime_rollback,
        retry_requested=directive.retry_authority_exhausted_probe,
        retry_authorized=not directive.retry_authority_exhausted_probe,
        retry_authorized_by=None
        if directive.retry_authority_exhausted_probe
        else "Runtime Executor",
        previous_attempt_ref=None,
    )

    envelope = HandoffEnvelopeV1(
        handoff_id=handoff.handoff_id,
        source_owner=handoff.producer_owner,
        target_owner=handoff.consumer_owner,
        source_candidate_ref=handoff.action_candidate_ref,
        required_refs=(
            handoff.action_candidate_ref,
            *handoff.permission_refs,
            *handoff.safety_refs,
            handoff.execution_readiness,
        ),
        trace_ref=action_output.trace_candidate.trace_id,
        provenance_ref=handoff.provenance[0],
        schema_version=envelope_version.schema_version,
        contract_version=envelope_version.contract_version,
    )
    return runtime_input, envelope
