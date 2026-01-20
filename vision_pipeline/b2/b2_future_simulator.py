"""
B2 Future Simulator - 未来世界预演器

职责：
- 对 TaskCorridor 内的未来 5-10 秒做世界投影
- 输出 impact_events（不做语义）
- 只做几何 + 时间投影，不理解世界
"""

from typing import Dict, Any, List, Tuple, Optional
from dataclasses import dataclass, field
from .b2_types import TaskCorridor, ImpactEvent


@dataclass
class FutureWorld:
    """未来世界投影结果"""
    horizon_sec: float
    projected_ego_poses: List[Dict[str, Any]] = field(default_factory=list)
    projected_object_poses: List[Dict[str, Any]] = field(default_factory=list)
    potential_intersections: List[Dict[str, Any]] = field(default_factory=list)
    
    def add_impact(self, event_id: str, time_sec: float, distance: Optional[float] = None):
        """添加潜在冲突"""
        self.potential_intersections.append({
            "event_id": event_id,
            "time_sec": time_sec,
            "distance": distance,
        })


class FutureSimulator:
    """
    B2 未来预演器
    
    核心职责：
    - 将「我未来 5-10 秒的路径」投影成 corridor
    - 将「周边对象/区域」投影到未来时间轴
    - 判断：是否相交、何时相交、影响范围多大
    
    注意：这一步不需要语义模型
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化未来预演器
        
        Args:
            config: 配置字典，包含：
                - time_step: 时间步长（默认 0.5 秒）
                - ego_velocity: 默认自速度（默认 1.0 m/s）
        """
        self.config = config or {}
        self.time_step = self.config.get("time_step", 0.5)
        self.ego_velocity = self.config.get("ego_velocity", 1.0)
    
    def simulate_future(
        self,
        world_snapshot: Dict[str, Any],
        corridor: TaskCorridor,
        horizon_sec: float,
    ) -> FutureWorld:
        """
        模拟未来世界
        
        Args:
            world_snapshot: 世界快照，包含：
                - ego_pose: 自位姿
                - objects: 对象列表
            corridor: 任务走廊
            horizon_sec: 预演时间窗口（秒）
        
        Returns:
            FutureWorld: 未来世界投影结果
        """
        future = FutureWorld(horizon_sec=horizon_sec)
        
        ego_pose = world_snapshot.get("ego_pose", {})
        objects = world_snapshot.get("objects", [])
        
        # 预测自位姿（简化：直线运动）
        for t in range(1, int(horizon_sec / self.time_step) + 1):
            t_sec = t * self.time_step
            ego_future = self._predict_ego(ego_pose, t_sec)
            future.projected_ego_poses.append(ego_future)
        
        # 预测对象位姿并检查冲突
        for obj in objects:
            obj_id = obj.get("id") or obj.get("event_id", "unknown")
            obj_velocity = obj.get("velocity") or 0.0
            
            for t in range(1, int(horizon_sec / self.time_step) + 1):
                t_sec = t * self.time_step
                obj_future = self._predict_object(obj, t_sec)
                future.projected_object_poses.append(obj_future)
                
                # 检查是否与走廊相交
                if self._intersects(ego_future, obj_future, corridor):
                    distance = self._compute_distance(ego_future, obj_future)
                    future.add_impact(obj_id, t_sec, distance)
        
        return future
    
    def _predict_ego(self, ego_pose: Dict[str, Any], t_sec: float) -> Dict[str, Any]:
        """
        预测自位姿（简化：直线运动）
        
        Args:
            ego_pose: 当前自位姿
            t_sec: 未来时间（秒）
        
        Returns:
            Dict[str, Any]: 未来自位姿
        """
        heading = ego_pose.get("heading", 0)
        position = ego_pose.get("position", (0.0, 0.0))
        velocity = ego_pose.get("velocity", self.ego_velocity)
        
        # 简化：直线运动
        import math
        dx = velocity * t_sec * math.cos(math.radians(heading))
        dy = velocity * t_sec * math.sin(math.radians(heading))
        
        future_position = (
            position[0] + dx if isinstance(position, (list, tuple)) and len(position) >= 2 else 0.0,
            position[1] + dy if isinstance(position, (list, tuple)) and len(position) >= 2 else 0.0,
        )
        
        return {
            "position": future_position,
            "heading": heading,
            "t_sec": t_sec,
        }
    
    def _predict_object(self, obj: Dict[str, Any], t_sec: float) -> Dict[str, Any]:
        """
        预测对象位姿（简化：直线运动）
        
        Args:
            obj: 对象信息
            t_sec: 未来时间（秒）
        
        Returns:
            Dict[str, Any]: 未来对象位姿
        """
        position = obj.get("position", (0.0, 0.0))
        velocity = obj.get("velocity", 0.0)
        heading = obj.get("heading", 0)
        
        # 简化：直线运动
        import math
        dx = velocity * t_sec * math.cos(math.radians(heading))
        dy = velocity * t_sec * math.sin(math.radians(heading))
        
        future_position = (
            position[0] + dx if isinstance(position, (list, tuple)) and len(position) >= 2 else 0.0,
            position[1] + dy if isinstance(position, (list, tuple)) and len(position) >= 2 else 0.0,
        )
        
        return {
            "position": future_position,
            "heading": heading,
            "t_sec": t_sec,
            "object_id": obj.get("id") or obj.get("event_id", "unknown"),
        }
    
    def _intersects(
        self,
        ego_future: Dict[str, Any],
        obj_future: Dict[str, Any],
        corridor: TaskCorridor,
    ) -> bool:
        """
        检查是否与走廊相交（简化：距离判断）
        
        Args:
            ego_future: 未来自位姿
            obj_future: 未来对象位姿
            corridor: 任务走廊
        
        Returns:
            bool: 是否相交
        """
        # 简化：如果对象在走廊宽度内，认为相交
        ego_pos = ego_future.get("position", (0.0, 0.0))
        obj_pos = obj_future.get("position", (0.0, 0.0))
        
        # 计算距离
        import math
        dx = obj_pos[0] - ego_pos[0] if isinstance(obj_pos, (list, tuple)) and len(obj_pos) >= 2 else 0.0
        dy = obj_pos[1] - ego_pos[1] if isinstance(obj_pos, (list, tuple)) and len(obj_pos) >= 2 else 0.0
        distance = math.sqrt(dx * dx + dy * dy)
        
        # 简化：如果距离 < 5 米，认为相交
        return distance < 5.0
    
    def _compute_distance(
        self,
        ego_future: Dict[str, Any],
        obj_future: Dict[str, Any],
    ) -> float:
        """
        计算距离
        
        Args:
            ego_future: 未来自位姿
            obj_future: 未来对象位姿
        
        Returns:
            float: 距离（米）
        """
        ego_pos = ego_future.get("position", (0.0, 0.0))
        obj_pos = obj_future.get("position", (0.0, 0.0))
        
        import math
        dx = obj_pos[0] - ego_pos[0] if isinstance(obj_pos, (list, tuple)) and len(obj_pos) >= 2 else 0.0
        dy = obj_pos[1] - ego_pos[1] if isinstance(obj_pos, (list, tuple)) and len(obj_pos) >= 2 else 0.0
        return math.sqrt(dx * dx + dy * dy)

