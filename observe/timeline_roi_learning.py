from __future__ import annotations

from typing import Any, Dict, List

from roi_learning_c1.schema import ROIPromotionProposal


def snapshot_roi_learning_debug(
    proposals: List[ROIPromotionProposal],
    version: str = "c1-v0",
) -> Dict[str, Any]:
    """
    Debug-only snapshot.
    - No side effects
    - Safe when proposals is empty
    """
    if not proposals:
        return {}

    return {
        "roi_learning_debug": {
            "version": version,
            "proposals": [
                {
                    "roi_kind": p.roi_kind,
                    "score": p.score,
                    "suggestion": p.suggestion,
                    "confidence": p.confidence,
                    "evidence": p.evidence,
                }
                for p in proposals
            ],
        }
    }
