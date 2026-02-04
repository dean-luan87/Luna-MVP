"""
Authority Confidence Store (v1.4.8 Step 8)

存储策略：内存 RingBuffer

核心设计：
- v1.4.8 只做内存 RingBuffer
- 不落盘、不跨进程、不持久化
- 滑动窗口，永不无限增长
"""

from typing import Optional
from navigation.authority_confidence_timeline import (
    AuthorityConfidenceFrame,
    AuthorityConfidenceTimeline
)


class AuthorityConfidenceStore:
    """
    主权置信度存储（内存 RingBuffer）
    
    职责：
    - 管理 Timeline 的存储
    - 实现 RingBuffer（滑动窗口）
    - 确保内存上限
    """
    
    def __init__(self, max_frames: int = 300):
        """
        初始化存储
        
        Args:
            max_frames: 最大帧数（默认 300，约 150 秒 @ 2Hz）
        """
        self.timeline = AuthorityConfidenceTimeline(max_frames=max_frames)
        self.max_frames = max_frames
    
    def store_frame(self, frame: AuthorityConfidenceFrame) -> None:
        """
        存储帧
        
        Args:
            frame: 时间轴帧
        """
        self.timeline.add_frame(frame)
    
    def get_timeline(self) -> AuthorityConfidenceTimeline:
        """获取 Timeline 对象"""
        return self.timeline
    
    def get_frames(
        self,
        start_ts: Optional[float] = None,
        end_ts: Optional[float] = None
    ) -> list[AuthorityConfidenceFrame]:
        """
        获取时间范围内的帧
        
        Args:
            start_ts: 开始时间戳（可选）
            end_ts: 结束时间戳（可选）
            
        Returns:
            时间范围内的帧列表
        """
        return self.timeline.get_frames(start_ts=start_ts, end_ts=end_ts)
    
    def get_stats(self) -> dict:
        """获取统计信息"""
        return self.timeline.get_stats()






