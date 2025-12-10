# -*- coding: utf-8 -*-
"""
Luna Badge 语音播报模块（B1：子进程 TTS 队列，基于 pyttsx3/nsss）

设计要点：
- 主进程绝不直接播放音频，只把文本丢给一个 TTS 子进程
- 子进程内部只维护一个 pyttsx3 引擎，顺序播报队列中的文本
- 串行播报：不会叠音
- 主进程退出时，子进程自动退出，不会留下残留播放
- 兼容旧接口：Voice.speak(text, tts_manager=None)
"""

import logging
import multiprocessing as mp
import platform
import queue
import threading
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)


# ===== 子进程端：TTS Worker ==================================================


@dataclass
class TTSMessage:
    """子进程消息结构"""

    type: str  # "SAY" / "STOP" / "EXIT"
    text: str = ""


def _select_best_voice(engine, worker_logger: logging.Logger) -> Optional[object]:
    """
    选择最合适的中文女声语音：

    优先级：
    1）名称包含 "ting-ting" / "tingting"（用户之前用的）
    2）中文女声（Sin-ji, Meijia 等）
    3）任意中文语音
    4）默认 voices[0]
    """
    try:
        voices = engine.getProperty("voices") or []
    except Exception as e:
        worker_logger.error(f"获取 voices 失败: {e}")
        return None

    if not voices:
        worker_logger.warning("系统中未找到任何 TTS 语音")
        return None

    # 统一小写名称方便匹配
    def voice_name(v) -> str:
        try:
            return (v.name or "").lower()
        except Exception:
            return ""

    # 1）优先精确匹配 Ting-Ting
    preferred_names = ("ting-ting", "tingting")
    for v in voices:
        name = voice_name(v)
        if any(p in name for p in preferred_names):
            worker_logger.info(f"首选中文女声: {v.name}")
            return v

    # 2）其它中文女声（通过名称启发式判断）
    female_keywords = ("female", "女", "sin-ji", "sinji", "meijia")
    chinese_keywords = ("zh", "chinese", "mandarin", "han", "中文", "普通话")
    for v in voices:
        name = voice_name(v)
        if any(k in name for k in chinese_keywords) and any(
            k in name for k in female_keywords
        ):
            worker_logger.info(f"次选中文女声: {v.name}")
            return v

    # 3）任意中文语音
    for v in voices:
        name = voice_name(v)
        if any(k in name for k in chinese_keywords + ("ting-ting", "tingting")):
            worker_logger.info(f"使用中文语音: {v.name}")
            return v

    # 4）兜底：默认语音
    v = voices[0]
    worker_logger.info(f"使用默认语音: {v.name}")
    return v


def _tts_worker_main(msg_queue: "mp.Queue") -> None:
    """
    子进程主循环：
    - 初始化 pyttsx3（nsss）
    - 持续从队列中取消息
    - 顺序播报 SAY 消息
    """
    import pyttsx3
    import time

    worker_logger = logging.getLogger("voice_worker")
    worker_logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    fmt = logging.Formatter(
        "[TTS-WORKER] %(asctime)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
    )
    handler.setFormatter(fmt)
    # 避免重复添加 handler
    if not worker_logger.handlers:
        worker_logger.addHandler(handler)

    worker_logger.info("TTS 子进程启动中...")

    try:
        # Mac 上强制使用 nsss 驱动
        if platform.system() == "Darwin":
            engine = pyttsx3.init(driverName="nsss")
            worker_logger.info("使用 nsss 驱动初始化 pyttsx3")
        else:
            engine = pyttsx3.init()
            worker_logger.info("使用默认驱动初始化 pyttsx3")

        # 基础参数
        engine.setProperty("rate", 150)
        engine.setProperty("volume", 1.0)  # 直接拉满，让系统音量来控制总输出

        # 选择语音
        selected = _select_best_voice(engine, worker_logger)
        if selected is not None:
            try:
                engine.setProperty("voice", selected.id)
                worker_logger.info(f"已设置语音: {selected.name}")
            except Exception as e:
                worker_logger.error(f"设置语音失败: {e}")
        else:
            worker_logger.warning("未能选择到合适语音，使用 pyttsx3 默认配置")

        # === 关键：预热，解决首句杂音 / 卡顿 / 无声 ===
        try:
            worker_logger.info("TTS 预热开始（静默 utterance）...")
            # 用一个"空格+短停顿"的极短语音做预热，用户几乎感知不到
            engine.say(" ")
            engine.runAndWait()
            worker_logger.info("TTS 预热完成")
        except Exception as e:
            worker_logger.warning(f"TTS 预热失败: {e}")

    except Exception as e:
        worker_logger.error(f"初始化 pyttsx3 失败，TTS 不可用: {e}")
        return

    worker_logger.info("TTS 子进程初始化完成，进入主循环")

    running = True
    while running:
        try:
            # 阻塞等待下一条消息，超时只是为了能响应 EXIT
            try:
                msg = msg_queue.get(timeout=0.5)
            except queue.Empty:
                continue

            if not isinstance(msg, TTSMessage):
                worker_logger.warning(f"收到未知消息类型: {msg}")
                continue

            if msg.type == "EXIT":
                worker_logger.info("收到 EXIT，准备退出")
                try:
                    engine.stop()
                except Exception:
                    pass
                running = False
                break

            if msg.type == "STOP":
                worker_logger.info("收到 STOP，打断当前播报")
                try:
                    engine.stop()
                except Exception:
                    pass
                continue

            if msg.type == "SAY":
                text = (msg.text or "").strip()
                if not text:
                    continue
                worker_logger.info(
                    f"开始播报 ({len(text)} 字符): {text[:50]}{'...' if len(text) > 50 else ''}"
                )
                try:
                    engine.say(text)
                    engine.runAndWait()
                    worker_logger.info("播报完成")
                except Exception as e:
                    worker_logger.error(f"播报失败: {e}")
                    # 出错后短暂休眠，避免疯狂重试
                    time.sleep(0.5)
                continue

            worker_logger.warning(f"收到未识别消息类型: {msg.type}")

        except KeyboardInterrupt:
            worker_logger.info("TTS 子进程收到 KeyboardInterrupt，退出")
            running = False
        except Exception as e:
            worker_logger.error(f"TTS 子进程主循环异常: {e}")

    worker_logger.info("TTS 子进程退出")


# ===== 主进程端：Voice 封装 ==================================================


class Voice:
    """
    主进程使用的语音接口：

    - speak(text, tts_manager=None): 提交一条 TTS 播报请求到子进程队列
    - stop(): 发送 STOP 消息打断当前播报
    - close()/__del__(): 发送 EXIT 消息，关闭 TTS 子进程
    """

    def __init__(self) -> None:
        self.logger = logger
        self.logger.info("[Voice] 初始化 TTS 子进程...")

        ctx = mp.get_context("spawn")  # macOS 必须使用 spawn
        self._queue = ctx.Queue()
        self._proc: Optional[mp.Process] = ctx.Process(
            target=_tts_worker_main,
            args=(self._queue,),
            daemon=True,
        )
        self._proc.start()

        self._alive = True
        self._lock = threading.Lock()

        self.logger.info(
            "[Voice] TTS 子进程已启动 pid=%s",
            self._proc.pid if self._proc is not None else "N/A",
        )

    # 对外接口 -------------------------------------------------------------

    def speak(self, text: str, tts_manager: Optional[object] = None) -> bool:
        """
        提交一条文本播报请求。

        为兼容旧代码保留 tts_manager 参数，但当前版本不使用。
        """
        text = (text or "").strip()
        if not text:
            return True

        with self._lock:
            if not self._alive or self._proc is None or not self._proc.is_alive():
                self.logger.warning("[Voice] TTS 子进程已不在，无法播报")
                return False
            try:
                msg = TTSMessage(type="SAY", text=text)
                self._queue.put_nowait(msg)
                # qsize 在部分平台可能不支持，这里做保护
                try:
                    qsize = self._queue.qsize()
                except (NotImplementedError, AttributeError):
                    qsize = -1
                if qsize >= 0:
                    self.logger.info(
                        "[Voice] TTS 请求已入队（队列大小=%d）: %s",
                        qsize,
                        (text[:50] + "...") if len(text) > 50 else text,
                    )
                else:
                    self.logger.info(
                        "[Voice] TTS 请求已入队: %s",
                        (text[:50] + "...") if len(text) > 50 else text,
                    )
                return True
            except Exception as e:
                self.logger.error(f"[Voice] 提交 TTS 请求失败: {e}")
                return False

    def play_audio(self, file_path: Optional[str]) -> bool:
        """
        播放已存在的音频文件（兼容接口，B1 方案不支持文件播放）
        """
        self.logger.warning("[Voice] B1 方案不支持 play_audio，请使用 speak()")
        return False

    def stop(self) -> None:
        """请求子进程停止当前播报"""
        with self._lock:
            if not self._alive or self._proc is None or not self._proc.is_alive():
                return
            try:
                self._queue.put_nowait(TTSMessage(type="STOP"))
                self.logger.info("[Voice] 已发送 STOP 请求给 TTS 子进程")
            except Exception as e:
                self.logger.error(f"[Voice] 发送 STOP 失败: {e}")

    def is_speaking(self) -> bool:
        """
        这里无法精确知道 pyttsx3 是否正在说话，
        简化处理：只要子进程活着，就认为"可用/可能在播报"。
        """
        with self._lock:
            return bool(self._proc and self._proc.is_alive())

    @property
    def is_available(self) -> bool:
        """
        语音模块是否可用（兼容旧接口）
        """
        with self._lock:
            return self._alive and bool(self._proc and self._proc.is_alive())

    def get_status(self) -> dict:
        with self._lock:
            alive = self._alive and bool(self._proc and self._proc.is_alive())
            return {
                "engine": "pyttsx3-subprocess",
                "platform": platform.system(),
                "alive": alive,
                "available": alive,  # 兼容旧接口，alive 即表示可用
            }

    # 生命周期管理 ---------------------------------------------------------

    def close(self) -> None:
        """显式关闭 TTS 子进程"""
        with self._lock:
            if not self._alive:
                return
            self._alive = False
            if self._proc is None or not self._proc.is_alive():
                return
            try:
                self._queue.put_nowait(TTSMessage(type="EXIT"))
                self.logger.info("[Voice] 已发送 EXIT 给 TTS 子进程")
            except Exception as e:
                self.logger.error(f"[Voice] 发送 EXIT 失败: {e}")
            try:
                self._proc.join(timeout=2.0)
            except Exception:
                pass

    def __del__(self) -> None:
        try:
            self.close()
        except Exception:
            pass
