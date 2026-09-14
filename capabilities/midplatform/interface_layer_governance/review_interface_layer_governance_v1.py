# -*- coding: utf-8 -*-
"""Interface Layer Governance Protocol — baseline matrix + review (compressed)."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.midplatform.interface_layer_governance.interface_layer_governance_registry_v1 import (
    INTERFACE_PROFILE_TO_STANDARD,
    REGISTRY_ID,
    build_interface_layer_governance_baseline_matrix_v1,
    validate_registry,
)
from capabilities.midplatform.interface_layer_governance.interface_layer_governance_types_v1 import (
    ACTIVE_INTERNAL_STANDARD_REFS,
    CLASSIFICATION,
    CORE_INTERFACE_GOVERNANCE_RULES,
    FIELD_SYNTHESIS_ENTRYPOINT,
    FINAL_DECISION_BASELINE_READY,
    FINAL_DECISION_REVIEW_BLOCKED,
    INTERFACE_GOVERNANCE_PRINCIPLE_ZH,
    INTERFACE_PROFILE_REFS,
    MODEL_ADMISSION_STANDARD_REF,
    MODEL_MANAGEMENT_PROTOCOL_REF,
    NON_EXECUTION_FLAGS,
    PLANNING_OBJECT_TYPES,
    PLANNED_INTERNAL_STANDARD_REFS,
    PROTOCOL_ID,
    PROTOCOL_NAME,
    SHARED_INGEST_CHAIN,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT / "_tmp_eval_out" / "interface_layer_governance_v1_smoke_v0"
)
REVIEW_FILENAME = "interface_layer_governance_review_v1.json"

FINAL_DECISION_GO = FINAL_DECISION_BASELINE_READY

STEP_FILES = (
    "capabilities/midplatform/interface_layer_governance/interface_layer_governance_types_v1.py",
    "capabilities/midplatform/interface_layer_governance/interface_layer_governance_registry_v1.py",
    "capabilities/midplatform/interface_layer_governance/review_interface_layer_governance_v1.py",
)

SEALED_SPATIAL_PARSER_PATH = (
    "capabilities/field_understanding/generic_json_spatial_trace_parser/"
    "generic_json_spatial_trace_parser_types_v1.py"
)


def validate_baseline_matrix_v1(
    matrix: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, List[str]]:
    matrix = matrix or build_interface_layer_governance_baseline_matrix_v1()
    issues: List[str] = []

    registry_ok, registry_issues = validate_registry()
    issues.extend(registry_issues)

    standard = matrix.get("external_backend_interface_standard") or {}
    if standard.get("protocol_id") != PROTOCOL_ID:
        issues.append("external_standard.protocol_id_mismatch")
    if standard.get("model_management_protocol_ref") != MODEL_MANAGEMENT_PROTOCOL_REF:
        issues.append("external_standard.model_management_protocol_ref_mismatch")
    if tuple(standard.get("core_rules") or ()) != CORE_INTERFACE_GOVERNANCE_RULES:
        issues.append("external_standard.core_rules_mismatch")
    if list(standard.get("ingest_chain") or []) != list(SHARED_INGEST_CHAIN):
        issues.append("external_standard.ingest_chain_mismatch")

    adapters = matrix.get("interface_adapter_profiles") or []
    if len(adapters) != 5:
        issues.append(f"interface_adapter_profile_count:{len(adapters)}")

    internal_standards = matrix.get("internal_standard_format_refs") or []
    if len(internal_standards) != 5:
        issues.append(f"internal_standard_format_ref_count:{len(internal_standards)}")

    mappings = matrix.get("candidate_schema_mapping_refs") or []
    if len(mappings) != 5:
        issues.append(f"candidate_schema_mapping_ref_count:{len(mappings)}")

    if not matrix.get("interface_admission_policy"):
        issues.append("interface_admission_policy_missing")
    if not matrix.get("interface_lifecycle_decision"):
        issues.append("interface_lifecycle_decision_missing")

    active_formats = {
        item.get("format_ref")
        for item in internal_standards
        if item.get("format_status") == "active_sealed_baseline"
    }
    if active_formats != {"generic_json_spatial_trace"}:
        issues.append(f"active_internal_standard_refs_mismatch:{sorted(active_formats)!r}")

    slam_adapter = next(
        (a for a in adapters if a.get("adapter_profile_ref") == "slam_spatial_evidence_adapter"),
        None,
    )
    if not slam_adapter:
        issues.append("slam_spatial_evidence_adapter_missing")
    elif slam_adapter.get("internal_standard_format_ref") != "generic_json_spatial_trace":
        issues.append("slam_adapter_internal_standard_not_generic_json")

    policy = matrix.get("interface_admission_policy") or {}
    if policy.get("direct_main_chain_write_forbidden") is not True:
        issues.append("policy.direct_main_chain_write_not_forbidden")
    if policy.get("private_ingest_entrypoint_forbidden") is not True:
        issues.append("policy.private_ingest_entrypoint_not_forbidden")
    if policy.get("version_lineage_required") is not True:
        issues.append("policy.version_lineage_not_required")

    decision = matrix.get("interface_lifecycle_decision") or {}
    if decision.get("sealed_spatial_evidence_standard") != "generic_json_spatial_trace":
        issues.append("decision.sealed_spatial_evidence_standard_mismatch")
    if decision.get("architecture_principle_locked") is not True:
        issues.append("decision.architecture_principle_not_locked")
    if decision.get("final_decision") != FINAL_DECISION_BASELINE_READY:
        issues.append("decision.final_decision_not_ready")

    for profile_ref, format_ref in INTERFACE_PROFILE_TO_STANDARD.items():
        adapter_match = any(a.get("interface_profile_ref") == profile_ref for a in adapters)
        standard_match = any(s.get("interface_profile_ref") == profile_ref for s in internal_standards)
        if not adapter_match or not standard_match:
            issues.append(f"interface_profile_incomplete:{profile_ref}")
        if standard_match:
            std = next(s for s in internal_standards if s.get("interface_profile_ref") == profile_ref)
            if std.get("format_ref") != format_ref:
                issues.append(f"interface_profile_standard_mismatch:{profile_ref}")

    return len(issues) == 0 and registry_ok, issues


def review_protocol_relationship(matrix: Dict[str, Any]) -> Tuple[Dict[str, bool], List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    standard = matrix.get("external_backend_interface_standard") or {}
    policy = matrix.get("interface_admission_policy") or {}
    decision = matrix.get("interface_lifecycle_decision") or {}

    checks = {
        "model_management_protocol_bound": standard.get("model_management_protocol_ref")
        == MODEL_MANAGEMENT_PROTOCOL_REF,
        "model_admission_standard_ref_present": matrix.get("model_admission_standard_ref")
        == MODEL_ADMISSION_STANDARD_REF,
        "provider_governance_bound": policy.get("provider_governance_ref") is not None,
        "ingest_chain_declared": list(standard.get("ingest_chain") or []) == list(SHARED_INGEST_CHAIN),
        "generic_json_spatial_trace_elevated": decision.get("sealed_spatial_evidence_standard")
        == "generic_json_spatial_trace",
        "no_direct_main_chain_write": policy.get("direct_main_chain_write_forbidden") is True,
        "no_private_ingest_entrypoint": policy.get("private_ingest_entrypoint_forbidden") is True,
    }

    for key, ok in checks.items():
        if ok:
            passed.append(f"protocol_relationship.{key}=true")
        else:
            failed.append(f"protocol_relationship.{key}=false")

    return checks, passed, failed


def review_core_rules(matrix: Dict[str, Any]) -> Tuple[Dict[str, bool], List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    standard = matrix.get("external_backend_interface_standard") or {}
    rules = tuple(standard.get("core_rules") or ())

    checks = {rule: rule in rules for rule in CORE_INTERFACE_GOVERNANCE_RULES}
    checks["core_rules_count_is_8"] = len(rules) == 8

    for key, ok in checks.items():
        if ok:
            passed.append(f"core_rules.{key}=true")
        else:
            failed.append(f"core_rules.{key}=false")

    return checks, passed, failed


def review_sealed_spatial_baseline() -> Tuple[Dict[str, bool], List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    parser_path = _REPO_ROOT / SEALED_SPATIAL_PARSER_PATH
    parser_exists = parser_path.is_file()

    checks = {
        "generic_json_spatial_trace_parser_module_present": parser_exists,
        "spatial_evidence_active_only_one_standard": len(ACTIVE_INTERNAL_STANDARD_REFS) == 1,
        "planned_standards_not_active": "generic_json_spatial_trace" not in PLANNED_INTERNAL_STANDARD_REFS,
    }

    for key, ok in checks.items():
        if ok:
            passed.append(f"sealed_baseline.{key}=true")
        else:
            failed.append(f"sealed_baseline.{key}=false")

    return checks, passed, failed


def review_non_execution_boundary() -> Tuple[Dict[str, bool], List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    flags = dict(NON_EXECUTION_FLAGS)
    boundary = {
        "protocol_baseline_planning_only": flags.get("protocol_baseline_planning_only") is True,
        "no_runtime_activation": flags.get("no_runtime_activation") is True,
        "no_provider_runtime_activation": flags.get("no_provider_runtime_activation") is True,
        "no_commercial_runtime_approval": flags.get("no_commercial_runtime_approval") is True,
        "no_direct_main_chain_write": flags.get("no_direct_main_chain_write") is True,
        "no_per_model_private_ingest_entrypoint": flags.get("no_per_model_private_ingest_entrypoint") is True,
    }

    for key, ok in boundary.items():
        if ok:
            passed.append(f"boundary.{key}=true")
        else:
            failed.append(f"boundary.{key}=false")

    return boundary, passed, failed


def review_interface_layer_governance_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
) -> Dict[str, Any]:
    matrix = build_interface_layer_governance_baseline_matrix_v1()
    matrix_ok, matrix_issues = validate_baseline_matrix_v1(matrix)
    registry_ok, registry_issues = validate_registry()

    all_passed: List[str] = []
    all_failed: List[str] = []

    for rel in STEP_FILES:
        if (_REPO_ROOT / rel).is_file():
            all_passed.append(f"step.file_present={rel.split('/')[-1]}")
        else:
            all_failed.append(f"step.file_missing={rel}")

    if matrix_ok:
        all_passed.append("matrix_validation_ok=true")
    else:
        all_failed.extend(matrix_issues)

    if registry_ok:
        all_passed.append("registry_validation_ok=true")
    else:
        all_failed.extend(registry_issues)

    protocol_review, p, f = review_protocol_relationship(matrix)
    all_passed.extend(p)
    all_failed.extend(f)

    core_rules_review, p, f = review_core_rules(matrix)
    all_passed.extend(p)
    all_failed.extend(f)

    sealed_review, p, f = review_sealed_spatial_baseline()
    all_passed.extend(p)
    all_failed.extend(f)

    boundary_review, p, f = review_non_execution_boundary()
    all_passed.extend(p)
    all_failed.extend(f)

    blocker_count = len(all_failed)
    decision = matrix.get("interface_lifecycle_decision") or {}
    review_ok = (
        matrix_ok
        and registry_ok
        and all(protocol_review.values())
        and all(core_rules_review.values())
        and all(sealed_review.values())
        and all(boundary_review.values())
        and blocker_count == 0
    )

    result: Dict[str, Any] = {
        "phase_id": "Phase-Midplatform-Interface-Layer-Governance-Protocol-v1-001",
        "step": "Interface Layer Governance Protocol Baseline Matrix + Review",
        "lifecycle_variant": "compressed_protocol_baseline_review",
        "classification": CLASSIFICATION,
        "interface_governance_principle_zh": INTERFACE_GOVERNANCE_PRINCIPLE_ZH,
        "protocol_id": PROTOCOL_ID,
        "protocol_name": PROTOCOL_NAME,
        "registry_id": REGISTRY_ID,
        "matrix_review_ok": matrix_ok,
        "planning_object_types": list(PLANNING_OBJECT_TYPES),
        "interface_profile_refs": list(INTERFACE_PROFILE_REFS),
        "shared_ingest_chain": list(SHARED_INGEST_CHAIN),
        "core_interface_governance_rules": list(CORE_INTERFACE_GOVERNANCE_RULES),
        "protocol_relationship_review": protocol_review,
        "core_rules_review": core_rules_review,
        "sealed_baseline_review": sealed_review,
        "boundary_review": boundary_review,
        "baseline_matrix": matrix,
        "conclusions": {
            "model_management_protocol_role": "model identity and lifecycle governance",
            "interface_layer_protocol_role": "external capability ingest and main-chain entry governance",
            "active_internal_standard_refs": list(ACTIVE_INTERNAL_STANDARD_REFS),
            "planned_internal_standard_refs": list(PLANNED_INTERNAL_STANDARD_REFS),
            "sealed_spatial_evidence_standard": decision.get("sealed_spatial_evidence_standard"),
            "spatial_evidence_interface_profile": "spatial_evidence_ingest_interface",
            "field_synthesis_entrypoint_locked": FIELD_SYNTHESIS_ENTRYPOINT,
            "next_step_hint": (
                "Adopt interface profiles under L1; continue RTAB-Map P0 subset fixture "
                "through generic_json_spatial_trace ingest chain"
            ),
        },
        "blocker_count": blocker_count,
        "failed_checks": all_failed,
        "passed_checks": all_passed,
        "final_decision": FINAL_DECISION_GO if review_ok else FINAL_DECISION_REVIEW_BLOCKED,
    }

    if write_file:
        out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
        out_root.mkdir(parents=True, exist_ok=True)
        out_path = out_root / REVIEW_FILENAME
        out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        result["output_review_file"] = str(out_path)

    return result


def main() -> int:
    result = review_interface_layer_governance_v1()
    print(
        json.dumps(
            {
                "matrix_review_ok": result["matrix_review_ok"],
                "protocol_id": result["protocol_id"],
                "planning_object_type_count": len(result["planning_object_types"]),
                "interface_profile_count": len(result["interface_profile_refs"]),
                "core_rules_count": len(result["core_interface_governance_rules"]),
                "active_internal_standard_refs": result["conclusions"]["active_internal_standard_refs"],
                "sealed_spatial_evidence_standard": result["conclusions"]["sealed_spatial_evidence_standard"],
                "blocker_count": result["blocker_count"],
                "output_review_file": result.get("output_review_file"),
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
