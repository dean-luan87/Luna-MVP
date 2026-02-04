REQUIRED_FIELDS = {
    "authority",
    "abilities",
    "gate",
    "decision",
    "distortion",
    "c_decision",
    "bc_action",
    "can_recover",
}


def test_bc_snapshot_required_fields():
    sample_bc_snapshot = {
        "authority": {},
        "abilities": {},
        "gate": "PASS",
        "decision": "fallback",
        "distortion": {},
        "c_decision": None,
        "bc_action": None,
        "can_recover": None,
    }
    for key in REQUIRED_FIELDS:
        assert key in sample_bc_snapshot


def test_bc_snapshot_not_used_as_input():
    sample_bc_snapshot = {
        "authority": {},
        "abilities": {},
        "gate": "PASS",
        "decision": "fallback",
        "distortion": {},
        "c_decision": None,
        "bc_action": None,
        "can_recover": None,
    }
    forbidden = {"used_as_input", "fed_back"}
    for key in forbidden:
        assert key not in sample_bc_snapshot
