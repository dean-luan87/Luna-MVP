# -*- coding: utf-8 -*-
"""Provider Manager Runtime Skeleton — static validators v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.midplatform.provider_manager_runtime_skeleton.provider_manager_runtime_skeleton_registry_v1 import (
    ACTIVATION_GATE_REQUIRED_CHECKS,
    FORBIDDEN_RUNTIME_SKELETON_POLICIES,
    SYNTHESIS_ENTRYPOINTS,
    build_provider_manager_runtime_skeleton_matrix_v1,
    is_registered,
    validate_registry,
)
from capabilities.midplatform.provider_manager_runtime_skeleton.provider_manager_runtime_skeleton_types_v1 import (
    ACTIVATION_GATE_REQUIRED_CHECKS as TYPE_ACTIVATION_GATES,
    DOMAIN_SPATIAL_EVIDENCE,
    DOMAIN_VISION_OCR,
    FIELD_SYNTHESIS_ENTRYPOINT,
    FINAL_DECISION_READY_FOR_DRYRUN_CASES,
    MIDPLATFORM_SYNTHESIS_ENTRYPOINT,
    PHASE_ID,
    PROVIDER_ACTIVATION_GATE_FIELDS,
    PROVIDER_FALLBACK_EXECUTOR_CANDIDATE_FIELDS,
    PROVIDER_MANAGER_RUNTIME_SKELETON_FIELDS,
    PROVIDER_OUTPUT_DISPATCH_CANDIDATE_FIELDS,
    PROVIDER_RUNTIME_DECISION_FIELDS,
    PROVIDER_RUNTIME_HEALTH_LOOP_FIELDS,
    PROVIDER_RUNTIME_SKELETON_PLANNING_DECISION_FIELDS,
    RUNTIME_PROVIDER_REGISTRY_FIELDS,
    RUNTIME_SKELETON_PRINCIPLE_ZH,
    SHARED_GOVERNANCE_SOURCE_REF,
)

VALIDATOR_RULE_IDS: Tuple[str, ...] = (
    "rule_01_all_objects_candidate_only_required",
    "rule_02_runtime_execution_allowed_must_be_false",
    "rule_03_provider_activation_allowed_must_be_false",
    "rule_04_fallback_execution_allowed_must_be_false",
    "rule_05_output_dispatch_allowed_must_be_false",
    "rule_06_real_provider_connected_must_be_false",
    "rule_07_domain_id_registered",
    "rule_08_synthesis_entrypoint_registered",
    "rule_09_shared_governance_source_required",
    "rule_10_domain_profile_source_required",
    "rule_11_registry_provider_refs_from_domain_profile",
    "rule_12_activation_gate_required_gates_present",
    "rule_13_activation_not_allowed_until_all_gates_pass",
    "rule_14_health_loop_no_direct_runtime_disable",
    "rule_15_health_loop_decision_candidate_only",
    "rule_16_fallback_executor_no_execution",
    "rule_17_fallback_preserves_source_chain",
    "rule_18_output_dispatch_no_direct_paths",
    "rule_19_spatial_synthesis_field_synthesis_v1_only",
    "rule_20_vision_ocr_synthesis_abstraction_path_only",
    "rule_21_no_cross_domain_candidate_schema_pollution",
    "rule_22_no_domain_specific_manager_duplication",
    "rule_23_forbidden_runtime_skeleton_policies_absent",
    "rule_24_final_decision_ready_for_dryrun_cases",
)

_SPATIAL_POLLUTION_CANDIDATES = frozenset({"PoseCandidate", "SLAMHealthCandidate"})
_VISION_OCR_SIGNATURE_CANDIDATES = frozenset(
    {
        "DetectionCandidate",
        "TrackingCandidate",
        "SceneUnderstandingCandidate",
        "ocr_result_candidate",
        "ocr_evidence_pack_candidate",
        "roi_candidate",
    }
)


def _missing_fields(data: Dict[str, Any], fields: Sequence[str]) -> List[str]:
    return [f"missing_{f}" for f in fields if f not in data]


def _text_fields(data: Dict[str, Any]) -> List[str]:
    texts: List[str] = []
    for key in (
        "activation_decision_candidate",
        "health_decision_candidate",
        "decision_candidate_ref",
        "decision_status",
        "decision_type",
    ):
        val = data.get(key)
        if isinstance(val, str):
            texts.append(val)
    return texts


def validate_candidate_only(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("candidate_only") is not True:
        return False, ["candidate_only_required"]
    return True, []


def validate_runtime_execution_allowed_false(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("runtime_execution_allowed") is True:
        return False, ["runtime_execution_allowed_must_be_false"]
    return True, []


def validate_provider_activation_allowed_false(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("provider_activation_allowed") is True:
        return False, ["provider_activation_allowed_must_be_false"]
    return True, []


def validate_fallback_execution_allowed_false(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("fallback_execution_allowed") is True:
        return False, ["fallback_execution_allowed_must_be_false"]
    return True, []


def validate_output_dispatch_allowed_false(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("output_dispatch_allowed") is True:
        return False, ["output_dispatch_allowed_must_be_false"]
    return True, []


def validate_real_provider_connected_false(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("real_provider_connected") is True:
        return False, ["real_provider_connected_must_be_false"]
    return True, []


def validate_domain_id_registered(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    domain_id = data.get("domain_id")
    if not domain_id:
        return False, ["domain_id_required"]
    if not is_registered("supported_domain_ids", domain_id):
        return False, ["domain_id_not_registered"]
    return True, []


def validate_synthesis_entrypoint_registered(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    entrypoint = data.get("synthesis_entrypoint")
    if not entrypoint:
        return True, []
    if entrypoint not in SYNTHESIS_ENTRYPOINTS:
        return False, ["synthesis_entrypoint_not_registered"]
    return True, []


def validate_shared_governance_source(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    source = data.get("shared_governance_source_ref")
    if source != SHARED_GOVERNANCE_SOURCE_REF:
        return False, [f"shared_governance_source_must_be_{SHARED_GOVERNANCE_SOURCE_REF}"]
    return True, []


def validate_domain_profile_source(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if not data.get("domain_profile_ref") and not data.get("domain_profile_refs"):
        return False, ["domain_profile_source_required"]
    return True, []


def validate_forbidden_policies_absent(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    for text in _text_fields(data):
        for policy in FORBIDDEN_RUNTIME_SKELETON_POLICIES:
            if policy == text or policy in text:
                issues.append(f"forbidden_runtime_skeleton_policy_present:{policy}")
    return len(issues) == 0, issues


def validate_provider_manager_runtime_skeleton(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, PROVIDER_MANAGER_RUNTIME_SKELETON_FIELDS)
    for validator in (
        validate_candidate_only,
        validate_runtime_execution_allowed_false,
        validate_provider_activation_allowed_false,
        validate_real_provider_connected_false,
        validate_domain_id_registered,
        validate_shared_governance_source,
        validate_domain_profile_source,
        validate_forbidden_policies_absent,
    ):
        ok, part = validator(data)
        if not ok:
            issues.extend(part)
    status = data.get("skeleton_status")
    if status and not is_registered("skeleton_statuses", status):
        issues.append("skeleton_status_not_registered")
    return len(issues) == 0, issues


def validate_runtime_provider_registry(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, RUNTIME_PROVIDER_REGISTRY_FIELDS)
    for validator in (
        validate_candidate_only,
        validate_runtime_execution_allowed_false,
        validate_provider_activation_allowed_false,
        validate_real_provider_connected_false,
        validate_domain_id_registered,
        validate_shared_governance_source,
        validate_domain_profile_source,
        validate_forbidden_policies_absent,
    ):
        ok, part = validator(data)
        if not ok:
            issues.extend(part)
    reg_status = data.get("registration_status")
    if reg_status and not is_registered("registration_statuses", reg_status):
        issues.append("registration_status_not_registered")
    return len(issues) == 0, issues


def validate_provider_activation_gate(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, PROVIDER_ACTIVATION_GATE_FIELDS)
    for validator in (
        validate_candidate_only,
        validate_runtime_execution_allowed_false,
        validate_provider_activation_allowed_false,
        validate_domain_id_registered,
        validate_shared_governance_source,
        validate_domain_profile_source,
        validate_forbidden_policies_absent,
    ):
        ok, part = validator(data)
        if not ok:
            issues.extend(part)

    required = data.get("required_gates") or ()
    for gate in ACTIVATION_GATE_REQUIRED_CHECKS:
        if gate not in required:
            issues.append(f"activation_gate_missing_required_gate:{gate}")

    all_passed = data.get("all_gates_passed") is True
    if data.get("provider_activation_allowed") is True and not all_passed:
        issues.append("activation_allowed_without_all_gates_passed")
    if all_passed and data.get("provider_activation_allowed") is True:
        issues.append("activation_allowed_in_planning_even_when_gates_passed")

    return len(issues) == 0, issues


def validate_provider_runtime_health_loop(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, PROVIDER_RUNTIME_HEALTH_LOOP_FIELDS)
    for validator in (
        validate_candidate_only,
        validate_runtime_execution_allowed_false,
        validate_forbidden_policies_absent,
    ):
        ok, part = validator(data)
        if not ok:
            issues.extend(part)

    if data.get("runtime_disable_executed") is True:
        issues.append("health_loop_runtime_disable_executed_not_allowed")
    if data.get("direct_runtime_disable_allowed") is True:
        issues.append("health_loop_direct_runtime_disable_not_allowed")

    decision = data.get("health_decision_candidate")
    if decision and not is_registered("health_decision_candidates", decision):
        issues.append("health_decision_candidate_not_registered")

    return len(issues) == 0, issues


def validate_provider_fallback_executor_candidate(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, PROVIDER_FALLBACK_EXECUTOR_CANDIDATE_FIELDS)
    for validator in (
        validate_candidate_only,
        validate_runtime_execution_allowed_false,
        validate_fallback_execution_allowed_false,
        validate_domain_id_registered,
        validate_forbidden_policies_absent,
    ):
        ok, part = validator(data)
        if not ok:
            issues.extend(part)

    if data.get("fallback_executed") is True:
        issues.append("fallback_executed_not_allowed_in_planning")
    if data.get("preserve_source_chain") is not True:
        issues.append("preserve_source_chain_required")
    if data.get("preserve_conflict_refs") is not True:
        issues.append("preserve_conflict_refs_required")

    mode = data.get("fallback_mode")
    if mode and not is_registered("fallback_modes", mode):
        issues.append("fallback_mode_not_registered")

    return len(issues) == 0, issues


def validate_provider_output_dispatch_candidate(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, PROVIDER_OUTPUT_DISPATCH_CANDIDATE_FIELDS)
    for validator in (
        validate_candidate_only,
        validate_runtime_execution_allowed_false,
        validate_output_dispatch_allowed_false,
        validate_domain_id_registered,
        validate_synthesis_entrypoint_registered,
        validate_forbidden_policies_absent,
    ):
        ok, part = validator(data)
        if not ok:
            issues.extend(part)

    for flag in ("direct_action_allowed", "direct_speech_allowed", "direct_fact_write_allowed"):
        if data.get(flag) is True:
            issues.append(f"{flag}_must_be_false")

    return len(issues) == 0, issues


def validate_provider_runtime_decision(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, PROVIDER_RUNTIME_DECISION_FIELDS)
    for validator in (
        validate_candidate_only,
        validate_runtime_execution_allowed_false,
        validate_provider_activation_allowed_false,
        validate_fallback_execution_allowed_false,
        validate_output_dispatch_allowed_false,
        validate_domain_id_registered,
        validate_forbidden_policies_absent,
    ):
        ok, part = validator(data)
        if not ok:
            issues.extend(part)

    decision_type = data.get("decision_type")
    if decision_type and not is_registered("decision_types", decision_type):
        issues.append("decision_type_not_registered")

    return len(issues) == 0, issues


def validate_provider_runtime_skeleton_planning_decision(
    data: Dict[str, Any],
) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, PROVIDER_RUNTIME_SKELETON_PLANNING_DECISION_FIELDS)
    for validator in (
        validate_candidate_only,
        validate_runtime_execution_allowed_false,
        validate_provider_activation_allowed_false,
        validate_fallback_execution_allowed_false,
        validate_output_dispatch_allowed_false,
        validate_real_provider_connected_false,
        validate_shared_governance_source,
        validate_domain_profile_source,
        validate_forbidden_policies_absent,
    ):
        ok, part = validator(data)
        if not ok:
            issues.extend(part)

    if data.get("final_decision") != FINAL_DECISION_READY_FOR_DRYRUN_CASES:
        issues.append(f"final_decision_must_be_{FINAL_DECISION_READY_FOR_DRYRUN_CASES}")

    return len(issues) == 0, issues


def _registry_provider_refs_subset(
    registry: Dict[str, Any],
    domain_profiles: Dict[str, Any],
) -> Tuple[bool, List[str]]:
    domain_id = registry.get("domain_id")
    profile = domain_profiles.get(domain_id) or {}
    profile_refs = set(profile.get("provider_refs") or ())
    registry_refs = set(registry.get("provider_refs") or ())
    if not registry_refs.issubset(profile_refs):
        return False, [
            f"registry_provider_refs_not_from_domain_profile:{sorted(registry_refs - profile_refs)!r}"
        ]
    return True, []


def _no_cross_domain_pollution(matrix: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    domain_profiles = matrix.get("domain_profiles") or {}
    spatial_types = set(
        (domain_profiles.get(DOMAIN_SPATIAL_EVIDENCE) or {}).get(
            "supported_output_candidate_types"
        )
        or ()
    )
    vision_types = set(
        (domain_profiles.get(DOMAIN_VISION_OCR) or {}).get("supported_output_candidate_types")
        or ()
    )

    if spatial_types.intersection(_VISION_OCR_SIGNATURE_CANDIDATES):
        issues.append("spatial_profile_polluted_by_vision_ocr_candidates")
    if vision_types.intersection(_SPATIAL_POLLUTION_CANDIDATES):
        issues.append("vision_ocr_profile_polluted_by_spatial_candidates")

    for dispatch in matrix.get("output_dispatch_candidates") or ():
        domain_id = dispatch.get("domain_id")
        output_types = set(dispatch.get("output_candidate_types") or ())
        if domain_id == DOMAIN_SPATIAL_EVIDENCE:
            if dispatch.get("synthesis_entrypoint") != FIELD_SYNTHESIS_ENTRYPOINT:
                issues.append(
                    f"spatial_dispatch_wrong_synthesis:{dispatch.get('dispatch_ref')}"
                )
            if output_types.intersection(_VISION_OCR_SIGNATURE_CANDIDATES):
                issues.append(f"spatial_dispatch_vision_pollution:{dispatch.get('dispatch_ref')}")
        if domain_id == DOMAIN_VISION_OCR:
            if dispatch.get("synthesis_entrypoint") != MIDPLATFORM_SYNTHESIS_ENTRYPOINT:
                issues.append(
                    f"vision_ocr_dispatch_wrong_synthesis:{dispatch.get('dispatch_ref')}"
                )
            if output_types.intersection(_SPATIAL_POLLUTION_CANDIDATES):
                issues.append(f"vision_ocr_dispatch_spatial_pollution:{dispatch.get('dispatch_ref')}")

    return len(issues) == 0, issues


def _no_domain_specific_manager_duplication() -> bool:
    legacy_path = (
        _REPO_ROOT
        / "capabilities/field_understanding/spatial_evidence_provider_manager"
        / "field_spatial_evidence_provider_manager_types_v1.py"
    )
    if not legacy_path.is_file():
        return True
    return "SUPERSEDED_BY_SHARED_PROVIDER_RUNTIME_GOVERNANCE" in legacy_path.read_text(
        encoding="utf-8"
    )


def _registry_candidate_types_subset(
    registry: Dict[str, Any],
    domain_profiles: Dict[str, Any],
) -> Tuple[bool, List[str]]:
    domain_id = registry.get("domain_id")
    profile = domain_profiles.get(domain_id) or {}
    declared = set(profile.get("supported_output_candidate_types") or ())
    issues: List[str] = []
    for ctype in registry.get("supported_output_candidate_types") or ():
        if ctype not in declared:
            issues.append(f"candidate_not_in_domain_profile:{ctype}")
    return len(issues) == 0, issues


def _validate_provider_manager_runtime_skeleton_bundle_core(
    bundle: Dict[str, Any],
    *,
    validate_planning_final_decision: bool,
) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    domain_profiles = bundle.get("domain_profiles") or {}

    for idx, item in enumerate(bundle.get("runtime_skeletons") or ()):
        ok, part = validate_provider_manager_runtime_skeleton(item)
        if not ok:
            issues.extend([f"runtime_skeleton_{idx}:{i}" for i in part])

    for idx, item in enumerate(bundle.get("runtime_registries") or ()):
        ok, part = validate_runtime_provider_registry(item)
        if not ok:
            issues.extend([f"runtime_registry_{idx}:{i}" for i in part])
        subset_ok, subset_issues = _registry_provider_refs_subset(item, domain_profiles)
        if not subset_ok:
            issues.extend([f"runtime_registry_{idx}:{i}" for i in subset_issues])
        types_ok, types_issues = _registry_candidate_types_subset(item, domain_profiles)
        if not types_ok:
            issues.extend([f"runtime_registry_{idx}:{i}" for i in types_issues])

    for idx, item in enumerate(bundle.get("activation_gates") or ()):
        ok, part = validate_provider_activation_gate(item)
        if not ok:
            issues.extend([f"activation_gate_{idx}:{i}" for i in part])

    for idx, item in enumerate(bundle.get("health_loops") or ()):
        ok, part = validate_provider_runtime_health_loop(item)
        if not ok:
            issues.extend([f"health_loop_{idx}:{i}" for i in part])

    for idx, item in enumerate(bundle.get("fallback_executor_candidates") or ()):
        ok, part = validate_provider_fallback_executor_candidate(item)
        if not ok:
            issues.extend([f"fallback_executor_{idx}:{i}" for i in part])

    for idx, item in enumerate(bundle.get("output_dispatch_candidates") or ()):
        ok, part = validate_provider_output_dispatch_candidate(item)
        if not ok:
            issues.extend([f"output_dispatch_{idx}:{i}" for i in part])

    for idx, item in enumerate(bundle.get("runtime_decisions") or ()):
        ok, part = validate_provider_runtime_decision(item)
        if not ok:
            issues.extend([f"runtime_decision_{idx}:{i}" for i in part])

    if validate_planning_final_decision:
        for idx, item in enumerate(bundle.get("planning_decisions") or ()):
            ok, part = validate_provider_runtime_skeleton_planning_decision(item)
            if not ok:
                issues.extend([f"planning_decision_{idx}:{i}" for i in part])

    pollution_ok, pollution_issues = _no_cross_domain_pollution(
        {
            "domain_profiles": domain_profiles,
            "output_dispatch_candidates": bundle.get("output_dispatch_candidates") or (),
        }
    )
    if not pollution_ok:
        issues.extend(pollution_issues)

    return len(issues) == 0, issues


def validate_provider_manager_runtime_skeleton_case_bundle(
    bundle: Dict[str, Any],
) -> Tuple[bool, List[str]]:
    """Validate a single dry-run case bundle (shared by cases and runner)."""
    return _validate_provider_manager_runtime_skeleton_bundle_core(
        bundle,
        validate_planning_final_decision=False,
    )


def validate_provider_manager_runtime_skeleton_matrix_v1(
    matrix: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, List[str]]:
    matrix = matrix or build_provider_manager_runtime_skeleton_matrix_v1()
    issues: List[str] = []

    registry_ok, registry_issues = validate_registry()
    issues.extend(registry_issues)

    bundle = {
        "runtime_skeletons": [matrix.get("runtime_skeleton")] if matrix.get("runtime_skeleton") else [],
        "runtime_registries": matrix.get("runtime_registries") or [],
        "activation_gates": matrix.get("activation_gates") or [],
        "health_loops": matrix.get("health_loops") or [],
        "fallback_executor_candidates": matrix.get("fallback_executor_candidates") or [],
        "output_dispatch_candidates": matrix.get("output_dispatch_candidates") or [],
        "runtime_decisions": matrix.get("runtime_decisions") or [],
        "planning_decisions": [matrix.get("planning_decision")]
        if matrix.get("planning_decision")
        else [],
        "domain_profiles": matrix.get("domain_profiles") or {},
    }
    ok, core_issues = _validate_provider_manager_runtime_skeleton_bundle_core(
        bundle,
        validate_planning_final_decision=True,
    )
    issues.extend(core_issues)

    if not _no_domain_specific_manager_duplication():
        issues.append("domain_specific_manager_duplication_detected")

    return len(issues) == 0 and registry_ok, issues


def summarize_provider_manager_runtime_skeleton_planning_v1() -> Dict[str, Any]:
    import_ok = True
    try:
        from capabilities.midplatform.provider_manager_runtime_skeleton import (  # noqa: F401
            provider_manager_runtime_skeleton_registry_v1,
            provider_manager_runtime_skeleton_types_v1,
        )
        from capabilities.midplatform.provider_runtime_governance import (  # noqa: F401
            provider_runtime_governance_registry_v1,
        )
    except Exception:
        import_ok = False

    registry_ok, registry_issues = validate_registry()
    matrix = build_provider_manager_runtime_skeleton_matrix_v1()
    matrix_ok, matrix_issues = validate_provider_manager_runtime_skeleton_matrix_v1(matrix)

    skeleton = matrix.get("runtime_skeleton") or {}
    planning = matrix.get("planning_decision") or {}
    no_dup = _no_domain_specific_manager_duplication()

    candidate_only_enforced = all(
        item.get("candidate_only") is True
        for section in (
            "runtime_registries",
            "activation_gates",
            "health_loops",
            "fallback_executor_candidates",
            "output_dispatch_candidates",
            "runtime_decisions",
        )
        for item in matrix.get(section) or ()
    ) and skeleton.get("candidate_only") is True and planning.get("candidate_only") is True

    ready = (
        import_ok
        and registry_ok
        and matrix_ok
        and len(VALIDATOR_RULE_IDS) >= 24
        and skeleton.get("runtime_execution_allowed") is False
        and skeleton.get("provider_activation_allowed") is False
        and planning.get("fallback_execution_allowed") is False
        and planning.get("output_dispatch_allowed") is False
        and candidate_only_enforced
        and skeleton.get("shared_governance_source_ref") == SHARED_GOVERNANCE_SOURCE_REF
        and bool(skeleton.get("domain_profile_refs"))
        and no_dup
        and planning.get("final_decision") == FINAL_DECISION_READY_FOR_DRYRUN_CASES
    )

    return {
        "phase_id": PHASE_ID,
        "step": "Step 1 Provider Manager Runtime Skeleton Types / Registry / Validators",
        "runtime_skeleton_principle_zh": RUNTIME_SKELETON_PRINCIPLE_ZH,
        "inherited_principles_zh": [
            "能翻译，不等于能启用。",
            "能准入规划，不等于能 runtime enable。",
            "能定义 runtime skeleton，不等于能 runtime execute。",
        ],
        "import_ok": import_ok,
        "runtime_skeleton_count": 1 if skeleton else 0,
        "runtime_registry_count": len(matrix.get("runtime_registries") or ()),
        "activation_gate_count": len(matrix.get("activation_gates") or ()),
        "health_loop_count": len(matrix.get("health_loops") or ()),
        "fallback_executor_candidate_count": len(
            matrix.get("fallback_executor_candidates") or ()
        ),
        "output_dispatch_candidate_count": len(
            matrix.get("output_dispatch_candidates") or ()
        ),
        "runtime_decision_count": len(matrix.get("runtime_decisions") or ()),
        "validator_rules": len(VALIDATOR_RULE_IDS),
        "activation_gate_required_checks": list(TYPE_ACTIVATION_GATES),
        "control_chain": matrix.get("control_chain") or [],
        "registry_ok": registry_ok,
        "registry_issues": registry_issues,
        "matrix_ok": matrix_ok,
        "matrix_issues": matrix_issues,
        "runtime_execution_allowed": skeleton.get("runtime_execution_allowed"),
        "provider_activation_allowed": skeleton.get("provider_activation_allowed"),
        "fallback_execution_allowed": planning.get("fallback_execution_allowed"),
        "output_dispatch_allowed": planning.get("output_dispatch_allowed"),
        "candidate_only_enforced": candidate_only_enforced,
        "shared_governance_source_required": skeleton.get("shared_governance_source_ref")
        == SHARED_GOVERNANCE_SOURCE_REF,
        "domain_profile_source_required": bool(skeleton.get("domain_profile_refs")),
        "no_domain_specific_manager_duplication": no_dup,
        "domain_profiles_attached": list((matrix.get("domain_profiles") or {}).keys()),
        "final_decision": (
            FINAL_DECISION_READY_FOR_DRYRUN_CASES
            if ready
            else "PROVIDER_MANAGER_RUNTIME_SKELETON_PLANNING_NOT_READY"
        ),
    }


def main() -> int:
    summary = summarize_provider_manager_runtime_skeleton_planning_v1()
    print(json.dumps(summary, ensure_ascii=False))
    return 0 if summary["final_decision"] == FINAL_DECISION_READY_FOR_DRYRUN_CASES else 1


if __name__ == "__main__":
    raise SystemExit(main())
