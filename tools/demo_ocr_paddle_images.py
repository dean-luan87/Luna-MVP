import os
import sys
from pathlib import Path

import cv2

# silence Ultralytics settings write warnings (if any)
os.environ["ULTRALYTICS_SETTINGS_DIR"] = "/tmp/ultralytics"
os.environ.setdefault("XDG_CACHE_HOME", "/tmp")
os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")
# reduce thread-related instability on macOS
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")
os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "True")

# Ensure repo root on sys.path for direct execution
_root = Path(__file__).resolve().parents[1]
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from vision.ocr.paddle_ocr_model import PaddleOcrModel


def main():
    samples_dir = Path(_root) / "test_data" / "ocr_samples"
    if not samples_dir.exists():
        raise RuntimeError(f"Missing samples dir: {samples_dir}")

    images = sorted(
        [
            p
            for p in samples_dir.iterdir()
            if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".bmp", ".webp"}
        ]
    )
    if not images:
        raise RuntimeError("No images found in test_data/ocr_samples")

    model = PaddleOcrModel()

    for img_path in images:
        img = cv2.imread(str(img_path))
        if img is None:
            print(f"[SKIP] failed to read: {img_path.name}")
            continue

        tokens = model.infer(img)
        print(f"\n== {img_path.name} ==")
        print(f"tokens: {len(tokens)}")
        for t in tokens[:20]:
            print(f"{t.text}  {t.confidence:.2f}  {t.bbox_xyxy}")


if __name__ == "__main__":
    main()
