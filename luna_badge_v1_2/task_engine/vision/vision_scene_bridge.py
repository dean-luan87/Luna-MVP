"""
VisionSceneTaskBridge: 视觉 → 场景 → 任务建议的统一桥接

Pro-1 核心：把 VisionEvent 串到 Scene + Task 建议。

它不直接调用 TaskChainManager，只返回推荐的 task_meta，
由上层决定是否调用 register_task()。
"""

from dataclasses import dataclass
from typing import Optional

from task_engine.vision.vision_event import VisionEvent
from task_engine.vision.scene_observer import SceneObserver
from task_engine.scene.scene_task_binder import SceneTaskBinder
from task_engine.scene.scene_context import SceneContext
from task_engine.scene.scene_classifier import SceneGuess


@dataclass
class VisionSceneTaskResult:
    """
    视觉 → 场景 → 任务建议 的统一结果。
    """

    scene: Optional[str]
    tag: Optional[str]
    confidence: float
    suggested_task_meta: Optional[dict]
    context: SceneContext
    reason: str = ""


class VisionSceneTaskBridge:
    """
    Pro-1 核心：把 VisionEvent 串到 Scene + Task 建议。

    它不直接调用 TaskChainManager，只返回推荐的 task_meta，
    由上层决定是否调用 register_task()。
    """

    def __init__(
        self,
        observer: SceneObserver,
        binder: SceneTaskBinder,
    ) -> None:
        """
        Args:
            observer: SceneObserver 实例，用于场景识别
            binder: SceneTaskBinder 实例，用于任务建议
        """
        self._observer = observer
        self._binder = binder

    def handle_vision_event(self, event: VisionEvent) -> VisionSceneTaskResult:
        """
        处理视觉事件，返回场景识别结果和任务建议。

        Args:
            event: VisionEvent 实例

        Returns:
            VisionSceneTaskResult: 包含场景信息、任务建议和上下文的结果
        """
        # 使用 observer 进行场景识别
        # 获取当前上下文的 history_tags
        current_ctx = self._observer._context
        history_tags = current_ctx.history_tags if current_ctx else None
        
        guess, ctx = self._observer.observe(
            ocr_lines=event.ocr_lines,
            objects=event.objects,
            history_tags=history_tags,
        )

        scene = guess.scene
        tag = guess.tag
        confidence = guess.confidence
        reason = getattr(guess, "reason", "")

        # 使用 binder 获取任务建议
        task_meta = self._binder.suggest_task(ctx)

        return VisionSceneTaskResult(
            scene=scene,
            tag=tag,
            confidence=confidence,
            suggested_task_meta=task_meta,
            context=ctx,
            reason=reason,
        )

