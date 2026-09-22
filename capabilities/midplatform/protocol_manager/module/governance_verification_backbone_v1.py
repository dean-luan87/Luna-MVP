"""Deterministic governance verification backbone for controlled phases.

This module extends the existing Protocol Manager boundary.  It is a typed
governance verification layer: it resolves declared governance scope, checks
authority/responsibility symmetry, validates common boundary flags, and
computes a final verification decision.  It supports candidate-only phases
and explicitly non-runtime authoritative decisions.  It never executes a
business module, mutates a registry, invokes a provider, or becomes a new
semantic owner.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping, Optional, Tuple


OWNER = "Protocol Manager"
VERSION = "v1"
CONSTITUTION_SOURCE_REF = (
    "docs/architecture/luna_system_constitution_governance_v1/"
    "luna_system_constitution_v1.md"
)
PROTOCOL_SOURCE_REF = (
    "docs/architecture/cognitive_governance_plane_v1/"
    "protocol_manager_governance_manual_v1.md"
)
ARCHITECTURE_SOURCE_REF = "docs/architecture/LUNA_ENGINEERING_ARCHITECTURE_CONSTITUTION_V1.md"
KNOWN_RULE_SOURCES = (
    CONSTITUTION_SOURCE_REF,
    PROTOCOL_SOURCE_REF,
    ARCHITECTURE_SOURCE_REF,
)

RULE_GOVERNED_EXECUTION = "RULE_GOVERNED_EXECUTION"
AUTHORITY_RESPONSIBILITY_UNITY = "AUTHORITY_RESPONSIBILITY_UNITY"
NO_AUTHORITY_WITHOUT_RESPONSIBILITY = "NO_AUTHORITY_WITHOUT_RESPONSIBILITY"
NO_RESPONSIBILITY_WITHOUT_AUTHORITY = "NO_RESPONSIBILITY_WITHOUT_AUTHORITY"
OWNER_BOUNDARY_REQUIRED = "OWNER_BOUNDARY_REQUIRED"
CANDIDATE_IS_NOT_AUTHORITY = "CANDIDATE_IS_NOT_AUTHORITY"
NO_TRUTH_WITHOUT_TRUTH_AUTHORITY = "NO_TRUTH_WITHOUT_TRUTH_AUTHORITY"
NO_RUNTIME_WITHOUT_RUNTIME_AUTHORITY = "NO_RUNTIME_WITHOUT_RUNTIME_AUTHORITY"
REQUESTER_OWNS_REQUIREMENT_COMPLEXITY = "REQUESTER_OWNS_REQUIREMENT_COMPLEXITY"
EXECUTOR_OWNS_EXECUTION_COMPLEXITY = "EXECUTOR_OWNS_EXECUTION_COMPLEXITY"
FAILURE_RESPONSIBILITY_FOLLOWS_AUTHORITY = "FAILURE_RESPONSIBILITY_FOLLOWS_AUTHORITY"
ADAPTER_HAS_NO_SEMANTIC_AUTHORITY = "ADAPTER_HAS_NO_SEMANTIC_AUTHORITY"

BLOCKER = "BLOCKER"
WARNING = "WARNING"

COMMON_GOVERNANCE_PROFILES = (
    "GOVERNED_EXECUTION",
    "AUTHORITY_RESPONSIBILITY",
    "CANDIDATE_ONLY",
    "READ_ONLY",
    "NO_TRUTH",
    "NO_WORLD_MUTATION",
    "NO_RUNTIME",
    "NO_PROVIDER_INVOCATION",
    "NO_MODEL_INVOCATION",
    "NO_DECISION_ACTION_TASK",
    "REQUESTER_EXECUTOR_BOUNDARY",
    "ADAPTER_BOUNDARY",
)

# These fields describe real runtime signals.  Mechanical record formation
# uses the explicitly namespaced fields below and must not suppress these
# checks.
RUNTIME_SIGNAL_FIELDS = (
    "runtime_started",
    "provider_session_started",
    "gateway_submission",
    "execution_instance_created",
    "resource_allocated",
)

# These fields are scoped to controlled mechanical records.  They do not
# assert that a runtime instance, provider session, gateway request, or real
# resource was created.
MECHANICAL_RECORD_FIELDS = (
    "mechanical_provider_session_record_created",
    "mechanical_execution_identity_record_created",
    "mechanical_resource_allocation_record_created",
)


def _unique(values: Iterable[str]) -> Tuple[str, ...]:
    return tuple(dict.fromkeys(value for value in values if value and value.strip()))


@dataclass(frozen=True)
class GovernanceRuleV1:
    rule_ref: str
    rule_name: str
    rule_owner_ref: str
    rule_source_ref: str
    rule_version: str
    severity: str
    rule_domain: str
    applies_to_domains: Tuple[str, ...]
    applies_to_owners: Tuple[str, ...]
    applies_to_profiles: Tuple[str, ...]
    applies_to_contract_refs: Tuple[str, ...]
    trigger_refs: Tuple[str, ...]
    required_invariants: Tuple[str, ...]
    forbidden_invariants: Tuple[str, ...]
    authority_ref: str
    responsibility_ref: str
    preflight_checkable: bool
    postflight_checkable: bool
    description: str
    candidate_only: bool = True
    read_only: bool = True
    constitution_ref: str = CONSTITUTION_SOURCE_REF
    protocol_ref: str = PROTOCOL_SOURCE_REF
    architecture_ref: str = ARCHITECTURE_SOURCE_REF


@dataclass(frozen=True)
class GovernanceRuleRegistryV1:
    registry_ref: str
    registry_version: str
    owner_ref: str
    rules: Tuple[GovernanceRuleV1, ...]
    candidate_only: bool = True
    read_only: bool = True


@dataclass(frozen=True)
class GovernanceAuthorityResponsibilityRecordV1:
    module_ref: str
    owner_ref: str
    authority_refs: Tuple[str, ...]
    responsibility_refs: Tuple[str, ...]
    decision_types: Tuple[str, ...]
    failure_types: Tuple[str, ...]
    authority_responsibility_map: Tuple[Tuple[str, str], ...]
    responsibility_owner_refs: Tuple[Tuple[str, str], ...] = ()
    semantic_authority: bool = False
    operational_authority: bool = False
    admission_authority: bool = False
    mutation_authority: bool = False
    truth_authority: bool = False
    runtime_authority: bool = False
    candidate_only: bool = True


@dataclass(frozen=True)
class PhaseGovernanceProfileV1:
    phase_ref: str
    phase_owner_ref: str
    domains: Tuple[str, ...]
    owners_touched: Tuple[str, ...]
    governance_profiles: Tuple[str, ...]
    maturity_level: str
    runtime_level: str
    candidate_only: bool
    read_only: bool
    truth_authority: bool
    world_truth_authority: bool
    runtime_authority: bool
    authority_refs: Tuple[str, ...]
    responsibility_refs: Tuple[str, ...]
    input_contract_refs: Tuple[str, ...]
    output_contract_refs: Tuple[str, ...]
    protocol_refs: Tuple[str, ...]
    constitution_refs: Tuple[str, ...]
    context_refs: Tuple[str, ...] = ()
    trace_ref: str = ""
    # Controlled authoritative records may be created without starting a
    # runtime.  This is distinct from runtime invocation authority.
    mechanical_authority: bool = False


@dataclass(frozen=True)
class ApplicableGovernanceSetV1:
    phase_ref: str
    resolved_rule_refs: Tuple[str, ...]
    blocker_rule_refs: Tuple[str, ...]
    warning_rule_refs: Tuple[str, ...]
    resolution_basis_refs: Tuple[str, ...]
    resolution_status: str
    validation_errors: Tuple[str, ...] = ()


@dataclass(frozen=True)
class GovernancePreflightResultV1:
    phase_ref: str
    status: str
    applicable_governance: ApplicableGovernanceSetV1
    authority_responsibility_errors: Tuple[str, ...]
    profile_errors: Tuple[str, ...]
    protocol_errors: Tuple[str, ...]
    candidate_only: bool = True
    read_only: bool = True


@dataclass(frozen=True)
class ProtocolRuntimeComplianceResultV1:
    """Current Protocol Manager compliance prerequisite for runtime grant."""

    result_ref: str
    binding_key: Tuple[str, ...]
    protocol_refs: Tuple[str, ...]
    status: str
    reason: str
    policy_version_ref: str
    owner_ref: str = OWNER
    authoritative: bool = True
    candidate_only: bool = False
    read_only: bool = True


@dataclass(frozen=True)
class GovernancePostflightResultV1:
    phase_ref: str
    status: str
    blocker_refs: Tuple[str, ...]
    observations: Tuple[str, ...] = ()
    candidate_only: bool = True
    read_only: bool = True


def _rule(
    rule_ref: str,
    description: str,
    profiles: Tuple[str, ...],
    authority_ref: str,
    responsibility_ref: str,
    *,
    severity: str = BLOCKER,
    required: Tuple[str, ...] = (),
    forbidden: Tuple[str, ...] = (),
    contracts: Tuple[str, ...] = (),
) -> GovernanceRuleV1:
    return GovernanceRuleV1(
        rule_ref=rule_ref,
        rule_name=rule_ref,
        rule_owner_ref=OWNER,
        rule_source_ref=CONSTITUTION_SOURCE_REF,
        rule_version=VERSION,
        severity=severity,
        rule_domain="LUNA_GOVERNANCE_VERIFICATION",
        applies_to_domains=("CONTROLLED_PHASE",),
        applies_to_owners=(),
        applies_to_profiles=profiles,
        applies_to_contract_refs=contracts,
        trigger_refs=(f"trigger:{rule_ref.lower()}",),
        required_invariants=required,
        forbidden_invariants=forbidden,
        authority_ref=authority_ref,
        responsibility_ref=responsibility_ref,
        preflight_checkable=True,
        postflight_checkable=True,
        description=description,
    )


def build_core_governance_rule_registry_v1() -> GovernanceRuleRegistryV1:
    rules = (
        _rule(
            RULE_GOVERNED_EXECUTION,
            "A governed phase resolves at least one applicable rule or is canonically exempt.",
            ("GOVERNED_EXECUTION",),
            "authority:governance-scope",
            "responsibility:governance-scope-resolution",
            required=("applicable_rule_set_resolved",),
        ),
        _rule(
            AUTHORITY_RESPONSIBILITY_UNITY,
            "Every declared authority has a paired responsibility.",
            ("AUTHORITY_RESPONSIBILITY",),
            "authority:authority-responsibility-consistency",
            "responsibility:authority-responsibility-consistency",
            required=("authority_responsibility_pairs_complete",),
        ),
        _rule(
            NO_AUTHORITY_WITHOUT_RESPONSIBILITY,
            "Authority cannot be declared without responsibility.",
            ("AUTHORITY_RESPONSIBILITY",),
            "authority:authority-responsibility-consistency",
            "responsibility:authority-failure-responsibility",
        ),
        _rule(
            NO_RESPONSIBILITY_WITHOUT_AUTHORITY,
            "Responsibility cannot be declared without matching authority.",
            ("AUTHORITY_RESPONSIBILITY",),
            "authority:authority-responsibility-consistency",
            "responsibility:authority-responsibility-consistency",
        ),
        _rule(
            OWNER_BOUNDARY_REQUIRED,
            "Authoritative effects require an explicit owner.",
            ("GOVERNED_EXECUTION", "AUTHORITY_RESPONSIBILITY"),
            "authority:owner-boundary",
            "responsibility:owner-boundary",
        ),
        _rule(
            CANDIDATE_IS_NOT_AUTHORITY,
            "Candidate-only artifacts are not authoritative decisions.",
            ("CANDIDATE_ONLY",),
            "authority:candidate-boundary",
            "responsibility:candidate-boundary",
            required=("candidate_only",),
            forbidden=("authoritative_effect", "authoritative_decision"),
        ),
        _rule(
            NO_TRUTH_WITHOUT_TRUTH_AUTHORITY,
            "Without truth authority, truth and world truth must remain false.",
            ("NO_TRUTH",),
            "authority:truth-boundary",
            "responsibility:truth-boundary",
            forbidden=("truth_declared", "world_truth_declared"),
        ),
        _rule(
            NO_RUNTIME_WITHOUT_RUNTIME_AUTHORITY,
            "Planning/candidate phases cannot create runtime effects without runtime authority.",
            ("NO_RUNTIME",),
            "authority:runtime-boundary",
            "responsibility:runtime-boundary",
            forbidden=(
                "runtime_started",
                "execution_instance_created",
                "provider_session_started",
                "gateway_submission",
                "resource_allocated",
            ),
        ),
        _rule(
            REQUESTER_OWNS_REQUIREMENT_COMPLEXITY,
            "The requester owns semantic requirement complexity.",
            ("REQUESTER_EXECUTOR_BOUNDARY",),
            "authority:requirement-semantics",
            "responsibility:requirement-completeness",
            forbidden=("downstream_invents_requirement", "downstream_reinterprets_requirement"),
        ),
        _rule(
            EXECUTOR_OWNS_EXECUTION_COMPLEXITY,
            "Execution owners carry operational execution complexity.",
            ("REQUESTER_EXECUTOR_BOUNDARY",),
            "authority:execution-complexity",
            "responsibility:execution-complexity",
            forbidden=("requester_owns_resource_failure", "requester_owns_execution_failure"),
        ),
        _rule(
            FAILURE_RESPONSIBILITY_FOLLOWS_AUTHORITY,
            "Failure responsibility follows the authority for the failed decision.",
            ("AUTHORITY_RESPONSIBILITY",),
            "authority:failure-ownership",
            "responsibility:failure-ownership",
        ),
        _rule(
            ADAPTER_HAS_NO_SEMANTIC_AUTHORITY,
            "Adapters preserve shape and lineage but do not acquire semantic authority.",
            ("ADAPTER_BOUNDARY",),
            "authority:adapter-boundary",
            "responsibility:adapter-boundary",
            forbidden=("adapter_semantic_authority", "adapter_requirement_authority"),
        ),
    )
    return GovernanceRuleRegistryV1(
        registry_ref="governance-rule-registry:luna-core:v1",
        registry_version=VERSION,
        owner_ref=OWNER,
        rules=rules,
    )


CORE_GOVERNANCE_RULE_REGISTRY_V1 = build_core_governance_rule_registry_v1()


def _profile_errors(profile: object) -> Tuple[str, ...]:
    if not isinstance(profile, PhaseGovernanceProfileV1):
        return ("profile_type_invalid",)
    errors = []
    for field_name, value in (
        ("phase_ref", profile.phase_ref),
        ("phase_owner_ref", profile.phase_owner_ref),
        ("maturity_level", profile.maturity_level),
        ("runtime_level", profile.runtime_level),
        ("trace_ref", profile.trace_ref),
    ):
        if not value:
            errors.append(f"{field_name}_missing")
    if not profile.domains:
        errors.append("domains_missing")
    if not profile.owners_touched:
        errors.append("owners_touched_missing")
    if not profile.governance_profiles:
        errors.append("governance_profiles_missing")
    if not profile.input_contract_refs or not profile.output_contract_refs:
        errors.append("contract_refs_missing")
    if not profile.protocol_refs:
        errors.append("protocol_refs_missing")
    if not profile.constitution_refs:
        errors.append("constitution_refs_missing")
    # A governed phase may expose an authoritative *non-runtime* decision
    # (for example a pre-execution grant) without becoming a candidate-only
    # execution owner.  Candidate-only remains mandatory for planning and
    # projection profiles; an authoritative profile is valid only when it is
    # explicitly non-runtime and declares its authority boundary.
    if not profile.candidate_only and (
        profile.runtime_level != "NONE"
        or profile.runtime_authority
        or not profile.authority_refs
        or not profile.responsibility_refs
        or "CANDIDATE_ONLY" in profile.governance_profiles
    ):
        errors.append("profile_authoritative_boundary_invalid")
    if not profile.read_only:
        errors.append("profile_not_read_only")
    if profile.runtime_level != "NONE" and not profile.runtime_authority:
        errors.append("runtime_profile_authority_inconsistent")
    return tuple(dict.fromkeys(errors))


def _registry_errors(registry: object) -> Tuple[str, ...]:
    if not isinstance(registry, GovernanceRuleRegistryV1):
        return ("registry_type_invalid",)
    errors = []
    if not registry.registry_ref or not registry.registry_version or not registry.owner_ref:
        errors.append("registry_header_incomplete")
    refs = set()
    for rule in registry.rules:
        if not isinstance(rule, GovernanceRuleV1):
            errors.append("rule_type_invalid")
            continue
        if not rule.rule_ref or rule.rule_ref in refs:
            errors.append(f"rule_ref_invalid_or_duplicate:{rule.rule_ref}")
        refs.add(rule.rule_ref)
        if not rule.rule_owner_ref:
            errors.append(f"unknown_rule_owner:{rule.rule_ref}")
        if not rule.rule_source_ref or rule.rule_source_ref not in KNOWN_RULE_SOURCES:
            errors.append(f"unknown_rule_source:{rule.rule_ref}")
        if not rule.rule_version:
            errors.append(f"rule_version_missing:{rule.rule_ref}")
        if rule.severity not in {BLOCKER, WARNING}:
            errors.append(f"rule_severity_invalid:{rule.rule_ref}")
        if not rule.constitution_ref and not rule.protocol_ref and not rule.architecture_ref:
            errors.append(f"orphan_governance_rule:{rule.rule_ref}")
    return tuple(dict.fromkeys(errors))


def _rule_applies(rule: GovernanceRuleV1, profile: PhaseGovernanceProfileV1) -> bool:
    domain_match = not rule.applies_to_domains or bool(
        set(rule.applies_to_domains).intersection(profile.domains)
    )
    owner_match = not rule.applies_to_owners or bool(
        set(rule.applies_to_owners).intersection(profile.owners_touched)
    )
    profile_match = not rule.applies_to_profiles or bool(
        set(rule.applies_to_profiles).intersection(profile.governance_profiles)
    )
    contract_refs = set(profile.input_contract_refs).union(profile.output_contract_refs)
    contract_match = not rule.applies_to_contract_refs or bool(
        set(rule.applies_to_contract_refs).intersection(contract_refs)
    )
    # Trigger refs are optional matching evidence.  Core rules use profile
    # matches; a declared trigger only narrows a rule when the profile exposes
    # the same ref through a contract declaration.
    return domain_match and owner_match and profile_match and contract_match


def resolve_applicable_governance_set(
    profile: PhaseGovernanceProfileV1,
    registry: GovernanceRuleRegistryV1 = CORE_GOVERNANCE_RULE_REGISTRY_V1,
) -> ApplicableGovernanceSetV1:
    profile_errors = _profile_errors(profile)
    registry_errors = _registry_errors(registry)
    if profile_errors or registry_errors:
        return ApplicableGovernanceSetV1(
            phase_ref=getattr(profile, "phase_ref", ""),
            resolved_rule_refs=(),
            blocker_rule_refs=(),
            warning_rule_refs=(),
            resolution_basis_refs=(),
            resolution_status="INVALID_INPUT",
            validation_errors=tuple((*profile_errors, *registry_errors)),
        )
    resolved = tuple(rule for rule in registry.rules if _rule_applies(rule, profile))
    if not resolved:
        return ApplicableGovernanceSetV1(
            phase_ref=profile.phase_ref,
            resolved_rule_refs=(),
            blocker_rule_refs=(),
            warning_rule_refs=(),
            resolution_basis_refs=("exact:domain-owner-profile-contract",),
            resolution_status="GOVERNANCE_SCOPE_UNRESOLVED",
            validation_errors=("applicable_rule_count_zero",),
        )
    return ApplicableGovernanceSetV1(
        phase_ref=profile.phase_ref,
        resolved_rule_refs=tuple(rule.rule_ref for rule in resolved),
        blocker_rule_refs=tuple(rule.rule_ref for rule in resolved if rule.severity == BLOCKER),
        warning_rule_refs=tuple(rule.rule_ref for rule in resolved if rule.severity == WARNING),
        resolution_basis_refs=("exact:domain-owner-profile-contract",),
        resolution_status="RESOLVED",
    )


def validate_authority_responsibility_records(
    records: Tuple[GovernanceAuthorityResponsibilityRecordV1, ...],
) -> Tuple[str, ...]:
    errors = []
    authority_owners = {}
    for record in records:
        if not isinstance(record, GovernanceAuthorityResponsibilityRecordV1):
            errors.append("authority_record_type_invalid")
            continue
        if record.authority_refs and not record.owner_ref:
            errors.append(f"AUTHORITY_OWNER_MISSING:{record.module_ref}")
        responsibility_map = dict(record.authority_responsibility_map)
        responsibility_owners = dict(record.responsibility_owner_refs)
        for authority_ref in record.authority_refs:
            prior_owner = authority_owners.get(authority_ref)
            if prior_owner and prior_owner != record.owner_ref:
                errors.append(f"AUTHORITY_COLLISION:{authority_ref}")
            authority_owners[authority_ref] = record.owner_ref
            if not responsibility_map.get(authority_ref):
                errors.append(f"AUTHORITY_WITHOUT_RESPONSIBILITY:{authority_ref}")
        for responsibility_ref in record.responsibility_refs:
            if responsibility_ref not in responsibility_map.values():
                errors.append(f"RESPONSIBILITY_WITHOUT_AUTHORITY:{responsibility_ref}")
            mapped_owner = responsibility_owners.get(responsibility_ref)
            if mapped_owner and mapped_owner != record.owner_ref:
                errors.append(f"RESPONSIBILITY_OWNER_MISMATCH:{responsibility_ref}")
        for authority_ref, responsibility_ref in record.authority_responsibility_map:
            if authority_ref not in record.authority_refs:
                errors.append(f"AUTHORITY_MAP_SOURCE_MISSING:{authority_ref}")
            if responsibility_ref not in record.responsibility_refs:
                errors.append(f"RESPONSIBILITY_MAP_TARGET_MISSING:{responsibility_ref}")
    return tuple(dict.fromkeys(errors))


def run_governance_preflight(
    profile: PhaseGovernanceProfileV1,
    registry: GovernanceRuleRegistryV1,
    authority_records: Tuple[GovernanceAuthorityResponsibilityRecordV1, ...],
    resolvable_protocol_refs: Tuple[str, ...],
) -> GovernancePreflightResultV1:
    profile_errors = _profile_errors(profile)
    applicable = resolve_applicable_governance_set(profile, registry)
    authority_errors = validate_authority_responsibility_records(authority_records)
    profile_protocol_refs = (
        profile.protocol_refs
        if isinstance(profile, PhaseGovernanceProfileV1)
        else ()
    )
    protocol_errors = tuple(
        f"protocol_ref_unresolvable:{ref}"
        for ref in profile_protocol_refs
        if ref not in resolvable_protocol_refs
    )
    declared_authorities = set(getattr(profile, "authority_refs", ()))
    declared_responsibilities = set(getattr(profile, "responsibility_refs", ()))
    record_authorities = {
        ref
        for record in authority_records
        if isinstance(record, GovernanceAuthorityResponsibilityRecordV1)
        for ref in record.authority_refs
    }
    record_responsibilities = {
        ref
        for record in authority_records
        if isinstance(record, GovernanceAuthorityResponsibilityRecordV1)
        for ref in record.responsibility_refs
    }
    boundary_errors = tuple(
        f"profile_authority_ref_unresolved:{ref}"
        for ref in sorted(declared_authorities - record_authorities)
    ) + tuple(
        f"profile_responsibility_ref_unresolved:{ref}"
        for ref in sorted(declared_responsibilities - record_responsibilities)
    )
    errors = tuple(
        (*profile_errors, *applicable.validation_errors, *authority_errors, *protocol_errors, *boundary_errors)
    )
    if applicable.resolution_status != "RESOLVED":
        errors = tuple((*errors, "governance_scope_unresolved"))
    if errors:
        status = "GOVERNANCE_PREFLIGHT_BLOCKED"
    else:
        status = "PASS"
    return GovernancePreflightResultV1(
        phase_ref=getattr(profile, "phase_ref", ""),
        status=status,
        applicable_governance=applicable,
        authority_responsibility_errors=authority_errors,
        profile_errors=tuple(dict.fromkeys((*profile_errors, *applicable.validation_errors))),
        protocol_errors=protocol_errors,
        candidate_only=getattr(profile, "candidate_only", True),
        read_only=getattr(profile, "read_only", True),
    )


def run_governance_postflight(
    profile: PhaseGovernanceProfileV1,
    artifact: Mapping[str, Any],
) -> GovernancePostflightResultV1:
    blockers = []
    observations = []
    if profile.candidate_only and artifact.get("candidate_only") is not True:
        blockers.append("candidate_only_required")
    if profile.read_only and artifact.get("read_only") is not True:
        blockers.append("read_only_required")
    if not profile.truth_authority and artifact.get("truth_declared") is True:
        blockers.append("truth_declared_without_authority")
    if not profile.world_truth_authority and artifact.get("world_truth_declared") is True:
        blockers.append("world_truth_declared_without_authority")
    if not profile.runtime_authority:
        for field_name in RUNTIME_SIGNAL_FIELDS:
            if artifact.get(field_name) is True:
                blockers.append(f"runtime_effect_without_authority:{field_name}")
    if artifact.get("authoritative_effects"):
        blockers.append("candidate_authoritative_effect")
    if artifact.get("mutation_effects"):
        blockers.append("unexpected_mutation_effect")
    if artifact.get("failure_owner_ref") and not artifact.get("authority_ref"):
        blockers.append("failure_responsibility_without_authority")
    if artifact.get("warning_refs"):
        observations.extend(str(item) for item in artifact["warning_refs"])
    status = "GOVERNANCE_POSTFLIGHT_BLOCKED" if blockers else "PASS"
    return GovernancePostflightResultV1(
        phase_ref=profile.phase_ref,
        status=status,
        blocker_refs=tuple(dict.fromkeys(blockers)),
        observations=tuple(observations),
        candidate_only=profile.candidate_only,
        read_only=profile.read_only,
    )


def evaluate_runtime_protocol_compliance_v1(
    *,
    binding_key: Tuple[str, ...],
    protocol_refs: Tuple[str, ...],
) -> ProtocolRuntimeComplianceResultV1:
    """Evaluate current Protocol policy without trusting caller status fields."""

    policy_version_ref = "protocol-runtime-compliance:v1"
    valid_binding = (
        len(binding_key) == 7
        and binding_key[0] == "runtime-scope:v2"
        and all(binding_key)
    )
    valid_refs = isinstance(protocol_refs, tuple) and bool(protocol_refs)
    compliant = valid_binding and valid_refs
    digest = hashlib.sha256(
        "|".join((*binding_key, *protocol_refs, policy_version_ref)).encode("utf-8")
    ).hexdigest()[:24]
    return ProtocolRuntimeComplianceResultV1(
        result_ref=f"protocol-runtime-compliance:{digest}" if valid_binding else "",
        binding_key=tuple(binding_key),
        protocol_refs=tuple(protocol_refs),
        status="COMPLIANT" if compliant else "BLOCKED",
        reason="current_protocol_profile_compliant" if compliant else "protocol_scope_unresolved",
        policy_version_ref=policy_version_ref,
    )


def validate_adapter_boundary(adapter: Mapping[str, Any]) -> Tuple[str, ...]:
    errors = []
    if not adapter.get("source_refs") or not adapter.get("output_refs"):
        errors.append("adapter_lineage_refs_missing")
    if adapter.get("lineage_preserved") is not True:
        errors.append("adapter_lineage_not_preserved")
    if adapter.get("semantic_authority") is True or adapter.get("authority_refs"):
        errors.append("ADAPTER_HAS_SEMANTIC_AUTHORITY")
    return tuple(errors)


def validate_requester_executor_boundary(payload: Mapping[str, Any]) -> Tuple[str, ...]:
    errors = []
    if payload.get("downstream_invents_requirement") is True:
        errors.append("downstream_invents_requirement")
    if payload.get("downstream_reinterprets_requirement") is True:
        errors.append("downstream_reinterprets_requirement")
    if payload.get("requester_assigned_resource_failure") is True:
        errors.append("requester_assigned_resource_failure")
    if payload.get("requester_assigned_execution_failure") is True:
        errors.append("requester_assigned_execution_failure")
    if payload.get("requester_allocates_resources") is True:
        errors.append("requester_allocates_resources")
    if payload.get("authority_ref") and not payload.get("responsibility_ref"):
        errors.append("AUTHORITY_WITHOUT_RESPONSIBILITY")
    if payload.get("responsibility_ref") and not payload.get("authority_ref"):
        errors.append("RESPONSIBILITY_WITHOUT_AUTHORITY")
    return tuple(errors)


def validate_failure_ownership(payload: Mapping[str, Any]) -> Tuple[str, ...]:
    """Validate that a declared operational failure stays with its authority owner."""

    errors = []
    if payload.get("failure_owner_ref") and not payload.get("authority_ref"):
        errors.append("FAILURE_RESPONSIBILITY_WITHOUT_AUTHORITY")
    if payload.get("authority_ref") and not payload.get("responsibility_ref"):
        errors.append("AUTHORITY_WITHOUT_FAILURE_RESPONSIBILITY")
    authority_owner = payload.get("authority_owner_ref")
    failure_owner = payload.get("failure_owner_ref")
    if authority_owner and failure_owner and authority_owner != failure_owner:
        errors.append("FAILURE_RESPONSIBILITY_OWNER_MISMATCH")
    if payload.get("laundered_as_upstream") is True:
        errors.append("RESPONSIBILITY_LAUNDERING")
    return tuple(errors)


def validate_gateway_authority_boundary(payload: Mapping[str, Any]) -> Tuple[str, ...]:
    errors = []
    if payload.get("gateway_authority") != "RUNTIME_OBSERVATION_INGRESS_ADMISSION":
        errors.append("gateway_authority_must_be_runtime_ingress_admission")
    if payload.get("pre_execution_authorization") is True:
        errors.append("gateway_must_not_be_pre_execution_authority")
    return tuple(errors)


def compute_unified_final_decision(
    *,
    functional_checks_passed: bool,
    contract_failures: Tuple[str, ...],
    governance_preflight: str,
    governance_postflight: str,
    cognitive_logic_result: str,
    operational_result: str,
) -> str:
    if (
        functional_checks_passed
        and not contract_failures
        and governance_preflight == "PASS"
        and governance_postflight == "PASS"
        and cognitive_logic_result == "PASS"
        and operational_result == "PASS"
    ):
        return "GO"
    return "NO_GO"


__all__ = [
    "OWNER",
    "VERSION",
    "KNOWN_RULE_SOURCES",
    "RULE_GOVERNED_EXECUTION",
    "AUTHORITY_RESPONSIBILITY_UNITY",
    "NO_AUTHORITY_WITHOUT_RESPONSIBILITY",
    "NO_RESPONSIBILITY_WITHOUT_AUTHORITY",
    "OWNER_BOUNDARY_REQUIRED",
    "CANDIDATE_IS_NOT_AUTHORITY",
    "NO_TRUTH_WITHOUT_TRUTH_AUTHORITY",
    "NO_RUNTIME_WITHOUT_RUNTIME_AUTHORITY",
    "REQUESTER_OWNS_REQUIREMENT_COMPLEXITY",
    "EXECUTOR_OWNS_EXECUTION_COMPLEXITY",
    "FAILURE_RESPONSIBILITY_FOLLOWS_AUTHORITY",
    "ADAPTER_HAS_NO_SEMANTIC_AUTHORITY",
    "COMMON_GOVERNANCE_PROFILES",
    "GovernanceRuleV1",
    "GovernanceRuleRegistryV1",
    "GovernanceAuthorityResponsibilityRecordV1",
    "PhaseGovernanceProfileV1",
    "ApplicableGovernanceSetV1",
    "GovernancePreflightResultV1",
    "ProtocolRuntimeComplianceResultV1",
    "GovernancePostflightResultV1",
    "CORE_GOVERNANCE_RULE_REGISTRY_V1",
    "build_core_governance_rule_registry_v1",
    "resolve_applicable_governance_set",
    "validate_authority_responsibility_records",
    "run_governance_preflight",
    "run_governance_postflight",
    "evaluate_runtime_protocol_compliance_v1",
    "validate_adapter_boundary",
    "validate_requester_executor_boundary",
    "validate_failure_ownership",
    "validate_gateway_authority_boundary",
    "compute_unified_final_decision",
]
