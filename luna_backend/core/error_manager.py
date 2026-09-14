"""
Luna Badge 错误管理器 (v1.2.0)
统一错误处理和记录
"""

from typing import Optional, Dict, Any
from core.logger import logger
from core.exceptions import LunaException
try:
    from config.error_codes import get_module_name
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from config.error_codes import get_module_name

class ErrorManager:
    """错误管理器"""
    
    @staticmethod
    def handle_error(error_code: int, details: Optional[Dict[str, Any]] = None, exception: Optional[Exception] = None):
        """
        统一错误处理
        
        Args:
            error_code: 错误码
            details: 错误详情
            exception: 异常对象（如果有）
        """
        module = get_module_name(error_code)
        
        error_info = {
            "error_code": error_code,
            "module": module
        }
        if details:
            error_info.update(details)
        
        if exception:
            error_info["exception_type"] = type(exception).__name__
            error_info["exception_message"] = str(exception)
        
        logger.error(
            f"错误码 {error_code}",
            details=error_info,
            module=module
        )
    
    @staticmethod
    def log_warning(message: str, details: Optional[Dict[str, Any]] = None, module: str = "System"):
        """记录警告"""
        logger.warn(message, details=details, module=module)
    
    @staticmethod
    def log_info(message: str, details: Optional[Dict[str, Any]] = None, module: str = "System"):
        """记录信息"""
        logger.info(message, details=details, module=module)

# 全局错误管理器实例
error_manager = ErrorManager()

