"""
SceneObserver: 视觉输入 → SceneClassifierInput 的转换层

职责：
- 接收 OCR 文本行列表和 YOLO 物体标签列表
- 转换为 SceneClassifier 需要的统一输入格式
- 不直接触碰 TaskChain，只做数据转换
"""

from typing import List, Optional

from task_engine.scene.scene_classifier import SceneClassifier, SceneGuess


class SceneObserver:
    """
    将 OCR + YOLO 结果转换为统一的场景识别输入。

    这个类只负责数据转换，不直接动 TaskChain。
    """

    def __init__(self, classifier: SceneClassifier) -> None:
        """
        Args:
            classifier: SceneClassifier 实例，用于场景识别
        """
        self.classifier = classifier

    def observe(
        self,
        ocr_lines: Optional[List[str]] = None,
        objects: Optional[List[str]] = None,
        history_tags: Optional[List[str]] = None,
        gps_hint: Optional[str] = None,
    ) -> SceneGuess:
        """
        观察视觉输入并返回场景识别结果。

        Args:
            ocr_lines: OCR 识别到的文本行列表
            objects: YOLO 识别到的物体标签列表（类名或高层标签，如 "ticket_machine", "gate"）
            history_tags: 历史访问过的场景标签
            gps_hint: 可选的 GPS 文本提示

        Returns:
            SceneGuess: 场景识别结果
        """
        # 将 OCR 行列表合并为单个文本字符串
        text = " ".join(ocr_lines or [])

        # 调用 SceneClassifier 进行分类
        return self.classifier.classify(
            ocr_text=text if text else None,
            objects=objects or [],
            history_tags=history_tags or [],
            gps_hint=gps_hint,
        )

