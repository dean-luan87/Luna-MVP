# -*- coding: utf-8 -*-
"""Multi-Model alignment result assembler v1."""

from __future__ import annotations

import uuid
from collections import Counter
from typing import Any, Dict, List

from capabilities.midplatform.multi_model_alignment_types_v1 import NON_EXECUTION_FLAGS


def assemble_multi_model_alignment_result(
    *,
    aligned_candidates: List[Dict[str, Any]],
    rejected_outputs: List[Dict[str, Any]],
) -> Dict[str, Any]:
    missing_summary: Dict[str, int] = dict(Counter(
        role for c in aligned_candidates for role in (c.get("missing_model_roles") or [])
    ))
    all_conflicts = [cr for c in aligned_candidates for cr in (c.get("conflict_refs") or [])]
    all_conflicts.extend(cr for r in rejected_outputs for cr in (r.get("conflict_refs") or []))
    all_warnings = [w for c in aligned_candidates for w in (c.get("warning_codes") or [])]
    all_warnings.extend(w for r in rejected_outputs for w in (r.get("warning_codes") or []))

    strong_or_weak = [
        c for c in aligned_candidates
        if c.get("alignment_status") in ("aligned_strong", "aligned_weak", "aligned_degraded")
        and c.get("primary_object_observation_ref")
    ]
    readiness = (
        len(strong_or_weak) > 0
        and all(c.get("candidate_only") is True for c in aligned_candidates)
        and any(c.get("depth_observation_ref") for c in strong_or_weak)
    )

    return {
        "alignment_result_id": f"mar_{uuid.uuid4().hex[:12]}",
        "aligned_candidates": aligned_candidates,
        "rejected_outputs": rejected_outputs,
        "missing_model_roles_summary": missing_summary,
        "conflict_summary": {
            "conflicts": all_conflicts,
            "conflict_count": len(all_conflicts),
        },
        "warning_summary": {
            "warnings": all_warnings,
            "warning_count": len(all_warnings),
        },
        "readiness_for_depth_object_fusion": readiness,
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "candidate_only": True,
    }
