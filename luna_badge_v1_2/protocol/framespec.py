#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FrameSpec - 前端到后端帧数据规范

版本: 1.0.0
"""

from typing import Dict, Any, Optional
import base64


class FrameSpec:
    """帧数据规范验证和转换"""
    
    PROTOCOL_VERSION = "1.0.0"
    
    @staticmethod
    def validate(data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        验证帧数据是否符合规范
        
        Returns:
            (is_valid, error_message)
        """
        # 必须字段检查
        required = ["type", "frame_id", "client_ts", "width", "height", "image_base64"]
        for field in required:
            if field not in data:
                return False, f"缺少必须字段: {field}"
        
        # 类型检查
        if data["type"] != "frame":
            return False, f"type 必须是 'frame'，实际: {data['type']}"
        
        if not isinstance(data["frame_id"], int):
            return False, f"frame_id 必须是整数，实际: {type(data['frame_id'])}"
        
        if not isinstance(data["client_ts"], (int, float)):
            return False, f"client_ts 必须是数字，实际: {type(data['client_ts'])}"
        
        if not isinstance(data["width"], int) or data["width"] <= 0:
            return False, f"width 必须是正整数，实际: {data['width']}"
        
        if not isinstance(data["height"], int) or data["height"] <= 0:
            return False, f"height 必须是正整数，实际: {data['height']}"
        
        if not isinstance(data["image_base64"], str) or not data["image_base64"]:
            return False, "image_base64 必须是非空字符串"
        
        # 验证 base64 格式
        try:
            base64.b64decode(data["image_base64"], validate=True)
        except Exception as e:
            return False, f"image_base64 格式无效: {e}"
        
        return True, None
    
    @staticmethod
    def parse(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        解析并标准化帧数据
        
        Returns:
            标准化后的帧数据
        """
        is_valid, error = FrameSpec.validate(data)
        if not is_valid:
            raise ValueError(f"FrameSpec 验证失败: {error}")
        
        # 确保 protocol_version 存在
        result = data.copy()
        result.setdefault("protocol_version", FrameSpec.PROTOCOL_VERSION)
        
        return result
    
    @staticmethod
    def create(
        frame_id: int,
        client_ts: float,
        width: int,
        height: int,
        image_base64: str,
        meta: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        创建符合规范的帧数据
        
        Args:
            frame_id: 帧序号
            client_ts: 客户端时间戳
            width: 图像宽度
            height: 图像高度
            image_base64: Base64 编码的图像
            meta: 元数据（可选）
        
        Returns:
            符合规范的帧数据字典
        """
        frame = {
            "type": "frame",
            "protocol_version": FrameSpec.PROTOCOL_VERSION,
            "frame_id": frame_id,
            "client_ts": client_ts,
            "width": width,
            "height": height,
            "image_base64": image_base64,
        }
        
        if meta:
            frame["meta"] = meta
        
        is_valid, error = FrameSpec.validate(frame)
        if not is_valid:
            raise ValueError(f"创建的帧数据无效: {error}")
        
        return frame


