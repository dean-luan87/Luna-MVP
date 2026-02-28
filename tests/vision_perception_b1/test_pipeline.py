from dynamic_view.roi import RoiHint

from vision_perception_b1.pipeline import run_roi_perception


class _CounterRunner:
    def __init__(self, out):
        self.calls = 0
        self.out = out

    def run(self, image):
        self.calls += 1
        return list(self.out)


def test_pipeline_no_roi_no_run():
    ocr = _CounterRunner([{"text": "EXIT", "confidence": 0.4}])
    tracker = _CounterRunner([{"label": "person", "confidence": 0.6}])
    out = run_roi_perception(frame=[[0]], roi_hints=[], ocr=ocr, tracker=tracker)
    assert out == []
    assert ocr.calls == 0
    assert tracker.calls == 0


def test_pipeline_runs_on_roi():
    ocr = _CounterRunner([{"text": "EXIT", "confidence": 0.4}])
    tracker = _CounterRunner([{"label": "person", "confidence": 0.6}])
    roi = RoiHint(area_type="x", hint="h", bbox=(0, 0, 1, 1))
    out = run_roi_perception(frame=[[0]], roi_hints=[roi], ocr=ocr, tracker=tracker)
    assert len(out) == 2
    assert ocr.calls == 1
    assert tracker.calls == 1
