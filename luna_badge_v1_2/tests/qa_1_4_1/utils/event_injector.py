"""
异常事件注入器
用于测试中模拟各种异常事件
"""
import time
import threading
from typing import List, Callable, Optional

from core.failsafe.health_events import HealthEvent


class EventInjector:
    """
    事件注入器
    
    用于在测试中模拟各种异常事件，验证系统响应
    """
    
    def __init__(self, callback: Optional[Callable[[str], None]] = None):
        """
        初始化事件注入器
        
        Args:
            callback: 事件回调函数（通常是 FailSafeManager.on_health_event）
        """
        self.callback = callback
        self.injected_events: List[tuple[float, str]] = []
        self.running = False
        self._thread: Optional[threading.Thread] = None
    
    def inject(self, event: str) -> None:
        """
        注入单个事件
        
        Args:
            event: 事件类型（HealthEvent 常量）
        """
        if self.callback:
            self.callback(event)
        self.injected_events.append((time.time(), event))
    
    def inject_batch(self, events: List[str], interval: float = 0.1) -> None:
        """
        批量注入事件
        
        Args:
            events: 事件列表
            interval: 事件间隔（秒）
        """
        for event in events:
            self.inject(event)
            time.sleep(interval)
    
    def start_random_injection(
        self,
        duration: float = 60.0,
        interval: float = 1.0,
        event_types: Optional[List[str]] = None
    ) -> None:
        """
        启动随机事件注入（用于压力测试）
        
        Args:
            duration: 持续时间（秒）
            interval: 注入间隔（秒）
            event_types: 可选的事件类型列表，None 表示使用所有类型
        """
        if event_types is None:
            event_types = [
                HealthEvent.CAMERA_STALE,
                HealthEvent.INFER_STALE,
                HealthEvent.HIGH_CPU,
                HealthEvent.HIGH_MEM,
                HealthEvent.THREAD_HANG,
            ]
        
        self.running = True
        
        def _inject_loop():
            start_time = time.time()
            while self.running and (time.time() - start_time) < duration:
                import random
                event = random.choice(event_types)
                self.inject(event)
                time.sleep(interval)
        
        self._thread = threading.Thread(target=_inject_loop, daemon=True)
        self._thread.start()
    
    def stop(self) -> None:
        """停止事件注入"""
        self.running = False
        if self._thread:
            self._thread.join(timeout=2.0)
    
    def get_stats(self) -> dict:
        """获取统计信息"""
        return {
            "injected_count": len(self.injected_events),
            "running": self.running,
        }
















