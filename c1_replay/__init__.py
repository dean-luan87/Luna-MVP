"""
C1 Replay Tool（C1 回访工具）

工具定位：
C1 回访工具不是 Debug 工具，而是"事后理解 Luna 当时为什么这么看、这么决策"的系统级审计与复盘工具。

它服务的对象不是模型，而是：
- 决策机制
- 抽帧策略
- 状态切换逻辑
- 安全兜底是否生效

这是后面能放心升级 C1 / C2 / C3 的基础设施。
"""

from .replay_models import C1DecisionRecord, PipelineExecutionRecord
from .replay_loader import load_c1_logs
from .replay_engine import C1ReplayEngine
from .replay_report import generate_summary, print_timeline, print_summary

__all__ = [
    "C1DecisionRecord",
    "PipelineExecutionRecord",
    "load_c1_logs",
    "C1ReplayEngine",
    "generate_summary",
    "print_timeline",
    "print_summary",
]
