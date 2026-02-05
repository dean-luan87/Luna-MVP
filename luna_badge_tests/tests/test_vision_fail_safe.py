from core.vision.vision_fail_safe import VisionFailSafe, FailSafeConfig


def test_fail_safe_enters_degraded():
    cfg = FailSafeConfig(timeout_threshold=1, model_error_threshold=1, camera_error_threshold=1, cooldown_seconds=0)
    fs = VisionFailSafe(cfg)

    fs.report_infer_timeout()
    assert fs.get_state() == "degraded"




