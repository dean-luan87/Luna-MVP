def test_freeze_does_not_mutate_snapshot(controller, freeze_snapshot, freeze_inputs):
    import copy

    snapshot_copy = copy.deepcopy(freeze_snapshot)
    controller.process(
        task_domain="NAVIGATION",
        model_outputs=freeze_inputs["model_outputs"],
        system_snapshot=freeze_inputs["system_snapshot"],
    )
    assert freeze_snapshot == snapshot_copy, "Freeze snapshot was mutated"


def test_freeze_output_contains_bc_snapshot(controller, freeze_inputs):
    result = controller.process(
        task_domain="NAVIGATION",
        model_outputs=freeze_inputs["model_outputs"],
        system_snapshot=freeze_inputs["system_snapshot"],
    )
    trace = result["decision_trace"]
    assert "bc_snapshot" in trace
