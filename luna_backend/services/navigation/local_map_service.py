"""
本地地图服务 (LocalMapService) v1.2.0
简单2D小地图：记录用户相对移动和关键点
"""

from typing import Dict, Any, Tuple, List
import math
from dataclasses import dataclass, field


@dataclass
class Landmark:
    """地标点"""
    type: str
    position: Tuple[float, float]  # (x, y) 本地坐标
    label: str
    confidence: float


@dataclass
class LocalMapState:
    """本地地图状态"""
    x: float = 0.0
    y: float = 0.0
    theta: float = 0.0  # 朝向（弧度）
    landmarks: List[Landmark] = field(default_factory=list)


class LocalMapService:
    """
    简单 2D 小地图：记录用户相对移动和关键点
    
    用于室内导航、小范围地图构建
    """
    
    def __init__(self):
        """初始化本地地图服务"""
        self.state = LocalMapState()
    
    def reset(self):
        """重置地图状态"""
        self.state = LocalMapState()
    
    def update_pose(self, dx: float, dy: float, dtheta: float):
        """
        更新位姿（相对移动）
        
        Args:
            dx: X方向移动距离（米）
            dy: Y方向移动距离（米）
            dtheta: 角度变化（弧度）
        """
        # 简单积分位姿（可以后面接上真正的SLAM）
        self.state.theta += dtheta
        
        # 把移动量旋转到全局坐标系
        global_dx = dx * math.cos(self.state.theta) - dy * math.sin(self.state.theta)
        global_dy = dx * math.sin(self.state.theta) + dy * math.cos(self.state.theta)
        
        self.state.x += global_dx
        self.state.y += global_dy
    
    def add_landmark(self, type_: str, rel_pos: Tuple[float, float],
                     label: str, confidence: float = 1.0):
        """
        添加地标点
        
        Args:
            type_: 地标类型（如"door", "elevator", "stairs"）
            rel_pos: 相对位置 (x, y)
            label: 地标标签（如"305", "电梯1"）
            confidence: 置信度
        """
        # 把相对坐标转成全局
        rx, ry = rel_pos
        gx = self.state.x + rx
        gy = self.state.y + ry
        
        self.state.landmarks.append(Landmark(type_, (gx, gy), label, confidence))
    
    def get_landmarks(self) -> List[Landmark]:
        """
        获取所有地标点
        
        Returns:
            地标点列表
        """
        return self.state.landmarks.copy()
    
    def get_pose(self) -> Dict[str, float]:
        """
        获取当前位姿
        
        Returns:
            位姿字典 {"x": x, "y": y, "theta": theta}
        """
        return {
            "x": self.state.x,
            "y": self.state.y,
            "theta": self.state.theta
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """
        转换为字典格式
        
        Returns:
            地图状态字典
        """
        return {
            "pose": {
                "x": self.state.x,
                "y": self.state.y,
                "theta": self.state.theta
            },
            "landmarks": [
                {
                    "type": lm.type,
                    "x": lm.position[0],
                    "y": lm.position[1],
                    "label": lm.label,
                    "confidence": lm.confidence
                }
                for lm in self.state.landmarks
            ]
        }



