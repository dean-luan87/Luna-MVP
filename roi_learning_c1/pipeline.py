from __future__ import annotations

from typing import Dict, Any, List

from roi_learning_c1.reader import read_timeline_jsonl
from roi_learning_c1.metrics import compute_roi_metrics
from roi_learning_c1.proposer import build_proposals
from roi_learning_c1.schema import ROIPromotionProposal


def run_c1_from_timeline(path: str) -> List[ROIPromotionProposal]:
    frames = list(read_timeline_jsonl(path))
    metrics: Dict[str, Dict[str, Any]] = compute_roi_metrics(frames)
    return build_proposals(metrics)
