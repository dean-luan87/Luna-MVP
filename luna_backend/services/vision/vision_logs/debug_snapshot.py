"""
用于保存调试时的截图、框图、可视化 (v1.2.0)
"""

import os
import cv2
import numpy as np
from typing import Optional, Tuple, List, Dict
from datetime import datetime
from utils.logger import vision_log


class DebugSnapshot:
    """调试快照管理器"""
    
    def __init__(self, root: str = "debug_snapshots", enabled: bool = False):
        """
        初始化调试快照管理器
        
        Args:
            root: 快照保存根目录
            enabled: 是否启用快照功能
        """
        self.root = root
        self.enabled = enabled
        
        if self.enabled:
            os.makedirs(root, exist_ok=True)
            vision_log("DEBUG_SNAPSHOT_INIT", {"root": root, "enabled": enabled})
    
    def save(self, frame: np.ndarray, name: str, draw_boxes: Optional[List[Dict]] = None) -> Optional[str]:
        """
        保存快照
        
        Args:
            frame: 图像帧（numpy数组）
            name: 快照名称
            draw_boxes: 要绘制的边界框列表（可选）
        
        Returns:
            保存的文件路径，如果未启用则返回None
        """
        if not self.enabled:
            return None
        
        try:
            # 复制帧以避免修改原始数据
            snapshot = frame.copy()
            
            # 绘制边界框（如果有）
            if draw_boxes:
                for box in draw_boxes:
                    x1, y1, x2, y2 = box.get("bbox", (0, 0, 0, 0))
                    label = box.get("label", "")
                    color = box.get("color", (0, 255, 0))
                    
                    cv2.rectangle(snapshot, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
                    if label:
                        cv2.putText(snapshot, label, (int(x1), int(y1) - 10),
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            
            # 生成文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = f"{name}_{timestamp}.jpg"
            path = os.path.join(self.root, filename)
            
            # 保存图像
            cv2.imwrite(path, snapshot)
            
            vision_log("DEBUG_SNAPSHOT_SAVED", {"path": path, "name": name})
            
            return path
            
        except Exception as e:
            vision_log("DEBUG_SNAPSHOT_ERROR", {"error": str(e), "name": name})
            return None
    
    def save_with_detections(self, frame: np.ndarray, detections: List[Dict], name: str) -> Optional[str]:
        """
        保存带检测结果的快照
        
        Args:
            frame: 图像帧
            detections: 检测结果列表
            name: 快照名称
        
        Returns:
            保存的文件路径
        """
        draw_boxes = []
        for det in detections:
            bbox = det.get("bbox", [])
            if len(bbox) >= 4:
                draw_boxes.append({
                    "bbox": bbox,
                    "label": det.get("label", ""),
                    "color": (0, 255, 0)  # 绿色
                })
        
        return self.save(frame, name, draw_boxes)
    
    def enable(self):
        """启用快照功能"""
        self.enabled = True
        os.makedirs(self.root, exist_ok=True)
    
    def disable(self):
        """禁用快照功能"""
        self.enabled = False

