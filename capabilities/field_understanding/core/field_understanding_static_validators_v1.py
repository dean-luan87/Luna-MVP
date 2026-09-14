# -*- coding: utf-8 -*-
"""Field-Oriented Egocentric Action Understanding — static validators v1."""

from __future__ import annotations

import re
from typing import Any, Dict, List, Sequence, Tuple

from capabilities.field_understanding.core.field_understanding_registry_v1 import (
    ACTION_READINESS,
    AFFECTED_TARGETS,
    ALIGNMENT_CONFLICT_STATUSES,
    ALIGNMENT_STATUSES,
    DISTANCE_BANDS,
    DISTANCE_METHODS,
    DYNAMIC_TYPES,
    FACT_INFLUENCE_LEVELS,
    FIELD_DIMENSIONS,
    FIELD_REVISION_POLICIES,
    FIELD_TYPES,
    FACT_DERIVED_FIELD_IDENTITY_KEYS,
    HIGH_RISK_DISTANCE_BANDS,
    INFLUENCE_SCOPES,
    INFLUENCE_TYPES,
    MAP_FRESHNESS,
    MAP_SOURCES,
    MAP_TYPES,
    POSITION_BANDS,
    PROHIBITED_FIELD_REVISION_POLICIES,
    PROHIBITED_FIELD_TYPES_FROM_ISOLATED_FACT,
    RISK_LEVELS,
    SEMANTIC_ROLES,
    SPEECH_DISTANCE_OUTPUT_FORBIDDEN_PATTERNS,
    STATIC_OBJECT_CLASSES,
    is_registered,
)
from capabilities.field_understanding.core.field_understanding_types_v1 import (
    ACTION_DISTANCE_CANDIDATE_FIELDS,
    DYNAMIC_FIELD_STATE_CANDIDATE_FIELDS,
    EGOCENTRIC_MAP_ALIGNMENT_CANDIDATE_FIELDS,
    EXTERNAL_MAP_CANDIDATE_FIELDS,
    FIELD_CANDIDATE_FIELDS,
    FIELD_INFLUENCE_CANDIDATE_FIELDS,
    SEMANTIC_FIELD_OBJECT_CANDIDATE_FIELDS,
    SPATIAL_FUSION_CANDIDATE_FIELDS,
    STATIC_FIELD_STRUCTURE_CANDIDATE_FIELDS,
    candidate_to_dict,
)

VALIDATOR_RULE_IDS: Tuple[str, ...] = (
    "rule_01_candidate_only_required",
    "rule_02_dynamic_ttl_required",
    "rule_03_dynamic_not_in_static",
    "rule_04_map_not_fact_layer",
    "rule_05_alignment_anchor_required",
    "rule_06_distance_band_required",
    "rule_07_high_risk_distance_source_refs",
    "rule_08_semantic_tag_fields_present",
    "rule_09_influence_affected_target",
    "rule_10_fusion_conflict_readiness",
    "rule_11_confidence_range",
    "rule_12_static_stability_observed",
    "rule_13_dynamic_risk_level",
    "rule_14_alignment_conflict_downgrade",
    "rule_15_speech_no_precise_distance",
    "rule_16_fact_must_not_directly_override_field",
    "rule_17_critical_fact_influence_requires_influence_path",
    "rule_18_user_request_must_not_skip_field_synthesis",
    "rule_19_fact_field_conflict_must_be_recorded",
    "rule_20_field_revision_policy_governed_only",
    "rule_21_field_context_before_fact_action",
    "rule_22_facts_affect_dimensions_not_identity",
)

FACT_OVERRIDE_FIELD_KEYS: Tuple[str, ...] = (
    "fact_overrides_field",
    "field_override_from_fact",
    "direct_fact_to_action",
    "override_field",
    "replace_field",
)


def _missing_fields(data: Dict[str, Any], fields: Sequence[str]) -> List[str]:
    return [f"missing_{f}" for f in fields if f not in data]


def _confidence_ok(value: Any) -> bool:
    return isinstance(value, (int, float)) and 0.0 <= float(value) <= 1.0


def validate_candidate_only(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    if data.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    if data.get("is_fact") is True:
        issues.append("is_fact_not_allowed")
    if data.get("fact_layer_admitted") is True:
        issues.append("fact_layer_admission_not_allowed")
    return len(issues) == 0, issues


def validate_field_candidate(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, FIELD_CANDIDATE_FIELDS)
    ok, cand_issues = validate_candidate_only(data)
    issues.extend(cand_issues)
    if not _confidence_ok(data.get("field_confidence")):
        issues.append("field_confidence_out_of_range")
    if data.get("field_type") and not is_registered("field_types", data["field_type"]):
        issues.append("field_type_not_registered")
    return len(issues) == 0, issues


def validate_static_field_structure_candidate(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, STATIC_FIELD_STRUCTURE_CANDIDATE_FIELDS)
    ok, cand_issues = validate_candidate_only(data)
    issues.extend(cand_issues)
    if data.get("object_class") and not is_registered("static_object_classes", data["object_class"]):
        issues.append("object_class_not_registered")
    if data.get("position_band") and not is_registered("position_bands", data["position_band"]):
        issues.append("position_band_not_registered")
    ok12, issues12 = validate_static_stability_observed(data)
    if not ok12:
        issues.extend(issues12)
    return len(issues) == 0, issues


def validate_dynamic_field_state_candidate(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, DYNAMIC_FIELD_STATE_CANDIDATE_FIELDS)
    ok, cand_issues = validate_candidate_only(data)
    issues.extend(cand_issues)
    ttl = data.get("ttl_ms")
    if not isinstance(ttl, int) or ttl <= 0:
        issues.append("ttl_ms_required_positive")
    if data.get("dynamic_type") and not is_registered("dynamic_types", data["dynamic_type"]):
        issues.append("dynamic_type_not_registered")
    ok13, issues13 = validate_dynamic_risk_level(data)
    if not ok13:
        issues.extend(issues13)
    tracker = data.get("tracker_ref")
    if tracker is None and data.get("current_state") not in ("unknown", "temporary_obstacle"):
        issues.append("tracker_ref_or_untrackable_state_required")
    return len(issues) == 0, issues


def validate_semantic_field_object_candidate(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, SEMANTIC_FIELD_OBJECT_CANDIDATE_FIELDS)
    ok, cand_issues = validate_candidate_only(data)
    issues.extend(cand_issues)
    if not _confidence_ok(data.get("confidence")):
        issues.append("confidence_out_of_range")
    ok8, issues8 = validate_semantic_tag_fields_present(data)
    if not ok8:
        issues.extend(issues8)
    for role in data.get("semantic_roles") or ():
        if not is_registered("semantic_roles", role):
            issues.append(f"semantic_role_not_registered:{role}")
    return len(issues) == 0, issues


def validate_field_influence_candidate(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, FIELD_INFLUENCE_CANDIDATE_FIELDS)
    ok, cand_issues = validate_candidate_only(data)
    issues.extend(cand_issues)
    if not _confidence_ok(data.get("confidence")):
        issues.append("confidence_out_of_range")
    ok9, issues9 = validate_influence_affected_target(data)
    if not ok9:
        issues.extend(issues9)
    if data.get("influence_type") and not is_registered("influence_types", data["influence_type"]):
        issues.append("influence_type_not_registered")
    if data.get("risk_level") and not is_registered("risk_levels", data["risk_level"]):
        issues.append("risk_level_not_registered")
    scope = data.get("influence_scope")
    if scope and not is_registered("influence_scopes", scope):
        issues.append("influence_scope_not_registered")
    dim = data.get("affected_field_dimension")
    if data.get("fact_ref") and not dim:
        issues.append("affected_field_dimension_required_when_fact_ref_present")
    elif dim and not is_registered("field_dimensions", dim):
        issues.append("affected_field_dimension_not_registered")
    return len(issues) == 0, issues


def validate_action_distance_candidate(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, ACTION_DISTANCE_CANDIDATE_FIELDS)
    ok, cand_issues = validate_candidate_only(data)
    issues.extend(cand_issues)
    ok6, issues6 = validate_distance_band_required(data)
    if not ok6:
        issues.extend(issues6)
    if not _confidence_ok(data.get("confidence")):
        issues.append("confidence_out_of_range")
    if data.get("method") and not is_registered("distance_methods", data["method"]):
        issues.append("distance_method_not_registered")
    ok7, issues7 = validate_high_risk_distance_source_refs(data)
    if not ok7:
        issues.extend(issues7)
    return len(issues) == 0, issues


def validate_external_map_candidate(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, EXTERNAL_MAP_CANDIDATE_FIELDS)
    ok, cand_issues = validate_candidate_only(data)
    issues.extend(cand_issues)
    ok4, issues4 = validate_map_not_fact_layer(data)
    if not ok4:
        issues.extend(issues4)
    if not _confidence_ok(data.get("confidence")):
        issues.append("confidence_out_of_range")
    if data.get("map_source") and not is_registered("map_sources", data["map_source"]):
        issues.append("map_source_not_registered")
    if data.get("map_type") and not is_registered("map_types", data["map_type"]):
        issues.append("map_type_not_registered")
    if data.get("freshness") and not is_registered("map_freshness", data["freshness"]):
        issues.append("map_freshness_not_registered")
    return len(issues) == 0, issues


def validate_egocentric_map_alignment_candidate(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, EGOCENTRIC_MAP_ALIGNMENT_CANDIDATE_FIELDS)
    ok, cand_issues = validate_candidate_only(data)
    issues.extend(cand_issues)
    if not _confidence_ok(data.get("confidence")):
        issues.append("confidence_out_of_range")
    ok5, issues5 = validate_alignment_anchor_required(data)
    if not ok5:
        issues.extend(issues5)
    ok14, issues14 = validate_alignment_conflict_downgrade(data)
    if not ok14:
        issues.extend(issues14)
    if data.get("alignment_status") and not is_registered("alignment_statuses", data["alignment_status"]):
        issues.append("alignment_status_not_registered")
    return len(issues) == 0, issues


def validate_spatial_fusion_candidate(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, SPATIAL_FUSION_CANDIDATE_FIELDS)
    ok, cand_issues = validate_candidate_only(data)
    issues.extend(cand_issues)
    if not _confidence_ok(data.get("confidence")):
        issues.append("confidence_out_of_range")
    ok10, issues10 = validate_fusion_conflict_readiness(data)
    if not ok10:
        issues.extend(issues10)
    if data.get("action_readiness") and not is_registered("action_readiness", data["action_readiness"]):
        issues.append("action_readiness_not_registered")
    level = data.get("fact_influence_level")
    if level and not is_registered("fact_influence_levels", level):
        issues.append("fact_influence_level_not_registered")
    policy = data.get("field_revision_policy")
    if policy and not is_registered("field_revision_policies", policy):
        issues.append("field_revision_policy_not_registered")
    ok20, issues20 = validate_field_revision_policy_governed_only(data)
    if not ok20:
        issues.extend(issues20)
    return len(issues) == 0, issues


def validate_dynamic_not_in_static(
    static_candidates: Sequence[Dict[str, Any]],
    dynamic_candidates: Sequence[Dict[str, Any]],
) -> Tuple[bool, List[str]]:
    static_refs = {s.get("structure_ref") for s in static_candidates}
    static_objects = {s.get("object_class") for s in static_candidates}
    issues: List[str] = []
    for dyn in dynamic_candidates:
        if dyn.get("object_ref") in static_refs:
            issues.append(f"dynamic_object_ref_in_static:{dyn.get('object_ref')}")
        if dyn.get("dynamic_type") in static_objects:
            issues.append(f"dynamic_type_as_static_class:{dyn.get('dynamic_type')}")
    return len(issues) == 0, issues


def validate_map_not_fact_layer(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    if data.get("is_fact") is True:
        issues.append("external_map_is_fact_not_allowed")
    if data.get("fact_layer_admitted") is True:
        issues.append("external_map_fact_layer_admission_not_allowed")
    if data.get("verified_as_truth") is True:
        issues.append("external_map_verified_as_truth_not_allowed")
    return len(issues) == 0, issues


def validate_alignment_anchor_required(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("alignment_status") != "aligned":
        return True, []
    visual = data.get("visual_anchor_refs") or ()
    ocr = data.get("ocr_anchor_refs") or ()
    if not visual and not ocr:
        return False, ["aligned_requires_visual_or_ocr_anchor_refs"]
    return True, []


def validate_distance_band_required(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    band = data.get("distance_band")
    if not band:
        issues.append("distance_band_required")
    elif not is_registered("distance_bands", band):
        issues.append("distance_band_not_registered")
    if data.get("estimated_distance_m") is not None and not band:
        issues.append("estimated_distance_m_without_distance_band")
    return len(issues) == 0, issues


def validate_high_risk_distance_source_refs(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    band = data.get("distance_band")
    if band not in HIGH_RISK_DISTANCE_BANDS:
        return True, []
    refs = data.get("source_refs") or ()
    if not refs:
        return False, ["high_risk_distance_band_requires_source_refs"]
    return True, []


def validate_semantic_tag_fields_present(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    for key in ("risk_tags", "attention_tags", "destination_tags", "memory_tags"):
        if key not in data:
            issues.append(f"missing_{key}")
        elif not isinstance(data.get(key), (list, tuple)):
            issues.append(f"{key}_must_be_sequence")
    return len(issues) == 0, issues


def validate_influence_affected_target(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    target = data.get("affected_target")
    if not target:
        return False, ["affected_target_required"]
    if not is_registered("affected_targets", target):
        return False, ["affected_target_not_registered"]
    return True, []


def validate_fusion_conflict_readiness(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    conflicts = data.get("conflict_refs") or ()
    readiness = data.get("action_readiness")
    if conflicts and readiness == "ready_for_action_decision":
        return False, ["conflict_refs_present_action_readiness_must_not_be_ready"]
    return True, []


def validate_confidence_range(data: Dict[str, Any], field_name: str = "confidence") -> Tuple[bool, List[str]]:
    if not _confidence_ok(data.get(field_name)):
        return False, [f"{field_name}_out_of_range"]
    return True, []


def validate_static_stability_observed(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    score = data.get("stability_score")
    count = data.get("observed_count")
    if not isinstance(score, (int, float)) or not 0.0 <= float(score) <= 1.0:
        issues.append("stability_score_out_of_range")
    if not isinstance(count, int) or count < 0:
        issues.append("observed_count_invalid")
    return len(issues) == 0, issues


def validate_dynamic_risk_level(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    risk = data.get("risk_level")
    if not risk:
        return False, ["risk_level_required"]
    if not is_registered("risk_levels", risk):
        return False, ["risk_level_not_registered"]
    return True, []


def validate_alignment_conflict_downgrade(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    status = data.get("alignment_status")
    confidence = data.get("confidence")
    if status in ALIGNMENT_CONFLICT_STATUSES and isinstance(confidence, (int, float)) and confidence > 0.85:
        return False, ["alignment_conflict_requires_downgraded_confidence"]
    return True, []


def validate_speech_no_precise_distance(text: str) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    for pattern in SPEECH_DISTANCE_OUTPUT_FORBIDDEN_PATTERNS:
        if re.search(pattern, text, flags=re.IGNORECASE):
            issues.append(f"speech_precise_distance_forbidden:{pattern}")
    return len(issues) == 0, issues


def validate_fact_must_not_directly_override_field(
    field: Dict[str, Any],
    fusion: Dict[str, Any],
) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    for key in FACT_OVERRIDE_FIELD_KEYS:
        if field.get(key) is True:
            issues.append(f"field_direct_override_flag_not_allowed:{key}")
        if fusion.get(key) is True:
            issues.append(f"fusion_direct_override_flag_not_allowed:{key}")
    policy = fusion.get("field_revision_policy")
    if policy in PROHIBITED_FIELD_REVISION_POLICIES:
        issues.append(f"field_revision_policy_prohibited:{policy}")
    return len(issues) == 0, issues


def validate_field_revision_policy_governed_only(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    policy = data.get("field_revision_policy")
    if policy in PROHIBITED_FIELD_REVISION_POLICIES:
        return False, [f"field_revision_policy_prohibited:{policy}"]
    return True, []


def validate_critical_fact_influence_requires_influence_path(
    fusion: Dict[str, Any],
    influences: Sequence[Dict[str, Any]],
) -> Tuple[bool, List[str]]:
    if fusion.get("fact_influence_level") != "critical":
        return True, []
    refs = fusion.get("fact_influence_refs") or ()
    influence_fact_refs = [i.get("fact_ref") for i in influences if i.get("fact_ref")]
    if not refs and not influence_fact_refs:
        return False, ["critical_fact_influence_requires_fact_influence_refs_or_influence_fact_ref"]
    return True, []


def validate_user_request_must_not_skip_field_synthesis(
    fusion: Dict[str, Any],
    semantic_objects: Sequence[Dict[str, Any]],
) -> Tuple[bool, List[str]]:
    user_requested = any(
        "user_requested" in (s.get("attention_tags") or ())
        for s in semantic_objects
    )
    if not user_requested:
        return True, []
    policy = fusion.get("field_revision_policy")
    if policy in PROHIBITED_FIELD_REVISION_POLICIES:
        return False, ["user_requested_fact_must_not_skip_field_synthesis"]
    if policy == "no_revision" and fusion.get("fact_influence_level") in ("strong", "critical"):
        return False, ["user_requested_strong_fact_requires_governed_revision_policy"]
    return True, []


def validate_fact_field_conflict_must_be_recorded(
    fusion: Dict[str, Any],
    *,
    semantic_objects: Sequence[Dict[str, Any]] = (),
    external_maps: Sequence[Dict[str, Any]] = (),
    alignments: Sequence[Dict[str, Any]] = (),
) -> Tuple[bool, List[str]]:
    conflicts = fusion.get("conflict_refs") or ()
    fact_refs = fusion.get("fact_influence_refs") or ()
    has_map_unconfirmed = any(
        a.get("alignment_status") in ("not_observed", "conflicted")
        for a in alignments
    )
    has_exit_semantic = any(
        "exit" in (s.get("object_class") or "").lower()
        or "exit_candidate" in (s.get("destination_tags") or ())
        for s in semantic_objects
    )
    potential_conflict = has_map_unconfirmed or (
        has_exit_semantic and fusion.get("action_readiness") == "needs_more_observation"
    )
    if potential_conflict and not conflicts and not fact_refs:
        return False, ["fact_field_conflict_requires_conflict_refs_or_fact_influence_refs"]
    return True, []


def validate_field_context_before_fact_action(
    field: Dict[str, Any],
    fusion: Dict[str, Any],
    influences: Sequence[Dict[str, Any]],
) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    fact_influence_active = (
        fusion.get("fact_influence_level") not in (None, "none")
        or bool(fusion.get("fact_influence_refs"))
        or any(i.get("fact_ref") for i in influences)
    )
    action_uses_facts = fusion.get("action_readiness") in (
        "ready_for_action_decision",
        "needs_more_observation",
    )
    if not fact_influence_active and not action_uses_facts:
        return True, []

    if not field.get("field_ref"):
        issues.append("field_context_unresolved_missing_field_ref")
    if field.get("field_type") in (None, "unknown"):
        issues.append("field_context_unresolved_before_fact_action")
    if fusion.get("field_ref") and field.get("field_ref") and fusion.get("field_ref") != field.get("field_ref"):
        issues.append("field_context_fusion_field_ref_mismatch")
    if fact_influence_active and float(field.get("field_confidence") or 0) <= 0:
        issues.append("field_context_confidence_required_before_fact_influence")
    return len(issues) == 0, issues


def validate_facts_affect_dimensions_not_identity(
    field: Dict[str, Any],
    fusion: Dict[str, Any],
    influences: Sequence[Dict[str, Any]],
    semantic_objects: Sequence[Dict[str, Any]] = (),
) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    for key in FACT_DERIVED_FIELD_IDENTITY_KEYS:
        if field.get(key):
            issues.append(f"field_identity_change_from_fact_not_allowed:{key}")
        if fusion.get(key):
            issues.append(f"fusion_field_identity_change_from_fact_not_allowed:{key}")

    field_type = field.get("field_type")
    if field_type in PROHIBITED_FIELD_TYPES_FROM_ISOLATED_FACT:
        issues.append("field_type_must_not_be_isolated_fact_identity")

    for idx, influence in enumerate(influences):
        if influence.get("fact_ref") and not influence.get("affected_field_dimension"):
            issues.append(f"influence_{idx}:affected_field_dimension_required_for_fact_influence")

    fact_object_classes = {
        str(s.get("object_class") or "").lower()
        for s in semantic_objects
        if s.get("object_ref") in (fusion.get("fact_influence_refs") or ())
        or any(
            s.get("object_ref") == i.get("fact_ref")
            for i in influences
            if i.get("fact_ref")
        )
    }
    if field_type and field_type.lower() in fact_object_classes:
        issues.append("field_type_must_not_equal_isolated_fact_object_class")

    return len(issues) == 0, issues


def validate_field_information_priority_governance(
    *,
    field: Dict[str, Any],
    fusion: Dict[str, Any],
    influences: Sequence[Dict[str, Any]] = (),
    semantic_objects: Sequence[Dict[str, Any]] = (),
    external_maps: Sequence[Dict[str, Any]] = (),
    alignments: Sequence[Dict[str, Any]] = (),
) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    checks = (
        validate_fact_must_not_directly_override_field(field, fusion),
        validate_critical_fact_influence_requires_influence_path(fusion, influences),
        validate_user_request_must_not_skip_field_synthesis(fusion, semantic_objects),
        validate_fact_field_conflict_must_be_recorded(
            fusion,
            semantic_objects=semantic_objects,
            external_maps=external_maps,
            alignments=alignments,
        ),
        validate_field_context_before_fact_action(field, fusion, influences),
        validate_facts_affect_dimensions_not_identity(
            field, fusion, influences, semantic_objects=semantic_objects
        ),
    )
    for ok, item_issues in checks:
        if not ok:
            issues.extend(item_issues)
    return len(issues) == 0, issues


def validate_core_bundle(
    *,
    field: Dict[str, Any],
    static_structures: Sequence[Dict[str, Any]] = (),
    dynamic_states: Sequence[Dict[str, Any]] = (),
    semantic_objects: Sequence[Dict[str, Any]] = (),
    influences: Sequence[Dict[str, Any]] = (),
    distances: Sequence[Dict[str, Any]] = (),
    external_maps: Sequence[Dict[str, Any]] = (),
    alignments: Sequence[Dict[str, Any]] = (),
    fusions: Sequence[Dict[str, Any]] = (),
) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    validators = [
        ("field", validate_field_candidate(field)),
    ]
    for idx, item in enumerate(static_structures):
        validators.append((f"static_{idx}", validate_static_field_structure_candidate(item)))
    for idx, item in enumerate(dynamic_states):
        validators.append((f"dynamic_{idx}", validate_dynamic_field_state_candidate(item)))
    for idx, item in enumerate(semantic_objects):
        validators.append((f"semantic_{idx}", validate_semantic_field_object_candidate(item)))
    for idx, item in enumerate(influences):
        validators.append((f"influence_{idx}", validate_field_influence_candidate(item)))
    for idx, item in enumerate(distances):
        validators.append((f"distance_{idx}", validate_action_distance_candidate(item)))
    for idx, item in enumerate(external_maps):
        validators.append((f"map_{idx}", validate_external_map_candidate(item)))
    for idx, item in enumerate(alignments):
        validators.append((f"alignment_{idx}", validate_egocentric_map_alignment_candidate(item)))
    for idx, item in enumerate(fusions):
        validators.append((f"fusion_{idx}", validate_spatial_fusion_candidate(item)))

    ok3, issues3 = validate_dynamic_not_in_static(static_structures, dynamic_states)
    if not ok3:
        issues.extend(issues3)

    if fusions:
        primary_fusion = fusions[0]
        ok_gov, gov_issues = validate_field_information_priority_governance(
            field=field,
            fusion=primary_fusion,
            influences=influences,
            semantic_objects=semantic_objects,
            external_maps=external_maps,
            alignments=alignments,
        )
        if not ok_gov:
            issues.extend([f"governance:{i}" for i in gov_issues])

    for label, (ok, item_issues) in validators:
        if not ok:
            issues.extend([f"{label}:{i}" for i in item_issues])
    return len(issues) == 0, issues


def validate_dataclass_instance(obj: Any) -> Tuple[bool, List[str]]:
    data = candidate_to_dict(obj)
    dispatch = {
        "FieldCandidate": validate_field_candidate,
        "StaticFieldStructureCandidate": validate_static_field_structure_candidate,
        "DynamicFieldStateCandidate": validate_dynamic_field_state_candidate,
        "SemanticFieldObjectCandidate": validate_semantic_field_object_candidate,
        "FieldInfluenceCandidate": validate_field_influence_candidate,
        "ActionDistanceCandidate": validate_action_distance_candidate,
        "ExternalMapCandidate": validate_external_map_candidate,
        "EgocentricMapAlignmentCandidate": validate_egocentric_map_alignment_candidate,
        "SpatialFusionCandidate": validate_spatial_fusion_candidate,
    }
    fn = dispatch.get(type(obj).__name__)
    if fn is None:
        return False, ["unknown_candidate_type"]
    return fn(data)
