from dynamic_view.roi import RoiHint

from vision_perception_b1.adapter import to_reference_cards
from vision_ocr.types import ReferenceCard


def test_adapter_outputs_reference_cards():
    roi = RoiHint(area_type="exit_area", hint="h", bbox=(0, 0, 1, 1))
    cards = to_reference_cards([{"text": "EXIT", "confidence": 0.4}], roi)
    assert cards
    assert isinstance(cards[0], ReferenceCard)
    assert cards[0].kind == "vision_reference"
