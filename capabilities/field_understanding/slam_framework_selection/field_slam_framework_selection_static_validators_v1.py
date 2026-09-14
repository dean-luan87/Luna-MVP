# -*- coding: utf-8 -*-
"""Field SLAM Framework Selection — static validators v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence, Tuple

from capabilities.field_understanding.slam_framework_selection.field_slam_framework_selection_registry_v1 import (
    FORBIDDEN_SELECTION_POLICIES,
    GPL_LICENSE_TYPES,
    OBSERVATION_ONLY_FRAMEWORK_REFS,
    P0_EVIDENCE_FIT_LEVELS,
    is_registered,
    validate_registry,
)
from capabilities.field_understanding.slam_framework_selection.field_slam_framework_selection_types_v1 import (
    FINAL_DECISION_MATRIX_READY,
    SLAM_FRAMEWORK_CANDIDATE_FIELDS,
    SLAM_FRAMEWORK_EVALUATION_FIELDS,
    SLAM_FRAMEWORK_SELECTION_DECISION_FIELDS,
)

VALIDATOR_RULE_IDS: Tuple[str, ...] = (
    "rule_01_selection_candidate_only_required",
    "rule_02_framework_group_registered",
    "rule_03_license_type_registered",
    "rule_04_license_risk_registered",
    "rule_05_commercial_modification_risk_registered",
    "rule_06_recommended_priority_registered",
    "rule_07_primary_role_for_luna_required",
    "rule_08_technical_reference_candidate_explicit",
    "rule_09_commercial_runtime_candidate_explicit",
    "rule_10_gpl_not_commercial_runtime",
    "rule_11_grapheqa_observation_only",
    "rule_12_p0_technical_pose_or_motion_fit",
    "rule_13_p0_not_mapping_only_selection",
    "rule_14_decision_p0_technical_vs_commercial_safe",
    "rule_15_final_decision_matrix_ready",
)


def _missing_fields(data: Dict[str, Any], fields: Sequence[str]) -> List[str]:
    return [f"missing_{f}" for f in fields if f not in data]


def validate_selection_candidate_only(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    if data.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    return len(issues) == 0, issues


def validate_framework_candidate(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, SLAM_FRAMEWORK_CANDIDATE_FIELDS)
    ok, cand_issues = validate_selection_candidate_only(data)
    issues.extend(cand_issues)

    ok2, i2 = validate_framework_group_registered(data)
    ok3, i3 = validate_license_type_registered(data)
    ok4, i4 = validate_license_risk_registered(data)
    ok5, i5 = validate_commercial_modification_risk_registered(data)
    ok7, i7 = validate_primary_role_for_luna_required(data)
    ok8, i8 = validate_technical_reference_candidate_explicit(data)
    ok9, i9 = validate_commercial_runtime_candidate_explicit(data)
    ok10, i10 = validate_gpl_not_commercial_runtime(data)
    ok11, i11 = validate_grapheqa_observation_only(data)

    for ok_part, part_issues in (
        (ok2, i2),
        (ok3, i3),
        (ok4, i4),
        (ok5, i5),
        (ok7, i7),
        (ok8, i8),
        (ok9, i9),
        (ok10, i10),
        (ok11, i11),
    ):
        if not ok_part:
            issues.extend(part_issues)

    if data.get("runtime_priority") and not is_registered("priority_levels", data["runtime_priority"]):
        issues.append("runtime_priority_not_registered")
    if data.get("observation_priority") and not is_registered("priority_levels", data["observation_priority"]):
        issues.append("observation_priority_not_registered")
    if data.get("open_source_status") and not is_registered("open_source_status", data["open_source_status"]):
        issues.append("open_source_status_not_registered")

    return len(issues) == 0, issues


def validate_framework_evaluation(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, SLAM_FRAMEWORK_EVALUATION_FIELDS)
    ok, cand_issues = validate_selection_candidate_only(data)
    issues.extend(cand_issues)

    ok6, i6 = validate_recommended_priority_registered(data)
    if not ok6:
        issues.extend(i6)

    fit_fields = (
        "pose_candidate_fit",
        "motion_candidate_fit",
        "spatial_anchor_fit",
        "local_map_fit",
        "slam_health_fit",
        "map_drift_fit",
        "relocalization_fit",
        "field_synthesis_fit",
        "wearable_fit",
        "semantic_extension_fit",
        "static_dynamic_split_fit",
        "action_semantic_map_fit",
    )
    for field in fit_fields:
        val = data.get(field)
        if val and not is_registered("fit_levels", val):
            issues.append(f"{field}_not_registered")

    if data.get("runtime_weight") and not is_registered("runtime_weights", data["runtime_weight"]):
        issues.append("runtime_weight_not_registered")
    if data.get("engineering_risk") and not is_registered("engineering_risks", data["engineering_risk"]):
        issues.append("engineering_risk_not_registered")

    ok12, i12 = validate_p0_technical_pose_or_motion_fit(data)
    ok13, i13 = validate_p0_not_mapping_only_selection(data)
    if not ok12:
        issues.extend(i12)
    if not ok13:
        issues.extend(i13)

    return len(issues) == 0, issues


def validate_selection_decision(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, SLAM_FRAMEWORK_SELECTION_DECISION_FIELDS)
    ok, cand_issues = validate_selection_candidate_only(data)
    issues.extend(cand_issues)

    ok14, i14 = validate_decision_p0_technical_vs_commercial_safe(data)
    ok15, i15 = validate_final_decision_matrix_ready(data)
    if not ok14:
        issues.extend(i14)
    if not ok15:
        issues.extend(i15)

    if data.get("selection_policy") in FORBIDDEN_SELECTION_POLICIES:
        issues.append(f"forbidden_selection_policy:{data['selection_policy']}")

    return len(issues) == 0, issues


def validate_framework_group_registered(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    group = data.get("framework_group")
    if not group:
        return False, ["framework_group_required"]
    if not is_registered("framework_groups", group):
        return False, ["framework_group_not_registered"]
    return True, []


def validate_license_type_registered(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    lic = data.get("license_type")
    if not lic:
        return False, ["license_type_required"]
    if not is_registered("license_types", lic):
        return False, ["license_type_not_registered"]
    return True, []


def validate_license_risk_registered(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    risk = data.get("license_risk")
    if not risk:
        return False, ["license_risk_required"]
    if not is_registered("license_risks", risk):
        return False, ["license_risk_not_registered"]
    return True, []


def validate_commercial_modification_risk_registered(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    risk = data.get("commercial_modification_risk")
    if not risk:
        return False, ["commercial_modification_risk_required"]
    if not is_registered("commercial_modification_risks", risk):
        return False, ["commercial_modification_risk_not_registered"]
    return True, []


def validate_recommended_priority_registered(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    priority = data.get("recommended_priority")
    if not priority:
        return False, ["recommended_priority_required"]
    if not is_registered("priority_levels", priority):
        return False, ["recommended_priority_not_registered"]
    return True, []


def validate_primary_role_for_luna_required(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if not data.get("primary_role_for_luna"):
        return False, ["primary_role_for_luna_required"]
    return True, []


def validate_technical_reference_candidate_explicit(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("technical_reference_candidate") is not True:
        return False, ["technical_reference_candidate_must_be_true_for_matrix_v1"]
    return True, []


def validate_commercial_runtime_candidate_explicit(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("commercial_runtime_candidate") is not False:
        return False, ["commercial_runtime_candidate_must_be_false_for_matrix_v1"]
    return True, []


def validate_gpl_not_commercial_runtime(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("license_type") in GPL_LICENSE_TYPES and data.get("commercial_runtime_candidate") is True:
        return False, ["gpl_framework_cannot_be_commercial_runtime_candidate"]
    return True, []


def validate_grapheqa_observation_only(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    ref = data.get("framework_ref")
    if ref != "grapheqa":
        return True, []
    issues: List[str] = []
    if data.get("runtime_priority") != "observation":
        issues.append("grapheqa_runtime_priority_must_be_observation")
    if data.get("recommended_priority") == "p0":
        issues.append("grapheqa_cannot_be_p0_runtime")
    return len(issues) == 0, issues


def validate_p0_technical_pose_or_motion_fit(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("recommended_priority") != "p0":
        return True, []
    pose = data.get("pose_candidate_fit")
    motion = data.get("motion_candidate_fit")
    if pose in P0_EVIDENCE_FIT_LEVELS or motion in P0_EVIDENCE_FIT_LEVELS:
        return True, []
    return False, ["p0_technical_requires_pose_or_motion_high_or_medium_fit"]


def validate_p0_not_mapping_only_selection(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("recommended_priority") != "p0":
        return True, []
    pose = data.get("pose_candidate_fit")
    motion = data.get("motion_candidate_fit")
    local_map = data.get("local_map_fit")
    if local_map in P0_EVIDENCE_FIT_LEVELS and pose not in P0_EVIDENCE_FIT_LEVELS and motion not in P0_EVIDENCE_FIT_LEVELS:
        return False, ["p0_cannot_be_selected_by_local_map_only"]
    return True, []


def validate_decision_p0_technical_vs_commercial_safe(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    p0_tech = data.get("recommended_p0_technical") or ()
    p0_safe = data.get("recommended_p0_commercial_safe") or ()
    if not isinstance(p0_tech, (list, tuple)):
        issues.append("recommended_p0_technical_must_be_sequence")
    if not isinstance(p0_safe, (list, tuple)):
        issues.append("recommended_p0_commercial_safe_must_be_sequence")
    if p0_tech and p0_safe and set(p0_tech) & set(p0_safe):
        issues.append("p0_technical_and_commercial_safe_must_not_overlap")
    if not data.get("license_gate_required"):
        issues.append("license_gate_required_must_be_true")
    if not data.get("adapter_contract_required"):
        issues.append("adapter_contract_required_must_be_true")
    return len(issues) == 0, issues


def validate_final_decision_matrix_ready(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("final_decision") != FINAL_DECISION_MATRIX_READY:
        return False, [f"final_decision_must_be_{FINAL_DECISION_MATRIX_READY}"]
    return True, []


def validate_framework_selection_matrix_v1(
    matrix: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, List[str]]:
    if matrix is None:
        from capabilities.field_understanding.slam_framework_selection.field_slam_framework_selection_matrix_v1 import (
            build_framework_selection_matrix_v1,
        )

        matrix = build_framework_selection_matrix_v1()

    issues: List[str] = []
    registry_ok, registry_issues = validate_registry()
    if not registry_ok:
        issues.extend(registry_issues)

    frameworks = matrix.get("frameworks") or []
    evaluations = matrix.get("evaluations") or []
    decision = matrix.get("decision") or {}

    framework_refs = {f.get("framework_ref") for f in frameworks}
    for idx, fw in enumerate(frameworks):
        ok, fw_issues = validate_framework_candidate(fw)
        if not ok:
            issues.extend([f"framework_{idx}:{i}" for i in fw_issues])

    for idx, ev in enumerate(evaluations):
        ok, ev_issues = validate_framework_evaluation(ev)
        if not ok:
            issues.extend([f"evaluation_{idx}:{i}" for i in ev_issues])
        if ev.get("framework_ref") not in framework_refs:
            issues.append(f"evaluation_{idx}:framework_ref_not_in_frameworks")

    ok_dec, dec_issues = validate_selection_decision(decision)
    if not ok_dec:
        issues.extend([f"decision:{i}" for i in dec_issues])

    all_decision_refs = set(
        list(decision.get("recommended_p0_technical") or ())
        + list(decision.get("recommended_p0_commercial_safe") or ())
        + list(decision.get("recommended_p1") or ())
        + list(decision.get("recommended_p2") or ())
        + list(decision.get("recommended_observation") or ())
        + list(decision.get("deferred") or ())
        + list(decision.get("blocked") or ())
    )
    for ref in all_decision_refs:
        if ref and ref not in framework_refs:
            issues.append(f"decision_references_unknown_framework:{ref}")

    for ref in OBSERVATION_ONLY_FRAMEWORK_REFS:
        if ref in (decision.get("recommended_p0_technical") or ()):
            issues.append(f"observation_framework_in_p0_technical:{ref}")
        if ref in (decision.get("recommended_p0_commercial_safe") or ()):
            issues.append(f"observation_framework_in_p0_commercial_safe:{ref}")

    if len(frameworks) != 7:
        issues.append(f"framework_count_expected_7_actual_{len(frameworks)}")
    if len(evaluations) != 7:
        issues.append(f"evaluation_count_expected_7_actual_{len(evaluations)}")

    return len(issues) == 0, issues
