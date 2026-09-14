# -*- coding: utf-8 -*-
"""Supervision structure reference analysis (no mainline, no YOLO, no real detector).

Phase-Vision-Supervision-Structure-Reference-Analysis-001
"""

from __future__ import annotations

import importlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ANALYSIS_SCHEMA = "supervision_structure_reference_analysis_v0"
CAPABILITY_REPORT_SCHEMA = "supervision_capability_structure_report_v0"
MAPPING_MATRIX_SCHEMA = "supervision_to_luna_mapping_matrix_v0"
REUSE_CLASSIFICATION_SCHEMA = "supervision_reuse_classification_report_v0"
RISK_REPORT_SCHEMA = "supervision_architecture_risk_report_v0"
AB_TEST_PLAN_SCHEMA = "supervision_ab_test_plan_v0"
ANALYSIS_AUDIT_SCHEMA = "supervision_structure_reference_audit_v0"


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _safe_read(p: Path) -> Optional[Any]:
    if not p.is_file():
        return None
    try:
        return _read_json(p)
    except Exception:
        return None


def probe_supervision_structure_extended_v0() -> Dict[str, Any]:
    """Runtime probe for structure reference (no detector inference)."""
    from capabilities.vision_runtime.external_supervision_adapter_experiment_v0 import probe_supervision_v0

    base = probe_supervision_v0()
    extended: Dict[str, Any] = {
        "byte_track_available": False,
        "byte_track_note": "",
        "polygon_zone_available": False,
        "line_zone_available": False,
        "annotators_available": False,
        "annotator_symbols": [],
        "dataset_helpers_available": False,
        "mask_api_available": False,
        "dependency_risks": [],
    }
    if not base.get("supervision_installed"):
        extended["dependency_risks"].append("supervision_not_installed_in_runner_env")
        return {**base, "extended_probe": extended}

    try:
        import supervision as sv  # type: ignore

        extended["mask_api_available"] = hasattr(sv, "mask") or hasattr(sv, "Mask")
        extended["polygon_zone_available"] = hasattr(sv, "PolygonZone")
        extended["line_zone_available"] = hasattr(sv, "LineZone")
        if hasattr(sv, "ByteTrack"):
            extended["byte_track_available"] = True
            extended["byte_track_note"] = "supervision.ByteTrack attribute present"
        else:
            try:
                importlib.import_module("supervision.tracker.byte_tracker")
                extended["byte_track_available"] = True
                extended["byte_track_note"] = "supervision.tracker.byte_tracker import ok"
            except Exception as e:
                extended["byte_track_note"] = f"byte_tracker: {type(e).__name__}"

        ann_syms: List[str] = []
        for name in ("BoxAnnotator", "LabelAnnotator", "MaskAnnotator", "TraceAnnotator"):
            if hasattr(sv, name):
                ann_syms.append(name)
        extended["annotators_available"] = len(ann_syms) > 0
        extended["annotator_symbols"] = ann_syms

        for name in ("ClassificationDataset", "DetectionDataset"):
            if hasattr(sv, name):
                extended["dataset_helpers_available"] = True
                break

        extended["dependency_risks"].append(
            "supervision_is_third_party_library_version_pinned_recommended"
        )
        if not extended["byte_track_available"]:
            extended["dependency_risks"].append("byte_track_not_confirmed_in_probe")
    except Exception as e:
        extended["dependency_risks"].append(f"extended_probe_error:{type(e).__name__}")

    return {**base, "extended_probe": extended}


def build_capability_structure_report_v0(
    *,
    experiment_probe: Optional[Dict[str, Any]],
    runtime_probe: Dict[str, Any],
    experiment_feature_matrix: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    sf = {}
    if isinstance(experiment_probe, dict):
        sf = experiment_probe.get("supported_features_probe") if isinstance(
            experiment_probe.get("supported_features_probe"), dict
        ) else {}
    ext = runtime_probe.get("extended_probe") if isinstance(runtime_probe.get("extended_probe"), dict) else {}

    installed = bool(runtime_probe.get("supervision_installed") or (experiment_probe or {}).get("supervision_installed"))
    version = runtime_probe.get("supervision_version") or (experiment_probe or {}).get("supervision_version")

    return {
        "schema": CAPABILITY_REPORT_SCHEMA,
        "supervision_installed": installed,
        "supervision_version": version,
        "detections_api": {
            "available": bool(sf.get("detections_class") or installed),
            "notes": "supervision.Detections — xyxy, confidence, class_id, tracker_id, mask fields",
        },
        "mask_polygon_support": {
            "mask_api": bool(ext.get("mask_api_available") or sf.get("polygon_or_mask_helpers")),
            "polygon_zone": bool(ext.get("polygon_zone_available") or sf.get("polygon_or_mask_helpers")),
            "notes": "mask / polygon are candidate geometry; not Luna facts",
        },
        "tracker_support": {
            "tracker_module_hint": bool(sf.get("tracker_module_hint")),
            "byte_track_available": bool(ext.get("byte_track_available")),
            "byte_track_note": ext.get("byte_track_note") or sf.get("tracker_capability_note"),
        },
        "zone_line_annotation": {
            "polygon_zone": bool(ext.get("polygon_zone_available")),
            "line_zone": bool(ext.get("line_zone_available")),
            "annotators": bool(ext.get("annotators_available")),
            "annotator_symbols": list(ext.get("annotator_symbols") or []),
            "dataset_helpers": bool(ext.get("dataset_helpers_available")),
        },
        "experiment_feature_matrix_ref": experiment_feature_matrix,
        "dependency_risks": list(ext.get("dependency_risks") or []),
    }


def build_luna_mapping_matrix_v0() -> Dict[str, Any]:
    rows = [
        {
            "supervision_concept": "supervision.Detections",
            "luna_target": "Luna VisionDetectionEvidence",
            "field_mappings": [
                {"supervision": "xyxy", "luna": "bbox_in_frame"},
                {"supervision": "confidence", "luna": "confidence"},
                {"supervision": "class_id / data", "luna": "label (candidate_only, not_fact)"},
                {"supervision": "tracker_id", "luna": "tracking_ref (not identity fact)"},
            ],
            "disposition": "candidate_observation_not_fact",
        },
        {
            "supervision_concept": "mask / polygon / segmentation helpers",
            "luna_target": "Luna VisionSegmentationEvidence / VisionROIProposalCandidate",
            "field_mappings": [
                {"supervision": "mask", "luna": "mask_ref / segmentation_candidate"},
                {"supervision": "polygon", "luna": "polygon_in_frame / roi_polygon"},
            ],
            "disposition": "geometry_candidate_later",
        },
        {
            "supervision_concept": "tracker_id / ByteTrack",
            "luna_target": "Luna VisionTrackingEvidence",
            "field_mappings": [
                {"supervision": "tracker_id", "luna": "track_id_candidate"},
                {"supervision": "ByteTrack update", "luna": "temporal_association_stub"},
            ],
            "disposition": "temporal_candidate_not_identity",
        },
        {
            "supervision_concept": "PolygonZone / LineZone",
            "luna_target": "Luna VisionZoneEvidence / RiskRegion / TaskROI",
            "field_mappings": [
                {"supervision": "zone trigger", "luna": "zone_event_candidate"},
                {"supervision": "line crossing", "luna": "line_crossing_candidate"},
            ],
            "disposition": "governance_gated_reference_only",
        },
        {
            "supervision_concept": "Annotators (Box/Mask/Label/Trace)",
            "luna_target": "Luna Whitebox Debug Overlay / Dev HUD",
            "field_mappings": [
                {"supervision": "render overlay", "luna": "debug_visualization_only"},
            ],
            "disposition": "dev_tooling_not_runtime_decision",
        },
        {
            "supervision_concept": "Dataset / annotation workflow",
            "luna_target": "Luna evaluation fixtures / offline tooling",
            "field_mappings": [
                {"supervision": "ClassificationDataset", "luna": "eval_dataset_helper"},
            ],
            "disposition": "reference_only_offline",
        },
    ]
    return {"schema": MAPPING_MATRIX_SCHEMA, "rows": rows}


def build_reuse_classification_report_v0(capability: Dict[str, Any]) -> Dict[str, Any]:
    ext = capability.get("zone_line_annotation") if isinstance(capability.get("zone_line_annotation"), dict) else {}
    items = [
        {
            "capability": "Detections data structure",
            "classification": "direct_reuse_candidate",
            "rationale": "Align Luna VisionDetectionEvidence fields with Detections xyxy/confidence/class_id pattern.",
        },
        {
            "capability": "mask / polygon helpers",
            "classification": "requires_adapter",
            "rationale": "Map to VisionSegmentationEvidence / ROI proposal via adapter; must pass Frame Input Governance.",
        },
        {
            "capability": "ByteTrack / tracker_id",
            "classification": "requires_governance",
            "rationale": "tracker_id is temporal association only; never identity fact or navigation input.",
        },
        {
            "capability": "PolygonZone / LineZone",
            "classification": "reference_only",
            "rationale": "Use for zone semantics reference; gate via governance before TaskROI / RiskRegion.",
        },
        {
            "capability": "Annotators",
            "classification": "direct_reuse_candidate",
            "rationale": "Whitebox overlay / dev HUD only; not mainline decision path.",
        },
        {
            "capability": "Dataset workflow",
            "classification": "reference_only",
            "rationale": "Offline eval fixtures; not runtime mainline.",
        },
        {
            "capability": "Supervision as Luna Core replacement",
            "classification": "not_recommended",
            "rationale": "Must not replace Frame Trace, Input Governance, or Evidence Pack ownership.",
        },
    ]
    if not ext.get("byte_track_available"):
        for it in items:
            if it["capability"].startswith("ByteTrack"):
                it["classification"] = "requires_adapter"
                it["rationale"] += " (ByteTrack not confirmed in probe — verify before adoption)"
    return {"schema": REUSE_CLASSIFICATION_SCHEMA, "items": items}


def build_architecture_risk_report_v0() -> Dict[str, Any]:
    return {
        "schema": RISK_REPORT_SCHEMA,
        "must_not": [
            "supervision_must_not_replace_luna_core",
            "must_not_bypass_frame_input_governance",
            "must_not_bypass_vision_provider_input_pack",
            "must_not_write_midplatform_fact",
            "must_not_write_scene_delta",
            "must_not_write_world_model",
            "must_not_invoke_navigation_decision",
            "must_not_treat_tracker_id_as_identity_fact",
            "must_not_treat_detection_label_as_confirmed_fact",
            "mask_and_bbox_are_candidate_geometry_only",
        ],
        "narrative": [
            "Supervision is a reference and adapter candidate library, not Luna Core.",
            "All geometry must flow through Frame Input Governance and vision_provider_input_pack_v0.",
            "Detections labels and tracker_id remain not_fact / candidate_only in Luna evidence packs.",
            "No MidPlatform fact, Scene Delta, or WorldModel writes from this analysis phase.",
            "No navigation decisions or AI interpretation on Supervision outputs alone.",
        ],
        "supervision_must_not_replace_luna_core": True,
        "must_not_bypass_frame_input_governance": True,
        "must_not_bypass_vision_provider_input_pack": True,
        "must_not_write_midplatform_fact": True,
        "must_not_write_scene_delta": True,
        "must_not_invoke_navigation_decision": True,
    }


def build_recommended_adoption_plan_v0() -> Dict[str, Any]:
    return {
        "schema": "supervision_recommended_adoption_plan_v0",
        "horizons": {
            "short_term": {
                "label": "A",
                "title": "Reference Detections structure for Luna VisionDetectionEvidence",
                "actions": [
                    "Document field parity: xyxy, confidence, class_id, optional mask, optional tracker_id.",
                    "Keep fact_status=not_fact and synthetic/stub flags in evidence pack.",
                ],
            },
            "medium_term": {
                "label": "B",
                "title": "Supervision Adapter A/B Test (synthetic / detections adapter vs rule_stub ROI)",
                "actions": [
                    "Run controlled A/B on same frame envelopes.",
                    "Compare ROI count, bbox validity, coordinate lift completeness.",
                ],
            },
            "long_term": {
                "label": "C",
                "title": "Whitebox Overlay / Debug Tools / Test Board",
                "actions": [
                    "Optional annotators for dev HUD only.",
                    "Optional zones for offline risk-region experiments with explicit governance.",
                ],
            },
        },
    }


def build_ab_test_plan_v0() -> Dict[str, Any]:
    return {
        "schema": AB_TEST_PLAN_SCHEMA,
        "variants": [
            {
                "id": "A",
                "name": "Luna rule_stub ROI",
                "description": "Existing vision_roi_proposal_stub / governance path.",
            },
            {
                "id": "B",
                "name": "Supervision synthetic / detections adapter",
                "description": "external_supervision_adapter experiment synthetic detections → ROI candidate.",
            },
            {
                "id": "C",
                "name": "future YOLO + Supervision",
                "description": "Deferred — requires gated real detector phase; not in this analysis.",
                "status": "planned_not_in_scope",
            },
            {
                "id": "D",
                "name": "Luna native evidence pack",
                "description": "vision_recognition_evidence_pack_v0 stub/mainline comparison baseline.",
            },
        ],
        "metrics": [
            "roi_count",
            "bbox_validity",
            "coordinate_lift_completeness",
            "tracker_stability",
            "frame_latency_ms",
            "memory_footprint_mb",
            "audit_completeness",
            "forbidden_write_boundary_violations",
        ],
        "success_criteria": {
            "no_midplatform_fact_write": True,
            "no_scene_delta_write": True,
            "no_navigation_decision": True,
            "audit_flags_complete_per_variant": True,
        },
        "notes": "A/B is evaluation-only; does not modify runtime mainline defaults.",
    }


def build_structure_reference_audit_v0() -> Dict[str, Any]:
    return {
        "schema": ANALYSIS_AUDIT_SCHEMA,
        "supervision_analysis_executed": True,
        "supervision_mainline_invoked": False,
        "yolo_invoked": False,
        "real_detector_invoked": False,
        "navigation_decision_invoked": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "ai_interpretation_invoked": False,
        "database_write_invoked": False,
        "runtime_mainline_modified": False,
    }


def run_supervision_structure_reference_analysis_v0(
    *,
    supervision_experiment_root: str,
) -> Tuple[
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    List[str],
]:
    """Returns summary, capability, mapping, reuse, risk, adoption, ab_plan, audit, errors."""
    errs: List[str] = []
    root = Path(supervision_experiment_root).resolve()
    if not root.is_dir():
        errs.append(f"experiment_root_missing:{root}")
        return (
            {"schema": "supervision_structure_reference_summary_v0", "errors": errs},
            {},
            {},
            {},
            {},
            {},
            {},
            build_structure_reference_audit_v0(),
            errs,
        )

    exp_probe = _safe_read(root / "external_supervision_availability_probe.json")
    exp_matrix = _safe_read(root / "external_supervision_feature_matrix.json")
    exp_audit = _safe_read(root / "external_supervision_audit_report.json")
    exp_summary = _safe_read(root / "external_supervision_adapter_experiment_summary.json")

    if exp_probe is None:
        errs.append("missing_external_supervision_availability_probe")
    elif exp_probe.get("supervision_installed") is not True:
        errs.append("experiment_probe_supervision_not_installed")

    runtime_probe = probe_supervision_structure_extended_v0()

    capability = build_capability_structure_report_v0(
        experiment_probe=exp_probe if isinstance(exp_probe, dict) else None,
        runtime_probe=runtime_probe,
        experiment_feature_matrix=exp_matrix if isinstance(exp_matrix, dict) else None,
    )
    mapping = build_luna_mapping_matrix_v0()
    reuse = build_reuse_classification_report_v0(capability)
    risk = build_architecture_risk_report_v0()
    adoption = build_recommended_adoption_plan_v0()
    ab_plan = build_ab_test_plan_v0()
    audit = build_structure_reference_audit_v0()

    if exp_audit and isinstance(exp_audit, dict):
        if exp_audit.get("yolo_invoked") is True or exp_audit.get("real_detector_invoked") is True:
            errs.append("experiment_audit_forbidden_invocation")

    summary = {
        "schema_version": "supervision_structure_reference_summary_v0",
        "phase": "Phase-Vision-Supervision-Structure-Reference-Analysis-001",
        "analysis_schema": ANALYSIS_SCHEMA,
        "supervision_experiment_root": str(root),
        "supervision_installed": capability.get("supervision_installed"),
        "supervision_version": capability.get("supervision_version"),
        "experiment_summary_ref": str((root / "external_supervision_adapter_experiment_summary.json").resolve())
        if exp_summary
        else None,
        "mapping_row_count": len(mapping.get("rows") or []),
        "reuse_item_count": len(reuse.get("items") or []),
        "errors": list(errs),
    }

    return summary, capability, mapping, reuse, risk, adoption, ab_plan, audit, errs
