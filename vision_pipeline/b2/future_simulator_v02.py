"""
Future Simulator v0.2 - Part 1: 多未来分支预演

B2 v0.2 Part 1: 多未来分支预演（Future Branch Simulation）

核心问题：
v0.1 的 B2 只是在看「当前世界是否稳定」，
但人类真正的提前反应来自于：
"如果我继续这样走，5 秒后会发生什么？"

模块职责（非常重要）：
- 不做理解
- 不做判断
- 只做几何 / 时序层面的预演

预演方式（工程可落地）：
- 时间离散：t = 1s, 3s, 5s, 8s
- 位置预测：线性外推（先别复杂）
- 路径：导航 polyline + buffer
- 判断：AABB / 距离阈值
"""

import math
from typing import List, Optional, Dict, Any
from .future_simulator_input import FutureSimulatorInput, DynamicObject, StaticRegion
from .future_simulation_result import FutureSimulationResult, CollisionEvent, RegionEnterEvent


class FutureSimulator:
    """
    B2 未来预演器 v0.2 Part 1
    
    核心职责：
    - 将「我未来 5-10 秒的路径」投影成 corridor
    - 将「周边对象/区域」投影到未来时间轴
    - 判断：是否相交、何时相交、影响范围多大
    
    注意：这一步不需要语义模型
    """
    
    def __init__(
        self,
        horizon_sec: float = 8.0,
        time_steps: List[float] = None,
        path_buffer_m: float = 1.2,
        collision_radius_m: float = 2.0,
    ):
        """
        初始化未来预演器
        
        Args:
            horizon_sec: 预演时间窗口（秒），默认 8 秒
            time_steps: 时间步长列表（秒），默认 [1.0, 3.0, 5.0, 8.0]
            path_buffer_m: 路径缓冲区宽度（米）
            collision_radius_m: 碰撞半径（米）
        """
        self.horizon_sec = horizon_sec
        self.time_steps = time_steps or [1.0, 3.0, 5.0, 8.0]
        self.path_buffer_m = path_buffer_m
        self.collision_radius_m = collision_radius_m
    
    def run(self, input_data: FutureSimulatorInput) -> FutureSimulationResult:
        """
        运行未来预演
        
        B2 v0.2 Part 1: 多未来分支预演
        
        C1: FutureSimulator.run()
        要求：
        - 单次调用 ≤ 5ms（CPU）
        - 不缓存（缓存放在 B2 上层）
        
        Args:
            input_data: FutureSimulatorInput
        
        Returns:
            FutureSimulationResult: 预演结果（不判断，只标记）
        """
        result = FutureSimulationResult(
            horizon_sec=self.horizon_sec,
            timestamp=input_data.timestamp,
        )
        
        # B1: Ego 未来轨迹生成
        ego_future_positions = self._predict_ego_positions(
            input_data.ego_path,
            input_data.ego_velocity,
            input_data.ego_position,
            input_data.ego_heading,
        )
        
        # B2: 动态物体未来位置预测
        object_future_positions = self._predict_dynamic_objects(
            input_data.dynamic_objects,
        )
        
        # 对每个时间步进行预演
        for t_sec in self.time_steps:
            if t_sec > self.horizon_sec:
                break
            
            # 获取 ego 未来位置
            ego_future_pos = ego_future_positions.get(t_sec)
            if not ego_future_pos:
                continue
            
            # B5: 检查动态对象碰撞（弱几何）
            # 构建 ego corridor（用于碰撞检测）
            ego_corridor = self._build_ego_corridor(input_data)
            collisions = self._check_collisions(
                ego_corridor=ego_corridor,
                dynamic_objects=input_data.dynamic_objects,
                t_sec=t_sec,
            )
            result.collisions.extend(collisions)
            
            # B3: 检查路径重叠
            if not result.path_overlap:
                result.path_overlap = self._check_path_overlap(
                    ego_future_pos=ego_future_pos,
                    ego_path=input_data.ego_path,
                    object_future_positions=object_future_positions,
                    t_sec=t_sec,
                )
            
            # B4: 检查区域进入
            ego_corridor = self._build_ego_corridor(input_data)
            region_events = self._check_region_enter(
                ego_corridor=ego_corridor,
                static_regions=input_data.static_regions,
                t_sec=t_sec,
            )
            result.region_enter.extend(region_events)
        
        return result
    
    def _predict_ego_positions(
        self,
        ego_path: Optional[List[List[float]]],
        ego_velocity: List[float],
        ego_position: List[float],
        ego_heading: float,
    ) -> Dict[float, List[float]]:
        """
        预测 ego 未来位置
        
        Args:
            ego_path: 导航路径（可选）
            ego_velocity: ego 速度 [vx, vy]
            ego_position: ego 当前位置 [x, y]
            ego_heading: ego 朝向（度）
        
        Returns:
            Dict[float, List[float]]: {t_sec: [x, y]} 未来位置字典
        """
        positions = {}
        
        for t_sec in self.time_steps:
            if t_sec > self.horizon_sec:
                break
            
            if ego_path and len(ego_path) > 0:
                # 有路径：沿路径移动
                # 简化：按速度和时间计算路径上的位置
                speed = math.sqrt(ego_velocity[0]**2 + ego_velocity[1]**2) or 1.0
                distance = speed * t_sec
                
                # 在路径上找到对应位置
                current_dist = 0.0
                future_pos = ego_position[:] if ego_position else [0.0, 0.0]
                
                for i in range(len(ego_path) - 1):
                    p1 = ego_path[i]
                    p2 = ego_path[i + 1]
                    seg_len = math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
                    
                    if current_dist + seg_len >= distance:
                        # 在这个线段上
                        ratio = (distance - current_dist) / seg_len if seg_len > 0 else 0
                        future_pos = [
                            p1[0] + (p2[0] - p1[0]) * ratio,
                            p1[1] + (p2[1] - p1[1]) * ratio,
                        ]
                        break
                    current_dist += seg_len
                
                positions[t_sec] = future_pos
            else:
                # 无路径：直线外推
                speed = math.sqrt(ego_velocity[0]**2 + ego_velocity[1]**2) or 1.0
                heading_rad = math.radians(ego_heading)
                dx = speed * math.cos(heading_rad) * t_sec
                dy = speed * math.sin(heading_rad) * t_sec
                
                start_pos = ego_position[:] if ego_position else [0.0, 0.0]
                positions[t_sec] = [start_pos[0] + dx, start_pos[1] + dy]
        
        return positions
    
    def _predict_dynamic_objects(
        self,
        dynamic_objects: List[DynamicObject],
    ) -> List[Dict[str, Any]]:
        """
        预测动态对象未来位置
        
        Args:
            dynamic_objects: 动态对象列表
        
        Returns:
            List[Dict[str, Any]]: 每个对象包含 {obj_id, positions: {t_sec: [x, y]}}
        """
        object_futures = []
        
        for obj in dynamic_objects:
            positions = {}
            
            # 计算对象中心
            if obj.bbox and len(obj.bbox) >= 4:
                center_x = (obj.bbox[0] + obj.bbox[2]) / 2.0
                center_y = (obj.bbox[1] + obj.bbox[3]) / 2.0
            else:
                center_x, center_y = 0.0, 0.0
            
            # 预测每个时间步的位置
            for t_sec in self.time_steps:
                if t_sec > self.horizon_sec:
                    break
                
                vel = obj.velocity if obj.velocity and len(obj.velocity) >= 2 else [0.0, 0.0]
                future_x = center_x + vel[0] * t_sec
                future_y = center_y + vel[1] * t_sec
                positions[t_sec] = [future_x, future_y]
            
            object_futures.append({
                "obj_id": obj.obj_id,
                "positions": positions,
            })
        
        return object_futures
    
    def _build_ego_corridor(self, input_data: FutureSimulatorInput) -> Dict[str, Any]:
        """
        构建 ego 未来路径（corridor）
        
        Args:
            input_data: FutureSimulatorInput
        
        Returns:
            Dict: corridor 信息（polygon, points, buffer）
        """
        # 如果有导航路径，使用导航路径
        if input_data.ego_path and len(input_data.ego_path) > 0:
            # 使用导航路径构建 corridor
            return {
                "type": "route",
                "points": input_data.ego_path,
                "buffer_m": self.path_buffer_m,
            }
        
        # 无导航：ego heading + velocity 构造直走 corridor
        heading_rad = math.radians(input_data.ego_heading)
        speed = math.sqrt(input_data.ego_velocity[0]**2 + input_data.ego_velocity[1]**2) or 1.0
        
        # 计算未来路径长度
        path_length = speed * self.horizon_sec
        
        # 构建简单的矩形 corridor（从当前位置向前延伸）
        half_width = self.path_buffer_m / 2.0
        start_x, start_y = input_data.ego_position[0], input_data.ego_position[1]
        
        # 计算方向向量
        dx = math.cos(heading_rad)
        dy = math.sin(heading_rad)
        
        # 计算垂直向量（用于宽度）
        perp_dx = -dy
        perp_dy = dx
        
        # 构建矩形 polygon（4 个点）
        polygon = [
            [start_x + perp_dx * half_width, start_y + perp_dy * half_width],
            [start_x + dx * path_length + perp_dx * half_width, start_y + dy * path_length + perp_dy * half_width],
            [start_x + dx * path_length - perp_dx * half_width, start_y + dy * path_length - perp_dy * half_width],
            [start_x - perp_dx * half_width, start_y - perp_dy * half_width],
        ]
        
        return {
            "type": "heading",
            "polygon": polygon,
            "points": [
                [start_x, start_y],
                [start_x + dx * path_length, start_y + dy * path_length],
            ],
            "buffer_m": self.path_buffer_m,
        }
    
    def _check_collisions(
        self,
        ego_corridor: Dict[str, Any],
        dynamic_objects: List[DynamicObject],
        t_sec: float,
    ) -> List[CollisionEvent]:
        """
        检查动态对象碰撞
        
        Args:
            ego_corridor: ego 路径 corridor
            dynamic_objects: 动态对象列表
            t_sec: 未来时间（秒）
        
        Returns:
            List[CollisionEvent]: 碰撞事件列表
        """
        collisions = []
        
        for obj in dynamic_objects:
            if obj.confidence < 0.3:
                continue
            
            # 外推对象位置
            future_x = obj.bbox[0] + obj.velocity[0] * t_sec
            future_y = obj.bbox[1] + obj.velocity[1] * t_sec
            
            # 计算对象中心
            obj_center_x = (obj.bbox[0] + obj.bbox[2]) / 2.0
            obj_center_y = (obj.bbox[1] + obj.bbox[3]) / 2.0
            future_center_x = obj_center_x + obj.velocity[0] * t_sec
            future_center_y = obj_center_y + obj.velocity[1] * t_sec
            
            # 检查是否在 corridor 内（简化：点-in-polygon）
            if self._point_in_corridor(future_center_x, future_center_y, ego_corridor):
                # 计算距离和重叠比例
                distance = self._distance_to_corridor(future_center_x, future_center_y, ego_corridor)
                overlap_ratio = min(1.0, max(0.0, 1.0 - distance / self.path_buffer_m))
                
                collisions.append(CollisionEvent(
                    obj_id=obj.obj_id,
                    t_sec=t_sec,
                    overlap_ratio=overlap_ratio,
                    distance=distance,
                    meta={
                        "confidence": obj.confidence,
                    }
                ))
        
        return collisions
    
    def _check_path_overlap(
        self,
        ego_future_pos: List[float],
        ego_path: Optional[List[List[float]]],
        object_future_positions: List[Dict[str, Any]],
        t_sec: float,
    ) -> bool:
        """
        B3: 路径重叠判断（核心）
        
        判断条件：
        - 动态物体未来位置与 ego_path buffer 距离 < threshold
        
        输出：
        path_overlap = True / False
        
        Args:
            ego_future_pos: ego 未来位置
            ego_path: ego 路径（可选）
            object_future_positions: 动态对象未来位置
            t_sec: 未来时间（秒）
        
        Returns:
            bool: 路径是否会被占用
        """
        if not ego_path or len(ego_path) < 2:
            # 无路径，使用碰撞判断
            return False
        
        # 检查每个动态对象是否接近路径
        for obj_data in object_future_positions:
            obj_pos = obj_data["positions"].get(t_sec)
            if not obj_pos:
                continue
            
            # 检查对象是否在路径附近
            if self._is_close_to_path(obj_pos, ego_path):
                return True
        
        return False
    
    def _check_region_enter(
        self,
        ego_corridor: Dict[str, Any],
        static_regions: List[StaticRegion],
        t_sec: float,
    ) -> List[RegionEnterEvent]:
        """
        检查是否会进入风险区域
        
        Args:
            ego_corridor: ego 路径 corridor
            static_regions: 静态区域列表
            t_sec: 未来时间（秒）
        
        Returns:
            List[RegionEnterEvent]: 区域进入事件列表
        """
        events = []
        
        # 计算 ego 在 t_sec 时的位置
        # 简化：使用 corridor 的终点
        if ego_corridor.get("points") and len(ego_corridor["points"]) > 0:
            ego_future_pos = ego_corridor["points"][-1] if len(ego_corridor["points"]) > 1 else ego_corridor["points"][0]
        else:
            return events
        
        # 检查是否进入任何静态区域
        for region in static_regions:
            if self._point_in_polygon(ego_future_pos[0], ego_future_pos[1], region.polygon):
                events.append(RegionEnterEvent(
                    region_id=region.region_id,
                    region_type=region.region_type,
                    t_sec=t_sec,
                    meta={}
                ))
        
        return events
    
    def _point_in_corridor(self, x: float, y: float, corridor: Dict[str, Any]) -> bool:
        """检查点是否在 corridor 内"""
        if corridor.get("polygon"):
            return self._point_in_polygon(x, y, corridor["polygon"])
        elif corridor.get("points"):
            # 简化：检查点是否在路径附近
            return self._point_near_path(x, y, corridor["points"], corridor.get("buffer_m", 1.2))
        return False
    
    def _is_close_to_path(self, point: List[float], path: List[List[float]]) -> bool:
        """
        几何判断工具：检查点是否在路径附近
        
        def is_close_to_path(point, path):
            for seg in path.segments:
                if point_to_segment_distance(point, seg) < PATH_BUFFER:
                    return True
            return False
        """
        if len(path) < 2:
            return False
        
        # 计算点到路径的最短距离
        min_dist = float('inf')
        for i in range(len(path) - 1):
            p1 = path[i]
            p2 = path[i + 1]
            dist = self._point_to_segment_distance(point[0], point[1], p1[0], p1[1], p2[0], p2[1])
            min_dist = min(min_dist, dist)
        
        return min_dist <= self.path_buffer_m
    
    def _point_near_path(self, x: float, y: float, path_points: List[List[float]], buffer_m: float) -> bool:
        """检查点是否在路径附近（简化，保留兼容）"""
        return self._is_close_to_path([x, y], path_points)
    
    def _point_to_segment_distance(self, px: float, py: float, x1: float, y1: float, x2: float, y2: float) -> float:
        """计算点到线段的距离"""
        dx = x2 - x1
        dy = y2 - y1
        if dx == 0 and dy == 0:
            return math.sqrt((px - x1)**2 + (py - y1)**2)
        
        t = max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)))
        proj_x = x1 + t * dx
        proj_y = y1 + t * dy
        return math.sqrt((px - proj_x)**2 + (py - proj_y)**2)
    
    def _distance_to_corridor(self, x: float, y: float, corridor: Dict[str, Any]) -> float:
        """计算点到 corridor 的距离"""
        if corridor.get("points"):
            return self._point_to_path_distance(x, y, corridor["points"])
        return 0.0
    
    def _point_to_path_distance(self, x: float, y: float, path_points: List[List[float]]) -> float:
        """计算点到路径的最短距离"""
        if len(path_points) < 2:
            return float('inf')
        
        min_dist = float('inf')
        for i in range(len(path_points) - 1):
            p1 = path_points[i]
            p2 = path_points[i + 1]
            dist = self._point_to_segment_distance(x, y, p1[0], p1[1], p2[0], p2[1])
            min_dist = min(min_dist, dist)
        
        return min_dist
    
    def _point_in_polygon(self, x: float, y: float, polygon: List[List[float]]) -> bool:
        """简化的点-in-polygon 判断（射线法）"""
        if len(polygon) < 3:
            return False
        
        n = len(polygon)
        inside = False
        
        p1x, p1y = polygon[0]
        for i in range(1, n + 1):
            p2x, p2y = polygon[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        
        return inside
