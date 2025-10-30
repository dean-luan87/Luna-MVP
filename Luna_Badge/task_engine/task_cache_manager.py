#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Luna Badge v1.4 - 任务缓存管理器
管理任务执行过程中的中间缓存状态、参数、输出数据，控制生命周期，适配低资源场景
"""

import logging
import time
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)


@dataclass
class CacheEntry:
    """缓存条目"""
    key: str
    value: Any
    created_at: str
    expires_at: str
    access_count: int = 0
    last_accessed: Optional[str] = None
    
    def __post_init__(self):
        if not self.last_accessed:
            self.last_accessed = self.created_at
    
    def is_expired(self) -> bool:
        """检查是否过期"""
        try:
            expires_time = datetime.fromisoformat(self.expires_at)
            return datetime.now() > expires_time
        except:
            return False
    
    def touch(self):
        """更新访问信息"""
        self.access_count += 1
        self.last_accessed = datetime.now().isoformat()


class TaskCacheManager:
    """任务缓存管理器"""
    
    def __init__(self, default_ttl: int = 600, max_size: int = 1000):
        """
        初始化缓存管理器
        
        Args:
            default_ttl: 默认过期时间（秒）
            max_size: 最大缓存条目数
        """
        self.cache: Dict[str, CacheEntry] = {}  # key -> CacheEntry
        self.snapshots: Dict[str, Dict[str, CacheEntry]] = {}  # snapshot_id -> {key: CacheEntry}
        self.default_ttl = default_ttl
        self.max_size = max_size
        self.logger = logging.getLogger("TaskCacheManager")
        
        self.logger.info(f"🚀 TaskCacheManager 初始化 (default_ttl={default_ttl}s, max_size={max_size})")
    
    def set_cache(self, key: str, value: Any, ttl: int = None) -> bool:
        """
        设置缓存
        
        Args:
            key: 缓存键
            value: 缓存值
            ttl: 过期时间（秒），默认使用 default_ttl
            
        Returns:
            bool: 是否成功设置
        """
        if ttl is None:
            ttl = self.default_ttl
        
        # 检查缓存大小
        if len(self.cache) >= self.max_size and key not in self.cache:
            # 清理过期缓存
            self.clear_expired_cache()
            
            # 如果还是满了，删除最旧的
            if len(self.cache) >= self.max_size:
                self._remove_oldest()
        
        # 计算过期时间
        created_at = datetime.now().isoformat()
        expires_at = (datetime.now() + timedelta(seconds=ttl)).isoformat()
        
        # 创建缓存条目
        entry = CacheEntry(
            key=key,
            value=value,
            created_at=created_at,
            expires_at=expires_at
        )
        
        self.cache[key] = entry
        self.logger.debug(f"💾 缓存已设置: {key} (ttl={ttl}s)")
        
        return True
    
    def get_cache(self, key: str, default: Any = None) -> Any:
        """
        获取缓存
        
        Args:
            key: 缓存键
            default: 默认值（如果不存在或过期）
            
        Returns:
            缓存值，如果不存在或过期返回default
        """
        if key not in self.cache:
            return default
        
        entry = self.cache[key]
        
        # 检查是否过期
        if entry.is_expired():
            del self.cache[key]
            self.logger.debug(f"⏰ 缓存已过期: {key}")
            return default
        
        # 更新访问信息
        entry.touch()
        
        return entry.value
    
    def has_cache(self, key: str) -> bool:
        """
        检查缓存是否存在且未过期
        
        Args:
            key: 缓存键
            
        Returns:
            bool: 是否存在且未过期
        """
        if key not in self.cache:
            return False
        
        entry = self.cache[key]
        if entry.is_expired():
            del self.cache[key]
            return False
        
        return True
    
    def clear_cache(self, key: str) -> bool:
        """
        清除特定缓存
        
        Args:
            key: 缓存键
            
        Returns:
            bool: 是否成功清除
        """
        if key in self.cache:
            del self.cache[key]
            self.logger.debug(f"🗑️ 缓存已清除: {key}")
            return True
        return False
    
    def clear_expired_cache(self) -> int:
        """
        清除所有过期缓存
        
        Returns:
            int: 清除的数量
        """
        expired_keys = []
        
        for key, entry in self.cache.items():
            if entry.is_expired():
                expired_keys.append(key)
        
        for key in expired_keys:
            del self.cache[key]
        
        if expired_keys:
            self.logger.info(f"🧹 清除了 {len(expired_keys)} 个过期缓存")
        
        return len(expired_keys)
    
    def snapshot_current_state(self, snapshot_id: str, prefix: str = "") -> int:
        """
        快照当前缓存状态（用于插入任务）
        
        Args:
            snapshot_id: 快照ID
            prefix: 键前缀（用于筛选）
            
        Returns:
            int: 快照的缓存条目数
        """
        snapshot = {}
        
        for key, entry in self.cache.items():
            if not prefix or key.startswith(prefix):
                # 创建新条目副本
                snapshot[key] = CacheEntry(
                    key=entry.key,
                    value=entry.value,
                    created_at=entry.created_at,
                    expires_at=entry.expires_at,
                    access_count=entry.access_count,
                    last_accessed=entry.last_accessed
                )
        
        self.snapshots[snapshot_id] = snapshot
        
        self.logger.info(f"📸 快照已创建: {snapshot_id} ({len(snapshot)}个条目)")
        
        return len(snapshot)
    
    def restore_from_snapshot(self, snapshot_id: str) -> int:
        """
        从快照恢复缓存状态
        
        Args:
            snapshot_id: 快照ID
            
        Returns:
            int: 恢复的缓存条目数
        """
        if snapshot_id not in self.snapshots:
            self.logger.warning(f"⚠️ 快照不存在: {snapshot_id}")
            return 0
        
        snapshot = self.snapshots[snapshot_id]
        
        # 恢复快照中的缓存
        restored_count = 0
        for key, entry in snapshot.items():
            # 只恢复未过期的条目
            if not entry.is_expired():
                self.cache[key] = entry
                restored_count += 1
        
        self.logger.info(f"🔄 快照已恢复: {snapshot_id} ({restored_count}个条目)")
        
        return restored_count
    
    def clear_snapshot(self, snapshot_id: str) -> bool:
        """
        清除快照
        
        Args:
            snapshot_id: 快照ID
            
        Returns:
            bool: 是否成功清除
        """
        if snapshot_id in self.snapshots:
            del self.snapshots[snapshot_id]
            self.logger.debug(f"🗑️ 快照已清除: {snapshot_id}")
            return True
        return False
    
    def clear_all_cache(self):
        """清除所有缓存"""
        count = len(self.cache)
        self.cache.clear()
        self.logger.info(f"🧹 所有缓存已清除 ({count}个条目)")
    
    def clear_all_snapshots(self):
        """清除所有快照"""
        count = len(self.snapshots)
        self.snapshots.clear()
        self.logger.info(f"🧹 所有快照已清除 ({count}个快照)")
    
    def _remove_oldest(self):
        """移除最旧的缓存条目（LRU策略）"""
        if not self.cache:
            return
        
        # 按最后访问时间排序
        sorted_entries = sorted(
            self.cache.items(),
            key=lambda x: x[1].last_accessed or ""
        )
        
        oldest_key = sorted_entries[0][0]
        del self.cache[oldest_key]
        self.logger.debug(f"🗑️ 移除了最旧缓存: {oldest_key}")
    
    def get_cache_info(self) -> Dict[str, Any]:
        """
        获取缓存信息
        
        Returns:
            Dict: 缓存统计信息
        """
        expired_count = sum(1 for entry in self.cache.values() if entry.is_expired())
        valid_count = len(self.cache) - expired_count
        
        return {
            "total_entries": len(self.cache),
            "valid_entries": valid_count,
            "expired_entries": expired_count,
            "snapshots_count": len(self.snapshots),
            "max_size": self.max_size,
            "usage_percent": int(len(self.cache) / self.max_size * 100) if self.max_size > 0 else 0
        }
    
    def get_usage(self) -> Dict[str, Any]:
        """
        获取缓存使用情况（向后兼容）
        
        Returns:
            Dict: 使用情况
        """
        info = self.get_cache_info()
        return {
            "current_size": info["total_entries"],
            "max_size": info["max_size"],
            "usage_percent": info["usage_percent"],
            "cached_items": list(self.cache.keys())[:10]  # 只显示前10个
        }
    
    def add_task(self, graph_id: str, task_data: Any):
        """
        添加任务（向后兼容）
        
        Args:
            graph_id: 任务ID
            task_data: 任务数据
        """
        self.set_cache(f"task_{graph_id}", task_data, ttl=3600)
    
    def get_task(self, graph_id: str) -> Any:
        """
        获取任务（向后兼容）
        
        Args:
            graph_id: 任务ID
            
        Returns:
            任务数据
        """
        return self.get_cache(f"task_{graph_id}")
    
    def remove_task(self, graph_id: str) -> bool:
        """
        移除任务（向后兼容）
        
        Args:
            graph_id: 任务ID
            
        Returns:
            bool: 是否成功移除
        """
        return self.clear_cache(f"task_{graph_id}")
    
    def get_cache_list(self) -> list:
        """获取缓存列表（向后兼容）"""
        return list(self.cache.keys())
    
    def clear_cache_method(self):
        """清空缓存（向后兼容）"""
        self.clear_all_cache()


if __name__ == "__main__":
    # 测试缓存管理器
    print("💾 TaskCacheManager测试")
    print("=" * 60)
    
    manager = TaskCacheManager(default_ttl=10)  # 10秒过期
    
    # 测试1: 设置和获取缓存
    print("\n1. 设置和获取缓存...")
    manager.set_cache("plan_route.eta", "18分钟", ttl=60)
    manager.set_cache("plan_route.route", ["站台A", "公交B"])
    manager.set_cache("user_reply_history", {"confirm_hospital": "虹口医院"})
    
    eta = manager.get_cache("plan_route.eta")
    route = manager.get_cache("plan_route.route")
    print(f"   ETA: {eta}")
    print(f"   路线: {route}")
    
    # 测试2: 检查缓存
    print("\n2. 检查缓存是否存在...")
    print(f"   plan_route.eta 存在: {manager.has_cache('plan_route.eta')}")
    print(f"   unknown_key 存在: {manager.has_cache('unknown_key')}")
    
    # 测试3: 清除过期缓存
    print("\n3. 等待5秒...")
    time.sleep(5)
    expired_count = manager.clear_expired_cache()
    print(f"   已清除过期缓存: {expired_count}个")
    
    # 测试4: 快照功能
    print("\n4. 快照功能测试...")
    snapshot_id = "insert_task_snapshot"
    snapshot_count = manager.snapshot_current_state(snapshot_id, prefix="plan_route.")
    print(f"   快照已创建: {snapshot_id} ({snapshot_count}个条目)")
    
    # 清除一些缓存
    manager.clear_cache("plan_route.eta")
    print(f"   清除plan_route.eta后，缓存数: {len(manager.cache)}")
    
    # 恢复快照
    restored_count = manager.restore_from_snapshot(snapshot_id)
    print(f"   恢复快照后，缓存数: {len(manager.cache)} ({restored_count}个条目恢复)")
    
    # 测试5: 获取缓存信息
    print("\n5. 缓存信息...")
    info = manager.get_cache_info()
    print(f"   总条目数: {info['total_entries']}")
    print(f"   有效条目: {info['valid_entries']}")
    print(f"   快照数: {info['snapshots_count']}")
    print(f"   使用率: {info['usage_percent']}%")
    
    print("\n🎉 TaskCacheManager测试完成！")