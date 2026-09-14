from vision_ocr import ReferenceCard, reference_to_change_demands


def test_reference_to_change_demand_is_suggest_only():
    cards = [
        ReferenceCard(kind="signage", meaning="exit", confidence=0.7),
    ]
    demands = reference_to_change_demands(cards)
    assert len(demands) == 1
    assert demands[0].demand_type == "exit_area"
    assert demands[0].source == "ocr_reference"
    assert demands[0].constraints.get("reason") == "exit_sign_detected"
