#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 增强版事件总线
P1-2: 统一事件驱动架构

功能:
- 增强事件总线
- 统一模块间通信
- 支持异步处理
- 支持优先级队列
- 支持事件过滤
"""

import logging
import queue
import threading
import time
from typing import Dict, Any, Callable, Optional, List, Set
from dataclasses import dataclass
from enum import Enum
from collections import defaultdict

logger = logging.getLogger(__name__)


class EventType(Enum):
    """事件类型"""
    # 语音事件
    VOICE_RECOGNIZED = "voice_recognized"
    VOICE_INTENT_PARSED = "voice_intent_parsed"
    VOICE_COMMAND = "voice_command"
    
    # 视觉事件
    VISUAL_DETECTION = "visual_detection"
    OBJECT_DETECTED = "object_detected"
    OCR_RESULT = "ocr_result"
    
    # 导航事件
    NAVIGATION_STARTED = "navigation_started"
    NAVIGATION_UPDATED = "navigation_updated"
    NAVIGATION_COMPLETED = "navigation_completed"
    PATH_PLANNED = "path_planned"
    
    # 记忆事件
    MEMORY_SAVED = "memory_saved"
    MEMORY_RECALLED = "memory_recalled"
    
    # TTS事件
    TTS_BROADCAST = "tts_broadcast"
    TTS_STARTED = "tts_started"
    TTS_COMPLETED = "tts_completed"
    
    # 系统事件
    SYSTEM_STARTED = "system_started"
    SYSTEM_STOPPED = "system_stopped"
    SYSTEM_ERROR = "system_error"
    MODULE_STATUS_CHANGED = "module_status_changed"
    
    # 任务事件
    TASK_STARTED = "task_started"
    TASK_COMPLETED = "task_completed"
    TASK_INTERRUPTED = "task_interrupted"
    TASK_RESUMED = "task_resumed"
    
    # 用户事件
    USER_FEEDBACK = "user_feedback"
    USER_INPUT = "user_input"


class EventPriority(Enum):
    """事件优先级"""
    HIGH = 1
    NORMAL = 2
    LOW = 3


@dataclass
class Event:
    """事件"""
    event_type: EventType
    data: Dict[str, Any]
    timestamp: float
    source: str
    priority: EventPriority = EventPriority.NORMAL
    correlation_id: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "event_type": self.event_type.value,
            "data": self.data,
            "timestamp": self.timestamp,
            "source": self.source,
            "priority": self.priority.value if isinstance(self.priority, EventPriority) else self.priority
        }


class PriorityQueue(queue.PriorityQueue):
    """优先级队列"""
    
    def __init__(self, maxsize=0):
        super().__init__(maxsize)
        self.counter = 0
    
    def put(self, item, block=True, timeout=None):
        """添加事件到队列"""
        priority, _, event = item
        super().put((priority, time.time(), self.counter, event), block, timeout)
        self.counter += 1
    
    def get(self, block=True, timeout=None):
        """从队列获取事件"""
        _, _, _, event = super().get(block, timeout)
        return event


class EnhancedEventBus:
    """
    增强版事件总线
    
    功能:
    1. 优先级队列
    2. 事件过滤
    3. 异步处理
    4. 事件追踪
    5. 统计信息
    """
    
    def __init__(self, max_queue_size: int = 1000):
        """
        初始化事件总线
        
        Args:
            max_queue_size: 最大队列大小
        """
        # 事件队列（优先级队列）
        self.event_queue = PriorityQueue(maxsize=max_queue_size)
        
        # 订阅者字典：{event_type: [handlers]}
        self.subscribers: Dict[EventType, List[Callable]] = defaultdict(list)
        
        # 事件过滤器
        self.event_filters: List[Callable[[Event], bool]] = []
        
        # 工作线程
        self.running = False
        self.worker_thread: Optional[threading.Thread] = None
        
        # 统计信息
        self.stats = {
            "events_published": 0,
            "events_processed": 0,
            "events_dropped": 0,
            "events_by_type": defaultdict(int)
        }
        
        # 事件追踪
        self.event_history: List[Event] = []
        self.max_history = 100
        
        logger.info("📡 增强版事件总线初始化完成")
    
    def subscribe(self, event_type: EventType, handler: Callable, priority: int = 0):
        """
        订阅事件
        
        Args:
            event_type: 事件类型
            handler: 处理函数
            priority: 优先级（数字越小优先级越高）
        """
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        
        self.subscribers[event_type].append((priority, handler))
        # 按优先级排序
        self.subscribers[event_type].sort(key=lambda x: x[0])
        
        logger.debug(f"📡 订阅事件: {event_type.value} (优先级: {priority})")
    
    def unsubscribe(self, event_type: EventType, handler: Callable):
        """
        取消订阅
        
        Args:
            event_type: 事件类型
            handler: 处理函数
        """
        if event_type in self.subscribers:
            # 移除handler
            self.subscribers[event_type] = [
                (p, h) for p, h in self.subscribers[event_type] if h != handler
            ]
            logger.debug(f"📡 取消订阅: {event_type.value}")
    
    def add_filter(self, filter_func: Callable[[Event], bool]):
        """
        添加事件过滤器
        
        Args:
            filter_func: 过滤函数，返回True表示保留事件
        """
        self.event_filters.append(filter_func)
        logger.debug("📡 添加事件过滤器")
    
    def publish(self,
                event_type: EventType,
                data: Dict[str, Any],
                source: str = "unknown",
                priority: EventPriority = EventPriority.NORMAL,
                correlation_id: Optional[str] = None):
        """
        发布事件
        
        Args:
            event_type: 事件类型
            data: 事件数据
            source: 事件源
            priority: 优先级
            correlation_id: 关联ID
        """
        event = Event(
            event_type=event_type,
            data=data,
            timestamp=time.time(),
            source=source,
            priority=priority,
            correlation_id=correlation_id
        )
        
        # 应用过滤器
        if self.event_filters:
            if not all(f(event) for f in self.event_filters):
                logger.debug(f"📡 事件被过滤: {event_type.value}")
                self.stats["events_dropped"] += 1
                return
        
        # 添加到队列
        try:
            self.event_queue.put((priority.value, time.time(), event))
            self.stats["events_published"] += 1
            self.stats["events_by_type"][event_type.value] += 1
            logger.debug(f"📡 发布事件: {event_type.value} from {source}")
        except queue.Full:
            logger.error(f"❌ 事件队列已满，丢弃事件: {event_type.value}")
            self.stats["events_dropped"] += 1
    
    def publish_async(self, *args, **kwargs):
        """异步发布事件"""
        threading.Thread(target=self.publish, args=args, kwargs=kwargs, daemon=True).start()
    
    def start(self):
        """启动事件总线"""
        if self.running:
            logger.warning("⚠️ 事件总线已在运行")
            return
        
        self.running = True
        self.worker_thread = threading.Thread(target=self._worker, daemon=True)
        self.worker_thread.start()
        logger.info("📡 增强版事件总线已启动")
    
    def stop(self, timeout: float = 5.0):
        """
        停止事件总线
        
        Args:
            timeout: 超时时间（秒）
        """
        if not self.running:
            return
        
        self.running = False
        
        if self.worker_thread:
            self.worker_thread.join(timeout=timeout)
        
        logger.info("📡 增强版事件总线已停止")
        
        # 打印统计信息
        self._print_stats()
    
    def _worker(self):
        """工作线程"""
        while self.running:
            try:
                # 从队列获取事件
                event = self.event_queue.get(timeout=1.0)
                
                # 添加到历史
                self.event_history.append(event)
                if len(self.event_history) > self.max_history:
                    self.event_history.pop(0)
                
                # 分发给订阅者
                if event.event_type in self.subscribers:
                    for priority, handler in self.subscribers[event.event_type]:
                        try:
                            handler(event)
                        except Exception as e:
                            logger.error(f"⚠️ 事件处理失败: {event.event_type.value} - {e}")
                
                self.stats["events_processed"] += 1
                
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"⚠️ 事件总线错误: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "events_published": self.stats["events_published"],
            "events_processed": self.stats["events_processed"],
            "events_dropped": self.stats["events_dropped"],
            "events_by_type": dict(self.stats["events_by_type"]),
            "subscribers_count": sum(len(handlers) for handlers in self.subscribers.values()),
            "queue_size": self.event_queue.qsize()
        }
    
    def _print_stats(self):
        """打印统计信息"""
        stats = self.get_stats()
        logger.info("📊 事件总线统计:")
        logger.info(f"   发布: {stats['events_published']}")
        logger.info(f"   处理: {stats['events_processed']}")
        logger.info(f"   丢弃: {stats['events_dropped']}")
        logger.info(f"   队列大小: {stats['queue_size']}")
        logger.info(f"   订阅者: {stats['subscribers_count']}")
    
    def clear_history(self):
        """清空历史记录"""
        self.event_history.clear()
        logger.debug("📡 事件历史已清空")
    
    def get_recent_events(self, count: int = 10) -> List[Event]:
        """
        获取最近的事件
        
        Args:
            count: 事件数量
            
        Returns:
            最近的事件列表
        """
        return self.event_history[-count:]
    
    def get_events_by_type(self, event_type: EventType, count: int = 10) -> List[Event]:
        """
        获取指定类型的最近事件
        
        Args:
            event_type: 事件类型
            count: 事件数量
            
        Returns:
            事件列表
        """
        return [e for e in self.event_history if e.event_type == event_type][-count:]
    
    # 便捷方法
    def broadcast_tts(self, text: str, style: str = "default", **kwargs):
        """广播TTS消息"""
        self.publish(
            event_type=EventType.TTS_BROADCAST,
            data={"text": text, "style": style, **kwargs},
            source="event_bus"
        )
    
    def emit_navigation(self, path: List[str], **kwargs):
        """发出导航事件"""
        self.publish(
            event_type=EventType.NAVIGATION_STARTED,
            data={"path": path, **kwargs},
            source="navigation"
        )
    
    def emit_visual_detection(self, detection_type: str, objects: List[Dict], **kwargs):
        """发出视觉检测事件"""
        self.publish(
            event_type=EventType.VISUAL_DETECTION,
            data={"type": detection_type, "objects": objects, **kwargs},
            source="vision",
            priority=EventPriority.HIGH
        )


# 全局事件总线实例
_global_enhanced_bus: Optional[EnhancedEventBus] = None


def get_event_bus() -> EnhancedEventBus:
    """获取全局事件总线实例"""
    global _global_enhanced_bus
    if _global_enhanced_bus is None:
        _global_enhanced_bus = EnhancedEventBus()
    return _global_enhanced_bus


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 70)
    print("📡 增强版事件总线测试")
    print("=" * 70)
    
    bus = EnhancedEventBus()
    bus.start()
    
    # 测试订阅者
    def tts_handler(event: Event):
        print(f"🔊 TTS: {event.data.get('text', '')}")
    
    def visual_handler(event: Event):
        print(f"👁️  视觉检测: {event.data.get('type', '')}")
    
    bus.subscribe(EventType.TTS_BROADCAST, tts_handler)
    bus.subscribe(EventType.VISUAL_DETECTION, visual_handler)
    
    # 发布事件
    print("\n发布测试事件...")
    bus.broadcast_tts("测试播报", style="cheerful")
    bus.emit_visual_detection("stairs", [{"confidence": 0.9}])
    
    # 等待处理
    time.sleep(1)
    
    # 打印统计
    stats = bus.get_stats()
    print(f"\n统计信息:")
    print(f"  发布: {stats['events_published']}")
    print(f"  处理: {stats['events_processed']}")
    
    bus.stop()
    
    print("\n" + "=" * 70)

