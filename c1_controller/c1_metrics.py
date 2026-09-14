"""
C1 效能评估（Metrics）

C1 的效能评估指标：
- avg_pipeline_fps: Pipeline 实际执行频率
- modeling_execution_ratio: ModelingExecutor 执行占比
- suspended_ratio: 视觉暂停占比
- decision_latency: C1 决策耗时
"""

import time
from typing import Dict, Any, Optional
from collections import deque


class C1Metrics:
    """
    C1 效能评估器
    
    职责：
    - 记录 C1 的关键指标
    - 计算统计值
    - 不侵入业务逻辑
    """
    
    def __init__(self, window_size: int = 1000):
        """
        初始化 C1 效能评估器
        
        Args:
            window_size: 滑动窗口大小（用于计算平均值）
        """
        self.window_size = window_size
        
        # 指标记录（使用滑动窗口）
        self._allow_frame_history = deque(maxlen=window_size)
        self._target_fps_history = deque(maxlen=window_size)
        self._priority_history = deque(maxlen=window_size)
        self._modeling_executed_history = deque(maxlen=window_size)
        self._decision_latency_history = deque(maxlen=window_size)
        
        # 时间戳记录（用于计算 fps）
        self._frame_timestamps = deque(maxlen=window_size)
    
    def record(
        self,
        allow_frame: bool,
        target_fps: int,
        priority: str,
        modeling_executed: bool,
        decision_latency: Optional[float] = None,
    ) -> None:
        """
        记录 C1 指标
        
        Args:
            allow_frame: 是否允许抽帧
            target_fps: 目标 fps
            priority: 优先级
            modeling_executed: ModelingExecutor 是否执行
            decision_latency: C1 决策耗时（可选）
        """
        now = time.time()
        
        self._allow_frame_history.append(allow_frame)
        self._target_fps_history.append(target_fps)
        self._priority_history.append(priority)
        self._modeling_executed_history.append(modeling_executed)
        
        if decision_latency is not None:
            self._decision_latency_history.append(decision_latency)
        
        # 只记录允许的帧的时间戳（用于计算实际 fps）
        if allow_frame:
            self._frame_timestamps.append(now)
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        获取当前指标
        
        Returns:
            指标字典
        """
        metrics = {}
        
        # 1. avg_pipeline_fps: Pipeline 实际执行频率
        if len(self._frame_timestamps) >= 2:
            time_span = self._frame_timestamps[-1] - self._frame_timestamps[0]
            if time_span > 0:
                metrics["avg_pipeline_fps"] = (len(self._frame_timestamps) - 1) / time_span
            else:
                metrics["avg_pipeline_fps"] = 0.0
        else:
            metrics["avg_pipeline_fps"] = 0.0
        
        # 2. modeling_execution_ratio: ModelingExecutor 执行占比
        if len(self._modeling_executed_history) > 0:
            metrics["modeling_execution_ratio"] = sum(self._modeling_executed_history) / len(self._modeling_executed_history)
        else:
            metrics["modeling_execution_ratio"] = 0.0
        
        # 3. suspended_ratio: 视觉暂停占比
        if len(self._allow_frame_history) > 0:
            metrics["suspended_ratio"] = 1.0 - (sum(self._allow_frame_history) / len(self._allow_frame_history))
        else:
            metrics["suspended_ratio"] = 0.0
        
        # 4. decision_latency: C1 决策耗时
        if len(self._decision_latency_history) > 0:
            metrics["avg_decision_latency"] = sum(self._decision_latency_history) / len(self._decision_latency_history)
            metrics["max_decision_latency"] = max(self._decision_latency_history)
            metrics["min_decision_latency"] = min(self._decision_latency_history)
        else:
            metrics["avg_decision_latency"] = 0.0
            metrics["max_decision_latency"] = 0.0
            metrics["min_decision_latency"] = 0.0
        
        # 5. 平均 target_fps
        if len(self._target_fps_history) > 0:
            metrics["avg_target_fps"] = sum(self._target_fps_history) / len(self._target_fps_history)
        else:
            metrics["avg_target_fps"] = 0.0
        
        # 6. 优先级分布
        priority_counts = {}
        for priority in self._priority_history:
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
        metrics["priority_distribution"] = priority_counts
        
        return metrics
    
    def reset(self) -> None:
        """重置所有指标"""
        self._allow_frame_history.clear()
        self._target_fps_history.clear()
        self._priority_history.clear()
        self._modeling_executed_history.clear()
        self._decision_latency_history.clear()
        self._frame_timestamps.clear()


