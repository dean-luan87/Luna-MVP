#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ErrorSpec - 标准错误码规范

版本: 1.0.0
"""

from typing import Dict, Any, Optional
import re
import time


class ErrorSpec:
    """错误码规范验证和转换"""
    
    PROTOCOL_VERSION = "1.0.0"
    
    # 错误码定义
    ERROR_CODES = {
        # 摄像头相关
        "CAM-001": "相机权限被拒绝",
        "CAM-002": "无法获取相机数据",
        "CAM-003": "帧编码失败",
        # WebSocket 相关
        "WS-001": "WS 连接失败",
        "WS-002": "WS 发送数据失败",
        "WS-003": "WS 意外断开",
        # 推理相关
        "INF-001": "YOLO 推理超时",
        "INF-002": "推理结果为空",
        "INF-003": "模型加载失败",
        # 导航相关
        "NAV-001": "无法生成导航决策",
        "NAV-002": "地图/路径规划失败",
        "NAV-003": "导航超时",
        # 系统相关
        "SYS-001": "CPU/内存过载",
        "SYS-002": "GPU 过热",
        "SYS-003": "磁盘空间不足",
    }
    
    @staticmethod
    def validate(data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        验证错误数据是否符合规范
        
        Returns:
            (is_valid, error_message)
        """
        # 必须字段检查
        required = ["type", "code", "message"]
        for field in required:
            if field not in data:
                return False, f"缺少必须字段: {field}"
        
        # 类型检查
        if data["type"] != "error":
            return False, f"type 必须是 'error'，实际: {data['type']}"
        
        # 错误码格式检查
        code = data["code"]
        if not re.match(r"^[A-Z]{3}-\d{3}$", code):
            return False, f"错误码格式无效: {code}，应为 XXX-###"
        
        # 检查错误码是否在定义中
        if code not in ErrorSpec.ERROR_CODES:
            return False, f"未知错误码: {code}"
        
        return True, None
    
    @staticmethod
    def parse(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        解析并标准化错误数据
        
        Returns:
            标准化后的错误数据
        """
        is_valid, error = ErrorSpec.validate(data)
        if not is_valid:
            raise ValueError(f"ErrorSpec 验证失败: {error}")
        
        result = data.copy()
        result.setdefault("protocol_version", ErrorSpec.PROTOCOL_VERSION)
        
        return result
    
    @staticmethod
    def create(
        code: str,
        message: Optional[str] = None,
        detail: Optional[str] = None,
        client_ts: Optional[float] = None,
        server_ts: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        创建符合规范的错误数据
        
        Args:
            code: 错误码（格式：XXX-###）
            message: 错误消息（如果为 None，使用默认消息）
            detail: 错误详情
            client_ts: 客户端时间戳
            server_ts: 服务器时间戳
        
        Returns:
            符合规范的错误字典
        """
        if message is None:
            message = ErrorSpec.ERROR_CODES.get(code, "未知错误")
        
        error = {
            "type": "error",
            "protocol_version": ErrorSpec.PROTOCOL_VERSION,
            "code": code,
            "message": message,
        }
        
        if detail:
            error["detail"] = detail
        
        if client_ts is not None:
            error["client_ts"] = client_ts
        
        if server_ts is not None:
            error["server_ts"] = server_ts
        else:
            error["server_ts"] = time.time()
        
        is_valid, err_msg = ErrorSpec.validate(error)
        if not is_valid:
            raise ValueError(f"创建的错误数据无效: {err_msg}")
        
        return error
    
    @staticmethod
    def get_message(code: str) -> str:
        """获取错误码对应的默认消息"""
        return ErrorSpec.ERROR_CODES.get(code, "未知错误")

















