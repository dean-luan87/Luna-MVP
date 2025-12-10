from typing import Callable
from infra.logging_manager import get_logger

logger = get_logger("speech")


class DummyASR:
    """
    demo 用 ASR：这里不做真实识别，只是读取标准输入。
    真机替换为 whisper / 设备 ASR。
    """

    def listen(self):
        try:
            text = input()
        except EOFError:
            return None
        return text


class DummyTTS:
    """
    demo 用 TTS：直接 print 文本。
    """

    def speak(self, text: str) -> None:
        logger.info(f"[TTS] {text}")


class SpeechPipeline:
    def __init__(
        self,
        asr: DummyASR,
        tts: DummyTTS,
        query_bus,
        intent_parser,
    ) -> None:
        self.asr = asr
        self.tts = tts
        self.query_bus = query_bus
        self.intent_parser = intent_parser

    def loop(self) -> None:
        while True:
            text = self.asr.listen()
            if text is None or not text.strip():
                continue

            if self.query_bus.has_active_query():
                parsed = self.intent_parser.parse(text)
                self.query_bus.resolve_active(parsed)
                continue

            parsed = self.intent_parser.parse(text)
            self._handle_normal_command(parsed)

    def _handle_normal_command(self, parsed: dict) -> None:
        intent = parsed.get("intent")
        if intent == "stop_navigation":
            self.tts.speak("收到，后来由导航模块处理停止逻辑。")
        elif intent == "start_navigation":
            self.tts.speak("收到，可以开始或继续导航。")
        elif intent == "unknown":
            self.tts.speak("我听到了，但暂时还不支持这个指令。")

