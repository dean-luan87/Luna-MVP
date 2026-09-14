#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
语音引擎
"""

import yaml
import os
import logging
import threading
import queue
import time
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class SpeechEngine:
    """语音引擎"""
    
    def __init__(self):
        """初始化语音引擎"""
        self.config = {}
        self.speech_queue = queue.PriorityQueue()
        self.voice_thread = None
        self.running = False
        self.current_voice = None
        self.stats = {
            "total_played": 0,
            "total_queued": 0,
            "total_failed": 0
        }
        
        logger.info("✅ 语音引擎初始化完成")
    
    def initialize(self, config_file: str = "speech/tts_config.yaml") -> bool:
        """
        初始化语音引擎
        
        Args:
            config_file: 配置文件路径
            
        Returns:
            bool: 是否初始化成功
        """
        try:
            # 加载配置文件
            if os.path.exists(config_file):
                with open(config_file, 'r', encoding='utf-8') as f:
                    self.config = yaml.safe_load(f)
                logger.info(f"✅ 语音配置文件加载成功: {config_file}")
            else:
                logger.warning(f"⚠️ 语音配置文件不存在: {config_file}")
                self._create_default_config()
            
            # 启动语音线程
            self.running = True
            self.voice_thread = threading.Thread(target=self._voice_worker, daemon=True)
            self.voice_thread.start()
            
            logger.info("✅ 语音引擎初始化成功")
            return True
            
        except Exception as e:
            logger.error(f"❌ 语音引擎初始化失败: {e}")
            return False
    
    def _create_default_config(self):
        """创建默认配置"""
        self.config = {
            "speech_events": {
                "system_startup": {
                    "text_variants": ["Luna系统启动完成"],
                    "style": "friendly",
                    "priority": 0,
                    "cooldown": 10
                }
            },
            "speech_styles": {
                "friendly": {
                    "speed": 1.0,
                    "volume": 0.8,
                    "voice": "zh-CN-XiaoxiaoNeural"
                }
            },
            "default_config": {
                "voice": "zh-CN-XiaoxiaoNeural",
                "speed": 1.0,
                "volume": 0.8,
                "language": "zh-CN"
            }
        }
    
    def _voice_worker(self):
        """语音工作线程"""
        while self.running:
            try:
                # 获取语音任务
                priority, task = self.speech_queue.get(timeout=1.0)
                
                # 执行语音播报
                self._execute_speech(task)
                
                # 标记任务完成
                self.speech_queue.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"❌ 语音工作线程错误: {e}")
                self.stats["total_failed"] += 1
    
    def _execute_speech(self, task: Dict[str, Any]):
        """
        执行语音播报
        
        Args:
            task: 语音任务
        """
        try:
            text = task.get("text", "")
            style = task.get("style", "friendly")
            
            # 获取语音配置
            style_config = self.config.get("speech_styles", {}).get(style, {})
            default_config = self.config.get("default_config", {})
            
            # 使用系统say命令播报
            voice = style_config.get("voice", default_config.get("voice", "zh-CN-XiaoxiaoNeural"))
            speed = style_config.get("speed", default_config.get("speed", 1.0))
            
            # 执行语音播报
            self._play_speech(text, voice, speed)
            
            self.stats["total_played"] += 1
            logger.info(f"🗣️ 语音播报完成: {text}")
            
        except Exception as e:
            logger.error(f"❌ 语音播报失败: {e}")
            self.stats["total_failed"] += 1
    
    def _play_speech(self, text: str, voice: str, speed: float):
        """
        播放语音
        
        Args:
            text: 要播报的文本
            voice: 语音类型
            speed: 语速
        """
        try:
            # 使用系统say命令
            import subprocess
            
            # 构建命令
            cmd = ["say", "-v", voice, "-r", str(int(speed * 200)), text]
            
            # 执行命令
            subprocess.run(cmd, check=True, capture_output=True)
            
        except Exception as e:
            logger.error(f"❌ 语音播放失败: {e}")
            raise
    
    def speak(self, text: str, priority: int = 1, style: str = "friendly") -> bool:
        """
        添加语音播报任务
        
        Args:
            text: 要播报的文本
            priority: 优先级
            style: 语音风格
            
        Returns:
            bool: 是否添加成功
        """
        try:
            # 创建语音任务
            task = {
                "text": text,
                "style": style,
                "timestamp": time.time()
            }
            
            # 添加到队列
            self.speech_queue.put((priority, task))
            self.stats["total_queued"] += 1
            
            logger.info(f"🗣️ 语音任务已添加: {text} (优先级: {priority})")
            return True
            
        except Exception as e:
            logger.error(f"❌ 语音任务添加失败: {e}")
            return False
    
    def speak_event(self, event_name: str, priority: int = 1) -> bool:
        """
        播报预定义事件
        
        Args:
            event_name: 事件名称
            priority: 优先级
            
        Returns:
            bool: 是否播报成功
        """
        try:
            # 获取事件配置
            event_config = self.config.get("speech_events", {}).get(event_name)
            if not event_config:
                logger.warning(f"⚠️ 未找到事件配置: {event_name}")
                return False
            
            # 获取文本变体
            text_variants = event_config.get("text_variants", [])
            if not text_variants:
                logger.warning(f"⚠️ 事件无文本变体: {event_name}")
                return False
            
            # 选择文本变体
            import random
            text = random.choice(text_variants)
            
            # 获取风格
            style = event_config.get("style", "friendly")
            
            # 播报语音
            return self.speak(text, priority, style)
            
        except Exception as e:
            logger.error(f"❌ 事件播报失败: {e}")
            return False
    
    def stop(self):
        """停止语音引擎"""
        self.running = False
        
        # 等待语音线程结束
        if self.voice_thread and self.voice_thread.is_alive():
            self.voice_thread.join(timeout=5.0)
        
        logger.info("✅ 语音引擎已停止")
    
    def get_status(self) -> Dict[str, Any]:
        """
        获取语音引擎状态
        
        Returns:
            Dict[str, Any]: 状态信息
        """
        return {
            "running": self.running,
            "queue_size": self.speech_queue.qsize(),
            "current_voice": self.current_voice,
            "stats": self.stats.copy()
        }

# 使用示例
if __name__ == "__main__":
    # 创建语音引擎
    engine = SpeechEngine()
    
    # 初始化语音引擎
    if engine.initialize():
        print("✅ 语音引擎初始化成功")
        
        # 测试语音播报
        engine.speak("测试语音播报", priority=0)
        engine.speak_event("system_startup", priority=0)
        
        # 等待播报完成
        time.sleep(3)
        
        # 停止语音引擎
        engine.stop()
    else:
        print("❌ 语音引擎初始化失败")
