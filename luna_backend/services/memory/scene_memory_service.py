"""
场景记忆 + 本地地图服务 (v1.2.0)
记录关键节点（门、楼梯、电梯、标识牌等）
维护小范围地图，为导航/任务链提供上下文
"""

from typing import Dict, Any, List, Tuple, Optional
from core.runtime import scene_memory_system, local_map_generator
from utils.logger import scene_log
from config.error_codes import ERR


class SceneMemoryService:
    """
    场景记忆 + 本地地图服务：
    - 记录关键节点（门、楼梯、电梯、标识牌等）
    - 维护小范围地图
    - 为导航 / 任务链提供上下文
    """
    
    def __init__(self):
        """初始化场景记忆服务"""
        pass
    
    def is_ready(self) -> bool:
        """检查服务是否就绪"""
        return scene_memory_system is not None and local_map_generator is not None
    
    def add_node(self, node_type: str, position: Tuple[float, float], meta: Dict[str, Any]):
        """
        添加节点
        
        Args:
            node_type: 节点类型（如 "door", "stairs", "elevator"）
            position: 位置坐标 (x, y)
            meta: 元数据
        """
        if scene_memory_system is None:
            raise RuntimeError(f"场景记忆系统未初始化 (错误码: {ERR.SCENE_NODE_DETECT_FAILED})")
        
        # 尝试调用add_node方法（如果存在）
        if hasattr(scene_memory_system, 'add_node'):
            scene_memory_system.add_node(node_type=node_type, position=position, meta=meta)
        elif hasattr(scene_memory_system, 'record_node'):
            # 兼容record_node方法
            scene_memory_system.record_node(
                image=None,  # 如果没有图像
                path_id=meta.get("path_id", "current"),
                path_name=meta.get("path_name", "未命名路径")
            )
        
        scene_log("ADD_NODE", {
            "node_type": node_type,
            "pos": position,
        })
    
    def get_nodes(self) -> List[Dict[str, Any]]:
        """获取所有节点"""
        if scene_memory_system is None:
            return []
        
        # 尝试导出节点
        if hasattr(scene_memory_system, 'export_nodes'):
            return scene_memory_system.export_nodes()
        elif hasattr(scene_memory_system, 'get_nodes'):
            nodes = scene_memory_system.get_nodes()
            if nodes:
                return [n.to_dict() if hasattr(n, 'to_dict') else str(n) for n in nodes]
        
        return []
    
    def update_pose(self, dx: float, dy: float, angle_delta: float):
        """
        更新位姿
        
        Args:
            dx: x方向位移
            dy: y方向位移
            angle_delta: 角度变化
        """
        if local_map_generator is None:
            raise RuntimeError(f"本地地图生成器未初始化 (错误码: {ERR.VISION_NOT_INITIALIZED})")
        
        local_map_generator.update_position(dx, dy, angle_delta)
        scene_log("UPDATE_POSE", {"dx": dx, "dy": dy, "angle_delta": angle_delta})
    
    def export_map(self) -> Dict[str, Any]:
        """导出地图"""
        if local_map_generator is None:
            return {}
        
        m = local_map_generator.get_map()
        if m:
            if hasattr(m, 'to_dict'):
                return m.to_dict()
            elif isinstance(m, dict):
                return m
            else:
                return {"map": str(m)}
        
        return {}


# 单例
_scene_memory_service: Optional[SceneMemoryService] = None

def get_scene_memory_service() -> SceneMemoryService:
    """获取场景记忆服务单例"""
    global _scene_memory_service
    if _scene_memory_service is None:
        _scene_memory_service = SceneMemoryService()
    return _scene_memory_service

# 兼容性：直接导出实例
scene_memory_service = get_scene_memory_service()



