"""
Authority Confidence Timeline (v1.4.8 Step 8)

重要禁令：
- Step 8 不参与决策，不影响体验，不接管系统
- 只做一件事：把已经发生的"判断依据"结构化保存下来
- 默认开启，但可通过配置关闭
- 内存上限必须生效

核心原则：
- 只记录"解释所必需的最小信息"
- 时间是第一维度（连续轨迹）
- 可关闭、可裁剪、可回放
"""

from dataclasses import dataclass, asdict
from typing import Optional, Dict
import time


@dataclass
class AuthorityConfidenceFrame:
    """
    Timeline Entry（核心数据结构）
    
    注意：不是完整 Snapshot，只保留 confidence 数值
    """
    ts: float                           # 时间戳
    scene: str                          # 当前场景
    
    # 主权视角
    active_authority: str              # 当前活动主权
    candidate_authority: Optional[str]  # 候选主权（如果有）
    
    # Step 5 Snapshot（裁剪版，只保留 confidence 数值）
    confidence: Dict[str, float]       # {"VISUAL": 0.8, "MAP_VISION": 0.6, "GPS": 0.3}
    
    # FSM 状态
    takeover_state: str                # IDLE / CANDIDATE / LOCKING / TAKEN / COOLDOWN
    
    # 可选字段
    hint_active: bool = False          # 是否有 Hint 激活
    
    def to_dict(self) -> Dict:
        """转换为字典（用于序列化）"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> "AuthorityConfidenceFrame":
        """从字典创建（用于反序列化）"""
        return cls(**data)


class AuthorityConfidenceTimeline:
    """
    主权置信度时间轴管理器
    
    职责：
    - 管理 Timeline 的存储
    - 提供查询接口
    - 确保内存上限
    """
    
    def __init__(self, max_frames: int = 300):
        """
        初始化时间轴管理器
        
        Args:
            max_frames: 最大帧数（默认 300，约 150 秒 @ 2Hz）
        """
        self.max_frames = max_frames
        self._frames: list[AuthorityConfidenceFrame] = []
        self._frame_count = 0
    
    def add_frame(self, frame: AuthorityConfidenceFrame) -> None:
        """
        添加帧
        
        如果超过 max_frames，自动丢弃最旧的数据
        
        Args:
            frame: 时间轴帧
        """
        self._frames.append(frame)
        self._frame_count += 1
        
        # 如果超过上限，移除最旧的帧
        if len(self._frames) > self.max_frames:
            self._frames.pop(0)
    
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
        if not self._frames:
            return []
        
        if start_ts is None and end_ts is None:
            return self._frames.copy()
        
        filtered = []
        for frame in self._frames:
            if start_ts is not None and frame.ts < start_ts:
                continue
            if end_ts is not None and frame.ts > end_ts:
                continue
            filtered.append(frame)
        
        return filtered
    
    def get_latest_frame(self) -> Optional[AuthorityConfidenceFrame]:
        """获取最新的帧"""
        return self._frames[-1] if self._frames else None
    
    def get_oldest_frame(self) -> Optional[AuthorityConfidenceFrame]:
        """获取最旧的帧"""
        return self._frames[0] if self._frames else None
    
    def size(self) -> int:
        """获取当前帧数"""
        return len(self._frames)
    
    def clear(self) -> None:
        """清空时间轴"""
        self._frames.clear()
        self._frame_count = 0
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        if not self._frames:
            return {
                "frame_count": 0,
                "oldest_ts": None,
                "newest_ts": None,
                "duration_s": 0.0
            }
        
        oldest = self._frames[0].ts
        newest = self._frames[-1].ts
        
        return {
            "frame_count": len(self._frames),
            "oldest_ts": oldest,
            "newest_ts": newest,
            "duration_s": newest - oldest if newest > oldest else 0.0
        }






