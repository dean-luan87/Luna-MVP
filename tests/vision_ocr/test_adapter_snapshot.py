from vision_ocr import OcrSignal, OcrSemanticPipeline, attach_ocr_reference


def test_attach_reference_does_not_touch_facts():
    ws = {"facts": {"vision": {"entities": ["x"]}}}
    pipe = OcrSemanticPipeline()
    cards = pipe.run([OcrSignal(text="EXIT", score=0.9)])

    out = attach_ocr_reference(ws, cards)
    assert out["facts"] == ws["facts"]
    assert "reference" in out
    assert "ocr_reference_cards" in out["reference"]
    assert out["reference"]["ocr_reference_cards"][0]["meaning"] == "exit"
