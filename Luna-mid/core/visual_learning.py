#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视觉学习引擎
记录视觉识别结果，学习物体特征，优化识别准确率
"""

__version__ = "1.0.0"
__version_info__ = (1, 0, 0)

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict

logger = logging.getLogger(__name__)


class RecognitionSource(Enum):
    """识别来源枚举"""
    CAMERA = "camera"  # 摄像头
    IMAGE = "image"  # 图片文件
    VIDEO = "video"  # 视频文件
    USER_UPLOAD = "user_upload"  # 用户上传


class ObjectCategory(Enum):
    """物体类别枚举"""
    PERSON = "person"
    VEHICLE = "vehicle"
    BUILDING = "building"
    SIGN = "sign"
    OBSTACLE = "obstacle"
    LANDMARK = "landmark"
    OTHER = "other"


@dataclass
class VisualObject:
    """视觉物体"""
    object_id: str
    category: str
    name: Optional[str]  # 物体名称
    confidence: float  # 置信度
    bbox: Dict[str, float]  # 边界框 {x, y, width, height}
    features: Dict[str, Any]  # 特征描述
    location: Optional[Dict[str, Any]] = None  # 位置信息
    timestamp: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'VisualObject':
        """从字典创建"""
        return cls(**data)


@dataclass
class ObjectKnowledge:
    """物体知识"""
    object_id: str
    category: str
    name: str
    recognition_count: int  # 识别次数
    first_seen: str  # 首次识别时间
    last_seen: str  # 最后识别时间
    locations: List[Dict[str, Any]]  # 出现位置列表
    confidence_history: List[float]  # 置信度历史
    average_confidence: float  # 平均置信度
    features: Dict[str, Any]  # 特征描述
    user_corrections: List[Dict[str, Any]]  # 用户纠正记录
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ObjectKnowledge':
        """从字典创建"""
        return cls(**data)


class VisualLearningEngine:
    """视觉学习引擎"""
    
    def __init__(self, data_dir: Optional[Path] = None):
        """
        初始化视觉学习引擎
        
        Args:
            data_dir: 数据存储目录，默认为 ./data/visual_learning
        """
        if data_dir is None:
            data_dir = Path(__file__).parent.parent.parent / "data" / "visual_learning"
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.objects_file = self.data_dir / "objects.json"
        self.knowledge_file = self.data_dir / "knowledge.json"
        
        # 内存缓存
        self._objects: List[VisualObject] = []
        self._knowledge: Dict[str, ObjectKnowledge] = {}
        
        # 加载数据
        self._load_data()
    
    def _load_data(self):
        """加载历史数据"""
        try:
            # 加载物体记录
            if self.objects_file.exists():
                with open(self.objects_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._objects = [VisualObject.from_dict(o) for o in data]
                logger.info(f"已加载 {len(self._objects)} 条物体记录")
            
            # 加载知识库
            if self.knowledge_file.exists():
                with open(self.knowledge_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._knowledge = {
                        obj_id: ObjectKnowledge.from_dict(k)
                        for obj_id, k in data.items()
                    }
                logger.info(f"已加载 {len(self._knowledge)} 条知识记录")
        except Exception as e:
            logger.error(f"加载数据失败: {e}")
    
    def _save_data(self):
        """保存数据到文件"""
        try:
            # 保存物体记录（只保存最近1000条）
            objects_data = [o.to_dict() for o in self._objects[-1000:]]
            with open(self.objects_file, 'w', encoding='utf-8') as f:
                json.dump(objects_data, f, ensure_ascii=False, indent=2)
            
            # 保存知识库
            knowledge_data = {
                obj_id: k.to_dict()
                for obj_id, k in self._knowledge.items()
            }
            with open(self.knowledge_file, 'w', encoding='utf-8') as f:
                json.dump(knowledge_data, f, ensure_ascii=False, indent=2)
            
            logger.debug("数据保存成功")
        except Exception as e:
            logger.error(f"保存数据失败: {e}")
    
    def record_recognition(
        self,
        category: str,
        name: Optional[str],
        confidence: float,
        bbox: Dict[str, float],
        features: Dict[str, Any],
        source: str = "camera",
        location: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> str:
        """
        记录识别结果
        
        Args:
            category: 物体类别
            name: 物体名称
            confidence: 置信度
            bbox: 边界框
            features: 特征描述
            source: 识别来源
            location: 位置信息
            **kwargs: 其他参数
            
        Returns:
            物体ID
        """
        object_id = f"obj_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        obj = VisualObject(
            object_id=object_id,
            category=category,
            name=name,
            confidence=confidence,
            bbox=bbox,
            features=features,
            location=location,
            timestamp=datetime.now().isoformat(),
            **kwargs
        )
        
        # 添加到内存
        self._objects.append(obj)
        
        # 更新知识库
        self._update_knowledge(obj)
        
        # 保存数据
        self._save_data()
        
        logger.debug(f"已记录识别结果: {object_id} ({category})")
        return object_id
    
    def _update_knowledge(self, obj: VisualObject):
        """更新知识库"""
        # 使用物体名称或类别作为知识ID
        knowledge_id = obj.name if obj.name else f"{obj.category}_{obj.object_id[:8]}"
        
        if knowledge_id not in self._knowledge:
            # 创建新知识
            knowledge = ObjectKnowledge(
                object_id=knowledge_id,
                category=obj.category,
                name=obj.name or obj.category,
                recognition_count=1,
                first_seen=obj.timestamp or datetime.now().isoformat(),
                last_seen=obj.timestamp or datetime.now().isoformat(),
                locations=[obj.location] if obj.location else [],
                confidence_history=[obj.confidence],
                average_confidence=obj.confidence,
                features=obj.features,
                user_corrections=[]
            )
            self._knowledge[knowledge_id] = knowledge
        else:
            # 更新现有知识
            knowledge = self._knowledge[knowledge_id]
            knowledge.recognition_count += 1
            knowledge.last_seen = obj.timestamp or datetime.now().isoformat()
            
            if obj.location:
                knowledge.locations.append(obj.location)
                # 只保留最近50个位置
                if len(knowledge.locations) > 50:
                    knowledge.locations = knowledge.locations[-50:]
            
            knowledge.confidence_history.append(obj.confidence)
            # 只保留最近100个置信度
            if len(knowledge.confidence_history) > 100:
                knowledge.confidence_history = knowledge.confidence_history[-100:]
            
            knowledge.average_confidence = sum(knowledge.confidence_history) / len(knowledge.confidence_history)
            
            # 更新特征（合并新特征）
            if obj.features:
                knowledge.features.update(obj.features)
    
    def get_knowledge(self, object_id: Optional[str] = None) -> Dict[str, ObjectKnowledge]:
        """
        获取知识库
        
        Args:
            object_id: 物体ID，如果提供则返回单个知识，否则返回所有
            
        Returns:
            知识字典
        """
        if object_id:
            return {object_id: self._knowledge[object_id]} if object_id in self._knowledge else {}
        return self._knowledge.copy()
    
    def get_frequent_objects(self, limit: int = 10) -> List[ObjectKnowledge]:
        """
        获取频繁出现的物体
        
        Args:
            limit: 返回数量
            
        Returns:
            物体知识列表，按识别次数排序
        """
        objects = sorted(
            self._knowledge.values(),
            key=lambda k: k.recognition_count,
            reverse=True
        )
        return objects[:limit]
    
    def get_objects_by_category(self, category: str) -> List[ObjectKnowledge]:
        """
        获取指定类别的物体
        
        Args:
            category: 物体类别
            
        Returns:
            物体知识列表
        """
        return [
            k for k in self._knowledge.values()
            if k.category == category
        ]
    
    def get_objects_by_location(
        self,
        location: Dict[str, Any],
        radius: float = 100.0
    ) -> List[ObjectKnowledge]:
        """
        获取指定位置附近的物体
        
        Args:
            location: 位置信息 {lat, lon} 或 {x, y}
            radius: 搜索半径（米）
            
        Returns:
            物体知识列表
        """
        # 简化实现：如果有位置信息，返回包含该位置的物体
        # 实际应用中可以使用地理空间索引
        result = []
        for k in self._knowledge.values():
            if k.locations:
                # 检查是否有接近的位置
                for loc in k.locations[-10:]:  # 只检查最近10个位置
                    if loc.get('lat') and location.get('lat'):
                        # 计算距离（简化版）
                        result.append(k)
                        break
        return result
    
    def correct_recognition(
        self,
        object_id: str,
        correct_category: Optional[str] = None,
        correct_name: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> bool:
        """
        纠正识别结果
        
        Args:
            object_id: 物体ID
            correct_category: 正确的类别
            correct_name: 正确的名称
            user_id: 用户ID
            
        Returns:
            是否成功
        """
        if object_id not in self._knowledge:
            logger.warning(f"物体 {object_id} 不存在于知识库")
            return False
        
        knowledge = self._knowledge[object_id]
        
        correction = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "original_category": knowledge.category,
            "original_name": knowledge.name,
            "correct_category": correct_category,
            "correct_name": correct_name
        }
        
        knowledge.user_corrections.append(correction)
        
        # 更新知识
        if correct_category:
            knowledge.category = correct_category
        if correct_name:
            knowledge.name = correct_name
        
        # 保存数据
        self._save_data()
        
        logger.info(f"已纠正物体 {object_id} 的识别结果")
        return True
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        获取统计信息
        
        Returns:
            统计信息字典
        """
        category_counts = defaultdict(int)
        for k in self._knowledge.values():
            category_counts[k.category] += k.recognition_count
        
        return {
            "total_objects": len(self._objects),
            "total_knowledge": len(self._knowledge),
            "category_distribution": dict(category_counts),
            "average_confidence": sum(
                k.average_confidence for k in self._knowledge.values()
            ) / len(self._knowledge) if self._knowledge else 0,
            "total_corrections": sum(
                len(k.user_corrections) for k in self._knowledge.values()
            )
        }
    
    def export_data(self, output_file: Path) -> bool:
        """
        导出数据
        
        Args:
            output_file: 输出文件路径
            
        Returns:
            是否成功
        """
        try:
            data = {
                "objects": [o.to_dict() for o in self._objects[-1000:]],
                "knowledge": {
                    obj_id: k.to_dict()
                    for obj_id, k in self._knowledge.items()
                },
                "export_time": datetime.now().isoformat()
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"已导出数据到 {output_file}")
            return True
        except Exception as e:
            logger.error(f"导出数据失败: {e}")
            return False

