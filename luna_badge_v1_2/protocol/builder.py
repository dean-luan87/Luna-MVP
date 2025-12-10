#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
协议构建器 - 统一消息构建

版本: 1.0.0
"""

from typing import Dict, Any, Optional, List
import time

from .inferspec import InferSpec
from .heartbeatspec import HeartbeatSpec
from .errorspec import ErrorSpec


def build_infer_result(
    frame_id: int,
    client_ts: float,
    infer_ms: float,
    nav_ms: float,
    objects: Optional[List[Dict[str, Any]]] = None,
    nav: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    构建推理结果（InferSpec）
    
    Args:
        frame_id: 帧 ID
        client_ts: 客户端时间戳
        infer_ms: YOLO 推理耗时（毫秒）
        nav_ms: 导航决策耗时（毫秒）
        objects: 检测到的对象列表
        nav: 导航决策信息
    
    Returns:
        符合 InferSpec 的推理结果字典
    """
    server_ts = time.time() * 1000  # 转换为毫秒
    infer_ts = server_ts + infer_ms
    nav_ts = infer_ts + nav_ms
    
    return InferSpec.create(
        frame_id=frame_id,
        client_ts=client_ts,
        server_ts=server_ts,
        infer_ts=infer_ts,
        nav_ts=nav_ts,
        infer_ms=infer_ms,
        nav_ms=nav_ms,
        objects=objects or [],
        nav=nav
    )


def build_heartbeat_ack(seq: int, client_ts: float) -> Dict[str, Any]:
    """
    构建心跳确认（HeartbeatSpec）
    
    Args:
        seq: 心跳序号
        client_ts: 客户端时间戳
    
    Returns:
        符合 HeartbeatSpec 的心跳确认字典
    """
    return HeartbeatSpec.create_heartbeat_ack(seq=seq, client_ts=client_ts)


def build_error(code: str, message: Optional[str] = None, detail: Optional[str] = None) -> Dict[str, Any]:
    """
    构建错误响应（ErrorSpec）
    
    Args:
        code: 错误码
        message: 错误消息（可选）
        detail: 错误详情（可选）
    
    Returns:
        符合 ErrorSpec 的错误字典
    """
    return ErrorSpec.create(code=code, message=message, detail=detail)





