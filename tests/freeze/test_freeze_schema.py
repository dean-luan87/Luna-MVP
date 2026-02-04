def test_fixture_has_required_sections(freeze_snapshot):
    assert "system_snapshot" in freeze_snapshot
    assert "model_outputs" in freeze_snapshot
    assert "meta" in freeze_snapshot


def test_no_decision_fields_in_fixture(freeze_snapshot):
    forbidden = {
        "decision",
        "selected_result",
        "reason",
        "authority",
        "abilities",
        "risk",
        "c_decision",
    }

    def walk(obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                assert key not in forbidden, f"Forbidden field in fixture: {key}"
                walk(value)
        elif isinstance(obj, list):
            for item in obj:
                walk(item)

    walk(freeze_snapshot)
