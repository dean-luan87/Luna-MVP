"""
Phase-Model-002

Model Candidate Adapter v0

Responsibilities:
- Enforce input boundary policy at the adapter boundary (detect/strip forbidden input keys).
- Parse model raw output (strict JSON expected; fallback on malformed JSON).
- Enforce output contract: allowlist output kinds only; block forbidden output kinds/semantics.
- Map to candidate schema v0 for whitebox/replay.
- Never produce executable commands; on any failure, fallback to baseline.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional, Tuple


ALLOWED_OUTPUT_KINDS_V0 = {
    "candidate",
    "draft_explanation",
    "structured_suggestion",
    "confidence_hint",
    "comparison_hint",
}

FORBIDDEN_OUTPUT_KINDS_V0 = {
    "execute_now",
    "open_release_window",
    "retry_now",
    "reopen_now",
    "enable_default_path",
    "override_governance",
    "grant_control",
    "long_running_enablement",
}

# Input boundary: forbidden key names (v0 minimal filter).
FORBIDDEN_INPUT_KEYS_V0 = {
    "side_effects_released",
    "release_window",
    "enable_default_path",
    "default_path_enabled",
    "start_event_observed",
    "allows_next_runtime_now",
    "grant_control",
    "override_governance",
    "manual_override_token",
    "trigger_execute",
    "trigger_retry",
    "trigger_reopen",
}


def _strip_forbidden_inputs(summary: Mapping[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Returns (sanitized_summary, report).
    This is a shallow filter only (v0); callers must only pass restricted summaries anyway.
    """
    sanitized: Dict[str, Any] = {}
    blocked: Dict[str, Any] = {}
    for k, v in summary.items():
        if str(k) in FORBIDDEN_INPUT_KEYS_V0:
            blocked[str(k)] = "<blocked>"
        else:
            sanitized[str(k)] = v
    report = {
        "forbidden_input_keys_seen": sorted(blocked.keys()),
        "forbidden_input_blocked": bool(blocked),
    }
    return sanitized, report


def _contains_forbidden_semantics(obj: Any) -> bool:
    """
    Minimal semantics scan (v0): search string values for forbidden tokens.
    """
    forbidden_tokens = [
        "execute_now",
        "open_release_window",
        "retry_now",
        "reopen_now",
        "enable_default_path",
        "override_governance",
        "grant_control",
        "long_running_enablement",
    ]
    if isinstance(obj, str):
        s = obj.lower()
        return any(t in s for t in forbidden_tokens)
    if isinstance(obj, dict):
        return any(_contains_forbidden_semantics(k) or _contains_forbidden_semantics(v) for k, v in obj.items())
    if isinstance(obj, list):
        return any(_contains_forbidden_semantics(x) for x in obj)
    return False


@dataclass(frozen=True)
class AdaptedCandidateResultV0:
    input_boundary_applied: bool
    candidate_generated: bool
    candidate_schema_valid: bool
    forbidden_output_blocked: bool
    baseline_fallback_used: bool
    illegal_state_detected: bool
    adapter_notes: Dict[str, Any]
    candidate_schema_v0: Optional[Dict[str, Any]]


def adapt_model_output_to_candidate_schema_v0(
    *,
    raw_output: str,
    request_id: str,
    timestamp: float,
    model_id: str,
    model_version: str,
    input_hash: str,
    prompt_hash: str,
    restricted_context_summary: Mapping[str, Any],
) -> AdaptedCandidateResultV0:
    """
    Enforce Model-001 contracts and produce candidate schema v0 (or fallback).
    """
    sanitized_summary, in_report = _strip_forbidden_inputs(restricted_context_summary)
    input_boundary_applied = True

    notes: Dict[str, Any] = {
        "input_boundary": in_report,
        "parse_error": None,
        "output_kind": None,
        "forbidden_semantics_detected": False,
    }

    # If forbidden inputs were present, we still proceed but record; do not forward blocked keys.
    parsed: Optional[Dict[str, Any]] = None
    try:
        parsed_any = json.loads(raw_output)
        if not isinstance(parsed_any, dict):
            raise ValueError("output_not_object")
        parsed = parsed_any
    except Exception as e:  # noqa: BLE001
        notes["parse_error"] = f"{type(e).__name__}:{e}"
        return AdaptedCandidateResultV0(
            input_boundary_applied=input_boundary_applied,
            candidate_generated=False,
            candidate_schema_valid=False,
            forbidden_output_blocked=False,
            baseline_fallback_used=True,
            illegal_state_detected=False,
            adapter_notes=notes,
            candidate_schema_v0=None,
        )

    output_kind = str(parsed.get("output_kind") or parsed.get("kind") or "candidate")
    notes["output_kind"] = output_kind

    forbidden_semantics = _contains_forbidden_semantics(parsed)
    notes["forbidden_semantics_detected"] = forbidden_semantics

    forbidden_blocked = False
    illegal_state_detected = False

    if output_kind in FORBIDDEN_OUTPUT_KINDS_V0 or forbidden_semantics:
        forbidden_blocked = True
        illegal_state_detected = True
        # Block and fallback to baseline (do not propagate any candidate).
        return AdaptedCandidateResultV0(
            input_boundary_applied=input_boundary_applied,
            candidate_generated=False,
            candidate_schema_valid=False,
            forbidden_output_blocked=True,
            baseline_fallback_used=True,
            illegal_state_detected=illegal_state_detected,
            adapter_notes=notes,
            candidate_schema_v0={
                "schema_version": "candidate_schema_v0",
                "policy_version": "phase_model_001_v0",
                "request_id": request_id,
                "timestamp": str(timestamp),
                "model_id": model_id,
                "model_version": model_version,
                "input_hash": input_hash,
                "prompt_hash": prompt_hash,
                "output_kind": "candidate",
                "candidates": [],
                "comparisons": [],
                "draft_explanation": {"text": "", "structure": {}},
                "meta": {"parse_warnings": ["forbidden_output_blocked"], "redaction_summary": ""},
            },
        )

    if output_kind not in ALLOWED_OUTPUT_KINDS_V0:
        # Unknown output kind -> illegal state -> baseline fallback.
        illegal_state_detected = True
        return AdaptedCandidateResultV0(
            input_boundary_applied=input_boundary_applied,
            candidate_generated=False,
            candidate_schema_valid=False,
            forbidden_output_blocked=False,
            baseline_fallback_used=True,
            illegal_state_detected=illegal_state_detected,
            adapter_notes=notes,
            candidate_schema_v0=None,
        )

    # Map into candidate schema v0 (v0 minimal mapping).
    candidates = parsed.get("candidates")
    if not isinstance(candidates, list):
        candidates = []

    out_schema: Dict[str, Any] = {
        "schema_version": "candidate_schema_v0",
        "policy_version": "phase_model_001_v0",
        "request_id": request_id,
        "timestamp": str(timestamp),
        "model_id": model_id,
        "model_version": model_version,
        "input_hash": input_hash,
        "prompt_hash": prompt_hash,
        "output_kind": output_kind,
        "candidates": [],
        "comparisons": parsed.get("comparisons", []) if isinstance(parsed.get("comparisons"), list) else [],
        "draft_explanation": parsed.get("draft_explanation", {"text": "", "structure": {}}),
        "meta": {"parse_warnings": [], "redaction_summary": parsed.get("redaction_summary", "")},
    }

    for idx, c in enumerate(candidates):
        if not isinstance(c, dict):
            continue
        # Drop any forbidden semantics at per-candidate granularity.
        if _contains_forbidden_semantics(c):
            forbidden_blocked = True
            illegal_state_detected = True
            continue
        out_schema["candidates"].append(
            {
                "candidate_id": str(c.get("candidate_id") or f"c{idx}"),
                "candidate_type": str(c.get("candidate_type") or "unknown"),
                "summary": str(c.get("summary") or ""),
                "structured_fields": c.get("structured_fields", {}) if isinstance(c.get("structured_fields"), dict) else {},
                "confidence": c.get("confidence", {"score": 0.0, "calibration_hint": ""}),
                "reason_codes": c.get("reason_codes", []) if isinstance(c.get("reason_codes"), list) else [],
                "evidence_pointers": c.get("evidence_pointers", []) if isinstance(c.get("evidence_pointers"), list) else [],
                "safety_notes": c.get("safety_notes", []) if isinstance(c.get("safety_notes"), list) else [],
            }
        )

    candidate_generated = len(out_schema["candidates"]) > 0 or output_kind != "candidate"
    candidate_schema_valid = True

    notes["sanitized_input_summary_keys"] = sorted(sanitized_summary.keys())

    return AdaptedCandidateResultV0(
        input_boundary_applied=input_boundary_applied,
        candidate_generated=candidate_generated,
        candidate_schema_valid=candidate_schema_valid,
        forbidden_output_blocked=forbidden_blocked,
        baseline_fallback_used=False,
        illegal_state_detected=illegal_state_detected,
        adapter_notes=notes,
        candidate_schema_v0=out_schema,
    )

