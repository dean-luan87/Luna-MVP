from c1_v0.analyzer import analyze_timeline


def test_analyze_timeline_empty():
    frames = [{"ts": 1.0}, {"ts": 2.0}]
    proposals = analyze_timeline(frames)
    assert proposals == []
