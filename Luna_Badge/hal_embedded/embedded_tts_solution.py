#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
嵌入式TTS解决方案
解决Edge-TTS网络依赖问题，提供完全离线的语音播报功能
"""

import os
import subprocess
import threading
import time
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path

logger = logging.getLogger(__name__)

class EmbeddedTTSSolution:
    """嵌入式TTS解决方案"""
    
    def __init__(self):
        self.voice_engine = None
        self.voice_type = None
        self.voice_command = None
        self.is_initialized = False
        self.audio_files_dir = "audio_files"
        self.preloaded_audio = {}
        
        # 创建音频文件目录
        Path(self.audio_files_dir).mkdir(exist_ok=True)
    
    def initialize(self) -> bool:
        """初始化TTS引擎"""
        try:
            logger.info("🔊 初始化嵌入式TTS引擎...")
            
            # 检测可用的语音引擎
            available_engines = self._detect_voice_engines()
            
            if not available_engines:
                logger.error("❌ 没有找到可用的语音引擎")
                return False
            
            # 选择最佳语音引擎
            self.voice_engine, self.voice_type, self.voice_command = self._select_best_voice(available_engines)
            
            logger.info(f"✅ 选择语音引擎: {self.voice_engine} - {self.voice_type}")
            
            # 预加载常用音频文件
            self._preload_common_audio()
            
            self.is_initialized = True
            logger.info("✅ 嵌入式TTS引擎初始化成功")
            return True
            
        except Exception as e:
            logger.error(f"❌ TTS引擎初始化失败: {e}")
            return False
    
    def _detect_voice_engines(self) -> List[tuple]:
        """检测可用的语音引擎"""
        engines = []
        
        # 检测espeak
        if self._test_espeak():
            engines.extend(self._get_espeak_voices())
        
        # 检测festival
        if self._test_festival():
            engines.append(("festival", "默认", 'echo "{text}" | festival --tts'))
        
        # 检测系统say命令
        if self._test_say():
            engines.append(("say", "系统默认", 'say "{text}"'))
        
        return engines
    
    def _test_espeak(self) -> bool:
        """测试espeak是否可用"""
        try:
            result = subprocess.run(['espeak', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except:
            return False
    
    def _test_festival(self) -> bool:
        """测试festival是否可用"""
        try:
            result = subprocess.run(['festival', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except:
            return False
    
    def _test_say(self) -> bool:
        """测试系统say命令是否可用"""
        try:
            # 检查say命令是否存在
            result = subprocess.run(['which', 'say'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print(f"✅ 找到say命令: {result.stdout.strip()}")
                return True
            else:
                print("❌ 未找到say命令")
                return False
        except Exception as e:
            print(f"❌ say命令检测失败: {e}")
            return False
    
    def _get_espeak_voices(self) -> List[tuple]:
        """获取espeak可用语音"""
        voices = []
        
        espeak_voices = [
            ("中文女性", 'espeak -s 150 -v zh+f3 "{text}"'),
            ("中文男性", 'espeak -s 150 -v zh+m1 "{text}"'),
            ("英文女性", 'espeak -s 150 -v en+f3 "{text}"'),
            ("英文男性", 'espeak -s 150 -v en+m1 "{text}"'),
            ("中文默认", 'espeak -s 150 -v zh "{text}"')
        ]
        
        for name, cmd_template in espeak_voices:
            try:
                test_cmd = cmd_template.format(text="测试")
                result = subprocess.run(test_cmd, shell=True, 
                                      capture_output=True, text=True, timeout=3)
                if result.returncode == 0:
                    voices.append(("espeak", name, cmd_template))
            except:
                continue
        
        return voices
    
    def _select_best_voice(self, engines: List[tuple]) -> tuple:
        """选择最佳语音引擎"""
        # 优先选择女性语音
        female_voices = [v for v in engines if '女性' in v[1] or 'female' in v[1]]
        
        if female_voices:
            return female_voices[0]
        
        # 其次选择中文语音
        chinese_voices = [v for v in engines if '中文' in v[1] or 'zh' in v[1]]
        if chinese_voices:
            return chinese_voices[0]
        
        # 最后选择默认语音
        return engines[0]
    
    def _preload_common_audio(self):
        """预加载常用音频文件"""
        logger.info("🎵 预加载常用音频文件...")
        
        common_texts = {
            "crowd_alert": "前方人较多，请靠边行走",
            "system_start": "系统启动完成",
            "system_stop": "系统已关闭",
            "detection_start": "开始环境检测",
            "detection_complete": "环境检测完成",
            "safety_alert": "请注意安全",
            "navigation_start": "开始导航",
            "navigation_stop": "导航结束"
        }
        
        for key, text in common_texts.items():
            audio_file = os.path.join(self.audio_files_dir, f"{key}.wav")
            
            if not os.path.exists(audio_file):
                if self._generate_audio_file(text, audio_file):
                    self.preloaded_audio[key] = audio_file
                    logger.info(f"✅ 预加载音频: {key}")
                else:
                    logger.warning(f"⚠️ 预加载音频失败: {key}")
            else:
                self.preloaded_audio[key] = audio_file
                logger.info(f"✅ 使用已有音频: {key}")
    
    def _generate_audio_file(self, text: str, output_file: str) -> bool:
        """生成音频文件"""
        try:
            if self.voice_engine == "espeak":
                cmd = f'espeak -s 150 -v zh+f3 "{text}" -w "{output_file}"'
            elif self.voice_engine == "festival":
                cmd = f'echo "{text}" | festival --tts --pipe > "{output_file}"'
            else:
                # 对于say命令，先生成音频再转换
                temp_file = output_file.replace('.wav', '.aiff')
                cmd = f'say "{text}" -o "{temp_file}"'
                subprocess.run(cmd, shell=True, check=True)
                
                # 转换为wav格式
                convert_cmd = f'ffmpeg -i "{temp_file}" "{output_file}" -y'
                subprocess.run(convert_cmd, shell=True, check=True)
                os.remove(temp_file)
                return True
            
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return result.returncode == 0
            
        except Exception as e:
            logger.error(f"❌ 音频文件生成失败: {e}")
            return False
    
    def speak(self, text: str, use_preloaded: bool = True) -> bool:
        """语音播报"""
        try:
            if not self.is_initialized:
                logger.error("❌ TTS引擎未初始化")
                return False
            
            # 尝试使用预加载音频
            if use_preloaded:
                for key, audio_file in self.preloaded_audio.items():
                    if text in key or key in text:
                        return self._play_audio_file(audio_file)
            
            # 实时生成语音
            return self._speak_real_time(text)
            
        except Exception as e:
            logger.error(f"❌ 语音播报失败: {e}")
            return False
    
    def _play_audio_file(self, audio_file: str) -> bool:
        """播放音频文件"""
        try:
            if os.path.exists(audio_file):
                # 使用aplay播放音频（Linux）
                cmd = f'aplay "{audio_file}"'
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    return True
                
                # 备用方案：使用mplayer
                cmd = f'mplayer "{audio_file}"'
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                return result.returncode == 0
            
            return False
            
        except Exception as e:
            logger.error(f"❌ 音频文件播放失败: {e}")
            return False
    
    def _speak_real_time(self, text: str) -> bool:
        """实时语音播报"""
        try:
            cmd = self.voice_command.format(text=text)
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return result.returncode == 0
            
        except Exception as e:
            logger.error(f"❌ 实时语音播报失败: {e}")
            return False
    
    def speak_async(self, text: str, use_preloaded: bool = True):
        """异步语音播报"""
        def _speak_thread():
            self.speak(text, use_preloaded)
        
        thread = threading.Thread(target=_speak_thread, daemon=True)
        thread.start()
    
    def cleanup(self):
        """清理资源"""
        self.is_initialized = False
        self.preloaded_audio.clear()
    
    def get_info(self) -> Dict[str, Any]:
        """获取TTS信息"""
        return {
            "initialized": self.is_initialized,
            "voice_engine": self.voice_engine,
            "voice_type": self.voice_type,
            "preloaded_audio_count": len(self.preloaded_audio),
            "audio_files_dir": self.audio_files_dir
        }

# 全局实例
embedded_tts = EmbeddedTTSSolution()

def initialize_embedded_tts() -> bool:
    """初始化嵌入式TTS"""
    return embedded_tts.initialize()

def speak(text: str, use_preloaded: bool = True) -> bool:
    """语音播报"""
    return embedded_tts.speak(text, use_preloaded)

def speak_async(text: str, use_preloaded: bool = True):
    """异步语音播报"""
    embedded_tts.speak_async(text, use_preloaded)

def cleanup_embedded_tts():
    """清理嵌入式TTS"""
    embedded_tts.cleanup()

if __name__ == "__main__":
    # 测试嵌入式TTS
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    
    print("🎯 嵌入式TTS解决方案测试")
    print("=" * 50)
    
    # 初始化
    if initialize_embedded_tts():
        print("✅ TTS引擎初始化成功")
        
        # 测试语音播报
        test_texts = [
            "前方人较多，请靠边行走",
            "系统启动完成",
            "环境检测完成"
        ]
        
        for text in test_texts:
            print(f"🗣️ 播报: {text}")
            speak(text)
            time.sleep(1)
        
        print("✅ 测试完成")
    else:
        print("❌ TTS引擎初始化失败")
