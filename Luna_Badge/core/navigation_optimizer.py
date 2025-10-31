#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 导航优化器
P1-4: 导航响应时间优化

功能:
- 路径预加载
- 路径缓存
- 并行处理
"""

import logging
import time
from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass, field
from collections import OrderedDict
import threading

logger = logging.getLogger(__name__)


@dataclass
class PathCache:
    """路径缓存项"""
    path: Any
    distance: float
    created_at: float
    access_count: int = 0
    last_access: float = field(default_factory=time.time)


class NavigationOptimizer:
    """
    导航优化器
    
    功能:
    1. 路径预加载
    2. LRU缓存
    3. 并行规划
    4. 响应时间优化
    """
    
    def __init__(self, max_cache_size: int = 100):
        """
        初始化导航优化器
        
        Args:
            max_cache_size: 最大缓存大小
        """
        # 路径缓存
        self.path_cache = OrderedDict()
        self.max_cache_size = max_cache_size
        
        # 预加载标志
        self.preload_enabled = True
        
        # 统计信息
        self.stats = {
            "cache_hits": 0,
            "cache_misses": 0,
            "paths_cached": 0,
            "avg_response_time": 0.0
        }
        
        self.lock = threading.Lock()
        
        logger.info(f"🧭 导航优化器初始化 (max_cache={max_cache_size})")
    
    def get_cached_path(self, 
                       start: str,
                       destination: str,
                       path_planner) -> Optional[Any]:
        """
        获取缓存的路径
        
        Args:
            start: 起点
            destination: 终点
            path_planner: 路径规划器
            
        Returns:
            路径或None
        """
        cache_key = f"{start}_{destination}"
        
        with self.lock:
            if cache_key in self.path_cache:
                # 缓存命中
                cache_item = self.path_cache[cache_key]
                cache_item.access_count += 1
                cache_item.last_access = time.time()
                
                # 移到最前面（LRU）
                self.path_cache.move_to_end(cache_key)
                
                self.stats["cache_hits"] += 1
                logger.debug(f"📦 缓存命中: {cache_key}")
                return cache_item.path
            else:
                self.stats["cache_misses"] += 1
                return None
    
    def cache_path(self,
                  start: str,
                  destination: str,
                  path: Any):
        """
        缓存路径
        
        Args:
            start: 起点
            destination: 终点
            path: 路径对象
        """
        cache_key = f"{start}_{destination}"
        
        with self.lock:
            # 如果超出限制，清理最旧的
            while len(self.path_cache) >= self.max_cache_size:
                self._evict_lru()
            
            # 添加新缓存
            self.path_cache[cache_key] = PathCache(
                path=path,
                distance=0.0,  # 可选的路径距离
                created_at=time.time(),
                access_count=0
            )
            
            self.stats["paths_cached"] += 1
    
    def _evict_lru(self):
        """清理最少使用的项"""
        if self.path_cache:
            self.path_cache.popitem(last=False)
    
    def preload_paths(self,
                     start: str,
                     common_destinations: List[str],
                     path_planner,
                     max_paths: int = 10):
        """
        预加载常用路径
        
        Args:
            start: 起点
            common_destinations: 常用目的地列表
            path_planner: 路径规划器
            max_paths: 最大预加载数量
        """
        if not self.preload_enabled:
            return
        
        logger.info(f"🔄 预加载路径: {start} → {len(common_destinations)}个目的地")
        
        loaded = 0
        for dest in common_destinations[:max_paths]:
            # 检查是否已缓存
            if self.get_cached_path(start, dest, path_planner) is None:
                try:
                    # 规划路径（异步优化）
                    import concurrent.futures
                    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                        future = executor.submit(path_planner.plan_route, start, [dest])
                        # 不等待完成，让它在后台执行
                
                except Exception as e:
                    logger.error(f"❌ 预加载路径失败 {dest}: {e}")
                else:
                    loaded += 1
        
        logger.info(f"✅ 预加载完成: {loaded}个路径")
    
    def optimize_response_time(self,
                              planner_func: Callable,
                              *args,
                              **kwargs) -> Any:
        """
        优化响应时间
        
        Args:
            planner_func: 规划函数
            *args: 参数
            **kwargs: 关键字参数
            
        Returns:
            结果
        """
        start_time = time.time()
        
        try:
            result = planner_func(*args, **kwargs)
            
            # 更新平均响应时间
            response_time = time.time() - start_time
            self._update_avg_response_time(response_time)
            
            return result
            
        except Exception as e:
            logger.error(f"❌ 优化失败: {e}")
            raise
    
    def _update_avg_response_time(self, response_time: float):
        """更新平均响应时间"""
        avg = self.stats["avg_response_time"]
        count = self.stats.get("plan_count", 0)
        count += 1
        self.stats["plan_count"] = count
        
        self.stats["avg_response_time"] = (avg * (count - 1) + response_time) / count
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        total = self.stats["cache_hits"] + self.stats["cache_misses"]
        hit_rate = (self.stats["cache_hits"] / total * 100) if total > 0 else 0
        
        return {
            "cache_size": len(self.path_cache),
            "cache_hits": self.stats["cache_hits"],
            "cache_misses": self.stats["cache_misses"],
            "hit_rate": round(hit_rate, 2),
            "avg_response_time_ms": round(self.stats["avg_response_time"] * 1000, 2)
        }
    
    def clear_cache(self):
        """清空缓存"""
        with self.lock:
            self.path_cache.clear()
            logger.info("🗑️ 路径缓存已清空")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 70)
    print("🧭 导航优化器测试")
    print("=" * 70)
    
    optimizer = NavigationOptimizer(max_cache_size=10)
    
    # 模拟路径对象
    class MockPath:
        def __init__(self, start, dest):
            self.start = start
            self.dest = dest
    
    # 缓存路径
    print("\n1️⃣ 测试路径缓存...")
    for i in range(15):
        path = MockPath("start", f"dest_{i}")
        optimizer.cache_path("start", f"dest_{i}", path)
    
    stats = optimizer.get_stats()
    print(f"   缓存大小: {stats['cache_size']}/{optimizer.max_cache_size}")
    
    # 获取缓存
    print("\n2️⃣ 测试缓存命中...")
    cached = optimizer.get_cached_path("start", "dest_5", None)
    print(f"   缓存结果: {'✅ 命中' if cached else '❌ 未命中'}")
    
    # 统计
    stats = optimizer.get_stats()
    print(f"\n   命中率: {stats['hit_rate']}%")
    print(f"   平均响应时间: {stats['avg_response_time_ms']}ms")
    
    print("\n" + "=" * 70)

