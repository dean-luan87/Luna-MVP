#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 性能优化系统
P1-4: 性能优化

功能:
- 异步图像处理管道
- 图像缓存机制
- 性能监控
- YOLO推理优化
"""

import logging
import time
import threading
import queue
from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass, field
from datetime import datetime
from collections import OrderedDict
import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class PerformanceMetric:
    """性能指标"""
    name: str
    value: float
    timestamp: float
    unit: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


class ImageCache:
    """
    图像缓存
    使用LRU策略管理缓存
    """
    
    def __init__(self, max_size: int = 100, max_memory_mb: int = 500):
        """
        初始化图像缓存
        
        Args:
            max_size: 最大缓存数量
            max_memory_mb: 最大内存（MB）
        """
        self.cache = OrderedDict()
        self.max_size = max_size
        self.max_memory_mb = max_memory_mb
        self.current_memory_mb = 0
        self.hits = 0
        self.misses = 0
        self.lock = threading.Lock()
        
        logger.info(f"🗄️ 图像缓存初始化 (max_size={max_size}, max_memory={max_memory_mb}MB)")
    
    def get(self, key: str) -> Optional[np.ndarray]:
        """
        获取缓存的图像
        
        Args:
            key: 缓存键
            
        Returns:
            图像或None
        """
        with self.lock:
            if key in self.cache:
                # 移到最前面（LRU）
                self.cache.move_to_end(key)
                self.hits += 1
                return self.cache[key]
            else:
                self.misses += 1
                return None
    
    def put(self, key: str, image: np.ndarray):
        """
        缓存图像
        
        Args:
            key: 缓存键
            image: 图像数据
        """
        with self.lock:
            # 如果已存在，先移除
            if key in self.cache:
                self._remove_key(key)
            
            # 计算内存占用
            image_mb = image.nbytes / (1024 * 1024)
            
            # 如果超出内存限制，清理
            while (self.current_memory_mb + image_mb > self.max_memory_mb and 
                   len(self.cache) > 0):
                self._evict_lru()
            
            # 如果超出数量限制，清理
            while len(self.cache) >= self.max_size:
                self._evict_lru()
            
            # 添加新项（只缓存numpy数组）
            if isinstance(image, np.ndarray):
                self.cache[key] = image
                self.current_memory_mb += image_mb
                self.cache.move_to_end(key)
    
    def _remove_key(self, key: str):
        """移除缓存项"""
        if key in self.cache:
            image = self.cache.pop(key)
            if isinstance(image, np.ndarray):
                self.current_memory_mb -= image.nbytes / (1024 * 1024)
    
    def _evict_lru(self):
        """清理最少使用的项"""
        if self.cache:
            key, image = self.cache.popitem(last=False)
            if isinstance(image, np.ndarray):
                self.current_memory_mb -= image.nbytes / (1024 * 1024)
    
    def clear(self):
        """清空缓存"""
        with self.lock:
            self.cache.clear()
            self.current_memory_mb = 0
    
    def get_stats(self) -> Dict[str, Any]:
        """获取缓存统计"""
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        
        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "memory_mb": round(self.current_memory_mb, 2),
            "max_memory_mb": self.max_memory_mb,
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": round(hit_rate, 2)
        }


class AsyncImageProcessor:
    """
    异步图像处理管道
    
    功能:
    - 异步处理图像
    - 队列管理
    - 线程池处理
    """
    
    def __init__(self, 
                 max_queue_size: int = 10,
                 worker_count: int = 2,
                 cache: Optional[ImageCache] = None):
        """
        初始化异步图像处理器
        
        Args:
            max_queue_size: 最大队列大小
            worker_count: 工作线程数
            cache: 图像缓存
        """
        self.request_queue = queue.Queue(maxsize=max_queue_size)
        self.result_map = {}
        self.workers = []
        self.worker_count = worker_count
        self.running = False
        self.processors = {}  # {name: processor_func}
        self.cache = cache or ImageCache()
        self.lock = threading.Lock()
        
        # 统计信息
        self.stats = {
            "requests_received": 0,
            "requests_processed": 0,
            "requests_dropped": 0,
            "avg_processing_time": 0.0
        }
        
        logger.info(f"⚡ 异步图像处理器初始化 (workers={worker_count}, queue={max_queue_size})")
    
    def register_processor(self, name: str, processor_func: Callable):
        """
        注册处理器
        
        Args:
            name: 处理器名称
            processor_func: 处理函数
        """
        self.processors[name] = processor_func
        logger.debug(f"📦 注册处理器: {name}")
    
    def process_async(self, 
                     request_id: str,
                     image: np.ndarray,
                     processor_name: str,
                     timeout: float = 10.0) -> Optional[Any]:
        """
        异步处理图像
        
        Args:
            request_id: 请求ID
            image: 图像数据
            processor_name: 处理器名称
            timeout: 超时时间（秒）
            
        Returns:
            处理结果或None
        """
        if processor_name not in self.processors:
            logger.error(f"❌ 未知处理器: {processor_name}")
            return None
        
        # 尝试从缓存获取（仅对图像结果缓存）
        cache_key = f"{request_id}_{processor_name}"
        cached_result = None  # 简化缓存逻辑，后续可按需扩展
        
        try:
            # 添加到请求队列
            self.request_queue.put_nowait({
                "request_id": request_id,
                "image": image,
                "processor_name": processor_name,
                "cache_key": cache_key
            })
            
            # 等待结果
            start_time = time.time()
            while time.time() - start_time < timeout:
                with self.lock:
                    if request_id in self.result_map:
                        result = self.result_map.pop(request_id)
                        return result
                
                time.sleep(0.01)
            
            logger.warning(f"⏱️ 处理超时: {request_id}")
            return None
            
        except queue.Full:
            self.stats["requests_dropped"] += 1
            logger.error(f"❌ 队列已满，丢弃请求: {request_id}")
            return None
    
    def start(self):
        """启动处理器"""
        if self.running:
            return
        
        self.running = True
        
        # 创建工作线程
        for i in range(self.worker_count):
            worker = threading.Thread(target=self._worker_loop, daemon=True)
            worker.start()
            self.workers.append(worker)
        
        logger.info(f"⚡ 异步图像处理器已启动 (workers={self.worker_count})")
    
    def stop(self):
        """停止处理器"""
        self.running = False
        
        # 等待工作线程完成
        for worker in self.workers:
            worker.join(timeout=2.0)
        
        logger.info("⚡ 异步图像处理器已停止")
    
    def _worker_loop(self):
        """工作线程循环"""
        while self.running:
            try:
                # 从队列获取请求
                request = self.request_queue.get(timeout=1.0)
                
                start_time = time.time()
                
                # 处理图像
                processor = self.processors[request["processor_name"]]
                result = processor(request["image"])
                
                # 存储结果
                with self.lock:
                    self.result_map[request["request_id"]] = result
                
                # 更新统计
                processing_time = time.time() - start_time
                self._update_stats(processing_time)
                
                # 缓存numpy数组结果
                if isinstance(result, np.ndarray):
                    self.cache.put(request["cache_key"], result)
                
                self.request_queue.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"❌ 处理失败: {e}")
    
    def _update_stats(self, processing_time: float):
        """更新统计信息"""
        self.stats["requests_processed"] += 1
        
        # 计算平均处理时间（移动平均）
        avg_time = self.stats["avg_processing_time"]
        count = self.stats["requests_processed"]
        self.stats["avg_processing_time"] = (avg_time * (count - 1) + processing_time) / count
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            **self.stats,
            "queue_size": self.request_queue.qsize(),
            "cache_stats": self.cache.get_stats()
        }


class PerformanceMonitor:
    """
    性能监控器
    
    功能:
    - 收集性能指标
    - 实时监控
    - 性能报告
    """
    
    def __init__(self, max_history: int = 1000):
        """
        初始化性能监控器
        
        Args:
            max_history: 最大历史记录数
        """
        self.metrics: List[PerformanceMetric] = []
        self.max_history = max_history
        self.active_monitors = {}
        self.lock = threading.Lock()
        
        logger.info("📊 性能监控器初始化完成")
    
    def record_metric(self, 
                     name: str,
                     value: float,
                     unit: str = "",
                     metadata: Dict[str, Any] = None):
        """
        记录性能指标
        
        Args:
            name: 指标名称
            value: 指标值
            unit: 单位
            metadata: 元数据
        """
        metric = PerformanceMetric(
            name=name,
            value=value,
            timestamp=time.time(),
            unit=unit,
            metadata=metadata or {}
        )
        
        with self.lock:
            self.metrics.append(metric)
            
            # 限制历史记录
            if len(self.metrics) > self.max_history:
                self.metrics.pop(0)
    
    def start_monitor(self, name: str) -> Callable:
        """
        启动监控（上下文管理器）
        
        Args:
            name: 监控名称
            
        Returns:
            停止函数
        """
        start_time = time.time()
        self.active_monitors[name] = start_time
        
        def stop_monitor(*metadata):
            if name in self.active_monitors:
                duration = time.time() - self.active_monitors[name]
                self.record_metric(f"{name}_duration", duration, "s", metadata[0] if metadata else {})
                del self.active_monitors[name]
        
        return stop_monitor
    
    def get_metrics(self, 
                   name: Optional[str] = None,
                   count: int = 100) -> List[PerformanceMetric]:
        """
        获取指标
        
        Args:
            name: 指标名称（None表示所有）
            count: 数量
            
        Returns:
            指标列表
        """
        with self.lock:
            if name:
                metrics = [m for m in self.metrics if m.name == name]
            else:
                metrics = self.metrics
            
            return metrics[-count:]
    
    def get_summary(self) -> Dict[str, Any]:
        """
        获取性能摘要
        
        Returns:
            性能摘要
        """
        with self.lock:
            summary = {}
            
            for metric in self.metrics[-100:]:  # 最近100个
                if metric.name not in summary:
                    summary[metric.name] = {
                        "min": metric.value,
                        "max": metric.value,
                        "count": 0,
                        "sum": 0.0
                    }
                
                stats = summary[metric.name]
                stats["count"] += 1
                stats["sum"] += metric.value
                stats["min"] = min(stats["min"], metric.value)
                stats["max"] = max(stats["max"], metric.value)
            
            # 计算平均值
            for name, stats in summary.items():
                stats["avg"] = stats["sum"] / stats["count"]
            
            return summary
    
    def clear(self):
        """清空所有指标"""
        with self.lock:
            self.metrics.clear()


# 全局性能优化器实例
_global_performance_optimizer = None


def get_performance_optimizer() -> Dict[str, Any]:
    """获取全局性能优化器组件"""
    global _global_performance_optimizer
    
    if _global_performance_optimizer is None:
        _global_performance_optimizer = {
            "cache": ImageCache(),
            "processor": AsyncImageProcessor(),
            "monitor": PerformanceMonitor()
        }
    
    return _global_performance_optimizer


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 70)
    print("⚡ 性能优化系统测试")
    print("=" * 70)
    
    # 测试图像缓存
    print("\n1️⃣ 测试图像缓存...")
    cache = ImageCache(max_size=10, max_memory_mb=10)
    
    for i in range(15):
        img = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        cache.put(f"image_{i}", img)
    
    stats = cache.get_stats()
    print(f"   缓存大小: {stats['size']}/{stats['max_size']}")
    print(f"   命中率: {stats['hit_rate']}%")
    
    # 测试性能监控
    print("\n2️⃣ 测试性能监控...")
    monitor = PerformanceMonitor()
    
    stop = monitor.start_monitor("test_operation")
    time.sleep(0.1)
    stop()
    
    summary = monitor.get_summary()
    if "test_operation_duration" in summary:
        duration = summary["test_operation_duration"]
        print(f"   测试操作平均耗时: {duration['avg']:.3f}s")
    
    # 测试异步处理器
    print("\n3️⃣ 测试异步处理器...")
    processor = AsyncImageProcessor(worker_count=2)
    
    def test_processor(image):
        # 模拟处理
        time.sleep(0.05)
        return {"processed": True}
    
    processor.register_processor("test", test_processor)
    processor.start()
    
    # 提交任务
    result = processor.process_async("test_1", np.zeros((100, 100)), "test")
    print(f"   处理结果: {'✅ 成功' if result else '❌ 失败'}")
    
    processor.stop()
    
    # 获取统计
    stats = processor.get_stats()
    print(f"   处理统计: {stats}")
    
    print("\n" + "=" * 70)
    print("✅ 测试完成")

