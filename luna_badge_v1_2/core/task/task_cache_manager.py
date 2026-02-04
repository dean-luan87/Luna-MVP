# task_cache_manager.py

import json
import time
import os
from typing import Optional, Dict, Any
from core.logging import get_logger



log = get_logger("task_cache_manager")
class TaskCacheManager:
    """
    任务缓存管理器：持久化任务状态，支持崩溃恢复
    """
    
    DEFAULT_FILE = "data/task_cache.json"
    
    def __init__(self, cache_file: Optional[str] = None):
        self.cache_file = cache_file or self.DEFAULT_FILE
        # 确保目录存在
        os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
    
    def save(self, engine, map_manager=None):
        """
        保存任务引擎状态到缓存文件
        """
        data = {
            "timestamp": int(time.time()),
            "main_task": self._ctx_to_dict(engine.main_task),
            "current_task": self._ctx_to_dict(engine.current_task),
            "stack": [self._ctx_to_dict(t) for t in engine.stack],
            "forced_task": self._ctx_to_dict(engine.forced_task),
            "map_scene_id": map_manager.scene_id if map_manager else None,
            "map_last_node_index": len(map_manager.current_map) if map_manager else 0
        }
        
        try:
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            log.info(f"[TaskCacheManager] Saved state to {self.cache_file}")
        except Exception as e:
            log.error(f"[TaskCacheManager] Failed to save: {e}")
    
    def load(self) -> Optional[Dict[str, Any]]:
        """
        从缓存文件加载任务状态
        """
        try:
            if not os.path.exists(self.cache_file):
                return None
            
            with open(self.cache_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            log.info(f"[TaskCacheManager] Loaded state from {self.cache_file}")
            return data
        except Exception as e:
            log.error(f"[TaskCacheManager] Failed to load: {e}")
            return None
    
    def clear(self):
        """
        清除缓存文件
        """
        try:
            if os.path.exists(self.cache_file):
                os.remove(self.cache_file)
                log.info(f"[TaskCacheManager] Cleared cache file")
        except Exception as e:
            log.error(f"[TaskCacheManager] Failed to clear: {e}")
    
    @staticmethod
    def _ctx_to_dict(ctx):
        """
        将 TaskContext 转换为字典
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

























