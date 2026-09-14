"""
Phase-Model-002

Navigation Single Model Shadow Integration Implementation v0

Hard boundaries (must hold):
- Non-default explicit enable flag; default disabled.
- Single model only; no model pool, no scheduler, no multi-model fallback.
- Shadow / candidate-only: never triggers execute/retry/reopen/release; no real side effects expansion.
- Input boundary must be applied (forbidden inputs filtered/blocked).
- Output contract must be applied (candidate schema v0; forbidden outputs blocked).
- Must be auditable, replayable, disableable, and able to rollback-to-baseline on failure.
"""

from __future__ import annotations

import json
import os
import time
import uuid
from dataclasses import dataclass
from typing import Any, Callable, Dict, Mapping, Optional

from capabilities.model_integration.model_candidate_adapter_v0 import (
    AdaptedCandidateResultV0,
    adapt_model_output_to_candidate_schema_v0,
)


ModelCallable = Callable[[Mapping[str, Any]], str]


DEFAULT_WHITEBOX_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "var", "model_whitebox")
DEFAULT_REPLAY_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "var", "model_replay")


def _ensure_dir(p: str) -> None:
    os.makedirs(p, exist_ok=True)


def _write_jsonl(path: str, record: Dict[str, Any]) -> None:
    _ensure_dir(os.path.dirname(path))
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False, sort_keys=False) + "\n")


def _hash_fingerprint(obj: Any) -> str:
    # Stable-enough v0 fingerprint (not cryptographic).
    try:
        s = json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    except Exception:
        s = repr(obj)
    return str(abs(hash(s)))


@dataclass(frozen=True)
class ShadowIntegrationInputV0:
    """
    Input to single-model shadow integration.
    This layer is intentionally read-only; it never returns any executable command.
    """

    explicit_model_integration_enable_v0: bool
    model_name: str
    model_call: ModelCallable
    restricted_context_summary: Mapping[str, Any]

    # Control plane / safety
    disable_switch: bool = False
    request_id: Optional[str] = None

    # Output sinks
    whitebox_dir: str = DEFAULT_WHITEBOX_DIR
    replay_dir: str = DEFAULT_REPLAY_DIR


def run_single_model_shadow_integration_v0(inp: ShadowIntegrationInputV0) -> Dict[str, Any]:
    """
    Run single model shadow integration (candidate-only).

    Returns a structured dict with required visibility fields (Phase-Model-002).
    """

    request_id = inp.request_id or f"m002-{uuid.uuid4()}"
    ts = time.time()

    # A. Explicit enable + runtime disable switch.
    model_enabled_seen = bool(inp.explicit_model_integration_enable_v0) and (not bool(inp.disable_switch))
    model_disabled_fallback_available = True

    baseline_fallback_used = False
    model_invoked = False
    candidate_generated = False
    candidate_schema_valid = False
    forbidden_output_blocked = False
    input_boundary_applied = False
    output_contract_applied = False
    written_to_whitebox = False
    replay_record_ready = False
    illegal_state_detected = False

    # Base whitebox record.
    whitebox_path = os.path.join(inp.whitebox_dir, "model_shadow_whitebox_v0.jsonl")
    replay_path = os.path.join(inp.replay_dir, "model_shadow_replay_v0.jsonl")

    # Default: if not enabled, do not call model; return baseline.
    if not model_enabled_seen:
        baseline_fallback_used = True
        record = {
            "request_id": request_id,
            "timestamp": ts,
            "model_enabled_seen": model_enabled_seen,
            "model_invoked": False,
            "baseline_fallback_used": True,
            "reason": "model_disabled_by_default_or_runtime_disable",
        }
        _write_jsonl(whitebox_path, record)
        written_to_whitebox = True
        replay_record_ready = True
        _write_jsonl(replay_path, {"request_id": request_id, "timestamp": ts, "replay_kind": "baseline_only"})
        return {
            "model_enabled_seen": model_enabled_seen,
            "model_invoked": model_invoked,
            "model_name": inp.model_name,
            "input_boundary_applied": False,
            "output_contract_applied": False,
            "candidate_generated": False,
            "candidate_schema_valid": False,
            "forbidden_output_blocked": False,
            "written_to_whitebox": written_to_whitebox,
            "replay_record_ready": replay_record_ready,
            "model_disabled_fallback_available": model_disabled_fallback_available,
            "baseline_fallback_used": baseline_fallback_used,
            "illegal_state_detected": False,
            "whitebox_path": whitebox_path,
            "replay_path": replay_path,
            "no_execution_side_effects": True,
        }

    # C. Apply input boundary (policy enforcement is in adapter; this runtime just uses the adapter report).
    input_hash = _hash_fingerprint(inp.restricted_context_summary)
    prompt_hash = _hash_fingerprint({"model_name": inp.model_name, "policy": "phase_model_001_v0"})

    # Invoke model with restricted context summary (shadow).
    raw_output: Optional[str] = None
    err: Optional[str] = None
    try:
        model_invoked = True
        raw_output = inp.model_call(inp.restricted_context_summary)
    except TimeoutError as e:
        err = f"timeout:{e}"
    except Exception as e:  # noqa: BLE001
        err = f"exception:{type(e).__name__}:{e}"

    if err is not None:
        baseline_fallback_used = True
        record = {
            "request_id": request_id,
            "timestamp": ts,
            "model_enabled_seen": model_enabled_seen,
            "model_invoked": model_invoked,
            "model_name": inp.model_name,
            "input_hash": input_hash,
            "prompt_hash": prompt_hash,
            "error": err,
            "baseline_fallback_used": True,
        }
        _write_jsonl(whitebox_path, record)
        written_to_whitebox = True
        _write_jsonl(replay_path, {"request_id": request_id, "timestamp": ts, "replay_kind": "fallback_error", "error": err})
        replay_record_ready = True
        return {
            "model_enabled_seen": model_enabled_seen,
            "model_invoked": model_invoked,
            "model_name": inp.model_name,
            "input_boundary_applied": False,
            "output_contract_applied": False,
            "candidate_generated": False,
            "candidate_schema_valid": False,
            "forbidden_output_blocked": False,
            "written_to_whitebox": written_to_whitebox,
            "replay_record_ready": replay_record_ready,
            "model_disabled_fallback_available": model_disabled_fallback_available,
            "baseline_fallback_used": baseline_fallback_used,
            "illegal_state_detected": False,
            "whitebox_path": whitebox_path,
            "replay_path": replay_path,
            "no_execution_side_effects": True,
        }

    # D. Apply output contract + candidate schema mapping.
    adapted: AdaptedCandidateResultV0 = adapt_model_output_to_candidate_schema_v0(
        raw_output=raw_output or "",
        request_id=request_id,
        timestamp=ts,
        model_id=inp.model_name,
        model_version="unknown",
        input_hash=input_hash,
        prompt_hash=prompt_hash,
        restricted_context_summary=inp.restricted_context_summary,
    )
    input_boundary_applied = adapted.input_boundary_applied
    output_contract_applied = True
    forbidden_output_blocked = adapted.forbidden_output_blocked
    candidate_generated = adapted.candidate_generated
    candidate_schema_valid = adapted.candidate_schema_valid
    illegal_state_detected = adapted.illegal_state_detected

    if adapted.baseline_fallback_used:
        baseline_fallback_used = True

    # E. Whitebox + replay writes.
    _write_jsonl(
        whitebox_path,
        {
            "request_id": request_id,
            "timestamp": ts,
            "model_enabled_seen": model_enabled_seen,
            "model_invoked": model_invoked,
            "model_name": inp.model_name,
            "input_boundary_applied": input_boundary_applied,
            "output_contract_applied": output_contract_applied,
            "candidate_generated": candidate_generated,
            "candidate_schema_valid": candidate_schema_valid,
            "forbidden_output_blocked": forbidden_output_blocked,
            "baseline_fallback_used": baseline_fallback_used,
            "illegal_state_detected": illegal_state_detected,
            "adapter_notes": adapted.adapter_notes,
        },
    )
    written_to_whitebox = True

    _write_jsonl(
        replay_path,
        {
            "request_id": request_id,
            "timestamp": ts,
            "replay_kind": "model_output",
            "model_name": inp.model_name,
            "candidate_schema_v0": adapted.candidate_schema_v0,
            "baseline_fallback_used": baseline_fallback_used,
            "adapter_notes": adapted.adapter_notes,
        },
    )
    replay_record_ready = True

    # F. Shadow: return structured status only; never returns executable action.
    return {
        "model_enabled_seen": model_enabled_seen,
        "model_invoked": model_invoked,
        "model_name": inp.model_name,
        "input_boundary_applied": input_boundary_applied,
        "output_contract_applied": output_contract_applied,
        "candidate_generated": candidate_generated,
        "candidate_schema_valid": candidate_schema_valid,
        "forbidden_output_blocked": forbidden_output_blocked,
        "written_to_whitebox": written_to_whitebox,
        "replay_record_ready": replay_record_ready,
        "model_disabled_fallback_available": model_disabled_fallback_available,
        "baseline_fallback_used": baseline_fallback_used,
        "illegal_state_detected": illegal_state_detected,
        "whitebox_path": whitebox_path,
        "replay_path": replay_path,
        # Explicit guardrail: no execution outputs.
        "no_execution_side_effects": True,
    }

