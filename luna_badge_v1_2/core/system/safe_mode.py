from dataclasses import dataclass
from typing import Optional, Callable


@dataclass
class SafeModeContext:
    obstacle_distance: Optional[float] = None


class SafeModeManager:
    def __init__(self, tts_say: Callable[[str], None]) -> None:
        self._active: bool = False
        self._tts_say = tts_say

    def enter(self) -> None:
        if not self._active:
            self._active = True
            self._tts_say("系统进入安全模式，请放慢脚步。")

    def exit(self) -> None:
        if self._active:
            self._active = False
            self._tts_say("系统退出安全模式，恢复正常。")

    def is_active(self) -> bool:
        return self._active

    def handle_frame(self, ctx: SafeModeContext) -> None:
        if not self._active:
            return
        if ctx.obstacle_distance is not None and ctx.obstacle_distance < 1.0:
            self._tts_say("前方一米内有障碍物，请小心。")
