from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping, Sequence


def _stable_hash(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def build_ocr_manager_trace_replay_v1(
    *,
    request_id: str,
    source_refs: Sequence[str],
    engine_snapshot: Mapping[str, Any],
    ocr_contract_version: str,
    enhancement_version: str,
    correction_refs: Sequence[str],
    input_payload: Mapping[str, Any],
    result_summary: Mapping[str, Any],
) -> Mapping[str, str]:
    input_hash = _stable_hash(input_payload)
    result_hash = _stable_hash(result_summary)
    trace_basis = {
        "request_id": request_id,
        "source_refs": tuple(source_refs),
        "engine_snapshot": engine_snapshot,
        "ocr_contract_version": ocr_contract_version,
        "enhancement_version": enhancement_version,
        "correction_refs": tuple(correction_refs),
        "input_hash": input_hash,
        "result_hash": result_hash,
    }
    trace_hash = _stable_hash(trace_basis)
    trace_ref = f"ocr_mgr_trace_{request_id}_{trace_hash[:16]}"
    replay_key = f"ocr_mgr_replay_{request_id}_{input_hash[:12]}_{result_hash[:12]}"
    return {
        "trace_ref": trace_ref,
        "replay_key": replay_key,
        "input_hash": input_hash,
        "result_hash": result_hash,
    }
