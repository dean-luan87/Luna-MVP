import os
import sys
from pathlib import Path

# silence Ultralytics settings write warnings
os.environ["ULTRALYTICS_SETTINGS_DIR"] = "/tmp/ultralytics"
# reduce cache permission warnings
os.environ.setdefault("XDG_CACHE_HOME", "/tmp")
os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")

# Ensure repo root on sys.path for direct execution
_root = Path(__file__).resolve().parents[1]
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from world_knowledge.loop.recorder import EvidenceRecorder
from vision.ocr.paddle_ocr_runner import PaddleOcrRunner


def main():
    recorder = EvidenceRecorder()
    runner = PaddleOcrRunner(recorder=recorder)

    runner.run_video(
        video_path="test_video_complex_6m42s.mp4",
        max_frames=50,
    )

    signals = recorder.drain()
    print(f"OCR signals: {len(signals)}")
    for s in signals[:20]:
        print(s.payload["text"], s.payload["confidence"])


if __name__ == "__main__":
    main()
