# -*- coding: utf-8 -*-
"""OCR Provider Input Pack schema v0 — normalized units for provider consumption only."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List

SCHEMA_VERSION = "ocr_provider_input_pack_v0"


def new_pack_id() -> str:
    return f"pack_{uuid.uuid4().hex[:20]}"


def validate_provider_input_pack_v0(pack: Dict[str, Any]) -> List[str]:
    errs: List[str] = []
    if str(pack.get("schema_version") or "") != SCHEMA_VERSION:
        errs.append("schema_version")
    for k in ("pack_id", "source_image_ref", "image_fingerprint", "input_units", "processing_policy", "source_chain"):
        if k not in pack:
            errs.append(f"missing:{k}")
    units = pack.get("input_units")
    pol = pack.get("processing_policy") if isinstance(pack.get("processing_policy"), dict) else {}
    strat = str(pol.get("strategy") or "")
    if not isinstance(units, list) or not units:
        errs.append("input_units_empty")
    else:
        for i, ux in enumerate(units):
            if not isinstance(ux, dict):
                errs.append(f"input_unit_not_dict:{i}")
                continue
            if str(ux.get("unit_type") or "") == "roi":
                bb = ux.get("bbox_in_original")
                if not isinstance(bb, list) or len(bb) != 4:
                    errs.append(f"roi_unit_bbox_in_original_required_xyxy:{i}")
                if strat == "roi_list":
                    if not str(ux.get("roi_id") or "").strip():
                        errs.append(f"roi_list_unit_missing_roi_id:{i}")
                    if not str(ux.get("unit_id") or "").strip():
                        errs.append(f"roi_list_unit_missing_unit_id:{i}")
    return errs
