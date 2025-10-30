#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 路径解析器
判断节点是否在同一条路径上，决定导航连续性
"""

import logging
from typing import List, Dict, Any, Optional, Tuple
from core.scene_memory_system import get_scene_memory_system

logger = logging.getLogger(__name__)

class PathResolver:
    """路径解析器"""
    
    def __init__(self):
        """初始化路径解析器"""
        self.scene_memory = get_scene_memory_system()
        logger.info("🔍 路径解析器初始化完成")
    
    def is_node_in_path(self, path_id: str, node_label: str) -> bool:
        """
        判断节点是否在指定路径中
        
        Args:
            path_id: 路径ID
            node_label: 节点标签
            
        Returns:
            bool: 是否在路径中
        """
        try:
            path_memory = self.scene_memory.memory_mapper.get_path(path_id)
            if not path_memory:
                return False
            
            # 检查节点标签
            node_labels = [n.label for n in path_memory.nodes]
            result = node_label in node_labels
            
            logger.debug(f"节点 {node_label} 在路径 {path_id} 中: {result}")
            return result
            
        except Exception as e:
            logger.error(f"❌ 判断节点路径失败: {e}")
            return False
    
    def find_path_for_node(self, node_label: str) -> Optional[str]:
        """
        查找包含指定节点的路径
        
        Args:
            node_label: 节点标签
            
        Returns:
            Optional[str]: 路径ID，如果未找到则返回None
        """
        try:
            for path_id in self.scene_memory.memory_mapper.list_paths():
                if self.is_node_in_path(path_id, node_label):
                    logger.info(f"✅ 找到包含节点 {node_label} 的路径: {path_id}")
                    return path_id
            
            logger.info(f"⚠️ 未找到包含节点 {node_label} 的路径")
            return None
            
        except Exception as e:
            logger.error(f"❌ 查找节点路径失败: {e}")
            return None
    
    def should_create_new_path(self, current_node: str, target_node: str) -> Dict[str, Any]:
        """
        判断是否需要创建新路径
        
        Args:
            current_node: 当前节点标签
            target_node: 目标节点标签
            
        Returns:
            Dict: 判断结果
        """
        try:
            # 查找当前节点所在的路径
            current_path_id = self.find_path_for_node(current_node)
            target_path_id = self.find_path_for_node(target_node)
            
            # 情况1: 两个节点在同一条路径中
            if current_path_id and target_path_id and current_path_id == target_path_id:
                path_memory = self.scene_memory.memory_mapper.get_path(current_path_id)
                nodes = [n.label for n in path_memory.nodes]
                
                # 检查顺序
                current_idx = nodes.index(current_node)
                target_idx = nodes.index(target_node)
                
                if current_idx < target_idx:
                    # 顺序正确，可以继续使用当前路径
                    return {
                        "should_create": False,
                        "reason": "same_path_forward",
                        "path_id": current_path_id,
                        "message": "目标在当前路径的前方"
                    }
                else:
                    # 需要反向或回退
                    return {
                        "should_create": False,
                        "reason": "same_path_backward",
                        "path_id": current_path_id,
                        "message": "目标是当前路径的后方，需要回退"
                    }
            
            # 情况2: 当前节点在路径A，目标节点在路径B
            elif current_path_id and target_path_id and current_path_id != target_path_id:
                # 需要创建连接路径或触发切换
                return {
                    "should_create": True,
                    "reason": "cross_path",
                    "current_path": current_path_id,
                    "target_path": target_path_id,
                    "message": "需要跨路径导航，建议创建连接路径"
                }
            
            # 情况3: 当前节点有路径，目标节点无路径
            elif current_path_id and not target_path_id:
                return {
                    "should_create": True,
                    "reason": "target_unknown",
                    "current_path": current_path_id,
                    "message": "目标节点不存在，将创建新路径"
                }
            
            # 情况4: 目标节点有路径，当前节点无路径
            elif not current_path_id and target_path_id:
                return {
                    "should_create": True,
                    "reason": "current_unknown",
                    "target_path": target_path_id,
                    "message": "当前节点不在任何路径中，将创建新路径"
                }
            
            # 情况5: 两个节点都不在任何路径中
            else:
                return {
                    "should_create": True,
                    "reason": "both_unknown",
                    "message": "两个节点都不存在，将创建全新的路径"
                }
            
        except Exception as e:
            logger.error(f"❌ 判断路径创建失败: {e}")
            return {
                "should_create": True,
                "reason": "error",
                "message": f"判断失败: {e}"
            }
    
    def get_path_continuity(self, path_id: str, node_label: str) -> Dict[str, Any]:
        """
        获取路径连续性信息
        
        Args:
            path_id: 路径ID
            node_label: 节点标签
            
        Returns:
            Dict: 连续性信息
        """
        try:
            path_memory = self.scene_memory.memory_mapper.get_path(path_id)
            if not path_memory:
                return {"continuous": False, "message": "路径不存在"}
            
            nodes = path_memory.nodes
            node_labels = [n.label for n in nodes]
            
            if node_label not in node_labels:
                return {"continuous": False, "message": "节点不在路径中"}
            
            # 找到节点在路径中的位置
            node_index = node_labels.index(node_label)
            
            # 判断是否在路径末尾
            is_at_end = node_index == len(nodes) - 1
            
            # 判断是否在路径开头
            is_at_start = node_index == 0
            
            return {
                "continuous": True,
                "index": node_index,
                "total_nodes": len(nodes),
                "is_at_end": is_at_end,
                "is_at_start": is_at_start,
                "has_next": not is_at_end,
                "has_prev": not is_at_start,
                "next_node": nodes[node_index + 1].label if not is_at_end else None,
                "prev_node": nodes[node_index - 1].label if not is_at_start else None
            }
            
        except Exception as e:
            logger.error(f"❌ 获取路径连续性失败: {e}")
            return {"continuous": False, "message": str(e)}


if __name__ == "__main__":
    # 测试路径解析器
    import logging
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 60)
    print("🔍 路径解析器测试")
    print("=" * 60)
    
    resolver = PathResolver()
    
    # 测试节点查找
    print("\n1. 测试节点查找")
    for node in ["挂号处", "检查室", "Unknown Node"]:
        path_id = resolver.find_path_for_node(node)
        print(f"   节点 '{node}' 在路径: {path_id or '未找到'}")
    
    # 测试路径判断
    print("\n2. 测试路径创建判断")
    result = resolver.should_create_new_path("挂号处", "检查室")
    print(f"   {result}")
    
    # 测试连续性
    print("\n3. 测试路径连续性")
    result = resolver.get_path_continuity("test_hospital_path", "挂号处（已修正）")
    print(f"   {result}")
    
    print("\n" + "=" * 60)

