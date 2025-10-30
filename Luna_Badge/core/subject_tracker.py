#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 多主体追踪模块
实时检测和追踪家庭成员 vs 陌生人状态
"""

import logging
import json
import time
import os
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import numpy as np

logger = logging.getLogger(__name__)

class DetectionType(Enum):
    """检测类型"""
    KNOWN = "known"           # 已知（家人）
    UNKNOWN = "unknown"      # 未知（陌生人）

class PositionType(Enum):
    """位置类型"""
    FRONT_LEFT = "left-front"
    FRONT_CENTER = "center-front"
    FRONT_RIGHT = "right-front"
    REAR_LEFT = "rear-left"
    REAR_CENTER = "rear-center"
    REAR_RIGHT = "rear-right"
    SIDE_LEFT = "side-left"
    SIDE_RIGHT = "side-right"

@dataclass
class TrackedSubject:
    """追踪对象"""
    face_id: str                 # 人脸ID
    detection_type: DetectionType  # 检测类型
    position: str               # 位置
    relation: Optional[str]      # 关系（如果是家人）
    nickname: Optional[str]      # 昵称
    confidence: float            # 置信度
    timestamp: float            # 时间戳
    bbox: Tuple[int, int, int, int]  # 边界框

@dataclass
class TrackingEvent:
    """追踪事件"""
    event_type: str              # 事件类型
    subject_id: str             # 对象ID
    position: str               # 位置
    relation: Optional[str]     # 关系
    confidence: float           # 置信度
    timestamp: str              # 时间戳
    metadata: Dict[str, Any]    # 元数据
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "event_type": self.event_type,
            "subject_id": self.subject_id,
            "position": self.position,
            "relation": self.relation,
            "confidence": self.confidence,
            "timestamp": self.timestamp,
            "metadata": self.metadata
        }

class SubjectTracker:
    """多主体追踪器"""
    
    def __init__(self, family_registry=None, relationship_mapper=None,
                 log_file: str = "logs/subject_tracking.json"):
        """
        初始化追踪器
        
        Args:
            family_registry: 家庭注册器实例
            relationship_mapper: 关系映射器实例
            log_file: 日志文件路径
        """
        self.logger = logging.getLogger(__name__)
        self.family_registry = family_registry
        self.relationship_mapper = relationship_mapper
        self.log_file = log_file
        
        # 确保日志目录存在
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        # 当前追踪的对象
        self.tracked_subjects: Dict[str, TrackedSubject] = {}
        
        # 事件历史
        self.event_history: List[TrackingEvent] = []
        
        # 统计信息
        self.stats: Dict[str, Any] = {
            "total_detections": 0,
            "known_detections": 0,
            "unknown_detections": 0,
            "family_appearances": {},
            "total_time_tracked": {}
        }
        
        self.logger.info("👥 多主体追踪器初始化完成")
    
    def detect_and_track(self, faces: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        检测和追踪人脸
        
        Args:
            faces: 人脸检测结果列表
            
        Returns:
            List[Dict[str, Any]]: 追踪事件列表
        """
        events = []
        
        for face in faces:
            # 识别是否家人
            recognition_result = self._recognize_face(face)
            
            # 生成追踪事件
            event = self._create_tracking_event(face, recognition_result)
            
            if event:
                events.append(event)
                self.event_history.append(event)
                
                # 更新统计
                self._update_stats(event)
                
                # 记录到日志
                self._log_event(event)
        
        self.logger.debug(f"👥 检测到 {len(events)} 个追踪事件")
        
        return events
    
    def _recognize_face(self, face: Dict[str, Any]) -> Dict[str, Any]:
        """
        识别人脸（家人 vs 陌生人）
        
        Args:
            face: 人脸信息
            
        Returns:
            Dict[str, Any]: 识别结果
        """
        # TODO: 实现真实的人脸识别逻辑
        # 比对家庭注册器中的特征向量
        
        # 模拟识别结果
        is_family = np.random.random() > 0.5  # 50%概率是家人
        
        if is_family and self.family_registry:
            # 假设匹配到家人
            members = self.family_registry.list_all_members()
            if members:
                member = members[0]  # 简化为第一个匹配
                
                # 获取关系配置
                profile = None
                if self.relationship_mapper:
                    profile = self.relationship_mapper.get_relation_by_face(member.face_id)
                
                return {
                    "detection_type": DetectionType.KNOWN.value,
                    "face_id": member.face_id,
                    "relation": member.relationship,
                    "label": member.label,
                    "nickname": profile.nickname if profile else None,
                    "confidence": 0.92
                }
        
        # 陌生人
        return {
            "detection_type": DetectionType.UNKNOWN.value,
            "face_id": "unknown",
            "relation": None,
            "label": None,
            "nickname": None,
            "confidence": 0.8,
            "alert_level": "medium"
        }
    
    def _create_tracking_event(self, face: Dict[str, Any], 
                              recognition: Dict[str, Any]) -> Optional[TrackingEvent]:
        """创建追踪事件"""
        # 确定位置
        position = self._determine_position(face.get("bbox"))
        
        # 确定事件类型
        if recognition["detection_type"] == DetectionType.KNOWN.value:
            event_type = "family_detected"
        else:
            event_type = "stranger_detected"
        
        # 检查是否持续靠近
        alert_level = self._check_proximity_threat(recognition)
        
        event = TrackingEvent(
            event_type=event_type,
            subject_id=recognition["face_id"],
            position=position,
            relation=recognition.get("relation"),
            confidence=recognition.get("confidence", 0.8),
            timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            metadata={
                "bbox": face.get("bbox"),
                "label": recognition.get("label"),
                "nickname": recognition.get("nickname"),
                "alert_level": recognition.get("alert_level", "none"),
                "proximity_alert": alert_level
            }
        )
        
        return event
    
    def _determine_position(self, bbox: Tuple[int, int, int, int]) -> str:
        """
        确定人脸位置
        
        Args:
            bbox: 边界框
            
        Returns:
            str: 位置描述
        """
        # TODO: 实现真实的位置计算逻辑
        # 基于图像中心和bbox位置关系
        return PositionType.FRONT_CENTER.value  # 简化实现
    
    def _check_proximity_threat(self, recognition: Dict[str, Any]) -> str:
        """检查接近威胁"""
        if recognition["detection_type"] == DetectionType.UNKNOWN.value:
            # 陌生人持续靠近
            return "medium"
        return "none"
    
    def _update_stats(self, event: TrackingEvent):
        """更新统计信息"""
        self.stats["total_detections"] += 1
        
        if event.event_type == "family_detected":
            self.stats["known_detections"] += 1
            
            # 记录家庭出现次数
            if event.relation:
                if event.relation not in self.stats["family_appearances"]:
                    self.stats["family_appearances"][event.relation] = 0
                self.stats["family_appearances"][event.relation] += 1
        else:
            self.stats["unknown_detections"] += 1
    
    def _log_event(self, event: TrackingEvent):
        """记录事件到日志文件"""
        try:
            # 读取现有日志
            events = []
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    events = json.load(f)
            
            # 添加新事件
            events.append(event.to_dict())
            
            # 保存日志
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(events, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.logger.error(f"⚠️ 记录事件失败: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return self.stats
    
    def generate_daily_report(self) -> Dict[str, Any]:
        """生成每日报告"""
        return {
            "date": time.strftime("%Y-%m-%d", time.gmtime()),
            "total_detections": self.stats["total_detections"],
            "known_detections": self.stats["known_detections"],
            "unknown_detections": self.stats["unknown_detections"],
            "family_appearances": self.stats["family_appearances"],
            "events_count": len(self.event_history)
        }


# 全局追踪器实例
global_subject_tracker = None

def get_subject_tracker(family_registry=None, relationship_mapper=None) -> SubjectTracker:
    """获取追踪器实例"""
    global global_subject_tracker
    if global_subject_tracker is None:
        global_subject_tracker = SubjectTracker(family_registry, relationship_mapper)
    return global_subject_tracker


if __name__ == "__main__":
    # 测试追踪器
    import logging
    logging.basicConfig(level=logging.INFO)
    
    # 创建模拟的注册器和映射器
    class MockRegistry:
        def list_all_members(self):
            return []
    
    class MockMapper:
        pass
    
    registry = MockRegistry()
    mapper = MockMapper()
    
    tracker = SubjectTracker(registry, mapper)
    
    print("=" * 70)
    print("👥 多主体追踪器测试")
    print("=" * 70)
    
    # 模拟检测
    mock_faces = [
        {"bbox": (100, 100, 200, 200)},
        {"bbox": (300, 100, 400, 200)}
    ]
    
    events = tracker.detect_and_track(mock_faces)
    
    print("\n检测结果:")
    for event in events:
        print(json.dumps(event.to_dict(), ensure_ascii=False, indent=2))
    
    # 显示统计
    stats = tracker.get_stats()
    print("\n统计信息:")
    print(json.dumps(stats, ensure_ascii=False, indent=2))
    
    print("\n" + "=" * 70)

