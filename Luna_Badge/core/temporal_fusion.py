"""
时序融合模块（借鉴BEVFormer的时序融合机制）
用于提高检测稳定性和减少误检
"""

import logging
from typing import Dict, List, Any, Optional
from collections import deque
import numpy as np

logger = logging.getLogger(__name__)

class TemporalFusion:
    """时序融合（借鉴BEVFormer的时序融合机制）"""
    
    def __init__(self, window_size: int = 3, vote_threshold: int = 2):
        """
        初始化时序融合器
        
        Args:
            window_size: 时序窗口大小（保留最近N帧）
            vote_threshold: 投票阈值（物体需要在至少N帧中出现才认为是稳定的）
        """
        self.window_size = window_size
        self.vote_threshold = vote_threshold
        self.history = deque(maxlen=window_size)
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"✅ 时序融合器初始化完成（窗口大小: {window_size}）")
    
    def fuse(self, current_detection: Dict[str, Any]) -> Dict[str, Any]:
        """
        使用时序信息融合当前检测结果
        
        Args:
            current_detection: {
                'objects': List[Dict],
                'texts': List[Dict],
                'signboards': List[Dict],
                'step_detected': bool,
                'hazards': List[Dict]
            }
        
        Returns:
            融合后的稳定检测结果
        """
        # 1. 添加到历史
        self.history.append(current_detection)
        
        # 2. 如果历史数据不足，直接返回当前结果
        if len(self.history) < self.vote_threshold:
            return current_detection
        
        # 3. 时序投票：只保留在多帧中出现的物体
        stable_objects = self._temporal_voting('objects')
        stable_texts = self._temporal_voting('texts')
        stable_signboards = self._temporal_voting('signboards')
        
        # 4. 时序平滑：台阶和危险检测（需要连续多帧才确认）
        stable_step = self._temporal_smooth_bool('step_detected')
        stable_hazards = self._temporal_voting('hazards')
        
        # 5. 计算置信度提升
        confidence_boost = self._calculate_confidence_boost()
        
        return {
            'objects': stable_objects,
            'texts': stable_texts,
            'signboards': stable_signboards,
            'step_detected': stable_step,
            'hazards': stable_hazards,
            'confidence_boost': confidence_boost,
            'stability_score': len(stable_objects) / max(len(current_detection.get('objects', [])), 1)
        }
    
    def _temporal_voting(self, key: str) -> List[Dict[str, Any]]:
        """
        时序投票：只保留在多帧中出现的物体
        
        Args:
            key: 检测结果中的键名（'objects', 'texts', 'signboards'等）
        
        Returns:
            稳定的物体列表
        """
        if not self.history:
            return []
        
        # 统计每个物体出现的次数
        object_votes = {}
        object_instances = {}
        
        for frame in self.history:
            items = frame.get(key, [])
            for item in items:
                # 生成物体唯一标识
                item_id = self._generate_item_id(item, key)
                
                if item_id not in object_votes:
                    object_votes[item_id] = 0
                    object_instances[item_id] = item
                
                object_votes[item_id] += 1
        
        # 只保留投票数>=threshold的物体
        stable_items = []
        for item_id, votes in object_votes.items():
            if votes >= self.vote_threshold:
                item = object_instances[item_id].copy()
                # 提升置信度（基于投票数）
                if 'confidence' in item:
                    item['confidence'] = min(1.0, item['confidence'] * (1 + votes * 0.1))
                item['temporal_votes'] = votes
                stable_items.append(item)
        
        return stable_items
    
    def _generate_item_id(self, item: Dict[str, Any], key: str) -> str:
        """生成物体的唯一标识"""
        if key == 'objects':
            # 对于物体：使用类别+位置
            bbox = item.get('bbox', (0, 0, 0, 0))
            return f"{item.get('class', 'unknown')}_{bbox[0]}_{bbox[1]}"
        elif key == 'texts':
            # 对于文字：使用文字内容
            text = item.get('text', '')
            bbox = item.get('bbox', (0, 0, 0, 0))
            return f"text_{text[:20]}_{bbox[0]}_{bbox[1]}"
        elif key == 'signboards':
            # 对于标识牌：使用类型+位置
            sign_type = item.get('type', 'unknown')
            bbox = item.get('bbox', (0, 0, 0, 0))
            return f"sign_{sign_type}_{bbox[0]}_{bbox[1]}"
        elif key == 'hazards':
            # 对于危险：使用类型+位置
            hazard_type = item.get('type', 'unknown')
            bbox = item.get('bbox', (0, 0, 0, 0))
            return f"hazard_{hazard_type}_{bbox[0]}_{bbox[1]}"
        else:
            return str(hash(str(item)))
    
    def _temporal_smooth_bool(self, key: str) -> bool:
        """
        时序平滑：布尔值需要连续多帧才确认
        
        Args:
            key: 检测结果中的键名（如'step_detected'）
        
        Returns:
            平滑后的布尔值
        """
        if not self.history:
            return False
        
        # 统计最近N帧中为True的次数
        true_count = sum(1 for frame in self.history if frame.get(key, False))
        
        # 如果超过一半的帧都为True，则认为是稳定的
        return true_count >= (len(self.history) // 2 + 1)
    
    def _calculate_confidence_boost(self) -> float:
        """计算置信度提升（基于时序稳定性）"""
        if len(self.history) < self.vote_threshold:
            return 1.0
        
        # 计算最近几帧的一致性
        # 简单实现：如果最近3帧的检测结果相似度高，则提升置信度
        consistency_score = 0.0
        
        if len(self.history) >= 3:
            # 比较最近3帧的物体数量
            recent_counts = [len(frame.get('objects', [])) for frame in list(self.history)[-3:]]
            if len(set(recent_counts)) == 1:  # 数量一致
                consistency_score += 0.2
        
        # 置信度提升：1.0（无提升）到1.3（30%提升）
        confidence_boost = 1.0 + consistency_score
        
        return min(1.3, confidence_boost)
    
    def reset(self):
        """重置历史记录"""
        self.history.clear()
        self.logger.info("🔄 时序融合器历史记录已重置")






