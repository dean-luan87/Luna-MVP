from __future__ import annotations

from typing import Any, Dict, List

from vision_ocr.types import ReferenceCard, OcrSignal
from vision_ocr.signal_normalizer import OcrSignalNormalizer
from vision_ocr.text_semantic_mapper import TextSemanticMapper


def attach_ocr_reference(world_snapshot: Dict[str, Any], cards: List[ReferenceCard]) -> Dict[str, Any]:
    """
    把 OCR 语义卡片写入 reference，不得影响 facts。
    """
    ws = dict(world_snapshot) if world_snapshot is not None else {}
    ref = dict(ws.get("reference", {}))
    ref_cards = [c.__dict__ for c in cards]
    ref["ocr_reference_cards"] = ref_cards
    ws["reference"] = ref
    return ws


class OcrSemanticPipeline:
    """
    端到端：OcrSignal -> tokens -> reference cards
    """

    def __init__(self):
        self.norm = OcrSignalNormalizer()
        self.mapper = TextSemanticMapper()

    def run(self, signals: List[OcrSignal]) -> List[ReferenceCard]:
        tokens = []
        for s in signals:
            tokens.extend(self.norm.normalize(s))
        return self.mapper.to_reference_cards(tokens)
