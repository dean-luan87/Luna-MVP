#!/usr/bin/env python3
"""
语音管线集成点
v1.4.2: 整合 QueryBus, ASR, TTS
"""
import logging
from typing import Optional, Callable, Dict, Any

from core.task.query_bus import QueryBus, QueryStatus

logger = logging.getLogger(__name__)


class SpeechPipelineIntegration:
    """
    语音管线集成：整合问询总线、ASR、TTS
    """
    
    def __init__(
        self,
        query_bus: Optional[QueryBus] = None,
        asr_recognize: Optional[Callable[[], Optional[str]]] = None,
        tts_say: Optional[Callable[[str], None]] = None,
        nlu_parse: Optional[Callable[[str], Dict[str, Any]]] = None,
    ):
        """
        初始化语音管线集成
        
        Args:
            query_bus: 问询总线
            asr_recognize: ASR 识别函数（返回文本或 None）
            tts_say: TTS 播报函数
            nlu_parse: NLU 解析函数（文本 -> 意图+槽位）
        """
        self.query_bus = query_bus
        self.asr_recognize = asr_recognize
        self.tts_say = tts_say
        self.nlu_parse = nlu_parse
        
        # 统计
        self.asr_count = 0
        self.tts_count = 0
        
        logger.info("[SPEECH_PIPELINE] Initialized")
    
    def tick(self) -> None:
        """
        语音管线 tick（应该每帧调用）
        处理问询总线的播报和超时
        """
        if self.query_bus:
            self.query_bus.tick()
    
    def process_asr_result(self, asr_text: Optional[str]) -> None:
        """
        处理 ASR 结果
        
        Args:
            asr_text: ASR 识别的文本
        """
        if not asr_text or not self.query_bus:
            return
        
        # 检查是否有活跃的问询
        active_query = self.query_bus.get_active_query()
        if not active_query:
            # 没有活跃问询，正常处理 ASR 结果
            logger.debug(f"[SPEECH_PIPELINE] ASR result (no active query): {asr_text}")
            return
        
        # 有活跃问询，解析用户回答
        logger.info(f"[SPEECH_PIPELINE] ASR result for active query: {asr_text}")
        
        # 使用 NLU 解析（如果有）
        if self.nlu_parse:
            try:
                parsed = self.nlu_parse(asr_text)
                self.query_bus.resolve_active(parsed)
                logger.info(f"[SPEECH_PIPELINE] Query resolved with NLU: {parsed}")
            except Exception as e:
                logger.exception(f"[SPEECH_PIPELINE] NLU parse error: {e}")
                # 降级：简单关键词匹配
                self._resolve_with_keywords(asr_text)
        else:
            # 没有 NLU，使用关键词匹配
            self._resolve_with_keywords(asr_text)
        
        self.asr_count += 1
    
    def _resolve_with_keywords(self, text: str) -> None:
        """使用关键词匹配解析用户回答"""
        text_lower = text.lower()
        
        # 确认关键词
        if any(kw in text_lower for kw in ["是", "yes", "对", "好", "可以", "继续", "去"]):
            self.query_bus.resolve_active({"answer": "yes"})
            logger.info("[SPEECH_PIPELINE] Resolved as YES")
        # 否定关键词
        elif any(kw in text_lower for kw in ["否", "no", "不", "不要", "停止", "结束"]):
            self.query_bus.resolve_active({"answer": "no"})
            logger.info("[SPEECH_PIPELINE] Resolved as NO")
        else:
            # 无法解析，记录日志
            logger.warning(f"[SPEECH_PIPELINE] Cannot resolve answer from: {text}")
    
    def say(self, text: str) -> None:
        """
        TTS 播报
        
        Args:
            text: 要播报的文本
        """
        if self.tts_say:
            try:
                self.tts_say(text)
                self.tts_count += 1
                logger.info(f"[SPEECH_PIPELINE] TTS: {text}")
            except Exception as e:
                logger.exception(f"[SPEECH_PIPELINE] TTS error: {e}")
        else:
            logger.warning(f"[SPEECH_PIPELINE] TTS function not available: {text}")
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "asr_count": self.asr_count,
            "tts_count": self.tts_count,
            "has_active_query": self.query_bus.get_active_query() is not None if self.query_bus else False,
        }




