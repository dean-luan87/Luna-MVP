# core/response.py
# 统一 API 响应封装（与错误码规范对接）

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple, Union

from flask import jsonify

from config.error_codes import ErrorCodeSpec, get_error_spec, DEFAULT_INTERNAL_ERROR


def api_success(data: Any = None, message: Optional[str] = None):
    """
    统一成功响应格式：
    {
      "success": true,
      "data": {...},
      "message": "可选提示"
    }
    """
    resp: Dict[str, Any] = {
        "success": True,
        "data": data,
    }
    if message:
        resp["message"] = message
    return jsonify(resp)


def api_error(
    error: Union[str, ErrorCodeSpec],
    details: Optional[Dict[str, Any]] = None,
    status_code: Optional[int] = None,
):
    """
    统一错误响应格式：
    {
      "success": false,
      "error": {
        "key": "VISION_ENGINE_NOT_INITIALIZED",
        "code": "VIS-1001",
        "category": "VIS",
        "message": "Vision engine is not initialized",
        "user_message": "视觉模块暂时不可用。"
      },
      "details": {...}  // 可选
    }

    调用方式：
      - api_error("VISION_ENGINE_NOT_INITIALIZED")
      - api_error("VIS-1001")
      - api_error("自定义错误提示字符串")  # 兼容老代码
    """

    # 1) 解析错误规范
    if isinstance(error, ErrorCodeSpec):
        spec = error
        key = None  # 无 key 信息
    elif isinstance(error, str):
        # 尝试作为 key 或 code 解析
        from config.error_codes import ERROR_REGISTRY
        spec = get_error_spec(error)
        # 如果spec是默认错误且error不在注册表中，说明是自定义字符串
        if spec == DEFAULT_INTERNAL_ERROR and error not in ERROR_REGISTRY:
            # 自定义字符串，创建临时错误规范
            from config.error_codes import ErrorCategory
            spec = ErrorCodeSpec(
                code="CUSTOM-0001",
                category=ErrorCategory.UNKNOWN,
                http_status=status_code or 500,
                message=error,
                user_message=error
            )
        key = error if error in ERROR_REGISTRY else None
    else:
        spec = DEFAULT_INTERNAL_ERROR
        key = None

    # 2) HTTP 状态码
    http_status = status_code or spec.http_status

    # 3) 组装响应体
    error_payload: Dict[str, Any] = {
        "code": spec.code,
        "category": spec.category.value,
        "message": spec.message,
        "user_message": spec.user_message,
    }
    if key:
        error_payload["key"] = key

    resp: Dict[str, Any] = {
        "success": False,
        "error": error_payload,
    }

    if details:
        resp["details"] = details

    return jsonify(resp), http_status


# ========== 向后兼容：保留ok()和error()函数 ==========

def ok(data: Any = None, message: Optional[str] = None):
    """向后兼容：成功响应（别名）"""
    return api_success(data, message)


def error(
    code: Union[int, str, ErrorCodeSpec],
    message: Optional[str] = None,
    http_status: Optional[int] = None,
    details: Optional[Dict[str, Any]] = None,
):
    """
    向后兼容：错误响应（别名）
    
    支持多种调用方式：
    - error(ERR.VISION_NOT_READY, "视觉引擎未初始化")
    - error("VISION_ENGINE_NOT_INITIALIZED")
    - error("VIS-1001")
    """
    if isinstance(code, int):
        # 数字错误码，转换为字符串key查找
        from config.error_codes import ERROR_REGISTRY
        # 尝试通过数字码查找
        for key, spec in ERROR_REGISTRY.items():
            if hasattr(spec, 'code') and str(code) in spec.code:
                return api_error(key, details, http_status)
        # 找不到，使用message作为自定义错误
        if message:
            return api_error(message, details, http_status or 500)
        return api_error("SYS_INTERNAL_ERROR", details, http_status)
    else:
        # 字符串错误码或ErrorCodeSpec
        return api_error(code, details, http_status)
