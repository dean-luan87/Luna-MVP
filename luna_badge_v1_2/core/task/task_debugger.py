# task_debugger.py

from typing import Optional, Dict, Any


class TaskDebugger:
    """
    任务调试器：可视化任务引擎状态
    """
    
    def __init__(self, engine, map_manager=None):
        self.engine = engine
        self.map_manager = map_manager
    
    def print_tree(self):
        """
        打印任务树（ASCII 格式）
        """
        print("\n" + "=" * 50)
        print("TaskEngine State:")
        print("=" * 50)
        
        # 主任务
        print(f"  MAIN: {self._ctx_str(self.engine.main_task)}")
        
        # 插入任务栈
        print("\n  INSERT STACK:")
        if self.engine.stack:
            for i, ctx in enumerate(reversed(self.engine.stack)):
                print(f"    [{i}] {self._ctx_str(ctx)}")
        else:
            print("    (empty)")
        
        # 当前任务
        print(f"\n  CURRENT: {self._ctx_str(self.engine.current_task)}")
        
        # 强制任务
        print(f"  FORCE: {self._ctx_str(self.engine.forced_task)}")
        
        # 地图状态
        if self.map_manager:
            print(f"\n  MAP: {self.map_manager.scene_id or 'None'} nodes={len(self.map_manager.current_map)}")
        else:
            print("\n  MAP: None")
        
        print("=" * 50 + "\n")
    
    def get_status_json(self) -> Dict[str, Any]:
        """
        获取任务状态 JSON（供后台 API 使用）
        """
        return {
            "main_task": self._ctx_to_dict(self.engine.main_task),
            "current_task": self._ctx_to_dict(self.engine.current_task),
            "stack": [self._ctx_to_dict(ctx) for ctx in self.engine.stack],
            "forced_task": self._ctx_to_dict(self.engine.forced_task),
            "map": {
                "scene_id": self.map_manager.scene_id if self.map_manager else None,
                "node_count": len(self.map_manager.current_map) if self.map_manager else 0
            } if self.map_manager else None
        }
    
    def _ctx_str(self, ctx) -> str:
        """
        格式化任务上下文为字符串
        """
        if ctx is None:
            return "None"
        
        node_index = 0
        if hasattr(ctx, 'chain') and ctx.chain:
            if hasattr(ctx.chain, 'current_node'):
                node_index = ctx.chain.current_node
            elif hasattr(ctx.chain, 'node_index'):
                node_index = ctx.chain.node_index
        
        return f"{ctx.task_id} ({ctx.state}) type={ctx.task_type} node={node_index}"
    
    def _ctx_to_dict(self, ctx) -> Optional[Dict[str, Any]]:
        """
        将任务上下文转换为字典
        """
        if ctx is None:
            return None
        
        node_index = 0
        if hasattr(ctx, 'chain') and ctx.chain:
            if hasattr(ctx.chain, 'current_node'):
                node_index = ctx.chain.current_node
            elif hasattr(ctx.chain, 'node_index'):
                node_index = ctx.chain.node_index
        
        return {
            "task_id": ctx.task_id,
            "task_type": ctx.task_type,
            "state": ctx.state,
            "node_index": node_index
        }










