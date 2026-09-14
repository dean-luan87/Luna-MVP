def test_timeline_roi_no_side_effects_imports():
    import observe.timeline_roi as m

    forbidden = ["Task", "CController", "execute"]
    for k in forbidden:
        assert k not in m.__dict__
