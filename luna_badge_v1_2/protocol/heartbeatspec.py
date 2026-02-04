#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HeartbeatSpec - WebSocket 心跳规范

版本: 1.0.0
"""

from typing import Dict, Any, Optional
import time


class HeartbeatSpec:
    """心跳规范验证和转换"""
    
    PROTOCOL_VERSION = "1.0.0"
    
    @staticmethod
    def validate_heartbeat(data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """验证心跳消息"""
        required = ["type", "seq", "client_ts"]
        for field in required:
            if field not in data:
                return False, f"缺少必须字段: {field}"
        
        if data["type"] != "heartbeat":
            return False, f"type 必须是 'heartbeat'"
        
        if not isinstance(data["seq"], int):
            return False, "seq 必须是整数"
        
        if not isinstance(data["client_ts"], (int, float)):
            return False, "client_ts 必须是数字"
        
        return True, None
    
    @staticmethod
    def validate_heartbeat_ack(data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """验证心跳确认消息"""
        required = ["type", "seq", "client_ts", "server_ts"]
        for field in required:
            if field not in data:
                return False, f"缺少必须字段: {field}"
        
        if data["type"] != "heartbeat_ack":
            return False, f"type 必须是 'heartbeat_ack'"
        
        if not isinstance(data["seq"], int):
            return False, "seq 必须是整数"
        
        if not isinstance(data["client_ts"], (int, float)):
            return False, "client_ts 必须是数字"
        
        if not isinstance(data["server_ts"], (int, float)):
            return False, "server_ts 必须是数字"
        
        return True, None
    
    @staticmethod
    def create_heartbeat(seq: int, client_ts: Optional[float] = None) -> Dict[str, Any]:
        """创建心跳消息"""
        if client_ts is None:
            client_ts = time.time()
        
        heartbeat = {
            "type": "heartbeat",
            "protocol_version": HeartbeatSpec.PROTOCOL_VERSION,
            "seq": seq,
            "client_ts": client_ts
        }
        
        is_valid, error = HeartbeatSpec.validate_heartbeat(heartbeat)
        if not is_valid:
            raise ValueError(f"创建的心跳消息无效: {error}")
        
        return heartbeat
    
    @staticmethod
    def create_heartbeat_ack(
        seq: int,
        client_ts: float,
        server_ts: Optional[float] = None
    ) -> Dict[str, Any]:
        """创建心跳确认消息"""
        if server_ts is None:
            server_ts = time.time()
        
        ack = {
            "type": "heartbeat_ack",
            "protocol_version": HeartbeatSpec.PROTOCOL_VERSION,
            "seq": seq,
            "client_ts": client_ts,
            "server_ts": server_ts
        }
        
        is_valid, error = HeartbeatSpec.validate_heartbeat_ack(ack)
        if not is_valid:
            raise ValueError(f"创建的心跳确认消息无效: {error}")
        
        return ack

















