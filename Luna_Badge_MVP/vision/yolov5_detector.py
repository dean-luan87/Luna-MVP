#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YOLOv5 检测器
"""

import cv2
import numpy as np
import torch
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class YOLOv5Detector:
    """YOLOv5检测器"""
    
    def __init__(self):
        """初始化检测器"""
        self.model = None
        self.device = None
        self.confidence_threshold = 0.5
        self.nms_threshold = 0.4
        self.input_size = 640
        
        logger.info("✅ YOLOv5检测器初始化完成")
    
    def initialize(self, model_path: str = "yolov5n.pt") -> bool:
        """
        初始化模型
        
        Args:
            model_path: 模型文件路径
            
        Returns:
            bool: 是否初始化成功
        """
        try:
            # 检查是否有GPU
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            logger.info(f"使用设备: {self.device}")
            
            # 加载模型
            self.model = torch.hub.load('ultralytics/yolov5', 'yolov5n', pretrained=True)
            self.model.to(self.device)
            self.model.eval()
            
            logger.info(f"✅ YOLOv5模型加载成功: {model_path}")
            return True
            
        except Exception as e:
            logger.error(f"❌ YOLOv5模型加载失败: {e}")
            return False
    
    def detect(self, frame: np.ndarray) -> List[Dict[str, Any]]:
        """
        检测目标
        
        Args:
            frame: 输入图像帧
            
        Returns:
            List[Dict[str, Any]]: 检测结果列表
        """
        try:
            if self.model is None:
                logger.warning("⚠️ 模型未初始化")
                return []
            
            # 运行检测
            results = self.model(frame)
            
            # 解析结果
            detections = []
            for *box, conf, cls in results.xyxy[0].cpu().numpy():
                if conf > self.confidence_threshold:
                    x1, y1, x2, y2 = box
                    detection = {
                        "bbox": [int(x1), int(y1), int(x2), int(y2)],
                        "confidence": float(conf),
                        "class_id": int(cls),
                        "class_name": self.model.names[int(cls)]
                    }
                    detections.append(detection)
            
            return detections
            
        except Exception as e:
            logger.error(f"❌ 目标检测失败: {e}")
            return []
    
    def set_threshold(self, confidence: float, nms: float):
        """
        设置阈值
        
        Args:
            confidence: 置信度阈值
            nms: NMS阈值
        """
        self.confidence_threshold = confidence
        self.nms_threshold = nms
        logger.info(f"✅ 阈值设置完成: confidence={confidence}, nms={nms}")
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        获取模型信息
        
        Returns:
            Dict[str, Any]: 模型信息
        """
        return {
            "model_loaded": self.model is not None,
            "device": str(self.device),
            "confidence_threshold": self.confidence_threshold,
            "nms_threshold": self.nms_threshold,
            "input_size": self.input_size
        }

# 使用示例
if __name__ == "__main__":
    # 创建检测器
    detector = YOLOv5Detector()
    
    # 初始化模型
    if detector.initialize():
        print("✅ YOLOv5检测器初始化成功")
        
        # 测试检测
        test_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        detections = detector.detect(test_frame)
        print(f"检测结果: {len(detections)} 个目标")
    else:
        print("❌ YOLOv5检测器初始化失败")
