"""
Authority Confidence Sampler (v1.4.8 Step 8)

采样器：周期性采样并生成 Frame

核心职责：
- 周期性拉取当前 authority、最新 snapshot、FSM 状态
- 生成 Frame
- 交给 Store

采样频率：默认 2 Hz（每 0.5 秒）

强制插帧：
- FSM 状态变化 → 强制采样
- Authority 变化 → 强制采样
"""

from typing import Optional
import time
from navigation.authority_confidence_timeline import AuthorityConfidenceFrame
from navigation.authority_confidence_store import AuthorityConfidenceStore
from navigation.authority_takeover_fsm import AuthorityTakeoverFSM, TakeoverState


class AuthorityConfidenceSampler:
    """
    主权置信度采样器
    
    职责：
    - 定时采样（2Hz）
    - FSM 状态变化 → 强制采样
    - Authority 变化 → 强制采样
    """
    
    def __init__(
        self,
        store: AuthorityConfidenceStore,
        fsm: Optional[AuthorityTakeoverFSM] = None,
        sample_rate_hz: float = 2.0,
        enable_sampling: bool = True
    ):
        """
        初始化采样器
        
        Args:
            store: 存储对象
            fsm: FSM 实例（可选，用于获取状态）
            sample_rate_hz: 采样频率（Hz，默认 2.0 = 每 0.5 秒）
            enable_sampling: 是否启用采样（Feature Flag，默认 True）
        """
        self.store = store
        self.fsm = fsm
        self.sample_interval_s = 1.0 / sample_rate_hz if sample_rate_hz > 0 else 0.5
        self.enable_sampling = enable_sampling
        
        # 状态追踪（用于检测变化）
        self.last_sample_ts: float = 0.0
        self.last_takeover_state: Optional[str] = None
        self.last_active_authority: Optional[str] = None
    
    def sample(
        self,
        now_ts: float,
        active_authority: str,
        candidate_authority: Optional[str],
        scene: str,
        confidence: dict[str, float],
        hint_active: bool = False
    ) -> Optional[AuthorityConfidenceFrame]:
        """
        采样
        
        Args:
            now_ts: 当前时间戳
            active_authority: 当前活动主权
            candidate_authority: 候选主权（可选）
            scene: 当前场景
            confidence: 置信度字典 {"VISUAL": 0.8, "MAP_VISION": 0.6, "GPS": 0.3}
            hint_active: 是否有 Hint 激活
            
        Returns:
            AuthorityConfidenceFrame: 如果采样成功，返回 Frame；否则返回 None
        """
        if not self.enable_sampling:
            return None
        
        # 检查是否满足采样间隔（周期性采样）
        should_sample = False
        
        if now_ts - self.last_sample_ts >= self.sample_interval_s:
            should_sample = True
        
        # 检查 FSM 状态变化（强制插帧）
        current_takeover_state = None
        if self.fsm:
            current_takeover_state = self.fsm.current_state.value
            if current_takeover_state != self.last_takeover_state:
                should_sample = True
                self.last_takeover_state = current_takeover_state
        
        # 检查 Authority 变化（强制插帧）
        if active_authority != self.last_active_authority:
            should_sample = True
            self.last_active_authority = active_authority
        
        if not should_sample:
            return None
        
        # 生成 Frame
        frame = AuthorityConfidenceFrame(
            ts=now_ts,
            scene=scene,
            active_authority=active_authority,
            candidate_authority=candidate_authority,
            confidence=confidence.copy(),
            takeover_state=current_takeover_state or "UNKNOWN",
            hint_active=hint_active
        )
        
        # 存储 Frame
        self.store.store_frame(frame)
        
        # 更新最后采样时间
        self.last_sample_ts = now_ts
        
        return frame
    
    def force_sample(
        self,
        now_ts: float,
        active_authority: str,
        candidate_authority: Optional[str],
        scene: str,
        confidence: dict[str, float],
        hint_active: bool = False
    ) -> Optional[AuthorityConfidenceFrame]:
        """
        强制采样（忽略采样间隔）
        
        Args:
            同 sample() 方法
            
        Returns:
            AuthorityConfidenceFrame: 如果采样成功，返回 Frame；否则返回 None
        """
        if not self.enable_sampling:
            return None
        
        # 获取 FSM 状态
        current_takeover_state = None
        if self.fsm:
            current_takeover_state = self.fsm.current_state.value
        
        # 生成 Frame
        frame = AuthorityConfidenceFrame(
            ts=now_ts,
            scene=scene,
            active_authority=active_authority,
            candidate_authority=candidate_authority,
            confidence=confidence.copy(),
            takeover_state=current_takeover_state or "UNKNOWN",
            hint_active=hint_active
        )
        
        # 存储 Frame
        self.store.store_frame(frame)
        
        # 更新状态追踪
        self.last_sample_ts = now_ts
        self.last_takeover_state = current_takeover_state
        self.last_active_authority = active_authority
        
        return frame






