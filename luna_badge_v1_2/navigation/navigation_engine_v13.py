"""
NavigationEngineV13: 导航引擎 v1.3

核心能力：
- 可通行区域判断
- 台阶识别
- 风险级别事件生成（结构化输出）
"""

from typing import Dict, List, Any, Optional


class NavigationEngineV13:
    """
    导航引擎 v1.3：

    - 可通行区域判断
    - 台阶识别
    - 风险级别事件生成（结构化输出）
    """

    def __init__(self):
        """初始化导航引擎"""
        pass

    def evaluate(self, scene_graph: Dict[str, Any], movement_state: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        评估当前场景，返回结构化事件。

        Args:
            scene_graph: 场景图数据，包含：
                - obstacle_front_dist: float - 前方障碍物距离（米）
                - obstacle_left_dist: float - 左侧障碍物距离（米）
                - obstacle_right_dist: float - 右侧障碍物距离（米）
                - stairs_up_dist: float - 上台阶距离（米）
                - stairs_down_dist: float - 下台阶距离（米）
                - road_narrow: bool - 道路是否变窄
                - water_puddle: bool - 是否有积水
                - crowded_ahead: bool - 前方是否拥挤
                - complex_environment: bool - 环境是否复杂
            movement_state: 运动状态（可选）

        Returns:
            包含以下字段的字典：
                - events: List[Dict] - 结构化事件列表
                - nav_result: Optional[Dict] - 导航决策结果（保留兼容性）
                - speech_event: Optional[Dict] - 传统 speech_event（保留兼容性）

        事件结构：
            {
                'type': 'danger' | 'navigation' | 'system',
                'code': 'obstacle_front' | 'stairs_down' | ...,
                'distance': float,  # 可选，距离（米）
                ...  # 其他自定义字段
            }
        """
        events = []

        # 检查前方障碍物
        obstacle_front_dist = scene_graph.get("obstacle_front_dist")
        if obstacle_front_dist is not None:
            dist = float(obstacle_front_dist)
            if dist < 1.5:  # 1.5 米内视为危险
                events.append({
                    "type": "danger",
                    "code": "obstacle_front",
                    "distance": dist,
                })

        # 检查左侧障碍物
        obstacle_left_dist = scene_graph.get("obstacle_left_dist")
        if obstacle_left_dist is not None:
            dist = float(obstacle_left_dist)
            if dist < 1.0:  # 1.0 米内视为危险
                events.append({
                    "type": "danger",
                    "code": "obstacle_left",
                    "distance": dist,
                })

        # 检查右侧障碍物
        obstacle_right_dist = scene_graph.get("obstacle_right_dist")
        if obstacle_right_dist is not None:
            dist = float(obstacle_right_dist)
            if dist < 1.0:  # 1.0 米内视为危险
                events.append({
                    "type": "danger",
                    "code": "obstacle_right",
                    "distance": dist,
                })

        # 检查下台阶
        stairs_down_dist = scene_graph.get("stairs_down_dist")
        if stairs_down_dist is not None:
            dist = float(stairs_down_dist)
            if dist < 2.0:  # 2.0 米内需要提醒
                events.append({
                    "type": "danger",
                    "code": "stairs_down",
                    "distance": dist,
                })

        # 检查上台阶
        stairs_up_dist = scene_graph.get("stairs_up_dist")
        if stairs_up_dist is not None:
            dist = float(stairs_up_dist)
            if dist < 2.0:  # 2.0 米内需要提醒
                events.append({
                    "type": "danger",
                    "code": "stairs_up",
                    "distance": dist,
                })

        # 检查道路变窄
        if scene_graph.get("road_narrow", False):
            events.append({
                "type": "navigation",
                "code": "road_narrow",
            })

        # 检查积水
        if scene_graph.get("water_puddle", False):
            events.append({
                "type": "danger",
                "code": "water_puddle",
            })

        # 检查前方拥挤
        if scene_graph.get("crowded_ahead", False):
            events.append({
                "type": "danger",
                "code": "crowded_ahead",
            })

        # 检查复杂环境
        if scene_graph.get("complex_environment", False):
            events.append({
                "type": "danger",
                "code": "complex_environment",
            })

        return {
            "events": events,
            "nav_result": None,  # 保留兼容性
            "speech_event": None,  # 保留兼容性
        }

    def process_frame(self, frame: Any) -> Dict[str, Any]:
        """
        处理单帧数据（兼容接口）。

        Args:
            frame: 输入帧数据

        Returns:
            与 evaluate() 相同的结构
        """
        # 这里应该从 frame 中提取 scene_graph
        # 为了演示，我们使用一个空的 scene_graph
        scene_graph = {}
        return self.evaluate(scene_graph)
