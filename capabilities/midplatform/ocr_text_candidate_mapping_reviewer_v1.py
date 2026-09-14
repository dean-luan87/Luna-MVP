# -*- coding: utf-8 -*-
"""OCR / Text Model candidate mapping reviewer v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional

from capabilities.midplatform.ocr_text_model_smoke_io_inspection_items_v1 import CANDIDATE_MAPPING_TARGETS


def review_ocr_text_candidate_mapping_feasibility(
    *,
    smoke_run: Dict[str, Any],
    io_inspection: Dict[str, Any],
    focus_target: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Review how OCR/text outputs map to existing candidates."""
    raw = smoke_run.get("_raw_output") or {}
    mode = smoke_run.get("execution_mode", "blocked_by_authorization")
    subtype = smoke_run.get("_inspect_subtype", "ocr")
    results: List[Dict[str, Any]] = []

    targets = CANDIDATE_MAPPING_TARGETS
    if focus_target:
        targets = tuple(t for t in CANDIDATE_MAPPING_TARGETS if t["target"] == focus_target)

    key_map = {
        "TextObservationCandidate": "text",
        "TextRegionCandidate": "bbox",
        "TextAnchorCandidate": "text",
        "TextNormalizationCandidate": "normalized_text",
        "TextQualityCandidate": "confidence",
        "TextLayoutCandidate": "layout_block",
    }

    for target in targets:
        mapping_status = "blocked"
        blockers: List[str] = []
        source_refs = list(io_inspection.get("output_sample_refs") or [])

        if mode.startswith("blocked"):
            blockers.append(mode)
        elif mode == "cached_output":
            outputs = raw.get("outputs") or {}
            out_key = key_map.get(target["target"])
            if target["target"] == "TextRegionCandidate" and (outputs.get("bbox") or outputs.get("polygon")):
                mapping_status = "feasible"
            elif target["target"] == "TextAnchorCandidate" and outputs.get("text") and outputs.get("bbox"):
                mapping_status = "feasible"
            elif target["target"] == "TextNormalizationCandidate":
                if outputs.get("normalized_text"):
                    mapping_status = "feasible"
                elif subtype == "text_enhancement" and outputs.get("raw_text"):
                    mapping_status = "feasible"
                else:
                    blockers.append("normalization_output_missing")
            elif out_key and outputs.get(out_key):
                mapping_status = target["status"]
            elif target["target"] == "TextLayoutCandidate" and outputs.get("layout_block"):
                mapping_status = "feasible"
            else:
                blockers.append("output_key_missing")
        elif mode == "adapter_stub":
            mapping_status = "feasible"
        elif mode == "local_real_model" and target["target"] == "TextObservationCandidate":
            mapping_status = "feasible"
        else:
            blockers.append("insufficient_output_for_target")

        results.append({
            "mapping_feasibility_id": f"mcf_{uuid.uuid4().hex[:12]}",
            "model_role": "ocr_text_model",
            "source_output_refs": source_refs,
            "reusable_existing_candidates": [
                "RealFrameInputPackage",
                "ObjectObservationCandidate",
                "MultiModelAlignedObservationCandidate",
                "EnhancedFieldSceneCandidate",
                "FieldGeometryCandidate",
            ],
            "candidate_mapping_targets": [target["target"]],
            "mapping_status": mapping_status,
            "mapping_blockers": blockers,
            "reason_if_new_candidate_needed": None,
            "owner_approval_required_for_new_protocol": False,
            "candidate_only": True,
            "_model_output": target["model_output"],
        })
    return results
