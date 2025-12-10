#!/usr/bin/env python3
"""
语音管线完整对接
v1.4.2: ASR/TTS 完整接线，对接 QueryBus, RecoveryCenter
"""
import logging
import asyncio
from typing import Optional, Dict, Any, Callable

from core.task.query_bus import QueryBus
from core.system.system_recovery_center import RecoveryCenter

logger = logging.getLogger(__name__)


class IntentParser:
    """
    意图解析器（简单关键词匹配版本）
    实际项目中可以替换为更复杂的 NLU 模型
    """
    
    def parse(self, text: str) -> Dict[str, Any]:
        """
        解析用户输入文本
        
        Returns:
            包含 intent 和 slots 的字典
        """
        text_lower = text.lower().strip()
        
        # 停止/结束意图
        if any(kw in text_lower for kw in ["停止", "结束", "stop", "停", "到了", "到达"]):
            return {
                "intent": "stop",
                "answer": "yes",
                "slots": {},
            }
        
        # 继续意图
        if any(kw in text_lower for kw in ["继续", "继续走", "继续前进", "continue", "go"]):
            return {
                "intent": "continue",
                "answer": "no",
                "slots": {},
            }
        
        # 确认意图
        if any(kw in text_lower for kw in ["是", "yes", "对", "好", "可以", "行", "去"]):
            return {
                "intent": "confirm",
                "answer": "yes",
                "slots": {},
            }
        
        # 否定意图
        if any(kw in text_lower for kw in ["否", "no", "不", "不要", "不行", "不去"]):
            return {
                "intent": "deny",
                "answer": "no",
                "slots": {},
            }
        
        # 默认：无法识别
        return {
            "intent": "unknown",
            "answer": "unknown",
            "slots": {},
        }


class SpeechPipeline:
    """
    语音管线：整合 ASR, TTS, QueryBus, 意图解析
    """
    
    def __init__(
        self,
        asr: Optional[Any] = None,
        tts: Optional[Any] = None,
        query_bus: Optional[QueryBus] = None,
        recovery_center: Optional[RecoveryCenter] = None,
    ):
        """
        初始化语音管线
        
        Args:
            asr: ASR 模块（需要实现 listen() 方法）
            tts: TTS 模块（需要实现 speak() 方法）
            query_bus: 问询总线
            recovery_center: 恢复中心（用于心跳）
        """
        self.asr = asr
        self.tts = tts
        self.query_bus = query_bus
        self.recovery_center = recovery_center
        self.intent_parser = IntentParser()
        
        # 运行状态
        self.running = False
        self.asr_count = 0
        self.tts_count = 0
        
        # 普通指令处理器
        self.command_handlers: Dict[str, Callable] = {}
        
        logger.info("[SPEECH_PIPELINE] Initialized")
    
    def register_command_handler(self, intent: str, handler: Callable) -> None:
        """注册指令处理器"""
        self.command_handlers[intent] = handler
        logger.info(f"[SPEECH_PIPELINE] Registered command handler: {intent}")
    
    async def loop(self):
        """
        语音管线主循环（异步版本）
        """
        logger.info("[SPEECH_PIPELINE] Starting speech pipeline loop...")
        self.running = True
        
        while self.running:
            try:
                # 更新心跳
                if self.recovery_center:
                    self.recovery_center.update_heartbeat("speech")
                
                # ASR 监听
                if self.asr:
                    try:
                        text = await self.asr.listen()
                    except Exception as e:
                        logger.exception(f"[SPEECH_PIPELINE] ASR listen error: {e}")
                        await asyncio.sleep(0.1)
                        continue
                else:
                    # 如果没有 ASR，使用模拟输入（测试用）
                    await asyncio.sleep(0.1)
                    continue
                
                if text is None or text.strip() == "":
                    continue
                
                logger.info(f"[SPEECH_PIPELINE] ASR result: {text}")
                self.asr_count += 1
                
                # 1) 若当前有等待回答的 Query
                if self.query_bus and self.query_bus.get_active_query():
                    logger.info("[SPEECH_PIPELINE] Processing query response")
                    parsed = self.intent_parser.parse(text)
                    self.query_bus.resolve_active(parsed)
                    continue
                
                # 2) 若无 Query → 普通指令
                parsed = self.intent_parser.parse(text)
                self.handle_normal_command(parsed)
                
            except Exception as e:
                logger.exception(f"[SPEECH_PIPELINE] Loop error: {e}")
                await asyncio.sleep(0.1)
    
    def loop_sync(self):
        """
        语音管线主循环（同步版本，用于非异步环境）
        """
        logger.info("[SPEECH_PIPELINE] Starting speech pipeline loop (sync)...")
        self.running = True
        
        import time
        while self.running:
            try:
                # 更新心跳
                if self.recovery_center:
                    self.recovery_center.update_heartbeat("speech")
                
                # ASR 监听（同步版本）
                if self.asr and hasattr(self.asr, 'listen_sync'):
                    try:
                        text = self.asr.listen_sync()
                    except Exception as e:
                        logger.exception(f"[SPEECH_PIPELINE] ASR listen error: {e}")
                        time.sleep(0.1)
                        continue
                else:
                    # 如果没有 ASR，跳过
                    time.sleep(0.1)
                    continue
                
                if text is None or text.strip() == "":
                    continue
                
                logger.info(f"[SPEECH_PIPELINE] ASR result: {text}")
                self.asr_count += 1
                
                # 1) 若当前有等待回答的 Query
                if self.query_bus and self.query_bus.get_active_query():
                    logger.info("[SPEECH_PIPELINE] Processing query response")
                    parsed = self.intent_parser.parse(text)
                    self.query_bus.resolve_active(parsed)
                    continue
                
                # 2) 若无 Query → 普通指令
                parsed = self.intent_parser.parse(text)
                self.handle_normal_command(parsed)
                
            except Exception as e:
                logger.exception(f"[SPEECH_PIPELINE] Loop error: {e}")
                time.sleep(0.1)
    
    def handle_normal_command(self, parsed: Dict[str, Any]) -> None:
        """
        处理普通指令
        
        Args:
            parsed: 解析后的意图结果
        """
        intent = parsed.get("intent")
        logger.info(f"[SPEECH_PIPELINE] Handling normal command: {intent}")
        
        # 查找对应的处理器
        if intent in self.command_handlers:
            try:
                self.command_handlers[intent](parsed)
            except Exception as e:
                logger.exception(f"[SPEECH_PIPELINE] Command handler error: {e}")
        else:
            logger.warning(f"[SPEECH_PIPELINE] No handler for intent: {intent}")
    
    def say(self, text: str) -> None:
        """
        TTS 播报
        
        Args:
            text: 要播报的文本
        """
        if self.tts:
            try:
                if hasattr(self.tts, 'speak'):
                    self.tts.speak(text)
                elif hasattr(self.tts, 'say'):
                    self.tts.say(text)
                else:
                    logger.warning("[SPEECH_PIPELINE] TTS object has no speak/say method")
                self.tts_count += 1
                logger.info(f"[SPEECH_PIPELINE] TTS: {text}")
            except Exception as e:
                logger.exception(f"[SPEECH_PIPELINE] TTS error: {e}")
        else:
            logger.warning(f"[SPEECH_PIPELINE] TTS not available: {text}")
    
    def restart(self) -> None:
        """
        重启语音模块
        """
        logger.warning("[SPEECH_PIPELINE] Restarting speech pipeline...")
        
        # 停止当前循环
        self.running = False
        
        # TODO: 实际重启逻辑
        # 1. 停止 ASR/TTS 线程
        # 2. 重新初始化
        # 3. 重启线程
        
        # 更新心跳
        if self.recovery_center:
            self.recovery_center.update_heartbeat("speech")
        
        # 重新启动循环（在后台线程中）
        import threading
        def restart_loop():
            time.sleep(0.5)  # 等待一下
            self.running = True
            if asyncio.iscoroutinefunction(self.loop):
                asyncio.run(self.loop())
            else:
                self.loop_sync()
        
        thread = threading.Thread(target=restart_loop, daemon=True)
        thread.start()
        
        logger.info("[SPEECH_PIPELINE] Speech pipeline restarted")
    
    def stop(self) -> None:
        """停止语音管线"""
        self.running = False
        logger.info("[SPEECH_PIPELINE] Speech pipeline stopped")
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "asr_count": self.asr_count,
            "tts_count": self.tts_count,
            "running": self.running,
            "has_active_query": self.query_bus.get_active_query() is not None if self.query_bus else False,
        }




