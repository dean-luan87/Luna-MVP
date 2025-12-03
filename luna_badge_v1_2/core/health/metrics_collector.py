"""
指标收集器
提供简单的计数和耗时记录，用于性能监控和故障诊断
"""
import time
from contextlib import contextmanager
from typing import Dict
import logging

# 使用标准 logging，避免循环依赖
logger = logging.getLogger(__name__)


class MetricsCollector:
    """
    指标收集器（单例模式）
    
    提供简单的计数和耗时记录功能
    """
    
    _counters: Dict[str, int] = {}
    _timings: Dict[str, float] = {}
    _counts: Dict[str, int] = {}  # 用于记录 timing 的调用次数

    @classmethod
    def incr(cls, name: str, value: int = 1) -> None:
        """
        增加计数器
        
        Args:
            name: 指标名称
            value: 增加值，默认为 1
        
        Examples:
            >>> MetricsCollector.incr("frames_processed")
            >>> MetricsCollector.incr("errors", 5)
        """
        cls._counters[name] = cls._counters.get(name, 0) + value
        logger.debug(f"Metric '{name}' incremented by {value}")

    @classmethod
    def add_timing(cls, name: str, elapsed: float) -> None:
        """
        添加耗时记录
        
        Args:
            name: 指标名称
            elapsed: 耗时（秒）
        
        Examples:
            >>> MetricsCollector.add_timing("inference", 0.012)
        """
        cls._timings[name] = cls._timings.get(name, 0.0) + elapsed
        cls._counts[name] = cls._counts.get(name, 0) + 1
        logger.debug(f"Metric '{name}' timing added: {elapsed:.4f}s")

    @classmethod
    @contextmanager
    def timeit(cls, name: str):
        """
        上下文管理器，自动记录耗时
        
        Args:
            name: 指标名称
        
        Examples:
            >>> with MetricsCollector.timeit("inference"):
            ...     result = model.predict(frame)
        """
        start = time.perf_counter()
        try:
            yield
        finally:
            elapsed = time.perf_counter() - start
            cls.add_timing(name, elapsed)

    @classmethod
    def snapshot(cls) -> dict:
        """
        获取当前指标快照
        
        Returns:
            包含计数器和耗时信息的字典
        
        Examples:
            >>> metrics = MetricsCollector.snapshot()
            >>> print(metrics["counters"]["frames_processed"])
            >>> print(metrics["timings"]["inference"])
        """
        # 计算平均耗时
        avg_timings = {}
        for name, total in cls._timings.items():
            count = cls._counts.get(name, 1)
            avg_timings[name] = {
                "total": total,
                "count": count,
                "avg": total / count if count > 0 else 0.0
            }

        return {
            "counters": dict(cls._counters),
            "timings": avg_timings,
        }

    @classmethod
    def reset(cls) -> None:
        """重置所有指标"""
        cls._counters.clear()
        cls._timings.clear()
        cls._counts.clear()
        logger.info("MetricsCollector reset")

    @classmethod
    def get_counter(cls, name: str) -> int:
        """
        获取计数器值
        
        Args:
            name: 指标名称
        
        Returns:
            计数器值，如果不存在则返回 0
        """
        return cls._counters.get(name, 0)

    @classmethod
    def get_avg_timing(cls, name: str) -> float:
        """
        获取平均耗时
        
        Args:
            name: 指标名称
        
        Returns:
            平均耗时（秒），如果不存在则返回 0.0
        """
        if name not in cls._timings:
            return 0.0
        count = cls._counts.get(name, 1)
        return cls._timings[name] / count if count > 0 else 0.0

