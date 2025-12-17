"""
Vision Timeline Fixture

模拟真实"视觉节奏时间线"
"""

from dataclasses import dataclass
from typing import List, Callable, Dict, Any
import time


@dataclass
class VisionFrame:
    """
    视觉帧
    
    - state: 视觉状态（STABLE / TURNING / LOCKED / SEARCHING / UNSTABLE）
    - speed: 速度（m/s）
    - duration: 持续时间（秒）
    """
    state: str           # STABLE / TURNING / LOCKED / SEARCHING / UNSTABLE
    speed: float         # m/s
    duration: float      # seconds


def replay_vision_timeline(
    frames: List[VisionFrame],
    on_update: Callable[[Dict[str, Any]], None]
):
    """
    回放视觉节奏时间线
    
    Args:
        frames: 视觉帧列表
        on_update: 更新回调函数 (vision_context)
    """
    for i, frame in enumerate(frames):
        print(f"  [视觉帧 {i+1}/{len(frames)}] state={frame.state}, speed={frame.speed:.2f} m/s, duration={frame.duration:.1f}s")
        
        on_update({
            "vision_state": frame.state,
            "speed": frame.speed
        })
        
        if i < len(frames) - 1:  # 最后一帧不需要 sleep
            time.sleep(frame.duration)
