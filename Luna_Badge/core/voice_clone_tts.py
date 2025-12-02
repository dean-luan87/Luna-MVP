#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Luna - 语音克隆 TTS 模块
基于 Coqui TTS XTTS-v2 实现真人语音克隆
"""

import logging
import os
import tempfile
from pathlib import Path
from typing import Optional, Union

logger = logging.getLogger(__name__)


class VoiceCloneTTS:
    """基于 Coqui TTS 的语音克隆TTS
    
    使用 XTTS-v2 模型，仅需3-5秒参考音频即可克隆语音
    """
    
    def __init__(
        self,
        reference_audio_path: str,
        model_name: str = "tts_models/multilingual/multi-dataset/xtts_v2",
        use_gpu: bool = False,
        output_dir: Optional[str] = None
    ):
        """初始化语音克隆TTS
        
        Args:
            reference_audio_path: 参考音频路径（3-5秒清晰音频）
            model_name: TTS模型名称
            use_gpu: 是否使用GPU加速
            output_dir: 输出目录（可选，默认使用临时目录）
        """
        self.reference_audio_path = reference_audio_path
        self.model_name = model_name
        self.use_gpu = use_gpu
        self.output_dir = Path(output_dir) if output_dir else Path(tempfile.gettempdir()) / "luna_tts"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.tts = None
        self._initialized = False
        
        logger.info(f"🎙️ 语音克隆TTS初始化 (模型: {model_name})")
        logger.info(f"📁 参考音频: {reference_audio_path}")
    
    def _initialize(self):
        """延迟初始化TTS模型"""
        if self._initialized:
            return
        
        try:
            from TTS.api import TTS
            
            logger.info("⏳ 正在加载TTS模型...")
            self.tts = TTS(self.model_name, gpu=self.use_gpu)
            self._initialized = True
            logger.info("✅ TTS模型加载完成")
            
            # 验证参考音频存在
            if not os.path.exists(self.reference_audio_path):
                raise FileNotFoundError(f"参考音频文件不存在: {self.reference_audio_path}")
            
        except ImportError:
            logger.error("❌ 未安装 TTS 库，请运行: pip install TTS")
            raise
        except Exception as e:
            logger.error(f"❌ TTS模型加载失败: {e}", exc_info=True)
            raise
    
    def speak(
        self,
        text: str,
        language: str = "zh",
        output_path: Optional[str] = None,
        speed: float = 1.0
    ) -> str:
        """生成语音
        
        Args:
            text: 要转换的文本
            language: 语言代码（zh中文, en英文等）
            output_path: 输出文件路径（可选）
            speed: 语速倍数（1.0为正常速度）
        
        Returns:
            生成的音频文件路径
        """
        if not self._initialized:
            self._initialize()
        
        try:
            # 生成输出路径
            if not output_path:
                import hashlib
                file_hash = hashlib.md5(text.encode()).hexdigest()[:8]
                output_path = str(self.output_dir / f"tts_{file_hash}.wav")
            
            logger.debug(f"🎤 生成语音: {text[:50]}...")
            
            # 使用XTTS模型生成语音
            self.tts.tts_to_file(
                text=text,
                speaker_wav=self.reference_audio_path,  # 使用参考音频克隆语音
                language=language,
                file_path=output_path,
                speed=speed
            )
            
            logger.debug(f"✅ 语音生成完成: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"❌ 语音生成失败: {e}", exc_info=True)
            raise
    
    def speak_async(
        self,
        text: str,
        language: str = "zh",
        callback: Optional[callable] = None
    ):
        """异步生成语音（可在后台线程中调用）
        
        Args:
            text: 要转换的文本
            language: 语言代码
            callback: 完成后的回调函数 callback(output_path)
        """
        import threading
        
        def _generate():
            try:
                output_path = self.speak(text, language)
                if callback:
                    callback(output_path)
            except Exception as e:
                logger.error(f"❌ 异步语音生成失败: {e}")
                if callback:
                    callback(None)
        
        thread = threading.Thread(target=_generate, daemon=True)
        thread.start()
        return thread
    
    def cleanup(self):
        """清理资源"""
        if self.tts:
            # TTS库通常不需要显式清理
            self.tts = None
            self._initialized = False
            logger.info("🧹 TTS资源已清理")
    
    def get_supported_languages(self) -> list:
        """获取支持的语言列表
        
        Returns:
            支持的语言代码列表
        """
        # XTTS-v2 支持的语言
        return [
            "zh",  # 中文
            "en",  # 英文
            "es",  # 西班牙语
            "fr",  # 法语
            "de",  # 德语
            "it",  # 意大利语
            "pt",  # 葡萄牙语
            "pl",  # 波兰语
            "tr",  # 土耳其语
            "ru",  # 俄语
            "nl",  # 荷兰语
            "cs",  # 捷克语
            "ar",  # 阿拉伯语
            "ja",  # 日语
            "hu",  # 匈牙利语
            "ko",  # 韩语
        ]


def create_voice_clone_tts(
    reference_audio_path: str,
    use_gpu: bool = False
) -> VoiceCloneTTS:
    """创建语音克隆TTS实例（便捷函数）
    
    Args:
        reference_audio_path: 参考音频路径
        use_gpu: 是否使用GPU
    
    Returns:
        VoiceCloneTTS实例
    """
    return VoiceCloneTTS(
        reference_audio_path=reference_audio_path,
        use_gpu=use_gpu
    )


if __name__ == "__main__":
    # 测试代码
    logging.basicConfig(level=logging.INFO)
    
    # 示例使用
    print("🎙️ 语音克隆TTS测试")
    print("=" * 70)
    
    # 注意：需要先准备一个3-5秒的参考音频文件
    reference_audio = "reference_voice.wav"  # 替换为实际路径
    
    if not os.path.exists(reference_audio):
        print(f"⚠️ 请先准备参考音频文件: {reference_audio}")
        print("   需要3-5秒的清晰音频（WAV格式）")
    else:
        try:
            tts = VoiceCloneTTS(
                reference_audio_path=reference_audio,
                use_gpu=False  # 如果没有GPU，设为False
            )
            
            # 测试生成语音
            output = tts.speak(
                text="你好，这是使用语音克隆技术生成的语音。",
                language="zh"
            )
            
            print(f"✅ 语音生成成功: {output}")
            
        except ImportError:
            print("❌ 请先安装 Coqui TTS:")
            print("   pip install TTS")
        except Exception as e:
            print(f"❌ 测试失败: {e}")
