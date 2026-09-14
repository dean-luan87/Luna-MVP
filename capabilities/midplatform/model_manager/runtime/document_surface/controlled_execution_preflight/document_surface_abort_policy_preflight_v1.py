# -*- coding: utf-8 -*-
"""Document Surface — abort policy preflight v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

REQUIRED_ABORT_IDS: List[str] = [
    "attention_gate_not_allowed",
    "input_not_in_registry",
    "dependency_missing",
    "unsupported_image_format",
    "image_read_failed",
    "candidate_output_schema_invalid",
    "output_contains_ocr_text",
    "output_contains_fact",
    "fallback_attempt_detected",
    "runtime_timeout",
    "excessive_candidate_count",
    "write_outside_output_dir",
    "protocol_compliance_failed",
]

REQUIRED_ABORT_ALIASES = {
    "attention_gate_status_not_allowed": "attention_gate_not_allowed",
}


def _load_abort_policy(repo_root: Path) -> Dict[str, Any]:
    path = repo_root / "capabilities/midplatform/model_manager/runtime/document_surface/controlled_execution_planning/document_surface_abort_condition_policy_v1.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def run_abort_policy_preflight(*, repo_root: Path) -> Dict[str, Any]:
    policy = _load_abort_policy(repo_root)
    conditions = policy.get("abort_conditions") or []
    by_id = {c.get("abort_id"): c for c in conditions}

    missing: List[str] = []
    incomplete: List[str] = []
    for aid in REQUIRED_ABORT_IDS:
        cond = by_id.get(aid)
        if not cond:
            missing.append(aid)
            continue
        if not (cond.get("abort_reason") and cond.get("output_candidate") and cond.get("next_action") and cond.get("forbidden_fallback")):
            incomplete.append(aid)

    alias_ok = by_id.get("attention_gate_not_allowed") is not None

    return {
        "check_id": "abort_policy_preflight_v1",
        "required_abort_count": len(REQUIRED_ABORT_IDS),
        "found_abort_count": len(conditions),
        "missing_abort_ids": missing,
        "incomplete_abort_ids": incomplete,
        "attention_gate_alias_ok": alias_ok,
        "all_complete": not missing and not incomplete,
        "passed": not missing and not incomplete and len(conditions) >= 13,
        "candidate_only": True,
        "not_fact": True,
    }
