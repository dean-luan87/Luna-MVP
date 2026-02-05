# tests/test_model_scheduler.py
from core.model_scheduler.registry import (
    ModelRegistry,
    ModelDescriptor,
    CapabilityDescriptor,
    ModelType,
)
from core.model_scheduler.selector import ContextAwareModelSelector, ModelSelectionContext
from core.model_scheduler.executor import ModelScheduler


def _dummy_runner_fast(**kwargs):
    return {"result": "fast", "input": kwargs}


def _dummy_runner_slow(**kwargs):
    return {"result": "slow", "input": kwargs}


def test_model_selection_prefers_low_latency_and_capability():
    registry = ModelRegistry()

    # 模型 A：低延迟但能力一般
    model_fast = ModelDescriptor(
        id="fast_model",
        model_type=ModelType.VISION_DETECT,
        provider="local",
        version="1.0",
        capabilities=CapabilityDescriptor(
            can_detect_obstacle=True,
            latency_level=1,
            accuracy_level=2,
        ),
        runner=_dummy_runner_fast,
    )

    # 模型 B：高精度但延迟高
    model_slow = ModelDescriptor(
        id="slow_model",
        model_type=ModelType.VISION_DETECT,
        provider="local",
        version="1.0",
        capabilities=CapabilityDescriptor(
            can_detect_obstacle=True,
            latency_level=3,
            accuracy_level=3,
        ),
        runner=_dummy_runner_slow,
    )

    registry.register_model(model_fast)
    registry.register_model(model_slow)

    selector = ContextAwareModelSelector(registry)

    ctx = ModelSelectionContext(
        scene_type="outdoor",
        task_node_type="detect_obstacle",
        low_light=False,
        need_high_accuracy=False,
        real_time_required=True,
    )

    best = selector.select_best_model(ModelType.VISION_DETECT, ctx)
    assert best is not None
    # 在实时要求场景下，应优先选择低延迟模型
    assert best.id == "fast_model"


def test_model_scheduler_single_and_fallback():
    registry = ModelRegistry()

    good_model = ModelDescriptor(
        id="good_model",
        model_type=ModelType.OCR,
        provider="local",
        version="1.0",
        capabilities=CapabilityDescriptor(can_ocr_text=True),
        runner=_dummy_runner_fast,
    )

    def _bad_runner(**kwargs):
        raise RuntimeError("ocr failed")

    bad_model = ModelDescriptor(
        id="bad_model",
        model_type=ModelType.OCR,
        provider="local",
        version="1.0",
        capabilities=CapabilityDescriptor(can_ocr_text=True),
        runner=_bad_runner,
    )

    registry.register_model(good_model)
    registry.register_model(bad_model)

    scheduler = ModelScheduler()

    # 单模型运行
    res_single = scheduler.run_single_model(good_model, image="fake_image")
    assert res_single["success"] is True
    assert res_single["model_id"] == "good_model"
    assert res_single["output"]["result"] == "fast"

    # fallback 链：先坏后好，应切到 good_model
    res_fb = scheduler.run_fallback_chain([bad_model, good_model], image="fake_image")
    assert res_fb["success"] is True
    assert res_fb["model_id"] == "good_model"












