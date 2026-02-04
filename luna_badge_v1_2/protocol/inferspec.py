#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
InferSpec - 后端到前端推理结果规范

版本: 1.0.0
"""

from typing import Dict, Any, Optional, List
import time


class InferSpec:
    """推理结果规范验证和转换"""
    
    PROTOCOL_VERSION = "1.0.0"
    
    @staticmethod
    def validate(data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        验证推理结果是否符合规范
        
        Returns:
            (is_valid, error_message)
        """
        # 必须字段检查
        required = [
            "type", "frame_id", "client_ts", "server_ts",
            "infer_ts", "nav_ts", "infer_ms", "nav_ms", "total_ms"
        ]
        for field in required:
            if field not in data:
                return False, f"缺少必须字段: {field}"
        
        # 类型检查
        if data["type"] != "infer_result":
            return False, f"type 必须是 'infer_result'，实际: {data['type']}"
        
        if not isinstance(data["frame_id"], int):
            return False, f"frame_id 必须是整数"
        
        # 时间戳检查
        for ts_field in ["client_ts", "server_ts", "infer_ts", "nav_ts"]:
            if not isinstance(data[ts_field], (int, float)):
                return False, f"{ts_field} 必须是数字"
        
        # 延迟检查
        for ms_field in ["infer_ms", "nav_ms", "total_ms"]:
            if not isinstance(data[ms_field], (int, float)) or data[ms_field] < 0:
                return False, f"{ms_field} 必须是非负数字"
        
        return True, None
    
    @staticmethod
    def parse(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        解析并标准化推理结果
        
        Returns:
            标准化后的推理结果
        """
        is_valid, error = InferSpec.validate(data)
        if not is_valid:
            raise ValueError(f"InferSpec 验证失败: {error}")
        
        result = data.copy()
        result.setdefault("protocol_version", InferSpec.PROTOCOL_VERSION)
        
        return result
    
    @staticmethod
    def create(
        frame_id: int,
        client_ts: float,
        server_ts: float,
        infer_ts: float,
        nav_ts: float,
        infer_ms: float,
        nav_ms: float,
        objects: Optional[List[Dict[str, Any]]] = None,
        nav: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        创建符合规范的推理结果
        
        Args:
            frame_id: 帧 ID
            client_ts: 客户端时间戳
            server_ts: 服务器收到时间戳
            infer_ts: 推理结束时间戳
            nav_ts: 导航结束时间戳
            infer_ms: 推理耗时（毫秒）
            nav_ms: 导航耗时（毫秒）
            objects: 检测到的对象列表
            nav: 导航决策信息
        
        Returns:
            符合规范的推理结果字典
        """
        total_ms = infer_ms + nav_ms
        
        result = {
            "type": "infer_result",
            "protocol_version": InferSpec.PROTOCOL_VERSION,
            "frame_id": frame_id,
            "client_ts": client_ts,
            "server_ts": server_ts,
            "infer_ts": infer_ts,
            "nav_ts": nav_ts,
            "infer_ms": infer_ms,
            "nav_ms": nav_ms,
            "total_ms": total_ms,
        }
        
        if objects is not None:
            result["objects"] = objects
        
        if nav is not None:
            result["nav"] = nav
        
        is_valid, error = InferSpec.validate(result)
        if not is_valid:
            raise ValueError(f"创建的推理结果无效: {error}")
        
        return result

















