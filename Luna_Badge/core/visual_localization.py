"""
视觉定位模块（借鉴ORB-SLAM2的特征跟踪）
用于实时定位和场景识别
"""

import cv2
import numpy as np
import logging
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
import time

logger = logging.getLogger(__name__)

@dataclass
class KeyFrame:
    """关键帧"""
    timestamp: float
    image: np.ndarray
    keypoints: List[cv2.KeyPoint]
    descriptors: np.ndarray
    location_info: Dict[str, Any]  # 位置信息（楼层、房间号等）

class VisualLocalization:
    """视觉定位（借鉴ORB-SLAM2的特征跟踪）"""
    
    def __init__(self, n_features: int = 500, match_threshold: float = 0.7):
        """
        初始化视觉定位系统
        
        Args:
            n_features: ORB特征点数量
            match_threshold: 匹配阈值（0-1）
        """
        # 使用ORB特征（轻量级，适合实时）
        self.orb = cv2.ORB_create(nfeatures=n_features)
        
        # 特征匹配器
        self.bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        
        # 关键帧数据库
        self.keyframes: List[KeyFrame] = []
        
        # 匹配阈值
        self.match_threshold = match_threshold
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("✅ 视觉定位系统初始化完成")
    
    def extract_features(self, image: np.ndarray) -> Tuple[List[cv2.KeyPoint], np.ndarray]:
        """
        提取ORB特征
        
        Args:
            image: 输入图像
        
        Returns:
            (关键点列表, 描述符)
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        keypoints, descriptors = self.orb.detectAndCompute(gray, None)
        
        if descriptors is None:
            descriptors = np.array([])
        
        return keypoints, descriptors
    
    def add_keyframe(self, image: np.ndarray, location_info: Optional[Dict[str, Any]] = None):
        """
        添加关键帧
        
        Args:
            image: 图像
            location_info: 位置信息（如{'floor': 3, 'room': '101'}）
        """
        keypoints, descriptors = self.extract_features(image)
        
        keyframe = KeyFrame(
            timestamp=time.time(),
            image=image.copy(),
            keypoints=keypoints,
            descriptors=descriptors,
            location_info=location_info or {}
        )
        
        self.keyframes.append(keyframe)
        self.logger.info(f"✅ 添加关键帧（总数: {len(self.keyframes)}）")
    
    def match_location(self, current_image: np.ndarray) -> Optional[Dict[str, Any]]:
        """
        匹配当前位置
        
        Args:
            current_image: 当前图像
        
        Returns:
            匹配的位置信息，如果没有匹配则返回None
        """
        if not self.keyframes:
            return None
        
        # 提取当前图像的特征
        current_kp, current_desc = self.extract_features(current_image)
        
        if current_desc is None or len(current_desc) == 0:
            return None
        
        best_match = None
        best_score = 0.0
        
        # 与所有关键帧匹配
        for keyframe in self.keyframes:
            if keyframe.descriptors is None or len(keyframe.descriptors) == 0:
                continue
            
            # 特征匹配
            matches = self.bf.match(current_desc, keyframe.descriptors)
            
            # 计算匹配得分（匹配数量 / 特征点数量）
            match_score = len(matches) / max(len(current_kp), len(keyframe.keypoints), 1)
            
            if match_score > best_score:
                best_score = match_score
                best_match = {
                    'keyframe': keyframe,
                    'match_score': match_score,
                    'matches': matches
                }
        
        # 如果匹配得分超过阈值，返回位置信息
        if best_match and best_match['match_score'] >= self.match_threshold:
            return {
                'location_info': best_match['keyframe'].location_info,
                'match_score': best_match['match_score'],
                'timestamp': best_match['keyframe'].timestamp
            }
        
        return None
    
    def recognize_scene(self, current_image: np.ndarray) -> Optional[str]:
        """
        识别场景（基于视觉特征）
        
        Args:
            current_image: 当前图像
        
        Returns:
            场景类型（如'corridor', 'room', 'elevator_hall'等）
        """
        match_result = self.match_location(current_image)
        
        if match_result:
            location_info = match_result['location_info']
            scene_type = location_info.get('scene_type')
            return scene_type
        
        return None
    
    def get_nearby_keyframes(self, current_image: np.ndarray, 
                           max_distance: float = 0.3) -> List[Dict[str, Any]]:
        """
        获取附近的关键帧
        
        Args:
            current_image: 当前图像
            max_distance: 最大距离阈值
        
        Returns:
            附近的关键帧列表
        """
        current_kp, current_desc = self.extract_features(current_image)
        
        if current_desc is None or len(current_desc) == 0:
            return []
        
        nearby_keyframes = []
        
        for keyframe in self.keyframes:
            if keyframe.descriptors is None or len(keyframe.descriptors) == 0:
                continue
            
            matches = self.bf.match(current_desc, keyframe.descriptors)
            match_score = len(matches) / max(len(current_kp), len(keyframe.keypoints), 1)
            
            if match_score >= max_distance:
                nearby_keyframes.append({
                    'keyframe': keyframe,
                    'match_score': match_score,
                    'location_info': keyframe.location_info
                })
        
        # 按匹配得分排序
        nearby_keyframes.sort(key=lambda x: x['match_score'], reverse=True)
        
        return nearby_keyframes
    
    def cleanup_old_keyframes(self, max_age_seconds: float = 3600):
        """
        清理旧的关键帧
        
        Args:
            max_age_seconds: 最大保留时间（秒）
        """
        current_time = time.time()
        original_count = len(self.keyframes)
        
        self.keyframes = [
            kf for kf in self.keyframes
            if current_time - kf.timestamp < max_age_seconds
        ]
        
        removed_count = original_count - len(self.keyframes)
        if removed_count > 0:
            self.logger.info(f"🗑️ 清理了 {removed_count} 个旧关键帧")

