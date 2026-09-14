# -*- coding: utf-8 -*-
"""Real observation ingestion result assembler v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List

from capabilities.midplatform.real_observation_candidate_ingestion_types_v1 import NON_EXECUTION_FLAGS


def assemble_real_observation_ingestion_result(
    *,
    accepted_candidates: List[Dict[str, Any]],
    rejected_detections: List[Dict[str, Any]],
    warning_summary: List[str],
    missing_information: List[str],
) -> Dict[str, Any]:
    readiness = len(accepted_candidates) > 0 and all(
        c.get("validation_status") == "valid" and c.get("candidate_only") is True
        for c in accepted_candidates
    )
    return {
        "ingestion_result_id": f"roi_{uuid.uuid4().hex[:12]}",
        "accepted_candidates": accepted_candidates,
        "rejected_detections": rejected_detections,
        "warning_summary": {
            "warnings": warning_summary,
            "warning_count": len(warning_summary),
        },
        "missing_information": missing_information,
        "readiness_for_field_first_core": readiness,
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
    }
