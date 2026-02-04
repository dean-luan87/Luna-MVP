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

        - 会终止当前 Popen
        - 同时尝试 kill 系统所有 say 进程（双保险）
        """
        if not self._available:
            return
        with self._lock:
            logger.info("[VoiceAV] stop() 被调用，尝试停止当前播报")
            self._stop_locked()

    def is_speaking(self) -> bool:
        """
        当前是否有语音在播放
        """
        if not self._available:
            return False
        with self._lock:
            if self._current_proc is None:
                return False
            return self._current_proc.poll() is None

    def wait_until_done(self, timeout: Optional[float] = None) -> bool:
        """
        等待当前播放完成（阻塞）
        
        Args:
            timeout: 超时时间（秒），None 表示无限等待
        
        Returns:
            bool: True 表示播放完成，False 表示超时或出错
        """
        if not self._available:
            return False
        
        import time
        start_time = time.time()
        
        while True:
            if not self.is_speaking():
                return True
            
            if timeout is not None:
                elapsed = time.time() - start_time
                if elapsed >= timeout:
                    logger.warning(f"[VoiceAV] wait_until_done 超时（{timeout}秒）")
                    return False
            
            time.sleep(0.1)  # 每 100ms 检查一次

    def speak_and_wait(self, text: str, tts_manager: Optional[object] = None, timeout: Optional[float] = None) -> bool:
        """
        播报文本并等待完成（阻塞）
        
        适用于需要确保完整播放的场景（如测试脚本、重要提示等）
        
        Args:
            text: 要播报的文本
            tts_manager: 兼容参数，不使用
            timeout: 超时时间（秒），None 表示无限等待
        
        Returns:
            bool: True 表示播放成功并完成，False 表示失败或超时
        """
        if not self.speak(text, tts_manager):
            return False
        
        return self.wait_until_done(timeout=timeout)

    def get_status(self) -> Dict[str, Any]:
        """
        返回语音模块状态，供 main.py 打日志用
        """
        return {
            "engine": "macos-say",
            "platform": self._platform,
            "available": self._available,
            "speaking": self.is_speaking(),
            "voice": self._voice_name,
            "rate": self._rate,
        }

    # ===== 内部工具方法 =====

    def _stop_locked(self) -> None:
        """
        仅在持有 self._lock 时调用
        """
        # 1）先尝试结束当前 Popen
        if self._current_proc is not None:
            try:
                if self._current_proc.poll() is None:
                    self._current_proc.terminate()
                    try:
                        self._current_proc.wait(timeout=0.3)
                    except Exception:
                        self._current_proc.kill()
            except Exception:
                pass
            finally:
                self._current_proc = None

        # 2）双保险：杀掉系统级 say（避免残留）
        if self._platform == "Darwin":
            try:
                subprocess.run(
                    ["killall", "-q", "say"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            except Exception:
                # 没有 say 进程时会报错，忽略即可
                pass

