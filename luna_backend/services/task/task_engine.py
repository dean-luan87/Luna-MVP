"""
后端统一任务链引擎 (v1.2.0)
支持同步/异步任务、顺序执行、记录错误&上报错误码
"""

import asyncio
from typing import Callable, Awaitable, Union, List, Optional
from utils.logger import task_log
from config.error_codes import ERR

TaskType = Union[Callable[[], None], Callable[[], Awaitable[None]]]


class TaskEngine:
    """
    后端统一任务链引擎：
    - 支持同步 / 异步任务
    - 顺序执行
    - 记录错误 & 上报错误码
    """
    
    def __init__(self):
        self._queue: List[TaskType] = []
        self._running = False
    
    def enqueue(self, task: TaskType):
        """入队任务"""
        if not callable(task):
            task_log("ENQUEUE_INVALID", {"error": "task is not callable"}, ERR.TASK_ENQUEUE_FAIL)
            return
        
        self._queue.append(task)
        task_log("ENQUEUE", {"queue_len": len(self._queue)})
        
        if not self._running:
            self._run_loop()
    
    def _run_loop(self):
        """运行任务循环"""
        self._running = True
        
        async def runner():
            while self._queue:
                t = self._queue.pop(0)
                try:
                    if asyncio.iscoroutinefunction(t):
                        await t()
                    else:
                        t()
                except Exception as e:
                    task_log("STEP_ERROR", {
                        "error": str(e),
                    }, ERR.TASK_STEP_ERROR)
            
            self._running = False
        
        # 独立事件循环
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(runner())
            loop.close()
        except Exception as e:
            task_log("LOOP_ERROR", {"error": str(e)}, ERR.TASK_STEP_ERROR)
            self._running = False
    
    def clear(self):
        """清空任务队列"""
        self._queue.clear()
        self._running = False
        task_log("CLEAR", {})
    
    @property
    def running(self) -> bool:
        """是否正在运行"""
        return self._running
    
    @property
    def queue_length(self) -> int:
        """队列长度"""
        return len(self._queue)


# 单例
_task_engine: Optional[TaskEngine] = None

def get_task_engine() -> TaskEngine:
    """获取任务引擎单例"""
    global _task_engine
    if _task_engine is None:
        _task_engine = TaskEngine()
    return _task_engine

# 兼容性：直接导出实例
task_engine = get_task_engine()

