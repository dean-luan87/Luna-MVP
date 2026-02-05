import time

from dynamic_view.engine import ObservationEngine
from dynamic_view.descriptors import EntityDescriptor
from dynamic_view.binder.simple import SimpleBinder
from dynamic_view.types import ObservationState
from observe.timeline.schema import TimelineFrame
from tools.run_dynamic_full_demo import snapshot_timeline
from world_knowledge.loop.recorder import EvidenceRecorder
from vision.ocr.ocr_pipeline import OcrPipelineV0
from vision.ocr.yolo11_ocr_adapter import YoloOcrToken


def test_ocr_signals_and_entities_coexist():
    obs = ObservationEngine(binder=SimpleBinder())
    t0 = time.time()

    desc = EntityDescriptor(kind="traffic_light", signature="sig_demo_light")
    obs.ingest_descriptor(desc, t0)
    obs.tick(t0)
    obs.tick(t0 + 0.1)

    ocr = OcrPipelineV0(recorder=EvidenceRecorder())
    signals = ocr.process_yolo_tokens(
        [YoloOcrToken(text="2号线", bbox_xyxy=(1, 1, 2, 2), confidence=0.5)],
        frame_id="f1",
        ts=t0 + 0.1,
    )

    frame = snapshot_timeline(obs, task_engine=_EmptyTaskEngine(), c_decision={}, ts=t0 + 0.1, signals=signals)
    assert isinstance(frame, TimelineFrame)
    assert "traffic_light" in list(frame.entities.keys())[0]
    assert len(frame.signals) == 1
    assert frame.signals[0]["signal_type"] == "ocr_text"


def test_entity_occlusion_does_not_block_ocr_signals():
    obs = ObservationEngine(binder=SimpleBinder())
    t0 = time.time()

    desc = EntityDescriptor(kind="traffic_light", signature="sig_demo_light")
    obs.ingest_descriptor(desc, t0)
    obs.tick(t0)
    obs.tick(t0 + 0.1)

    # Occlude entity
    obs.tick(t0 + 3.0)
    assert obs.entities
    ent = list(obs.entities.values())[0]
    assert ent.state in (ObservationState.INVISIBLE, ObservationState.DISAPPEARED)

    ocr = OcrPipelineV0(recorder=EvidenceRecorder())
    signals = ocr.process_yolo_tokens(
        [YoloOcrToken(text="出口", bbox_xyxy=(3, 3, 4, 4), confidence=0.6)],
        frame_id="f2",
        ts=t0 + 3.0,
    )

    frame = snapshot_timeline(obs, task_engine=_EmptyTaskEngine(), c_decision={}, ts=t0 + 3.0, signals=signals)
    assert len(frame.signals) == 1
    assert frame.signals[0]["payload"]["text"] == "出口"


class _EmptyTaskEngine:
    def __init__(self):
        self.active_task = None
