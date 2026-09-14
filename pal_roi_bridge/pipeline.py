from __future__ import annotations

from typing import List

from .adapter import convert_pal_to_rois
from .schema import PalRoiHint
from . import config


def run_pal_roi_pipeline(pal_hints: List[PalRoiHint]):
    if not config.PAL_ROI_ENABLED:
        return []
    limited = pal_hints[: config.PAL_ROI_MAX_HINTS]
    return convert_pal_to_rois(limited)
