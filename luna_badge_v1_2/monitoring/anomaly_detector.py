#!/usr/bin/env python3
"""
异常检测器 v1.0
基于窗口的异常检测：Spike / Drift / Stall / Threshold
"""

import time
from collections import defaultdict, deque
from typing import Callable, Dict, Deque, Any, Optional


class AnomalyDetector:
    """
    基于窗口的异常检测：
    - Spike：短时间内重复同类错误
    - Drift：指标平均值漂移
    - Threshold：超过阈值
    - Stall：长时间无更新
    """
    
    def __init__(self, on_anomaly: Callable[[dict], None]):
        """
        初始化异常检测器
        
        Args:
            on_anomaly: 异常回调函数
        """
        self.on_anomaly = on_anomaly
        
        # error spike 检测
        self.error_window: Dict[str, Deque[float]] = defaultdict(lambda: deque(maxlen=50))
        self.error_window_sec = 20.0
        self.error_spike_threshold = 5  # N 次错误 / 窗口
        
        # latency 漂移检测
        self.latency_window: Dict[str, Deque[float]] = defaultdict(lambda: deque(maxlen=60))
        self.latency_drift_factor = 2.5  # 均值涨到初始的 N 倍视为 drift
        
        # stall 检测：domain 最后一次事件时间
        self.last_seen: Dict[str, float] = {}
        self.stall_timeout_sec = {
            "vision.yolo": 5.0,
            "audio.asr": 10.0,
            "navigation.path": 10.0,
            "taskchain": 20.0,
        }
    
    def handle_event(self, event: dict):
        """
        处理事件，检测异常
        
        Args:
            event: 监控事件字典
        """
        now = time.time()
        domain = event.get("domain") or event.get("type", "unknown")
        code = event.get("code")
        
        # 更新 last_seen
        self.last_seen[domain] = now
        
        # 1) error spike
        if event.get("type") == "error" and code:
            self._handle_error_spike(code, now)
        
        # 2) latency drift
        if event.get("type") == "latency":
            model = event.get("model", "unknown")
            value_ms = event.get("value_ms", 0.0)
            if isinstance(value_ms, (int, float)):
                self._handle_latency_drift(model, float(value_ms), now)
    
    def _handle_error_spike(self, code: str, now: float):
        """处理错误峰值检测"""
        dq = self.error_window[code]
        dq.append(now)
        
        # 清理窗口（按时间）
        while dq and now - dq[0] > self.error_window_sec:
            dq.popleft()
        
        if len(dq) >= self.error_spike_threshold:
            self.on_anomaly({
                "kind": "error_spike",
                "code": code,
                "count": len(dq),
                "window_sec": self.error_window_sec,
                "level": 3,
                "ts": now,
            })
            dq.clear()
    
    def _handle_latency_drift(self, model: str, value_ms: float, now: float):
        """处理延迟漂移检测"""
        dq = self.latency_window[model]
        dq.append(value_ms)
        
        if len(dq) < 10:
            return
        
        avg = sum(dq) / len(dq)
        # 取前 3 个点作为"基线"
        baseline = sum(list(dq)[:3]) / 3.0
        if baseline <= 0:
            return
        
        if avg >= baseline * self.latency_drift_factor and avg > 200:
            self.on_anomaly({
                "kind": "latency_drift",
                "model": model,
                "avg_ms": avg,
                "baseline_ms": baseline,
                "factor": self.latency_drift_factor,
                "level": 2,
                "ts": now,
            })
            dq.clear()
    
    def check_stall(self):
        """定时调用，用于检测 stall"""
        now = time.time()
        for domain, timeout in self.stall_timeout_sec.items():
            last = self.last_seen.get(domain)
            if last is None:
                continue
            if now - last > timeout:
                self.on_anomaly({
                    "kind": "stall",
                    "domain": domain,
                    "last_seen": last,
                    "timeout_sec": timeout,
                    "level": 3,
                    "ts": now,
                })
                # 重置 last_seen，避免重复触发
                self.last_seen[domain] = now
