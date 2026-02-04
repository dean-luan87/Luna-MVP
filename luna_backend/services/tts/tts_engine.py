"""
TTS引擎服务 (v1.2.0)
包含：分段合成、缓存、风格（rate + emotion）、日志、错误码
"""

import asyncio
import base64
import time
import re
from typing import Optional, Dict, Any

try:
    import edge_tts
except ImportError:
    edge_tts = None

from config.error_codes import ERR
from core.logger import logger
from utils.logger import log_tts
from services.tts.tts_cache import TTSCache

MAX_CHARS = 3800  # Edge-TTS单次请求限制（保守值）


class TTSEngine:
    """TTS引擎类"""
    
    def __init__(self):
        """初始化TTS引擎"""
        self.cache = TTSCache()
        self._style_map = {
            "cheerful": ("zh-CN-XiaoxiaoNeural", "+20%"),
            "calm": ("zh-CN-XiaoyiNeural", "-5%"),
            "urgent": ("zh-CN-XiaoxiaoNeural", "+50%"),
            "empathetic": ("zh-CN-YunxiNeural", "-10%"),
            "angry": ("zh-CN-YunjianNeural", "+30%"),
            "gentle": ("zh-CN-YunxiNeural", "-15%"),
            "default": ("zh-CN-XiaoxiaoNeural", "+0%")
        }
    
    def split_text(self, text: str) -> list:
        """
        智能分段：优先在句号、问号、感叹号处分割
        
        Args:
            text: 输入文本
        
        Returns:
            分段后的文本列表
        """
        if len(text) <= MAX_CHARS:
            return [text]
        
        sentences = re.split(r'([。！？.!?])', text)
        segments = []
        cur = ""
        
        for i in range(0, len(sentences), 2):
            seg = sentences[i] + (sentences[i+1] if i+1 < len(sentences) else "")
            
            if len(cur) + len(seg) <= MAX_CHARS:
                cur += seg
            else:
                if cur:
                    segments.append(cur)
                cur = seg
        
        if cur:
            segments.append(cur)
        
        return segments
    
    async def _generate(self, text: str, voice: str, rate: str) -> bytes:
        """
        生成单段音频
        
        Args:
            text: 文本
            voice: 语音
            rate: 语速
        
        Returns:
            音频数据（字节）
        """
        if not edge_tts:
            raise ImportError("edge_tts未安装")
        
        com = edge_tts.Communicate(text=text, voice=voice, rate=rate)
        audio = b""
        
        async for chunk in com.stream():
            if chunk["type"] == "audio":
                audio += chunk["data"]
        
        return audio
    
    def synthesize(self, text: str, style: str = "cheerful", voice: Optional[str] = None, rate: Optional[str] = None) -> str:
        """
        合成语音
        
        Args:
            text: 输入文本
            style: 风格（cheerful, calm, urgent等）
            voice: 语音（可选，覆盖style）
            rate: 语速（可选，覆盖style）
        
        Returns:
            base64编码的音频数据
        """
        if not text:
            log_tts("SYNTH_ERROR", {"error": "文本为空"}, ERR.TTS_SYNTH_FAIL)
            raise ValueError("文本不能为空")
        
        if not edge_tts:
            log_tts("SYNTH_ERROR", {"error": "edge_tts未安装"}, ERR.TTS_ENGINE_ERROR)
            raise ImportError("edge_tts未安装")
        
        # 获取语音和语速
        if voice and rate:
            pass  # 使用提供的voice和rate
        else:
            voice, rate = self._style_map.get(style, self._style_map["default"])
        
        start_time = time.time()
        
        # 查缓存
        cached = self.cache.get(text, voice, rate)
        if cached:
            cache_time = (time.time() - start_time) * 1000
            log_tts("CACHE_HIT", {
                "text_length": len(text),
                "style": style,
                "latency_ms": cache_time
            })
            logger.info("TTS缓存命中", details={"latency_ms": cache_time}, module="TTS")
            return cached
        
        # 分段处理
        segments = self.split_text(text)
        logger.info("TTS文本分段", details={"segment_count": len(segments), "text_length": len(text)}, module="TTS")
        
        # 创建事件循环
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        audio_all = b""
        try:
            for i, seg in enumerate(segments):
                logger.info(f"正在合成第 {i+1}/{len(segments)} 段", details={"segment_length": len(seg)}, module="TTS")
                audio_seg = loop.run_until_complete(self._generate(seg, voice, rate))
                audio_all += audio_seg
        except Exception as e:
            log_tts("SYNTH_ERROR", {"error": str(e), "text_length": len(text)}, ERR.TTS_SYNTH_FAIL)
            raise
        finally:
            loop.close()
        
        # 保存缓存
        self.cache.store(text, voice, rate, audio_all)
        
        # 转换为base64
        audio_base64 = base64.b64encode(audio_all).decode('utf-8')
        
        generation_time = (time.time() - start_time) * 1000
        log_tts("SYNTH_SUCCESS", {
            "text_length": len(text),
            "style": style,
            "segment_count": len(segments),
            "latency_ms": generation_time
        })
        
        logger.info("TTS合成完成", details={"latency_ms": generation_time}, module="TTS")
        
        return audio_base64


# 全局实例
_tts_engine: Optional[TTSEngine] = None

def get_tts_engine() -> TTSEngine:
    """获取全局TTS引擎实例"""
    global _tts_engine
    if _tts_engine is None:
        _tts_engine = TTSEngine()
    return _tts_engine



