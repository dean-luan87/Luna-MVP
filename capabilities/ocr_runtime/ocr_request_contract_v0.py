# -*- coding: utf-8 -*-
"""Minimal OCRRequest contract v0 for mainline bridge skeleton."""

from __future__ import annotations

import datetime as _dt
import json
import re
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal, Optional, Tuple

InputTypeV0 = Literal["image_path", "roi", "roi_list"]
UrgencyV0 = Literal["async", "interactive", "background"]
ExpectedOutputV0 = Literal["ocr_evidence"]


@dataclass
class OCRRequestV0:
    schema_version: str = "ocr_request_v0"
    request_id: str = ""
    source_task_id: Optional[str] = None
    task_context: str = "unknown"
    urgency: UrgencyV0 = "async"
    input_type: InputTypeV0 = "image_path"
    image_path: str = ""
    roi_refs: List[str] = field(default_factory=list)
    expected_output: ExpectedOutputV0 = "ocr_evidence"
    latency_budget_ms: int = 3000
    allow_heavy_ocr: bool = False
    allow_remote: bool = False
    allow_full_image: bool = False
    created_at: str = ""
    trace_id: str = ""

    def __post_init__(self) -> None:
        if not self.request_id.strip():
            self.request_id = f"ocr_req_{uuid.uuid4().hex[:16]}"
        if not self.trace_id.strip():
            self.trace_id = f"trace_{uuid.uuid4().hex[:12]}"
        if not self.created_at.strip():
            self.created_at = _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "request_id": self.request_id,
            "source_task_id": self.source_task_id,
            "task_context": self.task_context,
            "urgency": self.urgency,
            "input_type": self.input_type,
            "image_path": self.image_path,
            "roi_refs": list(self.roi_refs),
            "expected_output": self.expected_output,
            "latency_budget_ms": int(self.latency_budget_ms),
            "allow_heavy_ocr": bool(self.allow_heavy_ocr),
            "allow_remote": bool(self.allow_remote),
            "allow_full_image": bool(self.allow_full_image),
            "created_at": self.created_at,
            "trace_id": self.trace_id,
        }


def _parse_one_roi_bbox_string_v0(s: str) -> Optional[List[int]]:
    s = str(s).strip()
    if not s:
        return None
    if s.startswith("["):
        try:
            arr = json.loads(s)
            if isinstance(arr, list) and len(arr) == 4:
                return [int(arr[0]), int(arr[1]), int(arr[2]), int(arr[3])]
        except (json.JSONDecodeError, TypeError, ValueError):
            return None
        return None
    raw = s.replace("ocr_roi_xyxy:", "").strip()
    parts = [p.strip() for p in raw.split(",")]
    if len(parts) != 4:
        return None
    try:
        return [int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3])]
    except ValueError:
        return None


def parse_all_roi_bboxes_xyxy_v0(roi_refs: List[str]) -> List[List[int]]:
    """Parse every ROI ref as ``x0,y0,x1,y1`` (skips empty / invalid entries)."""
    out: List[List[int]] = []
    for ref in roi_refs or []:
        b = _parse_one_roi_bbox_string_v0(str(ref))
        if b:
            out.append(b)
    return out


def parse_roi_bbox_xyxy_v0(roi_refs: List[str]) -> Optional[List[int]]:
    """Parse first ROI as ``x0,y0,x1,y1`` integers (xyxy in original image pixels) or JSON ``[x0,y0,x1,y1]``."""
    allb = parse_all_roi_bboxes_xyxy_v0(roi_refs)
    return allb[0] if allb else None


def validate_ocr_request_v0(req: OCRRequestV0) -> Tuple[bool, List[str]]:
    errs: List[str] = []
    if req.schema_version != "ocr_request_v0":
        errs.append("schema_version_must_be_ocr_request_v0")
    if not req.request_id.strip():
        errs.append("missing_request_id")
    if not req.trace_id.strip():
        errs.append("missing_trace_id")
    if int(req.latency_budget_ms) <= 0:
        errs.append("latency_budget_ms_must_be_positive")
    if req.expected_output != "ocr_evidence":
        errs.append("expected_output_must_be_ocr_evidence")
    if req.input_type == "image_path":
        if not req.image_path.strip():
            errs.append("image_path_required_for_image_path_input")
        elif not re.match(r"^/", req.image_path.strip()):
            errs.append("image_path_must_be_absolute")
    if req.input_type in ("roi", "roi_list"):
        if not req.image_path.strip():
            errs.append("image_path_required_for_roi_input")
        elif not re.match(r"^/", req.image_path.strip()):
            errs.append("image_path_must_be_absolute")
        if not req.roi_refs:
            errs.append("roi_refs_required_for_roi_input")
        elif req.input_type == "roi_list":
            if len(req.roi_refs) < 2:
                errs.append("roi_list_requires_at_least_two_roi_refs")
            else:
                parsed = parse_all_roi_bboxes_xyxy_v0(req.roi_refs)
                if len(parsed) < 2:
                    errs.append("roi_list_requires_at_least_two_parseable_roi_bboxes")
                if len(parsed) != len(req.roi_refs):
                    errs.append("roi_list_contains_unparseable_roi_ref")
        elif parse_roi_bbox_xyxy_v0(req.roi_refs) is None:
            errs.append("roi_refs_unparseable_xyxy_expected")
    return (len(errs) == 0, errs)
