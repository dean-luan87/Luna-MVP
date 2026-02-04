import logging
import threading
import time
from typing import Optional

import numpy as np
import sounddevice as sd
import soundfile as sf


class SoundEngine:
    """
    基于 sounddevice 的音频播放引擎
    - 仅负责"播放已经存在的音频文件"（wav）
    - 不负责 TTS 文本转语音（由上层模块处理）
    - 提供：play / stop / is_playing / set_volume

    设计目标：
    1. 播放行为完全在本进程内可控，不依赖 afplay 等系统播放器
    2. 支持随时 stop()，立即中断播放
    3. 避免多路叠音（内部串行播放）
    """

    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        self.logger = logger or logging.getLogger(__name__)
        self._lock = threading.Lock()
        self._play_thread: Optional[threading.Thread] = None
        self._stop_flag = threading.Event()
        self._is_playing = False
        self._volume = 1.0

    # 对外接口 -----------------------------------------------------------------

    def play_file(self, file_path: str, volume: float = 1.0) -> bool:
        """
        播放指定音频文件（wav），非阻塞，内部起线程
        """
        if not file_path:
            self.logger.warning("[SoundEngine] play_file 收到空路径，跳过")
            return False

        with self._lock:
            # 强制停止之前的播放
            self._internal_stop_locked()
            self._stop_flag.clear()
            self._volume = max(0.0, min(volume, 1.0))
            self._is_playing = True

            t = threading.Thread(target=self._play_worker, args=(file_path,))
            t.daemon = True
            self._play_thread = t
            t.start()

        self.logger.info(f"[SoundEngine] 开始播放文件: {file_path}")
        return True

    def stop(self) -> None:
        """
        停止当前播放（如果有）
        """
        with self._lock:
            self._internal_stop_locked()

    def is_playing(self) -> bool:
        """
        是否有正在播放的任务
        """
        with self._lock:
            return self._is_playing

    def set_volume(self, volume: float) -> None:
        """
        设置当前播放音量（0.0 ~ 1.0），仅影响后续 chunk
        """
        with self._lock:
            self._volume = max(0.0, min(volume, 1.0))

    # 内部实现 -----------------------------------------------------------------

    def _internal_stop_locked(self) -> None:
        """
        内部停止逻辑（假定已持有 self._lock）
        """
        if self._play_thread is None:
            self._is_playing = False
            self._stop_flag.clear()
            return

        try:
            self._stop_flag.set()
        except Exception:
            # 防御性处理
            pass

        try:
            # 尝试等待线程结束，最多 1 秒
            self._play_thread.join(timeout=1.0)
        except Exception:
            pass

        # 停止底层 sounddevice 流
        try:
            sd.stop()
        except Exception:
            pass

        self._play_thread = None
        self._is_playing = False
        self._stop_flag.clear()
        self.logger.info("[SoundEngine] 已停止当前播放")

    def _play_worker(self, file_path: str) -> None:
        """
        播放线程：以块的形式向 sounddevice 输出，支持 stop() 中断
        """
        try:
            # 读取音频文件为 float32 数组
            data, samplerate = sf.read(file_path, dtype="float32")
            if data.ndim == 1:
                # 单声道情况统一扩展为 (N, 1)
                data = np.expand_dims(data, axis=1)

            channels = data.shape[1]
            block_size = 1024  # 每次写入的帧数

            self.logger.debug(
                f"[SoundEngine] 打开输出流: {samplerate} Hz, {channels} ch, blocks={block_size}"
            )

            with sd.OutputStream(
                samplerate=samplerate,
                channels=channels,
                dtype="float32",
                blocksize=block_size,
            ) as stream:
                num_frames = data.shape[0]
                idx = 0

                while idx < num_frames and not self._stop_flag.is_set():
                    end = min(idx + block_size, num_frames)
                    chunk = data[idx:end]  # (frames, channels)

                    # 读取当前音量（带锁以避免竞争）
                    with self._lock:
                        vol = self._volume

                    if vol < 1.0:
                        chunk = chunk * vol

                    stream.write(chunk)
                    idx = end

        except Exception as e:
            self.logger.error(f"[SoundEngine] 播放失败: {e}")
        finally:
            with self._lock:
                self._is_playing = False
                self._play_thread = None
                self._stop_flag.clear()
            self.logger.debug("[SoundEngine] 播放线程退出")











