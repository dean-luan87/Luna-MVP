"""
测试：SceneIntegrationService ensure_scene_context 行为。

覆盖点：
- 在 subway 场景下，OCR 包含"静安寺站"与地铁关键词 → 识别 + 绑定正确的 ScenePackRef；
- 在未注册场景的情况下，pack_ref 为空但 SceneContext 仍然可用；
- 连续两次调用：
    - 相同场景（scene/tag 一致）→ 复用同一个 SceneContext 实例；
    - 不同场景（如 subway → hospital）→ 创建新的 SceneContext；
"""

from typing import Optional

from task_engine.scene.scene_classifier import SceneClassifier
from task_engine.scene.scene_context import SceneContext, scene_context_manager
from task_engine.scene.scene_integration import SceneIntegrationService
from task_engine.scene.scene_registry import SceneRegistry


def test_integration_subway_with_registered_pack() -> None:
    classifier = SceneClassifier(min_confidence=0.5)
    registry = SceneRegistry()

    # 注册 subway 场景的默认包和静安寺站专属包
    registry.register(scene="subway", pack_id="packs/subway/default.json", tag=None)
    jingan_ref = registry.register(scene="subway", pack_id="packs/subway/jingan_temple.json", tag="静安寺站")

    service = SceneIntegrationService(classifier=classifier, registry=registry)

    # 确保全局上下文起始为空
    scene_context_manager.clear()

    ocr = "我现在在静安寺站这边，准备进地铁。"

    result = service.ensure_scene_context(ocr_text=ocr)

    ctx = result.context
    guess = result.guess
    ref = result.pack_ref

    assert ctx is not None
    assert isinstance(ctx, SceneContext)

    assert guess.scene == "subway"
    assert guess.tag == "静安寺站"
    assert ref is not None
    assert ref.pack_id == jingan_ref.pack_id

    # 全局管理器中也应为同一个引用
    assert scene_context_manager.get_current() is ctx


def test_integration_with_unregistered_scene_returns_context_without_packref() -> None:
    classifier = SceneClassifier(min_confidence=0.5)
    registry = SceneRegistry()  # 没有注册 hospital 场景

    service = SceneIntegrationService(classifier=classifier, registry=registry)

    scene_context_manager.clear()

    ocr = "我在医院门诊大厅准备挂号。"

    result = service.ensure_scene_context(ocr_text=ocr)

    ctx = result.context
    guess = result.guess
    ref = result.pack_ref

    assert ctx is not None
    assert guess.scene == "hospital"
    # registry 中没有 hospital 注册，因此 pack_ref 应为 None
    assert ref is None
    assert scene_context_manager.get_current() is ctx


def test_integration_reuses_context_for_same_scene_and_creates_new_for_different_scene() -> None:
    classifier = SceneClassifier(min_confidence=0.5)
    registry = SceneRegistry()

    # subway 注册一个默认包
    registry.register(scene="subway", pack_id="packs/subway/default.json", tag=None)
    # hospital 也注册一个默认包
    registry.register(scene="hospital", pack_id="packs/hospital/default.json", tag=None)

    service = SceneIntegrationService(classifier=classifier, registry=registry)

    scene_context_manager.clear()

    # 第一次：识别为 subway / 静安寺站
    ocr1 = "我在静安寺站地铁口。"
    result1 = service.ensure_scene_context(ocr_text=ocr1)
    ctx1 = result1.context

    # 第二次：仍然 subway 场景（内容相似）
    ocr2 = "我还在静安寺站里面，准备上车。"
    result2 = service.ensure_scene_context(ocr_text=ocr2)
    ctx2 = result2.context

    # 相同场景，应复用同一个 SceneContext 实例
    assert ctx1 is ctx2
    assert ctx2.scene == "subway"

    # 第三次：切换到医院场景
    ocr3 = "我现在到医院门诊大厅了，准备挂号。"
    result3 = service.ensure_scene_context(ocr_text=ocr3)
    ctx3 = result3.context

    # 不同场景，应创建新的 SceneContext 实例
    assert ctx3 is not ctx1
    assert ctx3.scene == "hospital"

    # 全局场景上下文应为医院场景
    current = scene_context_manager.get_current()
    assert current is ctx3
    assert current.scene == "hospital"
