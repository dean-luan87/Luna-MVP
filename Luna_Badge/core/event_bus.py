#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 事件总线模块
用于模块间的消息传递和事件调度，特别是TTS播报
"""

import logging
import queue
import threading
from typing import Dict, Any, Callable, Optional, List
from dataclasses import dataclass
from enum import Enum
import json

logger = logging.getLogger(__name__)

class EventType(Enum):
    """事件类型"""
    TTS_BROADCAST = "tts_broadcast"       # TTS播报事件
    NAVIGATION_UPDATE = "navigation_update" # 导航更新
    VISION_DETECTED = "vision_detected"     # 视觉检测
    USER_FEEDBACK = "user_feedback"         # 用户反馈
    SYSTEM_LOG = "system_log"              # 系统日志

@dataclass
class Event:
    """事件"""
    event_type: EventType
    data: Dict[str, Any]
    timestamp: float
    source: str
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "event_type": self.event_type.value,
            "data": self.data,
            "timestamp": self.timestamp,
            "source": self.source
        }

class EventBus:
    """事件总线"""
    
    def __init__(self):
        """初始化事件总线"""
        self.logger = logging.getLogger(__name__)
        
        # 事件队列
        self.event_queue = queue.Queue()
        
        # 订阅者字典：{event_type: [handlers]}
        self.subscribers: Dict[EventType, List[Callable]] = {}
        
        # 工作线程
        self.running = False
        self.worker_thread: Optional[threading.Thread] = None
        
        # TTS处理器（预留接口）
        self.tts_handler: Optional[Callable] = None
        
        self.logger.info("📡 事件总线初始化完成")
    
    def subscribe(self, event_type: EventType, handler: Callable):
        """
        订阅事件
        
        Args:
            event_type: 事件类型
            handler: 处理函数
        """
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        
        self.subscribers[event_type].append(handler)
        self.logger.debug(f"📡 订阅事件: {event_type.value}")
    
    def publish(self, event_type: EventType, data: Dict[str, Any], source: str = "unknown"):
        """
        发布事件
        
        Args:
            event_type: 事件类型
            data: 事件数据
            source: 事件源
        """
        event = Event(
            event_type=event_type,
            data=data,
            timestamp=time.time(),
            source=source
        )
        
        self.event_queue.put(event)
        self.logger.debug(f"📡 发布事件: {event_type.value} from {source}")
    
    def broadcast_tts(self, text: str, style: str = "default", **kwargs):
        """
        广播TTS消息
        
        Args:
            text: 播报文本
            style: 播报风格
            **kwargs: 其他参数
        """
        self.publish(
            event_type=EventType.TTS_BROADCAST,
            data={
                "text": text,
                "style": style,
                **kwargs
            },
            source="event_bus"
        )
    
    def start(self):
        """启动事件总线"""
        if self.running:
            return
        
        self.running = True
        self.worker_thread = threading.Thread(target=self._worker, daemon=True)
        self.worker_thread.start()
        self.logger.info("📡 事件总线已启动")
    
    def stop(self):
        """停止事件总线"""
        self.running = False
        if self.worker_thread:
            self.worker_thread.join(timeout=1.0)
        self.logger.info("📡 事件总线已停止")
    
    def _worker(self):
        """工作线程"""
        while self.running:
            try:
                # 从队列获取事件
                event = self.event_queue.get(timeout=1.0)
                
                # 分发给订阅者
                if event.event_type in self.subscribers:
                    for handler in self.subscribers[event.event_type]:
                        try:
                            handler(event)
                        except Exception as e:
                            self.logger.error(f"⚠️ 事件处理失败: {e}")
                
                # 特殊处理TTS事件
                if event.event_type == EventType.TTS_BROADCAST and self.tts_handler:
                    try:
                        self.tts_handler(event.data)
                    except Exception as e:
                        self.logger.error(f"⚠️ TTS处理失败: {e}")
                
                self.event_queue.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                self.logger.error(f"⚠️ 事件总线错误: {e}")
    
    def set_tts_handler(self, handler: Callable):
        """设置TTS处理器"""
        self.tts_handler = handler
        self.logger.info("📡 TTS处理器已注册")


# 全局事件总线实例
import time
global_event_bus = EventBus()

def get_event_bus() -> EventBus:
    """获取事件总线实例"""
    return global_event_bus


if __name__ == "__main__":
    # 测试事件总线
    import logging
    logging.basicConfig(level=logging.INFO)
    
    bus = EventBus()
    bus.start()
    
    # 测试TTS播报
    print("测试TTS播报...")
    bus.broadcast_tts("测试播报", style="empathetic")
    
    # 等待处理
    time.sleep(0.5)
    
    bus.stop()
    print("测试完成")

