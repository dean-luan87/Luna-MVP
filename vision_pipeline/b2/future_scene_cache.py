"""
Future Scene Cache - B2 v0.2 缓存逻辑：第二层

未来场景缓存（Future Scene Cache）

核心思想：
B2 不每帧算未来，
而是在"世界变化时"更新一次未来剧本。

何时更新缓存？
只在以下情况之一：
1. WorldSignature 变化（世界指纹变化）
2. TTL 过期（例如 8 秒）

好处：
- 不怕抖动
- 不怕抽帧
- 不怕建模暂时失败
- B2 真正"脱离帧率"
"""

import time
import math
from dataclasses import dataclass
from typing import Optional, Dict, Any, Tuple, Callable
from .future_simulation_result import FutureSimulationResult
from .future_simulator_input import FutureSimulatorInput
from .world_signature import WorldSignature


# Task 2.1: FutureCacheEntry 数据结构
@dataclass
class FutureCacheEntry:
    """FutureCache 条目"""
    signature: str  # WorldSignature digest
    result: FutureSimulationResult
    timestamp: float


class FutureSceneCache:
    """
    B2 v0.2 缓存逻辑：第二层 - 未来场景缓存
    
    Task 2.2: FutureCacheManager
    
    核心职责：
    - 缓存未来预演结果
    - 只在世界变化时更新
    - 提供稳定的未来剧本
    """
    
    # Task 2.3: 固定 TTL（v0.2）
    FUTURE_TTL_SEC = 8.0
    
    def __init__(self, ttl_sec: float = None):
        """
        初始化未来场景缓存
        
        Args:
            ttl_sec: 缓存有效期（秒），默认 8 秒
        """
        self.ttl_sec = ttl_sec or self.FUTURE_TTL_SEC
        self._cache_entry: Optional[FutureCacheEntry] = None
    
    def get_or_compute(
        self,
        world_signature: WorldSignature,
        compute_fn,
        current_ts: float,
    ) -> Tuple[FutureSimulationResult, bool]:
        """
        Task 2.2: get_or_compute 接口
        
        判断是否可复用，管理 TTL，记录命中/重算
        
        Args:
            world_signature: 当前世界指纹
            compute_fn: 计算函数（如果缓存不可用）
            current_ts: 当前时间戳
        
        Returns:
            Tuple[FutureSimulationResult, bool]: (结果, 是否复用)
        """
        # 检查缓存是否可用
        if self._cache_entry is not None:
            # 检查 TTL
            age = current_ts - self._cache_entry.timestamp
            if age < self.ttl_sec:
                # 检查 WorldSignature 是否一致
                if self._cache_entry.signature == world_signature.digest():
                    # 复用缓存
                    print(f"[B2] future_cache=reused age={age:.1f}s")
                    return self._cache_entry.result, True
        
        # 需要重新计算
        result = compute_fn()
        # 更新缓存
        self._cache_entry = FutureCacheEntry(
            signature=world_signature.digest(),
            result=result,
            timestamp=current_ts,
        )
        print(f"[B2] future_cache=expired recompute")
        return result, False

