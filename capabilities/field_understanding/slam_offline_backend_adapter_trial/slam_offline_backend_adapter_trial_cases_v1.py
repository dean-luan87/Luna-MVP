# -*- coding: utf-8 -*-
"""SLAM Offline Backend Adapter Trial — offline stub cases v1 (compressed)."""

from __future__ import annotations

import copy
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.slam_offline_backend_adapter_trial.slam_offline_backend_adapter_trial_registry_v1 import (
    build_slam_offline_backend_adapter_trial_matrix_v1,
)
from capabilities.field_understanding.slam_offline_backend_adapter_trial.slam_offline_backend_adapter_trial_static_validators_v1 import (
    validate_slam_offline_backend_adapter_trial_case_bundle,
)
from capabilities.field_understanding.slam_offline_backend_adapter_trial.slam_offline_backend_adapter_trial_types_v1 import (
    ADAPTER_PROFILE_REF,
    FIELD_SYNTHESIS_ENTRYPOINT,
    FINAL_DECISION_CASES_READY_FOR_RUNNER,
    MODEL_ADMISSION_STANDARD_REF,
    OFFLINE_BACKEND_FORMAT_STUBS,
    PHASE_ID,
    TRIAL_PRINCIPLE_ZH,
)

POSITIVE_STUB_CASES: Tuple[Tuple[str, str, str], ...] = (
    (
        "case_01_rtab_map_export_stub",
        "rtab_map_export_stub",
        "Validate RTAB-Map export stub offline parse → adapter mapping entrypoint.",
    ),
    (
        "case_02_kimera_export_stub",
        "kimera_export_stub",
        "Validate Kimera export stub offline parse → adapter mapping entrypoint.",
    ),
    (
        "case_03_hydra_scene_graph_stub",
        "hydra_scene_graph_stub",
        "Validate Hydra scene graph stub offline parse → adapter mapping entrypoint.",
    ),
    (
        "case_04_orb_slam3_trajectory_stub",
        "orb_slam3_trajectory_stub",
        "Validate ORB-SLAM3 trajectory stub (GPL technical_reference_only) offline chain.",
    ),
    (
        "case_05_openvins_trajectory_stub",
        "openvins_trajectory_stub",
        "Validate OpenVINS trajectory stub (GPL technical_reference_only) offline chain.",
    ),
    (
        "case_06_generic_tum_trajectory_stub",
        "generic_tum_trajectory_stub",
        "Validate generic TUM trajectory stub offline parse → adapter mapping entrypoint.",
    ),
    (
        "case_07_generic_json_spatial_trace_stub",
        "generic_json_spatial_trace_stub",
        "Validate generic JSON spatial trace stub offline parse → adapter mapping entrypoint.",
    ),
)


@dataclass(frozen=True)
class OfflineSLAMBackendAdapterTrialCase:
    case_id: str
    case_name: str
    case_type: str
    case_goal: str
    backend_format_stub: str
    offline_backend_output_file: Dict[str, Any]
    offline_backend_output_parser: Dict[str, Any]
    adapter_trial_config: Dict[str, Any]
    parsed_evidence_bundle: Dict[str, Any]
    expected_validation_ok: bool = True


def _matrix() -> Dict[str, Any]:
    return build_slam_offline_backend_adapter_trial_matrix_v1()


def _by_stub(items: List[Dict[str, Any]], stub: str, key: str = "backend_format_stub") -> Dict[str, Any]:
    return next(item for item in items if item.get(key) == stub)


def _by_ref(items: List[Dict[str, Any]], ref: str, key: str) -> Dict[str, Any]:
    return next(item for item in items if item.get(key) == ref)


def _trial_parts_for_stub(matrix: Dict[str, Any], backend_format_stub: str) -> Dict[str, Dict[str, Any]]:
    return {
        "offline_backend_output_file": _by_ref(
            matrix.get("offline_backend_output_files") or [],
            f"offline_file_{backend_format_stub}",
            "file_ref",
        ),
        "offline_backend_output_parser": _by_ref(
            matrix.get("offline_backend_output_parsers") or [],
            f"parser_{backend_format_stub}",
            "parser_ref",
        ),
        "adapter_trial_config": _by_ref(
            matrix.get("adapter_trial_configs") or [],
            f"config_{backend_format_stub}",
            "config_ref",
        ),
        "parsed_evidence_bundle": _by_ref(
            matrix.get("parsed_evidence_bundles") or [],
            f"parsed_bundle_{backend_format_stub}",
            "bundle_ref",
        ),
    }


def _positive_case(
    *,
    case_id: str,
    backend_format_stub: str,
    case_goal: str,
) -> OfflineSLAMBackendAdapterTrialCase:
    parts = _trial_parts_for_stub(_matrix(), backend_format_stub)
    return OfflineSLAMBackendAdapterTrialCase(
        case_id=case_id,
        case_name=backend_format_stub,
        case_type="positive",
        case_goal=case_goal,
        backend_format_stub=backend_format_stub,
        offline_backend_output_file=parts["offline_backend_output_file"],
        offline_backend_output_parser=parts["offline_backend_output_parser"],
        adapter_trial_config=parts["adapter_trial_config"],
        parsed_evidence_bundle=parts["parsed_evidence_bundle"],
        expected_validation_ok=True,
    )


def build_positive_trial_cases_v1() -> Tuple[OfflineSLAMBackendAdapterTrialCase, ...]:
    return tuple(
        _positive_case(case_id=case_id, backend_format_stub=stub, case_goal=goal)
        for case_id, stub, goal in POSITIVE_STUB_CASES
    )


def _invalid_from_positive(
    *,
    case_id: str,
    case_name: str,
    case_goal: str,
    backend_format_stub: str,
    mutate,
) -> OfflineSLAMBackendAdapterTrialCase:
    base = _positive_case(
        case_id=case_id,
        backend_format_stub=backend_format_stub,
        case_goal=case_goal,
    )
    mutated = mutate(
        {
            "offline_backend_output_file": copy.deepcopy(base.offline_backend_output_file),
            "offline_backend_output_parser": copy.deepcopy(base.offline_backend_output_parser),
            "adapter_trial_config": copy.deepcopy(base.adapter_trial_config),
            "parsed_evidence_bundle": copy.deepcopy(base.parsed_evidence_bundle),
        }
    )
    return OfflineSLAMBackendAdapterTrialCase(
        case_id=case_id,
        case_name=case_name,
        case_type="invalid",
        case_goal=case_goal,
        backend_format_stub=backend_format_stub,
        offline_backend_output_file=mutated["offline_backend_output_file"],
        offline_backend_output_parser=mutated["offline_backend_output_parser"],
        adapter_trial_config=mutated["adapter_trial_config"],
        parsed_evidence_bundle=mutated["parsed_evidence_bundle"],
        expected_validation_ok=False,
    )


def build_invalid_trial_cases_v1() -> Tuple[OfflineSLAMBackendAdapterTrialCase, ...]:
    def mutate_missing_source_chain(parts: Dict[str, Any]) -> Dict[str, Any]:
        parts["offline_backend_output_file"]["source_chain"] = ()
        return parts

    def mutate_adapter_profile_bypass(parts: Dict[str, Any]) -> Dict[str, Any]:
        parts["adapter_trial_config"]["adapter_profile_ref"] = "bypass_adapter_profile"
        return parts

    def mutate_synthesis_bypass(parts: Dict[str, Any]) -> Dict[str, Any]:
        parts["parsed_evidence_bundle"]["field_synthesis_entrypoint"] = "midplatform_synthesis_v1"
        return parts

    def mutate_gpl_commercial_runtime(parts: Dict[str, Any]) -> Dict[str, Any]:
        parts["offline_backend_output_file"]["commercial_runtime_candidate"] = True
        return parts

    return (
        _invalid_from_positive(
            case_id="invalid_trial_a_missing_source_chain",
            case_name="offline file missing source_chain",
            case_goal="Reject offline backend output file when source_chain is missing.",
            backend_format_stub="generic_tum_trajectory_stub",
            mutate=mutate_missing_source_chain,
        ),
        _invalid_from_positive(
            case_id="invalid_trial_b_adapter_profile_bypass",
            case_name="parser chain bypasses adapter_profile",
            case_goal="Reject trial config when adapter_profile bypasses slam_spatial_evidence_adapter.",
            backend_format_stub="generic_tum_trajectory_stub",
            mutate=mutate_adapter_profile_bypass,
        ),
        _invalid_from_positive(
            case_id="invalid_trial_c_field_synthesis_bypass",
            case_name="parsed bundle bypasses field_synthesis_v1",
            case_goal="Reject parsed evidence bundle when synthesis entrypoint bypasses field_synthesis_v1.",
            backend_format_stub="generic_tum_trajectory_stub",
            mutate=mutate_synthesis_bypass,
        ),
        _invalid_from_positive(
            case_id="invalid_trial_d_gpl_commercial_runtime_candidate",
            case_name="GPL stub marked commercial_runtime_candidate",
            case_goal=(
                "Reject GPL technical_reference_only backend when "
                "commercial_runtime_candidate=true."
            ),
            backend_format_stub="openvins_trajectory_stub",
            mutate=mutate_gpl_commercial_runtime,
        ),
    )


def build_all_trial_cases_v1() -> Tuple[OfflineSLAMBackendAdapterTrialCase, ...]:
    return build_positive_trial_cases_v1() + build_invalid_trial_cases_v1()


def bundle_from_slam_offline_backend_adapter_trial_case(
    case: OfflineSLAMBackendAdapterTrialCase,
) -> Dict[str, Any]:
    return {
        "case_id": case.case_id,
        "case_type": case.case_type,
        "backend_format_stub": case.backend_format_stub,
        "offline_backend_output_file": case.offline_backend_output_file,
        "offline_backend_output_parser": case.offline_backend_output_parser,
        "adapter_trial_config": case.adapter_trial_config,
        "parsed_evidence_bundle": case.parsed_evidence_bundle,
    }


def _validate_case(case: OfflineSLAMBackendAdapterTrialCase) -> Tuple[bool, List[str]]:
    return validate_slam_offline_backend_adapter_trial_case_bundle(
        bundle_from_slam_offline_backend_adapter_trial_case(case)
    )


def _check_cases(
    cases: Tuple[OfflineSLAMBackendAdapterTrialCase, ...],
    *,
    expect_valid: bool,
) -> Tuple[int, List[str]]:
    ok_count = 0
    mismatches: List[str] = []
    for case in cases:
        valid, issues = _validate_case(case)
        if valid == expect_valid:
            ok_count += 1
        else:
            mismatches.append(
                f"{case.case_id}:expected_valid={expect_valid}:actual_valid={valid}:issues={issues}"
            )
    return ok_count, mismatches


def summarize_slam_offline_backend_adapter_trial_cases_v1() -> Dict[str, Any]:
    positive = build_positive_trial_cases_v1()
    invalid = build_invalid_trial_cases_v1()
    all_cases = build_all_trial_cases_v1()

    case_ids = [case.case_id for case in all_cases]
    unique_ok = len(case_ids) == len(set(case_ids))
    pos_ok, pos_mismatches = _check_cases(positive, expect_valid=True)
    inv_ok, inv_mismatches = _check_cases(invalid, expect_valid=False)

    sample_positive_ok = False
    sample_invalid_rejected = False
    if positive:
        sample_positive_ok, _ = _validate_case(positive[0])
    if invalid:
        invalid_ok, _ = _validate_case(invalid[0])
        sample_invalid_rejected = not invalid_ok

    positive_stubs = {case.backend_format_stub for case in positive}
    stubs_cover_matrix = positive_stubs == set(OFFLINE_BACKEND_FORMAT_STUBS)

    ready = (
        len(positive) == 7
        and len(invalid) == 4
        and len(all_cases) == 11
        and unique_ok
        and stubs_cover_matrix
        and pos_ok == len(positive)
        and inv_ok == len(invalid)
        and not pos_mismatches
        and not inv_mismatches
        and sample_positive_ok
        and sample_invalid_rejected
    )

    return {
        "phase_id": PHASE_ID,
        "step": "Step 2 Offline Backend Adapter Trial Cases",
        "trial_principle_zh": TRIAL_PRINCIPLE_ZH,
        "positive_case_count": len(positive),
        "invalid_case_count": len(invalid),
        "case_count": len(all_cases),
        "positive_case_ids": [case.case_id for case in positive],
        "invalid_case_ids": [case.case_id for case in invalid],
        "case_ids_unique": unique_ok,
        "sample_positive_validate_ok": sample_positive_ok,
        "sample_invalid_rejected_ok": sample_invalid_rejected,
        "positive_validation_mismatches": pos_mismatches,
        "invalid_validation_mismatches": inv_mismatches,
        "offline_only": True,
        "model_admission_standard_ref_required": True,
        "adapter_profile_required": ADAPTER_PROFILE_REF,
        "field_synthesis_entrypoint_locked": FIELD_SYNTHESIS_ENTRYPOINT,
        "source_chain_required": True,
        "commercial_runtime_approved": False,
        "final_decision": (
            FINAL_DECISION_CASES_READY_FOR_RUNNER
            if ready
            else "SLAM_OFFLINE_BACKEND_ADAPTER_TRIAL_CASES_NOT_READY"
        ),
    }


def main() -> int:
    summary = summarize_slam_offline_backend_adapter_trial_cases_v1()
    print(json.dumps(summary, ensure_ascii=False))
    return (
        0
        if summary["final_decision"] == FINAL_DECISION_CASES_READY_FOR_RUNNER
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
