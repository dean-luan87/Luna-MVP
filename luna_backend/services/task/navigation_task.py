"""
导航任务 (NavigationTask) v1.2.0
将导航策略系统接入TaskChain，让导航成为可恢复任务
"""

from typing import Dict, Any, Optional
from .task_engine import TaskEngine, TaskType

# 延迟导入以避免循环依赖
def _get_logger():
    try:
        from luna_backend.utils.logger import system_log
        return system_log
    except ImportError:
        try:
            from utils.logger import system_log
            return system_log
        except ImportError:
            def _dummy_log(tag, extra):
                pass
            return _dummy_log


class NavigationTask:
    """
    导航任务
    
    将导航策略系统封装为TaskChain可执行的任务
    """
    
    TASK_NAME = "NAVIGATION_TASK"
    
    def __init__(self):
        """初始化导航任务"""
        try:
            from luna_backend.services.navigation.navigation_manager_v3 import NavigationManager
        except ImportError:
            try:
                from services.navigation.navigation_manager_v3 import NavigationManager
            except ImportError:
                NavigationManager = None
        
        if NavigationManager is None:
            raise RuntimeError("NavigationManager未找到")
        
        self.nav = NavigationManager()
        self._finished = False
        self._result = None
    
    def update_sensors(self, obs: Dict[str, Any]):
        """
        更新传感器数据（观察数据）
        
        Args:
            obs: 观察数据字典
        """
        self.nav.update_observation(obs)
    
    def run_step(self) -> Dict[str, Any]:
        """
        执行一步导航任务
        
        Returns:
            任务执行结果字典
        """
        system_log = _get_logger()
        
        try:
            result = self.nav.run_step()
            
            system_log("TASK:NAVIGATION_STEP", {
                "action": result.get("action"),
                "strategy": result.get("strategy"),
                "text": result.get("text"),
            })
            
            # 完成绕行/纠偏 → 返回主任务
            if result.get("action") == "RESUME_MAIN_TASK":
                self._finished = True
                self._result = result
                return {
                    "finished": True,
                    "result": result,
                    "message": "导航任务完成，返回主任务"
                }
            
            # 如果策略返回完成信号
            if result.get("action") == "COMPLETE" or result.get("action") == "ARRIVED":
                self._finished = True
                self._result = result
                return {
                    "finished": True,
                    "result": result,
                    "message": "导航任务完成"
                }
            
            return {
                "finished": False,
                "result": result,
                "message": "导航任务进行中"
            }
        
        except Exception as e:
            system_log("TASK:NAVIGATION_ERROR", {
                "error": str(e),
            })
            return {
                "finished": False,
                "error": str(e),
                "result": None
            }
    
    def is_finished(self) -> bool:
        """
        检查任务是否完成
        
        Returns:
            是否完成
        """
        return self._finished
    
    def get_result(self) -> Optional[Dict[str, Any]]:
        """
        获取任务结果
        
        Returns:
            任务结果字典
        """
        return self._result
    
    def reset(self):
        """重置任务状态"""
        self._finished = False
        self._result = None
        self.nav.reset()


# 任务注册函数（供TaskChainManager使用）
def create_navigation_task() -> NavigationTask:
    """
    创建导航任务实例
    
    Returns:
        NavigationTask实例
    """
    return NavigationTask()


# 任务映射（供TaskChainManager注册）
TASK_MAP = {
    "NAVIGATION_TASK": NavigationTask,
    "NAVIGATION": NavigationTask,  # 别名
}



