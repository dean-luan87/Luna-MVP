from vision_ocr import OcrSignal, OcrSignalNormalizer


def test_normalize_exit_and_elevator():
    n = OcrSignalNormalizer()
    sigs = [
        OcrSignal(text="EXIT", score=0.8),
        OcrSignal(text="电梯", score=0.7),
    ]
    t0 = n.normalize(sigs[0])
    t1 = n.normalize(sigs[1])
    assert any(t.key == "exit" for t in t0)
    assert any(t.key == "elevator" for t in t1)


def test_normalize_metro_line():
    n = OcrSignalNormalizer()
    t = n.normalize(OcrSignal(text="2号线", score=0.6))
    assert any(x.key == "metro_line" and x.value == "2" for x in t)
