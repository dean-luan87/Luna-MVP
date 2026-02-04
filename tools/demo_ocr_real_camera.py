import os
import sys
from pathlib import Path

# Ensure repo root on sys.path for direct execution
_root = Path(__file__).resolve().parents[1]
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

# silence Ultralytics settings write warnings
os.environ["ULTRALYTICS_SETTINGS_DIR"] = "/tmp/ultralytics"

from world_knowledge.loop.recorder import EvidenceRecorder
from vision.ocr.yolo11_ocr_runner import Yolo11OcrRunner


def main():
    recorder = EvidenceRecorder()
    runner = Yolo11OcrRunner(
        model_path="models/yolo11n.pt",
        recorder=recorder,
        device="cpu",
    )

    runner.run_video(
        video_path="test_video_complex_6m42s.mp4",
        max_frames=200,
    )

    signals = recorder.drain()
    print(f"OCR signals: {len(signals)}")
    for s in signals[:10]:
        print(s.payload["text"], s.payload["confidence"])


if __name__ == "__main__":
    main()
