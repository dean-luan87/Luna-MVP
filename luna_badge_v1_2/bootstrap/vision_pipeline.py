"""
Vision Pipeline Bootstrap

负责一次性构建：
- SceneContext
- SceneClassifier（可以注入真实模型，也可以用 Dummy）
- SceneObserver
- SceneTaskBinder
- VisionSceneTaskBridge
- （可选）VisionTaskOrchestrator
"""

from dataclasses import dataclass
from typing import Optional, List

from task_engine.scene.scene_context import SceneContext
from task_engine.scene.scene_classifier import SceneClassifier, SceneGuess
from task_engine.scene.scene_task_binder import create_default_scene_task_binder, SceneTaskBinder
from task_engine.vision.scene_observer import SceneObserver
from task_engine.vision.vision_scene_bridge import VisionSceneTaskBridge
from task_engine.vision.vision_task_orchestrator import VisionTaskOrchestrator
from task_chain.task_chain_manager import TaskChainManager


class DefaultSceneClassifier(SceneClassifier):
    """
    默认 classifier（可在生产中替换为真实模型接入）。
    """

    def classify(
        self,
        *,
        ocr_text: Optional[str] = None,
        objects: Optional[List[str]] = None,
        gps_hint: Optional[str] = None,
        history_tags: Optional[List[str]] = None,
    ) -> SceneGuess:
        text = (ocr_text or "").lower()
        obj_list = objects or []

        if "地铁" in text or "gate" in obj_list:
            return SceneGuess(
                scene="subway",
                tag="generic_subway",
                confidence=0.9,
                scores={"rule": 0.9},
            )
        if "医院" in text:
            return SceneGuess(
                scene="hospital",
                tag="generic_hospital",
                confidence=0.9,
                scores={"rule": 0.9},
            )
        return SceneGuess(scene=None, tag=None, confidence=0.0, scores={})


@dataclass
class VisionPipeline:
    """Vision Pipeline 完整配置"""
    context: SceneContext
    classifier: SceneClassifier
    binder: SceneTaskBinder
    observer: SceneObserver
    bridge: VisionSceneTaskBridge
    orchestrator: Optional[VisionTaskOrchestrator] = None


def create_vision_pipeline(
    task_manager: Optional[TaskChainManager] = None,
    classifier: Optional[SceneClassifier] = None,
    context: Optional[SceneContext] = None,
    binder: Optional[SceneTaskBinder] = None,
) -> VisionPipeline:
    """
    构建完整 Vision Pipeline：

    - 若未传入 classifier/context/binder，则使用默认实现
    - 若传入 task_manager，则同时构建 VisionTaskOrchestrator

    Args:
        task_manager: 可选的 TaskChainManager 实例
        classifier: 可选的 SceneClassifier 实例
        context: 可选的 SceneContext 实例
        binder: 可选的 SceneTaskBinder 实例

    Returns:
        VisionPipeline: 配置好的 pipeline 实例
    """
    ctx = context or SceneContext()
    clf = classifier or DefaultSceneClassifier()
    b = binder or create_default_scene_task_binder()

    observer = SceneObserver(classifier=clf, context=ctx)
    bridge = VisionSceneTaskBridge(observer=observer, binder=b)

    orchestrator: Optional[VisionTaskOrchestrator] = None
    if task_manager is not None:
        orchestrator = VisionTaskOrchestrator(
            bridge=bridge,
            task_manager=task_manager,
        )

    return VisionPipeline(
        context=ctx,
        classifier=clf,
        binder=b,
        observer=observer,
        bridge=bridge,
        orchestrator=orchestrator,
    )

