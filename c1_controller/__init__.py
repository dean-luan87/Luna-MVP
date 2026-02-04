"""
C1: Continuous Vision Controller（连续视觉调度中台）

工程定位：
C1 不是一个模型，也不是一个算法，而是一个"视觉是否工作、如何工作"的调度与安全控制系统。

它站在 Vision Pipeline 之前，决定：
- 是否允许抽帧
- 抽哪一帧
- 抽多少
- 是否暂停视觉
- 是否强制安全优先

关键原则：
- C1 不做识别，只做"是否看、怎么看"
- C1 有权短路整个视觉链路
- C1 在 PipelineController 之前
"""

from .c1_controller import C1Controller
from .c1_types import C1Input, C1Decision
from .c1_state import C1State
from .c1_governor import FrameRateGovernor
from .c1_logger import C1Logger, C1LogRecord
from .c1_metrics import C1Metrics
from .c1_replay import C1Replay

__all__ = [
    "C1Controller",
    "C1Input",
    "C1Decision",
    "C1State",
    "FrameRateGovernor",
    "C1Logger",
    "C1LogRecord",
    "C1Metrics",
    "C1Replay",
]
