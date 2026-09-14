import sys
import time
from pathlib import Path

# 确保仓库根在 path，便于直接运行
_root = Path(__file__).resolve().parents[1]
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from vision_interpretation.interpreter import interpret_ocr
from vision_interpretation.schema import RawTextCandidate
from observe.timeline.schema import TimelineFrame


def main():
    raw = [
        RawTextCandidate(text="EXIT", confidence=0.82),
        RawTextCandidate(text="E X I T", confidence=0.61),
    ]
    interpretation = interpret_ocr(roi_kind="exit_area", raw_text_candidates=raw)

    frame = TimelineFrame(
        ts=time.time(),
        entities={},
        tasks=[],
        c_decision={},
    )
    frame.vision_interpretation = interpretation.__dict__

    print(interpretation)
    print(frame.to_json())


if __name__ == "__main__":
    main()
