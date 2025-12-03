from core.logging import get_logger

#!/usr/bin/env python3
log = get_logger("resource_monitor")
"""
资源监控模块 v1.0
Resource Monitor - CPU / 内存 + LEAK 检测
"""

import time
import threading
from collections import deque
from typing import Callable, Deque, Optional

try:
    import psutil
except ImportError:
    psutil = None

try:
    from core.telemetry import log_event, build_event
except ImportError:
    # 兜底，避免在早期阶段崩
    import time as _time

    def log_event(evt: dict):
        log.info("[telemetry-fallback]", evt")

    def build_event(event_type: str, data: dict):
        d = {"ts": _time.time(), "type": event_type}
        d.update(data)
        return d


class ResourceMonitor:
    """
    轻量级资源监控：
    - 周期性采样 CPU / MEM
    - 检测 CPU_HIGH
    - 检测 MEMORY_LEAK（简单基线 + 漂移）
    """
    
    def __init__(
        self,
        poll_interval_sec: float = 5.0,
        cpu_high_threshold: float = 90.0,
        mem_high_threshold: float = 85.0,
        leak_window_sec: float = 300.0,
        cpu_provider: Optional[Callable[[], float]] = None,
        mem_provider: Optional[Callable[[], float]] = None,
        event_sink: Optional[Callable[[dict], None]] = None,
    ):
        """
        初始化资源监控器
        
        Args:
            poll_interval_sec: 采样间隔（秒）
            cpu_high_threshold: CPU 高阈值（%）
            mem_high_threshold: 内存高阈值（%）
            leak_window_sec: 内存泄漏检测窗口（秒）
            cpu_provider: CPU 数据提供函数
            mem_provider: 内存数据提供函数
            event_sink: 事件输出函数
        """
        self.poll_interval_sec = poll_interval_sec
        self.cpu_high_threshold = cpu_high_threshold
        self.mem_high_threshold = mem_high_threshold
        self.leak_window_sec = leak_window_sec
        
        self.cpu_provider = cpu_provider or self._default_cpu_provider
        self.mem_provider = mem_provider or self._default_mem_provider
        self.event_sink = event_sink or log_event
        
        # 用于 CPU_HIGH 判定
        self.cpu_window: Deque[float] = deque(maxlen=12)  # ~1 分钟窗口（5s*12）
        
        # 用于 MEMORY_LEAK 判定
        self.mem_window: Deque[tuple] = deque(maxlen=60)  # (ts, mem%)
        self._thread: Optional[threading.Thread] = None
        self._running = False
    
    # ========= 对外接口 =========
    
    def start(self, daemon: bool = True):
        """启动资源监控"""
        if self._thread and self._thread.is_alive():
            return
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=daemon)
        self._thread.start()
    
    def stop(self):
        """停止资源监控"""
        self._running = False
    
    # ========= 主循环 =========
    
    def _loop(self):
        """监控循环"""
        while self._running:
            try:
                self.sample_once()
            except Exception:
                # 监控不能弄挂主流程
                pass
            time.sleep(self.poll_interval_sec)
    
    # ========= 采样与检测 =========
    
    def sample_once(self):
        """执行一次采样"""
        ts = time.time()
        cpu = float(self.cpu_provider())
        mem = float(self.mem_provider())
        
        # 记录 resource 档位
        self._emit(build_event("resource", {"cpu": cpu, "mem": mem}))
        
        # --- CPU HIGH ---
        self.cpu_window.append(cpu)
        self._check_cpu_high(ts)
        
        # --- MEMORY LEAK ---
        self.mem_window.append((ts, mem))
        self._check_memory_leak(ts)
    
    def _check_cpu_high(self, ts: float):
        """检查 CPU 是否过高"""
        if len(self.cpu_window) < 3:
            return
        # 最近 3 次都超过阈值 → CPU_HIGH
        recent = list(self.cpu_window)[-3:]
        if all(v >= self.cpu_high_threshold for v in recent):
            evt = build_event(
                "error",
                {
                    "domain": "system.cpu",
                    "code": "CPU_HIGH",
                    "msg": "CPU usage high over window",
                    "values": list(self.cpu_window),
                    "severity": 2,
                },
            )
            self._emit(evt)
            # 清空窗口，避免连续刷
            self.cpu_window.clear()
    
    def _check_memory_leak(self, now: float):
        """检查内存泄漏"""
        if len(self.mem_window) < 5:
            return
        
        # 过滤出 leak_window_sec 内的样本
        recent = [(t, m) for (t, m) in self.mem_window if now - t <= self.leak_window_sec]
        if len(recent) < 5:
            return
        
        # 基线：前 20% 样本均值
        n_base = max(1, len(recent) // 5)
        baseline = sum(m for (_, m) in recent[:n_base]) / n_base
        current = recent[-1][1]
        
        # 漂移条件：当前值明显高于基线，且超过绝对阈值
        if baseline <= 0:
            return
        
        if current >= self.mem_high_threshold and current >= baseline * 1.5:
            evt = build_event(
                "error",
                {
                    "domain": "system.mem",
                    "code": "MEMORY_LEAK",
                    "msg": "memory usage drift upwards",
                    "baseline": baseline,
                    "current": current,
                    "severity": 3,
                },
            )
            self._emit(evt)
            # 防抖：清空窗口，等待下一轮重新观察
            self.mem_window.clear()
    
    # ========= 默认 provider =========
    
    @staticmethod
    def _default_cpu_provider() -> float:
        """默认 CPU 提供函数"""
        if psutil is None:
            return 0.0
        # interval=0 非阻塞，返回上一次的计算结果
        return float(psutil.cpu_percent(interval=0.0))
    
    @staticmethod
    def _default_mem_provider() -> float:
        """默认内存提供函数"""
        if psutil is None:
            return 0.0
        return float(psutil.virtual_memory().percent)
    
    # ========= 事件输出 =========
    
    def _emit(self, event: dict):
        """输出事件"""
        try:
            self.event_sink(event)
        except Exception:
            # 观测出问题不影响主流程
            pass


# 提供一个全局启动入口（给 main 调用）
_global_resource_monitor: Optional[ResourceMonitor] = None


def start_global_resource_monitor(
    poll_interval_sec: float = 5.0,
    cpu_high_threshold: float = 90.0,
    mem_high_threshold: float = 85.0
) -> ResourceMonitor:
    """
    启动全局资源监控器
    
    Args:
        poll_interval_sec: 采样间隔（秒）
        cpu_high_threshold: CPU 高阈值（%）
        mem_high_threshold: 内存高阈值（%）
    
    Returns:
        ResourceMonitor 实例
    """
    global _global_resource_monitor
    if _global_resource_monitor is None:
        _global_resource_monitor = ResourceMonitor(
            poll_interval_sec=poll_interval_sec,
            cpu_high_threshold=cpu_high_threshold,
            mem_high_threshold=mem_high_threshold
        )
        _global_resource_monitor.start()
    return _global_resource_monitor


if __name__ == "__main__":
    # 简单自测
    m = start_global_resource_monitor()
    log.info("[ResourceMonitor] Started, press Ctrl+C to stop")
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        log.info("\n[ResourceMonitor] Stopped")

