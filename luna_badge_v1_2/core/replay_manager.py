from core.logging import get_logger

log = get_logger("replay_manager")
"""
Replay Manager (v1.3.0)

回放系统

支持记录和回放系统运行过程，用于调试、测试和问题复现
支持从 trace_events.log 读取 trace_id 链路
"""

import json
import logging
import os
import time
from datetime import datetime
from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass, asdict
from enum import Enum

from .error_codes import ErrorCode, create_error_response, create_success_response

logger = logging.getLogger(__name__)

# trace_events.log 文件路径
TRACE_FILE = "logs/trace_events.log"


class ReplayMode(Enum):
    """回放模式"""
    RECORD = "record"  # 记录模式
    REPLAY = "replay"  # 回放模式
    OFF = "off"  # 关闭


@dataclass
class ReplayEvent:
    """回放事件数据结构"""

    event_type: str
    timestamp: float
    input_data: Dict[str, Any]
    output_data: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)


class ReplayManager:
    """
    回放管理器

    支持记录和回放系统运行过程
    """

    def __init__(
        self,
        replay_dir: str = "logs/replay",
        mode: ReplayMode = ReplayMode.OFF,
        replay_file: Optional[str] = None,
    ):
        """
        初始化回放管理器

        Args:
            replay_dir: 回放文件目录
            mode: 回放模式
            replay_file: 回放文件路径（仅回放模式需要）
        """
        self.replay_dir = replay_dir
        self.mode = mode
        self.replay_file = replay_file

        # 创建目录
        if self.mode == ReplayMode.RECORD:
            os.makedirs(self.replay_dir, exist_ok=True)

        # 记录模式：事件列表
        self.recorded_events: List[ReplayEvent] = []

        # 回放模式：加载的事件列表
        self.replay_events: List[ReplayEvent] = []
        self.replay_index: int = 0

        if self.mode == ReplayMode.REPLAY:
            self._load_replay_file()

        logger.info(f"回放管理器初始化: mode={self.mode.value}")

    def _load_replay_file(self):
        """加载回放文件"""
        if not self.replay_file:
            logger.error("回放模式需要指定 replay_file")
            return

        if not os.path.exists(self.replay_file):
            logger.error(f"回放文件不存在: {self.replay_file}")
            return

        try:
            with open(self.replay_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.replay_events = [
                    ReplayEvent(**event_data) for event_data in data.get("events", [])
                ]
            logger.info(f"加载回放文件成功: {len(self.replay_events)} 个事件")
        except Exception as e:
            logger.error(f"加载回放文件失败: {e}")

    def record_event(
        self,
        event_type: str,
        input_data: Dict[str, Any],
        output_data: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        记录事件（记录模式）

        Args:
            event_type: 事件类型
            input_data: 输入数据
            output_data: 输出数据
            metadata: 元数据
        """
        if self.mode != ReplayMode.RECORD:
            return

        event = ReplayEvent(
            event_type=event_type,
            timestamp=time.time(),
            input_data=input_data,
            output_data=output_data,
            metadata=metadata,
        )

        self.recorded_events.append(event)

    def get_next_replay_event(
        self, event_type: Optional[str] = None
    ) -> Optional[ReplayEvent]:
        """
        获取下一个回放事件（回放模式）

        Args:
            event_type: 事件类型过滤（可选）

        Returns:
            Optional[ReplayEvent]: 回放事件，如果没有更多事件则返回 None
        """
        if self.mode != ReplayMode.REPLAY:
            return None

        while self.replay_index < len(self.replay_events):
            event = self.replay_events[self.replay_index]
            self.replay_index += 1

            if event_type is None or event.event_type == event_type:
                return event

        return None

    def replay_function(
        self,
        func: Callable,
        event_type: str,
        *args,
        **kwargs,
    ) -> Any:
        """
        回放函数调用（回放模式）

        Args:
            func: 原始函数
            event_type: 事件类型
            *args: 函数参数
            **kwargs: 函数关键字参数

        Returns:
            Any: 函数返回值（从回放数据中获取）
        """
        if self.mode != ReplayMode.REPLAY:
            # 非回放模式，直接调用原函数
            return func(*args, **kwargs)

        # 尝试获取对应的回放事件
        event = self.get_next_replay_event(event_type)
        if event and event.output_data is not None:
            logger.debug(f"[回放] 使用记录的输出: {event_type}")
            return event.output_data.get("result")

        # 没有找到回放数据，调用原函数（并记录）
        logger.warning(f"[回放] 未找到回放数据，调用原函数: {event_type}")
        result = func(*args, **kwargs)
        return result

    def save_recorded_events(self, filename: Optional[str] = None) -> str:
        """
        保存记录的事件（记录模式）

        Args:
            filename: 文件名（可选，默认自动生成）

        Returns:
            str: 保存的文件路径
        """
        if self.mode != ReplayMode.RECORD:
            logger.warning("当前不是记录模式，无法保存")
            return ""

        if not self.recorded_events:
            logger.warning("没有记录的事件")
            return ""

        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"replay_{timestamp}.json"

        filepath = os.path.join(self.replay_dir, filename)

        try:
            data = {
                "created_at": datetime.now().isoformat(),
                "total_events": len(self.recorded_events),
                "events": [event.to_dict() for event in self.recorded_events],
            }

            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            logger.info(f"保存回放文件成功: {filepath} ({len(self.recorded_events)} 个事件)")
            return filepath

        except Exception as e:
            logger.error(f"保存回放文件失败: {e}")
            return ""

    def reset_replay(self):
        """重置回放索引（回放模式）"""
        if self.mode == ReplayMode.REPLAY:
            self.replay_index = 0
            logger.info("回放索引已重置")

    def clear_recorded_events(self):
        """清空记录的事件（记录模式）"""
        if self.mode == ReplayMode.RECORD:
            self.recorded_events.clear()
            logger.info("已清空记录的事件")

    def get_statistics(self) -> Dict[str, Any]:
        """
        获取统计信息

        Returns:
            Dict[str, Any]: 统计信息
        """
        if self.mode == ReplayMode.RECORD:
            return {
                "mode": "record",
                "recorded_events": len(self.recorded_events),
                "events_by_type": self._count_events_by_type(self.recorded_events),
            }
        elif self.mode == ReplayMode.REPLAY:
            return {
                "mode": "replay",
                "total_events": len(self.replay_events),
                "current_index": self.replay_index,
                "remaining_events": len(self.replay_events) - self.replay_index,
                "events_by_type": self._count_events_by_type(self.replay_events),
            }
        else:
            return {"mode": "off"}

    @staticmethod
    def _count_events_by_type(events: List[ReplayEvent]) -> Dict[str, int]:
        """统计各类型事件数量"""
        counts = {}
        for event in events:
            counts[event.event_type] = counts.get(event.event_type, 0) + 1
        return counts

    @staticmethod
    def load_trace(trace_id: str) -> List[Dict[str, Any]]:
        """
        从 trace_events.log 加载指定 trace_id 的所有事件

        Args:
            trace_id: 追踪ID

        Returns:
            List[Dict[str, Any]]: 按时间戳排序的事件列表
        """
        events = []

        if not os.path.exists(TRACE_FILE):
            logger.warning(f"trace_events.log 文件不存在: {TRACE_FILE}")
            return events

        try:
            with open(TRACE_FILE, "r", encoding="utf-8") as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue

                    try:
                        event_data = json.loads(line)
                        
                        # 检查 trace_id（可能在 payload 或顶层）
                        event_trace_id = None
                        if "trace_id" in event_data:
                            event_trace_id = event_data["trace_id"]
                        elif "payload" in event_data and isinstance(event_data["payload"], dict):
                            event_trace_id = event_data["payload"].get("trace_id")

                        if event_trace_id == trace_id:
                            events.append(event_data)

                    except json.JSONDecodeError as e:
                        logger.warning(f"解析 trace_events.log 第 {line_num} 行失败: {e}")
                        continue

            # 按时间戳排序
            events.sort(key=lambda x: x.get("ts", 0))

            logger.info(f"加载 trace_id={trace_id} 的事件: {len(events)} 个")
            return events

        except Exception as e:
            logger.error(f"加载 trace 失败: {e}")
            return events

    @staticmethod
    def print_trace(events: List[Dict[str, Any]]):
        """
        按时间顺序打印整条链路

        Args:
            events: 事件列表（已排序）
        """
        if not events:
            log.info("⚠️ 没有事件可打印")
            return

        log.info("\n" + "=" * 80")
        log.debug(f"📋 Trace 链路（共 {len(events)} 个事件）")
        log.info("=" * 80")

        for i, event in enumerate(events, 1):
            phase = event.get("phase", "unknown")
            event_name = event.get("event", "unknown")
            ts = event.get("ts", 0)
            payload = event.get("payload", {})

            # 格式化时间戳
            time_str = datetime.fromtimestamp(ts).strftime("%H:%M:%S.%f")[:-3] if ts else "N/A"

            log.info(f"\n[{i}] {time_str} | {phase}.{event_name}")

            # 打印 payload（美化）
            if payload:
                for key, value in payload.items():
                    if key == "trace_id":
                        continue  # trace_id 已经在标题中
                    if isinstance(value, (dict, list)):
                        value_str = json.dumps(value, ensure_ascii=False, indent=2)
                        if len(value_str) > 200:
                            value_str = value_str[:200] + "..."
                    else:
                        value_str = str(value)
                        if len(value_str) > 100:
                            value_str = value_str[:100] + "..."

                    log.info(f"    {key}: {value_str}")

            # 如果有错误信息
            if "error_code" in event or "error_message" in event:
                log.error(f"    ❌ ERROR: {event.get('error_code', '')} - {event.get('error_message', '')}")

        log.info("\n" + "=" * 80")


# 便捷函数
def create_replay_manager(
    mode: str = "off",
    replay_dir: str = "logs/replay",
    replay_file: Optional[str] = None,
) -> ReplayManager:
    """
    创建回放管理器（便捷函数）

    Args:
        mode: 模式（"record"/"replay"/"off"）
        replay_dir: 回放文件目录
        replay_file: 回放文件路径（仅回放模式需要）

    Returns:
        ReplayManager: 回放管理器实例
    """
    mode_enum = ReplayMode.OFF
    if mode == "record":
        mode_enum = ReplayMode.RECORD
    elif mode == "replay":
        mode_enum = ReplayMode.REPLAY

    return ReplayManager(
        replay_dir=replay_dir,
        mode=mode_enum,
        replay_file=replay_file,
    )

