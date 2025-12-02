"""
Tracking System (v1.3.0)

埋点系统（数据记录）

负责记录系统运行过程中的关键事件和数据，用于分析和调试
支持 trace_id 全链路追踪
"""

import json
import logging
import os
import time
from datetime import datetime
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from enum import Enum

logger = logging.getLogger(__name__)

# 全链路追踪日志文件（默认值，会被配置覆盖）
TRACE_FILE = "logs/trace_events.log"

# 日志等级顺序
LEVEL_ORDER = ["DEBUG", "INFO", "WARN", "ERROR"]

# 延迟导入配置，避免循环依赖
_config_loaded = False
_CONFIG = None


def _get_config():
    """延迟加载配置，避免循环依赖"""
    global _config_loaded, _CONFIG
    if not _config_loaded:
        try:
            from .config import CONFIG
            _CONFIG = CONFIG
        except ImportError:
            _CONFIG = None
        _config_loaded = True
    return _CONFIG


def _should_log(level: str) -> bool:
    """
    判断是否应该记录日志

    Args:
        level: 日志等级（DEBUG / INFO / WARN / ERROR）

    Returns:
        bool: 是否应该记录
    """
    config = _get_config()
    if config is None:
        # 如果没有配置，默认记录所有日志
        return True

    cfg_level = config.logging.get("level", "DEBUG")
    try:
        return LEVEL_ORDER.index(level) >= LEVEL_ORDER.index(cfg_level)
    except ValueError:
        # 未知等级，默认记录
        return True


def _should_trace_sample() -> bool:
    """
    判断是否应该采样记录 trace 事件

    Returns:
        bool: 是否应该记录
    """
    import random
    config = _get_config()
    if config is None:
        return True

    sampling_rate = config.logging.get("trace_sampling_rate", 1.0)
    if sampling_rate >= 1.0:
        return True
    return random.random() < sampling_rate


def _get_trace_file() -> str:
    """获取 trace 日志文件路径"""
    config = _get_config()
    if config:
        return config.logging.get("trace_log_file", TRACE_FILE)
    return TRACE_FILE


class EventType(Enum):
    """事件类型枚举"""
    # 模型相关
    MODEL_LOAD = "model_load"
    MODEL_INFERENCE = "model_inference"
    MODEL_ERROR = "model_error"

    # 路由相关
    ROUTER_DECISION = "router_decision"
    ROUTER_FALLBACK = "router_fallback"

    # 系统相关
    SYSTEM_START = "system_start"
    SYSTEM_STOP = "system_stop"
    SYSTEM_ERROR = "system_error"

    # 性能相关
    PERFORMANCE = "performance"
    LATENCY = "latency"


@dataclass
class TrackingEvent:
    """埋点事件数据结构"""

    event_type: str
    timestamp: float
    session_id: Optional[str] = None
    model: Optional[str] = None  # L1 / L2
    user_input: Optional[str] = None
    response: Optional[str] = None
    latency_ms: Optional[float] = None
    error_code: Optional[str] = None
    error_message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        data = asdict(self)
        # 移除 None 值
        return {k: v for k, v in data.items() if v is not None}


class TrackingSystem:
    """
    埋点系统

    负责记录和存储系统运行过程中的关键事件
    """

    def __init__(
        self,
        log_dir: str = "logs/tracking",
        enable_file_logging: bool = True,
        enable_console_logging: bool = False,
        max_buffer_size: int = 100,
    ):
        """
        初始化埋点系统

        Args:
            log_dir: 日志目录
            enable_file_logging: 是否启用文件日志
            enable_console_logging: 是否启用控制台日志
            max_buffer_size: 最大缓冲区大小
        """
        self.log_dir = log_dir
        self.enable_file_logging = enable_file_logging
        self.enable_console_logging = enable_console_logging
        self.max_buffer_size = max_buffer_size

        # 创建日志目录
        if self.enable_file_logging:
            os.makedirs(self.log_dir, exist_ok=True)
            # 创建 logs 目录用于 trace_events.log
            os.makedirs("logs", exist_ok=True)

        # 事件缓冲区
        self.event_buffer: List[TrackingEvent] = []
        self.session_id: Optional[str] = None
        self.start_time: float = time.time()

        logger.info(f"埋点系统初始化完成，日志目录: {self.log_dir}")

    def start_session(self, session_id: Optional[str] = None):
        """
        开始新的会话

        Args:
            session_id: 会话ID，如果为None则自动生成
        """
        if session_id is None:
            session_id = f"session_{int(time.time())}"
        self.session_id = session_id
        logger.info(f"开始新会话: {self.session_id}")

    def track_event(
        self,
        event_type: EventType,
        model: Optional[str] = None,
        user_input: Optional[str] = None,
        response: Optional[str] = None,
        latency_ms: Optional[float] = None,
        error_code: Optional[str] = None,
        error_message: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        trace_id: Optional[str] = None,
    ):
        """
        记录事件

        Args:
            event_type: 事件类型
            model: 模型标识（L1/L2）
            user_input: 用户输入
            response: 响应内容
            latency_ms: 延迟（毫秒）
            error_code: 错误码
            error_message: 错误消息
            metadata: 额外元数据
            trace_id: 追踪ID（用于全链路追踪）
        """
        # 合并 trace_id 到 metadata
        if metadata is None:
            metadata = {}
        if trace_id:
            metadata["trace_id"] = trace_id

        event = TrackingEvent(
            event_type=event_type.value,
            timestamp=time.time(),
            session_id=self.session_id,
            model=model,
            user_input=user_input,
            response=response,
            latency_ms=latency_ms,
            error_code=error_code,
            error_message=error_message,
            metadata=metadata,
        )

        # 添加到缓冲区
        self.event_buffer.append(event)

        # 同时写入 trace_events.log（实时写入，不缓冲）
        self._write_to_trace_file(event)

        # 如果缓冲区满了，自动刷新
        if len(self.event_buffer) >= self.max_buffer_size:
            self.flush()

        # 控制台日志
        if self.enable_console_logging:
            self._log_to_console(event)

    def _write_to_trace_file(self, event: TrackingEvent):
        """写入 trace_events.log 文件（实时写入）"""
        try:
            event_dict = event.to_dict()
            # 添加 trace_id 到顶层（方便查询）
            if event.metadata and "trace_id" in event.metadata:
                event_dict["trace_id"] = event.metadata["trace_id"]

            with open(TRACE_FILE, "a", encoding="utf-8") as f:
                json.dump(event_dict, f, ensure_ascii=False)
                f.write("\n")
        except Exception as e:
            logger.error(f"写入 trace_events.log 失败: {e}")

    def track_model_load(
        self,
        model: str,
        success: bool,
        latency_ms: Optional[float] = None,
        error_message: Optional[str] = None,
    ):
        """
        记录模型加载事件

        Args:
            model: 模型标识（L1/L2）
            success: 是否成功
            latency_ms: 加载耗时（毫秒）
            error_message: 错误消息
        """
        event_type = EventType.MODEL_LOAD
        if not success:
            event_type = EventType.MODEL_ERROR

        self.track_event(
            event_type=event_type,
            model=model,
            latency_ms=latency_ms,
            error_message=error_message,
            metadata={"success": success},
        )

    def track_inference(
        self,
        model: str,
        user_input: str,
        response: str,
        latency_ms: float,
        success: bool = True,
        error_code: Optional[str] = None,
    ):
        """
        记录推理事件

        Args:
            model: 模型标识（L1/L2）
            user_input: 用户输入
            response: 响应内容
            latency_ms: 延迟（毫秒）
            success: 是否成功
            error_code: 错误码
        """
        event_type = EventType.MODEL_INFERENCE
        if not success:
            event_type = EventType.MODEL_ERROR

        self.track_event(
            event_type=event_type,
            model=model,
            user_input=user_input,
            response=response if success else None,
            latency_ms=latency_ms,
            error_code=error_code,
            metadata={"success": success},
        )

    def track_router_decision(
        self,
        selected_model: str,
        reason: str,
        user_input: str,
        intent: Optional[str] = None,
    ):
        """
        记录路由决策事件

        Args:
            selected_model: 选择的模型（L1/L2）
            reason: 路由原因
            user_input: 用户输入
            intent: 意图分类结果
        """
        self.track_event(
            event_type=EventType.ROUTER_DECISION,
            model=selected_model,
            user_input=user_input,
            metadata={
                "reason": reason,
                "intent": intent,
            },
        )

    def track_router_fallback(
        self,
        from_model: str,
        to_model: str,
        reason: str,
        error_message: Optional[str] = None,
    ):
        """
        记录路由降级事件

        Args:
            from_model: 原模型（L1/L2）
            to_model: 目标模型（L1/L2）
            reason: 降级原因
            error_message: 错误消息
        """
        self.track_event(
            event_type=EventType.ROUTER_FALLBACK,
            model=to_model,
            error_message=error_message,
            metadata={
                "from_model": from_model,
                "to_model": to_model,
                "reason": reason,
            },
        )

    def track_latency(
        self,
        operation: str,
        latency_ms: float,
        model: Optional[str] = None,
    ):
        """
        记录延迟事件

        Args:
            operation: 操作名称
            latency_ms: 延迟（毫秒）
            model: 模型标识（可选）
        """
        self.track_event(
            event_type=EventType.LATENCY,
            model=model,
            latency_ms=latency_ms,
            metadata={"operation": operation},
        )

    def flush(self):
        """刷新缓冲区，将所有事件写入文件"""
        if not self.event_buffer:
            return

        if self.enable_file_logging:
            try:
                # 生成日志文件名
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                log_file = os.path.join(
                    self.log_dir, f"tracking_{timestamp}.jsonl"
                )

                # 写入文件（JSONL格式，每行一个JSON）
                with open(log_file, "a", encoding="utf-8") as f:
                    for event in self.event_buffer:
                        json.dump(event.to_dict(), f, ensure_ascii=False)
                        f.write("\n")

                logger.debug(f"已写入 {len(self.event_buffer)} 个事件到 {log_file}")
            except Exception as e:
                logger.error(f"写入埋点数据失败: {e}")

        # 清空缓冲区
        self.event_buffer.clear()

    def _log_to_console(self, event: TrackingEvent):
        """输出到控制台"""
        event_dict = event.to_dict()
        logger.info(f"[埋点] {event_dict}")

    def get_statistics(self) -> Dict[str, Any]:
        """
        获取统计信息

        Returns:
            Dict[str, Any]: 统计信息
        """
        # 刷新缓冲区以包含最新数据
        if self.event_buffer:
            self.flush()

        # 读取所有日志文件并统计
        stats = {
            "total_events": 0,
            "events_by_type": {},
            "events_by_model": {},
            "total_latency_ms": 0.0,
            "avg_latency_ms": 0.0,
            "errors": 0,
        }

        if not os.path.exists(self.log_dir):
            return stats

        try:
            for filename in os.listdir(self.log_dir):
                if not filename.startswith("tracking_") or not filename.endswith(".jsonl"):
                    continue

                filepath = os.path.join(self.log_dir, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    for line in f:
                        try:
                            event_data = json.loads(line.strip())
                            stats["total_events"] += 1

                            # 按类型统计
                            event_type = event_data.get("event_type", "unknown")
                            stats["events_by_type"][event_type] = stats["events_by_type"].get(event_type, 0) + 1

                            # 按模型统计
                            model = event_data.get("model")
                            if model:
                                stats["events_by_model"][model] = stats["events_by_model"].get(model, 0) + 1

                            # 延迟统计
                            latency = event_data.get("latency_ms")
                            if latency:
                                stats["total_latency_ms"] += latency

                            # 错误统计
                            if event_data.get("error_code") or event_data.get("error_message"):
                                stats["errors"] += 1

                        except json.JSONDecodeError:
                            continue

            # 计算平均延迟
            if stats["total_events"] > 0:
                stats["avg_latency_ms"] = stats["total_latency_ms"] / stats["total_events"]

        except Exception as e:
            logger.error(f"获取统计信息失败: {e}")

        return stats

    def close(self):
        """关闭埋点系统，刷新所有数据"""
        self.flush()
        logger.info("埋点系统已关闭")


# 便捷函数：track_event 和 track_error
def track_event(
    phase: str,
    event_name: str,
    payload: Dict[str, Any],
    tracking: Optional[TrackingSystem] = None,
    level: str = "INFO",
):
    """
    便捷函数：记录事件到 trace_events.log

    Args:
        phase: 阶段（如 "router", "l1", "l2"）
        event_name: 事件名称（如 "route_start", "l1_inference"）
        payload: 事件数据（必须包含 trace_id）
        tracking: TrackingSystem 实例（可选，如果为 None 则不写入传统埋点）
        level: 日志等级（DEBUG / INFO / WARN / ERROR）
    """
    # 检查日志等级
    if not _should_log(level):
        return

    trace_id = payload.get("trace_id")

    # 对于 trace 相关的事件，检查采样率
    if phase in ["router", "task_chain"] and not _should_trace_sample():
        return

    if not trace_id:
        logger.warning(f"track_event 调用缺少 trace_id: {event_name}")

    # 构建事件数据
    event_data = {
        "phase": phase,
        "event": event_name,
        "ts": time.time(),
        "payload": payload,
        "level": level,
    }

    # 写入 trace_events.log（使用配置的路径）
    try:
        trace_file = _get_trace_file()
        os.makedirs(os.path.dirname(trace_file) or "logs", exist_ok=True)
        with open(trace_file, "a", encoding="utf-8") as f:
            json.dump(event_data, f, ensure_ascii=False)
            f.write("\n")
    except Exception as e:
        logger.error(f"写入 trace_events.log 失败: {e}")

    # 如果有 tracking 实例，也写入传统埋点
    if tracking:
        event_type_map = {
            "route_start": EventType.ROUTER_DECISION,
            "l1_inference": EventType.MODEL_INFERENCE,
            "l2_inference": EventType.MODEL_INFERENCE,
            "route_decision": EventType.ROUTER_DECISION,
            "route_output": EventType.ROUTER_DECISION,
        }
        event_type = event_type_map.get(event_name, EventType.PERFORMANCE)
        tracking.track_event(
            event_type=event_type,
            model=payload.get("model"),
            user_input=payload.get("text") or payload.get("input_text"),
            response=payload.get("answer") or payload.get("final_answer"),
            latency_ms=payload.get("latency"),
            metadata=payload,
            trace_id=trace_id,
        )


def track_error(
    phase: str,
    error_code: str,
    error_message: str,
    payload: Dict[str, Any],
    tracking: Optional[TrackingSystem] = None,
):
    """
    便捷函数：记录错误到 trace_events.log

    Args:
        phase: 阶段（如 "router"）
        error_code: 错误码
        error_message: 错误消息
        payload: 错误数据（必须包含 trace_id）
        tracking: TrackingSystem 实例（可选）
    """
    # 错误总是记录（ERROR 级别）
    if not _should_log("ERROR"):
        return

    trace_id = payload.get("trace_id")
    if not trace_id:
        logger.warning(f"track_error 调用缺少 trace_id")

    # 构建错误事件数据
    event_data = {
        "phase": phase,
        "event": "error",
        "ts": time.time(),
        "error_code": error_code,
        "error_message": error_message,
        "payload": payload,
        "level": "ERROR",
    }

    # 写入 trace_events.log（使用配置的路径）
    try:
        trace_file = _get_trace_file()
        os.makedirs(os.path.dirname(trace_file) or "logs", exist_ok=True)
        with open(trace_file, "a", encoding="utf-8") as f:
            json.dump(event_data, f, ensure_ascii=False)
            f.write("\n")
    except Exception as e:
        logger.error(f"写入 trace_events.log 失败: {e}")

    # 如果有 tracking 实例，也写入传统埋点
    if tracking:
        tracking.track_event(
            event_type=EventType.SYSTEM_ERROR,
            error_code=error_code,
            error_message=error_message,
            metadata=payload,
            trace_id=trace_id,
        )

