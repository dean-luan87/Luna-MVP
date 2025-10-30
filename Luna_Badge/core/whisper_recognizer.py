#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge Whisper 语音识别引擎
集成 OpenAI Whisper 模型实现离线语音识别
"""

import os
import logging
import time
import numpy as np
from typing import Optional, Dict, Any, Tuple
import tempfile

logger = logging.getLogger(__name__)

class WhisperRecognizer:
    """Whisper语音识别引擎"""
    
    def __init__(self, model_name: str = "base", language: str = "zh"):
        """
        初始化Whisper识别引擎
        
        Args:
            model_name: Whisper模型名称 (tiny/base/small/medium/large)
            language: 语言代码 (zh=中文, en=英文)
        """
        self.model_name = model_name
        self.language = language
        self.model = None
        self.is_loaded = False
        
        logger.info(f"🎤 Whisper识别器初始化 (模型={model_name}, 语言={language})")
    
    def load_model(self) -> bool:
        """
        加载Whisper模型
        
        Returns:
            bool: 是否成功加载
        """
        try:
            import whisper
            
            logger.info(f"正在加载Whisper模型: {self.model_name}...")
            self.model = whisper.load_model(self.model_name)
            self.is_loaded = True
            
            logger.info("✅ Whisper模型加载成功")
            return True
            
        except ImportError:
            logger.error("❌ 未安装whisper库，请运行: pip install openai-whisper")
            return False
        except Exception as e:
            logger.error(f"❌ Whisper模型加载失败: {e}")
            return False
    
    def recognize_from_file(self, audio_file: str) -> Tuple[str, Dict[str, Any]]:
        """
        从音频文件识别语音
        
        Args:
            audio_file: 音频文件路径
            
        Returns:
            Tuple[str, Dict[str, Any]]: (识别的文本, 详细信息)
        """
        if not self.is_loaded:
            if not self.load_model():
                return "", {}
        
        try:
            logger.info(f"正在识别音频: {audio_file}")
            
            # 使用Whisper识别
            result = self.model.transcribe(
                audio_file,
                language=self.language,
                task="transcribe"
            )
            
            text = result.get("text", "").strip()
            
            # 提取详细结果
            details = {
                "language": result.get("language", self.language),
                "duration": result.get("segments", [{}])[0].get("duration", 0) if result.get("segments") else 0,
                "confidence": self._calculate_confidence(result),
                "segments": [
                    {
                        "start": seg.get("start", 0),
                        "end": seg.get("end", 0),
                        "text": seg.get("text", "").strip()
                    }
                    for seg in result.get("segments", [])
                ]
            }
            
            logger.info(f"✅ 识别成功: {text}")
            return text, details
            
        except Exception as e:
            logger.error(f"❌ 识别失败: {e}")
            return "", {}
    
    def recognize_from_array(self, audio_array: np.ndarray, sample_rate: int = 16000) -> Tuple[str, Dict[str, Any]]:
        """
        从numpy数组识别语音
        
        Args:
            audio_array: 音频数据数组
            sample_rate: 采样率
            
        Returns:
            Tuple[str, Dict[str, Any]]: (识别的文本, 详细信息)
        """
        try:
            import scipy.io.wavfile as wavfile
            
            # 创建临时音频文件
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
                temp_path = tmp_file.name
                
                # 保存音频数据
                wavfile.write(temp_path, sample_rate, audio_array)
                
                # 识别
                text, details = self.recognize_from_file(temp_path)
                
                # 清理临时文件
                os.unlink(temp_path)
                
                return text, details
                
        except Exception as e:
            logger.error(f"❌ 数组识别失败: {e}")
            return "", {}
    
    def recognize_from_microphone(self, duration: int = 5) -> Tuple[str, Dict[str, Any]]:
        """
        从麦克风实时录音并识别
        
        Args:
            duration: 录音时长（秒）
            
        Returns:
            Tuple[str, Dict[str, Any]]: (识别的文本, 详细信息)
        """
        try:
            import sounddevice as sd
            import scipy.io.wavfile as wavfile
            
            sample_rate = 16000
            
            logger.info(f"开始录音 {duration} 秒...")
            
            # 录音
            recording = sd.rec(
                int(sample_rate * duration),
                samplerate=sample_rate,
                channels=1,
                dtype='int16'
            )
            sd.wait()
            
            logger.info("录音完成，开始识别...")
            
            # 识别
            text, details = self.recognize_from_array(recording.flatten(), sample_rate)
            
            return text, details
            
        except ImportError:
            logger.error("❌ 未安装必要库，请运行: pip install sounddevice scipy")
            return "", {}
        except Exception as e:
            logger.error(f"❌ 麦克风识别失败: {e}")
            return "", {}
    
    def _calculate_confidence(self, result: Dict[str, Any]) -> float:
        """
        计算识别置信度
        
        Args:
            result: Whisper识别结果
            
        Returns:
            float: 置信度 (0-1)
        """
        try:
            # 从segments中提取平均no_speech_prob
            segments = result.get("segments", [])
            if not segments:
                return 0.5
            
            # 计算平均置信度
            no_speech_probs = [seg.get("no_speech_prob", 0.5) for seg in segments]
            avg_no_speech = np.mean(no_speech_probs)
            
            # 转换为置信度 (no_speech越小，置信度越高)
            confidence = 1.0 - avg_no_speech
            
            return max(0.0, min(1.0, confidence))
            
        except Exception:
            return 0.5
    
    def get_supported_languages(self) -> list:
        """获取支持的语言列表"""
        return ["zh", "en", "ja", "ko"]


# 全局实例
_whisper_recognizer: Optional[WhisperRecognizer] = None

def get_whisper_recognizer(model_name: str = "base", language: str = "zh") -> WhisperRecognizer:
    """
    获取全局Whisper识别器实例
    
    Args:
        model_name: 模型名称
        language: 语言代码
        
    Returns:
        WhisperRecognizer: 识别器实例
    """
    global _whisper_recognizer
    
    if _whisper_recognizer is None:
        _whisper_recognizer = WhisperRecognizer(model_name, language)
    
    return _whisper_recognizer


def recognize_speech(audio_file: str = None, audio_array: np.ndarray = None, 
                     duration: int = 5, model_name: str = "base") -> str:
    """
    便捷的语音识别函数
    
    Args:
        audio_file: 音频文件路径
        audio_array: 音频数组
        duration: 录音时长（秒）
        model_name: 模型名称
        
    Returns:
        str: 识别的文本
    """
    recognizer = get_whisper_recognizer(model_name)
    
    if audio_file:
        text, _ = recognizer.recognize_from_file(audio_file)
        return text
    elif audio_array is not None:
        text, _ = recognizer.recognize_from_array(audio_array)
        return text
    else:
        text, _ = recognizer.recognize_from_microphone(duration)
        return text


if __name__ == "__main__":
    # 测试Whisper识别器
    import logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    print("=" * 60)
    print("🎤 Whisper语音识别测试")
    print("=" * 60)
    
    recognizer = WhisperRecognizer(model_name="base")
    
    # 测试从麦克风识别
    print("\n测试麦克风录音识别（5秒）...")
    print("请开始说话...")
    
    text, details = recognizer.recognize_from_microphone(duration=5)
    
    print(f"\n✅ 识别结果: {text}")
    print(f"置信度: {details.get('confidence', 0):.2f}")
    print(f"语言: {details.get('language', 'unknown')}")
    
    print("\n" + "=" * 60)
