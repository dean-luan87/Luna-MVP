# -*- coding: utf-8 -*-
"""
Vision mainline minimal wiring v0.

Goal (P1-3):
- Convert an existing vision-related summary input into ONE minimal consumable slice.
- Write it into runtime_context.metadata["vision_consumable_slices_v0"] for mid-platform consume stub.

Hard boundaries:
- No model usage; no extra dispatch/decision.
- No Fabrication: do NOT create slice if input is missing/invalid; do NOT fill missing input fields.
- Do NOT generate time/space anchors.
- Do NOT write memory/navigation/voice outputs.
"""

from __future__ import annotations

from dataclasses import replace
from typing import Any, Dict, List, Optional, Tuple

from capabilities.voice.schemas.voice_runtime_context import VoiceRuntimeContext


_ALLOWED_RISK_LEVELS_V0: Tuple[str, ...] = ("none", "warning", "high")


def _risk_summary_v1_min_ready(rs: Any) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Minimal structural readiness check for risk_summary_v1.
    This is NOT a gate; it only prevents fabrication for the wiring stub.
    """
    if not isinstance(rs, dict) or not rs:
        return False, None

    # Required by the frozen gate-ready contract (see voice_risk_gate_ready_eval_v0).
    risk_level = rs.get("risk_level")
    risk_type = rs.get("risk_type")
    risk_reason = rs.get("risk_reason")
    confidence = rs.get("confidence")
    source = rs.get("source")
    is_gate_ready = rs.get("is_gate_ready")

    if risk_level is None or str(risk_level).strip() == "":
        return False, None
    rl = str(risk_level).strip().lower()
    if rl not in _ALLOWED_RISK_LEVELS_V0:
        return False, None
    if risk_type is None or str(risk_type).strip() == "":
        return False, None
    if risk_reason is None or str(risk_reason).strip() == "":
        return False, None
    if not isinstance(confidence, (int, float)):
        return False, None
    if source is None or str(source).strip() == "":
        return False, None
    if not isinstance(is_gate_ready, bool) or is_gate_ready is not True:
        return False, None

    return True, rs


def _build_risk_slice_from_risk_summary_v1(rs: Dict[str, Any]) -> Dict[str, Any]:
    # NOTE: payload is a subset mirror; no inference.
    rt = str(rs.get("risk_type") or "").strip()
    slice_id = f"risk_slice_v0_{rt[:24] or 'unknown'}"
    return {
        "slice_id": slice_id,
        "slice_type": "risk_slice",
        "source_modules": ["vision.mainline_minimal_wiring_v0"],
        "task_relevance": "unknown",
        "stability": "unstable",
        "confidence": float(rs.get("confidence") or 0.0),
        "needs_rerecognition": False,
        "needs_confirmation": False,
        "network_allowed": False,
        "memory_worthy": False,
        "consume_priority": "normal",
        "lane": "fast",
        "can_enter_mainline": False,
        "payload": {
            "risk_level": str(rs.get("risk_level") or "").strip().lower(),
            "risk_type": str(rs.get("risk_type") or "").strip(),
            "risk_reason": str(rs.get("risk_reason") or "").strip(),
            "source": str(rs.get("source") or "").strip(),
            "is_gate_ready": bool(rs.get("is_gate_ready") is True),
        },
    }


def maybe_attach_vision_consumable_slices_v0_from_risk_summary_v1(
    *,
    runtime_context: Optional[VoiceRuntimeContext],
) -> Optional[VoiceRuntimeContext]:
    """
    relevant-only:
    - returns the original runtime_context when not applicable or already has slices.
    - returns a replaced runtime_context when a valid slice is produced.
    """
    if runtime_context is None:
        return None

    md0 = getattr(runtime_context, "metadata", None)
    if not isinstance(md0, dict):
        return runtime_context

    # Do not override existing producer chain.
    if md0.get("vision_consumable_slices_v0") is not None:
        return runtime_context

    rs = md0.get("risk_summary_v1")
    ok, rs2 = _risk_summary_v1_min_ready(rs)
    if not ok or not isinstance(rs2, dict):
        return runtime_context

    sl = _build_risk_slice_from_risk_summary_v1(rs2)

    md = dict(md0)
    md["vision_consumable_slices_v0"] = [sl]
    return replace(runtime_context, metadata=md)

