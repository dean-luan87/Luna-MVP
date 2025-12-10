"""
DensityEstimator（动态路况密度分析器，1.3.0 MVP）

作用：
- 使用 YOLO 检测框
- 统计与导航相关的目标数量
- 输出用于 frame_scheduler 的 count

说明：
- YOLO 推理逻辑由外部执行
- 本模块只处理 YOLO 输出（boxes）
"""

from typing import List, Any


class DensityEstimator:
    def __init__(self):
        # 导航相关类别白名单
        # YOLOv8/YOLO11 的类别 ID 可能不同，后续可通过配置注入
        self.whitelist = [
            "person",
            "bicycle",
            "motorcycle",
            "car",
            "bus",
            "truck",
            "dog",
            "cat",
        ]

    # --------------------------------------------------------- #
    # 主入口
    # --------------------------------------------------------- #

    def count_objects(self, yolo_result: Any) -> int:
        """
        输入：YOLO 检测结果（单帧）
        输出：与导航相关的对象数量
        """

        if yolo_result is None:
            return 0

        boxes = getattr(yolo_result, "boxes", None)
        if boxes is None or len(boxes) == 0:
            return 0

        names = getattr(yolo_result, "names", {})

        count = 0

        for box in boxes:
            cls_id = int(box.cls[0])
            name = names.get(cls_id, "")

            if name in self.whitelist:
                count += 1

        return count














