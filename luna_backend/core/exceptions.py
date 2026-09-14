"""
Luna Badge 统一异常体系 (v1.2.0)
"""

from typing import Optional, Dict, Any
try:
    from config.error_codes import get_error_message, get_module_name
except ImportError:
    # 如果作为独立模块运行时
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from config.error_codes import get_error_message, get_module_name

class LunaException(Exception):
    """Luna 基础异常类"""
    
    def __init__(self, error_code: int, message: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        self.error_code = error_code
        self.message = message or get_error_message(error_code)
        self.details = details or {}
        self.module = get_module_name(error_code)
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "error_code": self.error_code,
            "error_message": self.message,
            "module": self.module,
            "details": self.details
        }

class TTSException(LunaException):
    """TTS 模块异常"""
    pass

class VisionException(LunaException):
    """视觉模块异常"""
    pass

class NavigationException(LunaException):
    """导航模块异常"""
    pass

class SceneException(LunaException):
    """场景记忆模块异常"""
    pass

class PathException(LunaException):
    """路径规划模块异常"""
    pass

class SystemException(LunaException):
    """系统模块异常"""
    pass

