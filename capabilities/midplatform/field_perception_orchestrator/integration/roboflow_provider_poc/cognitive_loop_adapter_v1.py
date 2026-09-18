from __future__ import annotations

from typing import Any, Mapping, Optional, Tuple

from capabilities.midplatform.core.cognitive_state_formation.cognitive_hypothesis_types_v1 import (
    CognitiveHypothesisCandidateV1,
)
from capabilities.midplatform.core.cognitive_state_formation.current_world_types_v1 import (
    CurrentWorldCandidateV1,
)
from capabilities.midplatform.core.decision_governance.decision_core_types_v1 import (
    DecisionCandidateV1,
)
from capabilities.midplatform.core.decision_governance.decision_registry_v1 import (
    DECISION_OWNER,
    STATE_SET,
)
from capabilities.midplatform.field_perception_orchestrator.integration.field_perception_active_observation_control_types_v1 import (
    EvidenceSufficiencyCandidateV1,
    NextCycleIngressCandidateV1,
)
from capabilities.midplatform.field_perception_orchestrator.module.field_perception_information_gap_detector_v1 import (
    build_field_perception_information_gap_v1,
)
from capabilities.midplatform.field_perception_orchestrator.module.field_perception_reobservation_policy_v1 import (
    build_field_perception_reobservation_policy_v1,
)

from .types_v1 import (
    RoboflowCognitiveLoopResultV1,
    RoboflowNormalizedProviderResultV1,
)


def _unique(*groups: Tuple[str, ...]) -> Tuple[str, ...]:
    return tuple(dict.fromkeys(str(item) for group in groups for item in group if str(item).strip()))


def _failed(
    provider_result: RoboflowNormalizedProviderResultV1,
    *,
    concern_ref: str,
    goal_refs: Tuple[str, ...],
    requirement_ref: str,
    classification: str,
    reason: str,
) -> RoboflowCognitiveLoopResultV1:
    return RoboflowCognitiveLoopResultV1(
        concern_ref=concern_ref,
        goal_refs=goal_refs,
        requirement_ref=requirement_ref,
        provider_result=provider_result,
        current_world_candidate=None,
        hypothesis_candidate=None,
        sufficiency_candidate=None,
        next_observation_candidate=None,
        decision_candidate=None,
        information_gap=(),
        trace_refs=(provider_result.trace_ref,),
        provenance_refs=provider_result.provenance_refs,
        source_version_refs=provider_result.source_version_refs,
        invalidation_refs=provider_result.invalidation_refs,
        accepted=False,
        failure_class=classification,
        failure_reason=reason,
    )


def _current_world(
    provider_result: RoboflowNormalizedProviderResultV1,
    *,
    concern_ref: str,
    intent_refs: Tuple[str, ...],
    context_refs: Tuple[str, ...],
    field_refs: Tuple[str, ...],
    observation_refs: Tuple[str, ...],
    hypothesis_ref: str,
    attention_refs: Tuple[str, ...],
    uncertainty_refs: Tuple[str, ...],
    conflict_refs: Tuple[str, ...],
) -> CurrentWorldCandidateV1:
    evidence_refs = tuple(
        item.evidence_id for item in provider_result.detection_evidence
    ) + tuple(item.evidence_id for item in provider_result.ocr_evidence)
    return CurrentWorldCandidateV1(
        current_world_id=f"current-world:candidate:{concern_ref}:{provider_result.result_id}",
        attention_refs=attention_refs,
        active_hypothesis_refs=(hypothesis_ref,) if hypothesis_ref else (),
        alternative_hypothesis_refs=(),
        context_refs=context_refs,
        field_state_refs=field_refs,
        pcn_refs=(),
        intent_refs=intent_refs,
        observation_refs=observation_refs,
        uncertainty_refs=uncertainty_refs,
        conflict_refs=conflict_refs,
        temporal_refs=(provider_result.frame_ref,),
        source_versions=(
            ((f"provider:{provider_result.provider_ref}", provider_result.source_version_refs[0]),)
            if provider_result.source_version_refs
            else ()
        ) + (("evidence", provider_result.result_id),),
        world_state_kind_candidate="visual-evidence-derived",
        world_stability_candidate="uncertain" if uncertainty_refs or conflict_refs else "candidate",
        trace_ref=f"{provider_result.trace_ref}:current-world-candidate",
        provenance_refs=_unique(
            provider_result.provenance_refs,
            (provider_result.provider_ref, provider_result.workflow_ref, *provider_result.model_refs),
        ),
        candidate_only=True,
        field_mutation=False,
        field_entity_creation=False,
        field_confidence_mutation=False,
        field_transition=False,
        event_admission=False,
        reducer_invocation_as_mutation_authority=False,
        field_truth_declaration=False,
    )


def _hypothesis(
    assessment: Mapping[str, Any],
    provider_result: RoboflowNormalizedProviderResultV1,
) -> Optional[CognitiveHypothesisCandidateV1]:
    if str(assessment.get("source_owner") or "") != "A":
        return None
    hypothesis_id = str(assessment.get("hypothesis_id") or "")
    statement = str(assessment.get("hypothesis_statement_candidate") or "")
    if not hypothesis_id or not statement:
        return None
    evidence_refs = _unique(
        tuple(str(item) for item in assessment.get("supporting_evidence_refs") or ()),
        tuple(item.evidence_id for item in provider_result.detection_evidence),
        tuple(item.evidence_id for item in provider_result.ocr_evidence),
    )

    return CognitiveHypothesisCandidateV1(
        hypothesis_id=hypothesis_id,
        hypothesis_statement_candidate=statement,
        subject_refs=tuple(str(item) for item in assessment.get("subject_refs") or ()),
        supporting_evidence_refs=evidence_refs,
        opposing_evidence_refs=tuple(str(item) for item in assessment.get("opposing_evidence_refs") or ()),
        alternative_hypothesis_refs=tuple(str(item) for item in assessment.get("alternative_hypothesis_refs") or ()),
        unknown_refs=tuple(str(item) for item in assessment.get("unknown_refs") or ()),
        conflict_refs=tuple(str(item) for item in assessment.get("conflict_refs") or ()),
        attention_refs=tuple(str(item) for item in assessment.get("attention_refs") or ()),
        context_refs=tuple(str(item) for item in assessment.get("context_refs") or ()),
        field_refs=tuple(str(item) for item in assessment.get("field_refs") or ()),
        pcn_refs=(),
        intent_refs=tuple(str(item) for item in assessment.get("intent_refs") or ()),
        confidence_candidate=str(assessment.get("confidence_candidate") or "uncertain"),
        state=str(assessment.get("state") or "ACTIVE_CANDIDATE"),
        revision_parent_ref=assessment.get("revision_parent_ref"),
        trace_ref=f"{provider_result.trace_ref}:hypothesis",
        provenance_refs=_unique(
            provider_result.provenance_refs,
            tuple(str(item) for item in assessment.get("provenance_refs") or ()),
        ),
        candidate_only=True,
        causal_truth=False,
        decision_output=False,
        action_output=False,
    )


def _decision_candidate_is_valid(candidate: Any) -> bool:
    """Validate the existing DecisionCandidateV1 shape without inventing fields."""
    return (
        isinstance(candidate, DecisionCandidateV1)
        and candidate.owner == DECISION_OWNER
        and candidate.candidate_kind == "DECISION_CANDIDATE"
        and candidate.decision_state in STATE_SET
        and candidate.decision_authority is True
        and candidate.action_authority is False
        and candidate.task_authority is False
        and bool(candidate.provenance)
    )


def _evidence_derived_assessment(
    provider_result: RoboflowNormalizedProviderResultV1,
    *,
    requirement_ref: str,
    expected_evidence_kinds: Tuple[str, ...],
) -> Mapping[str, Any]:
    """Form only structural A candidates from returned evidence coverage."""
    expected = tuple(dict.fromkeys(str(item) for item in expected_evidence_kinds if str(item).strip()))
    received = tuple(
        kind
        for kind, present in (
            ("VISION_DETECTION", bool(provider_result.detection_evidence)),
            ("OCR_TEXT_EVIDENCE", bool(provider_result.ocr_evidence)),
        )
        if present
    )
    missing = tuple(f"missing_expected_evidence:{kind}" for kind in expected if kind not in received)
    conflicts = tuple(
        ref
        for item in provider_result.detection_evidence
        for ref in item.contradiction_refs
    )
    uncertainties = tuple(
        ref
        for item in provider_result.detection_evidence
        for ref in item.uncertainty_refs
    )
    gap = tuple(dict.fromkeys((*missing, *conflicts, *uncertainties)))
    if conflicts:
        status = "CONTESTED"
        reason = "contradictory evidence preserved for A evaluation"
    elif missing or not received:
        status = "INSUFFICIENT"
        reason = "required evidence coverage remains incomplete"
    else:
        status = "SUFFICIENT"
        reason = "declared evidence-kind coverage is complete; semantic answer remains a candidate"
    return {
        "source_owner": "A",
        "hypothesis_id": f"hypothesis:{requirement_ref}:{provider_result.result_id}",
        "hypothesis_statement_candidate": "candidate visual interpretation from governed evidence; semantic identity remains unresolved",
        "unknown_refs": gap,
        "uncertainty_refs": uncertainties,
        "conflict_refs": conflicts,
        "confidence_candidate": "uncertain",
        "state": "CONTESTED" if conflicts else ("INSUFFICIENT_EVIDENCE" if status == "INSUFFICIENT" else "PROPOSED"),
        "sufficiency_status": status,
        "sufficiency_reason": reason,
        "information_gap": gap,
        "expected_evidence": expected,
        "target_coverage": bool(received),
        "semantic_coverage": not bool(missing) and bool(received),
        "spatial_coverage": bool(provider_result.detection_evidence),
        "source_diversity": len(set((provider_result.provider_ref, *provider_result.model_refs))),
        "observation_request_ref": f"{requirement_ref}:followup",
        "observation_demand_ref": f"observation-demand:{requirement_ref}",
        "next_observation_request_ref": f"{requirement_ref}:followup",
        "next_step_decision_ref": f"a-next-step:{requirement_ref}",
    }


def build_roboflow_cognitive_loop_candidates_v1(
    provider_result: RoboflowNormalizedProviderResultV1,
    *,
    concern_ref: str,
    goal_refs: Tuple[str, ...],
    requirement_ref: str,
    grant_refs: Tuple[str, ...],
    intent_refs: Tuple[str, ...] = (),
    context_refs: Tuple[str, ...] = (),
    field_refs: Tuple[str, ...] = (),
    observation_refs: Tuple[str, ...] = (),
    attention_refs: Tuple[str, ...] = (),
    semantic_assessment: Optional[Mapping[str, Any]] = None,
    decision_candidate: Any = None,
    expected_evidence_kinds: Tuple[str, ...] = (),
) -> RoboflowCognitiveLoopResultV1:
    """Assemble Luna candidates from provider evidence and A-owned assessment.

    Structural/fixture callers may supply an A assessment. Real callers may
    omit it: the narrow bridge then forms only evidence-coverage candidates,
    never a semantic answer. A Decision candidate, when present, must already
    be produced by Decision Governance.
    """

    if not provider_result.accepted:
        return _failed(
            provider_result,
            concern_ref=concern_ref,
            goal_refs=goal_refs,
            requirement_ref=requirement_ref,
            classification=provider_result.error_class or "PROVIDER_RESULT_INVALID",
            reason=provider_result.error_detail or "provider result cannot enter cognition",
        )
    assessment = dict(semantic_assessment or {})
    if not assessment:
        assessment = dict(
            _evidence_derived_assessment(
                provider_result,
                requirement_ref=requirement_ref,
                expected_evidence_kinds=expected_evidence_kinds,
            )
        )
    if bool(assessment.get("provider_autonomous_reobservation", False)):
        return _failed(
            provider_result,
            concern_ref=concern_ref,
            goal_refs=goal_refs,
            requirement_ref=requirement_ref,
            classification="PROVIDER_AUTONOMOUS_REOBSERVATION_FORBIDDEN",
            reason="Provider cannot initiate a Luna observation cycle",
        )
    if bool(assessment.get("provider_decides_hypothesis", False)):
        return _failed(
            provider_result,
            concern_ref=concern_ref,
            goal_refs=goal_refs,
            requirement_ref=requirement_ref,
            classification="PROVIDER_SEMANTIC_AUTHORITY_FORBIDDEN",
            reason="provider output cannot create or decide a Luna hypothesis",
        )
    hypothesis = _hypothesis(assessment, provider_result)
    if hypothesis is None:
        return _failed(
            provider_result,
            concern_ref=concern_ref,
            goal_refs=goal_refs,
            requirement_ref=requirement_ref,
            classification="A_HYPOTHESIS_ASSESSMENT_MISSING",
            reason="an A-owned hypothesis assessment is required; no semantic answer is synthesized",
        )

    evidence_refs = tuple(item.evidence_id for item in provider_result.detection_evidence) + tuple(
        item.evidence_id for item in provider_result.ocr_evidence
    )
    conflicts = _unique(
        tuple(str(item) for item in assessment.get("conflict_refs") or ()),
        tuple(
            ref
            for item in provider_result.detection_evidence
            for ref in item.contradiction_refs
        ),
    )
    uncertainties = _unique(
        tuple(str(item) for item in assessment.get("uncertainty_refs") or ()),
        tuple(
            ref
            for item in provider_result.detection_evidence
            for ref in item.uncertainty_refs
        ),
    )
    status = str(assessment.get("sufficiency_status") or "")
    if status not in {"SUFFICIENT", "INSUFFICIENT", "CONTESTED", "STALE", "NEEDS_CONFIRMATION", "NEEDS_ADDITIONAL_MODALITY", "NEEDS_REDIRECT", "NEEDS_PROVIDER_SWITCH"}:
        return _failed(
            provider_result,
            concern_ref=concern_ref,
            goal_refs=goal_refs,
            requirement_ref=requirement_ref,
            classification="A_SUFFICIENCY_ASSESSMENT_MISSING",
            reason="A-owned sufficiency status is required and cannot be derived from provider confidence",
        )
    if bool(assessment.get("provider_confidence_is_sufficiency", False)):
        return _failed(
            provider_result,
            concern_ref=concern_ref,
            goal_refs=goal_refs,
            requirement_ref=requirement_ref,
            classification="PROVIDER_CONFIDENCE_CANNOT_SET_SUFFICIENCY",
            reason="provider confidence is evidence metadata only",
        )

    field_snapshot = {
        "missing_information": tuple(str(item) for item in assessment.get("information_gap") or ()),
        "stale_evidence": tuple(str(item) for item in assessment.get("stale_evidence_refs") or ()),
        "uncertainties": uncertainties,
        "conflicts": conflicts,
    }
    gap_result = build_field_perception_information_gap_v1(
        {"task_goal_class": assessment.get("task_goal_class") or "observation_evidence_coverage"},
        field_snapshot,
        {"information_gap": tuple(str(item) for item in assessment.get("information_gap") or ())},
        {"conflicting_claims": conflicts},
        {"sufficient_for_decision": status == "SUFFICIENT", "expired": status == "STALE"},
    )
    information_gap = tuple(gap_result.get("information_gap") or ())
    if status != "SUFFICIENT" and not information_gap:
        return _failed(
            provider_result,
            concern_ref=concern_ref,
            goal_refs=goal_refs,
            requirement_ref=requirement_ref,
            classification="INFORMATION_GAP_MISSING",
            reason="non-sufficient cognition must expose an information gap",
        )
    reobservation_policy = build_field_perception_reobservation_policy_v1(
        gap_result,
        {"fast_changing_scene": bool(assessment.get("fast_changing_scene", False))},
    )
    world = _current_world(
        provider_result,
        concern_ref=concern_ref,
        intent_refs=intent_refs,
        context_refs=context_refs,
        field_refs=field_refs,
        observation_refs=observation_refs,
        hypothesis_ref=hypothesis.hypothesis_id,
        attention_refs=attention_refs,
        uncertainty_refs=uncertainties,
        conflict_refs=conflicts,
    )
    sufficiency = EvidenceSufficiencyCandidateV1(
        sufficiency_id=f"sufficiency:{provider_result.result_id}",
        information_need_ref=requirement_ref,
        observation_request_ref=str(assessment.get("observation_request_ref") or ""),
        expected_evidence=tuple(str(item) for item in assessment.get("expected_evidence") or ("VISION_DETECTION", "OCR_TEXT_EVIDENCE")),
        received_evidence_refs=evidence_refs,
        received_evidence_kinds=tuple(
            ["VISION_DETECTION"] if provider_result.detection_evidence else []
        ) + tuple(["OCR_TEXT_EVIDENCE"] if provider_result.ocr_evidence else []),
        source_diversity=int(assessment.get("source_diversity") or len(set((provider_result.provider_ref, *provider_result.model_refs)))),
        source_independence_candidate=bool(assessment.get("source_independence_candidate", True)),
        contradiction_refs=conflicts,
        uncertainty_refs=uncertainties,
        temporal_validity=dict(assessment.get("temporal_validity") or {}),
        target_coverage=bool(assessment.get("target_coverage", False)),
        semantic_coverage=bool(assessment.get("semantic_coverage", False)),
        spatial_coverage=bool(assessment.get("spatial_coverage", False)),
        user_confirmation_required=bool(assessment.get("user_confirmation_required", False)),
        user_confirmed=bool(assessment.get("user_confirmed", False)),
        safety_requirement=bool(assessment.get("safety_requirement", False)),
        model_confidence_input=0.0,
        status=status,
        reason=str(assessment.get("sufficiency_reason") or gap_result.get("gap_severity") or "A-owned sufficiency assessment"),
        trace_ref=f"{provider_result.trace_ref}:sufficiency",
        provenance_refs=_unique(provider_result.provenance_refs, tuple(str(item) for item in assessment.get("provenance_refs") or ())),
    )
    next_observation = None
    if status != "SUFFICIENT":
        next_observation = NextCycleIngressCandidateV1(
            ingress_id=f"next-observation:{provider_result.result_id}",
            source_control_decision_ref=str(assessment.get("next_step_decision_ref") or "a-next-step:candidate"),
            observation_demand_ref=str(assessment.get("observation_demand_ref") or ""),
            observation_request_ref=str(assessment.get("next_observation_request_ref") or ""),
            feedback_refs=(sufficiency.sufficiency_id, *evidence_refs),
            correction_refs=information_gap,
            trace_ref=f"{provider_result.trace_ref}:next-observation",
            provenance_refs=_unique(provider_result.provenance_refs, (sufficiency.trace_ref,)),
        )
    decision_failure_class = ""
    decision_failure_reason = ""
    decision_candidate_to_emit = decision_candidate
    if status == "SUFFICIENT" and decision_candidate is not None:
        if not _decision_candidate_is_valid(decision_candidate):
            decision_candidate_to_emit = None
            decision_failure_class = "DECISION_CANDIDATE_OWNER_INVALID"
            decision_failure_reason = "Decision candidate must be a valid Decision Governance candidate"
    return RoboflowCognitiveLoopResultV1(
        concern_ref=concern_ref,
        goal_refs=goal_refs,
        requirement_ref=requirement_ref,
        provider_result=provider_result,
        current_world_candidate=world,
        hypothesis_candidate=hypothesis,
        sufficiency_candidate=sufficiency,
        next_observation_candidate=next_observation,
        decision_candidate=decision_candidate_to_emit if status == "SUFFICIENT" else None,
        information_gap=information_gap,
        trace_refs=_unique(
            (provider_result.trace_ref, world.trace_ref, hypothesis.trace_ref, sufficiency.trace_ref),
            (next_observation.trace_ref,) if next_observation else (),
        ),
        provenance_refs=_unique(provider_result.provenance_refs, hypothesis.provenance_refs, sufficiency.provenance_refs),
        source_version_refs=provider_result.source_version_refs,
        invalidation_refs=provider_result.invalidation_refs,
        reobservation_policy=reobservation_policy,
        accepted=not decision_failure_class,
        failure_class=decision_failure_class,
        failure_reason=decision_failure_reason,
    )


__all__ = ["build_roboflow_cognitive_loop_candidates_v1"]
