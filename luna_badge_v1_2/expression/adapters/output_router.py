"""
Output Router (C-4)

输出路由器（一期先支持 debug/voice_text）
"""

from typing import Dict, Any, Optional
from .output_channel_models import OutputChannel
from ..renderer.render_models import RenderedMessage


class OutputRouter:
    """
    输出路由器
    
    职责：
    - 输入 RenderedMessage
    - 输出 channel + payload（先用 print 或返回 dict）
    - 一期先支持 debug/voice_text
    """
    
    def __init__(self, default_channel: OutputChannel = OutputChannel.DEBUG):
        """
        初始化输出路由器
        
        Args:
            default_channel: 默认输出通道
        """
        self.default_channel = default_channel
    
    def route(
        self,
        message: RenderedMessage,
        channel: Optional[OutputChannel] = None
    ) -> Dict[str, Any]:
        """
        路由消息到输出通道
        
        Args:
            message: 渲染后的消息
            channel: 输出通道（可选，默认使用 default_channel）
            
        Returns:
            Dict[str, Any]: 输出结果（channel + payload）
        """
        if channel is None:
            channel = self.default_channel
        
        # 根据通道类型处理
        if channel == OutputChannel.DEBUG:
            payload = self._route_to_debug(message)
        elif channel == OutputChannel.VOICE_TEXT:
            payload = self._route_to_voice_text(message)
        else:
            payload = {"error": f"Unsupported channel: {channel}"}
        
        return {
            "channel": channel.value,
            "payload": payload
        }
    
    def _route_to_debug(self, message: RenderedMessage) -> Dict[str, Any]:
        """
        路由到调试输出
        
        Args:
            message: 渲染后的消息
            
        Returns:
            Dict[str, Any]: 调试输出负载
        """
        # 一期：先用 print
        print(f"[EXPR_OUTPUT] {message.text}")
        
        return {
            "text": message.text,
            "protocol": message.protocol.value,
            "embodiment": message.embodiment,
            "tags": message.tags
        }
    
    def _route_to_voice_text(self, message: RenderedMessage) -> Dict[str, Any]:
        """
        路由到语音文本输出
        
        Args:
            message: 渲染后的消息
            
        Returns:
            Dict[str, Any]: 语音文本输出负载
        """
        # 一期：返回文本（后续接 TTS）
        return {
            "text": message.text,
            "protocol": message.protocol.value,
            "embodiment": message.embodiment
        }
