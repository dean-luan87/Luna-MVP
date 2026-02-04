"""
TTS缓存服务 (v1.2.0)
"""

import hashlib
import os
import json
import base64
from typing import Optional
from core.logger import logger

CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "tts_cache")
os.makedirs(CACHE_DIR, exist_ok=True)


class TTSCache:
    """TTS缓存类"""
    
    def __init__(self, cache_dir: str = CACHE_DIR):
        """
        初始化TTS缓存
        
        Args:
            cache_dir: 缓存目录
        """
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def _get_cache_key(self, text: str, voice: str, rate: str) -> str:
        """生成缓存键"""
        key_str = f"{text}|{voice}|{rate}"
        return hashlib.md5(key_str.encode('utf-8')).hexdigest()
    
    def _get_cache_path(self, cache_key: str) -> str:
        """获取缓存文件路径"""
        return os.path.join(self.cache_dir, f"{cache_key}.cache")
    
    def get(self, text: str, voice: str, rate: str) -> Optional[str]:
        """
        获取缓存
        
        Args:
            text: 文本
            voice: 语音
            rate: 语速
        
        Returns:
            base64编码的音频数据，如果不存在返回None
        """
        try:
            cache_key = self._get_cache_key(text, voice, rate)
            cache_path = self._get_cache_path(cache_key)
            
            if os.path.exists(cache_path):
                with open(cache_path, 'rb') as f:
                    audio_data = f.read()
                    return base64.b64encode(audio_data).decode('utf-8')
            
            return None
        except Exception as e:
            logger.warn("TTS缓存读取失败", details={"error": str(e)}, module="TTS")
            return None
    
    def store(self, text: str, voice: str, rate: str, audio_data: bytes):
        """
        存储缓存
        
        Args:
            text: 文本
            voice: 语音
            rate: 语速
            audio_data: 音频数据（字节）
        """
        try:
            cache_key = self._get_cache_key(text, voice, rate)
            cache_path = self._get_cache_path(cache_key)
            
            with open(cache_path, 'wb') as f:
                f.write(audio_data)
            
            logger.info("TTS缓存保存成功", details={"cache_key": cache_key}, module="TTS")
        except Exception as e:
            logger.warn("TTS缓存保存失败", details={"error": str(e)}, module="TTS")
    
    def get_stats(self) -> dict:
        """获取缓存统计信息"""
        try:
            cache_files = [f for f in os.listdir(self.cache_dir) if f.endswith('.cache')]
            total_size = sum(
                os.path.getsize(os.path.join(self.cache_dir, f))
                for f in cache_files
            )
            
            return {
                "count": len(cache_files),
                "total_size_bytes": total_size,
                "total_size_mb": round(total_size / 1024 / 1024, 2)
            }
        except Exception as e:
            logger.warn("获取缓存统计失败", details={"error": str(e)}, module="TTS")
            return {"count": 0, "total_size_bytes": 0, "total_size_mb": 0}



