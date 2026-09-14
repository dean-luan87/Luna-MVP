"""Candidate-only capability usage, experience, and Hive feedback governance."""

from __future__ import annotations

from collections import Counter
from typing import Iterable, Optional, Tuple

from .universal_capability_slot_types_v1 import (
    CapabilityOutcomeAssessmentV1,
    CapabilityUsageRecordV1,
    CapabilityWeaknessCandidateV1,
    HiveCapabilityDemandCandidateV1,
    HiveCapabilityFeedbackCandidateV1,
    IndividualCapabilityExperienceProfileV1,
)


EXECUTION_OUTCOMES = ("SUCCESS", "FAILURE", "DEGRADED", "TIMEOUT", "CANCELLED", "UNKNOWN")
REQUIREMENT_SATISFACTION = ("SATISFIED", "PARTIAL", "UNSATISFIED", "UNKNOWN")
TASK_CONTRIBUTION = ("RESOLVED", "CONTRIBUTED", "NO_CONTRIBUTION", "UNRESOLVED", "UNKNOWN")
DEMAND_KINDS = ("CAPABILITY_WEAKNESS", "CAPABILITY_GAP")


def build_capability_usage_record(
    *,
    usage_id: str,
    module_ref: str,
    module_version_ref: Optional[str],
    slot_ref: Optional[str],
    invocation_ref: str,
    requirement_ref: str,
    problem_class: str,
    operation: str,
    context_refs: Iterable[str],
    task_refs: Iterable[str],
    trace_refs: Iterable[str],
    execution_result_ref: Optional[str],
    execution_outcome: str,
    requirement_satisfaction: str,
    task_contribution: str,
    failure_refs: Iterable[str] = (),
    degradation_refs: Iterable[str] = (),
    dependency_refs: Iterable[str] = (),
    temporal_refs: Iterable[str] = (),
) -> CapabilityUsageRecordV1:
    if execution_outcome not in EXECUTION_OUTCOMES:
        raise ValueError(f"unsupported execution outcome: {execution_outcome}")
    if requirement_satisfaction not in REQUIREMENT_SATISFACTION:
        raise ValueError(f"unsupported requirement satisfaction: {requirement_satisfaction}")
    if task_contribution not in TASK_CONTRIBUTION:
        raise ValueError(f"unsupported task contribution: {task_contribution}")
    return CapabilityUsageRecordV1(
        usage_id=usage_id,
        module_ref=module_ref,
        module_version_ref=module_version_ref,
        slot_ref=slot_ref,
        invocation_ref=invocation_ref,
        requirement_ref=requirement_ref,
        problem_class=problem_class,
        operation=operation,
        context_refs=tuple(context_refs),
        task_refs=tuple(task_refs),
        trace_refs=tuple(trace_refs),
        execution_result_ref=execution_result_ref,
        execution_outcome=execution_outcome,
        requirement_satisfaction=requirement_satisfaction,
        task_contribution=task_contribution,
        failure_refs=tuple(failure_refs),
        degradation_refs=tuple(degradation_refs),
        dependency_refs=tuple(dependency_refs),
        temporal_refs=tuple(temporal_refs),
    )


def assess_capability_outcome(
    usage: CapabilityUsageRecordV1,
    *,
    assessment_id: Optional[str] = None,
    evidence_refs: Iterable[str] = (),
) -> CapabilityOutcomeAssessmentV1:
    """Preserve three independent result dimensions without promotion."""
    return CapabilityOutcomeAssessmentV1(
        assessment_id=assessment_id or f"assessment:{usage.usage_id}",
        usage_ref=usage.usage_id,
        execution_outcome=usage.execution_outcome,
        requirement_satisfaction=usage.requirement_satisfaction,
        task_contribution=usage.task_contribution,
        evidence_refs=tuple(evidence_refs),
        failure_pattern_refs=tuple(dict.fromkeys(usage.failure_refs + usage.degradation_refs)),
        reason="CONTROLLED_CAPABILITY_OUTCOME_DIMENSIONS_PRESERVED",
    )


def _distribution(values: Iterable[str]) -> Tuple[str, ...]:
    counts = Counter(values)
    return tuple(f"{key}:{counts[key]}" for key in sorted(counts))


def aggregate_individual_capability_experience(
    *,
    profile_id: str,
    module_ref: str,
    aggregation_window_ref: str,
    usage_records: Iterable[CapabilityUsageRecordV1],
) -> IndividualCapabilityExperienceProfileV1:
    records = tuple(record for record in usage_records if record.module_ref == module_ref)
    return IndividualCapabilityExperienceProfileV1(
        profile_id=profile_id,
        module_ref=module_ref,
        aggregation_window_ref=aggregation_window_ref,
        usage_count=len(records),
        execution_success_count=sum(record.execution_outcome == "SUCCESS" for record in records),
        execution_failure_count=sum(record.execution_outcome in {"FAILURE", "TIMEOUT", "CANCELLED"} for record in records),
        execution_degraded_count=sum(record.execution_outcome == "DEGRADED" for record in records),
        requirement_satisfied_count=sum(record.requirement_satisfaction == "SATISFIED" for record in records),
        requirement_partial_count=sum(record.requirement_satisfaction == "PARTIAL" for record in records),
        requirement_unsatisfied_count=sum(record.requirement_satisfaction == "UNSATISFIED" for record in records),
        task_resolved_count=sum(record.task_contribution == "RESOLVED" for record in records),
        task_contributed_count=sum(record.task_contribution == "CONTRIBUTED" for record in records),
        task_no_contribution_count=sum(record.task_contribution in {"NO_CONTRIBUTION", "UNRESOLVED"} for record in records),
        problem_class_distribution=_distribution(record.problem_class for record in records),
        operation_distribution=_distribution(record.operation for record in records),
        failure_pattern_distribution=_distribution(
            pattern
            for record in records
            for pattern in record.failure_refs + record.degradation_refs
        ),
        evidence_refs=tuple(dict.fromkeys(ref for record in records for ref in record.trace_refs)),
        trace_refs=tuple(dict.fromkeys(ref for record in records for ref in record.trace_refs)),
    )


def build_capability_weakness_candidate(
    *,
    weakness_id: str,
    profile: IndividualCapabilityExperienceProfileV1,
    problem_class: str,
    operation: str,
    context_refs: Iterable[str],
    evidence_refs: Iterable[str],
    reason: str,
) -> CapabilityWeaknessCandidateV1:
    if profile.module_ref == "":
        raise ValueError("weakness candidate requires a module reference")
    insufficiency_observed = (
        profile.requirement_partial_count > 0
        or profile.requirement_unsatisfied_count > 0
        or profile.execution_failure_count > 0
        or profile.execution_degraded_count > 0
        or profile.task_no_contribution_count > 0
    )
    if not insufficiency_observed:
        raise ValueError("weakness candidate requires observed insufficiency evidence")
    return CapabilityWeaknessCandidateV1(
        weakness_id=weakness_id,
        module_ref=profile.module_ref,
        problem_class=problem_class,
        operation=operation,
        context_refs=tuple(context_refs),
        source_profile_ref=profile.profile_id,
        evidence_refs=tuple(evidence_refs),
        reason=reason,
    )


def build_hive_feedback_candidate(
    *,
    feedback_id: str,
    module_ref: str,
    aggregation_window_ref: str,
    profiles: Iterable[IndividualCapabilityExperienceProfileV1],
    weakness_refs: Iterable[str],
    gap_refs: Iterable[str],
    privacy_policy_ref: str,
) -> HiveCapabilityFeedbackCandidateV1:
    profile_list = tuple(profile for profile in profiles if profile.module_ref == module_ref)
    return HiveCapabilityFeedbackCandidateV1(
        feedback_id=feedback_id,
        module_ref=module_ref,
        aggregation_window_ref=aggregation_window_ref,
        sample_count=sum(profile.usage_count for profile in profile_list),
        problem_class_buckets=tuple(sorted({item for profile in profile_list for item in profile.problem_class_distribution})),
        operation_buckets=tuple(sorted({item for profile in profile_list for item in profile.operation_distribution})),
        execution_outcome_buckets=tuple(
            sorted(
                {
                    f"SUCCESS:{sum(profile.execution_success_count for profile in profile_list)}",
                    f"FAILURE:{sum(profile.execution_failure_count for profile in profile_list)}",
                    f"DEGRADED:{sum(profile.execution_degraded_count for profile in profile_list)}",
                }
            )
        ),
        requirement_satisfaction_buckets=tuple(
            sorted(
                {
                    f"SATISFIED:{sum(profile.requirement_satisfied_count for profile in profile_list)}",
                    f"PARTIAL:{sum(profile.requirement_partial_count for profile in profile_list)}",
                    f"UNSATISFIED:{sum(profile.requirement_unsatisfied_count for profile in profile_list)}",
                }
            )
        ),
        task_contribution_buckets=tuple(
            sorted(
                {
                    f"RESOLVED:{sum(profile.task_resolved_count for profile in profile_list)}",
                    f"CONTRIBUTED:{sum(profile.task_contributed_count for profile in profile_list)}",
                    f"NO_CONTRIBUTION:{sum(profile.task_no_contribution_count for profile in profile_list)}",
                }
            )
        ),
        weakness_refs=tuple(weakness_refs),
        gap_refs=tuple(gap_refs),
        provenance_refs=tuple(dict.fromkeys(ref for profile in profile_list for ref in profile.trace_refs)),
        privacy_policy_ref=privacy_policy_ref,
    )


def build_hive_demand_candidate(
    *,
    demand_id: str,
    demand_kind: str,
    problem_class: str,
    operation: str,
    source_feedback_ref: str,
    source_profile_refs: Iterable[str],
    existing_module_refs: Iterable[str],
    unmet_requirement_refs: Iterable[str],
    aggregate_count: int,
    reason: str,
) -> HiveCapabilityDemandCandidateV1:
    if demand_kind not in DEMAND_KINDS:
        raise ValueError(f"unsupported capability demand kind: {demand_kind}")
    return HiveCapabilityDemandCandidateV1(
        demand_id=demand_id,
        demand_kind=demand_kind,
        problem_class=problem_class,
        operation=operation,
        source_feedback_ref=source_feedback_ref,
        source_profile_refs=tuple(source_profile_refs),
        existing_module_refs=tuple(existing_module_refs),
        unmet_requirement_refs=tuple(unmet_requirement_refs),
        aggregate_count=aggregate_count,
        reason=reason,
    )
