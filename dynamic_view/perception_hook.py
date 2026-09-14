from __future__ import annotations

from typing import List, Protocol

from dynamic_view.roi import RoiHint


class RoiAwareDetector(Protocol):
    """
    感知层可选接口：实现者可忽略 ROI
    """

    def set_roi_hints(self, rois: List[RoiHint]) -> None:
        ...


def apply_roi_if_supported(detector: object, rois: List[RoiHint]) -> None:
    """
    安全应用 ROI：
    - detector 不支持就直接跳过
    - 不抛异常
    """
    if hasattr(detector, "set_roi_hints"):
        try:
            detector.set_roi_hints(rois)
        except Exception:
            pass
