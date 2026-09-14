import pal_roi_bridge.config as cfg
from pal_roi_bridge.pipeline import run_pal_roi_pipeline
from pal_roi_bridge.schema import PalRoiHint


def test_a1_enabled(monkeypatch):
    monkeypatch.setattr(cfg, "PAL_ROI_ENABLED", True)
    hint = PalRoiHint(roi_kind="exit_area", area=None, confidence=0.5, reason="x", ttl_s=3.0)
    rois = run_pal_roi_pipeline([hint])
    assert len(rois) == 1
