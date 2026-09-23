"""Luna Temporal Coordinate System v1.

This module is a domain-neutral, immutable temporal value layer.  It owns
coordinate semantics and temporal geometry only.  It does not own domain
truth, currentness, lifecycle, invalidation, admission, authorization, or
owner requery.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import json
from typing import Any, Mapping


TEMPORAL_COORDINATE_SCHEMA_VERSION_V1 = "luna.temporal_coordinate.v1"
TEMPORAL_COORDINATE_CONTRACT_VERSION_V1 = "luna.temporal_coordinate.contract.v1"


class TemporalCoordinateConstructionError(ValueError):
    """Raised when a temporal value violates its local typed contract."""


class _ValueEnum(str, Enum):
    """String enum base with stable wire values."""


class ClockKindV1(_ValueEnum):
    UTC_WALL = "utc_wall"
    PROCESS_MONOTONIC = "process_monotonic"
    DEVICE_MONOTONIC = "device_monotonic"
    DEVICE_TIMESTAMP = "device_timestamp"
    PROVIDER_TIMESTAMP = "provider_timestamp"
    EXTERNAL = "external"
    UNKNOWN = "unknown"


class TemporalUnitV1(_ValueEnum):
    NANOSECOND = "nanosecond"
    MICROSECOND = "microsecond"
    MILLISECOND = "millisecond"
    SECOND = "second"
    NATIVE_TICK = "native_tick"
    UNKNOWN = "unknown"


class TemporalOriginV1(_ValueEnum):
    UNIX_EPOCH_UTC = "unix_epoch_utc"
    PROCESS_START = "process_start"
    DEVICE_BOOT = "device_boot"
    PROVIDER_DEFINED = "provider_defined"
    EXTERNAL_DECLARED = "external_declared"
    UNKNOWN = "unknown"


class TemporalPersistenceScopeV1(_ValueEnum):
    PROCESS_ONLY = "process_only"
    DEVICE_SESSION = "device_session"
    DEVICE_PERSISTENT = "device_persistent"
    CROSS_PROCESS = "cross_process"
    CROSS_DEVICE = "cross_device"
    EXTERNAL_CONTRACT = "external_contract"
    UNKNOWN = "unknown"


class TemporalOrderingGuaranteeV1(_ValueEnum):
    STRICT_MONOTONIC = "strict_monotonic"
    NON_DECREASING = "non_decreasing"
    NONE = "none"
    UNKNOWN = "unknown"


class TemporalDurationSuitabilityV1(_ValueEnum):
    SAFE = "safe"
    CONDITIONAL = "conditional"
    UNSAFE = "unsafe"
    UNKNOWN = "unknown"


class ConditionalDurationOperationV1(_ValueEnum):
    BOUNDED_LOCAL_POLICY_DELTA = "bounded_local_policy_delta"


class ConditionalDurationBasisV1(_ValueEnum):
    DOMAIN_DECLARED_OPERATION = "domain_declared_operation"


class TemporalUncertaintyStatusV1(_ValueEnum):
    EXACT = "exact"
    BOUNDED = "bounded"
    ESTIMATED = "estimated"
    INFERRED = "inferred"
    UNKNOWN = "unknown"


class TemporalDerivationStatusV1(_ValueEnum):
    DIRECT = "direct"
    NORMALIZED = "normalized"
    ESTIMATED = "estimated"
    INFERRED = "inferred"
    MAPPED = "mapped"
    UNKNOWN = "unknown"


class TemporalMappingStatusV1(_ValueEnum):
    DECLARED = "declared"
    VERIFIED = "verified"
    UNKNOWN = "unknown"


class ComparabilityStatusV1(_ValueEnum):
    SAME_DOMAIN_COMPARABLE = "same_domain_comparable"
    MAPPED_DOMAIN_COMPARABLE = "mapped_domain_comparable"
    NOT_COMPARABLE = "not_comparable"
    UNKNOWN = "unknown"


class PointRelationV1(_ValueEnum):
    BEFORE = "before"
    AFTER = "after"
    EQUAL = "equal"
    UNCERTAIN = "uncertain"
    INCOMPARABLE = "incomparable"


class IntervalRelationV1(_ValueEnum):
    DISJOINT = "disjoint"
    OVERLAPS = "overlaps"
    CONTAINS = "contains"
    CONTAINED_BY = "contained_by"
    EQUAL = "equal"
    UNCERTAIN = "uncertain"
    INCOMPARABLE = "incomparable"


class TemporalDurationStatusV1(_ValueEnum):
    EXACT = "exact"
    UNCERTAIN = "uncertain"
    UNSUITABLE = "unsuitable"
    NOT_COMPARABLE = "not_comparable"
    UNKNOWN = "unknown"


def _require_nonempty_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise TemporalCoordinateConstructionError(
            f"{field_name} must be a non-empty string"
        )
    return value


def _require_enum(value: Any, enum_type: type[Enum], field_name: str) -> None:
    if not isinstance(value, enum_type):
        raise TypeError(f"{field_name} must be {enum_type.__name__}")


def _require_optional_nonnegative_int(value: Any, field_name: str) -> None:
    if value is None:
        return
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise TemporalCoordinateConstructionError(
            f"{field_name} must be a non-negative integer or None"
        )


def _require_schema(value: Any, expected: str) -> None:
    if value != expected:
        raise TemporalCoordinateConstructionError(
            f"schema_version must be {expected!r}"
        )


def _required_mapping(value: Any, field_name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise TypeError(f"{field_name} must be a mapping")
    return value


def _enum_from_wire(enum_type: type[_ValueEnum], value: Any, field_name: str) -> _ValueEnum:
    if not isinstance(value, str):
        raise TemporalCoordinateConstructionError(
            f"{field_name} must contain a canonical enum string"
        )
    try:
        return enum_type(value)
    except ValueError as exc:
        raise TemporalCoordinateConstructionError(
            f"unsupported {field_name}: {value!r}"
        ) from exc


def _clock_semantics_known(clock_domain: "ClockDomainV1") -> bool:
    return (
        clock_domain.clock_kind is not ClockKindV1.UNKNOWN
        and clock_domain.unit is not TemporalUnitV1.UNKNOWN
        and clock_domain.origin_semantics is not TemporalOriginV1.UNKNOWN
        and clock_domain.ordering_guarantee is not TemporalOrderingGuaranteeV1.UNKNOWN
    )


def _clock_semantics_equal(left: "ClockDomainV1", right: "ClockDomainV1") -> bool:
    return (
        left.clock_kind is right.clock_kind
        and left.unit is right.unit
        and left.origin_semantics is right.origin_semantics
        and left.persistence_scope is right.persistence_scope
        and left.ordering_guarantee is right.ordering_guarantee
        and left.duration_suitability is right.duration_suitability
    )


@dataclass(frozen=True)
class ConditionalDurationPolicyV1:
    """A domain contract declaration for one bounded duration operation.

    This value is not an authorization token or proof of authority.  It only
    identifies the domain-owned contract that permits a conditional duration
    operation when the Foundation checks all other temporal constraints.
    """

    policy_id: str
    policy_version: str
    applicable_domain_id: str
    allowed_operation: ConditionalDurationOperationV1
    semantic_basis: ConditionalDurationBasisV1

    def __post_init__(self) -> None:
        _require_nonempty_text(self.policy_id, "policy_id")
        _require_nonempty_text(self.policy_version, "policy_version")
        _require_nonempty_text(self.applicable_domain_id, "applicable_domain_id")
        _require_enum(
            self.allowed_operation,
            ConditionalDurationOperationV1,
            "allowed_operation",
        )
        _require_enum(
            self.semantic_basis,
            ConditionalDurationBasisV1,
            "semantic_basis",
        )


@dataclass(frozen=True)
class ClockDomainV1:
    """Typed identity and semantics for one numeric clock coordinate space."""

    domain_id: str
    clock_kind: ClockKindV1
    unit: TemporalUnitV1
    origin_semantics: TemporalOriginV1
    persistence_scope: TemporalPersistenceScopeV1
    ordering_guarantee: TemporalOrderingGuaranteeV1
    duration_suitability: TemporalDurationSuitabilityV1
    label: str | None = None
    schema_version: str = TEMPORAL_COORDINATE_SCHEMA_VERSION_V1

    def __post_init__(self) -> None:
        _require_nonempty_text(self.domain_id, "domain_id")
        for field_name, enum_type in (
            ("clock_kind", ClockKindV1),
            ("unit", TemporalUnitV1),
            ("origin_semantics", TemporalOriginV1),
            ("persistence_scope", TemporalPersistenceScopeV1),
            ("ordering_guarantee", TemporalOrderingGuaranteeV1),
            ("duration_suitability", TemporalDurationSuitabilityV1),
        ):
            _require_enum(getattr(self, field_name), enum_type, field_name)
        if self.label is not None:
            _require_nonempty_text(self.label, "label")
        _require_schema(self.schema_version, TEMPORAL_COORDINATE_SCHEMA_VERSION_V1)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "domain_id": self.domain_id,
            "clock_kind": self.clock_kind.value,
            "unit": self.unit.value,
            "origin_semantics": self.origin_semantics.value,
            "persistence_scope": self.persistence_scope.value,
            "ordering_guarantee": self.ordering_guarantee.value,
            "duration_suitability": self.duration_suitability.value,
            "label": self.label,
        }

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "ClockDomainV1":
        data = _required_mapping(value, "clock_domain")
        return cls(
            domain_id=data["domain_id"],
            clock_kind=_enum_from_wire(ClockKindV1, data["clock_kind"], "clock_kind"),
            unit=_enum_from_wire(TemporalUnitV1, data["unit"], "unit"),
            origin_semantics=_enum_from_wire(
                TemporalOriginV1, data["origin_semantics"], "origin_semantics"
            ),
            persistence_scope=_enum_from_wire(
                TemporalPersistenceScopeV1,
                data["persistence_scope"],
                "persistence_scope",
            ),
            ordering_guarantee=_enum_from_wire(
                TemporalOrderingGuaranteeV1,
                data["ordering_guarantee"],
                "ordering_guarantee",
            ),
            duration_suitability=_enum_from_wire(
                TemporalDurationSuitabilityV1,
                data["duration_suitability"],
                "duration_suitability",
            ),
            label=data.get("label"),
            schema_version=data.get("schema_version", ""),
        )


@dataclass(frozen=True)
class TemporalUncertaintyV1:
    """Bounded temporal precision/uncertainty, independent of confidence."""

    status: TemporalUncertaintyStatusV1
    precision_ticks: int | None = None
    uncertainty_before_ticks: int | None = None
    uncertainty_after_ticks: int | None = None
    schema_version: str = TEMPORAL_COORDINATE_SCHEMA_VERSION_V1

    def __post_init__(self) -> None:
        _require_enum(self.status, TemporalUncertaintyStatusV1, "status")
        for field_name in (
            "precision_ticks",
            "uncertainty_before_ticks",
            "uncertainty_after_ticks",
        ):
            _require_optional_nonnegative_int(getattr(self, field_name), field_name)
        if self.status is TemporalUncertaintyStatusV1.EXACT and any(
            value is not None
            for value in (
                self.precision_ticks,
                self.uncertainty_before_ticks,
                self.uncertainty_after_ticks,
            )
        ):
            raise TemporalCoordinateConstructionError(
                "EXACT uncertainty must use None for all precision/uncertainty fields"
            )
        if self.status in {
            TemporalUncertaintyStatusV1.BOUNDED,
            TemporalUncertaintyStatusV1.ESTIMATED,
            TemporalUncertaintyStatusV1.INFERRED,
        } and self.uncertainty_before_ticks is None and self.uncertainty_after_ticks is None:
            raise TemporalCoordinateConstructionError(
                f"{self.status.value} uncertainty requires at least one uncertainty bound"
            )
        if self.status is TemporalUncertaintyStatusV1.UNKNOWN and any(
            value is not None
            for value in (
                self.precision_ticks,
                self.uncertainty_before_ticks,
                self.uncertainty_after_ticks,
            )
        ):
            raise TemporalCoordinateConstructionError(
                "UNKNOWN uncertainty must use None for precision/uncertainty fields"
            )
        _require_schema(self.schema_version, TEMPORAL_COORDINATE_SCHEMA_VERSION_V1)

    def bounds_for(self, value_ticks: int) -> tuple[int, int] | None:
        """Return a closed possible-value range, or None if it is unknown."""

        if self.status is TemporalUncertaintyStatusV1.EXACT:
            return value_ticks, value_ticks
        if self.status is TemporalUncertaintyStatusV1.UNKNOWN:
            return None
        if self.uncertainty_before_ticks is None or self.uncertainty_after_ticks is None:
            return None
        return (
            value_ticks - self.uncertainty_before_ticks,
            value_ticks + self.uncertainty_after_ticks,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "status": self.status.value,
            "precision_ticks": self.precision_ticks,
            "uncertainty_before_ticks": self.uncertainty_before_ticks,
            "uncertainty_after_ticks": self.uncertainty_after_ticks,
        }

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "TemporalUncertaintyV1":
        data = _required_mapping(value, "uncertainty")
        return cls(
            status=_enum_from_wire(
                TemporalUncertaintyStatusV1, data["status"], "status"
            ),
            precision_ticks=data.get("precision_ticks"),
            uncertainty_before_ticks=data.get("uncertainty_before_ticks"),
            uncertainty_after_ticks=data.get("uncertainty_after_ticks"),
            schema_version=data.get("schema_version", ""),
        )


@dataclass(frozen=True)
class TemporalProvenanceV1:
    """Optional coordinate provenance, not Evidence provenance."""

    source_kind: str
    source_ref: str | None = None
    mapping_ref: str | None = None
    mapping_version: str | None = None
    derivation_status: TemporalDerivationStatusV1 = TemporalDerivationStatusV1.DIRECT
    schema_version: str = TEMPORAL_COORDINATE_SCHEMA_VERSION_V1

    def __post_init__(self) -> None:
        _require_nonempty_text(self.source_kind, "source_kind")
        for field_name in ("source_ref", "mapping_ref", "mapping_version"):
            value = getattr(self, field_name)
            if value is not None:
                _require_nonempty_text(value, field_name)
        _require_enum(
            self.derivation_status,
            TemporalDerivationStatusV1,
            "derivation_status",
        )
        if self.derivation_status is TemporalDerivationStatusV1.MAPPED and (
            not self.mapping_ref or not self.mapping_version
        ):
            raise TemporalCoordinateConstructionError(
                "MAPPED provenance requires mapping_ref and mapping_version"
            )
        _require_schema(self.schema_version, TEMPORAL_COORDINATE_SCHEMA_VERSION_V1)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "source_kind": self.source_kind,
            "source_ref": self.source_ref,
            "mapping_ref": self.mapping_ref,
            "mapping_version": self.mapping_version,
            "derivation_status": self.derivation_status.value,
        }

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "TemporalProvenanceV1":
        data = _required_mapping(value, "provenance")
        return cls(
            source_kind=data["source_kind"],
            source_ref=data.get("source_ref"),
            mapping_ref=data.get("mapping_ref"),
            mapping_version=data.get("mapping_version"),
            derivation_status=_enum_from_wire(
                TemporalDerivationStatusV1,
                data.get("derivation_status", TemporalDerivationStatusV1.DIRECT.value),
                "derivation_status",
            ),
            schema_version=data.get("schema_version", ""),
        )


@dataclass(frozen=True)
class TemporalPointV1:
    """One integer coordinate in one explicit ClockDomain."""

    value_ticks: int
    clock_domain: ClockDomainV1
    uncertainty: TemporalUncertaintyV1
    provenance: TemporalProvenanceV1 | None = None
    schema_version: str = TEMPORAL_COORDINATE_SCHEMA_VERSION_V1

    def __post_init__(self) -> None:
        if isinstance(self.value_ticks, bool) or not isinstance(self.value_ticks, int):
            raise TemporalCoordinateConstructionError("value_ticks must be an integer")
        if not isinstance(self.clock_domain, ClockDomainV1):
            raise TypeError("clock_domain must be ClockDomainV1")
        if not isinstance(self.uncertainty, TemporalUncertaintyV1):
            raise TypeError("uncertainty must be TemporalUncertaintyV1")
        if self.provenance is not None and not isinstance(
            self.provenance, TemporalProvenanceV1
        ):
            raise TypeError("provenance must be TemporalProvenanceV1 or None")
        _require_schema(self.schema_version, TEMPORAL_COORDINATE_SCHEMA_VERSION_V1)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "value_ticks": self.value_ticks,
            "clock_domain": self.clock_domain.to_dict(),
            "uncertainty": self.uncertainty.to_dict(),
            "provenance": self.provenance.to_dict() if self.provenance else None,
        }

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "TemporalPointV1":
        data = _required_mapping(value, "temporal_point")
        provenance = data.get("provenance")
        return cls(
            value_ticks=data["value_ticks"],
            clock_domain=ClockDomainV1.from_dict(data["clock_domain"]),
            uncertainty=TemporalUncertaintyV1.from_dict(data["uncertainty"]),
            provenance=(
                None
                if provenance is None
                else TemporalProvenanceV1.from_dict(provenance)
            ),
            schema_version=data.get("schema_version", ""),
        )


@dataclass(frozen=True)
class TemporalIntervalV1:
    """Half-open temporal geometry: [start, end)."""

    clock_domain: ClockDomainV1
    start: TemporalPointV1 | None
    end: TemporalPointV1 | None
    schema_version: str = TEMPORAL_COORDINATE_SCHEMA_VERSION_V1

    def __post_init__(self) -> None:
        if not isinstance(self.clock_domain, ClockDomainV1):
            raise TypeError("clock_domain must be ClockDomainV1")
        for field_name in ("start", "end"):
            value = getattr(self, field_name)
            if value is not None and not isinstance(value, TemporalPointV1):
                raise TypeError(f"{field_name} must be TemporalPointV1 or None")
            if value is not None and value.clock_domain.domain_id != self.clock_domain.domain_id:
                raise TemporalCoordinateConstructionError(
                    f"{field_name} domain_id must match interval clock_domain"
                )
            if value is not None and not _clock_semantics_equal(
                value.clock_domain, self.clock_domain
            ):
                raise TemporalCoordinateConstructionError(
                    f"{field_name} clock semantics must match interval clock_domain"
                )
        if self.start is not None and self.end is not None:
            if not _clock_semantics_equal(
                self.start.clock_domain, self.end.clock_domain
            ):
                raise TemporalCoordinateConstructionError(
                    "interval endpoints must use matching clock semantics"
                )
            if (
                self.start.uncertainty.status is TemporalUncertaintyStatusV1.EXACT
                and self.end.uncertainty.status is TemporalUncertaintyStatusV1.EXACT
                and self.end.value_ticks < self.start.value_ticks
            ):
                raise TemporalCoordinateConstructionError(
                    "interval end must not be before interval start"
                )
        _require_schema(self.schema_version, TEMPORAL_COORDINATE_SCHEMA_VERSION_V1)

    def is_empty(self) -> bool:
        return (
            self.start is not None
            and self.end is not None
            and self.start.uncertainty.status is TemporalUncertaintyStatusV1.EXACT
            and self.end.uncertainty.status is TemporalUncertaintyStatusV1.EXACT
            and self.start.value_ticks == self.end.value_ticks
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "clock_domain": self.clock_domain.to_dict(),
            "start": self.start.to_dict() if self.start else None,
            "end": self.end.to_dict() if self.end else None,
        }

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "TemporalIntervalV1":
        data = _required_mapping(value, "temporal_interval")
        return cls(
            clock_domain=ClockDomainV1.from_dict(data["clock_domain"]),
            start=(
                None
                if data["start"] is None
                else TemporalPointV1.from_dict(data["start"])
            ),
            end=(
                None
                if data["end"] is None
                else TemporalPointV1.from_dict(data["end"])
            ),
            schema_version=data.get("schema_version", ""),
        )


@dataclass(frozen=True)
class TemporalMappingV1:
    """Immutable mapping descriptor; it never executes a transformation."""

    mapping_ref: str
    mapping_version: str
    source_domain_id: str
    target_domain_id: str
    method: str
    status: TemporalMappingStatusV1
    schema_version: str = TEMPORAL_COORDINATE_SCHEMA_VERSION_V1

    def __post_init__(self) -> None:
        for field_name in (
            "mapping_ref",
            "mapping_version",
            "source_domain_id",
            "target_domain_id",
            "method",
        ):
            _require_nonempty_text(getattr(self, field_name), field_name)
        if self.source_domain_id == self.target_domain_id:
            raise TemporalCoordinateConstructionError(
                "mapping source and target domains must differ"
            )
        _require_enum(self.status, TemporalMappingStatusV1, "status")
        _require_schema(self.schema_version, TEMPORAL_COORDINATE_SCHEMA_VERSION_V1)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "mapping_ref": self.mapping_ref,
            "mapping_version": self.mapping_version,
            "source_domain_id": self.source_domain_id,
            "target_domain_id": self.target_domain_id,
            "method": self.method,
            "status": self.status.value,
        }

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "TemporalMappingV1":
        data = _required_mapping(value, "temporal_mapping")
        return cls(
            mapping_ref=data["mapping_ref"],
            mapping_version=data["mapping_version"],
            source_domain_id=data["source_domain_id"],
            target_domain_id=data["target_domain_id"],
            method=data["method"],
            status=_enum_from_wire(
                TemporalMappingStatusV1, data["status"], "status"
            ),
            schema_version=data.get("schema_version", ""),
        )


@dataclass(frozen=True)
class ComparabilityResultV1:
    status: ComparabilityStatusV1
    reason: str


@dataclass(frozen=True)
class PointRelationResultV1:
    relation: PointRelationV1
    comparability: ComparabilityStatusV1
    reason: str


@dataclass(frozen=True)
class IntervalRelationResultV1:
    relation: IntervalRelationV1
    comparability: ComparabilityStatusV1
    reason: str


@dataclass(frozen=True)
class TemporalDurationResultV1:
    status: TemporalDurationStatusV1
    duration_ticks: int | None
    comparability: ComparabilityStatusV1
    reason: str


def _domain_comparability(
    left: ClockDomainV1, right: ClockDomainV1
) -> ComparabilityResultV1:
    if left.domain_id != right.domain_id:
        return ComparabilityResultV1(
            ComparabilityStatusV1.NOT_COMPARABLE,
            "clock_domain_identity_mismatch",
        )
    if not _clock_semantics_known(left) or not _clock_semantics_known(right):
        return ComparabilityResultV1(
            ComparabilityStatusV1.UNKNOWN,
            "clock_domain_semantics_unknown",
        )
    if not _clock_semantics_equal(left, right):
        return ComparabilityResultV1(
            ComparabilityStatusV1.UNKNOWN,
            "same_domain_id_has_conflicting_semantics",
        )
    return ComparabilityResultV1(
        ComparabilityStatusV1.SAME_DOMAIN_COMPARABLE,
        "same_clock_domain_identity",
    )


def is_comparable(
    left: TemporalPointV1,
    right: TemporalPointV1,
    mapping: TemporalMappingV1 | None = None,
) -> ComparabilityResultV1:
    """Classify comparability without applying or trusting a mapping descriptor."""

    if not isinstance(left, TemporalPointV1) or not isinstance(right, TemporalPointV1):
        raise TypeError("is_comparable requires two TemporalPointV1 values")
    if mapping is not None and not isinstance(mapping, TemporalMappingV1):
        raise TypeError("mapping must be TemporalMappingV1 or None")
    result = _domain_comparability(left.clock_domain, right.clock_domain)
    if (
        result.status is ComparabilityStatusV1.NOT_COMPARABLE
        and mapping is not None
    ):
        return ComparabilityResultV1(
            ComparabilityStatusV1.NOT_COMPARABLE,
            "mapping_descriptor_does_not_execute_transformation",
        )
    return result


def _point_bounds(point: TemporalPointV1) -> tuple[int, int] | None:
    return point.uncertainty.bounds_for(point.value_ticks)


def _conditional_duration_policy_failure(
    policy: ConditionalDurationPolicyV1 | None,
    domain: ClockDomainV1,
) -> str | None:
    if policy is None:
        return "conditional_duration_policy_required"
    if policy.applicable_domain_id != domain.domain_id:
        return "conditional_duration_policy_domain_mismatch"
    if policy.allowed_operation is not ConditionalDurationOperationV1.BOUNDED_LOCAL_POLICY_DELTA:
        return "conditional_duration_policy_operation_mismatch"
    if policy.semantic_basis is not ConditionalDurationBasisV1.DOMAIN_DECLARED_OPERATION:
        return "conditional_duration_policy_basis_mismatch"
    return None


def compare_points(
    left: TemporalPointV1,
    right: TemporalPointV1,
    mapping: TemporalMappingV1 | None = None,
) -> PointRelationResultV1:
    """Compare points or return a typed non-comparable/uncertain result."""

    comparable = is_comparable(left, right, mapping)
    if comparable.status is not ComparabilityStatusV1.SAME_DOMAIN_COMPARABLE:
        return PointRelationResultV1(
            PointRelationV1.INCOMPARABLE,
            comparable.status,
            comparable.reason,
        )
    left_bounds = _point_bounds(left)
    right_bounds = _point_bounds(right)
    if left_bounds is None or right_bounds is None:
        return PointRelationResultV1(
            PointRelationV1.UNCERTAIN,
            comparable.status,
            "point_uncertainty_bounds_unknown",
        )
    left_lower, left_upper = left_bounds
    right_lower, right_upper = right_bounds
    if left_upper < right_lower:
        relation = PointRelationV1.BEFORE
    elif left_lower > right_upper:
        relation = PointRelationV1.AFTER
    elif left_lower == left_upper == right_lower == right_upper:
        relation = PointRelationV1.EQUAL
    else:
        relation = PointRelationV1.UNCERTAIN
    return PointRelationResultV1(relation, comparable.status, "point_ranges_evaluated")


def duration_between(
    start: TemporalPointV1,
    end: TemporalPointV1,
    mapping: TemporalMappingV1 | None = None,
    *,
    conditional_policy: ConditionalDurationPolicyV1 | None = None,
) -> TemporalDurationResultV1:
    """Return a numeric duration only under the domain duration contract."""

    if conditional_policy is not None and not isinstance(
        conditional_policy, ConditionalDurationPolicyV1
    ):
        raise TypeError(
            "conditional_policy must be ConditionalDurationPolicyV1 or None"
        )

    comparable = is_comparable(start, end, mapping)
    if comparable.status is ComparabilityStatusV1.UNKNOWN:
        return TemporalDurationResultV1(
            TemporalDurationStatusV1.UNKNOWN,
            None,
            comparable.status,
            comparable.reason,
        )
    if comparable.status is not ComparabilityStatusV1.SAME_DOMAIN_COMPARABLE:
        return TemporalDurationResultV1(
            TemporalDurationStatusV1.NOT_COMPARABLE,
            None,
            comparable.status,
            comparable.reason,
        )
    suitability = start.clock_domain.duration_suitability
    if suitability is TemporalDurationSuitabilityV1.UNKNOWN:
        return TemporalDurationResultV1(
            TemporalDurationStatusV1.UNKNOWN,
            None,
            comparable.status,
            "duration_suitability_unknown",
        )
    if suitability is TemporalDurationSuitabilityV1.UNSAFE:
        return TemporalDurationResultV1(
            TemporalDurationStatusV1.UNSUITABLE,
            None,
            comparable.status,
            f"duration_suitability_{suitability.value}",
        )
    if suitability is TemporalDurationSuitabilityV1.CONDITIONAL:
        policy_failure = _conditional_duration_policy_failure(
            conditional_policy,
            start.clock_domain,
        )
        if policy_failure is not None:
            return TemporalDurationResultV1(
                TemporalDurationStatusV1.UNSUITABLE,
                None,
                comparable.status,
                policy_failure,
            )
    if (
        start.uncertainty.status is not TemporalUncertaintyStatusV1.EXACT
        or end.uncertainty.status is not TemporalUncertaintyStatusV1.EXACT
    ):
        return TemporalDurationResultV1(
            TemporalDurationStatusV1.UNCERTAIN,
            None,
            comparable.status,
            "duration_endpoint_uncertainty_present",
        )
    return TemporalDurationResultV1(
        TemporalDurationStatusV1.EXACT,
        end.value_ticks - start.value_ticks,
        comparable.status,
        "safe_same_domain_exact_duration",
    )


def _interval_comparability(
    left: TemporalIntervalV1, right_domain: ClockDomainV1
) -> ComparabilityResultV1:
    return _domain_comparability(left.clock_domain, right_domain)


def contains(
    interval: TemporalIntervalV1,
    point: TemporalPointV1,
) -> IntervalRelationResultV1:
    """Classify half-open interval containment for one point."""

    if not isinstance(interval, TemporalIntervalV1) or not isinstance(
        point, TemporalPointV1
    ):
        raise TypeError("contains requires TemporalIntervalV1 and TemporalPointV1")
    comparable = _interval_comparability(interval, point.clock_domain)
    if comparable.status is not ComparabilityStatusV1.SAME_DOMAIN_COMPARABLE:
        return IntervalRelationResultV1(
            IntervalRelationV1.INCOMPARABLE,
            comparable.status,
            comparable.reason,
        )
    if interval.is_empty():
        return IntervalRelationResultV1(
            IntervalRelationV1.DISJOINT,
            comparable.status,
            "empty_interval_contains_no_point",
        )
    point_bounds = _point_bounds(point)
    if point_bounds is None:
        return IntervalRelationResultV1(
            IntervalRelationV1.UNCERTAIN,
            comparable.status,
            "point_uncertainty_bounds_unknown",
        )
    point_lower, point_upper = point_bounds
    start_bounds = _point_bounds(interval.start) if interval.start else None
    end_bounds = _point_bounds(interval.end) if interval.end else None
    if start_bounds is None and interval.start is not None:
        return IntervalRelationResultV1(
            IntervalRelationV1.UNCERTAIN,
            comparable.status,
            "interval_start_uncertainty_bounds_unknown",
        )
    if end_bounds is None and interval.end is not None:
        return IntervalRelationResultV1(
            IntervalRelationV1.UNCERTAIN,
            comparable.status,
            "interval_end_uncertainty_bounds_unknown",
        )
    if start_bounds and point_upper < start_bounds[0]:
        return IntervalRelationResultV1(
            IntervalRelationV1.DISJOINT,
            comparable.status,
            "point_before_interval_start",
        )
    if end_bounds and point_lower >= end_bounds[1]:
        return IntervalRelationResultV1(
            IntervalRelationV1.DISJOINT,
            comparable.status,
            "point_at_or_after_interval_end",
        )
    lower_certain = start_bounds is None or point_lower >= start_bounds[1]
    upper_certain = end_bounds is None or point_upper < end_bounds[0]
    relation = (
        IntervalRelationV1.CONTAINS
        if lower_certain and upper_certain
        else IntervalRelationV1.UNCERTAIN
    )
    return IntervalRelationResultV1(relation, comparable.status, "containment_evaluated")


def _exact_interval_relation(
    left: TemporalIntervalV1, right: TemporalIntervalV1
) -> IntervalRelationV1:
    if left.is_empty() or right.is_empty():
        return IntervalRelationV1.DISJOINT
    if left.end and right.start and left.end.value_ticks <= right.start.value_ticks:
        return IntervalRelationV1.DISJOINT
    if right.end and left.start and right.end.value_ticks <= left.start.value_ticks:
        return IntervalRelationV1.DISJOINT
    same_start = (
        left.start is None
        and right.start is None
    ) or (
        left.start is not None
        and right.start is not None
        and left.start.value_ticks == right.start.value_ticks
    )
    same_end = (
        left.end is None
        and right.end is None
    ) or (
        left.end is not None
        and right.end is not None
        and left.end.value_ticks == right.end.value_ticks
    )
    if same_start and same_end:
        return IntervalRelationV1.EQUAL
    left_contains_right = (
        left.start is None
        or (
            right.start is not None
            and left.start.value_ticks <= right.start.value_ticks
        )
    ) and (
        left.end is None
        or (right.end is not None and right.end.value_ticks <= left.end.value_ticks)
    )
    right_contains_left = (
        right.start is None
        or (
            left.start is not None
            and right.start.value_ticks <= left.start.value_ticks
        )
    ) and (
        right.end is None
        or (left.end is not None and left.end.value_ticks <= right.end.value_ticks)
    )
    if left_contains_right:
        return IntervalRelationV1.CONTAINS
    if right_contains_left:
        return IntervalRelationV1.CONTAINED_BY
    return IntervalRelationV1.OVERLAPS


def overlaps(
    left: TemporalIntervalV1,
    right: TemporalIntervalV1,
) -> IntervalRelationResultV1:
    """Classify half-open interval geometry without lifecycle semantics."""

    if not isinstance(left, TemporalIntervalV1) or not isinstance(
        right, TemporalIntervalV1
    ):
        raise TypeError("overlaps requires two TemporalIntervalV1 values")
    comparable = _interval_comparability(left, right.clock_domain)
    if comparable.status is not ComparabilityStatusV1.SAME_DOMAIN_COMPARABLE:
        return IntervalRelationResultV1(
            IntervalRelationV1.INCOMPARABLE,
            comparable.status,
            comparable.reason,
        )
    if left.is_empty() or right.is_empty():
        return IntervalRelationResultV1(
            IntervalRelationV1.DISJOINT,
            comparable.status,
            "empty_interval_has_no_overlap",
        )
    exact = all(
        point is None
        or point.uncertainty.status is TemporalUncertaintyStatusV1.EXACT
        for interval in (left, right)
        for point in (interval.start, interval.end)
    )
    if exact:
        relation = _exact_interval_relation(left, right)
        return IntervalRelationResultV1(relation, comparable.status, "interval_geometry_evaluated")
    if (
        left.end
        and right.start
        and _point_bounds(left.end)
        and _point_bounds(right.start)
        and _point_bounds(left.end)[1] <= _point_bounds(right.start)[0]
    ) or (
        right.end
        and left.start
        and _point_bounds(right.end)
        and _point_bounds(left.start)
        and _point_bounds(right.end)[1] <= _point_bounds(left.start)[0]
    ):
        return IntervalRelationResultV1(
            IntervalRelationV1.DISJOINT,
            comparable.status,
            "uncertainty_ranges_prove_disjoint",
        )
    return IntervalRelationResultV1(
        IntervalRelationV1.UNCERTAIN,
        comparable.status,
        "interval_endpoint_uncertainty_present",
    )


def classify_relation(
    left: TemporalPointV1 | TemporalIntervalV1,
    right: TemporalPointV1 | TemporalIntervalV1,
) -> PointRelationResultV1 | IntervalRelationResultV1:
    """Dispatch only between the two typed geometry families."""

    if isinstance(left, TemporalPointV1) and isinstance(right, TemporalPointV1):
        return compare_points(left, right)
    if isinstance(left, TemporalIntervalV1) and isinstance(right, TemporalIntervalV1):
        return overlaps(left, right)
    raise TypeError("classify_relation requires two points or two intervals")


def to_canonical_json_v1(
    value: ClockDomainV1
    | TemporalUncertaintyV1
    | TemporalProvenanceV1
    | TemporalPointV1
    | TemporalIntervalV1
    | TemporalMappingV1,
) -> str:
    """Serialize one supported temporal value deterministically as JSON."""

    supported_types = (
        ClockDomainV1,
        TemporalUncertaintyV1,
        TemporalProvenanceV1,
        TemporalPointV1,
        TemporalIntervalV1,
        TemporalMappingV1,
    )
    if not isinstance(value, supported_types):
        raise TypeError("value must be a supported temporal coordinate type")
    return json.dumps(
        value.to_dict(),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
