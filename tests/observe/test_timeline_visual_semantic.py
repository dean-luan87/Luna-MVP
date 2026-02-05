from observe.timeline.schema import TimelineFrame


def test_visual_semantic_written_to_timeline():
    frame = TimelineFrame(
        ts=0.0,
        entities={},
        tasks=[],
        c_decision={},
    )
    frame.visual_semantic_debug = {
        "roi_kind": "exit_area",
        "interpretations": [],
        "unresolved": True,
    }
    assert frame.visual_semantic_debug["roi_kind"] == "exit_area"
