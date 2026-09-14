"""Synthetic-only scenario descriptors for the controlled return-path slice."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from .types_v1 import OutcomeSourceInputV1, ResultSourceInputV1


@dataclass(frozen=True)
class SyntheticScenarioV1:
    scenario_id: str
    category: str
    description: str
    target_boundary: str = "CURRENT_WORLD"
    result: ResultSourceInputV1 | None = None
    outcome: OutcomeSourceInputV1 | None = None
    expected_blocked: bool = False
    observability_focus: str = "candidate_only"


def _result(
    scenario_id: str,
    *,
    status: str = "AVAILABLE",
    evidence: Tuple[str, ...] = ("evidence:synthetic:1",),
    provenance: Tuple[str, ...] = ("prov:synthetic:1",),
    versions: Tuple[str, ...] = ("Evidence:v1", "Field:v1", "World:v1"),
    invalidations: Tuple[str, ...] = (),
    source_valid: bool = True,
    concern_ref: str | None = "concern:synthetic:1",
) -> ResultSourceInputV1:
    return ResultSourceInputV1(
        source_result_ref=f"result:{scenario_id}",
        result_kind="ACTION_RESULT" if scenario_id.startswith("action_") else "PROVIDER_RESULT",
        status_candidate=status,
        source_version_refs=versions,
        evidence_refs=evidence,
        target_ref="field:synthetic:1",
        concern_ref=concern_ref,
        observed_time="2026-08-24T00:00:00Z",
        effective_time_ref="time:synthetic:1",
        uncertainty_refs=("uncertainty:synthetic",) if status in {"UNCERTAIN", "UNVERIFIED_EFFECT"} else (),
        confidence_candidate="0.8" if status not in {"UNCERTAIN", "UNVERIFIED_EFFECT"} else "unknown",
        provenance_refs=provenance,
        trace_refs=(f"trace:{scenario_id}",),
        invalidation_refs=invalidations,
        source_valid=source_valid,
    )


def _outcome(
    scenario_id: str,
    *,
    concern_ref: str | None = "concern:synthetic:1",
    grant_ref: str | None = "grant:synthetic:v1",
    provenance: Tuple[str, ...] = ("prov:outcome:synthetic",),
    versions: Tuple[str, ...] = ("Outcome:v1", "Concern:v1", "Grant:v1"),
    invalidations: Tuple[str, ...] = (),
    status: str = "SUCCESS_CANDIDATE",
    partiality: str = "NONE",
) -> OutcomeSourceInputV1:
    return OutcomeSourceInputV1(
        outcome_candidate_ref=f"outcome:{scenario_id}",
        outcome_version="v1",
        goal_refs=("goal:synthetic:1",),
        concern_ref=concern_ref,
        grant_ref=grant_ref,
        decision_refs=("decision:synthetic:1",),
        task_refs=("task:synthetic:1",),
        action_result_refs=("action-result:synthetic:1",),
        a_local_evaluation_refs=("a-evaluation:synthetic:1",),
        field_refs=("field:synthetic:1",),
        current_world_refs=("current-world:synthetic:1",),
        evaluation_status=status,
        partiality=partiality,
        uncertainty_refs=("uncertainty:outcome",) if status == "UNCERTAIN" else (),
        safety_refs=("safety:synthetic:v1",),
        permission_refs=("permission:synthetic:v1",),
        resource_refs=("resource:synthetic:v1",),
        followup_candidate_refs=(),
        source_version_refs=versions,
        invalidation_refs=invalidations,
        trace_refs=(f"trace:{scenario_id}",),
        provenance_refs=provenance,
    )


SCENARIOS = (
    SyntheticScenarioV1("evidence_current_world", "SOURCE_RETURN", "valid Evidence to Current World candidate", "CURRENT_WORLD", _result("evidence_current_world")),
    SyntheticScenarioV1("evidence_field_event", "SOURCE_RETURN", "valid Evidence to Field Event candidate", "FIELD", _result("evidence_field_event")),
    SyntheticScenarioV1("evidence_both", "SOURCE_RETURN", "valid Evidence to independent both candidates", "BOTH", _result("evidence_both")),
    SyntheticScenarioV1("evidence_malformed", "SOURCE_RETURN", "malformed Evidence", "CURRENT_WORLD", _result("evidence_malformed", evidence=()), expected_blocked=True),
    SyntheticScenarioV1("evidence_stale", "SOURCE_RETURN", "stale Evidence", "CURRENT_WORLD", _result("evidence_stale", status="STALE", source_valid=False, invalidations=("invalidation:evidence-stale",)), expected_blocked=True),
    SyntheticScenarioV1("evidence_missing_provenance", "SOURCE_RETURN", "Evidence without provenance", "CURRENT_WORLD", _result("evidence_missing_provenance", provenance=()), expected_blocked=True),
    SyntheticScenarioV1("evidence_version_mismatch", "SOURCE_RETURN", "Evidence source-version mismatch", "CURRENT_WORLD", _result("evidence_version_mismatch", status="VERSION_MISMATCH", invalidations=("invalidation:version",)), expected_blocked=True),
    SyntheticScenarioV1("evidence_cross_concern", "SOURCE_RETURN", "cross-Concern Evidence", "CURRENT_WORLD", _result("evidence_cross_concern", concern_ref="concern:other"), expected_blocked=True),
    SyntheticScenarioV1("field_event_guard", "SOURCE_RETURN", "Field Event does not mutate Field", "FIELD", _result("field_event_guard"), observability_focus="field_mutation_false"),
    SyntheticScenarioV1("current_world_truth_guard", "SOURCE_RETURN", "Current World does not declare Truth", "CURRENT_WORLD", _result("current_world_truth_guard"), observability_focus="world_truth_false"),
    SyntheticScenarioV1("action_success_verified", "ACTION_RETURN", "Action success with effect Evidence", "BOTH", _result("action_success_verified", status="SUCCESS", evidence=("evidence:action-effect",))),
    SyntheticScenarioV1("action_success_unverified", "ACTION_RETURN", "Action success without verified effect", "CURRENT_WORLD", _result("action_success_unverified", status="UNVERIFIED_EFFECT", evidence=())),
    SyntheticScenarioV1("action_partial", "ACTION_RETURN", "partial Action result", "BOTH", _result("action_partial", status="PARTIAL")),
    SyntheticScenarioV1("action_failed", "ACTION_RETURN", "failed Action", "CURRENT_WORLD", _result("action_failed", status="FAILED", evidence=())),
    SyntheticScenarioV1("action_uncertain", "ACTION_RETURN", "uncertain Action result", "CURRENT_WORLD", _result("action_uncertain", status="UNCERTAIN", evidence=())),
    SyntheticScenarioV1("action_stale", "ACTION_RETURN", "stale Action result", "CURRENT_WORLD", _result("action_stale", status="STALE", source_valid=False, invalidations=("invalidation:action-stale",)), expected_blocked=True),
    SyntheticScenarioV1("outcome_valid", "OUTCOME_RETURN", "valid Outcome to Brain input", outcome=_outcome("outcome_valid")),
    SyntheticScenarioV1("outcome_partial", "OUTCOME_RETURN", "partial Outcome", outcome=_outcome("outcome_partial", status="PARTIAL_SUCCESS_CANDIDATE", partiality="PARTIAL")),
    SyntheticScenarioV1("outcome_uncertain", "OUTCOME_RETURN", "uncertain Outcome", outcome=_outcome("outcome_uncertain", status="UNCERTAIN", partiality="UNCERTAIN")),
    SyntheticScenarioV1("outcome_stale", "OUTCOME_RETURN", "stale Outcome", outcome=_outcome("outcome_stale", invalidations=("invalidation:outcome-stale",)), expected_blocked=True),
    SyntheticScenarioV1("outcome_missing_concern", "OUTCOME_RETURN", "Outcome missing Concern", outcome=_outcome("outcome_missing_concern", concern_ref=None), expected_blocked=True),
    SyntheticScenarioV1("outcome_revoked_grant", "OUTCOME_RETURN", "Outcome with revoked Grant", outcome=_outcome("outcome_revoked_grant", grant_ref="grant:revoked:v1"), expected_blocked=True),
    SyntheticScenarioV1("outcome_missing_provenance", "OUTCOME_RETURN", "Outcome without provenance", outcome=_outcome("outcome_missing_provenance", provenance=()), expected_blocked=True),
    SyntheticScenarioV1("brain_candidate_only", "OUTCOME_RETURN", "Brain input remains candidate-only", outcome=_outcome("brain_candidate_only"), observability_focus="brain_mutation_false"),
    SyntheticScenarioV1("observability_owner", "OBSERVABILITY", "owner and responsibility preserved", "CURRENT_WORLD", _result("observability_owner"), observability_focus="owner"),
    SyntheticScenarioV1("observability_versions", "OBSERVABILITY", "version refs preserved", "CURRENT_WORLD", _result("observability_versions"), observability_focus="versions"),
    SyntheticScenarioV1("observability_lineage", "OBSERVABILITY", "Evidence lineage reversible", "BOTH", _result("observability_lineage"), observability_focus="lineage"),
    SyntheticScenarioV1("observability_invalidation", "OBSERVABILITY", "invalidation refs preserved", "CURRENT_WORLD", _result("observability_invalidation", invalidations=("invalidation:synthetic",)), expected_blocked=True, observability_focus="invalidation"),
    SyntheticScenarioV1("observability_next_target", "OBSERVABILITY", "next target correct", "FIELD", _result("observability_next_target"), observability_focus="next_target"),
    SyntheticScenarioV1("observability_no_leakage", "OBSERVABILITY", "no runtime or mutation leakage", "BOTH", _result("observability_no_leakage"), observability_focus="negative_guards"),
)
