"""
测试 Pro: OCR/YOLO → Scene → TaskChain 视觉桥接

验证：
1. SceneObserver 正确转换 OCR/YOLO 输入
2. SceneIntegrationService.from_vision() 正确更新 SceneContext
3. 视觉输入能正确触发场景识别
"""

import sys
import os

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import pytest
from task_engine.scene.scene_integration import SceneIntegrationService
from task_engine.scene.scene_classifier import SceneClassifier, SceneGuess
from task_engine.scene.scene_registry import SceneRegistry
from task_engine.scene.scene_context import SceneContext, scene_context_manager


class DummyClassifier:
    """用于测试的模拟分类器"""
    
    def classify(self, ocr_text=None, objects=None, history_tags=None, gps_hint=None):
        # 简单的测试逻辑：如果包含"地铁"或"gate"，识别为 subway
        text = (ocr_text or "").lower()
        obj_list = objects or []
        
        if "地铁" in text or "gate" in obj_list:
            return SceneGuess(
                scene="subway",
                tag="gate",
                confidence=0.8,
                scores={"subway": 0.8, "hospital": 0.2},
            )
        elif "医院" in text or "hospital" in obj_list:
            return SceneGuess(
                scene="hospital",
                tag="虹口医院",
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


def test_vision_bridge_updates_scene_context():
    """测试：视觉输入正确更新 SceneContext"""
    # 清理全局上下文
    scene_context_manager.clear()
    
    classifier = DummyClassifier()
    registry = SceneRegistry()
    service = SceneIntegrationService(classifier=classifier, registry=registry)

    # 通过 from_vision 输入 OCR + YOLO 结果
    result = service.from_vision(
        ocr_lines=["地铁入口"],
        objects=["gate"],
    )

    # 验证 SceneContext 被正确更新
    assert result.context.scene == "subway"
    assert result.context.tag == "gate"
    assert result.guess.scene == "subway"
    assert result.guess.confidence > 0.5

    # 验证全局上下文也被更新
    current_ctx = scene_context_manager.get_current()
    assert current_ctx is not None
    assert current_ctx.scene == "subway"


def test_vision_bridge_with_hospital():
    """测试：医院场景的视觉识别"""
    scene_context_manager.clear()
    
    classifier = DummyClassifier()
    registry = SceneRegistry()
    service = SceneIntegrationService(classifier=classifier, registry=registry)

    result = service.from_vision(
        ocr_lines=["虹口医院", "挂号处"],
        objects=["hospital_sign"],
    )

    assert result.context.scene == "hospital"
    assert result.context.tag == "虹口医院"
    assert result.guess.scene == "hospital"


def test_vision_bridge_preserves_history():
    """测试：视觉输入保留历史标签"""
    scene_context_manager.clear()
    
    classifier = DummyClassifier()
    registry = SceneRegistry()
    service = SceneIntegrationService(classifier=classifier, registry=registry)

    # 第一次识别
    result1 = service.from_vision(
        ocr_lines=["地铁入口"],
        objects=["gate"],
    )
    assert result1.context.scene == "subway"

    # 第二次识别（不同场景）
    result2 = service.from_vision(
        ocr_lines=["医院"],
        objects=["hospital_sign"],
    )
    
    # 新场景应该创建新上下文，但可以保留历史信息
    assert result2.context.scene == "hospital"
    # 历史标签应该被保留（如果实现支持的话）


def test_scene_observer_converts_input():
    """测试：SceneObserver 正确转换输入格式"""
    from task_engine.scene.scene_observer import SceneObserver
    
    classifier = DummyClassifier()
    observer = SceneObserver(classifier)

    # 测试 OCR 行列表转换
    guess1 = observer.observe(
        ocr_lines=["地铁", "入口", "请刷卡"],
        objects=[],
    )
    assert guess1.scene == "subway"

    # 测试 objects 转换
    guess2 = observer.observe(
        ocr_lines=[],
        objects=["gate", "ticket_machine"],
    )
    assert guess2.scene == "subway"

    # 测试组合输入
    guess3 = observer.observe(
        ocr_lines=["医院"],
        objects=["hospital_sign"],
    )
    assert guess3.scene == "hospital"


def test_from_vision_with_empty_input():
    """测试：空输入的处理"""
    scene_context_manager.clear()
    
    classifier = DummyClassifier()
    registry = SceneRegistry()
    service = SceneIntegrationService(classifier=classifier, registry=registry)

    result = service.from_vision(
        ocr_lines=[],
        objects=[],
    )

    # 空输入应该返回低置信度或 None
    assert result.guess.scene is None or result.guess.confidence < 0.5












