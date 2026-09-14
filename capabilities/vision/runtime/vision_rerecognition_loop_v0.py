# -*- coding: utf-8 -*-
"""
Recognition -> Correction -> Re-recognition Loop v0 (minimal placeholder wiring).

Goal:
- From existing upstream slices (v0), produce ONE needs_rerecognition_candidate (v0) when a
  conservative trigger condition is met.
- Write candidates to runtime_context.metadata["vision_interpretation_candidates_v0"].

Hard boundaries:
- Does NOT trigger real re-recognition execution.
- Does NOT trigger network verification.
- Does NOT drive voice/memory/navigation.
- Does NOT fabricate time/space anchors.
- relevant-only: if no valid upstream input, do not write.
"""

from __future__ import annotations

from dataclasses import replace
from typing import Any, Dict, List, Optional

from capabilities.voice.schemas.voice_runtime_context import VoiceRuntimeContext


def _as_slice_list(slices: Any) -> List[Dict[str, Any]]:
    if slices is None:
        return []
    if isinstance(slices, dict):
        return [slices]
    if isinstance(slices, list):
        out: List[Dict[str, Any]] = []
        for x in slices:
            if isinstance(x, dict):
                out.append(x)
        return out
    return []


def _maybe_build_needs_rerecognition_candidate_from_risk_slice(
    s: Dict[str, Any],
) -> Optional[Dict[str, Any]]:
    if str(s.get("slice_type") or "") != "risk_slice":
        return None

    # Conservative trigger:
    # - risk_level is warning/high (value-carrying)
    # - slice confidence below a threshold -> "high value but not stable enough"
    payload = s.get("payload")
    if not isinstance(payload, dict):
        return None

    rl = str(payload.get("risk_level") or "").strip().lower()
    if rl not in ("warning", "high"):
        return None

    conf = s.get("confidence")
    if not isinstance(conf, (int, float)):
        return None
    if float(conf) >= 0.75:
        return None

    sid = str(s.get("slice_id") or "").strip()
    if not sid:
        return None

    return {
        "candidate_id": f"cand_rerec_v0_from_{sid}",
        "candidate_type": "needs_rerecognition_candidate",
        "source_modules": ["vision.rerecognition_loop_v0"],
        "upstream_slice_refs": [sid],
        "task_relevance": "high",
        "stability": "unstable",
        "confidence": float(conf),
        "conflict_detected": False,
        "needs_rerecognition": True,
        "needs_confirmation": False,
        "network_verify_recommended": False,
        "memory_candidate": False,
        "consume_priority": "high",
        "lane": "fast",
        "can_enter_mid_platform": True,
        "payload": {
            "trigger_reason": "risk_slice_warning_or_high_with_low_confidence",
        },
    }


def maybe_attach_vision_interpretation_candidates_v0_from_slices(
    *,
    runtime_context: Optional[VoiceRuntimeContext],
) -> Optional[VoiceRuntimeContext]:
    """
    relevant-only:
    - If no candidates produced, returns runtime_context unchanged.
    - If candidates already exist, does not override.
    """
    if runtime_context is None:
        return None

    md0 = getattr(runtime_context, "metadata", None)
    if not isinstance(md0, dict):
        return runtime_context

    # Do not override existing producer chain.
    if md0.get("vision_interpretation_candidates_v0") is not None:
        return runtime_context

    slices = md0.get("vision_consumable_slices_v0")
    lst = _as_slice_list(slices)
    if not lst:
        return runtime_context

    cand: Optional[Dict[str, Any]] = None
    for s in lst:
        cand = _maybe_build_needs_rerecognition_candidate_from_risk_slice(s)
        if isinstance(cand, dict):
            break

    if not isinstance(cand, dict):
        return runtime_context

    md = dict(md0)
    md["vision_interpretation_candidates_v0"] = [cand]
    return replace(runtime_context, metadata=md)

