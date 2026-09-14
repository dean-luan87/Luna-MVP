# -*- coding: utf-8 -*-
"""SLAM Spatial Evidence Adapter — mapping delta cases v1 (compressed)."""

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

from capabilities.field_understanding.slam_spatial_evidence_adapter.slam_spatial_evidence_adapter_registry_v1 import (
    build_slam_spatial_evidence_adapter_matrix_v1,
)
from capabilities.field_understanding.slam_spatial_evidence_adapter.slam_spatial_evidence_adapter_static_validators_v1 import (
    validate_slam_spatial_evidence_adapter_mapping_case_bundle,
)
from capabilities.field_understanding.slam_spatial_evidence_adapter.slam_spatial_evidence_adapter_types_v1 import (
    ADAPTER_SKELETON_PRINCIPLE_ZH,
    FIELD_SYNTHESIS_ENTRYPOINT,
    FINAL_DECISION_MAPPING_CASES_READY_FOR_RUNNER,
    PHASE_ID,
)

POSITIVE_ADAPTER_REFS: Tuple[str, ...] = (
    "adapter_mock_vio_pose_motion",
    "adapter_mock_visual_slam_anchor_localmap",
    "adapter_mock_rgbd_localmap_health",
    "adapter_mock_metric_semantic_anchor_graph",
    "adapter_mock_scene_graph_field_structure",
)


@dataclass(frozen=True)
class SLAMSpatialEvidenceAdapterMappingCase:
    case_id: str
    case_name: str
    case_type: str
    case_goal: str
    adapter_ref: str
    backend_kind: str
    expected_candidate_types: Tuple[str, ...]
    mock_backend_outputs: Tuple[Dict[str, Any], ...]
    backend_output_frames: Tuple[Dict[str, Any], ...]
    input_envelopes: Tuple[Dict[str, Any], ...]
    mapping_rules: Tuple[Dict[str, Any], ...]
    adapters: Tuple[Dict[str, Any], ...]
    output_bundles: Tuple[Dict[str, Any], ...]
    health_reports: Tuple[Dict[str, Any], ...]
    expected_validation_ok: bool = True


def _matrix() -> Dict[str, Any]:
    return build_slam_spatial_evidence_adapter_matrix_v1()


def _by_adapter_ref(items: List[Dict[str, Any]], adapter_ref: str) -> List[Dict[str, Any]]:
    return [item for item in items if item.get("adapter_ref") == adapter_ref]


def _backend_output_for_adapter(matrix: Dict[str, Any], adapter_ref: str) -> Dict[str, Any]:
    bundle = next(
        item for item in matrix.get("output_bundles") or () if item.get("adapter_ref") == adapter_ref
    )
    backend_ref = bundle["source_chain"][1]
    return next(
        item for item in matrix.get("mock_backend_outputs") or () if item.get("backend_ref") == backend_ref
    )


def _backend_frame_for_adapter(matrix: Dict[str, Any], adapter_ref: str) -> Dict[str, Any]:
    bundle = next(
        item for item in matrix.get("output_bundles") or () if item.get("adapter_ref") == adapter_ref
    )
    frame_ref = bundle["source_chain"][-1]
    return next(
        item for item in matrix.get("backend_output_frames") or () if item.get("frame_ref") == frame_ref
    )


def _mapping_bundle_for_adapter(
    matrix: Dict[str, Any],
    adapter_ref: str,
) -> Dict[str, Tuple[Dict[str, Any], ...]]:
    return {
        "mock_backend_outputs": (
            _backend_output_for_adapter(matrix, adapter_ref),
        ),
        "backend_output_frames": (
            _backend_frame_for_adapter(matrix, adapter_ref),
        ),
        "input_envelopes": tuple(_by_adapter_ref(matrix.get("input_envelopes") or [], adapter_ref)),
        "mapping_rules": tuple(_by_adapter_ref(matrix.get("mapping_rules") or [], adapter_ref)),
        "adapters": tuple(_by_adapter_ref(matrix.get("adapters") or [], adapter_ref)),
        "output_bundles": tuple(_by_adapter_ref(matrix.get("output_bundles") or [], adapter_ref)),
        "health_reports": tuple(_by_adapter_ref(matrix.get("health_reports") or [], adapter_ref)),
    }


def _positive_case(
    *,
    case_id: str,
    case_name: str,
    case_goal: str,
    adapter_ref: str,
    backend_kind: str,
    expected_candidate_types: Tuple[str, ...],
) -> SLAMSpatialEvidenceAdapterMappingCase:
    parts = _mapping_bundle_for_adapter(_matrix(), adapter_ref)
    return SLAMSpatialEvidenceAdapterMappingCase(
        case_id=case_id,
        case_name=case_name,
        case_type="positive",
        case_goal=case_goal,
        adapter_ref=adapter_ref,
        backend_kind=backend_kind,
        expected_candidate_types=expected_candidate_types,
        mock_backend_outputs=parts["mock_backend_outputs"],
        backend_output_frames=parts["backend_output_frames"],
        input_envelopes=parts["input_envelopes"],
        mapping_rules=parts["mapping_rules"],
        adapters=parts["adapters"],
        output_bundles=parts["output_bundles"],
        health_reports=parts["health_reports"],
        expected_validation_ok=True,
    )


def build_positive_mapping_cases_v1() -> Tuple[SLAMSpatialEvidenceAdapterMappingCase, ...]:
    return (
        _positive_case(
            case_id="case_mapping_01_mock_vio_pose_motion",
            case_name="mock_vio pose + motion mapping",
            case_goal="Validate mock_vio backend maps to PoseCandidate + MotionCandidate.",
            adapter_ref="adapter_mock_vio_pose_motion",
            backend_kind="mock_vio",
            expected_candidate_types=("PoseCandidate", "MotionCandidate"),
        ),
        _positive_case(
            case_id="case_mapping_02_mock_visual_slam_anchor_localmap",
            case_name="mock_visual_slam anchor + localmap mapping",
            case_goal=(
                "Validate mock_visual_slam backend maps to SpatialAnchorCandidate + "
                "LocalMapCandidate."
            ),
            adapter_ref="adapter_mock_visual_slam_anchor_localmap",
            backend_kind="mock_visual_slam",
            expected_candidate_types=("SpatialAnchorCandidate", "LocalMapCandidate"),
        ),
        _positive_case(
            case_id="case_mapping_03_mock_rgbd_localmap_health",
            case_name="mock_rgbd_slam localmap + health mapping",
            case_goal=(
                "Validate mock_rgbd_slam backend maps to LocalMapCandidate + SLAMHealthCandidate."
            ),
            adapter_ref="adapter_mock_rgbd_localmap_health",
            backend_kind="mock_rgbd_slam",
            expected_candidate_types=("LocalMapCandidate", "SLAMHealthCandidate"),
        ),
        _positive_case(
            case_id="case_mapping_04_mock_metric_semantic_anchor_graph",
            case_name="mock_metric_semantic anchor + semantic placeholder mapping",
            case_goal=(
                "Validate mock_metric_semantic_slam maps to SpatialAnchorCandidate + "
                "semantic placeholder."
            ),
            adapter_ref="adapter_mock_metric_semantic_anchor_graph",
            backend_kind="mock_metric_semantic_slam",
            expected_candidate_types=(
                "SpatialAnchorCandidate",
                "SemanticFieldObjectCandidate",
            ),
        ),
        _positive_case(
            case_id="case_mapping_05_mock_scene_graph_field_structure",
            case_name="mock_scene_graph field structure placeholder mapping",
            case_goal=(
                "Validate mock_scene_graph maps to FieldGraph placeholder + Anchor placeholder."
            ),
            adapter_ref="adapter_mock_scene_graph_field_structure",
            backend_kind="mock_scene_graph",
            expected_candidate_types=("FieldGraphCandidate", "SpatialAnchorCandidate"),
        ),
    )


def _invalid_from_positive(
    *,
    case_id: str,
    case_name: str,
    case_goal: str,
    adapter_ref: str,
    mutate,
) -> SLAMSpatialEvidenceAdapterMappingCase:
    base = _positive_case(
        case_id=case_id,
        case_name=case_name,
        case_goal=case_goal,
        adapter_ref=adapter_ref,
        backend_kind="mock_vio",
        expected_candidate_types=("PoseCandidate", "MotionCandidate"),
    )
    mutated = mutate(
        {
            "mock_backend_outputs": list(base.mock_backend_outputs),
            "backend_output_frames": list(base.backend_output_frames),
            "input_envelopes": list(base.input_envelopes),
            "mapping_rules": [copy.deepcopy(r) for r in base.mapping_rules],
            "adapters": [copy.deepcopy(a) for a in base.adapters],
            "output_bundles": [copy.deepcopy(b) for b in base.output_bundles],
            "health_reports": list(base.health_reports),
        }
    )
    return SLAMSpatialEvidenceAdapterMappingCase(
        case_id=case_id,
        case_name=case_name,
        case_type="invalid",
        case_goal=case_goal,
        adapter_ref=adapter_ref,
        backend_kind=base.backend_kind,
        expected_candidate_types=base.expected_candidate_types,
        mock_backend_outputs=tuple(mutated["mock_backend_outputs"]),
        backend_output_frames=tuple(mutated["backend_output_frames"]),
        input_envelopes=tuple(mutated["input_envelopes"]),
        mapping_rules=tuple(mutated["mapping_rules"]),
        adapters=tuple(mutated["adapters"]),
        output_bundles=tuple(mutated["output_bundles"]),
        health_reports=tuple(mutated["health_reports"]),
        expected_validation_ok=False,
    )


def build_invalid_mapping_cases_v1() -> Tuple[SLAMSpatialEvidenceAdapterMappingCase, ...]:
    def mutate_unsupported(parts: Dict[str, Any]) -> Dict[str, Any]:
        parts["mapping_rules"][0]["luna_candidate_type"] = "UnsupportedCandidateType"
        return parts

    def mutate_missing_source_chain(parts: Dict[str, Any]) -> Dict[str, Any]:
        parts["output_bundles"][0]["source_chain"] = ()
        return parts

    def mutate_synthesis_bypass(parts: Dict[str, Any]) -> Dict[str, Any]:
        parts["adapters"][0]["field_synthesis_entrypoint"] = "midplatform_synthesis_v1"
        parts["output_bundles"][0]["field_synthesis_entrypoint"] = "midplatform_synthesis_v1"
        return parts

    return (
        _invalid_from_positive(
            case_id="invalid_mapping_a_unsupported_candidate_type",
            case_name="unsupported candidate type in mapping rule",
            case_goal="Reject mapping rule when luna_candidate_type is unsupported.",
            adapter_ref="adapter_mock_vio_pose_motion",
            mutate=mutate_unsupported,
        ),
        _invalid_from_positive(
            case_id="invalid_mapping_b_missing_source_chain",
            case_name="output bundle missing source_chain",
            case_goal="Reject output bundle when source_chain is missing.",
            adapter_ref="adapter_mock_vio_pose_motion",
            mutate=mutate_missing_source_chain,
        ),
        _invalid_from_positive(
            case_id="invalid_mapping_c_synthesis_entrypoint_bypass",
            case_name="field_synthesis_v1 bypass",
            case_goal="Reject adapter mapping when synthesis entrypoint bypasses field_synthesis_v1.",
            adapter_ref="adapter_mock_vio_pose_motion",
            mutate=mutate_synthesis_bypass,
        ),
    )


def build_all_mapping_cases_v1() -> Tuple[SLAMSpatialEvidenceAdapterMappingCase, ...]:
    return build_positive_mapping_cases_v1() + build_invalid_mapping_cases_v1()


def bundle_from_slam_spatial_evidence_adapter_mapping_case(
    case: SLAMSpatialEvidenceAdapterMappingCase,
) -> Dict[str, Any]:
    return {
        "case_id": case.case_id,
        "case_type": case.case_type,
        "adapter_ref": case.adapter_ref,
        "backend_kind": case.backend_kind,
        "expected_candidate_types": list(case.expected_candidate_types),
        "mock_backend_outputs": list(case.mock_backend_outputs),
        "backend_output_frames": list(case.backend_output_frames),
        "input_envelopes": list(case.input_envelopes),
        "mapping_rules": list(case.mapping_rules),
        "adapters": list(case.adapters),
        "output_bundles": list(case.output_bundles),
        "health_reports": list(case.health_reports),
    }


def _validate_case(case: SLAMSpatialEvidenceAdapterMappingCase) -> Tuple[bool, List[str]]:
    return validate_slam_spatial_evidence_adapter_mapping_case_bundle(
        bundle_from_slam_spatial_evidence_adapter_mapping_case(case)
    )


def _check_cases(
    cases: Tuple[SLAMSpatialEvidenceAdapterMappingCase, ...],
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


def summarize_slam_spatial_evidence_adapter_mapping_cases_v1() -> Dict[str, Any]:
    positive = build_positive_mapping_cases_v1()
    invalid = build_invalid_mapping_cases_v1()
    all_cases = build_all_mapping_cases_v1()

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

    ready = (
        len(positive) == 5
        and len(invalid) == 3
        and len(all_cases) == 8
        and unique_ok
        and pos_ok == len(positive)
        and inv_ok == len(invalid)
        and not pos_mismatches
        and not inv_mismatches
        and sample_positive_ok
        and sample_invalid_rejected
    )

    return {
        "phase_id": PHASE_ID,
        "step": "Step 2 SLAM Spatial Evidence Adapter Mapping Delta Cases",
        "adapter_skeleton_principle_zh": ADAPTER_SKELETON_PRINCIPLE_ZH,
        "positive_mapping_case_count": len(positive),
        "invalid_mapping_case_count": len(invalid),
        "case_count": len(all_cases),
        "positive_case_ids": [case.case_id for case in positive],
        "invalid_case_ids": [case.case_id for case in invalid],
        "case_ids_unique": unique_ok,
        "sample_positive_validate_ok": sample_positive_ok,
        "sample_invalid_rejected_ok": sample_invalid_rejected,
        "positive_validation_mismatches": pos_mismatches,
        "invalid_validation_mismatches": inv_mismatches,
        "field_synthesis_entrypoint_locked": FIELD_SYNTHESIS_ENTRYPOINT,
        "source_chain_required": True,
        "unsupported_candidate_type_rejected": True,
        "final_decision": (
            FINAL_DECISION_MAPPING_CASES_READY_FOR_RUNNER
            if ready
            else "SLAM_SPATIAL_EVIDENCE_ADAPTER_MAPPING_CASES_NOT_READY"
        ),
    }


def main() -> int:
    summary = summarize_slam_spatial_evidence_adapter_mapping_cases_v1()
    print(json.dumps(summary, ensure_ascii=False))
    return (
        0
        if summary["final_decision"] == FINAL_DECISION_MAPPING_CASES_READY_FOR_RUNNER
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
