# scene_graph.py

"""
跨场景知识图谱 Scene Graph V1

统一表达不同场景的结构（医院/商场/地铁/政务大厅等）
"""

import json
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict


@dataclass
class SceneNode:
    """
    场景节点：统一表达不同场景的结构节点
    """
    id: str
    type: str  # Entrance, Hall, Corridor, Stair, Elevator, Toilet, RegistrationCounter, etc.
    name: str = ""
    floor: int = 0  # 楼层（户外用0）
    position: Tuple[float, float] = (0.0, 0.0)  # (x, y) 或逻辑坐标
    tags: List[str] = None  # 其他标签（如：Toilet, Elevator）
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []


@dataclass
class SceneEdge:
    """
    场景边：连接关系
    """
    from_id: str
    to_id: str
    edge_type: str  # adjacent_to, route_segment, connected_by, contains
    distance: float = 0.0  # 距离（米），route_segment 专用
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class SceneGraph:
    """
    场景图谱：管理场景节点和边的图结构
    """
    
    def __init__(self):
        self.nodes: Dict[str, SceneNode] = {}
        self.edges: List[SceneEdge] = []
    
    def add_node(self, node: SceneNode):
        """
        添加节点
        """
        self.nodes[node.id] = node
    
    def add_edge(self, edge: SceneEdge):
        """
        添加边
        """
        self.edges.append(edge)
    
    def find_nearest(self, node_type: str, current_pos: Tuple[float, float]) -> Optional[SceneNode]:
        """
        查找最近的指定类型节点
        
        参数：
        - node_type: 节点类型（如 "Toilet", "Elevator"）
        - current_pos: 当前位置 (x, y)
        
        返回：
        - 最近的节点，如果未找到则返回 None
        """
        candidates = [node for node in self.nodes.values() if node.type == node_type]
        
        if not candidates:
            return None
        
        # 简单欧式距离计算
        def distance(pos1, pos2):
            return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5
        
        nearest = min(candidates, key=lambda n: distance(current_pos, n.position))
        return nearest
    
    def find_path(self, start_id: str, end_id: str) -> List[str]:
        """
        查找从起点到终点的路径（BFS算法）
        
        参数：
        - start_id: 起点节点ID
        - end_id: 终点节点ID
        
        返回：
        - 节点ID列表（路径），如果无法到达则返回空列表
        """
        if start_id not in self.nodes or end_id not in self.nodes:
            return []
        
        if start_id == end_id:
            return [start_id]
        
        # BFS 搜索
        queue = [(start_id, [start_id])]
        visited = {start_id}
        
        while queue:
            current_id, path = queue.pop(0)
            
            # 查找所有与当前节点相连的节点（通过 route_segment 边）
            neighbors = []
            for edge in self.edges:
                if edge.edge_type in ("route_segment", "adjacent_to"):
                    if edge.from_id == current_id and edge.to_id not in visited:
                        neighbors.append(edge.to_id)
                    elif edge.to_id == current_id and edge.from_id not in visited:
                        neighbors.append(edge.from_id)
            
            for neighbor_id in neighbors:
                if neighbor_id == end_id:
                    return path + [neighbor_id]
                
                if neighbor_id not in visited:
                    visited.add(neighbor_id)
                    queue.append((neighbor_id, path + [neighbor_id]))
        
        return []  # 无法到达
    
    def find_department(self, department_name: str) -> Optional[SceneNode]:
        """
        查找科室节点（医院场景专用）
        
        参数：
        - department_name: 科室名称（如 "牙科", "Dental"）
        
        返回：
        - 科室节点，如果未找到则返回 None
        """
        for node in self.nodes.values():
            if node.type == "DepartmentArea" and department_name.lower() in node.name.lower():
                return node
        return None
    
    def get_department_floor(self, department_name: str) -> Optional[int]:
        """
        获取科室所在楼层
        
        参数：
        - department_name: 科室名称
        
        返回：
        - 楼层号，如果未找到则返回 None
        """
        dept_node = self.find_department(department_name)
        if dept_node:
            return dept_node.floor
        return None
    
    def get_nodes_by_type(self, node_type: str) -> List[SceneNode]:
        """
        获取指定类型的所有节点
        """
        return [node for node in self.nodes.values() if node.type == node_type]
    
    def get_edges_by_type(self, edge_type: str) -> List[SceneEdge]:
        """
        获取指定类型的所有边
        """
        return [edge for edge in self.edges if edge.edge_type == edge_type]
    
    def export(self, filename: str):
        """
        导出图谱为 JSON 文件
        """
        data = {
            "nodes": [asdict(node) for node in self.nodes.values()],
            "edges": [asdict(edge) for edge in self.edges]
        }
        
        # 处理 position tuple
        for node_dict in data["nodes"]:
            node_dict["position"] = list(node_dict["position"])
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"[SceneGraph] Exported to {filename}")
    
    def load(self, filename: str):
        """
        从 JSON 文件加载图谱
        """
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # 加载节点
            self.nodes = {}
            for node_dict in data.get("nodes", []):
                node_dict["position"] = tuple(node_dict["position"])
                node = SceneNode(**node_dict)
                self.nodes[node.id] = node
            
            # 加载边
            self.edges = []
            for edge_dict in data.get("edges", []):
                edge = SceneEdge(**edge_dict)
                self.edges.append(edge)
            
            print(f"[SceneGraph] Loaded from {filename}")
        except Exception as e:
            print(f"[SceneGraph] Failed to load: {e}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        获取图谱统计信息（用于调试）
        """
        node_types = {}
        for node in self.nodes.values():
            node_types[node.type] = node_types.get(node.type, 0) + 1
        
        edge_types = {}
        for edge in self.edges:
            edge_types[edge.edge_type] = edge_types.get(edge.edge_type, 0) + 1
        
        return {
            "total_nodes": len(self.nodes),
            "total_edges": len(self.edges),
            "node_types": node_types,
            "edge_types": edge_types
        }

