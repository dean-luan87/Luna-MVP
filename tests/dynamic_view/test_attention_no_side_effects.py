def test_no_side_effects_imports():
    import dynamic_view.attention as a

    forbidden = ["Task", "CController", "execute"]
    for k in forbidden:
        assert k not in a.__dict__
