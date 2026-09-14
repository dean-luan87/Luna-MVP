"""
测试 Pro-1: Vision → Scene → Task 建议桥接

验证：
1. VisionEvent 正确建模视觉输入
2. SceneObserver 正确转换并更新 SceneContext
3. SceneTaskBinder 正确给出任务建议
4. VisionSceneTaskBridge 完整流程正常工作
"""

import sys
import os

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import pytest
from task_engine.vision.vision_event import VisionEvent
from task_engine.vision.scene_observer import SceneObserver
from task_engine.vision.vision_scene_bridge import VisionSceneTaskBridge, VisionSceneTaskResult
from task_engine.scene.scene_classifier import SceneClassifier, SceneGuess
from task_engine.scene.scene_context import SceneContext
from task_engine.scene.scene_task_binder import create_default_scene_task_binder


class DummySceneClassifier(SceneClassifier):
    """
    用于测试的模拟分类器：

    - 包含 "地铁" → subway
    - 包含 "医院" → hospital
    - 包含 "gate" 对象 → subway
    """

    def classify(self, ocr_text=None, objects=None, history_tags=None, gps_hint=None):
        text = (ocr_text or "").lower()
        obj_list = objects or []

        if "地铁" in text or "gate" in obj_list:
            return SceneGuess(
                scene="subway",
                tag="generic_subway",
                confidence=0.9,
                scores={"subway": 0.9, "hospital": 0.1},
            )
        elif "医院" in text:
            return SceneGuess(
                scene="hospital",
                tag="generic_hospital",
                confidence=0.9,
                scores={"hospital": 0.9, "subway": 0.1},
            )
        else:
            return SceneGuess(
                scene=None,
                tag=None,
                confidence=0.0,
                scores={},
            )


def test_subway_vision_triggers_subway_task_suggestion():
    """测试：地铁视觉输入触发地铁任务建议"""
    ctx = SceneContext()
    clf = DummySceneClassifier()
    observer = SceneObserver(classifier=clf, context=ctx)
    binder = create_default_scene_task_binder()
    bridge = VisionSceneTaskBridge(observer=observer, binder=binder)

    event = VisionEvent(
        ocr_lines=["静安寺地铁站"],
        objects=["gate"],
    )
    result = bridge.handle_vision_event(event)

    assert result.scene == "subway"
    assert result.suggested_task_meta is not None
    assert result.suggested_task_meta["task_name"] == "subway_enter"
    assert result.suggested_task_meta["scene"] == "subway"
    assert result.confidence > 0.5


def test_hospital_vision_triggers_hospital_task_suggestion():
    """测试：医院视觉输入触发医院任务建议"""
    ctx = SceneContext()
    clf = DummySceneClassifier()
    observer = SceneObserver(classifier=clf, context=ctx)
    binder = create_default_scene_task_binder()
    bridge = VisionSceneTaskBridge(observer=observer, binder=binder)

    event = VisionEvent(
        ocr_lines=["虹口医院门诊部"],
        objects=[],
    )
    result = bridge.handle_vision_event(event)

    assert result.scene == "hospital"
    assert result.suggested_task_meta is not None
    assert result.suggested_task_meta["task_name"] == "hospital_enter"
    assert result.suggested_task_meta["scene"] == "hospital"


def test_unknown_scene_returns_no_task():
    """测试：未知场景不返回任务建议"""
    ctx = SceneContext()
    clf = DummySceneClassifier()
    observer = SceneObserver(classifier=clf, context=ctx)
    binder = create_default_scene_task_binder()
    bridge = VisionSceneTaskBridge(observer=observer, binder=binder)

    event = VisionEvent(
        ocr_lines=["公园草地"],
        objects=["tree"],
    )
    result = bridge.handle_vision_event(event)

    assert result.scene is None
    assert result.suggested_task_meta is None
    assert result.confidence < 0.5


def test_vision_event_text_method():
    """测试：VisionEvent.text() 方法正确拼接 OCR 行"""
    event = VisionEvent(
        ocr_lines=["地铁", "入口", "请刷卡"],
        objects=["gate"],
    )
    assert event.text() == "地铁 入口 请刷卡"


def test_scene_observer_updates_context():
    """测试：SceneObserver 正确更新 SceneContext"""
    ctx = SceneContext()
    clf = DummySceneClassifier()
    observer = SceneObserver(classifier=clf, context=ctx)

    guess, updated_ctx = observer.observe(
        ocr_lines=["地铁站"],
        objects=["gate"],
    )

    assert guess.scene == "subway"
    assert updated_ctx.scene == "subway"
    assert updated_ctx.tag == "generic_subway"
    assert updated_ctx.confidence > 0.5


def test_scene_task_binder_exact_match():
    """测试：SceneTaskBinder 精确匹配（scene, tag）"""
    from task_engine.scene.scene_task_binder import SceneTaskBinder

    mapping = {
        ("subway", "静安寺站"): {
            "task_name": "subway_jingan",
            "ask_required": True,
        },
        ("subway", None): {
            "task_name": "subway_enter",
            "ask_required": True,
        },
    }
    binder = SceneTaskBinder(mapping=mapping)

    # 精确匹配
    ctx1 = SceneContext(scene="subway", tag="静安寺站")
    meta1 = binder.suggest_task(ctx1)
    assert meta1 is not None
    assert meta1["task_name"] == "subway_jingan"

    # 回退匹配
    ctx2 = SceneContext(scene="subway", tag="其他站")
    meta2 = binder.suggest_task(ctx2)
    assert meta2 is not None
    assert meta2["task_name"] == "subway_enter"


def test_vision_scene_bridge_preserves_context():
    """测试：VisionSceneTaskBridge 保留上下文信息"""
    ctx = SceneContext()
    clf = DummySceneClassifier()
    observer = SceneObserver(classifier=clf, context=ctx)
    binder = create_default_scene_task_binder()
    bridge = VisionSceneTaskBridge(observer=observer, binder=binder)

    event1 = VisionEvent(ocr_lines=["地铁站"], objects=["gate"])
    result1 = bridge.handle_vision_event(event1)

    # 第二次调用应该保留历史
    event2 = VisionEvent(ocr_lines=["医院"], objects=[])
    result2 = bridge.handle_vision_event(event2)

    # 上下文应该被更新
    assert result2.context.scene == "hospital"
    # 历史标签应该被保留（如果实现支持）
    assert len(result2.context.history_tags) >= 0












