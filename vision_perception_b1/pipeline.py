from __future__ import annotations

from typing import List, Any, Optional

from dynamic_view.roi import RoiHint
from .gate import should_run
from .crop import crop_by_roi
from .ocr_runner import OCRRunner
from .tracker_runner import TrackerRunner
from .adapter import to_reference_cards


_DEFAULT_OCR = OCRRunner()
_DEFAULT_TRACKER = TrackerRunner()


def run_roi_perception(
    frame: Any,
    roi_hints: List[RoiHint],
    *,
    ocr: Optional[OCRRunner] = None,
    tracker: Optional[TrackerRunner] = None,
) -> List:
    if not should_run(roi_hints):
        return []

    ocr = ocr or _DEFAULT_OCR
    tracker = tracker or _DEFAULT_TRACKER

    references = []
    for roi in roi_hints:
        patch = crop_by_roi(frame, roi)
        references.extend(to_reference_cards(ocr.run(patch), roi))
        references.extend(to_reference_cards(tracker.run(patch), roi))
    return references
