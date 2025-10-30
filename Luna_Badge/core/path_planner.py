#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 路径规划器
处理多目的地导航、路径合并、路径规划
"""

import logging
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
import copy

logger = logging.getLogger(__name__)

@dataclass
class RouteSegment:
    """路径段"""
    start_node: str          # 起始节点
    end_node: str            # 结束节点
    path_id: str            # 路径ID
    distance: float = 0.0   # 距离
    duration: float = 0.0   # 耗时
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "start_node": self.start_node,
            "end_node": self.end_node,
            "path_id": self.path_id,
            "distance": self.distance,
            "duration": self.duration
        }

class PathPlanner:
    """路径规划器"""
    
    def __init__(self, scene_memory):
        """
        初始化路径规划器
        
        Args:
            scene_memory: 场景记忆系统实例
        """
        self.scene_memory = scene_memory
        self.route_graph = {}  # 路径图 {节点: [连接的节点]}
        
        # 策略选择
        self.preferred_strategy = "smart_merge"  # smart_merge, fallback, ask_user
        
        logger.info("🗺️ 路径规划器初始化完成")
    
    def build_route_graph(self):
        """构建路径图"""
        self.route_graph = {}
        
        # 遍历所有路径，构建节点连接图
        for path_id, path_memory in self.scene_memory.memory_mapper.memories.items():
            nodes = path_memory.nodes
            if len(nodes) < 2:
                continue
            
            # 构建单向连接
            for i in range(len(nodes) - 1):
                start_label = nodes[i].label
                end_label = nodes[i + 1].label
                
                if start_label not in self.route_graph:
                    self.route_graph[start_label] = []
                
                self.route_graph[start_label].append({
                    "target": end_label,
                    "path_id": path_id,
                    "distance": self._estimate_distance(nodes[i], nodes[i + 1])
                })
        
        logger.info(f"✅ 路径图构建完成，包含 {len(self.route_graph)} 个节点")
    
    def _estimate_distance(self, node1, node2) -> float:
        """估算两节点间距离"""
        # 简化：基于时间戳差值估算
        # 实际应该使用GPS或步数数据
        return 10.0  # 默认10米
    
    def plan_route(self, start: str, destinations: List[str]) -> Dict[str, Any]:
        """
        规划从起点到多个目的地的路径
        
        Args:
            start: 起点（可以是节点标签或path_id）
            destinations: 目的地列表（节点标签）
            
        Returns:
            Dict: 规划的路径结果
        """
        # 首先构建路径图
        self.build_route_graph()
        
        # 规划到第一个目的地的路径
        route_segments = []
        current_pos = start
        unknown_segments = []
        
        for i, dest in enumerate(destinations):
            # 尝试找到从当前位置到目的地的路径
            path_to_dest = self._find_path(current_pos, dest)
            
            if path_to_dest:
                # 找到已知路径
                route_segments.extend(path_to_dest)
                logger.info(f"✅ 找到路径: {current_pos} -> {dest}")
                current_pos = dest  # 更新当前位置
            else:
                # 未找到路径
                unknown_segments.append({
                    "from": current_pos,
                    "to": dest,
                    "index": i
                })
                logger.warning(f"⚠️ 未找到路径: {current_pos} -> {dest}")
        
        # 处理未知路径段
        if unknown_segments:
            strategy_result = self._handle_unknown_paths(unknown_segments)
        else:
            strategy_result = {"can_navigate": True, "strategy": "direct"}
        
        # 合并结果
        result = {
            "can_navigate": strategy_result.get("can_navigate", False),
            "strategy": strategy_result.get("strategy", "unknown"),
            "segments": [s.to_dict() for s in route_segments],
            "unknown_segments": unknown_segments,
            "total_distance": sum(s.distance for s in route_segments),
            "message": self._generate_navigation_message(strategy_result, unknown_segments)
        }
        
        return result
    
    def _find_path(self, start: str, end: str) -> Optional[List[RouteSegment]]:
        """
        在路径图中查找路径
        
        Args:
            start: 起点
            end: 终点
            
        Returns:
            Optional[List[RouteSegment]]: 路径段列表
        """
        # BFS搜索
        from collections import deque
        
        visited = set()
        queue = deque([(start, [])])  # (当前节点, 路径)
        
        while queue:
            current, path = queue.popleft()
            
            if current == end:
                # 找到路径
                return [RouteSegment(**seg) for seg in path]
            
            if current in visited:
                continue
            visited.add(current)
            
            # 遍历邻居
            if current in self.route_graph:
                for neighbor in self.route_graph[current]:
                    if neighbor["target"] not in visited:
                        new_path = path + [{
                            "start_node": current,
                            "end_node": neighbor["target"],
                            "path_id": neighbor["path_id"],
                            "distance": neighbor["distance"]
                        }]
                        queue.append((neighbor["target"], new_path))
        
        return None
    
    def _handle_unknown_paths(self, unknown_segments: List[Dict]) -> Dict[str, Any]:
        """
        处理未知路径段
        
        Args:
            unknown_segments: 未知路径段列表
            
        Returns:
            Dict: 处理策略结果
        """
        if self.preferred_strategy == "smart_merge":
            return self._smart_merge_strategy(unknown_segments)
        elif self.preferred_strategy == "fallback":
            return self._fallback_strategy(unknown_segments)
        else:  # ask_user
            return self._ask_user_strategy(unknown_segments)
    
    def _smart_merge_strategy(self, unknown_segments: List[Dict]) -> Dict[str, Any]:
        """
        智能合并策略：
        1. 尝试通过回退到已知节点
        2. 如果不行，切换到实时路径记录模式
        
        Args:
            unknown_segments: 未知路径段
            
        Returns:
            Dict: 策略结果
        """
        results = []
        can_navigate = True
        all_parts_navigable = True
        
        for seg in unknown_segments:
            seg_from = seg["from"]
            seg_to = seg["to"]
            
            # 尝试策略1：寻找共同祖先节点
            common_ancestor = self._find_common_ancestor(seg_from, seg_to)
            
            if common_ancestor:
                # 通过回退到共同祖先，再前往目的地
                results.append({
                    "strategy": "backtrack",
                    "from": seg_from,
                    "via": common_ancestor,
                    "to": seg_to,
                    "message": f"需要回退到{common_ancestor}，再前往{seg_to}"
                })
                all_parts_navigable = False
            else:
                # 策略2：切换到实时路径记录模式
                results.append({
                    "strategy": "record_mode",
                    "from": seg_from,
                    "to": seg_to,
                    "message": f"将记录{seg_from}到{seg_to}的新路径"
                })
        
        return {
            "can_navigate": can_navigate,
            "strategy": "smart_merge",
            "partial_navigation": not all_parts_navigable,
            "details": results
        }
    
    def _fallback_strategy(self, unknown_segments: List[Dict]) -> Dict[str, Any]:
        """
        回退策略：遇到未知路径则建议回退
        
        Returns:
            Dict: 策略结果
        """
        # 找到最近的回退点
        messages = []
        for seg in unknown_segments:
            backtrack_point = self._find_nearest_known_node(seg["from"])
            if backtrack_point:
                messages.append(
                    f"需要从{seg['from']}回退到{backtrack_point}，"
                    f"再从{backtrack_point}前往{seg['to']}"
                )
            else:
                messages.append(f"无法从{seg['from']}前往{seg['to']}，建议返回起点")
        
        return {
            "can_navigate": False,
            "strategy": "fallback",
            "message": "；".join(messages)
        }
    
    def _ask_user_strategy(self, unknown_segments: List[Dict]) -> Dict[str, Any]:
        """询问用户策略"""
        return {
            "can_navigate": True,
            "strategy": "ask_user",
            "message": "需要您的帮助来确定路径"
        }
    
    def _find_common_ancestor(self, node1: str, node2: str) -> Optional[str]:
        """
        寻找两个节点的共同祖先
        
        Args:
            node1: 节点1
            node2: 节点2
            
        Returns:
            Optional[str]: 共同祖先节点
        """
        # 简化实现：在所有路径中查找公共节点
        for path_id, path_memory in self.scene_memory.memory_mapper.memories.items():
            node_labels = [n.label for n in path_memory.nodes]
            if node1 in node_labels and node2 in node_labels:
                # 找到包含两者的路径
                idx1 = node_labels.index(node1)
                idx2 = node_labels.index(node2)
                
                if idx1 < idx2:
                    # 在同一个路径中，且顺序正确
                    return None  # 不需要回退
                else:
                    # 需要回退到更早的节点
                    for i in range(min(idx1, idx2)):
                        if node_labels[i] in self.route_graph:
                            return node_labels[i]
        
        # 查找任一公共节点
        common_nodes = set()
        for path_id, path_memory in self.scene_memory.memory_mapper.memories.items():
            node_labels = set(n.label for n in path_memory.nodes)
            if not common_nodes:
                common_nodes = node_labels
            else:
                common_nodes &= node_labels
        
        return common_nodes.pop() if common_nodes else None
    
    def _find_nearest_known_node(self, node: str) -> Optional[str]:
        """查找最近的已知节点"""
        # 简化：返回起点或第一个节点
        for path_id, path_memory in self.scene_memory.memory_mapper.memories.items():
            if path_memory.nodes:
                return path_memory.nodes[0].label
        return None
    
    def _generate_navigation_message(self, strategy_result: Dict, 
                                    unknown_segments: List[Dict]) -> str:
        """生成导航提示消息"""
        strategy = strategy_result.get("strategy", "unknown")
        
        if strategy == "direct":
            return "可以开始导航"
        elif strategy == "smart_merge":
            if strategy_result.get("partial_navigation"):
                details = strategy_result.get("details", [])
                if details:
                    detail = details[0]
                    return detail.get("message", "")
            else:
                return "将启动路径记录模式"
        elif strategy == "fallback":
            return strategy_result.get("message", "需要回退")
        elif strategy == "ask_user":
            return "需要您的确认"
        
        return "路径规划完成"
    
    def merge_paths_to_continuous(self, path_ids: List[str]) -> Optional[Dict[str, Any]]:
        """
        将多个路径合并为连续导航
        
        Args:
            path_ids: 路径ID列表
            
        Returns:
            Optional[Dict]: 合并后的路径
        """
        merged_nodes = []
        
        for path_id in path_ids:
            path_memory = self.scene_memory.memory_mapper.get_path(path_id)
            if not path_memory:
                continue
            
            # 添加节点（避免重复）
            for node in path_memory.nodes:
                if node.label not in [n.label for n in merged_nodes]:
                    merged_nodes.append(copy.deepcopy(node))
        
        if not merged_nodes:
            return None
        
        # 创建合并路径
        return {
            "merged_nodes": merged_nodes,
            "total_length": len(merged_nodes),
            "source_paths": path_ids
        }


if __name__ == "__main__":
    # 测试路径规划器
    import logging
    logging.basicConfig(level=logging.INFO)
    
    from core.scene_memory_system import get_scene_memory_system
    
    print("=" * 60)
    print("🗺️ 路径规划器测试")
    print("=" * 60)
    
    system = get_scene_memory_system()
    planner = PathPlanner(system)
    
    # 构建路径图
    planner.build_route_graph()
    
    # 测试路径规划
    print("\n1. 测试单一路径规划")
    result = planner.plan_route("挂号处", ["检查室"])
    print(f"   结果: {result}")
    
    print("\n2. 测试多目的地路径规划")
    result = planner.plan_route("挂号处", ["检查室", "报告领取", "Exit"])
    print(f"   结果: {result}")
    
    print("\n3. 测试未知路径处理")
    result = planner.plan_route("未知起点", ["检查室"])
    print(f"   结果: {result}")
    
    print("\n" + "=" * 60)

