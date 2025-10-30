#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
邻接图构建器
为路径中的节点构建邻接关系图，添加adjacent字段
支持未来扩展为路径查找或Dijkstra算法
"""

import json
import os
import logging
from typing import Dict, List, Optional, Set
from collections import defaultdict

logger = logging.getLogger(__name__)

class AdjacencyGraphBuilder:
    """邻接图构建器"""
    
    def __init__(self):
        """初始化邻接图构建器"""
        self.adjacency_list = defaultdict(set)  # 全局邻接表
        logger.info("🕸️ 邻接图构建器初始化完成")
    
    def build_adjacency_graph(self, memory_store_path: str, 
                             output_path: str = None) -> Dict:
        """
        构建邻接图并更新记忆存储
        
        Args:
            memory_store_path: 记忆存储文件路径
            output_path: 输出文件路径（如果为None则覆盖原文件）
            
        Returns:
            Dict: 构建统计信息
        """
        if output_path is None:
            output_path = memory_store_path
        
        try:
            # 读取数据
            with open(memory_store_path, 'r', encoding='utf-8') as f:
                memory_data = json.load(f)
            
            if "paths" not in memory_data:
                logger.error("记忆存储中没有路径数据")
                return {"error": "No paths data"}
            
            # 统计信息
            stats = {
                "total_paths": 0,
                "total_nodes": 0,
                "total_edges": 0,
                "cross_path_connections": 0
            }
            
            # 为每个路径构建邻接关系
            for path in memory_data["paths"]:
                stats["total_paths"] += 1
                path_id = path.get("path_id", "")
                nodes = path.get("nodes", [])
                
                if len(nodes) < 2:
                    continue
                
                # 构建路径内部的邻接关系
                for i, node in enumerate(nodes):
                    stats["total_nodes"] += 1
                    node_id = node.get("node_id", f"{path_id}_node_{i}")
                    
                    # 确保adjacent字段存在
                    if "adjacent" not in node:
                        node["adjacent"] = []
                    
                    # 计算相邻节点
                    adjacent_ids = []
                    
                    # 前一个节点
                    if i > 0:
                        prev_id = nodes[i-1].get("node_id", f"{path_id}_node_{i-1}")
                        adjacent_ids.append(prev_id)
                        self.adjacency_list[node_id].add(prev_id)
                    
                    # 后一个节点
                    if i < len(nodes) - 1:
                        next_id = nodes[i+1].get("node_id", f"{path_id}_node_{i+1}")
                        adjacent_ids.append(next_id)
                        self.adjacency_list[node_id].add(next_id)
                    
                    # 更新节点
                    node["adjacent"] = adjacent_ids
                    stats["total_edges"] += len(adjacent_ids)
            
            # 检测跨路径连接（可选功能）
            stats["cross_path_connections"] = self._detect_cross_path_connections(memory_data)
            
            # 保存更新后的数据
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(memory_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"✅ 邻接图构建完成:")
            logger.info(f"   - 路径数: {stats['total_paths']}")
            logger.info(f"   - 节点数: {stats['total_nodes']}")
            logger.info(f"   - 边数: {stats['total_edges']}")
            logger.info(f"   - 跨路径连接: {stats['cross_path_connections']}")
            
            return stats
            
        except FileNotFoundError:
            logger.error(f"文件不存在: {memory_store_path}")
            return {"error": "File not found"}
        except json.JSONDecodeError:
            logger.error(f"文件格式错误: {memory_store_path}")
            return {"error": "JSON decode error"}
        except Exception as e:
            logger.error(f"构建邻接图失败: {e}")
            import traceback
            traceback.print_exc()
            return {"error": str(e)}
    
    def _detect_cross_path_connections(self, memory_data: Dict) -> int:
        """检测跨路径的连接点"""
        cross_connections = 0
        
        # 收集所有节点的位置信息
        node_locations = {}
        for path in memory_data.get("paths", []):
            for node in path.get("nodes", []):
                node_id = node.get("node_id")
                gps = node.get("gps")
                label = node.get("label", "")
                
                if gps and node_id:
                    key = f"{gps.get('lat', 0)}_{gps.get('lng', 0)}"
                    if key not in node_locations:
                        node_locations[key] = []
                    node_locations[key].append({
                        "node_id": node_id,
                        "path_id": path.get("path_id"),
                        "label": label
                    })
        
        # 检查位置接近的节点（可能是同一个物理位置）
        for location_key, nodes in node_locations.items():
            if len(nodes) > 1:
                # 有多个节点在同一位置，可能是跨路径连接点
                cross_connections += len(nodes) - 1
                logger.debug(f"发现跨路径连接点: {[n['label'] for n in nodes]}")
        
        return cross_connections
    
    def get_adjacent_nodes(self, memory_store_path: str, 
                          path_id: str, node_id: str) -> List[str]:
        """
        获取指定节点的相邻节点列表
        
        Args:
            memory_store_path: 记忆存储文件路径
            path_id: 路径ID
            node_id: 节点ID
            
        Returns:
            List[str]: 相邻节点ID列表
        """
        try:
            with open(memory_store_path, 'r', encoding='utf-8') as f:
                memory_data = json.load(f)
            
            for path in memory_data.get("paths", []):
                if path.get("path_id") == path_id:
                    for node in path.get("nodes", []):
                        if node.get("node_id") == node_id:
                            return node.get("adjacent", [])
            
            logger.warning(f"未找到节点: {path_id}/{node_id}")
            return []
            
        except Exception as e:
            logger.error(f"获取相邻节点失败: {e}")
            return []
    
    def find_shortest_path(self, memory_store_path: str, 
                          start_node_id: str, end_node_id: str) -> Optional[List[str]]:
        """
        查找两个节点之间的最短路径（简单BFS实现）
        
        Args:
            memory_store_path: 记忆存储文件路径
            start_node_id: 起始节点ID
            end_node_id: 目标节点ID
            
        Returns:
            Optional[List[str]]: 路径节点ID列表，如果不存在则返回None
        """
        try:
            # 加载邻接数据
            with open(memory_store_path, 'r', encoding='utf-8') as f:
                memory_data = json.load(f)
            
            # 构建完整邻接表
            adjacency_map = {}
            for path in memory_data.get("paths", []):
                for node in path.get("nodes", []):
                    node_id = node.get("node_id")
                    if node_id:
                        adjacency_map[node_id] = node.get("adjacent", [])
            
            # BFS搜索
            from collections import deque
            
            queue = deque([(start_node_id, [start_node_id])])
            visited = {start_node_id}
            
            while queue:
                current_node, path = queue.popleft()
                
                if current_node == end_node_id:
                    return path
                
                # 遍历相邻节点
                for adjacent_node in adjacency_map.get(current_node, []):
                    if adjacent_node not in visited:
                        visited.add(adjacent_node)
                        queue.append((adjacent_node, path + [adjacent_node]))
            
            # 未找到路径
            logger.warning(f"未找到从 {start_node_id} 到 {end_node_id} 的路径")
            return None
            
        except Exception as e:
            logger.error(f"查找最短路径失败: {e}")
            return None
    
    def get_graph_statistics(self, memory_store_path: str) -> Dict:
        """
        获取图的统计信息
        
        Args:
            memory_store_path: 记忆存储文件路径
            
        Returns:
            Dict: 图统计信息
        """
        try:
            with open(memory_store_path, 'r', encoding='utf-8') as f:
                memory_data = json.load(f)
            
            stats = {
                "total_nodes": 0,
                "total_edges": 0,
                "isolated_nodes": 0,
                "max_degree": 0,
                "node_degrees": {}
            }
            
            # 统计节点度数
            for path in memory_data.get("paths", []):
                for node in path.get("nodes", []):
                    node_id = node.get("node_id")
                    adjacent = node.get("adjacent", [])
                    
                    if node_id:
                        stats["total_nodes"] += 1
                        degree = len(adjacent)
                        stats["total_edges"] += degree
                        stats["node_degrees"][node_id] = degree
                        
                        if degree == 0:
                            stats["isolated_nodes"] += 1
                        
                        if degree > stats["max_degree"]:
                            stats["max_degree"] = degree
            
            return stats
            
        except Exception as e:
            logger.error(f"获取图统计信息失败: {e}")
            return {}

def main():
    """测试主函数"""
    import sys
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    builder = AdjacencyGraphBuilder()
    
    # 测试构建邻接图
    memory_file = "data/memory_store.json"
    if os.path.exists(memory_file):
        print("\n=== 构建邻接图 ===")
        stats = builder.build_adjacency_graph(memory_file)
        print(f"\n构建统计: {stats}")
        
        # 测试获取相邻节点
        print("\n=== 获取图的统计信息 ===")
        graph_stats = builder.get_graph_statistics(memory_file)
        print(f"\n图统计: {graph_stats}")

if __name__ == "__main__":
    main()


