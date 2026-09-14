"""
World Accumulator v0.2 - 世界稳定度判断（先做简单版）

职责：
- 世界去抖动
- 世界稳定判断
- 支撑"上帝视角"
"""

from typing import Optional
from .world_snapshot import WorldSnapshot


class WorldAccumulator:
    """
    B2 世界累积器 v0.2
    
    核心职责：
    - 世界稳定度判断（基于对象数 + 文本数）
    - 世界去抖动（滑动窗口）
    """
    
    def __init__(self, stable_obj_iou_th: float = 0.5, stable_min_frames: int = 10):
        """
        初始化世界累积器
        
        Args:
            stable_obj_iou_th: 稳定对象 IoU 阈值（暂未使用）
            stable_min_frames: 稳定最小帧数
        """
        self._last: Optional[tuple] = None
        self._stable_frames: int = 0
        self.stable_obj_iou_th = stable_obj_iou_th
        self.stable_min_frames = stable_min_frames
    
    def update(self, world_snapshot: WorldSnapshot) -> bool:
        """
        更新世界快照，判断是否稳定
        
        v0.2：先用"对象数 + 文本数 + 轻量 hash"判断稳定
        
        Args:
            world_snapshot: 世界快照
        
        Returns:
            bool: 是否稳定
        """
        # 计算签名（对象数 + 文本数）
        sig = (len(world_snapshot.objects), len(world_snapshot.texts))
        
        if self._last == sig:
            # 签名相同，稳定帧数 +1
            self._stable_frames += 1
        else:
            # 签名变化，重置稳定帧数
            self._stable_frames = 0
            self._last = sig
        
        # 如果稳定帧数 >= 最小帧数，认为稳定
        return self._stable_frames >= self.stable_min_frames

