"""
TTS Manager module (v1.3).

语音播报抽象层：
- v1.3 增加 mode 参数，预留情绪化语音（安抚/紧张/提示等）
- 未来可接 edge-tts 或本地 TTS 引擎
"""


class TTSManager:
    def __init__(self, mode: str = "normal"):
        """
        v1.3 新增 mode 参数。
        mode: "normal" | "urgent" | "calm" | "alert" 等（预留）
        """
        self.mode = mode
        # TODO: 未来可注入具体 TTS 实现

    def speak(self, text: str) -> None:
        """
        播放语音（目前用打印代替）。
        v1.3 打印时显示 mode 信息。
        """
        if not text:
            return
        print(f"[TTS][{self.mode}] {text}")

