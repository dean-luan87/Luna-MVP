#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Luna Badge 1.4.2a
TTSManager（仅负责合成，不负责播放）

职责：
1）接收文本，调用 edge-tts 生成 wav 文件
2）返回 wav 文件路径，不做任何播放动作
3）为上层 Voice 提供统一的 synthesize(text) 接口

注意：
- 不再调用 os.system('afplay'/'say'/'mpg123') 等系统命令
- 不再与 Voice 抢占音频设备
"""

import asyncio
import logging
import time
import os
from typing import Optional

import edge_tts

# 用于 MP3 转 WAV（如果需要）
try:
    from pydub import AudioSegment
    _pydub_available = True
except ImportError:
    _pydub_available = False


class TTSManager:
    """TTS 管理器：仅负责生成语音文件"""

    def __init__(self, voice: str = "zh-CN-XiaoxiaoNeural") -> None:
        self.logger = logging.getLogger(__name__)
        self.voice = voice
        self._pydub_available = _pydub_available

    async def _synthesize_async(self, text: str, output_file: str) -> None:
        """内部异步接口：调用 edge-tts 生成 wav 文件"""
        communicate = edge_tts.Communicate(text=text, voice=self.voice)
        await communicate.save(output_file)

    def synthesize(self, text: str) -> Optional[str]:
        """
        同步接口：生成 wav 文件并返回路径，不播放

        Args:
            text: 文本内容

        Returns:
            wav 文件路径；失败时返回 None
        """
        if not text or not text.strip():
            self.logger.warning("[TTS] 收到空文本，跳过合成")
            return None

        # edge-tts 默认生成 MP3，我们需要先生成 MP3 再转换为 WAV
        temp_mp3 = f"tts_{int(time.time() * 1000)}.mp3"
        output_file = temp_mp3.replace('.mp3', '.wav')

        try:
            self.logger.info(f"[TTS] 开始合成文本，临时文件: {temp_mp3}")
            loop = asyncio.new_event_loop()
            try:
                loop.run_until_complete(self._synthesize_async(text, temp_mp3))
            finally:
                loop.close()

            # 如果生成了 MP3，转换为 WAV
            if os.path.exists(temp_mp3):
                if self._pydub_available:
                    try:
                        self.logger.info(f"[TTS] 将 MP3 转换为 WAV: {output_file}")
                        audio = AudioSegment.from_mp3(temp_mp3)
                        audio.export(output_file, format="wav")
                        # 删除临时 MP3 文件
                        os.unlink(temp_mp3)
                        self.logger.info(f"[TTS] 合成完成: {output_file}")
                        return output_file
                    except Exception as e:
                        self.logger.error(f"[TTS] MP3 转 WAV 失败: {e}")
                        # 如果转换失败，返回 MP3 文件（虽然 Voice 不支持，但至少不会崩溃）
                        return temp_mp3
                else:
                    self.logger.warning(
                        "[TTS] pydub 未安装，无法转换为 WAV。"
                        "请安装: pip install pydub"
                    )
                    # 返回 MP3（虽然 Voice 不支持，但至少不会崩溃）
                    return temp_mp3
            else:
                self.logger.error(f"[TTS] 合成失败：未生成文件 {temp_mp3}")
                return None

        except Exception as e:
            self.logger.error(f"[TTS] 合成失败: {e}")
            # 清理可能的临时文件
            if os.path.exists(temp_mp3):
                try:
                    os.unlink(temp_mp3)
                except:
                    pass
            return None

    # 兼容旧 API：不再播放，只做合成
    def speak(self, text: str) -> Optional[str]:
        """
        为兼容旧代码保留的接口：
        - 旧逻辑：speak(text) = 合成+播放
        - 新逻辑：speak(text) = 仅合成，返回 wav 路径
        建议新代码统一使用 synthesize()，并交给 Voice 播放。
        """
        return self.synthesize(text)
