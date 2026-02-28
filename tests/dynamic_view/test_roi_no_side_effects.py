def test_roi_no_side_effects_imports():
    import dynamic_view.roi as r

    forbidden = ["Task", "CController", "execute"]
    for k in forbidden:
        assert k not in r.__dict__
