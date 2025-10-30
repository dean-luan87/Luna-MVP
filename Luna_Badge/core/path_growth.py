#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 路径增长管理器
决定路径扩展或创建新路径的逻辑
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime
from core.scene_memory_system import get_scene_memory_system

logger = logging.getLogger(__name__)

class PathGrowthManager:
    """路径增长管理器"""
    
    def __init__(self, distance_threshold: float = 50.0):
        """
        初始化路径增长管理器
        
        Args:
            distance_threshold: 距离阈值（米），超过此值创建新路径
        """
        self.scene_memory = get_scene_memory_system()
        self.distance_threshold = distance_threshold
        
        # 路径一致性指标
        self.coherence_threshold = 0.7  # 0-1之间，越高越严格
        
        logger.info(f"🌱 路径增长管理器初始化完成 (阈值: {distance_threshold}m)")
    
    def should_extend_path(self, path_id: str, new_node) -> Dict[str, Any]:
        """
        判断是否应该扩展路径
        
        Args:
            path_id: 当前路径ID
            new_node: 新节点对象
            
        Returns:
            Dict: 决策结果
        """
        try:
            path_memory = self.scene_memory.memory_mapper.get_path(path_id)
            if not path_memory or len(path_memory.nodes) == 0:
                return {
                    "should_extend": False,
                    "reason": "empty_path",
                    "action": "create_new"
                }
            
            # 获取最后一个节点
            last_node = path_memory.nodes[-1]
            
            # 计算距离
            distance = self._estimate_distance(last_node, new_node)
            
            # 判断视觉相似度
            visual_similarity = self._estimate_visual_similarity(last_node, new_node)
            
            # 判断时间间隔
            time_interval = self._get_time_interval(last_node.timestamp, new_node.timestamp)
            
            # 综合判断
            should_extend = (
                distance < self.distance_threshold and
                visual_similarity > self.coherence_threshold and
                time_interval < 300  # 5分钟内
            )
            
            reason = self._determine_reason(
                distance, visual_similarity, time_interval, should_extend
            )
            
            return {
                "should_extend": should_extend,
                "reason": reason,
                "action": "extend" if should_extend else "create_new",
                "metrics": {
                    "distance": distance,
                    "visual_similarity": visual_similarity,
                    "time_interval": time_interval
                }
            }
            
        except Exception as e:
            logger.error(f"❌ 判断路径扩展失败: {e}")
            return {
                "should_extend": False,
                "reason": "error",
                "action": "create_new"
            }
    
    def create_new_path(self, initial_node, path_name: str = None) -> Optional[str]:
        """
        创建新路径
        
        Args:
            initial_node: 初始节点
            path_name: 路径名称（可选）
            
        Returns:
            Optional[str]: 新路径ID
        """
        try:
            from core.scene_memory_system import SceneNode
            
            # 生成新路径ID
            path_id = f"path_{int(datetime.now().timestamp())}"
            
            if not path_name:
                path_name = f"路径_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # 创建路径
            success = self.scene_memory.memory_mapper.add_path(path_id, path_name)
            
            if success:
                # 添加初始节点
                success = self.scene_memory.memory_mapper.add_node(path_id, initial_node)
                
                if success:
                    logger.info(f"✅ 新路径已创建: {path_id} ({path_name})")
                    return path_id
                else:
                    logger.error("❌ 添加初始节点失败")
                    return None
            else:
                logger.error("❌ 创建路径失败")
                return None
                
        except Exception as e:
            logger.error(f"❌ 创建新路径失败: {e}")
            return None
    
    def extend_existing_path(self, path_id: str, new_node) -> bool:
        """
        扩展现有路径
        
        Args:
            path_id: 路径ID
            new_node: 新节点
            
        Returns:
            bool: 是否成功
        """
        try:
            success = self.scene_memory.memory_mapper.add_node(path_id, new_node)
            
            if success:
                logger.info(f"✅ 路径 {path_id} 已扩展，新增节点: {new_node.label}")
            else:
                logger.error(f"❌ 扩展路径 {path_id} 失败")
            
            return success
            
        except Exception as e:
            logger.error(f"❌ 扩展路径失败: {e}")
            return False
    
    def handle_path_interruption(self, path_id: str, new_node, 
                                user_override: bool = False) -> Dict[str, Any]:
        """
        处理路径中断
        
        Args:
            path_id: 当前路径ID
            new_node: 新节点
            user_override: 用户是否手动重置
            
        Returns:
            Dict: 处理结果
        """
        try:
            # 如果用户明确要求，创建新路径
            if user_override:
                logger.info("用户要求创建新路径")
                new_path_id = self.create_new_path(new_node)
                return {
                    "action": "created_new",
                    "path_id": new_path_id,
                    "message": "已按用户要求创建新路径"
                }
            
            # 自动判断
            decision = self.should_extend_path(path_id, new_node)
            
            if decision["should_extend"]:
                # 扩展现有路径
                success = self.extend_existing_path(path_id, new_node)
                return {
                    "action": "extended",
                    "path_id": path_id,
                    "success": success,
                    "message": "路径已扩展"
                }
            else:
                # 创建新路径
                new_path_id = self.create_new_path(new_node)
                return {
                    "action": "created_new",
                    "path_id": new_path_id,
                    "old_path_id": path_id,
                    "message": decision.get("reason", "路径已中断，创建新路径")
                }
                
        except Exception as e:
            logger.error(f"❌ 处理路径中断失败: {e}")
            return {
                "action": "error",
                "message": str(e)
            }
    
    def _estimate_distance(self, node1, node2) -> float:
        """
        估算两节点距离
        
        Args:
            node1: 节点1
            node2: 节点2
            
        Returns:
            float: 距离（米）
        """
        # 简化实现：基于时间戳差值
        # 实际应该使用GPS或步数数据
        
        try:
            from datetime import datetime
            
            t1 = datetime.fromisoformat(node1.timestamp)
            t2 = datetime.fromisoformat(node2.timestamp)
            
            # 假设步行速度 1 m/s
            time_diff = abs((t2 - t1).total_seconds())
            distance = time_diff * 1.0  # 简化计算
            
            return distance
            
        except Exception:
            return 0.0
    
    def _estimate_visual_similarity(self, node1, node2) -> float:
        """
        估算视觉相似度
        
        Args:
            node1: 节点1
            node2: 节点2
            
        Returns:
            float: 相似度 (0-1)
        """
        # 简化实现：比较标签相似度
        # 实际应该使用图像特征对比
        
        try:
            import difflib
            
            similarity = difflib.SequenceMatcher(None, node1.label, node2.label).ratio()
            return similarity
            
        except Exception:
            return 0.5  # 默认中等相似度
    
    def _get_time_interval(self, timestamp1: str, timestamp2: str) -> float:
        """
        获取时间间隔
        
        Args:
            timestamp1: 时间戳1
            timestamp2: 时间戳2
            
        Returns:
            float: 时间间隔（秒）
        """
        try:
            from datetime import datetime
            
            t1 = datetime.fromisoformat(timestamp1)
            t2 = datetime.fromisoformat(timestamp2)
            
            return abs((t2 - t1).total_seconds())
            
        except Exception:
            return 0.0
    
    def _determine_reason(self, distance: float, similarity: float, 
                         time_interval: float, should_extend: bool) -> str:
        """
        确定决策原因
        
        Args:
            distance: 距离
            similarity: 相似度
            time_interval: 时间间隔
            should_extend: 是否扩展
            
        Returns:
            str: 原因描述
        """
        if should_extend:
            return "路径连续性良好，适合扩展"
        else:
            reasons = []
            
            if distance >= self.distance_threshold:
                reasons.append(f"距离过远({distance:.1f}m)")
            if similarity < self.coherence_threshold:
                reasons.append(f"相似度低({similarity:.2f})")
            if time_interval >= 300:
                reasons.append(f"时间间隔过长({time_interval/60:.1f}分钟)")
            
            return "; ".join(reasons) if reasons else "路径已中断"


if __name__ == "__main__":
    # 测试路径增长管理器
    import logging
    logging.basicConfig(level=logging.INFO)
    
    from core.scene_memory_system import SceneNode
    
    print("=" * 60)
    print("🌱 路径增长管理器测试")
    print("=" * 60)
    
    manager = PathGrowthManager()
    
    # 创建测试节点
    node1 = SceneNode(
        node_id="test_001",
        label="Start",
        image_path="",
        timestamp=datetime.now().isoformat()
    )
    
    node2 = SceneNode(
        node_id="test_002",
        label="Hallway",
        image_path="",
        timestamp=datetime.now().isoformat()
    )
    
    # 测试判断
    print("\n1. 测试路径扩展判断")
    result = manager.should_extend_path("test_hospital_path", node2)
    print(f"   {result}")
    
    # 测试创建新路径
    print("\n2. 测试创建新路径")
    new_path_id = manager.create_new_path(node1, "测试路径")
    print(f"   新路径ID: {new_path_id}")
    
    print("\n" + "=" * 60)


