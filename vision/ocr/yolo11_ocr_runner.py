from __future__ import annotations

import time
from typing import Optional

import cv2

from vision.ocr.yolo11_ocr_model import Yolo11OcrModel
from vision.ocr.ocr_pipeline import OcrPipelineV0
from world_knowledge.loop.recorder import EvidenceRecorder


class Yolo11OcrRunner:
    """
    Run OCR pipeline on live camera/video frames.
    """

    def __init__(
        self,
        model_path: str,
        recorder: EvidenceRecorder,
        device: str = "cpu",
    ):
        self.model = Yolo11OcrModel(model_path, device=device)
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
                frame_id=f"cam_{camera_id}_{count}",
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
                frame_id=f"video_{count}",
                ts=ts,
            )

            count += 1
            if max_frames and count >= max_frames:
                break

        cap.release()
