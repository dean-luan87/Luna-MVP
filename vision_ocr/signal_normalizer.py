from __future__ import annotations

import re
from typing import List

from vision_ocr.types import OcrSignal, SemanticToken


class OcrSignalNormalizer:
    """
    L1：把 OCR 文本归一化到“意义 token”
    - 允许多语言/多写法
    - 不做事实判断
    """

    _re_spaces = re.compile(r"\s+")
    _re_line_num = re.compile(r"(?:line|线路|线)\s*([0-9]{1,2})", re.IGNORECASE)
    _re_pure_num_line = re.compile(r"^([0-9]{1,2})\s*(?:号线|线)$")
    _re_bus = re.compile(r"^(?:bus|公交)?\s*([0-9]{1,4})(?:路)?$", re.IGNORECASE)

    def normalize(self, sig: OcrSignal) -> List[SemanticToken]:
        raw = (sig.text or "").strip()
        if not raw:
            return []

        t = self._re_spaces.sub(" ", raw).lower()

        out: List[SemanticToken] = []

        if "exit" in t or "出口" in raw:
            out.append(
                SemanticToken(
                    key="exit",
                    confidence=max(sig.score, 0.4),
                    bbox=sig.bbox,
                    raw_text=raw,
                    meta={"source": sig.source},
                )
            )

        if "elevator" in t or "lift" in t or "电梯" in raw:
            out.append(
                SemanticToken(
                    key="elevator",
                    confidence=max(sig.score, 0.4),
                    bbox=sig.bbox,
                    raw_text=raw,
                    meta={"source": sig.source},
                )
            )

        m_floor = re.search(r"\b([bB]?\d{1,2})\s*(?:f|楼)\b", raw, re.IGNORECASE)
        if m_floor:
            out.append(
                SemanticToken(
                    key="floor",
                    value=m_floor.group(1).upper(),
                    confidence=max(sig.score, 0.35),
                    bbox=sig.bbox,
                    raw_text=raw,
                    meta={"source": sig.source},
                )
            )

        m_line = self._re_line_num.search(raw) or self._re_pure_num_line.search(raw)
        if m_line:
            num = m_line.group(1)
            out.append(
                SemanticToken(
                    key="metro_line",
                    value=num,
                    confidence=max(sig.score, 0.45),
                    bbox=sig.bbox,
                    raw_text=raw,
                    meta={"source": sig.source},
                )
            )

        m_bus = self._re_bus.match(t)
        if m_bus:
            out.append(
                SemanticToken(
                    key="bus_route",
                    value=m_bus.group(1),
                    confidence=max(sig.score, 0.35),
                    bbox=sig.bbox,
                    raw_text=raw,
                    meta={"source": sig.source},
                )
            )

        if (
            ("秒" in raw and ("red" in t or "green" in t or "红" in raw or "绿" in raw))
            or ("countdown" in t)
        ):
            out.append(
                SemanticToken(
                    key="signal_countdown",
                    confidence=max(sig.score, 0.3),
                    bbox=sig.bbox,
                    raw_text=raw,
                    meta={"source": sig.source},
                )
            )

        return out
