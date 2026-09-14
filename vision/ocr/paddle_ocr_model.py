from __future__ import annotations

from typing import List
import numpy as np

from paddleocr import PaddleOCR
from vision.ocr.yolo11_ocr_adapter import YoloOcrToken


class PaddleOcrModel:
    """
    L0 真·OCR：
    - 连续运行
    - 不做语义
    - 不做对齐
    - 只产 text token
    """

    def __init__(self, lang: str = "ch", use_angle_cls: bool = True):
        self.ocr = PaddleOCR(
            lang=lang,
            use_angle_cls=use_angle_cls,
        )

    def infer(self, frame: np.ndarray) -> List[YoloOcrToken]:
        # PaddleOCR API compatibility: some versions don't accept cls param
        try:
            results = self.ocr.ocr(frame, cls=True)
        except TypeError:
            results = self.ocr.ocr(frame)
        tokens: List[YoloOcrToken] = []

        if not results:
            return tokens

        for line in results:
            for item in line:
                bbox = item[0]
                info = item[1]

                text = None
                conf = 1.0
                if isinstance(info, (list, tuple)):
                    if len(info) == 2:
                        text, conf = info
                    elif len(info) == 1:
                        text = info[0]
                    else:
                        continue
                elif isinstance(info, dict):
                    text = info.get("text") or info.get("label")
                    conf = info.get("score", 1.0)
                else:
                    text = str(info)

                # bbox could be list of points or dict; skip invalid shapes
                points = None
                if isinstance(bbox, dict):
                    points = bbox.get("points")
                elif isinstance(bbox, (list, tuple)):
                    points = bbox

                if not points or not isinstance(points, (list, tuple)):
                    continue
                if not isinstance(points[0], (list, tuple)) or len(points[0]) < 2:
                    continue

                xs = [p[0] for p in points]
                ys = [p[1] for p in points]
                x1, y1, x2, y2 = min(xs), min(ys), max(xs), max(ys)

                if text is None:
                    continue

                tokens.append(
                    YoloOcrToken(
                        text=str(text),
                        bbox_xyxy=(float(x1), float(y1), float(x2), float(y2)),
                        confidence=float(conf),
                    )
                )

        return tokens
