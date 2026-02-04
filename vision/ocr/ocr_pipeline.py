from __future__ import annotations

from typing import Any, Dict, List, Optional
import time

from world_knowledge.schema import ObservationSignal
from world_knowledge.loop.recorder import EvidenceRecorder
from vision.ocr.yolo11_ocr_adapter import Yolo11OcrAdapter, YoloOcrToken


class OcrPipelineV0:
    """
    OCR v0: only records signals (EvidenceRecorder) and returns them.
    No semantics, no verification, no curation, no Task/C interaction.
    """

    def __init__(
        self, recorder: EvidenceRecorder, adapter: Optional[Yolo11OcrAdapter] = None
    ):
        self.recorder = recorder
        self.adapter = adapter or Yolo11OcrAdapter()

    def process_yolo_tokens(
        self,
        tokens: List[YoloOcrToken],
        frame_id: Optional[str] = None,
        ts: Optional[float] = None,
        extra: Optional[Dict[str, Any]] = None,
    ) -> List[ObservationSignal]:
        if ts is None:
            ts = time.time()
        signals = self.adapter.to_signals(
            tokens, frame_id=frame_id, ts=ts, extra=extra
        )

        for s in signals:
            self.recorder.add(s)

        return signals
