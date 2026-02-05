def test_provider_has_no_side_effects():
    import map_d0.candidate_provider as m

    src = m.__dict__
    forbidden = ["DynamicView", "Task", "CController"]
    for k in forbidden:
        assert k not in src
