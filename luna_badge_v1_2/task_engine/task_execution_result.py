"""
TaskExecutionResult: 统一的任务执行结果结构

用于封装 AskChain 和 TaskChain 的执行结果，提供统一的响应接口。
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List

from task_engine.tts import Utterance, tts_manager


@dataclass
class TaskExecutionResult:
    """
    统一的任务执行结果结构。

    用于 TaskChainManager.handle_user_turn() 的返回值，
    封装 AskChain 和 TaskChain 的执行状态和输出。

    ask_active:
        当前是否有活跃的 AskChain 正在执行。

    task_active:
        当前是否有活跃的 TaskChain 正在执行。

    ask_output:
        AskChain 的输出消息（prompt / retry / 完成提示）。

    task_output:
        TaskChain 的输出消息（执行结果 / 状态更新）。

    task_finished:
        主任务链是否已完成。

    phase:
        当前执行阶段："ask" 或 "task"。

    status:
        可选的状态标记，如 "ask_failed", "task_paused" 等。
    """

    ask_active: bool
    task_active: bool
    ask_output: Optional[str] = None
    task_output: Optional[str] = None
    task_finished: bool = False
    phase: str = "task"  # "ask" or "task"
    status: Optional[str] = None
    
    # --- A-5-4-4 新增：暂停相关 ---
    paused: bool = False
    pause_type: Optional[str] = None  # "user" / "system" / "temporary"
    
    # 预留元数据
    meta: Optional[Dict[str, Any]] = field(default_factory=dict)
    
    # --- P5-2 新增：TTS 输出列表（每次 step() 的播报队列） ---
    utterances: List[Utterance] = field(default_factory=list)
    
    # --- P5-3-D 新增：Scene 融合输出 ---
    scene_snapshot: Optional[Dict[str, Any]] = None  # 当前场景信息（tag / scene_id / context）
    scene_trace: List[Dict[str, Any]] = field(default_factory=list)  # 场景变化历史（进入/退出/事件）
    
    # --- P5-2 便捷方法：添加单条 TTS 文本 ---
    def add_utterance(
        self,
        text: str,
        level: str = "info",
        channel: str = "tts",
        **meta,
    ) -> Utterance:
        """
        添加一条待播报的文本。

        Args:
            text: 要播报的文本
            level: 消息级别（info / warning / error / debug / system）
            channel: 输出通道（tts / log / screen / hmi 等）
            **meta: 扩展元数据

        Returns:
            Utterance: 创建的 Utterance 实例
        """
        u = Utterance(text=text, level=level, channel=channel, meta=meta)
        self.utterances.append(u)
        return u
    
    # --- P5-2 便捷方法：添加多个 Utterance ---
    def extend_utterances(self, uts: List[Utterance]) -> None:
        """
        添加多个 Utterance 到队列。

        Args:
            uts: Utterance 列表
        """
        self.utterances.extend(uts)
    
    # --- P5-2 便捷方法：从全局 tts_manager 拉取并清空队列 ---
    def pop_utterances_from_tts_manager(self) -> List[Utterance]:
        """
        从全局 tts_manager 拉取并清空队列，添加到当前结果中。

        Returns:
            List[Utterance]: 拉取的 Utterance 列表
        """
        uts = tts_manager.pop_all()
        self.extend_utterances(uts)
        return uts

    def to_dict(self) -> dict:
        """转换为字典格式，便于序列化和调试。"""
        data = {
            "ask_active": self.ask_active,
            "task_active": self.task_active,
            "ask_output": self.ask_output,
            "task_output": self.task_output,
            "task_finished": self.task_finished,
            "phase": self.phase,
            "status": self.status,
            "paused": self.paused,
            "pause_type": self.pause_type,
            "meta": self.meta or {},
        }
        # P5-2 新增：序列化 utterances
        data["utterances"] = [u.to_dict() for u in self.utterances]
        # P5-3-D 新增：序列化场景信息
        data["scene_snapshot"] = self.scene_snapshot
        data["scene_trace"] = self.scene_trace
        return data

