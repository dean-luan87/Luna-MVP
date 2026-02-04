def test_replay_is_structurally_stable(controller, freeze_inputs):
    r1 = controller.process(
        "NAVIGATION",
        freeze_inputs["model_outputs"],
        freeze_inputs["system_snapshot"],
    )
    r2 = controller.process(
        "NAVIGATION",
        freeze_inputs["model_outputs"],
        freeze_inputs["system_snapshot"],
    )

    assert set(r1.keys()) == set(r2.keys())
    assert set(r1["decision_trace"].keys()) == set(r2["decision_trace"].keys())
