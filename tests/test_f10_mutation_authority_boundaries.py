from __future__ import annotations

import json
from dataclasses import FrozenInstanceError, replace

import pytest

from capabilities.midplatform.core.cognitive_flow.integration.brain_cognitive_loop_closure_assimilation_controlled.brain_cognitive_loop_closure_assimilation_engine_v1 import (
    run_brain_cognitive_case_v1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_core_types_v1 import (
    ProvenanceEnvelopeV1,
)
from capabilities.midplatform.core.cognitive_state_formation.integration.b2_current_world_cognitive_state_flow_controlled.b2_current_world_cognitive_state_flow_fixture_v1 import (
    _world,
)
def _gateway_case():
    case = run_brain_cognitive_case_v1("CASE_A_SUFFICIENT_STOP", "f10-boundary")
    proof = case.cognitive_proofs[-1]
    return case, proof


def test_gateway_proof_has_no_mutable_runtime_state_root() -> None:
    case, proof = _gateway_case()
    assert not hasattr(proof, "gateway_admission_runtime_state")
    assert not any(hasattr(query, "_records") for query in case.gateway_admission_queries)


def test_gateway_query_returns_immutable_current_record() -> None:
    case, proof = _gateway_case()
    query = case.gateway_admission_queries[-1]
    record = query.lookup(
        proof.gateway_execution_identity_ref,
        proof.gateway_admission_ref,
    )
    assert record is not None
    with pytest.raises(FrozenInstanceError):
        record.admission_state = "REVOKED"


def test_historical_admission_projection_requires_fresh_owner_query() -> None:
    case, proof = _gateway_case()
    query = case.gateway_admission_queries[-1]
    assert query.matches_canonical_admission(
        proof.gateway_execution_identity_ref,
        proof.gateway_admission_ref,
        proof.canonical_gateway_admission_result,
    ) is True
    substituted = replace(
        proof.canonical_gateway_admission_result,
        gateway_admission_ref="gateway-admission:historical-substitution",
    )
    assert query.matches_canonical_admission(
        proof.gateway_execution_identity_ref,
        proof.gateway_admission_ref,
        substituted,
    ) is False


def test_gateway_query_rejects_malformed_identity() -> None:
    case, proof = _gateway_case()
    query = case.gateway_admission_queries[-1]
    assert query.lookup("", proof.gateway_admission_ref) is None
    assert query.lookup(
        proof.gateway_execution_identity_ref, None
    ) is None


def test_current_world_snapshot_is_immutable_after_formation() -> None:
    world = _world(
        "world:f10",
        context="context:f10",
        observation="observation:f10",
    )
    before = world.source_versions
    with pytest.raises(FrozenInstanceError):
        world.source_versions += (("late", "v1"),)
    assert world.source_versions == before
    assert ("late", "v1") not in world.source_versions


def test_provenance_snapshot_is_immutable_after_formation() -> None:
    provenance = ProvenanceEnvelopeV1(
        source_refs=("source:f10",),
        owner_refs=("CState",),
        version_refs=("v1",),
        reverse_lookup=(("world:f10", ("source:f10",)),),
    )
    with pytest.raises(FrozenInstanceError):
        provenance.reverse_lookup += (("late", ("source:late",)),)


def test_caller_mapping_is_rejected_at_canonical_snapshot_boundary() -> None:
    world = _world(
        "world:f10",
        context="context:f10",
        observation="observation:f10",
    )
    with pytest.raises(TypeError):
        replace(world, source_versions={"current_world": "v1"})
    with pytest.raises(TypeError):
        replace(
            world,
            source_versions=(("current_world", "v1"), ["late", "v1"]),
        )


def test_snapshot_mapping_duplicate_keys_are_rejected() -> None:
    world = _world(
        "world:f10",
        context="context:f10",
        observation="observation:f10",
    )
    with pytest.raises(ValueError):
        replace(
            world,
            source_versions=(("current_world", "v1"), ("current_world", "v2")),
        )
    with pytest.raises(ValueError):
        ProvenanceEnvelopeV1(
            source_refs=("source:f10",),
            owner_refs=("CState",),
            version_refs=("v1",),
            reverse_lookup=(
                ("world:f10", ("source:f10",)),
                ("world:f10", ("source:other",)),
            ),
        )
    with pytest.raises(TypeError):
        ProvenanceEnvelopeV1(
            source_refs=("source:f10",),
            owner_refs=("CState",),
            version_refs=("v1",),
            reverse_lookup={"world:f10": ("source:f10",)},
        )


def test_snapshot_json_round_trip_reconstructs_canonical_tuples() -> None:
    world = _world(
        "world:f10",
        context="context:f10",
        observation="observation:f10",
    )
    encoded = json.dumps({"source_versions": world.source_versions})
    decoded = json.loads(encoded)
    reconstructed = tuple(tuple(item) for item in decoded["source_versions"])
    assert reconstructed == world.source_versions
