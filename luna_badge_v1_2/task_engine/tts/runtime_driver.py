"""
TTS Runtime Driver: TTS 运行时驱动层

职责：
- 从 TtsManager 的队列中取出 Utterance
- 按顺序执行播报（当前为 Stub，可替换为真实 TTS 实现）
- 支持单步处理（process_once），方便测试
- 支持后台线程循环（start/stop），方便在设备上常驻运行
"""

import threading
import time
from typing import Optional, List

from .tts_manager import TtsManager, tts_manager
from .utterance import Utterance


class TTSRuntimeDriver:
    """
    TTS Runtime Driver

    职责：
    - 从 TtsManager 的队列中取出 Utterance
    - 通过 _speak_utterance 执行播报（当前为 Stub，可替换为真实 TTS 实现）
    - 支持单步处理（process_once），方便测试和同步调用
    - 支持后台线程循环（start/stop），方便在设备上常驻运行

    优先级 / 打断策略（Patch-G + Patch-H）：
    - 实际的优先级排序由 TtsManager.pop_all() 处理；
    - 若本轮队列中存在 interrupt=True 的 Utterance：
        - 仅播报"最高优先级"的那一条（pop_all 后的第一个 interrupt=True）；
        - 其余 Utterance 本轮丢弃（视为被高优先级语音打断）。
      这样实现"强插队 + 软打断"语义。
    - 若不存在 interrupt=True：
        - 按排序结果依次播报全部 Utterance。
    """

    def __init__(
        self,
        manager: Optional[TtsManager] = None,
        loop_interval: float = 0.1,
    ) -> None:
        """
        初始化 TTS Runtime Driver

        Args:
            manager: 使用的 TtsManager 实例，默认使用模块级 tts_manager
            loop_interval: 循环处理的时间间隔（秒）
        """
        self._manager: TtsManager = manager or tts_manager
        self._loop_interval: float = loop_interval

        self._running: bool = False
        self._thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # 状态查询
    # ------------------------------------------------------------------

    @property
    def is_running(self) -> bool:
        """检查驱动是否正在运行"""
        with self._lock:
            return self._running

    # ------------------------------------------------------------------
    # 启停控制（后台线程）
    # ------------------------------------------------------------------

    def start(self) -> None:
        """
        启动后台处理线程。如果已在运行，则不重复启动。
        """
        with self._lock:
            if self._running:
                return
            self._running = True

        t = threading.Thread(target=self._process_loop, daemon=True)
        self._thread = t
        t.start()

    def stop(self, timeout: float = 1.0) -> None:
        """
        停止后台处理线程，并等待其退出。

        Args:
            timeout: 等待线程退出的超时时间（秒）
        """
        with self._lock:
            self._running = False

        t = self._thread
        if t is not None and t.is_alive():
            t.join(timeout=timeout)

    # ------------------------------------------------------------------
    # 主循环（内部）
    # ------------------------------------------------------------------

    def _process_loop(self) -> None:
        """
        后台线程循环，从队列中消费 Utterance。
        """
        while True:
            with self._lock:
                if not self._running:
                    break

            self.process_once()
            time.sleep(self._loop_interval)

    # ------------------------------------------------------------------
    # 单次处理（对外公开，便于测试和手动驱动）
    # ------------------------------------------------------------------

    def process_once(self) -> None:
        """
        从队列中取出下一条 Utterance 并执行播报。

        Step 12: 使用 PriorityScheduler 统一调度，每次只处理一条。

        该方法是无状态的，一次调用仅处理一条 Utterance。
        """
        # Step 12: 使用 pop_next() 获取下一条要播报的 Utterance
        utter = self._manager.pop_next()
        if utter is None:
            return

        # 分配一个 play_id 便于后续追踪
        if not hasattr(self, '_last_play_id'):
            self._last_play_id = 0
        self._last_play_id += 1
        utter.play_id = f"tts_{self._last_play_id}"

        # 容错：若不是 Utterance，则包装（理论上不会发生）
        if not isinstance(utter, Utterance):
            utter = Utterance(text=str(utter))

        self._speak_utterance(utter)

    # ------------------------------------------------------------------
    # 实际的"播放逻辑"（当前为 Stub，可被 monkeypatch / 继承覆盖）
    # ------------------------------------------------------------------

    def _speak_utterance(self, utter: Utterance) -> None:
        """
        执行实际的 TTS 播报。

        当前实现：
        - 使用 print 作为占位实现，便于本地调试和日志观察
        - 真实环境中，可以在这里调用 SoVITS / Edge TTS / 硬件 TTS 等

        Args:
            utter: 待播报的 Utterance 实例
        """
        # NOTE: 真正落地时，这里换成设备 TTS 调用即可
        from .priority_bands import PriorityBand
        band = PriorityBand.from_priority(utter.priority)
        print(f"[TTS][{utter.level}][prio={utter.priority}][band={band.name}]"
              f"[id={utter.play_id}] {utter.text}")

