# -*- coding: utf-8 -*-
"""SLAM Offline Real Backend Adapter Trial — static validators v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.slam_offline_backend_adapter_trial.slam_offline_backend_adapter_trial_registry_v1 import (
    GPL_TECHNICAL_REFERENCE_ONLY_STUBS,
    build_slam_offline_backend_adapter_trial_matrix_v1,
    is_registered,
    validate_registry,
)
from capabilities.field_understanding.slam_offline_backend_adapter_trial.slam_offline_backend_adapter_trial_types_v1 import (
    ADAPTER_PROFILE_REF,
    DOMAIN_ID,
    FIELD_SYNTHESIS_ENTRYPOINT,
    FINAL_DECISION_READY_FOR_CASES,
    FORBIDDEN_RUNTIME_MODES,
    MODEL_ADMISSION_STANDARD_REF,
    MODEL_FAMILY,
    MODEL_ID,
    MODEL_MANAGEMENT_PROTOCOL_REF,
    OFFLINE_SLAM_ADAPTER_TRIAL_CONFIG_FIELDS,
    OFFLINE_SLAM_BACKEND_OUTPUT_FILE_FIELDS,
    OFFLINE_SLAM_BACKEND_OUTPUT_PARSER_FIELDS,
    OFFLINE_SLAM_PARSED_EVIDENCE_BUNDLE_FIELDS,
    OFFLINE_SLAM_TRIAL_INPUT_MANIFEST_FIELDS,
    OFFLINE_SLAM_TRIAL_PLANNING_DECISION_FIELDS,
    OFFLINE_SLAM_TRIAL_REVIEW_POLICY_FIELDS,
    OUTPUT_CANDIDATE_CONTRACT_REF,
    PHASE_ID,
    TRIAL_PRINCIPLE_ZH,
)

VALIDATOR_RULE_IDS: Tuple[str, ...] = (
    "rule_01_not_independent_slam_flow_required",
    "rule_02_model_management_protocol_ref_required",
    "rule_03_model_admission_standard_ref_required",
    "rule_04_model_id_sample_slam_spatial_evidence_model",
    "rule_05_adapter_profile_slam_spatial_evidence_adapter",
    "rule_06_output_candidate_contract_spatial_evidence_bundle",
    "rule_07_offline_only_required",
    "rule_08_live_runtime_forbidden",
    "rule_09_provider_runtime_activation_forbidden",
    "rule_10_commercial_runtime_approved_forbidden",
    "rule_11_field_synthesis_entrypoint_locked",
    "rule_12_source_chain_required_on_output_file_and_bundle",
    "rule_13_candidate_only_default_true",
    "rule_14_direct_action_speech_fact_write_forbidden",
    "rule_15_backend_format_stub_registered",
    "rule_16_gpl_stub_technical_reference_only",
    "rule_17_gpl_stub_not_commercial_runtime_candidate",
    "rule_18_input_mode_not_live_camera_imu_ros",
    "rule_19_adapter_mapping_required_in_review_policy",
    "rule_20_planning_final_decision_ready_for_cases",
)


def _missing_fields(data: Dict[str, Any], fields: Sequence[str]) -> List[str]:
    return [f"missing_{field_name}" for field_name in fields if field_name not in data]


def validate_candidate_only(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("candidate_only") is not True:
        return False, ["candidate_only_required"]
    return True, []


def validate_offline_only(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("offline_only") is not True:
        return False, ["offline_only_required"]
    return True, []


def validate_live_runtime_forbidden(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    for key in ("live_runtime_forbidden", "live_camera_forbidden", "live_imu_forbidden", "ros_runtime_forbidden"):
        if key in data and data.get(key) is not True:
            issues.append(f"{key}_must_be_true")
    input_mode = data.get("input_mode")
    if input_mode in FORBIDDEN_RUNTIME_MODES:
        issues.append(f"forbidden_input_mode:{input_mode}")
    return len(issues) == 0, issues


def validate_model_binding(config: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    expectations = {
        "model_id": MODEL_ID,
        "model_family": MODEL_FAMILY,
        "domain_id": DOMAIN_ID,
        "model_management_protocol_ref": MODEL_MANAGEMENT_PROTOCOL_REF,
        "model_admission_standard_ref": MODEL_ADMISSION_STANDARD_REF,
        "adapter_profile_ref": ADAPTER_PROFILE_REF,
        "output_candidate_contract_ref": OUTPUT_CANDIDATE_CONTRACT_REF,
        "field_synthesis_entrypoint": FIELD_SYNTHESIS_ENTRYPOINT,
    }
    for key, expected in expectations.items():
        if config.get(key) != expected:
            issues.append(f"{key}: expected={expected!r}, actual={config.get(key)!r}")
    return len(issues) == 0, issues


def validate_offline_backend_output_file(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, OFFLINE_SLAM_BACKEND_OUTPUT_FILE_FIELDS)
    for validator in (validate_candidate_only, validate_offline_only, validate_live_runtime_forbidden):
        ok, part = validator(data)
        if not ok:
            issues.extend(part)
    stub = data.get("backend_format_stub")
    if stub and not is_registered("offline_backend_format_stubs", str(stub)):
        issues.append(f"backend_format_stub_not_registered:{stub}")
    if stub in GPL_TECHNICAL_REFERENCE_ONLY_STUBS:
        if data.get("technical_reference_only") is not True:
            issues.append(f"{stub}.technical_reference_only_required")
        if data.get("commercial_runtime_candidate") is True:
            issues.append(f"{stub}.commercial_runtime_candidate_forbidden")
    if not data.get("source_chain"):
        issues.append("source_chain_required")
    return len(issues) == 0, issues


def validate_offline_backend_output_parser(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, OFFLINE_SLAM_BACKEND_OUTPUT_PARSER_FIELDS)
    for validator in (validate_candidate_only, validate_offline_only, validate_live_runtime_forbidden):
        ok, part = validator(data)
        if not ok:
            issues.extend(part)
    stub = data.get("backend_format_stub")
    if stub and not is_registered("offline_backend_format_stubs", str(stub)):
        issues.append(f"backend_format_stub_not_registered:{stub}")
    return len(issues) == 0, issues


def validate_trial_input_manifest(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, OFFLINE_SLAM_TRIAL_INPUT_MANIFEST_FIELDS)
    for validator in (validate_candidate_only, validate_offline_only, validate_live_runtime_forbidden):
        ok, part = validator(data)
        if not ok:
            issues.extend(part)
    if data.get("model_id") != MODEL_ID:
        issues.append("manifest_model_id_mismatch")
    return len(issues) == 0, issues


def validate_adapter_trial_config(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, OFFLINE_SLAM_ADAPTER_TRIAL_CONFIG_FIELDS)
    for validator in (validate_candidate_only, validate_offline_only):
        ok, part = validator(data)
        if not ok:
            issues.extend(part)
    ok, part = validate_model_binding(data)
    if not ok:
        issues.extend(part)
    if data.get("provider_runtime_activation_allowed") is True:
        issues.append("provider_runtime_activation_allowed_must_be_false")
    if data.get("commercial_runtime_approved") is True:
        issues.append("commercial_runtime_approved_must_be_false")
    return len(issues) == 0, issues


def validate_parsed_evidence_bundle(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, OFFLINE_SLAM_PARSED_EVIDENCE_BUNDLE_FIELDS)
    ok, part = validate_candidate_only(data)
    if not ok:
        issues.extend(part)
    if data.get("field_synthesis_entrypoint") != FIELD_SYNTHESIS_ENTRYPOINT:
        issues.append("field_synthesis_entrypoint_bypass")
    if not data.get("source_chain"):
        issues.append("source_chain_required")
    for key in ("direct_action_allowed", "direct_speech_allowed", "direct_fact_write_allowed"):
        if data.get(key) is True:
            issues.append(f"{key}_must_be_false")
    if not data.get("output_candidate_types"):
        issues.append("output_candidate_types_required")
    return len(issues) == 0, issues


def validate_trial_review_policy(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, OFFLINE_SLAM_TRIAL_REVIEW_POLICY_FIELDS)
    ok, part = validate_candidate_only(data)
    if not ok:
        issues.extend(part)
    if data.get("offline_parse_only") is not True:
        issues.append("offline_parse_only_required")
    if data.get("adapter_mapping_required") is not True:
        issues.append("adapter_mapping_required")
    if data.get("field_synthesis_entrypoint_locked") != FIELD_SYNTHESIS_ENTRYPOINT:
        issues.append("field_synthesis_entrypoint_not_locked")
    if data.get("provider_runtime_activation_forbidden") is not True:
        issues.append("provider_runtime_activation_forbidden_required")
    if data.get("commercial_runtime_approval_forbidden") is not True:
        issues.append("commercial_runtime_approval_forbidden_required")
    return len(issues) == 0, issues


def validate_planning_decision(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, OFFLINE_SLAM_TRIAL_PLANNING_DECISION_FIELDS)
    ok, part = validate_candidate_only(data)
    if not ok:
        issues.extend(part)
    ok, part = validate_model_binding(data)
    if not ok:
        issues.extend(part)
    if data.get("not_independent_slam_flow") is not True:
        issues.append("not_independent_slam_flow_required")
    if data.get("offline_only") is not True:
        issues.append("offline_only_required")
    if data.get("provider_runtime_activation_allowed") is True:
        issues.append("provider_runtime_activation_allowed_must_be_false")
    if data.get("commercial_runtime_approved") is True:
        issues.append("commercial_runtime_approved_must_be_false")
    if data.get("candidate_only_enforced") is not True:
        issues.append("candidate_only_enforced_required")
    if data.get("final_decision") != FINAL_DECISION_READY_FOR_CASES:
        issues.append("planning_final_decision_not_ready_for_cases")
    return len(issues) == 0, issues


def validate_slam_offline_backend_adapter_trial_case_bundle(
    bundle: Dict[str, Any],
) -> Tuple[bool, List[str]]:
    """Minimal offline-trial case validator; does not repeat upstream governance checks."""
    issues: List[str] = []

    output_file = bundle.get("offline_backend_output_file") or {}
    parser = bundle.get("offline_backend_output_parser") or {}
    config = bundle.get("adapter_trial_config") or {}
    parsed = bundle.get("parsed_evidence_bundle") or {}

    if not output_file:
        issues.append("offline_backend_output_file_required")
    if not parser:
        issues.append("offline_backend_output_parser_required")
    if not config:
        issues.append("adapter_trial_config_required")
    if not parsed:
        issues.append("parsed_evidence_bundle_required")

    if output_file.get("offline_only") is not True:
        issues.append("output_file.offline_only_required")
    if parser.get("offline_only") is not True:
        issues.append("parser.offline_only_required")

    if not parser.get("parser_ref") or not parser.get("parser_status"):
        issues.append("parser_not_declared")

    if not output_file.get("source_chain"):
        issues.append("output_file.missing_source_chain")
    if not parsed.get("source_chain"):
        issues.append("parsed_bundle.missing_source_chain")

    admission_ref = config.get("model_admission_standard_ref")
    if not admission_ref:
        issues.append("model_admission_standard_ref_required")
    elif admission_ref != MODEL_ADMISSION_STANDARD_REF:
        issues.append(
            f"model_admission_standard_ref_mismatch:"
            f"expected={MODEL_ADMISSION_STANDARD_REF!r}, actual={admission_ref!r}"
        )

    if config.get("adapter_profile_ref") != ADAPTER_PROFILE_REF:
        issues.append(
            f"adapter_profile_bypass:"
            f"expected={ADAPTER_PROFILE_REF!r}, actual={config.get('adapter_profile_ref')!r}"
        )
    if config.get("output_candidate_contract_ref") != OUTPUT_CANDIDATE_CONTRACT_REF:
        issues.append(
            f"output_candidate_contract_bypass:"
            f"expected={OUTPUT_CANDIDATE_CONTRACT_REF!r}, "
            f"actual={config.get('output_candidate_contract_ref')!r}"
        )

    if config.get("field_synthesis_entrypoint") != FIELD_SYNTHESIS_ENTRYPOINT:
        issues.append(
            f"config.field_synthesis_entrypoint_bypass:"
            f"{config.get('field_synthesis_entrypoint')!r}"
        )
    if parsed.get("field_synthesis_entrypoint") != FIELD_SYNTHESIS_ENTRYPOINT:
        issues.append(
            f"parsed_bundle.field_synthesis_entrypoint_bypass:"
            f"{parsed.get('field_synthesis_entrypoint')!r}"
        )

    if parsed.get("candidate_only") is not True:
        issues.append("parsed_bundle.candidate_only_required")

    stub = output_file.get("backend_format_stub")
    if stub in GPL_TECHNICAL_REFERENCE_ONLY_STUBS:
        if output_file.get("commercial_runtime_candidate") is True:
            issues.append(f"{stub}.commercial_runtime_candidate_forbidden")

    return len(issues) == 0, issues


def validate_slam_offline_backend_adapter_trial_matrix_v1(
    matrix: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, List[str]]:
    matrix = matrix or build_slam_offline_backend_adapter_trial_matrix_v1()
    issues: List[str] = []

    registry_ok, registry_issues = validate_registry()
    issues.extend(registry_issues)

    binding = matrix.get("model_binding") or {}
    ok, part = validate_model_binding(binding)
    if not ok:
        issues.extend([f"model_binding.{err}" for err in part])

    for item in matrix.get("offline_backend_output_files") or ():
        ok, part = validate_offline_backend_output_file(item)
        if not ok:
            issues.extend([f"offline_backend_output_file.{item.get('file_ref')}.{err}" for err in part])

    for item in matrix.get("offline_backend_output_parsers") or ():
        ok, part = validate_offline_backend_output_parser(item)
        if not ok:
            issues.extend([f"offline_backend_output_parser.{item.get('parser_ref')}.{err}" for err in part])

    for item in matrix.get("trial_input_manifests") or ():
        ok, part = validate_trial_input_manifest(item)
        if not ok:
            issues.extend([f"trial_input_manifest.{item.get('manifest_ref')}.{err}" for err in part])

    for item in matrix.get("adapter_trial_configs") or ():
        ok, part = validate_adapter_trial_config(item)
        if not ok:
            issues.extend([f"adapter_trial_config.{item.get('config_ref')}.{err}" for err in part])

    for item in matrix.get("parsed_evidence_bundles") or ():
        ok, part = validate_parsed_evidence_bundle(item)
        if not ok:
            issues.extend([f"parsed_evidence_bundle.{item.get('bundle_ref')}.{err}" for err in part])

    ok, part = validate_trial_review_policy(matrix.get("trial_review_policy") or {})
    if not ok:
        issues.extend([f"trial_review_policy.{err}" for err in part])

    ok, part = validate_planning_decision(matrix.get("planning_decision") or {})
    if not ok:
        issues.extend([f"planning_decision.{err}" for err in part])

    return len(issues) == 0 and registry_ok, issues


def summarize_slam_offline_backend_adapter_trial_planning_v1() -> Dict[str, Any]:
    import_ok = True
    try:
        from capabilities.field_understanding.slam_offline_backend_adapter_trial import (  # noqa: F401
            slam_offline_backend_adapter_trial_registry_v1,
            slam_offline_backend_adapter_trial_types_v1,
        )
    except Exception:
        import_ok = False

    registry_ok, registry_issues = validate_registry()
    matrix = build_slam_offline_backend_adapter_trial_matrix_v1()
    matrix_ok, matrix_issues = validate_slam_offline_backend_adapter_trial_matrix_v1(matrix)
    planning = matrix.get("planning_decision") or {}
    binding = matrix.get("model_binding") or {}

    ready = (
        import_ok
        and registry_ok
        and matrix_ok
        and len(VALIDATOR_RULE_IDS) >= 20
        and len(matrix.get("offline_backend_output_files") or ()) >= 7
        and len(matrix.get("offline_backend_output_parsers") or ()) >= 7
        and len(matrix.get("trial_input_manifests") or ()) >= 7
        and len(matrix.get("adapter_trial_configs") or ()) >= 7
        and len(matrix.get("parsed_evidence_bundles") or ()) >= 7
        and planning.get("not_independent_slam_flow") is True
        and planning.get("offline_only") is True
        and planning.get("provider_runtime_activation_allowed") is False
        and planning.get("commercial_runtime_approved") is False
        and planning.get("candidate_only_enforced") is True
        and binding.get("model_admission_standard_ref") == MODEL_ADMISSION_STANDARD_REF
        and planning.get("final_decision") == FINAL_DECISION_READY_FOR_CASES
    )

    return {
        "phase_id": PHASE_ID,
        "step": "Step 1 Offline Backend Output Trial Planning",
        "trial_principle_zh": TRIAL_PRINCIPLE_ZH,
        "import_ok": import_ok,
        "model_binding": binding,
        "offline_backend_output_file_count": len(matrix.get("offline_backend_output_files") or ()),
        "offline_backend_output_parser_count": len(matrix.get("offline_backend_output_parsers") or ()),
        "trial_input_manifest_count": len(matrix.get("trial_input_manifests") or ()),
        "adapter_trial_config_count": len(matrix.get("adapter_trial_configs") or ()),
        "parsed_evidence_bundle_count": len(matrix.get("parsed_evidence_bundles") or ()),
        "trial_review_policy_count": 1 if matrix.get("trial_review_policy") else 0,
        "planning_decision_count": 1 if planning else 0,
        "offline_backend_format_stub_count": len(matrix.get("offline_backend_output_files") or ()),
        "validator_rules": len(VALIDATOR_RULE_IDS),
        "trial_pipeline": matrix.get("trial_pipeline") or [],
        "gpl_technical_reference_only_stubs": list(GPL_TECHNICAL_REFERENCE_ONLY_STUBS),
        "not_independent_slam_flow": planning.get("not_independent_slam_flow"),
        "offline_only": planning.get("offline_only"),
        "provider_runtime_activation_allowed": planning.get("provider_runtime_activation_allowed"),
        "commercial_runtime_approved": planning.get("commercial_runtime_approved"),
        "field_synthesis_entrypoint_locked": planning.get("field_synthesis_entrypoint"),
        "registry_ok": registry_ok,
        "registry_issues": registry_issues,
        "matrix_ok": matrix_ok,
        "matrix_issues": matrix_issues,
        "final_decision": (
            FINAL_DECISION_READY_FOR_CASES
            if ready
            else "SLAM_OFFLINE_BACKEND_ADAPTER_TRIAL_PLANNING_NOT_READY"
        ),
    }


def main() -> int:
    summary = summarize_slam_offline_backend_adapter_trial_planning_v1()
    print(json.dumps(summary, ensure_ascii=False))
    return 0 if summary["final_decision"] == FINAL_DECISION_READY_FOR_CASES else 1


if __name__ == "__main__":
    raise SystemExit(main())
