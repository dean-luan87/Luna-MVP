import time

from world_knowledge.loop.recorder import EvidenceRecorder
from vision.ocr.ocr_pipeline import OcrPipelineV0
from vision.ocr.yolo11_ocr_adapter import YoloOcrToken


def test_ocr_pipeline_records_signals():
    rec = EvidenceRecorder()
    pipe = OcrPipelineV0(recorder=rec)

    tokens = [YoloOcrToken(text="12", bbox_xyxy=(1, 2, 3, 4), confidence=0.5)]
    signals = pipe.process_yolo_tokens(tokens, frame_id="f1", ts=time.time())

    assert len(signals) == 1
    assert signals[0].signal_type == "ocr_text"
    assert signals[0].payload["text"] == "12"

    drained = rec.drain()
    assert len(drained) == 1
    assert drained[0].provider == "yolo11_ocr"
