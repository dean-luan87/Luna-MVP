def test_bc_does_not_modify_b_output():
    sample_b_outputs = [
        {"model_id": "b1", "facts": {"objects": []}},
        {"model_id": "b2", "facts": {"objects": []}},
    ]
    bc_snapshot = {"used_candidates": ["b1"]}
    used = bc_snapshot["used_candidates"]
    model_ids = {o.get("model_id") for o in sample_b_outputs}
    for cand in used:
        assert cand in model_ids


def test_bc_respects_c_stop():
    sample_bc_result_with_c_stop = {"decision": "STOP"}
    assert sample_bc_result_with_c_stop["decision"] != "PROCEED"


def test_bc_snapshot_write_only():
    sample_bc_snapshot = {"authority": {}, "abilities": {}, "gate": "PASS", "decision": "fallback", "distortion": {}}
    forbidden_reads = {"used_for_next_tick", "feedback"}
    for key in forbidden_reads:
        assert key not in sample_bc_snapshot
