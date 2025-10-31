#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 统一数据模型
P1-3: 统一数据结构和转换机制

功能:
- 统一数据模型定义（Pydantic）
- 数据转换层
- 标准化JSON格式
- 数据验证
"""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict, field
from datetime import datetime
from enum import Enum
import json
import logging

logger = logging.getLogger(__name__)


# ==========================================
# 基础数据类型
# ==========================================

class NodeType(Enum):
    """节点类型"""
    LANDMARK = "landmark"           # 地标
    ROOM = "room"                   # 房间
    FACILITY = "facility"           # 设施
    TOILET = "toilet"               # 洗手间
    ELEVATOR = "elevator"           # 电梯
    STAIRS = "stairs"               # 楼梯
    ENTRANCE = "entrance"           # 入口
    EXIT = "exit"                   # 出口
    TRANSIT = "transit"             # 公共交通
    UNKNOWN = "unknown"             # 未知


class LayerType(Enum):
    """图层类型"""
    OUTDOOR = "outdoor"             # 室外
    INDOOR = "indoor"               # 室内
    UNDERGROUND = "underground"     # 地下


class MovementType(Enum):
    """移动类型"""
    WALKING = "walking"             # 步行
    ELEVATOR = "elevator"           # 电梯
    STAIRS = "stairs"               # 楼梯
    ESCALATOR = "escalator"         # 自动扶梯


class EmotionTag(Enum):
    """情绪标签"""
    RECOMMENDED = "推荐"            # 推荐
    QUIET = "安静"                  # 安静
    NOISY = "嘈杂"                  # 嘈杂
    BRIGHT = "明亮"                 # 明亮
    DARK = "昏暗"                   # 昏暗
    CLEAN = "干净"                  # 干净
    WORRY = "担忧"                  # 担忧
    SAFE = "安全"                   # 安全


# ==========================================
# 核心数据模型
# ==========================================

@dataclass
class Position:
    """位置信息"""
    x: float = 0.0                  # X坐标
    y: float = 0.0                  # Y坐标
    z: float = 0.0                  # Z坐标（楼层）
    latitude: Optional[float] = None  # 纬度
    longitude: Optional[float] = None  # 经度
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = {
            "x": self.x,
            "y": self.y,
            "z": self.z
        }
        if self.latitude is not None:
            result["latitude"] = self.latitude
        if self.longitude is not None:
            result["longitude"] = self.longitude
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Position':
        """从字典创建"""
        return cls(
            x=data.get("x", 0.0),
            y=data.get("y", 0.0),
            z=data.get("z", 0.0),
            latitude=data.get("latitude"),
            longitude=data.get("longitude")
        )


@dataclass
class BoundingBox:
    """边界框"""
    x1: int                          # 左上X
    y1: int                          # 左上Y
    x2: int                          # 右下X
    y2: int                          # 右下Y
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "x1": self.x1,
            "y1": self.y1,
            "x2": self.x2,
            "y2": self.y2
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BoundingBox':
        """从字典创建"""
        return cls(
            x1=data["x1"],
            y1=data["y1"],
            x2=data["x2"],
            y2=data["y2"]
        )


@dataclass
class EmotionData:
    """情绪数据"""
    tags: List[str] = field(default_factory=list)  # 情绪标签
    confidence: float = 0.0                          # 置信度
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "tags": self.tags,
            "confidence": self.confidence
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EmotionData':
        """从字典创建"""
        return cls(
            tags=data.get("tags", []),
            confidence=data.get("confidence", 0.0)
        )


@dataclass
class MapNode:
    """地图节点（统一模型）"""
    # 基本信息
    node_id: str                     # 节点ID
    label: str                       # 标签
    node_type: str                   # 节点类型
    
    # 位置信息
    position: Position = field(default_factory=Position)
    layer: str = LayerType.INDOOR.value  # 图层
    
    # 视觉信息
    image_path: Optional[str] = None  # 图像路径
    bounding_box: Optional[BoundingBox] = None  # 边界框
    confidence: float = 0.0           # 识别置信度
    
    # 导航信息
    direction: str = ""               # 方向描述
    distance_meters: float = 0.0      # 距离（米）
    movement_type: str = MovementType.WALKING.value  # 移动类型
    
    # 情绪信息
    emotion: Optional[EmotionData] = None
    
    # 元数据
    notes: str = ""                   # 备注
    level: str = ""                   # 楼层信息（如"3楼"）
    timestamp: str = ""               # 时间戳
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = {
            "node_id": self.node_id,
            "label": self.label,
            "node_type": self.node_type,
            "position": self.position.to_dict(),
            "layer": self.layer,
            "confidence": self.confidence,
            "direction": self.direction,
            "distance_meters": self.distance_meters,
            "movement_type": self.movement_type,
            "notes": self.notes,
            "level": self.level,
            "timestamp": self.timestamp
        }
        
        if self.image_path:
            result["image_path"] = self.image_path
        if self.bounding_box:
            result["bounding_box"] = self.bounding_box.to_dict()
        if self.emotion:
            result["emotion"] = self.emotion.to_dict()
        
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MapNode':
        """从字典创建"""
        return cls(
            node_id=data["node_id"],
            label=data["label"],
            node_type=data["node_type"],
            position=Position.from_dict(data.get("position", {})),
            layer=data.get("layer", LayerType.INDOOR.value),
            image_path=data.get("image_path"),
            bounding_box=BoundingBox.from_dict(data["bounding_box"]) if data.get("bounding_box") else None,
            confidence=data.get("confidence", 0.0),
            direction=data.get("direction", ""),
            distance_meters=data.get("distance_meters", 0.0),
            movement_type=data.get("movement_type", MovementType.WALKING.value),
            emotion=EmotionData.from_dict(data["emotion"]) if data.get("emotion") else None,
            notes=data.get("notes", ""),
            level=data.get("level", ""),
            timestamp=data.get("timestamp", "")
        )


@dataclass
class NavigationPath:
    """导航路径（统一模型）"""
    # 路径基本信息
    path_id: str                     # 路径ID
    path_name: str                   # 路径名称
    description: str = ""            # 描述
    
    # 路径节点
    nodes: List[MapNode] = field(default_factory=list)
    
    # 路径属性
    total_distance_meters: float = 0.0  # 总距离（米）
    estimated_duration_minutes: float = 0.0  # 预计时长（分钟）
    
    # 区域信息
    regions: List[str] = field(default_factory=list)  # 区域列表
    
    # 元数据
    created_at: str = ""             # 创建时间
    updated_at: str = ""             # 更新时间
    version: str = "1.0"             # 版本
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "path_id": self.path_id,
            "path_name": self.path_name,
            "description": self.description,
            "nodes": [node.to_dict() for node in self.nodes],
            "total_distance_meters": self.total_distance_meters,
            "estimated_duration_minutes": self.estimated_duration_minutes,
            "regions": self.regions,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "version": self.version
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'NavigationPath':
        """从字典创建"""
        nodes = [
            MapNode.from_dict(node_data)
            for node_data in data.get("nodes", [])
        ]
        
        return cls(
            path_id=data["path_id"],
            path_name=data["path_name"],
            description=data.get("description", ""),
            nodes=nodes,
            total_distance_meters=data.get("total_distance_meters", 0.0),
            estimated_duration_minutes=data.get("estimated_duration_minutes", 0.0),
            regions=data.get("regions", []),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", ""),
            version=data.get("version", "1.0")
        )


@dataclass
class UserMemory:
    """用户记忆（统一模型）"""
    # 用户信息
    user_id: str                     # 用户ID
    date: str                        # 日期
    
    # 地图记忆
    map_visits: List[Dict[str, Any]] = field(default_factory=list)
    
    # 行为记录
    app_behavior: Dict[str, Any] = field(default_factory=dict)
    
    # 元数据
    created_at: str = ""             # 创建时间
    updated_at: str = ""             # 更新时间
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "user_id": self.user_id,
            "date": self.date,
            "map_visits": self.map_visits,
            "app_behavior": self.app_behavior,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserMemory':
        """从字典创建"""
        return cls(
            user_id=data["user_id"],
            date=data["date"],
            map_visits=data.get("map_visits", []),
            app_behavior=data.get("app_behavior", {}),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )


# ==========================================
# 数据转换层
# ==========================================

class DataConverter:
    """数据转换器"""
    
    @staticmethod
    def scene_node_to_map_node(scene_node: Any) -> MapNode:
        """
        将SceneNode转换为MapNode
        
        Args:
            scene_node: SceneNode实例
            
        Returns:
            MapNode实例
        """
        return MapNode(
            node_id=scene_node.node_id,
            label=scene_node.label,
            node_type=scene_node.node_type,
            position=Position(
                x=scene_node.box[0][0] if scene_node.box else 0,
                y=scene_node.box[0][1] if scene_node.box else 0
            ),
            layer=scene_node.layer,
            image_path=scene_node.image_path,
            bounding_box=BoundingBox(
                x1=scene_node.box[0][0] if scene_node.box else 0,
                y1=scene_node.box[0][1] if scene_node.box else 0,
                x2=scene_node.box[1][0] if scene_node.box else 0,
                y2=scene_node.box[1][1] if scene_node.box else 0
            ) if scene_node.box else None,
            confidence=scene_node.confidence,
            direction=scene_node.direction,
            distance_meters=scene_node.distance_meters,
            notes=scene_node.notes,
            level=scene_node.layer,
            timestamp=scene_node.timestamp
        )
    
    @staticmethod
    def path_memory_to_navigation_path(path_memory: Any) -> NavigationPath:
        """
        将PathMemory转换为NavigationPath
        
        Args:
            path_memory: PathMemory实例
            
        Returns:
            NavigationPath实例
        """
        nodes = [
            DataConverter.scene_node_to_map_node(scene_node)
            for scene_node in path_memory.nodes
        ]
        
        return NavigationPath(
            path_id=path_memory.path_id,
            path_name=path_memory.path_name,
            nodes=nodes,
            created_at=path_memory.created_at,
            updated_at=path_memory.updated_at
        )
    
    @staticmethod
    def validate_json(data: Dict[str, Any], schema_type: str) -> bool:
        """
        验证JSON数据
        
        Args:
            data: JSON数据
            schema_type: 模式类型（"node", "path", "memory"）
            
        Returns:
            是否有效
        """
        try:
            if schema_type == "node":
                MapNode.from_dict(data)
            elif schema_type == "path":
                NavigationPath.from_dict(data)
            elif schema_type == "memory":
                UserMemory.from_dict(data)
            else:
                logger.warning(f"未知模式类型: {schema_type}")
                return False
            
            return True
        except Exception as e:
            logger.error(f"JSON验证失败: {e}")
            return False


# ==========================================
# 导出接口
# ==========================================

# 全局转换器实例
_global_converter: Optional[DataConverter] = None


def get_data_converter() -> DataConverter:
    """获取全局数据转换器实例"""
    global _global_converter
    if _global_converter is None:
        _global_converter = DataConverter()
    return _global_converter


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 70)
    print("📐 统一数据模型测试")
    print("=" * 70)
    
    # 测试MapNode
    print("\n1️⃣ 测试MapNode...")
    node = MapNode(
        node_id="node_001",
        label="305号诊室",
        node_type=NodeType.ROOM.value,
        position=Position(x=100, y=200, z=3),
        layer=LayerType.INDOOR.value,
        confidence=0.9,
        direction="直行10米",
        distance_meters=10.0,
        movement_type=MovementType.WALKING.value,
        level="3楼",
        timestamp=datetime.now().isoformat()
    )
    
    # 转换为字典
    node_dict = node.to_dict()
    print(f"  节点字典: {json.dumps(node_dict, ensure_ascii=False, indent=2)}")
    
    # 从字典重建
    node_restored = MapNode.from_dict(node_dict)
    print(f"  重建成功: {node_restored.label}")
    
    # 测试NavigationPath
    print("\n2️⃣ 测试NavigationPath...")
    path = NavigationPath(
        path_id="path_001",
        path_name="医院导航路径",
        description="从入口到305号诊室",
        nodes=[node],
        total_distance_meters=50.0,
        estimated_duration_minutes=5.0,
        regions=["挂号大厅", "3楼病区"],
        created_at=datetime.now().isoformat()
    )
    
    # 转换为JSON字符串
    path_json = json.dumps(path.to_dict(), ensure_ascii=False, indent=2)
    print(f"  路径JSON: {len(path_json)} 字符")
    
    # 从JSON重建
    path_restored = NavigationPath.from_dict(json.loads(path_json))
    print(f"  重建成功: {path_restored.path_name}")
    
    # 测试数据验证
    print("\n3️⃣ 测试数据验证...")
    converter = get_data_converter()
    is_valid = converter.validate_json(node_dict, "node")
    print(f"  节点验证: {'✅ 有效' if is_valid else '❌ 无效'}")
    
    is_valid = converter.validate_json(path.to_dict(), "path")
    print(f"  路径验证: {'✅ 有效' if is_valid else '❌ 无效'}")
    
    print("\n" + "=" * 70)
    print("✅ 测试完成")

