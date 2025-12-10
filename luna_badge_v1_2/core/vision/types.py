"""
Vision Types (v1.3.0)

视觉数据结构定义

定义视觉检测结果的数据结构
"""

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class SceneObj:
    """
    场景对象

    表示检测到的一个物体
    """

    cls: str          # 类别名称，例如 "person", "car"
    conf: float       # 置信度
    bbox: List[int]   # [x1, y1, x2, y2]

    def center(self) -> List[int]:
        """
        返回 bbox 中心点

        Returns:
            List[int]: [cx, cy]
        """
        x1, y1, x2, y2 = self.bbox
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        return [cx, cy]

    def to_dict(self) -> Dict[str, Any]:
        """
        转换为字典

        Returns:
            Dict[str, Any]: 包含 cls、conf、bbox、center 的字典
        """
        return {
            "cls": self.cls,
            "conf": self.conf,
            "bbox": self.bbox,
            "center": self.center(),
        }

    def area(self) -> int:
        """
        返回 bbox 面积

        Returns:
            int: 面积（像素数）
        """
        x1, y1, x2, y2 = self.bbox
        return (x2 - x1) * (y2 - y1)


@dataclass
class SceneFrameResult:
    """
    场景帧检测结果

    表示一帧图像的检测结果
    """

    frame_id: int
    objects: List[SceneObj]
    risk_level: str        # "low" / "medium" / "high"
    timestamp: int         # 毫秒时间戳

    def to_dict(self) -> Dict[str, Any]:
        """
        转换为字典

        Returns:
            Dict[str, Any]: 包含 frame_id、risk_level、timestamp、objects 的字典
        """
        return {
            "frame_id": self.frame_id,
            "risk_level": self.risk_level,
            "timestamp": self.timestamp,
            "objects": [obj.to_dict() for obj in self.objects],
        }

    def get_object_count(self) -> int:
        """返回检测到的对象数量"""
        return len(self.objects)

    def get_objects_by_class(self, class_name: str) -> List[SceneObj]:
        """根据类别名称筛选对象"""
        return [obj for obj in self.objects if obj.cls == class_name]













