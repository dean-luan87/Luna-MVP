import time

from world_knowledge.loop.recorder import EvidenceRecorder
from vision.ocr.ocr_pipeline import OcrPipelineV0
from vision.ocr.yolo11_ocr_adapter import YoloOcrToken


def main():
    rec = EvidenceRecorder()
    pipe = OcrPipelineV0(recorder=rec)

    tokens = [
        YoloOcrToken(text="12", bbox_xyxy=(10, 10, 40, 40), confidence=0.62),
        YoloOcrToken(text="2号线", bbox_xyxy=(100, 20, 200, 60), confidence=0.71),
    ]
    signals = pipe.process_yolo_tokens(
        tokens, frame_id="frame_001", ts=time.time(), extra={"camera": "main"}
    )

    drained = rec.drain()
    assert len(drained) == 2
    print("signals:", [s.payload["text"] for s in signals])


if __name__ == "__main__":
    main()
