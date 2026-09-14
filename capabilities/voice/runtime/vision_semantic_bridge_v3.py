# -*- coding: utf-8 -*-
"""
Luna Voice V3: Vision-to-Semantic Bridge (stub v0).

This is a metadata-only, read-only bridge that:
- reads ONLY summary-level inputs from runtime_context.metadata
- builds a minimal JSON-serializable pack
- MUST NOT fabricate facts
- MUST NOT generate system-level time/space anchors
- MUST NOT pass raw detector/OCR/boxes through
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from capabilities.voice.schemas.voice_runtime_context import VoiceRuntimeContext


_ALLOWED_SUMMARY_KEYS_V0: List[str] = [
    "sidewalk_env_summary_v1",
    "retail_env_summary_v1",
    "risk_summary_v1",
]


def build_vision_semantic_input_pack_v0(
    runtime_context: Optional[VoiceRuntimeContext],
) -> Optional[Dict[str, Any]]:
    """
    Build a minimal VisionSemanticInputPack v0 from runtime_context.metadata.

    Returns:
    - dict: when at least one allowed summary exists and is a dict
    - None: when no allowed summaries present / runtime_context missing
    """
    if runtime_context is None:
        return None
    md = getattr(runtime_context, "metadata", None)
    if not isinstance(md, dict) or not md:
        return None

    present: List[str] = []
    for k in _ALLOWED_SUMMARY_KEYS_V0:
        if isinstance(md.get(k), dict):
            present.append(k)

    if not present:
        return None

    # v0 is intentionally conservative: it does not interpret any facts yet.
    pack: Dict[str, Any] = {
        "version": "v3_stub",
        "source_summaries": list(present),  # source keys only; not a claim of truth
        "scene_type": None,
        "task_relevant_facts": [],
        "risk_facts": [],
        "environment_facts": [],
        "uncertainties": ["vision_summary_present_but_not_yet_interpreted"],
        "confidence": 0.0,
        "anchor_ref": None,
    }
    return pack

