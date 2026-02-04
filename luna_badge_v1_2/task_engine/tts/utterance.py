"""
Utterance: 待播报的语音/文本输出数据结构

统一定义一条"要说的话"的结构，未来可扩展情感、声线、优先级。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Any
import time


@dataclass
class Utterance:
    """
    表示一条待播报的语音内容。

    字段说明：
    - text: 文本内容
    - level: 消息级别（info / warning / error / system 等）
    - channel: 输出通道（tts / log / screen / hmi 等）
    - priority: 优先级（数值越大越优先，建议范围 [0, 100]）
    - interrupt: 是否期望打断当前播报
      （Patch-H 中仅在队列层面生效：本轮只播这条；未来可扩展到流式打断）
    - created_at: 创建时间戳（秒）
    - meta: 其他元数据（情感、声线、语速等）
    - play_id: 用于标识唯一一次"播放会话"，
      未来接入异步 TTS / 回调时，可用来判断回调是否对应当前 Utterance
    """
    text: str
    level: str = "info"  # info / warning / error / debug / system
    channel: str = "tts"  # tts / log / screen / hmi 等
    priority: int = 50  # 优先级（数值越大越优先，建议范围 [0, 100]）
    interrupt: bool = False  # 是否期望打断当前播报
    created_at: float = field(default_factory=lambda: time.time())
    meta: Dict[str, Any] = field(default_factory=dict)
    play_id: str = ""  # 用于标识唯一一次"播放会话"

    def to_dict(self) -> Dict[str, Any]:
        """
        将 Utterance 序列化为字典结构，便于日志和上报。

        Returns:
            Dict[str, Any]: 字典表示
        """
        return {
            "text": self.text,
            "level": self.level,
            "channel": self.channel,
            "priority": self.priority,
            "interrupt": self.interrupt,
            "created_at": self.created_at,
            "meta": dict(self.meta) if self.meta is not None else {},
            "play_id": self.play_id,
        }

