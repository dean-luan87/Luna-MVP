from __future__ import annotations

from typing import List

from vision_ocr.types import SemanticToken, ReferenceCard


class TextSemanticMapper:
    """
    L2：把 token 映射为“ReferenceCard”
    - 仍不进入事实域
    - 只输出 reference cards（可被 Task/用户播报消费）
    """

    def to_reference_cards(self, tokens: List[SemanticToken]) -> List[ReferenceCard]:
        cards: List[ReferenceCard] = []

        for tk in tokens:
            if tk.key == "exit":
                cards.append(
                    ReferenceCard(
                        kind="signage",
                        meaning="exit",
                        confidence=tk.confidence,
                        bbox=tk.bbox,
                        attrs={"raw": tk.raw_text},
                    )
                )
            elif tk.key == "elevator":
                cards.append(
                    ReferenceCard(
                        kind="facility",
                        meaning="elevator",
                        confidence=tk.confidence,
                        bbox=tk.bbox,
                        attrs={"raw": tk.raw_text},
                    )
                )
            elif tk.key == "floor":
                cards.append(
                    ReferenceCard(
                        kind="facility",
                        meaning="floor_label",
                        confidence=tk.confidence,
                        bbox=tk.bbox,
                        attrs={"floor": tk.value, "raw": tk.raw_text},
                    )
                )
            elif tk.key == "metro_line":
                cards.append(
                    ReferenceCard(
                        kind="transport",
                        meaning="metro_line",
                        confidence=tk.confidence,
                        bbox=tk.bbox,
                        attrs={"line": tk.value, "raw": tk.raw_text},
                    )
                )
            elif tk.key == "bus_route":
                cards.append(
                    ReferenceCard(
                        kind="transport",
                        meaning="bus_route",
                        confidence=tk.confidence,
                        bbox=tk.bbox,
                        attrs={"route": tk.value, "raw": tk.raw_text},
                    )
                )
            elif tk.key == "signal_countdown":
                cards.append(
                    ReferenceCard(
                        kind="signal",
                        meaning="signal_countdown",
                        confidence=tk.confidence,
                        bbox=tk.bbox,
                        attrs={"raw": tk.raw_text},
                    )
                )
            else:
                continue

        return cards
