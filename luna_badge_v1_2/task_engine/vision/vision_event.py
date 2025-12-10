"""
VisionEvent: 视觉输入事件模型

表示一次视觉输入事件（OCR + 物体检测）。
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
import time


@dataclass
class VisionEvent:
    """
    表示一次视觉输入事件（OCR + 物体检测）。

    - ocr_lines: OCR 识别的文本行
    - objects:   目标检测模型识别出的物体标签（如 ticket_machine, gate）
    - timestamp: 事件发生时间（秒级）
    - source:    来源标识，如 'camera_front', 'camera_badge'
    - meta:      预留扩展字段（模型版本、置信度等）
    """

    ocr_lines: List[str] = field(default_factory=list)
    objects: List[str] = field(default_factory=list)
    timestamp: float = field(default_factory=lambda: time.time())
    source: str = "camera"
    meta: Dict[str, Any] = field(default_factory=dict)

    def text(self) -> str:
        """将 OCR 文本拼成一段，用于 SceneClassifier 输入。"""
        return " ".join(self.ocr_lines or [])

