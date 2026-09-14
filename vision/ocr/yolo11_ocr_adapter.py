from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple
import time

from world_knowledge.schema import ObservationSignal


@dataclass(frozen=True)
class YoloOcrToken:
    text: str
    bbox_xyxy: Tuple[float, float, float, float]
    confidence: float


class Yolo11OcrAdapter:
    """
    YOLO11 OCR results -> ObservationSignal.
    Only produces signals, no semantics, no alignment, no conclusions.
    """

    def __init__(self, provider: str = "yolo11_ocr"):
        self.provider = provider

    def to_signals(
        self,
        tokens: List[YoloOcrToken],
        frame_id: Optional[str] = None,
        ts: Optional[float] = None,
        extra: Optional[Dict[str, Any]] = None,
    ) -> List[ObservationSignal]:
        if ts is None:
            ts = time.time()
        extra = extra or {}

        out: List[ObservationSignal] = []
        for t in tokens:
            payload: Dict[str, Any] = {
                "text": t.text,
                "bbox_xyxy": list(t.bbox_xyxy),
                "confidence": float(t.confidence),
            }
            if frame_id is not None:
                payload["frame_id"] = frame_id
            payload.update(extra)

            out.append(
                ObservationSignal(
                    signal_type="ocr_text",
                    payload=payload,
                    provider=self.provider,
                    ts=float(ts),
                )
            )
        return out
