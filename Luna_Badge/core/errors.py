# core/errors.py

from typing import Any, Dict, Optional
from .error_codes import get_error_info, ErrorInfo


class LunaError(Exception):
    """统一的 Luna Badge 异常类型，携带错误码与上下文。"""

    def __init__(self, code: str, details: Optional[Dict[str, Any]] = None):
        self.code = code
        self.info: Optional[ErrorInfo] = get_error_info(code)
        self.details = details or {}

        message = self.info.message if self.info else "Unknown error"
        super().__init__(f"[{code}] {message}")


def make_error_response(code: str, details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    info = get_error_info(code)
    return {
        "success": False,
        "code": code,
        "message": info.message if info else "Unknown error",
        "category": info.category if info else "unknown",
        "suggestion": info.suggestion if info else "",
        "details": details or {},
    }


def make_success_response(data: Any = None, message: str = "OK") -> Dict[str, Any]:
    return {
        "success": True,
        "code": 0,
        "message": message,
        "data": data,
    }



