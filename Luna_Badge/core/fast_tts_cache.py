#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
快速TTS缓存系统 - 实现1秒内语音反馈
通过预生成和缓存常用短语，大幅降低延迟
"""

import os
import json
import hashlib
import base64
import asyncio
import logging
from typing import Dict, Optional, Tuple
from pathlib import Path
import time

logger = logging.getLogger(__name__)

class FastTTSCache:
    """快速TTS缓存系统"""
    
    def __init__(self, cache_dir: str = "tts_cache"):
        """初始化缓存系统"""
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        
        # 缓存索引文件
        self.index_file = self.cache_dir / "index.json"
        self.cache_index: Dict[str, Dict] = {}
        self._load_index()
        
        # 常用短语列表（预生成）
        self.common_phrases = [
            "前方有台阶，请小心",
            "检测到危险区域，请谨慎前行",
            "请向左转",
            "请向右转",
            "请保持直行",
            "检测到洗手间标识，就在前方",
            "检测到电梯标识，在您前方",
            "检测到出口标识",
            "前方道路畅通，请继续前行",
            "前方不可通行，建议右转",
            "前方拥挤，请靠右",
            "已到达目的地",
            "Luna已启动，开始环境扫描",
            "我将主动为您提示周围环境",
        ]
        
        logger.info(f"✅ 快速TTS缓存系统初始化完成，缓存目录: {self.cache_dir}")
    
    def _load_index(self):
        """加载缓存索引"""
        if self.index_file.exists():
            try:
                with open(self.index_file, 'r', encoding='utf-8') as f:
                    self.cache_index = json.load(f)
                logger.info(f"✅ 加载缓存索引: {len(self.cache_index)} 条记录")
            except Exception as e:
                logger.warning(f"⚠️ 加载缓存索引失败: {e}")
                self.cache_index = {}
    
    def _save_index(self):
        """保存缓存索引"""
        try:
            with open(self.index_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache_index, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.warning(f"⚠️ 保存缓存索引失败: {e}")
    
    def _get_cache_key(self, text: str, voice: str, rate: str) -> str:
        """生成缓存键"""
        key_str = f"{text}|{voice}|{rate}"
        return hashlib.md5(key_str.encode('utf-8')).hexdigest()
    
    def get_cached_audio(self, text: str, voice: str, rate: str) -> Optional[bytes]:
        """获取缓存的音频"""
        cache_key = self._get_cache_key(text, voice, rate)
        
        if cache_key in self.cache_index:
            cache_info = self.cache_index[cache_key]
            cache_file = self.cache_dir / cache_info['file']
            
            if cache_file.exists():
                try:
                    with open(cache_file, 'rb') as f:
                        audio_data = f.read()
                    logger.debug(f"✅ 缓存命中: {text[:20]}...")
                    return audio_data
                except Exception as e:
                    logger.warning(f"⚠️ 读取缓存文件失败: {e}")
        
        return None
    
    def save_cached_audio(self, text: str, voice: str, rate: str, audio_data: bytes):
        """保存音频到缓存"""
        cache_key = self._get_cache_key(text, voice, rate)
        cache_file = self.cache_dir / f"{cache_key}.mp3"
        
        try:
            with open(cache_file, 'wb') as f:
                f.write(audio_data)
            
            self.cache_index[cache_key] = {
                'text': text,
                'voice': voice,
                'rate': rate,
                'file': cache_file.name,
                'size': len(audio_data),
                'created_at': time.time()
            }
            
            self._save_index()
            logger.debug(f"✅ 缓存保存: {text[:20]}...")
        except Exception as e:
            logger.warning(f"⚠️ 保存缓存失败: {e}")
    
    async def pregenerate_common_phrases(self):
        """预生成常用短语的音频"""
        import edge_tts
        
        logger.info(f"🔄 开始预生成 {len(self.common_phrases)} 条常用短语...")
        
        # 常用语音和语速组合
        voice_rate_combinations = [
            ('zh-CN-XiaoxiaoNeural', '+50%'),  # 紧急
            ('zh-CN-XiaoxiaoNeural', '+20%'),  # 欢快
            ('zh-CN-XiaoyiNeural', '-5%'),     # 平静
        ]
        
        generated_count = 0
        skipped_count = 0
        
        for text in self.common_phrases:
            for voice, rate in voice_rate_combinations:
                # 检查是否已缓存
                if self.get_cached_audio(text, voice, rate):
                    skipped_count += 1
                    continue
                
                try:
                    # 生成音频
                    communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate)
                    audio_data = b""
                    async for chunk in communicate.stream():
                        if chunk["type"] == "audio":
                            audio_data += chunk["data"]
                    
                    # 保存缓存
                    if audio_data:
                        self.save_cached_audio(text, voice, rate, audio_data)
                        generated_count += 1
                        logger.info(f"  ✅ 预生成: {text[:30]}... ({voice}, {rate})")
                    
                    # 避免过快请求
                    await asyncio.sleep(0.1)
                    
                except Exception as e:
                    logger.warning(f"⚠️ 预生成失败: {text[:30]}... ({e})")
        
        logger.info(f"✅ 预生成完成: 新增 {generated_count} 条，跳过 {skipped_count} 条")
    
    def get_cache_stats(self) -> Dict:
        """获取缓存统计信息"""
        total_size = sum(info.get('size', 0) for info in self.cache_index.values())
        return {
            'count': len(self.cache_index),
            'total_size_mb': total_size / (1024 * 1024),
            'cache_dir': str(self.cache_dir)
        }






