# -*- coding: utf-8 -*-
"""
A 方案：macOS 专用语音播报模块

- 基于系统命令 `say` + Ting-Ting 中文女声
- 不依赖 pyttsx3 / pydub / simpleaudio / sounddevice
- 特性：
    - 单播：新播报会先停掉上一条
    - 不叠音：不会同时放多条
    - 可中断：随时调用 stop() 终止当前播报
    - 非阻塞：不卡主主循环
"""

import logging
import platform
import subprocess
import threading
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class Voice:
    """
    对外统一的语音接口类

    说明：
    - 保留 speak(text, tts_manager=None) 签名，兼容之前调用方式
    - 内部实现完全改为 macOS `say`，不再使用 pyttsx3 / pydub 等
    """

    def __init__(self, voice_name: str = "Ting-Ting", rate: int = 180) -> None:
        """
        Args:
            voice_name: macOS 系统语音名称，默认 Ting-Ting（中文女声）
            rate: 语速（words per minute），建议 160~200
        """
        self._platform = platform.system()
        self._available = self._platform == "Darwin"
        self._voice_name = voice_name
        self._rate = rate

        self._lock = threading.Lock()
        self._current_proc: Optional[subprocess.Popen] = None

        if not self._available:
            logger.warning("[VoiceAV] 当前平台不是 macOS（Darwin），语音功能将禁用")
        else:
            logger.info(
                "[VoiceAV] 使用 macOS 系统语音: voice=%s, rate=%d",
                self._voice_name,
                self._rate,
            )

    # ===== 对外主接口 =====

    def speak(self, text: str, tts_manager: Optional[object] = None) -> bool:
        """
        播报文本（非阻塞）

        - 新的播报会先 stop 掉上一条
        - 不会阻塞主线程
        - tts_manager 参数仅为兼容占位，不使用
        """
        if not text:
            return False
        if not self._available:
            logger.debug("[VoiceAV] 语音不可用，跳过播报: %s", text)
            return False

        safe_text = text.strip()
        if not safe_text:
            return False

        try:
            with self._lock:
                # 先尝试停止上一条
                self._stop_locked()

                cmd = ["say", "-v", self._voice_name]
                if self._rate > 0:
                    cmd += ["-r", str(self._rate)]
                cmd.append(safe_text)

                logger.info("[VoiceAV] speak: %s", safe_text)
                # 非阻塞启动，由 macOS 负责实际播放
                self._current_proc = subprocess.Popen(
                    cmd,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            return True

        except Exception as e:
            logger.error("[VoiceAV] speak 失败: %s", e, exc_info=True)
            return False

    def stop(self) -> None:
        """
        停止当前播报
        """
        with self._lock:
            self._stop_locked()

    def is_speaking(self) -> bool:
        """
        检查当前是否正在播报
        
        Returns:
            bool: True 表示正在播报，False 表示未播报
        """
        if not self._available:
            return False
        
        with self._lock:
            if self._current_proc is None:
                return False
            # 检查进程是否还在运行
            return self._current_proc.poll() is None

    def _stop_locked(self) -> None:
        """内部方法：停止当前播报（已持有锁）"""
        if self._current_proc is not None:
            try:
                self._current_proc.terminate()
                self._current_proc.wait(timeout=0.5)
            except subprocess.TimeoutExpired:
                self._current_proc.kill()
            except Exception as e:
                logger.debug("[VoiceAV] stop 失败: %s", e)
            finally:
                self._current_proc = None

    def speak_and_wait(
        self, text: str, tts_manager: Optional[object] = None, timeout: Optional[float] = None
    ) -> bool:
        """
        播报文本并等待完成（阻塞）

        Args:
            text: 要播报的文本
            tts_manager: 兼容参数，不使用
            timeout: 超时时间（秒），None 表示不超时

        Returns:
            是否成功
        """
        if not text:
            return False
        if not self._available:
            logger.debug("[VoiceAV] 语音不可用，跳过播报: %s", text)
            return False

        safe_text = text.strip()
        if not safe_text:
            return False

        try:
            with self._lock:
                self._stop_locked()

                cmd = ["say", "-v", self._voice_name]
                if self._rate > 0:
                    cmd += ["-r", str(self._rate)]
                cmd.append(safe_text)

                logger.info("[VoiceAV] speak_and_wait: %s", safe_text)
                # 阻塞等待完成
                result = subprocess.run(
                    cmd,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=timeout,
                )
                return result.returncode == 0

        except subprocess.TimeoutExpired:
            logger.warning("[VoiceAV] speak_and_wait 超时: %s", safe_text)
            return False
        except Exception as e:
            logger.error("[VoiceAV] speak_and_wait 失败: %s", e, exc_info=True)
            return False

    @property
    def is_available(self) -> bool:
        """语音功能是否可用"""
        return self._available

    def get_info(self) -> Dict[str, Any]:
        """获取语音模块信息"""
        return {
            "available": self._available,
            "platform": self._platform,
            "voice_name": self._voice_name,
            "rate": self._rate,
        }

