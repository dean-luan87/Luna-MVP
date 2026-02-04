"""
Error Codes (v1.3.0)

错误码体系

定义系统统一的错误码，便于错误追踪和处理
"""

from enum import Enum
from typing import Dict, Any


class ErrorCode(Enum):
    """错误码枚举"""

    # ========== 系统级错误 (E1xx) ==========
    E100 = "E100"  # 系统初始化失败
    E101 = "E101"  # 配置加载失败
    E102 = "E102"  # 资源不足
    E103 = "E103"  # 权限不足

    # ========== 模型相关错误 (E2xx) ==========
    E200 = "E200"  # 模型加载失败
    E201 = "E201"  # L1 模型加载失败
    E202 = "E202"  # L2 模型加载失败
    E203 = "E203"  # 模型推理失败
    E204 = "E204"  # 模型超时
    E205 = "E205"  # 模型内存不足
    E206 = "E206"  # 模型版本不匹配

    # ========== 路由相关错误 (E3xx) ==========
    E300 = "E300"  # 路由器初始化失败
    E301 = "E301"  # 路由决策失败
    E302 = "E302"  # L1 模型不可用
    E303 = "E303"  # L2 模型不可用
    E304 = "E304"  # 所有模型不可用
    E305 = "E305"  # 意图分类失败

    # ========== 推理相关错误 (E4xx) ==========
    E400 = "E400"  # 推理封装初始化失败
    E401 = "E401"  # 输入验证失败
    E402 = "E402"  # 输出解析失败
    E403 = "E403"  # 推理超时
    E404 = "E404"  # 推理异常

    # ========== 埋点相关错误 (E5xx) ==========
    E500 = "E500"  # 埋点系统初始化失败
    E501 = "E501"  # 埋点数据记录失败
    E502 = "E502"  # 埋点数据存储失败
    E503 = "E503"  # 埋点数据查询失败

    # ========== 回放相关错误 (E6xx) ==========
    E600 = "E600"  # 回放系统初始化失败
    E601 = "E601"  # 回放数据加载失败
    E602 = "E602"  # 回放数据解析失败
    E603 = "E603"  # 回放数据保存失败

    # ========== 成功状态 ==========
    SUCCESS = "SUCCESS"  # 成功
    PENDING = "PENDING"  # 进行中


class ErrorInfo:
    """错误信息类"""

    ERROR_MESSAGES: Dict[ErrorCode, str] = {
        # 系统级错误
        ErrorCode.E100: "系统初始化失败",
        ErrorCode.E101: "配置加载失败",
        ErrorCode.E102: "资源不足",
        ErrorCode.E103: "权限不足",

        # 模型相关错误
        ErrorCode.E200: "模型加载失败",
        ErrorCode.E201: "L1 模型加载失败",
        ErrorCode.E202: "L2 模型加载失败",
        ErrorCode.E203: "模型推理失败",
        ErrorCode.E204: "模型超时",
        ErrorCode.E205: "模型内存不足",
        ErrorCode.E206: "模型版本不匹配",

        # 路由相关错误
        ErrorCode.E300: "路由器初始化失败",
        ErrorCode.E301: "路由决策失败",
        ErrorCode.E302: "L1 模型不可用",
        ErrorCode.E303: "L2 模型不可用",
        ErrorCode.E304: "所有模型不可用",
        ErrorCode.E305: "意图分类失败",

        # 推理相关错误
        ErrorCode.E400: "推理封装初始化失败",
        ErrorCode.E401: "输入验证失败",
        ErrorCode.E402: "输出解析失败",
        ErrorCode.E403: "推理超时",
        ErrorCode.E404: "推理异常",

        # 埋点相关错误
        ErrorCode.E500: "埋点系统初始化失败",
        ErrorCode.E501: "埋点数据记录失败",
        ErrorCode.E502: "埋点数据存储失败",
        ErrorCode.E503: "埋点数据查询失败",

        # 回放相关错误
        ErrorCode.E600: "回放系统初始化失败",
        ErrorCode.E601: "回放数据加载失败",
        ErrorCode.E602: "回放数据解析失败",
        ErrorCode.E603: "回放数据保存失败",

        # 成功状态
        ErrorCode.SUCCESS: "操作成功",
        ErrorCode.PENDING: "操作进行中",
    }

    @classmethod
    def get_message(cls, error_code: ErrorCode) -> str:
        """
        获取错误码对应的消息

        Args:
            error_code: 错误码

        Returns:
            str: 错误消息
        """
        return cls.ERROR_MESSAGES.get(error_code, "未知错误")

    @classmethod
    def get_error_info(cls, error_code: ErrorCode, details: str = "") -> Dict[str, Any]:
        """
        获取完整的错误信息

        Args:
            error_code: 错误码
            details: 详细信息

        Returns:
            Dict[str, Any]: 错误信息字典
        """
        return {
            "code": error_code.value,
            "message": cls.get_message(error_code),
            "details": details,
        }


def create_error_response(error_code: ErrorCode, details: str = "") -> Dict[str, Any]:
    """
    创建错误响应

    Args:
        error_code: 错误码
        details: 详细信息

    Returns:
        Dict[str, Any]: 错误响应字典
    """
    return {
        "success": False,
        "error": ErrorInfo.get_error_info(error_code, details),
    }


def create_success_response(data: Any = None) -> Dict[str, Any]:
    """
    创建成功响应

    Args:
        data: 响应数据

    Returns:
        Dict[str, Any]: 成功响应字典
    """
    response = {
        "success": True,
        "code": ErrorCode.SUCCESS.value,
        "message": ErrorInfo.get_message(ErrorCode.SUCCESS),
    }
    if data is not None:
        response["data"] = data
    return response
























