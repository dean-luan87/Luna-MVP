from vision_ocr import SemanticToken, TextSemanticMapper


def test_mapper_to_reference_cards():
    m = TextSemanticMapper()
    cards = m.to_reference_cards(
        [
            SemanticToken(key="exit", confidence=0.8, raw_text="出口"),
            SemanticToken(key="metro_line", value="2", confidence=0.7, raw_text="2号线"),
        ]
    )
    assert any(c.kind == "signage" and c.meaning == "exit" for c in cards)
    assert any(
        c.kind == "transport" and c.meaning == "metro_line" and c.attrs.get("line") == "2"
        for c in cards
    )
