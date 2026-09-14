# -*- coding: utf-8 -*-
"""Document Surface — trace schema preflight v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_planning.document_surface_controlled_execution_contract_v1 import (
    build_controlled_execution_trace_template,
)

PREFLIGHT_REQUIRED_FIELDS: List[str] = [
    "execution_id",
    "source_image_ref",
    "source_region_id",
    "attention_gate_status",
    "field_context_candidate",
    "runtime_id",
    "implementation_mode",
    "dependency_status",
    "input_boundary_status",
    "output_boundary_status",
    "candidate_outputs",
    "validation_status_candidate",
    "abort_status",
    "fallback_attempted",
    "ocr_called",
    "vlm_called",
    "layout_called",
]


def _load_trace_schema(repo_root: Path) -> Dict[str, Any]:
    path = repo_root / "capabilities/midplatform/model_manager/runtime/document_surface/controlled_execution_planning/document_surface_runtime_trace_schema_v1.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def run_trace_schema_preflight(*, repo_root: Path) -> Dict[str, Any]:
    schema = _load_trace_schema(repo_root)
    template = build_controlled_execution_trace_template()
    schema_required = schema.get("required") or []
    template_ok = all(f in template for f in PREFLIGHT_REQUIRED_FIELDS)
    flags_ok = (
        template.get("fallback_attempted") is False
        and template.get("ocr_called") is False
        and template.get("vlm_called") is False
        and template.get("layout_called") is False
    )
    return {
        "check_id": "trace_schema_preflight_v1",
        "schema_id": schema.get("schema_id"),
        "preflight_required_fields": PREFLIGHT_REQUIRED_FIELDS,
        "schema_required_fields": schema_required,
        "template_fields_present": template_ok,
        "fallback_attempted_false": template.get("fallback_attempted") is False,
        "ocr_called_false": template.get("ocr_called") is False,
        "vlm_called_false": template.get("vlm_called") is False,
        "layout_called_false": template.get("layout_called") is False,
        "passed": template_ok and flags_ok and len(schema_required) >= 10,
        "candidate_only": True,
        "not_fact": True,
    }
