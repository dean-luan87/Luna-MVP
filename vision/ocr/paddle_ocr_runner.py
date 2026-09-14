from __future__ import annotations

import cv2
import time
from typing import Optional

from world_knowledge.loop.recorder import EvidenceRecorder
from vision.ocr.ocr_pipeline import OcrPipelineV0
from vision.ocr.paddle_ocr_model import PaddleOcrModel


class PaddleOcrRunner:
    """
    使用 PaddleOCR 作为 L0 真·OCR
    """

    def __init__(self, recorder: EvidenceRecorder):
        self.model = PaddleOcrModel()
        self.pipeline = OcrPipelineV0(recorder=recorder)

    def run_camera(self, camera_id: int = 0, max_frames: Optional[int] = None):
        cap = cv2.VideoCapture(camera_id)
        count = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            ts = time.time()
            tokens = self.model.infer(frame)

            self.pipeline.process_yolo_tokens(
                tokens,
                frame_id=f"paddle_cam_{camera_id}_{count}",
                ts=ts,
            )

            count += 1
            if max_frames and count >= max_frames:
                break

        cap.release()

    def run_video(self, video_path: str, max_frames: Optional[int] = None):
        cap = cv2.VideoCapture(video_path)
        count = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            ts = time.time()
            tokens = self.model.infer(frame)

            self.pipeline.process_yolo_tokens(
                tokens,
                frame_id=f"paddle_video_{count}",
                ts=ts,
            )

            count += 1
            if max_frames and count >= max_frames:
                break

        cap.release()
