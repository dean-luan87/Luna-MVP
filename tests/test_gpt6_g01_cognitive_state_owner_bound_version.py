from __future__ import annotations

from dataclasses import replace

import capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_engine_v1 as cognitive_state_engine

from capabilities.midplatform.core.cognitive_flow.cognitive_dynamic_loop_types_v1 import (
    CognitiveStateVersionCandidateV1,
)
from capabilities.midplatform.core.cognitive_state_formation import (
    invalidate_cognitive_state_version_v1,
    issue_cognitive_state_version_v1,
    query_valid_cognitive_state_version_v1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_core_types_v1 import (
    SourceRefV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_engine_v1 import (
    CognitiveStateFormationEngineV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_io_types_v1 import (
    CognitiveStateFormationInputV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_registry_v1 import (
    COGNITIVE_STATE_PROFILE_CONTROLLED_EVALUATION_V1,
    COGNITIVE_STATE_PROFILE_PRODUCTION_CANONICAL,
)


def _ref(owner: str, ref_id: str) -> SourceRefV1:
    return SourceRefV1(owner, ref_id, "v1", f"trace:{ref_id}", f"provenance:{ref_id}")


def _formed_output():
    return CognitiveStateFormationEngineV1().run_case(
        CognitiveStateFormationInputV1(
            scenario_id="F09",
            context_refs=(_ref("Context", "context:f09"),),
            pcn_refs=(_ref("PCN", "pcn:f09"),),
            intent_refs=(_ref("Intent", "intent:f09"),),
            field_refs=(_ref("Field", "field:f09"),),
            observation_refs=(_ref("Observation", "observation:f09"),),
            evidence_refs=(_ref("Evidence", "evidence:f09"),),
            concern_refs=(_ref("Concern", "concern:f09"),),
            goal_refs=(_ref("Goal", "goal:f09"),),
            information_need_refs=(_ref("Need", "need:f09"),),
            task_refs=(_ref("Task", "task:f09"),),
            role_refs=(_ref("Role", "role:f09"),),
            relation_refs=(_ref("Field", "relation:f09"),),
            candidate_only=True,
            synthetic_only=True,
        )
    )


def test_candidate_cannot_be_issued_as_canonical_version() -> None:
    candidate = CognitiveStateVersionCandidateV1(
        state_version_ref="state:forged:v1",
        parent_state_version_ref=None,
        evidence_update_ref=None,
        current_disposition="UNKNOWN",
        current_minimum_need_ref=None,
        active_hypothesis_refs=(),
        invalidated_hypothesis_refs=(),
        sufficiency_ref=None,
        reconsideration_ref=None,
        trace_ref="trace:forged",
    )
    assert issue_cognitive_state_version_v1(candidate) is None  # type: ignore[arg-type]


def test_owner_issuance_generates_identity_and_validity_query() -> None:
    record = issue_cognitive_state_version_v1(_formed_output())
    assert record is not None
    assert record.owner_ref == "Cognitive State Formation Governance"
    assert record.candidate_only is False
    assert record.canonical is True
    assert query_valid_cognitive_state_version_v1(record.version_ref) is record


def test_caller_cannot_select_identity_or_promote_projection() -> None:
    output = _formed_output()
    forged = replace(output, semantic_authority=True)
    assert issue_cognitive_state_version_v1(forged) is None
    record = issue_cognitive_state_version_v1(output)
    assert record is not None
    assert record.version_ref != "state:caller-selected:v1"


def test_invalidation_fails_closed_but_newer_version_does_not_revoke_old() -> None:
    first = issue_cognitive_state_version_v1(_formed_output())
    second = issue_cognitive_state_version_v1(_formed_output())
    assert first is not None and second is not None
    assert query_valid_cognitive_state_version_v1(first.version_ref) is first
    assert query_valid_cognitive_state_version_v1(second.version_ref) is second
    invalidated = invalidate_cognitive_state_version_v1(
        first.version_ref,
        reason_ref="invalidation:f09:cstate",
    )
    assert invalidated is not None
    assert invalidated.status == "INVALIDATED"
    assert query_valid_cognitive_state_version_v1(first.version_ref) is None
    assert query_valid_cognitive_state_version_v1(second.version_ref) is second


def test_source_lineage_and_provenance_are_preserved_without_authority_transfer() -> None:
    record = issue_cognitive_state_version_v1(_formed_output())
    assert record is not None
    assert record.source_version_refs
    assert record.source_identity_refs
    assert record.alignment_basis_refs
    assert record.provenance_refs
    assert "world:F09" in record.source_identity_refs
    assert "field:f09" in record.source_identity_refs
    assert "evidence:f09" in record.source_identity_refs
    assert record.owner_ref != "Field State Reducer"


def test_controlled_and_production_profiles_are_isolated_and_unknown_fails_closed() -> None:
    production = issue_cognitive_state_version_v1(
        _formed_output(), profile_ref=COGNITIVE_STATE_PROFILE_PRODUCTION_CANONICAL
    )
    controlled = issue_cognitive_state_version_v1(
        _formed_output(), profile_ref=COGNITIVE_STATE_PROFILE_CONTROLLED_EVALUATION_V1
    )
    assert production is not None and controlled is not None
    assert query_valid_cognitive_state_version_v1(
        production.version_ref,
        profile_ref=COGNITIVE_STATE_PROFILE_CONTROLLED_EVALUATION_V1,
    ) is None
    assert query_valid_cognitive_state_version_v1(
        controlled.version_ref,
        profile_ref=COGNITIVE_STATE_PROFILE_CONTROLLED_EVALUATION_V1,
    ) is controlled
    assert issue_cognitive_state_version_v1(
        _formed_output(), profile_ref="cognitive-state-profile:unknown"
    ) is None
    assert issue_cognitive_state_version_v1(_formed_output(), profile_ref="") is None


def test_controlled_version_supports_ref_only_owner_requery() -> None:
    controlled = issue_cognitive_state_version_v1(
        _formed_output(),
        profile_ref=COGNITIVE_STATE_PROFILE_CONTROLLED_EVALUATION_V1,
    )
    assert controlled is not None
    assert query_valid_cognitive_state_version_v1(controlled.version_ref) is controlled
    assert (
        query_valid_cognitive_state_version_v1(
            controlled.version_ref,
            profile_ref=COGNITIVE_STATE_PROFILE_PRODUCTION_CANONICAL,
        )
        is None
    )

    invalidated = invalidate_cognitive_state_version_v1(
        controlled.version_ref,
        reason_ref="invalidate:ref-only",
    )
    assert invalidated is not None
    assert query_valid_cognitive_state_version_v1(controlled.version_ref) is None


def test_cognitive_state_owner_namespace_collision_fails_closed() -> None:
    controlled = issue_cognitive_state_version_v1(
        _formed_output(),
        profile_ref=COGNITIVE_STATE_PROFILE_CONTROLLED_EVALUATION_V1,
    )
    assert controlled is not None
    assert (
        cognitive_state_engine._register_owner_version_namespace_v1(
            replace(
                controlled,
                profile_ref=COGNITIVE_STATE_PROFILE_PRODUCTION_CANONICAL,
            )
        )
        is False
    )
    assert query_valid_cognitive_state_version_v1(controlled.version_ref) is controlled
