# -*- coding: utf-8 -*-
"""Document Surface — Option B output contract v1."""

from __future__ import annotations

from typing import Any, Dict, List

from capabilities.midplatform.model_manager.runtime.document_surface.option_b_candidate_route_dryrun.document_surface_option_b_types_v1 import (
    ALLOWED_OUTPUT_TYPES,
    FORBIDDEN_OUTPUT_TYPES,
)


def validate_option_b_output_contract(outputs: Dict[str, Any]) -> Dict[str, Any]:
    violations: List[str] = []
    for key in outputs:
        kl = str(key).lower()
        if kl in FORBIDDEN_OUTPUT_TYPES or any(f in kl for f in ("ocr_text", "_fact", "document_content")):
            if not kl.startswith("no_") and "not_" not in kl:
                violations.append(key)
    out_types = outputs.get("output_types") or list(ALLOWED_OUTPUT_TYPES)
    for t in out_types:
        if t not in ALLOWED_OUTPUT_TYPES:
            violations.append(f"disallowed_type:{t}")
    return {
        "contract_id": "document_surface_option_b_output_contract_v1",
        "allowed_output_types": sorted(ALLOWED_OUTPUT_TYPES),
        "forbidden_output_types": sorted(FORBIDDEN_OUTPUT_TYPES),
        "contract_compliant": len(violations) == 0,
        "violations": violations,
        "candidate_only": True,
        "not_fact": True,
    }
