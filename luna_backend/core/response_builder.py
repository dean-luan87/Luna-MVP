"""
统一响应构建器 (v1.2.0)
提供ResponseBuilder类，统一构建API响应格式
"""

from flask import jsonify
from typing import Any, Dict, Optional
import time

# 生成request_id的简单计数器
_request_counter = 0

def _get_request_id() -> str:
    """生成请求ID"""
    global _request_counter
    _request_counter += 1
    return f"req_{int(time.time() * 1000)}_{_request_counter}"


class ResponseBuilder:
    """统一响应构建器"""
    
    def success(self, data: Optional[Any] = None, message: str = "OK") -> tuple:
        """
        构建成功响应
        
        Args:
            data: 响应数据
            message: 成功消息
        
        Returns:
            Flask Response: JSON格式的成功响应
        """
        return jsonify({
            "success": True,
            "code": 0,
            "message": message,
            "timestamp": int(time.time() * 1000),
            "request_id": _get_request_id(),
            "data": data or {}
        }), 200
    
    def error(self, error_code: str, details: Optional[Dict[str, Any]] = None, 
              status_code: int = 200, message: Optional[str] = None) -> tuple:
        """
        构建错误响应
        
        Args:
            error_code: 错误码（如 "NAV_MANAGER_NOT_INITIALIZED"）
            details: 错误详情
            status_code: HTTP状态码
            message: 错误消息（可选，如果不提供则从错误码描述中获取）
        
        Returns:
            Flask Response: JSON格式的错误响应
        """
        from config.error_codes import ErrorCode
        
        # 尝试从ErrorCode获取错误描述
        error_message = message
        if not error_message:
            try:
                # 解析错误码（如 "NAV_MANAGER_NOT_INITIALIZED"）
                parts = error_code.split("_", 1)
                if len(parts) == 2:
                    namespace = parts[0]
                    code_name = parts[1]
                    namespace_obj = getattr(ErrorCode, namespace, None)
                    if namespace_obj:
                        error_message = namespace_obj.describe(code_name)
            except:
                pass
        
        if not error_message:
            error_message = f"错误: {error_code}"
        
        # 记录错误日志
        from utils.logger import log_error
        try:
            # 尝试将错误码转换为数字（如果可能）
            error_code_num = getattr(ErrorCode, error_code.replace("_", "."), None)
            if error_code_num:
                log_error(error_code_num, error_message, details)
        except:
            pass
        
        response = {
            "success": False,
            "code": error_code,
            "message": error_message,
            "timestamp": int(time.time() * 1000),
            "request_id": _get_request_id(),
            "data": details or {}
        }
        
        return jsonify(response), status_code



