# vision_pipeline/b2/v03/snapshot_dumper.py
from __future__ import annotations
import os
import cv2
from dataclasses import dataclass


@dataclass
class SnapshotDumper:
    video_path: str
    output_dir: str
    enabled: bool = True

    def __post_init__(self) -> None:
        if self.enabled:
            os.makedirs(self.output_dir, exist_ok=True)
        self.cap = cv2.VideoCapture(self.video_path)
        if not self.cap.isOpened():
            raise RuntimeError(f"Cannot open video: {self.video_path}")

    def dump(self, frame_idx: int, out_path: str) -> bool:
        if not self.enabled:
            return False

        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ok, frame = self.cap.read()
        if not ok or frame is None:
            return False

        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        cv2.imwrite(out_path, frame)
        return True

    def close(self) -> None:
        self.cap.release()

