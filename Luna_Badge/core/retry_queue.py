#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 事件处理失败缓存机制 (Retry Queue)
缓存失败的事件，定时重试或用户唤醒时重新触发
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict, field
from enum import Enum

logger = logging.getLogger(__name__)


class RetryStatus(Enum):
    """重试状态"""
    PENDING = "pending"       # 等待重试
    RETRYING = "retrying"     # 重试中
    SUCCESS = "success"       # 成功
    FAILED = "failed"         # 失败


@dataclass
class RetryItem:
    """重试项"""
    item_id: str
    type: str
    payload: Any
    status: RetryStatus = RetryStatus.PENDING
    retry_count: int = 0
    max_retries: int = 3
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    last_retry_at: Optional[str] = None
    next_retry_at: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        data = asdict(self)
        data["status"] = self.status.value
        return data


class RetryQueue:
    """重试队列"""
    
    def __init__(self,
                 max_retries: int = 3,
                 retry_interval: int = 60):
        """
        初始化重试队列
        
        Args:
            max_retries: 最大重试次数
            retry_interval: 重试间隔（秒）
        """
        self.max_retries = max_retries
        self.retry_interval = retry_interval
        self.queue: List[RetryItem] = []
        
        # 重试回调函数
        self.retry_callbacks = {}
        
        # 计数器
        self.item_counter = 0
        
        logger.info("📂 重试队列初始化完成")
    
    def _generate_item_id(self) -> str:
        """生成项ID"""
        self.item_counter += 1
        return f"retry_{self.item_counter}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def register_retry_callback(self, item_type: str, callback: callable):
        """注册重试回调函数"""
        self.retry_callbacks[item_type] = callback
        logger.info(f"✅ 注册重试回调: {item_type}")
    
    def add_item(self,
                 item_type: str,
                 payload: Any,
                 max_retries: Optional[int] = None,
                 metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        添加重试项
        
        Args:
            item_type: 项类型
            payload: 载荷数据
            max_retries: 最大重试次数
            metadata: 额外元数据
            
        Returns:
            项ID
        """
        item = RetryItem(
            item_id=self._generate_item_id(),
            type=item_type,
            payload=payload,
            status=RetryStatus.PENDING,
            retry_count=0,
            max_retries=max_retries or self.max_retries,
            next_retry_at=(datetime.now() + timedelta(seconds=self.retry_interval)).isoformat(),
            metadata=metadata or {}
        )
        
        self.queue.append(item)
        
        logger.info(f"📝 添加重试项: {item.item_id} ({item_type})")
        
        return item.item_id
    
    def process_pending_items(self) -> List[str]:
        """
        处理待处理项
        
        Returns:
            成功项ID列表
        """
        success_items = []
        
        now = datetime.now()
        items_to_retry = [
            item for item in self.queue
            if item.status == RetryStatus.PENDING
            and item.next_retry_at
            and datetime.fromisoformat(item.next_retry_at) <= now
        ]
        
        for item in items_to_retry:
            if self._retry_item(item):
                success_items.append(item.item_id)
        
        return success_items
    
    def _retry_item(self, item: RetryItem) -> bool:
        """
        重试项
        
        Args:
            item: 重试项
            
        Returns:
            是否成功
        """
        item.status = RetryStatus.RETRYING
        item.retry_count += 1
        item.last_retry_at = datetime.now().isoformat()
        
        logger.info(f"🔄 重试项: {item.item_id} (第{item.retry_count}次)")
        
        # 调用重试回调
        if item.type in self.retry_callbacks:
            try:
                callback = self.retry_callbacks[item.type]
                success = callback(item.payload, item.metadata)
                
                if success:
                    item.status = RetryStatus.SUCCESS
                    logger.info(f"✅ 重试成功: {item.item_id}")
                    return True
                else:
                    logger.warning(f"⚠️ 重试失败: {item.item_id}")
                    
            except Exception as e:
                logger.error(f"❌ 重试回调异常: {e}")
        
        # 检查是否超过最大重试次数
        if item.retry_count >= item.max_retries:
            item.status = RetryStatus.FAILED
            logger.error(f"❌ 超过最大重试次数: {item.item_id}")
            return False
        
        # 安排下次重试
        item.status = RetryStatus.PENDING
        item.next_retry_at = (datetime.now() + timedelta(seconds=self.retry_interval)).isoformat()
        
        return False
    
    def get_queue_status(self) -> Dict[str, Any]:
        """获取队列状态"""
        by_status = {}
        by_type = {}
        
        for item in self.queue:
            # 按状态统计
            status = item.status.value
            by_status[status] = by_status.get(status, 0) + 1
            
            # 按类型统计
            item_type = item.type
            by_type[item_type] = by_type.get(item_type, 0) + 1
        
        return {
            "total_items": len(self.queue),
            "by_status": by_status,
            "by_type": by_type,
            "pending_items": [item.to_dict() for item in self.queue if item.status == RetryStatus.PENDING]
        }
    
    def get_pending_items(self, item_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        获取待处理项
        
        Args:
            item_type: 项类型（可选）
            
        Returns:
            待处理项列表
        """
        items = [
            item for item in self.queue
            if item.status == RetryStatus.PENDING
        ]
        
        if item_type:
            items = [item for item in items if item.type == item_type]
        
        return [item.to_dict() for item in items]
    
    def remove_item(self, item_id: str) -> bool:
        """
        移除项
        
        Args:
            item_id: 项ID
            
        Returns:
            是否成功
        """
        for item in self.queue:
            if item.item_id == item_id:
                self.queue.remove(item)
                logger.info(f"🗑️ 移除项: {item_id}")
                return True
        
        return False
    
    def clear_completed_items(self):
        """清空已完成和失败项"""
        self.queue = [item for item in self.queue if item.status not in [RetryStatus.SUCCESS, RetryStatus.FAILED]]
        logger.info("🗑️ 已清空已完成和失败项")


# 测试函数
if __name__ == "__main__":
    import logging
    import time
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 创建重试队列
    retry_queue = RetryQueue(max_retries=3, retry_interval=2)
    
    print("=" * 70)
    print("📂 测试事件处理失败缓存机制")
    print("=" * 70)
    
    # 注册TTS重试回调
    def tts_retry_callback(payload, metadata):
        """TTS重试回调"""
        print(f"   模拟TTS播报: {payload}")
        # 模拟失败
        return False
    
    retry_queue.register_retry_callback("TTS", tts_retry_callback)
    
    # 添加失败的TTS项
    print("\n1️⃣ 添加失败的TTS播报")
    tts_item_id = retry_queue.add_item(
        item_type="TTS",
        payload="前方有台阶，请小心",
        metadata={"priority": "high"}
    )
    print(f"   项ID: {tts_item_id}")
    
    # 查看队列状态
    print("\n2️⃣ 队列状态:")
    status = retry_queue.get_queue_status()
    print(f"   总项数: {status['total_items']}")
    print(f"   按状态: {status['by_status']}")
    print(f"   按类型: {status['by_type']}")
    
    # 处理待处理项
    print("\n3️⃣ 处理待处理项:")
    for i in range(3):
        print(f"\n   第{i+1}次尝试:")
        success_items = retry_queue.process_pending_items()
        if success_items:
            print(f"   ✅ 成功项: {success_items}")
        else:
            print("   ⏳ 等待中...")
        
        if i < 2:
            time.sleep(3)  # 等待下次重试
    
    # 最终状态
    print("\n4️⃣ 最终状态:")
    status = retry_queue.get_queue_status()
    print(f"   总项数: {status['total_items']}")
    print(f"   按状态: {status['by_status']}")
    
    print("\n✅ 测试完成")

