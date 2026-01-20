"""
C1 Decision Logger

只用于 C1 决策级日志节律统计

职责：
- 只记录 C1 产生"有效决策事件"的时间戳
- 不记录每帧、debug、executor skip
- 只记录「我作为 C1 做了一次判断」
"""

import time
from typing import List, Optional


class C1DecisionLogger:
    """
    只用于 C1 决策级日志节律统计
    
    只记录三类事件：
    - C1_DECISION: 每次状态机更新产生有效决策
    - C1_STATE_TRANSITION: 状态变化
    - C1_PROTECTION_EVENT: Protection 进入/退出
    """
    
    def __init__(self):
        """初始化决策日志记录器"""
        self.decision_timestamps: List[float] = []
        self.state_transition_timestamps: List[float] = []
        self.protection_event_timestamps: List[float] = []
    
    def record_decision(self, timestamp: Optional[float] = None):
        """
        只在 C1 产生"有效决策事件"时调用
        
        Args:
            timestamp: 时间戳（如果为 None，使用当前时间）
        """
        if timestamp is None:
            timestamp = time.time()
        self.decision_timestamps.append(timestamp)
    
    def record_state_transition(self, timestamp: Optional[float] = None):
        """
        记录状态切换事件
        
        Args:
            timestamp: 时间戳（如果为 None，使用当前时间）
        """
        if timestamp is None:
            timestamp = time.time()
        self.state_transition_timestamps.append(timestamp)
    
    def record_protection_event(self, timestamp: Optional[float] = None):
        """
        记录 Protection 事件（进入或退出）
        
        Args:
            timestamp: 时间戳（如果为 None，使用当前时间）
        """
        if timestamp is None:
            timestamp = time.time()
        self.protection_event_timestamps.append(timestamp)
    
    def get_all_timestamps(self) -> List[float]:
        """
        获取所有 C1 决策时间戳（合并三类事件，去重并排序）
        
        Returns:
            排序后的时间戳列表
        """
        all_timestamps = (
            self.decision_timestamps +
            self.state_transition_timestamps +
            self.protection_event_timestamps
        )
        return sorted(set(all_timestamps))
    
    def get_decision_timestamps(self) -> List[float]:
        """获取 C1_DECISION 时间戳"""
        return self.decision_timestamps
    
    def get_state_transition_timestamps(self) -> List[float]:
        """获取 C1_STATE_TRANSITION 时间戳"""
        return self.state_transition_timestamps
    
    def get_protection_event_timestamps(self) -> List[float]:
        """获取 C1_PROTECTION_EVENT 时间戳"""
        return self.protection_event_timestamps

