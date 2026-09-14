# -*- coding: utf-8 -*-
"""SLAM Spatial Evidence Adapter Skeleton — static validators v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.slam_spatial_evidence_adapter.slam_spatial_evidence_adapter_registry_v1 import (
    FORBIDDEN_ADAPTER_POLICIES,
    build_slam_spatial_evidence_adapter_matrix_v1,
    is_registered,
    validate_registry,
)
from capabilities.field_understanding.slam_spatial_evidence_adapter.slam_spatial_evidence_adapter_types_v1 import (
    ADAPTER_SKELETON_PRINCIPLE_ZH,
    FIELD_SYNTHESIS_ENTRYPOINT,
    FINAL_DECISION_READY_FOR_DRYRUN_CASES,
    RESERVED_CANDIDATE_TYPES,
    SUPPORTED_CANDIDATE_TYPES,
    FORBIDDEN_BACKEND_KINDS,
    FORBIDDEN_INPUT_MODES,
    FORBIDDEN_LICENSE_STATUSES,
    INHERITED_ADMISSION_PRINCIPLE_ZH,
    INHERITED_CANDIDATE_PRINCIPLE_ZH,
    INHERITED_SKELETON_PRINCIPLE_ZH,
    INHERITED_TRANSLATION_PRINCIPLE_ZH,
    MOCK_BACKEND_KINDS,
    PHASE_ID,
    SLAM_ADAPTER_INPUT_ENVELOPE_FIELDS,
    SLAM_ADAPTER_MAPPING_RULE_FIELDS,
    SLAM_ADAPTER_OUTPUT_BUNDLE_FIELDS,
    SLAM_ADAPTER_PLANNING_DECISION_FIELDS,
    SLAM_SPATIAL_EVIDENCE_ADAPTER_FIELDS,
    VISION_OCR_POLLUTION_CANDIDATES,
)

ALLOWED_MAPPING_CANDIDATE_TYPES: frozenset[str] = frozenset(
    SUPPORTED_CANDIDATE_TYPES + RESERVED_CANDIDATE_TYPES
)

VALIDATOR_RULE_IDS: Tuple[str, ...] = (
    "rule_01_all_objects_candidate_only_required",
    "rule_02_real_backend_connected_must_be_false",
    "rule_03_runtime_execution_allowed_must_be_false",
    "rule_04_provider_activation_allowed_must_be_false",
    "rule_05_camera_connected_must_be_false",
    "rule_06_imu_connected_must_be_false",
    "rule_07_ros_connected_must_be_false",
    "rule_08_backend_kind_must_be_mock_or_unknown_mock",
    "rule_09_input_mode_not_live_camera_imu_ros",
    "rule_10_license_gate_required_true",
    "rule_11_adapter_contract_required_true",
    "rule_12_field_synthesis_entrypoint_must_be_field_synthesis_v1",
    "rule_13_adapter_output_has_spatial_candidate",
    "rule_14_pose_candidate_requires_source_method_and_refs",
    "rule_15_motion_candidate_action_ready_must_be_false",
    "rule_16_spatial_anchor_no_confirm_destination",
    "rule_17_local_map_no_persistent_map_or_long_term_fact",
    "rule_18_slam_health_degradation_confidence_or_needs_observation_only",
    "rule_19_high_map_drift_not_ready_for_action_decision",
    "rule_20_relocalization_no_restore_runtime_trust",
    "rule_21_output_dispatch_no_direct_action",
    "rule_22_output_dispatch_no_direct_speech",
    "rule_23_output_dispatch_no_direct_fact_write",
    "rule_24_no_vision_ocr_candidate_schema_pollution",
    "rule_25_license_status_not_commercial_runtime_approved",
    "rule_26_recorded_offline_stub_not_enabled_by_default",
    "rule_27_output_bundle_preserves_source_chain",
    "rule_28_planning_decision_final_decision_ready_for_dryrun_cases",
)


def _missing_fields(data: Dict[str, Any], fields: Sequence[str]) -> List[str]:
    return [f"missing_{field_name}" for field_name in fields if field_name not in data]


def _is_mock_backend_kind(backend_kind: str) -> bool:
    return backend_kind in MOCK_BACKEND_KINDS or backend_kind.startswith("mock_")


def validate_candidate_only(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("candidate_only") is not True:
        return False, ["candidate_only_required"]
    return True, []


def validate_real_backend_connected_false(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("real_backend_connected") is True:
        return False, ["real_backend_connected_must_be_false"]
    return True, []


def validate_runtime_execution_allowed_false(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("runtime_execution_allowed") is True:
        return False, ["runtime_execution_allowed_must_be_false"]
    return True, []


def validate_provider_activation_allowed_false(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("provider_activation_allowed") is True:
        return False, ["provider_activation_allowed_must_be_false"]
    return True, []


def validate_sensor_connections_false(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    for key in ("camera_connected", "imu_connected", "ros_connected"):
        if data.get(key) is True:
            issues.append(f"{key}_must_be_false")
    return len(issues) == 0, issues


def validate_backend_kind_mock(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    backend_kind = data.get("backend_kind")
    if not backend_kind:
        return True, []
    if backend_kind in FORBIDDEN_BACKEND_KINDS:
        return False, [f"forbidden_backend_kind:{backend_kind}"]
    if not _is_mock_backend_kind(str(backend_kind)):
        return False, [f"backend_kind_not_mock:{backend_kind}"]
    return True, []


def validate_input_mode_allowed(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    input_mode = data.get("input_mode")
    if not input_mode:
        return True, []
    if input_mode in FORBIDDEN_INPUT_MODES:
        return False, [f"forbidden_input_mode:{input_mode}"]
    if input_mode == "recorded_offline_stub":
        if data.get("recorded_offline_stub_enabled") is True:
            return False, ["recorded_offline_stub_enabled_by_default"]
        return True, []
    if not is_registered("allowed_input_modes", str(input_mode)):
        return False, [f"input_mode_not_allowed:{input_mode}"]
    return True, []


def validate_license_gate_required(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("license_gate_required") is not True:
        return False, ["license_gate_required_must_be_true"]
    return True, []


def validate_adapter_contract_required(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("adapter_contract_required") is not True:
        return False, ["adapter_contract_required_must_be_true"]
    return True, []


def validate_field_synthesis_entrypoint(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    entrypoint = data.get("field_synthesis_entrypoint")
    if entrypoint and entrypoint != FIELD_SYNTHESIS_ENTRYPOINT:
        return False, [f"field_synthesis_entrypoint_must_be_{FIELD_SYNTHESIS_ENTRYPOINT}"]
    return True, []


def validate_direct_output_forbidden(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    for key in ("direct_action_allowed", "direct_speech_allowed", "direct_fact_write_allowed"):
        if data.get(key) is True:
            issues.append(f"{key}_must_be_false")
    return len(issues) == 0, issues


def validate_license_status(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    license_status = data.get("license_status")
    if license_status in FORBIDDEN_LICENSE_STATUSES:
        return False, [f"forbidden_license_status:{license_status}"]
    return True, []


def _bundle_has_spatial_candidate(bundle: Dict[str, Any]) -> bool:
    candidate_sections = (
        "pose_candidates",
        "motion_candidates",
        "spatial_anchor_candidates",
        "local_map_candidates",
        "slam_health_candidates",
        "map_drift_candidates",
        "relocalization_candidates",
    )
    for section in candidate_sections:
        value = bundle.get(section)
        if isinstance(value, (list, tuple)) and len(value) > 0:
            return True
    return False


def validate_output_bundle_candidates(bundle: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    bundle_ref = bundle.get("bundle_ref", "<unknown>")

    if not _bundle_has_spatial_candidate(bundle):
        issues.append(f"{bundle_ref}.missing_spatial_candidate")

    source_chain = bundle.get("source_chain")
    if not source_chain:
        issues.append(f"{bundle_ref}.missing_source_chain")

    output_types = set(bundle.get("output_candidate_types") or ())
    pollution = output_types.intersection(VISION_OCR_POLLUTION_CANDIDATES)
    if pollution:
        issues.append(f"{bundle_ref}.vision_ocr_pollution:{sorted(pollution)}")

    for pose in bundle.get("pose_candidates") or ():
        if not isinstance(pose, dict):
            continue
        if not pose.get("source_method") or not pose.get("source_refs"):
            issues.append(f"{bundle_ref}.pose_missing_source_method_or_refs")
        if pose.get("candidate_only") is not True:
            issues.append(f"{bundle_ref}.pose_not_candidate_only")

    for motion in bundle.get("motion_candidates") or ():
        if isinstance(motion, dict) and motion.get("action_ready") is True:
            issues.append(f"{bundle_ref}.motion_action_ready_forbidden")

    for anchor in bundle.get("spatial_anchor_candidates") or ():
        if isinstance(anchor, dict) and anchor.get("confirm_destination") is True:
            issues.append(f"{bundle_ref}.anchor_confirm_destination_forbidden")

    for local_map in bundle.get("local_map_candidates") or ():
        if not isinstance(local_map, dict):
            continue
        if local_map.get("persistent_map") is True:
            issues.append(f"{bundle_ref}.local_map_persistent_map_forbidden")
        if local_map.get("long_term_fact") is True:
            issues.append(f"{bundle_ref}.local_map_long_term_fact_forbidden")

    for health in bundle.get("slam_health_candidates") or ():
        if not isinstance(health, dict):
            continue
        effect = health.get("degradation_effect")
        if effect and effect not in ("confidence_downweight", "needs_more_observation"):
            issues.append(f"{bundle_ref}.health_degradation_effect_invalid:{effect}")

    for drift in bundle.get("map_drift_candidates") or ():
        if not isinstance(drift, dict):
            continue
        if drift.get("drift_risk") == "high" and drift.get("ready_for_action_decision") is True:
            issues.append(f"{bundle_ref}.high_drift_ready_for_action_forbidden")

    for reloc in bundle.get("relocalization_candidates") or ():
        if isinstance(reloc, dict) and reloc.get("restore_runtime_trust") is True:
            issues.append(f"{bundle_ref}.relocalization_restore_runtime_trust_forbidden")

    return len(issues) == 0, issues


def validate_slam_spatial_evidence_adapter(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, SLAM_SPATIAL_EVIDENCE_ADAPTER_FIELDS)
    for validator in (
        validate_candidate_only,
        validate_real_backend_connected_false,
        validate_runtime_execution_allowed_false,
        validate_provider_activation_allowed_false,
        validate_sensor_connections_false,
        validate_backend_kind_mock,
        validate_license_gate_required,
        validate_adapter_contract_required,
        validate_field_synthesis_entrypoint,
        validate_direct_output_forbidden,
    ):
        ok, part = validator(data)
        if not ok:
            issues.extend(part)
    return len(issues) == 0, issues


def validate_input_envelope(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, SLAM_ADAPTER_INPUT_ENVELOPE_FIELDS)
    for validator in (
        validate_candidate_only,
        validate_real_backend_connected_false,
        validate_sensor_connections_false,
        validate_backend_kind_mock,
        validate_input_mode_allowed,
        validate_license_gate_required,
        validate_adapter_contract_required,
        validate_license_status,
    ):
        ok, part = validator(data)
        if not ok:
            issues.extend(part)
    return len(issues) == 0, issues


def validate_mapping_rule(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, SLAM_ADAPTER_MAPPING_RULE_FIELDS)
    ok, part = validate_candidate_only(data)
    if not ok:
        issues.extend(part)
    if data.get("candidate_only_enforced") is not True:
        issues.append("candidate_only_enforced_required")
    if data.get("source_refs_required") is not True:
        issues.append("source_refs_required_must_be_true")
    candidate_type = data.get("luna_candidate_type")
    if candidate_type in VISION_OCR_POLLUTION_CANDIDATES:
        issues.append(f"vision_ocr_pollution_in_mapping:{candidate_type}")
    return len(issues) == 0, issues


def validate_planning_decision(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, SLAM_ADAPTER_PLANNING_DECISION_FIELDS)
    for validator in (
        validate_candidate_only,
        validate_real_backend_connected_false,
        validate_runtime_execution_allowed_false,
        validate_provider_activation_allowed_false,
        validate_sensor_connections_false,
        validate_license_gate_required,
        validate_adapter_contract_required,
        validate_field_synthesis_entrypoint,
        validate_direct_output_forbidden,
    ):
        ok, part = validator(data)
        if not ok:
            issues.extend(part)
    if data.get("candidate_only_enforced") is not True:
        issues.append("candidate_only_enforced_required")
    if data.get("final_decision") != FINAL_DECISION_READY_FOR_DRYRUN_CASES:
        issues.append("planning_final_decision_not_ready_for_dryrun_cases")
    return len(issues) == 0, issues


def validate_slam_spatial_evidence_adapter_mapping_case_bundle(
    bundle: Dict[str, Any],
) -> Tuple[bool, List[str]]:
    """Minimal mapping-delta validator (cases + runner); no upstream governance repeat."""
    issues: List[str] = []

    adapters = list(bundle.get("adapters") or ())
    output_bundles = list(bundle.get("output_bundles") or ())
    mapping_rules = list(bundle.get("mapping_rules") or ())

    if not adapters:
        issues.append("adapters_required")
    if not output_bundles:
        issues.append("output_bundles_required")
    if not mapping_rules:
        issues.append("mapping_rules_required")

    for adapter in adapters:
        if adapter.get("field_synthesis_entrypoint") != FIELD_SYNTHESIS_ENTRYPOINT:
            issues.append(
                f"adapter.{adapter.get('adapter_ref')}.synthesis_entrypoint_bypass:"
                f"{adapter.get('field_synthesis_entrypoint')!r}"
            )

    for rule in mapping_rules:
        candidate_type = rule.get("luna_candidate_type")
        if candidate_type not in ALLOWED_MAPPING_CANDIDATE_TYPES:
            issues.append(f"unsupported_candidate_type:{candidate_type}")

    for output_bundle in output_bundles:
        if output_bundle.get("field_synthesis_entrypoint") != FIELD_SYNTHESIS_ENTRYPOINT:
            issues.append(
                f"output_bundle.{output_bundle.get('bundle_ref')}.synthesis_entrypoint_bypass:"
                f"{output_bundle.get('field_synthesis_entrypoint')!r}"
            )
        source_chain = output_bundle.get("source_chain")
        if not source_chain:
            issues.append(
                f"output_bundle.{output_bundle.get('bundle_ref')}.missing_source_chain"
            )
        ok, part = validate_output_bundle_candidates(output_bundle)
        if not ok:
            issues.extend(part)

    return len(issues) == 0, issues


def validate_slam_spatial_evidence_adapter_matrix_v1(
    matrix: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, List[str]]:
    matrix = matrix or build_slam_spatial_evidence_adapter_matrix_v1()
    issues: List[str] = []

    for item in matrix.get("mock_backend_outputs") or ():
        for validator in (
            validate_candidate_only,
            validate_real_backend_connected_false,
            validate_runtime_execution_allowed_false,
            validate_provider_activation_allowed_false,
            validate_backend_kind_mock,
        ):
            ok, part = validator(item)
            if not ok:
                issues.extend([f"mock_backend_output.{err}" for err in part])

    for item in matrix.get("input_envelopes") or ():
        ok, part = validate_input_envelope(item)
        if not ok:
            issues.extend([f"input_envelope.{err}" for err in part])

    for item in matrix.get("mapping_rules") or ():
        ok, part = validate_mapping_rule(item)
        if not ok:
            issues.extend([f"mapping_rule.{err}" for err in part])

    for item in matrix.get("adapters") or ():
        ok, part = validate_slam_spatial_evidence_adapter(item)
        if not ok:
            issues.extend([f"adapter.{err}" for err in part])

    for item in matrix.get("output_bundles") or ():
        ok, part = validate_output_bundle_candidates(item)
        if not ok:
            issues.extend(part)
        ok2, part2 = validate_direct_output_forbidden(item)
        if not ok2:
            issues.extend([f"output_bundle.{err}" for err in part2])
        ok3, part3 = validate_field_synthesis_entrypoint(item)
        if not ok3:
            issues.extend([f"output_bundle.{err}" for err in part3])

    planning = matrix.get("planning_decision") or {}
    ok, part = validate_planning_decision(planning)
    if not ok:
        issues.extend([f"planning_decision.{err}" for err in part])

    for policy in FORBIDDEN_ADAPTER_POLICIES:
        serialized = json.dumps(matrix, ensure_ascii=False)
        if f'"policy": "{policy}"' in serialized or f"policy={policy}" in serialized:
            issues.append(f"forbidden_adapter_policy_present:{policy}")

    return len(issues) == 0, issues


def summarize_slam_spatial_evidence_adapter_planning_v1() -> Dict[str, Any]:
    import_ok = True
    try:
        from capabilities.field_understanding.slam_spatial_evidence_adapter import (  # noqa: F401
            slam_spatial_evidence_adapter_registry_v1,
            slam_spatial_evidence_adapter_types_v1,
        )
    except Exception:
        import_ok = False

    registry_ok, registry_issues = validate_registry()
    matrix = build_slam_spatial_evidence_adapter_matrix_v1()
    matrix_ok, matrix_issues = validate_slam_spatial_evidence_adapter_matrix_v1(matrix)
    planning = matrix.get("planning_decision") or {}

    candidate_only_enforced = all(
        item.get("candidate_only") is True
        for section in (
            "mock_backend_outputs",
            "backend_output_frames",
            "input_envelopes",
            "mapping_rules",
            "adapters",
            "output_bundles",
            "health_reports",
        )
        for item in matrix.get(section) or ()
    ) and planning.get("candidate_only") is True

    ready = (
        import_ok
        and registry_ok
        and matrix_ok
        and len(VALIDATOR_RULE_IDS) >= 24
        and len(matrix.get("mock_backend_outputs") or ()) >= 5
        and len(matrix.get("backend_output_frames") or ()) >= 5
        and len(matrix.get("input_envelopes") or ()) >= 5
        and len(matrix.get("mapping_rules") or ()) >= 7
        and len(matrix.get("adapters") or ()) >= 5
        and len(matrix.get("output_bundles") or ()) >= 5
        and len(matrix.get("health_reports") or ()) >= 5
        and len(matrix.get("planning_decision") or {}) >= 1
        and candidate_only_enforced
        and planning.get("real_backend_connected") is False
        and planning.get("runtime_execution_allowed") is False
        and planning.get("provider_activation_allowed") is False
        and planning.get("camera_connected") is False
        and planning.get("imu_connected") is False
        and planning.get("ros_connected") is False
        and planning.get("license_gate_required") is True
        and planning.get("adapter_contract_required") is True
        and planning.get("field_synthesis_entrypoint") == FIELD_SYNTHESIS_ENTRYPOINT
        and planning.get("direct_action_allowed") is False
        and planning.get("direct_speech_allowed") is False
        and planning.get("direct_fact_write_allowed") is False
        and planning.get("final_decision") == FINAL_DECISION_READY_FOR_DRYRUN_CASES
    )

    return {
        "phase_id": PHASE_ID,
        "step": "Step 1 SLAM Spatial Evidence Adapter Static Baseline",
        "adapter_skeleton_principle_zh": ADAPTER_SKELETON_PRINCIPLE_ZH,
        "inherited_principles_zh": [
            INHERITED_TRANSLATION_PRINCIPLE_ZH,
            INHERITED_ADMISSION_PRINCIPLE_ZH,
            INHERITED_SKELETON_PRINCIPLE_ZH,
            INHERITED_CANDIDATE_PRINCIPLE_ZH,
        ],
        "import_ok": import_ok,
        "mock_backend_output_count": len(matrix.get("mock_backend_outputs") or ()),
        "backend_output_frame_count": len(matrix.get("backend_output_frames") or ()),
        "adapter_input_envelope_count": len(matrix.get("input_envelopes") or ()),
        "mapping_rule_count": len(matrix.get("mapping_rules") or ()),
        "adapter_count": len(matrix.get("adapters") or ()),
        "output_bundle_count": len(matrix.get("output_bundles") or ()),
        "adapter_health_report_count": len(matrix.get("health_reports") or ()),
        "planning_decision_count": 1 if planning else 0,
        "validator_rules": len(VALIDATOR_RULE_IDS),
        "translation_chain": matrix.get("translation_chain") or [],
        "registry_ok": registry_ok,
        "registry_issues": registry_issues,
        "matrix_ok": matrix_ok,
        "matrix_issues": matrix_issues,
        "candidate_only_enforced": candidate_only_enforced,
        "real_backend_connected": planning.get("real_backend_connected"),
        "runtime_execution_allowed": planning.get("runtime_execution_allowed"),
        "provider_activation_allowed": planning.get("provider_activation_allowed"),
        "camera_connected": planning.get("camera_connected"),
        "imu_connected": planning.get("imu_connected"),
        "ros_connected": planning.get("ros_connected"),
        "license_gate_required": planning.get("license_gate_required"),
        "adapter_contract_required": planning.get("adapter_contract_required"),
        "field_synthesis_entrypoint_locked": planning.get("field_synthesis_entrypoint"),
        "direct_action_allowed": planning.get("direct_action_allowed"),
        "direct_speech_allowed": planning.get("direct_speech_allowed"),
        "direct_fact_write_allowed": planning.get("direct_fact_write_allowed"),
        "final_decision": (
            FINAL_DECISION_READY_FOR_DRYRUN_CASES
            if ready
            else "SLAM_SPATIAL_EVIDENCE_ADAPTER_SKELETON_PLANNING_NOT_READY"
        ),
    }


def main() -> int:
    summary = summarize_slam_spatial_evidence_adapter_planning_v1()
    print(json.dumps(summary, ensure_ascii=False))
    return 0 if summary["final_decision"] == FINAL_DECISION_READY_FOR_DRYRUN_CASES else 1


if __name__ == "__main__":
    raise SystemExit(main())
