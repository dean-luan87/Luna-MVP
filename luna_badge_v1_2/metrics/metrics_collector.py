"""
Metrics Collector

统一指标收集器。

v1.5 设计原则：
- 提供统一 API，让 MOC / PlanB / TaskChain / Watchdog 都能打点
- 不做 Prometheus，不做复杂可视化
- 先保证可写、可解析、可聚合
"""

import json
import time
import uuid
from pathlib import Path
from typing import Dict, Any, Optional


class MetricsCollector:
    """
    指标收集器
    
    职责：
    - 提供统一 API 用于打点
    - 写入三类日志：execution_trace.jsonl、runtime_metrics.log、error_log.jsonl
    - v1.5: 最小实现，够用即可
    """
    
    def __init__(
        self,
        metrics_path: str = "logs/runtime/runtime_metrics.log",
        trace_path: str = "logs/runtime/execution_trace.jsonl",
        error_path: str = "logs/runtime/error_log.jsonl"
    ):
        """
        初始化指标收集器
        
        Args:
            metrics_path: 性能指标日志路径
            trace_path: 执行跟踪日志路径
            error_path: 错误日志路径
        """
        self.metrics_path = Path(metrics_path)
        self.trace_path = Path(trace_path)
        self.error_path = Path(error_path)
        
        # 确保目录存在
        self.metrics_path.parent.mkdir(parents=True, exist_ok=True)
        self.trace_path.parent.mkdir(parents=True, exist_ok=True)
        self.error_path.parent.mkdir(parents=True, exist_ok=True)
    
    def _write(self, path: Path, obj: Dict[str, Any]):
        """
        写入 JSONL 文件
        
        Args:
            path: 文件路径
            obj: 要写入的对象
        """
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")
    
    def new_trace_id(self) -> str:
        """
        生成新的 trace ID
        
        Returns:
            trace ID（UUID）
        """
        return str(uuid.uuid4())
    
    def trace(
        self,
        trace_id: str,
        task_domain: str,
        node_id: str,
        event: str,
        payload: Optional[Dict[str, Any]] = None
    ):
        """
        记录执行跟踪事件
        
        Args:
            trace_id: 跟踪 ID
            task_domain: 任务领域
            node_id: 节点 ID
            event: 事件类型（moc_decision | fallback | node_start | node_end | watchdog）
            payload: 事件负载
        """
        self._write(self.trace_path, {
            "ts": int(time.time()),
            "trace_id": trace_id,
            "task_domain": task_domain,
            "node_id": node_id,
            "event": event,
            "payload": payload or {}
        })
    
    def metric(self, name: str, value: float, tags: Optional[Dict[str, Any]] = None):
        """
        记录性能指标
        
        Args:
            name: 指标名称（如 "latency_ms", "throughput"）
            value: 指标值
            tags: 标签（如 domain, model_id, version）
        """
        self._write(self.metrics_path, {
            "ts": int(time.time()),
            "metric": name,
            "value": value,
            "tags": tags or {}
        })
    
    def error(
        self,
        error_type: str,
        severity: str,
        context: Optional[Dict[str, Any]] = None
    ):
        """
        记录错误
        
        Args:
            error_type: 错误类型（timeout | invalid_output | contradiction | state_mismatch）
            severity: 严重程度（low | medium | high）
            context: 上下文信息
        """
        self._write(self.error_path, {
            "ts": int(time.time()),
            "error_type": error_type,
            "severity": severity,
            "context": context or {}
        })




