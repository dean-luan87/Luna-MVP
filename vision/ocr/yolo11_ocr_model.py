from __future__ import annotations

from typing import List
import numpy as np

try:
    from ultralytics import YOLO
except ImportError as e:
    raise RuntimeError("Ultralytics YOLO not installed") from e

from vision.ocr.yolo11_ocr_adapter import YoloOcrToken


class Yolo11OcrModel:
    """
    L0 OCR model wrapper:
    - no scene logic
    - no semantics
    - frame -> OCR tokens
    """

    def __init__(self, model_path: str, device: str = "cpu"):
        self.model = YOLO(model_path)
        self.device = device

    def infer(self, frame: np.ndarray) -> List[YoloOcrToken]:
        results = self.model.predict(
            source=frame,
            device=self.device,
            verbose=False,
            conf=0.25,
        )

        tokens: List[YoloOcrToken] = []

        for r in results:
            if r.boxes is None:
                continue

            for box in r.boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])

                text = None
                if hasattr(r, "names") and cls_id in r.names:
                    text = r.names[cls_id]

                if not text:
                    continue

                x1, y1, x2, y2 = box.xyxy[0].tolist()
                tokens.append(
                    YoloOcrToken(
                        text=text,
                        bbox_xyxy=(x1, y1, x2, y2),
                        confidence=conf,
                    )
                )

        return tokens
