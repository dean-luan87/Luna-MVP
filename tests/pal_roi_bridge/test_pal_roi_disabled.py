import pal_roi_bridge.config as cfg
from pal_roi_bridge.pipeline import run_pal_roi_pipeline
from pal_roi_bridge.schema import PalRoiHint


def test_a1_disabled(monkeypatch):
    monkeypatch.setattr(cfg, "PAL_ROI_ENABLED", False)
    hint = PalRoiHint(roi_kind="exit_area", area=None, confidence=0.5, reason="x", ttl_s=3.0)
    assert run_pal_roi_pipeline([hint]) == []
