from __future__ import annotations

from typing import Dict, Any

from visual_semantic_interpreter.types import InterpretationResult, VisualContext


def snapshot_visual_semantic_debug(
    ctx: VisualContext,
    result: InterpretationResult,
) -> Dict[str, Any]:
    return {
        "roi_kind": ctx.roi_kind,
        "scene_tags": ctx.scene_tags,
        "interpretations": [
            {
                "meaning": i.meaning,
                "category": i.category,
                "confidence": i.confidence,
                "ambiguity": i.ambiguity,
                "evidence": i.evidence,
            }
            for i in result.interpretations
        ],
        "unresolved": result.unresolved,
    }
