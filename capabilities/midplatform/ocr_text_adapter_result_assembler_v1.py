# -*- coding: utf-8 -*-
"""OCR / Text adapter result assembler v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List

from capabilities.midplatform.ocr_text_adapter_types_v1 import NON_EXECUTION_FLAGS


def assemble_ocr_text_adapter_result(
    *,
    adapter_input: Dict[str, Any],
    raw_output: Dict[str, Any],
    observations: List[Dict[str, Any]],
    regions: List[Dict[str, Any]],
    anchors: List[Dict[str, Any]],
    normalizations: List[Dict[str, Any]],
    qualities: List[Dict[str, Any]],
    warnings: List[str],
    failure_points: List[str],
) -> Dict[str, Any]:
    """Assemble OCRTextAdapterResultCandidate."""
    execution_mode = adapter_input.get("execution_mode", "adapter_stub")
    accepted = len(observations) + len(regions) + len(anchors) + len(normalizations) + len(qualities)
    rejected = len(failure_points)

    later_wm_ready = (bool(observations) or bool(anchors)) and not raw_output.get("_blocked")
    task_ready = later_wm_ready and execution_mode not in (
        "blocked_by_authorization", "blocked_by_missing_dependency", "blocked_by_missing_weight",
    )

    flags = dict(NON_EXECUTION_FLAGS)
    if execution_mode == "cached_output":
        flags["cached_output_not_marked_as_real_run"] = True
    if execution_mode == "adapter_stub":
        flags["adapter_stub_not_marked_as_real_run"] = True

    return {
        "adapter_result_id": f"otar_{uuid.uuid4().hex[:12]}",
        "adapter_input_ref": adapter_input.get("adapter_input_id"),
        "smoke_run_ref": adapter_input.get("smoke_run_ref"),
        "io_inspection_ref": adapter_input.get("io_inspection_ref"),
        "execution_mode": execution_mode,
        "text_observation_candidates": observations,
        "text_region_candidates": regions,
        "text_anchor_candidates": anchors,
        "text_normalization_candidates": normalizations,
        "text_quality_candidates": qualities,
        "accepted_output_count": accepted,
        "rejected_output_count": rejected,
        "missing_information": [w for w in warnings if "missing" in w or "blocked" in w],
        "warning_summary": {"warnings": sorted(set(warnings))},
        "conflict_summary": [],
        "readiness_for_midplatform_task_collaboration": task_ready,
        "readiness_for_later_world_model_candidate_assembly": later_wm_ready,
        "non_execution_flags": flags,
        "source_refs": list(adapter_input.get("source_refs") or []),
        "traceability_refs": list(adapter_input.get("traceability_refs") or []) + [
            o.get("text_observation_candidate_id") for o in observations
        ] + [a.get("text_anchor_candidate_id") for a in anchors],
        "candidate_only": True,
        "world_model_candidate_generated": False,
        "world_model_entry_created": False,
        "world_entity_candidate_generated": False,
        "fact_admission_executed": False,
        "task_action_output": False,
        "navigation_suggestion_output": False,
        "llm_text_correction_executed": False,
    }
