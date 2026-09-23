from __future__ import annotations

import ast
import json
from pathlib import Path

import pytest

from capabilities.midplatform.core.temporal_coordinate.temporal_coordinate_v1 import (
    ClockDomainV1,
    ClockKindV1,
    ComparabilityStatusV1,
    ConditionalDurationBasisV1,
    ConditionalDurationOperationV1,
    ConditionalDurationPolicyV1,
    IntervalRelationV1,
    PointRelationV1,
    TemporalCoordinateConstructionError,
    TemporalDerivationStatusV1,
    TemporalDurationStatusV1,
    TemporalDurationSuitabilityV1,
    TemporalIntervalV1,
    TemporalMappingStatusV1,
    TemporalMappingV1,
    TemporalOriginV1,
    TemporalOrderingGuaranteeV1,
    TemporalPersistenceScopeV1,
    TemporalPointV1,
    TemporalProvenanceV1,
    TemporalUncertaintyStatusV1,
    TemporalUncertaintyV1,
    TemporalUnitV1,
    compare_points,
    contains,
    duration_between,
    is_comparable,
    overlaps,
    to_canonical_json_v1,
)


SECOND = TemporalUnitV1.SECOND


def _domain(
    domain_id: str = "utc:test",
    *,
    kind: ClockKindV1 = ClockKindV1.UTC_WALL,
    unit: TemporalUnitV1 = SECOND,
    origin: TemporalOriginV1 = TemporalOriginV1.UNIX_EPOCH_UTC,
    persistence: TemporalPersistenceScopeV1 = TemporalPersistenceScopeV1.CROSS_PROCESS,
    ordering: TemporalOrderingGuaranteeV1 = TemporalOrderingGuaranteeV1.NON_DECREASING,
    suitability: TemporalDurationSuitabilityV1 = TemporalDurationSuitabilityV1.SAFE,
) -> ClockDomainV1:
    return ClockDomainV1(
        domain_id=domain_id,
        clock_kind=kind,
        unit=unit,
        origin_semantics=origin,
        persistence_scope=persistence,
        ordering_guarantee=ordering,
        duration_suitability=suitability,
    )


def _point(
    value: int,
    domain: ClockDomainV1 | None = None,
    *,
    uncertainty: TemporalUncertaintyV1 | None = None,
    provenance: TemporalProvenanceV1 | None = None,
) -> TemporalPointV1:
    return TemporalPointV1(
        value_ticks=value,
        clock_domain=domain or _domain(),
        uncertainty=uncertainty or TemporalUncertaintyV1(TemporalUncertaintyStatusV1.EXACT),
        provenance=provenance,
    )


def _conditional_policy(domain_id: str = "wall:conditional") -> ConditionalDurationPolicyV1:
    return ConditionalDurationPolicyV1(
        policy_id="policy:field-event-local-delta",
        policy_version="v1",
        applicable_domain_id=domain_id,
        allowed_operation=ConditionalDurationOperationV1.BOUNDED_LOCAL_POLICY_DELTA,
        semantic_basis=ConditionalDurationBasisV1.DOMAIN_DECLARED_OPERATION,
    )


def test_same_domain_before_after_equal() -> None:
    assert compare_points(_point(1), _point(2)).relation is PointRelationV1.BEFORE
    assert compare_points(_point(2), _point(1)).relation is PointRelationV1.AFTER
    assert compare_points(_point(2), _point(2)).relation is PointRelationV1.EQUAL


def test_different_domain_is_incomparable_even_when_structurally_identical() -> None:
    left = _point(1, _domain("clock:a"))
    right = _point(2, _domain("clock:b"))
    assert is_comparable(left, right).status is ComparabilityStatusV1.NOT_COMPARABLE
    assert compare_points(left, right).relation is PointRelationV1.INCOMPARABLE


def test_same_domain_id_with_conflicting_definition_fails_closed() -> None:
    left_domain = _domain("clock:conflict")
    right_domain = _domain(
        "clock:conflict",
        unit=TemporalUnitV1.MILLISECOND,
    )
    left = _point(1, left_domain)
    right = _point(2, right_domain)

    comparable = is_comparable(left, right)
    assert comparable.status is ComparabilityStatusV1.UNKNOWN
    assert comparable.reason == "same_domain_id_has_conflicting_semantics"

    relation = compare_points(left, right)
    assert relation.comparability is ComparabilityStatusV1.UNKNOWN
    assert relation.relation is PointRelationV1.INCOMPARABLE
    assert relation.relation not in {
        PointRelationV1.BEFORE,
        PointRelationV1.AFTER,
        PointRelationV1.EQUAL,
    }

    duration = duration_between(left, right)
    assert duration.duration_ticks is None
    assert duration.status is TemporalDurationStatusV1.UNKNOWN


def test_utc_and_monotonic_are_incomparable() -> None:
    mono = _domain(
        "mono:test",
        kind=ClockKindV1.PROCESS_MONOTONIC,
        origin=TemporalOriginV1.PROCESS_START,
        persistence=TemporalPersistenceScopeV1.PROCESS_ONLY,
        ordering=TemporalOrderingGuaranteeV1.STRICT_MONOTONIC,
    )
    result = compare_points(_point(1), _point(2, mono))
    assert result.comparability is ComparabilityStatusV1.NOT_COMPARABLE
    assert result.relation is PointRelationV1.INCOMPARABLE


def test_unknown_clock_semantics_fail_closed() -> None:
    unknown = _domain(
        "clock:unknown",
        kind=ClockKindV1.UNKNOWN,
        unit=TemporalUnitV1.UNKNOWN,
        origin=TemporalOriginV1.UNKNOWN,
        persistence=TemporalPersistenceScopeV1.UNKNOWN,
        ordering=TemporalOrderingGuaranteeV1.UNKNOWN,
        suitability=TemporalDurationSuitabilityV1.UNKNOWN,
    )
    result = compare_points(_point(1, unknown), _point(2, unknown))
    assert result.comparability is ComparabilityStatusV1.UNKNOWN
    assert result.relation is PointRelationV1.INCOMPARABLE


def test_tick_type_rejects_bool_and_float_and_accepts_negative() -> None:
    with pytest.raises(TemporalCoordinateConstructionError):
        _point(True)  # type: ignore[arg-type]
    with pytest.raises(TemporalCoordinateConstructionError):
        _point(1.5)  # type: ignore[arg-type]
    assert _point(-10).value_ticks == -10


def test_uncertainty_exact_invariant_and_bounded_geometry() -> None:
    exact = TemporalUncertaintyV1(TemporalUncertaintyStatusV1.EXACT)
    assert exact.bounds_for(4) == (4, 4)
    with pytest.raises(TemporalCoordinateConstructionError):
        TemporalUncertaintyV1(TemporalUncertaintyStatusV1.EXACT, precision_ticks=1)
    unknown = TemporalUncertaintyV1(TemporalUncertaintyStatusV1.UNKNOWN)
    assert unknown.bounds_for(4) is None
    with pytest.raises(TemporalCoordinateConstructionError):
        TemporalUncertaintyV1(
            TemporalUncertaintyStatusV1.UNKNOWN,
            uncertainty_before_ticks=1,
        )
    bounded = TemporalUncertaintyV1(
        TemporalUncertaintyStatusV1.BOUNDED,
        precision_ticks=1,
        uncertainty_before_ticks=2,
        uncertainty_after_ticks=3,
    )
    assert bounded.bounds_for(10) == (8, 13)


def test_overlapping_uncertainty_is_uncertain() -> None:
    uncertainty = TemporalUncertaintyV1(
        TemporalUncertaintyStatusV1.BOUNDED,
        uncertainty_before_ticks=2,
        uncertainty_after_ticks=2,
    )
    result = compare_points(_point(10, uncertainty=uncertainty), _point(11))
    assert result.relation is PointRelationV1.UNCERTAIN


def test_touching_uncertainty_ranges_are_uncertain() -> None:
    touching = TemporalUncertaintyV1(
        TemporalUncertaintyStatusV1.BOUNDED,
        uncertainty_before_ticks=1,
        uncertainty_after_ticks=1,
    )
    left = _point(1, uncertainty=touching)
    right = _point(3, uncertainty=touching)

    result = compare_points(left, right)
    assert result.relation is PointRelationV1.UNCERTAIN
    assert result.relation not in {
        PointRelationV1.BEFORE,
        PointRelationV1.AFTER,
        PointRelationV1.EQUAL,
    }


def test_non_overlapping_uncertainty_keeps_deterministic_order() -> None:
    uncertainty = TemporalUncertaintyV1(
        TemporalUncertaintyStatusV1.BOUNDED,
        uncertainty_before_ticks=1,
        uncertainty_after_ticks=1,
    )
    result = compare_points(_point(10, uncertainty=uncertainty), _point(20))
    assert result.relation is PointRelationV1.BEFORE


def test_half_open_interval_contains_start_not_end() -> None:
    interval = TemporalIntervalV1(_domain(), _point(1), _point(3))
    assert contains(interval, _point(1)).relation is IntervalRelationV1.CONTAINS
    assert contains(interval, _point(2)).relation is IntervalRelationV1.CONTAINS
    assert contains(interval, _point(3)).relation is IntervalRelationV1.DISJOINT


def test_zero_interval_is_empty() -> None:
    interval = TemporalIntervalV1(_domain(), _point(2), _point(2))
    assert interval.is_empty() is True
    assert contains(interval, _point(2)).relation is IntervalRelationV1.DISJOINT


def test_open_ended_and_fully_unbounded_intervals() -> None:
    domain = _domain()
    left_open = TemporalIntervalV1(domain, None, _point(3))
    right_open = TemporalIntervalV1(domain, _point(3), None)
    unbounded = TemporalIntervalV1(domain, None, None)
    assert contains(left_open, _point(-1)).relation is IntervalRelationV1.CONTAINS
    assert contains(right_open, _point(3)).relation is IntervalRelationV1.CONTAINS
    assert contains(unbounded, _point(999)).relation is IntervalRelationV1.CONTAINS
    assert "currentness" not in unbounded.to_dict()
    assert "authorized" not in unbounded.to_dict()


def test_invalid_interval_and_endpoint_domain_mismatch_rejected() -> None:
    with pytest.raises(TemporalCoordinateConstructionError):
        TemporalIntervalV1(_domain(), _point(4), _point(3))
    with pytest.raises(TemporalCoordinateConstructionError):
        TemporalIntervalV1(_domain("clock:a"), _point(1, _domain("clock:b")), None)


def test_interval_relations_use_half_open_geometry() -> None:
    domain = _domain()
    left = TemporalIntervalV1(domain, _point(1), _point(3))
    right = TemporalIntervalV1(domain, _point(3), _point(5))
    assert overlaps(left, right).relation is IntervalRelationV1.DISJOINT
    contained = TemporalIntervalV1(domain, _point(2), _point(3))
    assert overlaps(left, contained).relation is IntervalRelationV1.CONTAINS


def test_duration_requires_safe_same_domain_and_exact_points() -> None:
    assert duration_between(_point(2), _point(5)).duration_ticks == 3
    unsafe = _domain(
        "wall:unsafe",
        suitability=TemporalDurationSuitabilityV1.UNSAFE,
    )
    conditional = _domain(
        "wall:conditional",
        suitability=TemporalDurationSuitabilityV1.CONDITIONAL,
    )
    assert duration_between(_point(2, unsafe), _point(5, unsafe)).status is TemporalDurationStatusV1.UNSUITABLE
    assert duration_between(_point(2, conditional), _point(5, conditional)).status is TemporalDurationStatusV1.UNSUITABLE
    unknown = _domain(
        "wall:unknown",
        suitability=TemporalDurationSuitabilityV1.UNKNOWN,
    )
    assert duration_between(_point(2, unknown), _point(5, unknown)).status is TemporalDurationStatusV1.UNKNOWN
    uncertain = TemporalUncertaintyV1(
        TemporalUncertaintyStatusV1.BOUNDED,
        uncertainty_before_ticks=1,
        uncertainty_after_ticks=1,
    )
    assert duration_between(_point(2, uncertainty=uncertain), _point(5)).status is TemporalDurationStatusV1.UNCERTAIN


def test_safe_duration_with_conditional_policy_keeps_safe_semantics() -> None:
    safe = _domain("wall:safe")
    result = duration_between(
        _point(2, safe),
        _point(5, safe),
        conditional_policy=_conditional_policy("wall:other"),
    )
    assert result.status is TemporalDurationStatusV1.EXACT
    assert result.duration_ticks == 3


def test_conditional_duration_requires_matching_policy() -> None:
    domain = _domain(
        "wall:conditional",
        suitability=TemporalDurationSuitabilityV1.CONDITIONAL,
    )
    assert duration_between(_point(2, domain), _point(5, domain)).status is TemporalDurationStatusV1.UNSUITABLE
    result = duration_between(
        _point(2, domain),
        _point(5, domain),
        conditional_policy=_conditional_policy(),
    )
    assert result.status is TemporalDurationStatusV1.EXACT
    assert result.duration_ticks == 3


def test_conditional_duration_policy_domain_mismatch_is_blocked() -> None:
    domain = _domain(
        "wall:conditional",
        suitability=TemporalDurationSuitabilityV1.CONDITIONAL,
    )
    result = duration_between(
        _point(2, domain),
        _point(5, domain),
        conditional_policy=_conditional_policy("wall:other"),
    )
    assert result.status is TemporalDurationStatusV1.UNSUITABLE
    assert result.duration_ticks is None
    assert result.reason == "conditional_duration_policy_domain_mismatch"


@pytest.mark.parametrize("field_name", ["policy_id", "policy_version", "applicable_domain_id"])
def test_conditional_duration_policy_requires_nonempty_identity_fields(field_name: str) -> None:
    values = {
        "policy_id": "policy:test",
        "policy_version": "v1",
        "applicable_domain_id": "wall:conditional",
        "allowed_operation": ConditionalDurationOperationV1.BOUNDED_LOCAL_POLICY_DELTA,
        "semantic_basis": ConditionalDurationBasisV1.DOMAIN_DECLARED_OPERATION,
    }
    values[field_name] = ""
    with pytest.raises(TemporalCoordinateConstructionError):
        ConditionalDurationPolicyV1(**values)


def test_conditional_duration_policy_rejects_untyped_enum_values() -> None:
    with pytest.raises(TypeError):
        ConditionalDurationPolicyV1(
            policy_id="policy:test",
            policy_version="v1",
            applicable_domain_id="wall:conditional",
            allowed_operation="bounded_local_policy_delta",  # type: ignore[arg-type]
            semantic_basis=ConditionalDurationBasisV1.DOMAIN_DECLARED_OPERATION,
        )
    with pytest.raises(TypeError):
        ConditionalDurationPolicyV1(
            policy_id="policy:test",
            policy_version="v1",
            applicable_domain_id="wall:conditional",
            allowed_operation=ConditionalDurationOperationV1.BOUNDED_LOCAL_POLICY_DELTA,
            semantic_basis="domain_declared_operation",  # type: ignore[arg-type]
        )


def test_conditional_policy_cannot_upgrade_unsafe_or_unknown_domains() -> None:
    unsafe = _domain(
        "wall:unsafe",
        suitability=TemporalDurationSuitabilityV1.UNSAFE,
    )
    unknown = _domain(
        "wall:unknown",
        kind=ClockKindV1.UNKNOWN,
        unit=TemporalUnitV1.UNKNOWN,
        origin=TemporalOriginV1.UNKNOWN,
        persistence=TemporalPersistenceScopeV1.UNKNOWN,
        ordering=TemporalOrderingGuaranteeV1.UNKNOWN,
        suitability=TemporalDurationSuitabilityV1.UNKNOWN,
    )
    assert duration_between(
        _point(2, unsafe), _point(5, unsafe), conditional_policy=_conditional_policy("wall:unsafe")
    ).status is TemporalDurationStatusV1.UNSUITABLE
    assert duration_between(
        _point(2, unknown), _point(5, unknown), conditional_policy=_conditional_policy("wall:unknown")
    ).status is TemporalDurationStatusV1.UNKNOWN


def test_conditional_policy_cannot_bypass_domain_or_semantic_conflicts() -> None:
    left = _point(
        1,
        _domain("wall:conditional", suitability=TemporalDurationSuitabilityV1.CONDITIONAL),
    )
    right = _point(
        2,
        _domain("wall:other", suitability=TemporalDurationSuitabilityV1.CONDITIONAL),
    )
    assert duration_between(
        left,
        right,
        conditional_policy=_conditional_policy("wall:conditional"),
    ).status is TemporalDurationStatusV1.NOT_COMPARABLE

    conflicting = _domain(
        "wall:conditional",
        unit=TemporalUnitV1.MILLISECOND,
        suitability=TemporalDurationSuitabilityV1.CONDITIONAL,
    )
    result = duration_between(
        left,
        _point(2, conflicting),
        conditional_policy=_conditional_policy("wall:conditional"),
    )
    assert result.status is TemporalDurationStatusV1.UNKNOWN
    assert result.duration_ticks is None


def test_conditional_policy_cannot_bypass_uncertainty() -> None:
    domain = _domain(
        "wall:conditional",
        suitability=TemporalDurationSuitabilityV1.CONDITIONAL,
    )
    uncertainty = TemporalUncertaintyV1(
        TemporalUncertaintyStatusV1.BOUNDED,
        uncertainty_before_ticks=1,
        uncertainty_after_ticks=1,
    )
    result = duration_between(
        _point(2, domain, uncertainty=uncertainty),
        _point(5, domain),
        conditional_policy=_conditional_policy(),
    )
    assert result.status is TemporalDurationStatusV1.UNCERTAIN
    assert result.duration_ticks is None


def test_conditional_policy_does_not_change_point_comparison() -> None:
    domain = _domain(
        "wall:conditional",
        suitability=TemporalDurationSuitabilityV1.CONDITIONAL,
    )
    assert compare_points(_point(2, domain), _point(5, domain)).relation is PointRelationV1.BEFORE


def test_conditional_policy_value_is_immutable_and_deterministic() -> None:
    first = _conditional_policy()
    second = _conditional_policy()
    assert first == second
    assert first.policy_id == "policy:field-event-local-delta"
    assert first.policy_version == "v1"
    with pytest.raises(AttributeError):
        first.policy_id = "policy:changed"  # type: ignore[misc]


def test_cross_domain_duration_fails_closed() -> None:
    mono = _domain(
        "mono:test",
        kind=ClockKindV1.PROCESS_MONOTONIC,
        origin=TemporalOriginV1.PROCESS_START,
        persistence=TemporalPersistenceScopeV1.PROCESS_ONLY,
        ordering=TemporalOrderingGuaranteeV1.STRICT_MONOTONIC,
    )
    result = duration_between(_point(1), _point(2, mono))
    assert result.status is TemporalDurationStatusV1.NOT_COMPARABLE
    assert result.duration_ticks is None


def test_mapping_descriptor_does_not_grant_comparability_or_transform_ticks() -> None:
    mapping = TemporalMappingV1(
        mapping_ref="mapping:one",
        mapping_version="v1",
        source_domain_id="clock:a",
        target_domain_id="clock:b",
        method="declared_only",
        status=TemporalMappingStatusV1.VERIFIED,
    )
    left = _point(1, _domain("clock:a"))
    right = _point(2, _domain("clock:b"))
    result = is_comparable(left, right, mapping)
    assert result.status is ComparabilityStatusV1.NOT_COMPARABLE
    assert compare_points(left, right, mapping).relation is PointRelationV1.INCOMPARABLE
    assert left.value_ticks == 1
    assert right.value_ticks == 2


def test_provenance_requires_mapping_metadata_for_mapped_derivation() -> None:
    provenance = TemporalProvenanceV1(
        source_kind="provider",
        source_ref="provider:clock",
        mapping_ref="mapping:one",
        mapping_version="v1",
        derivation_status=TemporalDerivationStatusV1.MAPPED,
    )
    assert provenance.mapping_ref == "mapping:one"
    with pytest.raises(TemporalCoordinateConstructionError):
        TemporalProvenanceV1(
            source_kind="provider",
            derivation_status=TemporalDerivationStatusV1.MAPPED,
        )


def test_deterministic_roundtrip_for_all_wire_types() -> None:
    domain = _domain()
    uncertainty = TemporalUncertaintyV1(
        TemporalUncertaintyStatusV1.BOUNDED,
        precision_ticks=1,
        uncertainty_before_ticks=2,
        uncertainty_after_ticks=3,
    )
    provenance = TemporalProvenanceV1(
        source_kind="camera",
        source_ref="camera:one",
        derivation_status=TemporalDerivationStatusV1.DIRECT,
    )
    point = _point(7, domain, uncertainty=uncertainty, provenance=provenance)
    interval = TemporalIntervalV1(domain, point, None)
    mapping = TemporalMappingV1(
        mapping_ref="mapping:one",
        mapping_version="v1",
        source_domain_id="clock:a",
        target_domain_id="clock:b",
        method="declared_only",
        status=TemporalMappingStatusV1.DECLARED,
    )
    values = (
        domain,
        uncertainty,
        provenance,
        point,
        interval,
        mapping,
    )
    classes = (
        ClockDomainV1,
        TemporalUncertaintyV1,
        TemporalProvenanceV1,
        TemporalPointV1,
        TemporalIntervalV1,
        TemporalMappingV1,
    )
    for value, cls in zip(values, classes):
        encoded_a = to_canonical_json_v1(value)
        encoded_b = to_canonical_json_v1(value)
        assert encoded_a == encoded_b
        decoded = cls.from_dict(json.loads(encoded_a))
        assert decoded.to_dict() == value.to_dict()
        assert "float" not in encoded_a


def test_wire_enums_are_strings_and_ticks_are_integers() -> None:
    payload = _point(-3).to_dict()
    assert isinstance(payload["value_ticks"], int)
    assert isinstance(payload["clock_domain"]["clock_kind"], str)
    assert isinstance(payload["uncertainty"]["status"], str)


def test_static_architecture_guard_and_contract_negatives() -> None:
    module_path = Path(__file__).parents[2] / "capabilities/midplatform/core/temporal_coordinate/temporal_coordinate_v1.py"
    module_source = module_path.read_text(encoding="utf-8")
    tree = ast.parse(module_source)
    imported_modules = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_modules.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_modules.append(node.module)
    assert all(not name.startswith("capabilities") for name in imported_modules)
    assert not any("Owner" in node.name or "Manager" in node.name or "Registry" in node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef))
    assert not any(
        token in module_source
        for token in (
            "allow_conditional",
            "unsafe_override",
            "skip_validation",
            "trust_caller",
            "assume_safe",
            "force=True",
        )
    )
    contract_path = module_path.with_name("temporal_coordinate_contract_v1.json")
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    assert contract["system_class"] == "SYSTEM_PRIMITIVE"
    authority = contract["authority_boundary"]
    assert authority["domain_truth_authority"] is False
    assert authority["currentness_authority"] is False
    assert authority["effect_eligibility_authority"] is False
    assert authority["admission_authority"] is False
    assert authority["domain_mutation_authority"] is False
    assert authority["global_manager"] is False
    assert authority["registry"] is False
    assert authority["mapping_engine"] is False
    assert authority["automatic_clock_mapping"] is False
    assert authority["domain_imports"] is False
    conditional = contract["semantics"]["conditional_duration"]
    assert conditional["policy_type"] == "ConditionalDurationPolicyV1"
    assert conditional["policy_semantics"] == "domain_contract_declaration_not_authority_proof"
    assert conditional["requires_explicit_policy"] is True
    assert conditional["unsafe_policy_bypass"] is False
    assert conditional["unknown_policy_bypass"] is False
    assert conditional["caller_boolean_escape_hatch"] is False
    assert conditional["policy_registry"] is False
    assert conditional["policy_store"] is False
