from vision_interpretation.interpreter import interpret_ocr
from vision_interpretation.schema import RawTextCandidate


def test_schema_stability():
    raw = [
        RawTextCandidate(text="EXIT", confidence=0.82),
        RawTextCandidate(text="E X I T", confidence=0.61),
    ]
    out = interpret_ocr(roi_kind="exit_area", raw_text_candidates=raw)

    assert 0.0 <= out.uncertainty <= 1.0
    assert isinstance(out.interpreted_meanings, list)
    assert out.raw_text_candidates == raw
