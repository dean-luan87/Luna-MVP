"""
SceneObserver: OCR + YOLO → SceneClassifier 的适配层

职责：
- 将视觉输入转换为场景识别输入
- 更新 SceneContext
- 不启动任务，只负责场景识别
"""

from typing import List, Optional, Tuple

from task_engine.scene.scene_classifier import SceneClassifier, SceneGuess
from task_engine.scene.scene_context import SceneContext


class SceneObserver:
    """
    OCR + YOLO → SceneClassifier 的适配层。

    - 不关心具体模型实现，只依赖 SceneClassifier 的 classify() 接口。
    - 不启动任务，只负责更新 SceneContext。
    """

    def __init__(self, classifier: SceneClassifier, context: SceneContext) -> None:
        """
        Args:
            classifier: SceneClassifier 实例，用于场景识别
            context: SceneContext 实例，用于存储识别结果
        """
        self._classifier = classifier
        self._context = context

    def observe(
        self,
        ocr_lines: Optional[List[str]] = None,
        objects: Optional[List[str]] = None,
        history_tags: Optional[List[str]] = None,
    ) -> Tuple[SceneGuess, SceneContext]:
        """
        观察视觉输入并返回场景识别结果。

        Args:
            ocr_lines: OCR 识别到的文本行列表
            objects: YOLO 识别到的物体标签列表
            history_tags: 历史访问过的场景标签（如果为 None，使用 context 的 history_tags）

        Returns:
            Tuple[SceneGuess, SceneContext]: 场景识别结果和更新后的上下文
        """
        # 将 OCR 行列表合并为单个文本字符串
        text = " ".join(ocr_lines or [])

        # 使用 context 的 history_tags 如果未提供
        if history_tags is None:
            history_tags = self._context.history_tags

        # 调用 SceneClassifier 进行分类
        guess = self._classifier.classify(
            ocr_text=text if text else None,
            objects=objects or [],
            history_tags=history_tags or [],
        )

        # 更新上下文（SceneContext.update_from_guess 是就地修改）
        self._context.update_from_guess(
            guess,
            ocr_text=text if text else None,
            objects=objects,
            append_history_tag=True,
        )

        return guess, self._context












