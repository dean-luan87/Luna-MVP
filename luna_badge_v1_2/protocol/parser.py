#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
协议解析器 - 统一消息解析和验证

版本: 1.0.0
"""

from typing import Dict, Any, Optional, Tuple
import json

from .framespec import FrameSpec
from .heartbeatspec import HeartbeatSpec
from .errorspec import ErrorSpec


class ProtocolError(Exception):
    """协议错误"""
    pass


def parse_message(raw: str) -> Tuple[str, Dict[str, Any]]:
    """
    解析 WebSocket 消息
    
    Args:
        raw: 原始 JSON 字符串
    
    Returns:
        (message_type, parsed_data)
    
    Raises:
        ProtocolError: 如果消息格式无效
    """
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ProtocolError(f"JSON 解析失败: {e}")
    
    msg_type = data.get("type")
    if not msg_type:
        raise ProtocolError("缺少 type 字段")
    
    # 检查协议版本
    protocol_version = data.get("protocol_version", "1.0.0")
    if not _check_protocol_version(protocol_version):
        raise ProtocolError(f"协议版本不兼容: {protocol_version}")
    
    # 根据类型解析
    if msg_type == "frame":
        is_valid, error = FrameSpec.validate(data)
        if not is_valid:
            raise ProtocolError(f"FrameSpec 验证失败: {error}")
        return "frame", FrameSpec.parse(data)
    
    elif msg_type == "heartbeat":
        is_valid, error = HeartbeatSpec.validate_heartbeat(data)
        if not is_valid:
            raise ProtocolError(f"HeartbeatSpec 验证失败: {error}")
        return "heartbeat", data
    
    else:
        raise ProtocolError(f"未知消息类型: {msg_type}")


def _check_protocol_version(version: str) -> bool:
    """
    检查协议版本兼容性
    
    Args:
        version: 协议版本号（格式：MAJOR.MINOR.PATCH）
    
    Returns:
        是否兼容
    """
    try:
        major = int(version.split(".")[0])
        # 当前版本是 1.0.0，只支持主版本号为 1
        return major == 1
    except (ValueError, IndexError):
        return False


def create_error_response(code: str, message: Optional[str] = None, detail: Optional[str] = None) -> Dict[str, Any]:
    """
    创建错误响应（ErrorSpec）
    
    Args:
        code: 错误码
        message: 错误消息（可选，使用默认消息）
        detail: 错误详情（可选）
    
    Returns:
        符合 ErrorSpec 的错误字典
    """
    return ErrorSpec.create(code=code, message=message, detail=detail)


def create_protocol_warning(current_version: str, recommended_version: str = "1.0.0") -> Dict[str, Any]:
    """
    创建协议版本警告
    
    Args:
        current_version: 当前客户端版本
        recommended_version: 推荐版本
    
    Returns:
        警告消息字典
    """
    return {
        "type": "warning",
        "code": "PROTO-001",
        "message": f"您的协议版本 {current_version} 已过时。请升级到 {recommended_version}。",
        "current_version": current_version,
        "recommended_version": recommended_version
    }

