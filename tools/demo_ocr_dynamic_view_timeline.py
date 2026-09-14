import time
import sys
from pathlib import Path

# 确保仓库根在 path，便于直接运行
_root = Path(__file__).resolve().parents[1]
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from dynamic_view.engine import ObservationEngine
from dynamic_view.descriptors import EntityDescriptor
from dynamic_view.binder.simple import SimpleBinder
from observe.timeline.recorder import TimelineRecorder
from tools.run_dynamic_full_demo import snapshot_timeline
from world_knowledge.loop.recorder import EvidenceRecorder
from vision.ocr.ocr_pipeline import OcrPipelineV0
from vision.ocr.yolo11_ocr_adapter import YoloOcrToken


def main():
    obs = ObservationEngine(binder=SimpleBinder())
    timeline_fp = open("runs/ocr_dynamic_view.timeline.jsonl", "w", encoding="utf-8")
    recorder = TimelineRecorder(timeline_fp)

    ocr_rec = EvidenceRecorder()
    ocr = OcrPipelineV0(recorder=ocr_rec)

    t0 = time.time()

    # Entity appears
    desc = EntityDescriptor(kind="traffic_light", signature="sig_demo_light")
    eid = obs.ingest_descriptor(desc, t0)
    obs.tick(t0)
    obs.tick(t0 + 0.1)

    # OCR signals coexist
    signals = ocr.process_yolo_tokens(
        [
            YoloOcrToken(text="2号线", bbox_xyxy=(10, 10, 40, 40), confidence=0.62),
            YoloOcrToken(text="出口", bbox_xyxy=(50, 20, 90, 60), confidence=0.71),
        ],
        frame_id="frame_001",
        ts=t0 + 0.1,
        extra={"camera": "main"},
    )
    frame = snapshot_timeline(obs, task_engine=_EmptyTaskEngine(), c_decision={}, ts=t0 + 0.1, signals=signals)
    recorder.record(frame)

    # Entity occludes, OCR still appears
    obs.tick(t0 + 3.0)
    signals2 = ocr.process_yolo_tokens(
        [YoloOcrToken(text="出口", bbox_xyxy=(12, 12, 42, 42), confidence=0.64)],
        frame_id="frame_002",
        ts=t0 + 3.0,
        extra={"camera": "main"},
    )
    frame2 = snapshot_timeline(obs, task_engine=_EmptyTaskEngine(), c_decision={}, ts=t0 + 3.0, signals=signals2)
    recorder.record(frame2)

    timeline_fp.close()
    print("[OK] wrote runs/ocr_dynamic_view.timeline.jsonl")
    if eid:
        print("[OK] entity:", eid)


class _EmptyTaskEngine:
    def __init__(self):
        self.active_task = None


if __name__ == "__main__":
    main()
