# -*- coding: utf-8 -*-
"""OCR Mainline Final Closure v1.

Phase-OCR-Mainline-Final-Closure-v1-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Phase-OCR-Mainline-Final-Closure-v1-001"
FINAL_DECISION = "OCR_MAINLINE_FINAL_CLOSURE_RETURN_TO_VISION_MAINLINE"
PRIMARY_NEXT = "Phase-Return-To-Vision-Mainline-Planning-v1-001"
ALTERNATIVE_NEXT = "Phase-OCR-Mainline-Final-Closure-v1-001"
SOURCE_CHAIN = "ocr_mainline_final_closure_v1"
CLOSURE_ID = "ocr_mfc_v1_001"
CURRENT_STATUS = "closed_for_current_mainline"

ROOT_INPUT_SPECS = [
    {
        "intake_id": "ocr_regression_route_compliance",
        "path_arg": "ocr_regression_route_compliance_root",
        "label": "OCR StaticReading Poster RealVideo Regression Route Compliance",
        "required": False,
        "summary_file": "ocr_staticreading_poster_realvideo_regression_route_compliance_v1_summary.json",
        "extra_artifacts": ["ocr_staticreading_poster_realvideo_regression_v1_summary.json"],
    },
    {
        "intake_id": "roi_to_ocrrequest_reference",
        "path_arg": "roi_to_ocrrequest_reference_root",
        "label": "ROI-to-OCRRequest Reference",
        "required": False,
        "summary_file": "roi_to_ocrrequest_reference_v1_summary.json",
        "extra_artifacts": [],
    },
    {
        "intake_id": "ocr_evidence_pack_adapter_v1",
        "path_arg": "ocr_evidence_pack_adapter_v1_root",
        "label": "OCR Evidence Pack Adapter v1 Scan Observation Alignment",
        "required": False,
        "summary_file": "ocr_evidence_pack_adapter_v1_scan_observation_alignment_summary.json",
        "extra_artifacts": [],
    },
    {
        "intake_id": "mixed_batch_v2_gated_path",
        "path_arg": "mixed_batch_v2_gated_path_root",
        "label": "Mixed Video Poster Batch Smoke v2 Gated Path Only",
        "required": False,
        "summary_file": "mixed_batch_v2_gated_path_summary.json",
        "extra_artifacts": [],
    },
    {
        "intake_id": "realvideo_text_bearing_planning",
        "path_arg": "realvideo_text_bearing_planning_root",
        "label": "RealVideo OCR Text-Bearing Sample Planning",
        "required": False,
        "summary_file": "realvideo_ocr_text_bearing_sample_planning_summary.json",
        "extra_artifacts": [],
    },
    {
        "intake_id": "static_readable_region_discovery",
        "path_arg": "static_readable_region_discovery_root",
        "label": "Static Readable Region Discovery Guidance Policy",
        "required": False,
        "summary_file": "static_readable_region_discovery_guidance_policy_v1_summary.json",
        "extra_artifacts": [],
    },
    {
        "intake_id": "worldmodel_lookup_reading_framework",
        "path_arg": "worldmodel_lookup_reading_framework_root",
        "label": "WorldModel Lookup for Reading Framework",
        "required": False,
        "summary_file": "worldmodel_lookup_for_reading_framework_v1_summary.json",
        "extra_artifacts": [],
    },
    {
        "intake_id": "minimal_runtime_integration_closure",
        "path_arg": "minimal_runtime_integration_closure_root",
        "label": "Minimal Runtime Integration Closure",
        "required": True,
        "summary_file": "summary.json",
        "extra_artifacts": ["minimal_runtime_integration_closure_report.json"],
    },
    {
        "intake_id": "roi_crop_rerun",
        "path_arg": "roi_crop_rerun_root",
        "label": "ROI Crop Execution DryRun Rerun Better Frames",
        "required": False,
        "summary_file": "roi_crop_rerun_better_frames_summary.json",
        "extra_artifacts": [],
    },
    {
        "intake_id": "roi_bbox_expansion",
        "path_arg": "roi_bbox_expansion_root",
        "label": "ROI BBox Expansion Proposal",
        "required": False,
        "summary_file": "roi_bbox_expansion_proposal_v1_summary.json",
        "extra_artifacts": [],
    },
    {
        "intake_id": "better_frame_extraction",
        "path_arg": "better_frame_extraction_root",
        "label": "Better Frame Extraction DryRun",
        "required": False,
        "summary_file": "better_frame_extraction_dryrun_v1_summary.json",
        "extra_artifacts": [],
    },
    {
        "intake_id": "bbox_adjustment_multiframe",
        "path_arg": "bbox_adjustment_multiframe_root",
        "label": "BBox Adjustment Proposal v2 Multiframe",
        "required": False,
        "summary_file": "bbox_adjustment_proposal_v2_multiframe_summary.json",
        "extra_artifacts": [],
    },
    {
        "intake_id": "hardware_camera_control_contract",
        "path_arg": "hardware_camera_control_contract_root",
        "label": "Hardware Camera Control Contract",
        "required": False,
        "summary_file": "hardware_camera_control_contract_v1_summary.json",
        "extra_artifacts": [],
    },
    {
        "intake_id": "voice_interruption_governance",
        "path_arg": "voice_interruption_governance_root",
        "label": "Voice Interruption Governance DryRun",
        "required": False,
        "summary_file": "summary.json",
        "extra_artifacts": ["interruption_decision_candidates.json"],
    },
    {
        "intake_id": "basic_navigation_stabilization",
        "path_arg": "basic_navigation_stabilization_root",
        "label": "Basic Navigation Guidance Loop Stabilization Test",
        "required": False,
        "summary_file": "summary.json",
        "extra_artifacts": ["stabilization_scenarios.json"],
    },
]

REQUIRED_DOCS = {
    "ocr_phase_verdict_table": "docs/architecture/evaluation/LUNA_EVALUATION_OCR_PHASE_VERDICT_STATUS_TABLE_V0.md",
}

OPTIONAL_DOC_PATHS = {
    "ocr_activation_governance": [
        "docs/architecture/midplatform/LUNA_OCR_ACTIVATION_GOVERNANCE_POLICY_V1.md",
        "docs/architecture/evaluation/LUNA_EVALUATION_OCR_ACTIVATION_GOVERNANCE_POLICY_V1.md",
    ],
    "ocrrequest_reference": [
        "docs/architecture/midplatform/LUNA_ROI_TO_OCRREQUEST_REFERENCE_V1.md",
        "docs/architecture/evaluation/LUNA_EVALUATION_ROI_TO_OCRREQUEST_REFERENCE_V1.md",
    ],
    "evidence_pack_semantic_candidate": [
        "docs/architecture/midplatform/LUNA_OCR_EVIDENCE_PACK_ADAPTER_V1_SCAN_OBSERVATION_ALIGNMENT_V0.md",
        "docs/architecture/evaluation/LUNA_EVALUATION_OCR_EVIDENCE_PACK_ADAPTER_V1_SCAN_OBSERVATION_ALIGNMENT_V0.md",
    ],
    "poster_governance_ocr": [
        "docs/architecture/ocr/LUNA_POSTER_REAL_OCR_GATED_EXECUTION_V0.md",
        "docs/architecture/ocr/LUNA_POSTER_REAL_OCR_READONLY_CONSUMER_V0.md",
    ],
    "static_reading_readable_region": [
        "docs/architecture/midplatform/LUNA_STATIC_READABLE_REGION_DISCOVERY_GUIDANCE_POLICY_V1.md",
        "docs/architecture/evaluation/LUNA_EVALUATION_STATIC_READABLE_REGION_DISCOVERY_GUIDANCE_POLICY_V1.md",
    ],
    "realvideo_ocr_planning_or_readonly": [
        "docs/architecture/evaluation/LUNA_EVALUATION_REALVIDEO_OCR_EVIDENCE_READONLY_CONSUMER_GO_NO_GO_PACK_V0.md",
        "docs/architecture/evaluation/LUNA_EVALUATION_CROSS_MODAL_VISION_OCR_TESTBOARD_V1_REALVIDEO_FRAMESAMPLE_SMOKE_V0.md",
    ],
    "worldmodel_lookup_reading": [
        "docs/architecture/midplatform/LUNA_WORLDMODEL_LOOKUP_FOR_READING_FRAMEWORK_V1.md",
        "docs/architecture/evaluation/LUNA_EVALUATION_WORLDMODEL_LOOKUP_FOR_READING_FRAMEWORK_V1.md",
    ],
    "memory_handoff_or_governance": [
        "docs/architecture/midplatform/LUNA_CONFIRMED_TEXT_EVIDENCE_MEMORY_GOVERNANCE_CONTRACT_V1.md",
        "docs/architecture/evaluation/LUNA_EVALUATION_CONFIRMED_TEXT_EVIDENCE_MEMORY_GOVERNANCE_CONTRACT_V1.md",
    ],
    "stc_docs": [
        "docs/architecture/midplatform/LUNA_STC_SAMPLING_GUIDANCE_POLICY_V1.md",
        "docs/architecture/evaluation/LUNA_EVALUATION_STCM_CROSS_CONTRACT_FIELD_ALIGNMENT_V0.md",
    ],
    "system_health_docs": [
        "docs/architecture/midplatform/LUNA_SYSTEM_HEALTH_CENTER_GOVERNANCE_V0.md",
        "docs/architecture/evaluation/LUNA_EVALUATION_SYSTEM_HEALTH_CENTER_GOVERNANCE_V0.md",
    ],
    "minimal_runtime_integration_closure_doc": [
        "docs/architecture/midplatform/LUNA_MINIMAL_RUNTIME_INTEGRATION_CLOSURE_V1.md",
        "docs/architecture/evaluation/LUNA_EVALUATION_MINIMAL_RUNTIME_INTEGRATION_CLOSURE_V1.md",
    ],
    "speech_gate_or_vop_reference": [
        "docs/architecture/midplatform/LUNA_MINIMAL_RUNTIME_INTEGRATION_CONTROLLED_OUTPUT_DEFINITION_V1.md",
        "docs/architecture/midplatform/LUNA_VOICE_OUTPUT_PLANE_ADAPTER_FOR_GUIDANCE_V1.md",
    ],
}

BOUNDARY_FALSE_FLAGS = {
    "closure_only": True,
    "ocr_runtime_invoked": False,
    "ocr_provider_invoked": False,
    "ocrrequest_submitted": False,
    "paddleocr_invoked": False,
    "rapidocr_invoked": False,
    "deepseek_ocr_invoked": False,
    "camera_invoked": False,
    "frame_sampled": False,
    "new_crop_generated": False,
    "detector_invoked": False,
    "segmentation_invoked": False,
    "tracking_invoked": False,
    "provider_comparison_executed": False,
    "benchmark_accuracy_updated": False,
    "semantic_candidate_generated_now": False,
    "evidence_pack_generated_now": False,
    "world_model_written": False,
    "memory_written": False,
    "fact_written": False,
    "scene_delta_generated": False,
    "navigation_action_triggered": False,
    "task_state_committed_now": False,
    "map_api_invoked": False,
    "runtime_routing_changed": False,
    "new_runtime_enabled": False,
}

PHASE_MATRIX_SPECS = [
    {
        "phase_name": "RealVideo OCR Text-Bearing Sample Planning",
        "intake_id": "realvideo_text_bearing_planning",
        "scope": "planning_only",
        "closure_relevance": "realvideo_chain_kept_as_planning_reference_without_runtime_execution",
        "key_artifacts": ["realvideo_ocr_text_bearing_sample_planning_summary.json"],
    },
    {
        "phase_name": "Mixed Video Poster Batch Smoke v2 Gated Path Only",
        "intake_id": "mixed_batch_v2_gated_path",
        "scope": "gated_path_only",
        "closure_relevance": "confirms gated path replaces direct provider call",
        "key_artifacts": ["mixed_batch_v2_gated_path_summary.json"],
    },
    {
        "phase_name": "OCR Evidence Pack Adapter v1",
        "intake_id": "ocr_evidence_pack_adapter_v1",
        "scope": "adapter_alignment_only",
        "closure_relevance": "confirms scan observation alignment without fact promotion",
        "key_artifacts": ["ocr_evidence_pack_adapter_v1_scan_observation_alignment_summary.json"],
    },
    {
        "phase_name": "ROI Crop Execution DryRun",
        "intake_id": "roi_crop_rerun",
        "scope": "dryrun_only",
        "closure_relevance": "keeps crop path dryrun and reference-only",
        "key_artifacts": ["roi_crop_rerun_better_frames_summary.json"],
    },
    {
        "phase_name": "ROI-to-OCRRequest Reference",
        "intake_id": "roi_to_ocrrequest_reference",
        "scope": "reference_only",
        "closure_relevance": "confirms OCRRequest reference is not submission",
        "key_artifacts": ["roi_to_ocrrequest_reference_v1_summary.json"],
    },
    {
        "phase_name": "ROI BBox Expansion Proposal",
        "intake_id": "roi_bbox_expansion",
        "scope": "proposal_only",
        "closure_relevance": "keeps bbox expansion as future crop planning only",
        "key_artifacts": ["roi_bbox_expansion_proposal_v1_summary.json"],
    },
    {
        "phase_name": "Better Frame Extraction DryRun",
        "intake_id": "better_frame_extraction",
        "scope": "dryrun_only",
        "closure_relevance": "keeps frame selection as offline candidate path",
        "key_artifacts": ["better_frame_extraction_dryrun_v1_summary.json"],
    },
    {
        "phase_name": "BBox Adjustment Proposal v2 Multiframe",
        "intake_id": "bbox_adjustment_multiframe",
        "scope": "proposal_only",
        "closure_relevance": "keeps multiframe bbox adjustment as deferred re-ocr preparation",
        "key_artifacts": ["bbox_adjustment_proposal_v2_multiframe_summary.json"],
    },
    {
        "phase_name": "Static Readable Region Discovery Guidance Policy",
        "intake_id": "static_readable_region_discovery",
        "scope": "policy_only",
        "closure_relevance": "shows static reading depends on readable region discovery before OCR gate",
        "key_artifacts": ["static_readable_region_discovery_guidance_policy_v1_summary.json"],
    },
    {
        "phase_name": "Hardware Camera Control Contract",
        "intake_id": "hardware_camera_control_contract",
        "scope": "contract_only",
        "closure_relevance": "keeps camera handoff contractual and not enabled",
        "key_artifacts": ["hardware_camera_control_contract_v1_summary.json"],
    },
    {
        "phase_name": "WorldModel Lookup for Reading Framework",
        "intake_id": "worldmodel_lookup_reading_framework",
        "scope": "framework_only",
        "closure_relevance": "confirms worldmodel role is lookup candidate support and not write path",
        "key_artifacts": ["worldmodel_lookup_for_reading_framework_v1_summary.json"],
    },
    {
        "phase_name": "OCR StaticReading Poster RealVideo Regression Route Compliance",
        "intake_id": "ocr_regression_route_compliance",
        "scope": "regression_route_compliance_only",
        "closure_relevance": "confirms route compliance without runtime or provider bypass",
        "key_artifacts": ["ocr_staticreading_poster_realvideo_regression_route_compliance_v1_summary.json"],
    },
    {
        "phase_name": "Minimal Runtime Integration Closure",
        "intake_id": "minimal_runtime_integration_closure",
        "scope": "closure_only",
        "closure_relevance": "confirms OCR closure must align with text-only output baseline and no-write runtime boundary",
        "key_artifacts": ["summary.json", "minimal_runtime_integration_closure_report.json"],
    },
]

NON_CLAIMS = [
    "OCR closure does not equal production OCR runtime.",
    "OCRRequest reference does not equal OCRRequest submitted.",
    "crop generated or reference generated does not equal provider executed.",
    "Evidence Pack candidate does not equal fact.",
    "scan observation does not equal OCR text evidence.",
    "semantic candidate does not equal WorldModel write.",
    "readable region candidate does not equal detected text fact.",
    "static reading handoff does not equal camera capture.",
    "RealVideo planning does not equal real video OCR benchmark.",
    "Minimal Runtime Integration text-only output does not equal real voice output.",
    "OCR mainline must not bypass STC, SourceQuality, Readability, or OCRRequest gate.",
]

DEFERRED_CAPABILITIES = [
    "real_ocr_provider_integration",
    "paddleocr_heavy_runtime",
    "rapidocr_runtime_execution",
    "deepseek_ocr_remote_runtime",
    "ocrrequest_actual_submission",
    "provider_comparison_benchmark",
    "real_camera_capture",
    "real_frame_sampling",
    "real_crop_generation_from_live_stream",
    "text_detector_runtime",
    "segmentation_or_tracking_assisted_ocr",
    "worldmodel_ocr_fact_write",
    "memory_ocr_write",
    "scene_delta_generation",
    "public_facility_semantic_correction_runtime",
    "poster_ocr_production_route",
    "realvideo_ocr_benchmark_execution",
]

OCR_TO_VISION_ROLES = [
    "candidate_or_reference_evidence_provider",
    "text_region_hint_provider",
    "readable_region_support",
    "posterior_verification_tool",
    "worldmodel_verification_candidate_not_fact_writer",
    "map_route_scene_label_auxiliary_source_not_route_authority",
]

VISION_NEXT_FOCUS = [
    "return_to_vision_mainline_planning",
    "viewpoint_segmentation_or_view_slicing",
    "object_tracking",
    "visual_candidate_stabilization",
    "map_route_location_context_integration",
    "basic_navigation_loop_strengthening",
]


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _read_json(path: Path) -> Any:
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return None


def _boundary_payload() -> Dict[str, Any]:
    return {
        **BOUNDARY_FALSE_FLAGS,
        "boundary_ok": True,
        "violations": [],
        **_not_fact(),
    }


def _first_existing(root: Path, names: List[str]) -> Optional[Path]:
    for name in names:
        candidate = root / name
        if candidate.is_file():
            return candidate
    return None


def _bool_or_false(payload: Dict[str, Any], *keys: str) -> bool:
    return any(bool(payload.get(key)) for key in keys)


def _infer_verdict(summary: Dict[str, Any]) -> Optional[str]:
    for key in ("phase_verdict_hint", "phase_verdict", "verdict"):
        value = summary.get(key)
        if value:
            return value
    if summary.get("boundary_ok") is True and summary.get("final_decision"):
        return "GO"
    if summary.get("phase") and summary.get("write_allowed") is False:
        return "GO"
    return None


def _doc_rows(workspace_root: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for intake_id, rel in REQUIRED_DOCS.items():
        path = workspace_root / rel
        rows.append(
            {
                "intake_id": intake_id,
                "input_source": "required_documentation",
                "source_root_or_path": str(path),
                "artifact": path.name,
                "loaded": path.is_file(),
                "optional": False,
                "intake_status": "loaded" if path.is_file() else "missing",
                "missing_impact": "required_for_closure" if not path.is_file() else "none",
                **_not_fact(),
            }
        )
    for intake_id, candidates in OPTIONAL_DOC_PATHS.items():
        found = [workspace_root / rel for rel in candidates if (workspace_root / rel).is_file()]
        rows.append(
            {
                "intake_id": intake_id,
                "input_source": "optional_documentation",
                "source_root_or_path": str(found[0]) if found else "(not_found)",
                "artifact": found[0].name if found else None,
                "loaded": bool(found),
                "optional": True,
                "intake_status": "loaded" if found else "optional_missing",
                "missing_impact": "optional_reference_only",
                **_not_fact(),
            }
        )
    return rows


def run_ocr_mainline_final_closure_v1(
    *,
    ocr_regression_route_compliance_root: str,
    roi_to_ocrrequest_reference_root: str,
    ocr_evidence_pack_adapter_v1_root: str,
    mixed_batch_v2_gated_path_root: str,
    realvideo_text_bearing_planning_root: str,
    static_readable_region_discovery_root: str,
    worldmodel_lookup_reading_framework_root: str,
    minimal_runtime_integration_closure_root: str,
    roi_crop_rerun_root: Optional[str] = None,
    roi_bbox_expansion_root: Optional[str] = None,
    better_frame_extraction_root: Optional[str] = None,
    bbox_adjustment_multiframe_root: Optional[str] = None,
    hardware_camera_control_contract_root: Optional[str] = None,
    voice_interruption_governance_root: Optional[str] = None,
    basic_navigation_stabilization_root: Optional[str] = None,
    workspace_root: Optional[str] = None,
) -> Dict[str, Any]:
    workspace = Path(workspace_root or "/Users/luanlei/Desktop/Luna-Workspace-Min").resolve()
    arg_values = {
        "ocr_regression_route_compliance_root": ocr_regression_route_compliance_root,
        "roi_to_ocrrequest_reference_root": roi_to_ocrrequest_reference_root,
        "ocr_evidence_pack_adapter_v1_root": ocr_evidence_pack_adapter_v1_root,
        "mixed_batch_v2_gated_path_root": mixed_batch_v2_gated_path_root,
        "realvideo_text_bearing_planning_root": realvideo_text_bearing_planning_root,
        "static_readable_region_discovery_root": static_readable_region_discovery_root,
        "worldmodel_lookup_reading_framework_root": worldmodel_lookup_reading_framework_root,
        "minimal_runtime_integration_closure_root": minimal_runtime_integration_closure_root,
        "roi_crop_rerun_root": roi_crop_rerun_root,
        "roi_bbox_expansion_root": roi_bbox_expansion_root,
        "better_frame_extraction_root": better_frame_extraction_root,
        "bbox_adjustment_multiframe_root": bbox_adjustment_multiframe_root,
        "hardware_camera_control_contract_root": hardware_camera_control_contract_root,
        "voice_interruption_governance_root": voice_interruption_governance_root,
        "basic_navigation_stabilization_root": basic_navigation_stabilization_root,
    }

    root_meta: Dict[str, Dict[str, Any]] = {}
    input_root_rows: List[Dict[str, Any]] = []
    for spec in ROOT_INPUT_SPECS:
        path_value = arg_values.get(spec["path_arg"])
        root = Path(path_value).resolve() if path_value else None
        summary_path = _first_existing(root, [spec["summary_file"], *spec["extra_artifacts"]]) if root else None
        loaded = bool(root and root.is_dir() and summary_path)
        root_meta[spec["intake_id"]] = {
            "root": root,
            "loaded": loaded,
            "summary_path": summary_path,
            "required": spec["required"],
            "label": spec["label"],
        }
        input_root_rows.append(
            {
                "intake_id": spec["intake_id"],
                "input_source": spec["label"],
                "source_root_or_path": str(root) if root else "(not_provided)",
                "artifact": spec["summary_file"],
                "loaded": loaded,
                "optional": not spec["required"],
                "intake_status": (
                    "loaded"
                    if loaded
                    else ("missing" if spec["required"] else "optional_missing")
                ),
                "missing_impact": (
                    "closure_blocker_if_missing"
                    if spec["required"] and not loaded
                    else ("optional_reference_only" if not loaded else "none")
                ),
                **_not_fact(),
            }
        )
    input_root_rows.extend(_doc_rows(workspace))

    summaries: Dict[str, Dict[str, Any]] = {}
    for intake_id, meta in root_meta.items():
        summaries[intake_id] = _read_json(meta["summary_path"]) if meta["summary_path"] else {}

    completed_phase_rows: List[Dict[str, Any]] = []
    loaded_phase_count = 0
    for spec in PHASE_MATRIX_SPECS:
        meta = root_meta[spec["intake_id"]]
        summary = summaries[spec["intake_id"]]
        loaded_status = "loaded" if meta["loaded"] else "optional_missing"
        if meta["loaded"]:
            loaded_phase_count += 1
        runtime_invoked = _bool_or_false(
            summary,
            "ocr_runtime_invoked",
            "ocr_provider_invoked",
            "ocr_invoked",
            "provider_invoked",
            "new_ocr_invoked",
            "camera_invoked",
            "frame_sampled",
            "regression_runtime_executed",
            "runtime_execution",
        )
        write_boundary_ok = not _bool_or_false(
            summary,
            "world_model_written",
            "memory_written",
            "memory_written_now",
            "fact_written",
            "midplatform_fact_written",
            "scene_delta_generated",
            "scene_delta_candidate_generated",
        ) and summary.get("write_allowed") is False
        completed_phase_rows.append(
            {
                "phase_name": spec["phase_name"],
                "output_dir": str(meta["root"]) if meta["root"] else "(not_provided)",
                "loaded_status": loaded_status,
                "verdict_if_available": _infer_verdict(summary) if meta["loaded"] else "optional_missing",
                "scope": spec["scope"],
                "runtime_invoked": runtime_invoked,
                "write_boundary_status": "NO_WRITE_BOUNDARY_OK" if write_boundary_ok else "WRITE_BOUNDARY_REVIEW_REQUIRED",
                "key_artifacts": spec["key_artifacts"],
                "closure_relevance": spec["closure_relevance"],
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    ocr_phase_verdict_table_loaded = any(
        row["intake_id"] == "ocr_phase_verdict_table" and row["loaded"] for row in input_root_rows
    )
    minimal_runtime_integration_closure_loaded = root_meta["minimal_runtime_integration_closure"]["loaded"]

    mixed_batch_summary = summaries["mixed_batch_v2_gated_path"]
    adapter_summary = summaries["ocr_evidence_pack_adapter_v1"]
    roi_reference_summary = summaries["roi_to_ocrrequest_reference"]
    realvideo_planning_summary = summaries["realvideo_text_bearing_planning"]
    static_rrd_summary = summaries["static_readable_region_discovery"]
    worldmodel_lookup_summary = summaries["worldmodel_lookup_reading_framework"]
    regression_summary = summaries["ocr_regression_route_compliance"]
    mri_closure_summary = summaries["minimal_runtime_integration_closure"]

    ocr_validated_capability_summary = {
        "summary_id": f"{CLOSURE_ID}_validated",
        "ocr_activation_governance_exists": any(
            row["intake_id"] == "ocr_activation_governance" and row["loaded"] for row in input_root_rows
        ),
        "ocrrequest_reference_path_exists": root_meta["roi_to_ocrrequest_reference"]["loaded"],
        "roi_crop_dryrun_reference_path_exists_where_available": root_meta["roi_crop_rerun"]["loaded"]
        or root_meta["roi_to_ocrrequest_reference"]["loaded"],
        "gated_path_replaces_direct_provider_call": mixed_batch_summary.get("uses_gated_runtime_path") is True
        and mixed_batch_summary.get("direct_provider_bypass") is False,
        "evidence_pack_adapter_supports_scan_observation_alignment": adapter_summary.get("based_on_mixed_batch_v2") is True
        and adapter_summary.get("pack_schema_upgraded_to") == "ocr_text_evidence_pack_v1",
        "scan_observation_not_text_evidence": adapter_summary.get("scan_observation_not_primary_evidence") is True,
        "sq_e_low_quality_input_blocked": mixed_batch_summary.get("sq_e_submitted_to_ocr") is False,
        "full_frame_ocr_default_forbidden": mixed_batch_summary.get("full_frame_scan_not_primary_evidence") is True,
        "static_reading_requires_readable_region_discovery": (
            root_meta["static_readable_region_discovery"]["loaded"]
            and static_rrd_summary.get("readable_region_candidate_schema_defined") is True
            and static_rrd_summary.get("static_capture_handoff_policy_defined") is True
            and static_rrd_summary.get("ocrrequest_generated") is False
        ),
        "poster_ocr_uses_segment_first_governance_first_logic": regression_summary.get("poster_route_checked") is True,
        "realvideo_text_bearing_sample_planning_exists": root_meta["realvideo_text_bearing_planning"]["loaded"],
        "empty_ocr_text_is_not_automatically_failure_or_fact": (
            realvideo_planning_summary.get("prior_empty_text_count", 0) >= 0
            and realvideo_planning_summary.get("benchmark_result_claimed") is False
        ),
        "memory_worldmodel_write_remains_blocked": (
            worldmodel_lookup_summary.get("world_model_written") is False
            and worldmodel_lookup_summary.get("memory_written_now") is False
            and mri_closure_summary.get("memory_write_allowed") is False
            and mri_closure_summary.get("worldmodel_write_allowed") is False
        ),
        "ocr_can_support_future_vision_mainline_as_candidate_reference_layer": True,
        "direct_provider_bypass_forbidden": mixed_batch_summary.get("direct_provider_bypass") is False,
        "evidence_pack_not_fact": adapter_summary.get("write_allowed") is False,
        "semantic_candidate_not_fact": mixed_batch_summary.get("world_model_written") is False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    ocr_runtime_disabled_summary = {
        "summary_id": f"{CLOSURE_ID}_runtime_disabled",
        "real_ocr_provider_runtime_allowed": False,
        "ocrrequest_submission_allowed": False,
        "paddleocr_runtime_allowed": False,
        "rapidocr_runtime_allowed": False,
        "deepseek_ocr_runtime_allowed": False,
        "camera_runtime_allowed": False,
        "frame_sampling_runtime_allowed": False,
        "detector_runtime_allowed": False,
        "segmentation_runtime_allowed": False,
        "tracking_runtime_allowed": False,
        "provider_comparison_runtime_allowed": False,
        "benchmark_accuracy_update_allowed": False,
        "memory_write_allowed": False,
        "worldmodel_write_allowed": False,
        "fact_write_allowed": False,
        "scene_delta_commit_allowed": False,
        "navigation_action_allowed": False,
        "task_commit_allowed": False,
        "map_api_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    ocr_non_claims_register = {
        "register_id": f"{CLOSURE_ID}_non_claims",
        "statements": NON_CLAIMS,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_ocr_capability_pool = {
        "pool_id": f"{CLOSURE_ID}_deferred",
        "deferred_capabilities": [
            {
                "capability": item,
                "deferred_from_next_mainline_priority": True,
                "requires_separate_phase": True,
                **_not_fact(),
            }
            for item in DEFERRED_CAPABILITIES
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    ocr_to_vision_handoff_plan = {
        "handoff_id": f"{CLOSURE_ID}_handoff",
        "ocr_future_role_in_vision_mainline": OCR_TO_VISION_ROLES,
        "next_mainline_focus": VISION_NEXT_FOCUS,
        "next_phase_recommendation": PRIMARY_NEXT,
        "must_not_recommend_ocr_provider_runtime_next": True,
        "must_not_recommend_ocr_benchmark_execution_next": True,
        "must_not_recommend_memory_worldmodel_write_next": True,
        "must_not_recommend_map_api_next": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    ocr_mainline_final_closure_report = {
        "closure_id": CLOSURE_ID,
        "closure_scope": "ocr_mainline_final_closure",
        "loaded_phase_count": loaded_phase_count,
        "loaded_phase_refs": [row["phase_name"] for row in completed_phase_rows if row["loaded_status"] == "loaded"],
        "ocr_mainline_status": CURRENT_STATUS,
        "completed_capability_summary": "ocr_validated_capability_summary.json",
        "gated_path_summary": "gated_path_only_replaces_direct_provider_runtime",
        "reference_only_summary": "ocrrequest_reference_and_related_paths_remain_reference_only",
        "readonly_boundary_summary": "readonly_candidate_no_fact_no_write_boundary_maintained",
        "static_reading_link_summary": "static_reading_depends_on_readable_region_and_future_ocrrequest_gate",
        "poster_link_summary": "poster_path_remains_governance_first_segment_first",
        "realvideo_link_summary": "realvideo_path_remains_planning_readonly_and_no_benchmark_claim",
        "worldmodel_memory_link_summary": "worldmodel_and_memory_links_remain_lookup_reference_only",
        "minimal_runtime_integration_link_summary": "aligned_with_text_only_controlled_output_baseline_and_no_write_runtime_boundary",
        "remaining_runtime_disabled_summary": "ocr_runtime_disabled_summary.json",
        "non_claims_register": "ocr_non_claims_register.json",
        "deferred_ocr_capability_pool": "deferred_ocr_capability_pool.json",
        "vision_mainline_handoff_decision": "RETURN_TO_VISION_MAINLINE_AFTER_OCR_CLOSURE",
        "next_phase_recommendation": PRIMARY_NEXT,
        "final_closure_decision": FINAL_DECISION,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommendation_id": f"{CLOSURE_ID}_next_phase",
        "next_phase_recommendation": PRIMARY_NEXT,
        "must_not_recommend_ocr_provider_runtime_next": True,
        "must_not_recommend_ocr_benchmark_execution_next": True,
        "must_not_recommend_memory_worldmodel_write_next": True,
        "must_not_recommend_map_api_next": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    boundary = _boundary_payload()
    return {
        "summary": {
            "phase": PHASE_ID,
            "closure_scope": "ocr_mainline_final_closure_only",
            "closure_only": True,
            "minimal_runtime_integration_closure_loaded": minimal_runtime_integration_closure_loaded,
            "ocr_phase_verdict_table_loaded": ocr_phase_verdict_table_loaded,
            "loaded_phase_count": loaded_phase_count,
            "ocr_completed_phase_matrix_generated": True,
            "ocr_validated_capability_summary_generated": True,
            "ocr_runtime_disabled_summary_generated": True,
            "ocr_non_claims_register_generated": True,
            "deferred_ocr_capability_pool_generated": True,
            "ocr_to_vision_handoff_plan_generated": True,
            "ocr_mainline_status": CURRENT_STATUS,
            "ocr_runtime_allowed": False,
            "ocr_provider_allowed": False,
            "ocrrequest_submission_allowed": False,
            "fact_write_allowed": False,
            "worldmodel_write_allowed": False,
            "memory_write_allowed": False,
            "scene_delta_allowed": False,
            **BOUNDARY_FALSE_FLAGS,
            "boundary_ok": True,
            "violations": [],
            "fact_status": "not_fact",
            "write_allowed": False,
            "final_decision": FINAL_DECISION,
        },
        "input_root_matrix": {
            "row_count": len(input_root_rows),
            "rows": input_root_rows,
            **_not_fact(),
        },
        "ocr_mainline_final_closure_report": ocr_mainline_final_closure_report,
        "ocr_completed_phase_matrix": {
            "loaded_phase_count": loaded_phase_count,
            "rows": completed_phase_rows,
            **_not_fact(),
        },
        "ocr_validated_capability_summary": ocr_validated_capability_summary,
        "ocr_runtime_disabled_summary": ocr_runtime_disabled_summary,
        "ocr_non_claims_register": ocr_non_claims_register,
        "deferred_ocr_capability_pool": deferred_ocr_capability_pool,
        "ocr_to_vision_handoff_plan": ocr_to_vision_handoff_plan,
        "next_phase_recommendation": next_phase_recommendation,
        "no_runtime_boundary_report": boundary,
        "no_write_boundary_report": boundary,
        "debug_refs": {
            "ocr_regression_final_decision_hint": regression_summary.get("final_decision_hint"),
            "roi_reference_count": roi_reference_summary.get("ocrrequest_reference_count"),
            "mixed_batch_ocr_request_count": mixed_batch_summary.get("ocr_request_count"),
            "mixed_batch_semantic_candidate_count": mixed_batch_summary.get("semantic_candidate_count"),
            "adapter_pack_schema": adapter_summary.get("pack_schema_upgraded_to"),
            "realvideo_planning_case_count": realvideo_planning_summary.get("planning_case_count"),
            "worldmodel_lookup_framework_defined": worldmodel_lookup_summary.get("worldmodel_lookup_framework_defined"),
            "mri_closure_final_decision": mri_closure_summary.get("final_decision"),
            **_not_fact(),
        },
        "final": {
            "final_decision": FINAL_DECISION,
            "closure_verdict": "GO" if minimal_runtime_integration_closure_loaded and ocr_phase_verdict_table_loaded else "CONDITIONAL_GO",
            "next_phase_recommendation": PRIMARY_NEXT,
            **_not_fact(),
        },
    }
