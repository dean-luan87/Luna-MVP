#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 自动生成小范围地图模块
构建基于视觉锚点的局部空间地图，并进行关键点标注
"""

import logging
import json
import cv2
import numpy as np
import math
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import time
from collections import defaultdict

logger = logging.getLogger(__name__)

class LandmarkType(Enum):
    """地标类型"""
    ENTRANCE = "entrance"           # 出入口
    TOILET = "toilet"               # 洗手间
    ELEVATOR = "elevator"           # 电梯
    CHAIR = "chair"                 # 椅子
    HAZARD_EDGE = "hazard_edge"    # 危险边缘
    BUS_STOP = "bus_stop"          # 公交站
    EXIT = "exit"                   # 出口
    INFO_BOARD = "info_board"      # 导览牌
    STAIRS = "stairs"              # 楼梯
    ESCALATOR = "escalator"        # 扶梯

class VisualAnchor:
    """视觉锚点"""
    def __init__(self, x: float, y: float, timestamp: float, confidence: float):
        self.x = x
        self.y = y
        self.timestamp = timestamp
        self.confidence = confidence
        self.features = {}

@dataclass
class MapLandmark:
    """地图地标"""
    type: LandmarkType              # 地标类型
    position: Tuple[float, float]   # 位置 (x, y)
    label: str                      # 标签
    confidence: float               # 置信度
    timestamp: float                # 检测时间
    description: str                # 描述
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "type": self.type.value,
            "position": list(self.position),
            "label": self.label,
            "confidence": self.confidence,
            "timestamp": self.timestamp,
            "description": self.description
        }

@dataclass
class LocalMap:
    """局部地图"""
    origin: Tuple[float, float]     # 原点位置
    landmarks: List[MapLandmark]    # 地标列表
    paths: List[List[Tuple[float, float]]]  # 路径列表
    metadata: Dict[str, Any]        # 元数据
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "origin": list(self.origin),
            "landmarks": [lm.to_dict() for lm in self.landmarks],
            "paths": [list(path) for path in self.paths],
            "metadata": self.metadata
        }
    
    def to_json(self) -> str:
        """转换为JSON字符串"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

class LocalMapGenerator:
    """局部地图生成器"""
    
    def __init__(self, map_size: Tuple[float, float] = (100.0, 100.0)):
        """
        初始化局部地图生成器
        
        Args:
            map_size: 地图尺寸（米）
        """
        self.map_size = map_size
        self.current_position = (0.0, 0.0)  # 当前位置
        self.current_angle = 0.0            # 当前角度
        self.start_time = time.time()       # 开始时间
        
        # 视觉锚点列表
        self.visual_anchors: List[VisualAnchor] = []
        
        # 地图数据
        self.landmarks: List[MapLandmark] = []
        self.paths: List[List[Tuple[float, float]]] = []
        self.path_current: List[Tuple[float, float]] = []
        
        # 元数据
        self.metadata = {
            "created_at": time.time(),
            "version": "1.0",
            "map_size": map_size,
            "coordinate_system": "relative"
        }
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("🗺️ 局部地图生成器初始化完成")
    
    def update_position(self, dx: float, dy: float, angle_delta: float = 0.0):
        """
        更新位置
        
        Args:
            dx: x方向移动距离（米）
            dy: y方向移动距离（米）
            angle_delta: 角度变化（弧度）
        """
        # 根据当前角度旋转位移
        cos_a = math.cos(self.current_angle)
        sin_a = math.sin(self.current_angle)
        
        dx_rotated = dx * cos_a - dy * sin_a
        dy_rotated = dx * sin_a + dy * cos_a
        
        # 更新位置
        self.current_position = (
            self.current_position[0] + dx_rotated,
            self.current_position[1] + dy_rotated
        )
        
        # 更新角度
        self.current_angle += angle_delta
        
        # 记录路径点
        self.path_current.append(self.current_position)
        
        # 添加视觉锚点
        anchor = VisualAnchor(
            x=self.current_position[0],
            y=self.current_position[1],
            timestamp=time.time() - self.start_time,
            confidence=1.0
        )
        self.visual_anchors.append(anchor)
        
        self.logger.debug(f"位置更新: ({self.current_position[0]:.2f}, {self.current_position[1]:.2f})")
    
    def add_landmark_from_vision(self, image: np.ndarray, 
                                 landmark_type: LandmarkType,
                                 relative_position: Tuple[float, float],
                                 label: str = "") -> Optional[MapLandmark]:
        """
        从视觉检测添加地标
        
        Args:
            image: 当前图像
            landmark_type: 地标类型
            relative_position: 相对位置（前方米数，左侧米数）
            label: 标签文字
            
        Returns:
            MapLandmark: 创建的地标
        """
        # 根据当前角度和位置计算地标的绝对坐标
        distance, left_offset = relative_position
        
        # 计算地标在全局坐标系中的位置
        landmark_x = self.current_position[0] + distance * math.cos(self.current_angle) + left_offset * math.cos(self.current_angle - math.pi/2)
        landmark_y = self.current_position[1] + distance * math.sin(self.current_angle) + left_offset * math.sin(self.current_angle - math.pi/2)
        
        # 创建地标
        landmark = MapLandmark(
            type=landmark_type,
            position=(landmark_x, landmark_y),
            label=label,
            confidence=0.7,  # 视觉检测的置信度
            timestamp=time.time() - self.start_time,
            description=f"{landmark_type.value} at {distance:.1f}m ahead, {left_offset:.1f}m left"
        )
        
        self.landmarks.append(landmark)
        self.logger.info(f"✅ 添加地标: {landmark_type.value} at ({landmark_x:.2f}, {landmark_y:.2f})")
        
        return landmark
    
    def add_landmark_direct(self, landmark_type: LandmarkType,
                           position: Tuple[float, float],
                           label: str = "",
                           confidence: float = 1.0) -> MapLandmark:
        """
        直接添加地标（已知绝对位置）
        
        Args:
            landmark_type: 地标类型
            position: 绝对位置 (x, y)
            label: 标签
            confidence: 置信度
            
        Returns:
            MapLandmark: 创建的地标
        """
        landmark = MapLandmark(
            type=landmark_type,
            position=position,
            label=label,
            confidence=confidence,
            timestamp=time.time() - self.start_time,
            description=f"{landmark_type.value} at position ({position[0]:.2f}, {position[1]:.2f})"
        )
        
        self.landmarks.append(landmark)
        self.logger.info(f"✅ 添加地标: {landmark_type.value} at {position}")
        
        return landmark
    
    def finish_path(self):
        """完成当前路径"""
        if len(self.path_current) > 1:
            self.paths.append(self.path_current.copy())
            self.path_current = []
            self.logger.info("📍 路径已记录")
    
    def get_map(self) -> LocalMap:
        """
        获取生成的地图
        
        Returns:
            LocalMap: 局部地图对象
        """
        # 完成当前路径
        if len(self.path_current) > 1:
            self.finish_path()
        
        map_obj = LocalMap(
            origin=(0.0, 0.0),
            landmarks=self.landmarks,
            paths=self.paths,
            metadata=self.metadata
        )
        
        return map_obj
    
    def save_map(self, filepath: str):
        """
        保存地图到文件
        
        Args:
            filepath: 文件路径
        """
        map_obj = self.get_map()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(map_obj.to_json())
        
        self.logger.info(f"💾 地图已保存: {filepath}")
    
    def load_map(self, filepath: str):
        """
        从文件加载地图
        
        Args:
            filepath: 文件路径
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 加载地标
        self.landmarks = []
        for lm_data in data.get('landmarks', []):
            landmark = MapLandmark(
                type=LandmarkType(lm_data['type']),
                position=tuple(lm_data['position']),
                label=lm_data['label'],
                confidence=lm_data['confidence'],
                timestamp=lm_data['timestamp'],
                description=lm_data.get('description', '')
            )
            self.landmarks.append(landmark)
        
        # 加载路径
        self.paths = [tuple(path) for path in data.get('paths', [])]
        
        # 加载元数据
        self.metadata = data.get('metadata', {})
        
        self.logger.info(f"📂 地图已加载: {filepath}")
    
    def visualize_map(self, output_path: str, scale: int = 10):
        """
        生成地图可视化图像
        
        Args:
            output_path: 输出路径
            scale: 缩放比例（像素/米）
        """
        width = int(self.map_size[0] * scale)
        height = int(self.map_size[1] * scale)
        
        # 创建图像
        img = np.ones((height, width, 3), dtype=np.uint8) * 255
        
        # 绘制路径
        for path in self.paths:
            for i in range(len(path) - 1):
                p1 = self._world_to_pixel(path[i], width, height)
                p2 = self._world_to_pixel(path[i+1], width, height)
                cv2.line(img, p1, p2, (100, 100, 100), 2)
        
        # 当前路径
        if len(self.path_current) > 1:
            for i in range(len(self.path_current) - 1):
                p1 = self._world_to_pixel(self.path_current[i], width, height)
                p2 = self._world_to_pixel(self.path_current[i+1], width, height)
                cv2.line(img, p1, p2, (50, 50, 255), 2)
        
        # 地标颜色映射
        landmark_colors = {
            LandmarkType.ENTRANCE: (0, 255, 0),      # 绿色
            LandmarkType.EXIT: (0, 255, 0),          # 绿色
            LandmarkType.TOILET: (255, 165, 0),      # 橙色
            LandmarkType.ELEVATOR: (0, 0, 255),      # 蓝色
            LandmarkType.CHAIR: (128, 0, 128),       # 紫色
            LandmarkType.HAZARD_EDGE: (0, 0, 255),  # 红色
            LandmarkType.BUS_STOP: (255, 0, 255),    # 品红
            LandmarkType.INFO_BOARD: (255, 192, 203), # 粉红
            LandmarkType.STAIRS: (192, 192, 192),    # 灰色
            LandmarkType.ESCALATOR: (192, 192, 192), # 灰色
        }
        
        # 绘制地标
        for landmark in self.landmarks:
            pos = self._world_to_pixel(landmark.position, width, height)
            color = landmark_colors.get(landmark.type, (128, 128, 128))
            
            # 绘制地标点
            cv2.circle(img, pos, 8, color, -1)
            cv2.circle(img, pos, 10, (0, 0, 0), 2)
            
            # 绘制标签
            label_text = landmark.label if landmark.label else landmark.type.value
            cv2.putText(img, label_text, (pos[0] + 15, pos[1]), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
        
        # 绘制原点
        origin_pixel = self._world_to_pixel((0, 0), width, height)
        cv2.circle(img, origin_pixel, 6, (255, 0, 0), -1)
        cv2.putText(img, "START", (origin_pixel[0] + 15, origin_pixel[1]), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        
        # 绘制当前位置
        if len(self.path_current) > 0:
            current_pos = self._world_to_pixel(self.path_current[-1], width, height)
            cv2.circle(img, current_pos, 6, (0, 255, 0), -1)
            cv2.putText(img, "CURRENT", (current_pos[0] + 15, current_pos[1] - 15), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # 保存图像
        cv2.imwrite(output_path, img)
        self.logger.info(f"🖼️ 地图可视化已保存: {output_path}")
    
    def _world_to_pixel(self, world_pos: Tuple[float, float], width: int, height: int) -> Tuple[int, int]:
        """世界坐标转像素坐标"""
        # 地图中心为原点
        pixel_x = int(world_pos[0] * 10 + width / 2)
        pixel_y = int(-world_pos[1] * 10 + height / 2)  # Y轴翻转
        return (pixel_x, pixel_y)
    
    def get_landmarks_nearby(self, position: Tuple[float, float], radius: float = 5.0) -> List[MapLandmark]:
        """
        获取附近的地标
        
        Args:
            position: 位置
            radius: 搜索半径（米）
            
        Returns:
            List[MapLandmark]: 附近的地标
        """
        nearby = []
        for landmark in self.landmarks:
            dx = landmark.position[0] - position[0]
            dy = landmark.position[1] - position[1]
            distance = math.sqrt(dx * dx + dy * dy)
            
            if distance <= radius:
                nearby.append(landmark)
        
        return nearby


# 全局地图生成器实例
global_map_generator = LocalMapGenerator()

if __name__ == "__main__":
    # 测试局部地图生成
    import logging
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 60)
    print("🗺️ 局部地图生成测试")
    print("=" * 60)
    
    # 创建地图生成器
    generator = LocalMapGenerator(map_size=(50.0, 50.0))
    
    # 模拟移动和检测
    
    # 1. 向前移动5米
    print("\n📍 向前移动5米")
    generator.update_position(5.0, 0.0)
    
    # 2. 检测到入口
    print("\n✅ 检测到入口")
    generator.add_landmark_from_vision(
        image=None,
        landmark_type=LandmarkType.ENTRANCE,
        relative_position=(3.0, 0.0),
        label="商场入口"
    )
    
    # 3. 向右转90度，移动5米
    print("\n🔄 右转90度，移动5米")
    generator.update_position(0.0, 0.0, angle_delta=math.pi / 2)
    generator.update_position(5.0, 0.0)
    
    # 4. 检测到洗手间
    print("\n🚻 检测到洗手间")
    generator.add_landmark_from_vision(
        image=None,
        landmark_type=LandmarkType.TOILET,
        relative_position=(2.0, -3.0),
        label="洗手间A"
    )
    
    # 5. 检测到电梯
    print("\n🚪 检测到电梯")
    generator.add_landmark_from_vision(
        image=None,
        landmark_type=LandmarkType.ELEVATOR,
        relative_position=(5.0, 2.0),
        label="电梯1号"
    )
    
    # 6. 再向前移动10米
    print("\n📍 向前移动10米")
    generator.update_position(10.0, 0.0)
    
    # 7. 检测到椅子
    print("\n🪑 检测到椅子")
    generator.add_landmark_from_vision(
        image=None,
        landmark_type=LandmarkType.CHAIR,
        relative_position=(1.0, 0.0),
        label="休息区"
    )
    
    # 8. 检测到危险边缘
    print("\n⚠️ 检测到危险边缘")
    generator.add_landmark_direct(
        landmark_type=LandmarkType.HAZARD_EDGE,
        position=(generator.current_position[0] + 2.0, generator.current_position[1]),
        label="台阶边缘",
        confidence=0.8
    )
    
    # 完成路径
    generator.finish_path()
    
    # 获取地图
    print("\n📊 地图统计:")
    map_obj = generator.get_map()
    print(f"  地标数量: {len(map_obj.landmarks)}")
    print(f"  路径数量: {len(map_obj.paths)}")
    
    # 打印地标
    print("\n📍 地标列表:")
    for i, landmark in enumerate(map_obj.landmarks, 1):
        print(f"  {i}. {landmark.type.value}: {landmark.label} at {landmark.position}")
    
    # 查找附近地标
    print("\n🔍 当前位置附近的地标:")
    nearby = generator.get_landmarks_nearby(generator.current_position, radius=10.0)
    for landmark in nearby:
        dx = landmark.position[0] - generator.current_position[0]
        dy = landmark.position[1] - generator.current_position[1]
        distance = math.sqrt(dx * dx + dy * dy)
        print(f"  - {landmark.label}: {distance:.2f}m away")
    
    # 保存地图
    generator.save_map("data/local_map.json")
    
    # 生成可视化
    generator.visualize_map("data/local_map_visualization.png")
    
    print("\n" + "=" * 60)
    print("✅ 测试完成！")
    print("=" * 60)
