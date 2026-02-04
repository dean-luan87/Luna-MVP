"""
Navigation Context (v1.3.0)

导航任务上下文

记录导航任务的关键信息
"""

import time
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field


@dataclass
class NavigationContext:
    """
    导航任务上下文

    记录整个导航任务的关键信息
    """

    # 目标信息
    target: str = ""                    # 目标名称，如"711便利店"
    target_location: Optional[List[float]] = None  # 目标位置 [lat, lon] 或 [楼层, 区域]
    route_id: Optional[str] = None      # 路线ID（若从地图API规划出来）

    # 时间信息
    start_time: float = field(default_factory=time.time)  # 开始时间
    pause_time: Optional[float] = None  # 暂停时间
    resume_time: Optional[float] = None  # 恢复时间
    end_time: Optional[float] = None    # 结束时间

    # 进度信息
    progress: Dict[str, Any] = field(default_factory=dict)  # 进度信息
    current_step: int = 0               # 当前步骤索引

    # 视觉和决策信息
    last_frame: Optional[Any] = None     # 上一帧图像（可选，用于调试）
    last_nav_decision: Optional[Dict[str, Any]] = None  # 上一次导航决策
    last_speech_event: Optional[Dict[str, Any]] = None  # 上一次语音事件

    # 统计信息
    frame_count: int = 0                 # 处理的帧数
    decision_count: Dict[str, int] = field(default_factory=dict)  # 各决策类型的计数

    # 扩展字段（预留未来功能）
    meta: Dict[str, Any] = field(default_factory=dict)  # 元数据

    def to_dict(self) -> Dict[str, Any]:
        """
        转换为字典

        Returns:
            dict: 上下文字典
        """
        return {
            "target": self.target,
            "target_location": self.target_location,
            "route_id": self.route_id,
            "start_time": self.start_time,
            "pause_time": self.pause_time,
            "resume_time": self.resume_time,
            "end_time": self.end_time,
            "progress": self.progress,
            "current_step": self.current_step,
            "frame_count": self.frame_count,
            "decision_count": self.decision_count,
            "meta": self.meta,
        }

    def update_decision(self, nav_decision: Dict[str, Any]):
        """
        更新导航决策

        Args:
            nav_decision: 导航决策字典
        """
        self.last_nav_decision = nav_decision
        decision_type = nav_decision.get("decision", "UNKNOWN")
        self.decision_count[decision_type] = self.decision_count.get(decision_type, 0) + 1

    def update_speech_event(self, speech_event: Optional[Dict[str, Any]]):
        """
        更新语音事件

        Args:
            speech_event: 语音事件字典（可为 None）
        """
        self.last_speech_event = speech_event

    def get_duration(self) -> float:
        """
        获取导航持续时间（秒）

        Returns:
            float: 持续时间
        """
        end = self.end_time or time.time()
        return end - self.start_time

    def get_active_duration(self) -> float:
        """
        获取实际导航时间（排除暂停时间）

        Returns:
            float: 实际导航时间
        """
        # 简化计算：如果有暂停时间，减去暂停时长
        # 实际应该记录所有暂停/恢复时间点
        if self.pause_time and self.resume_time:
            pause_duration = self.resume_time - self.pause_time
            return self.get_duration() - pause_duration
        return self.get_duration()
























