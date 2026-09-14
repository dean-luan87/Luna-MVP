"""
Luna Backend 配置模块
"""

from .settings import settings
from .constants import *
# 从error_codes导入（兼容新旧版本）
try:
    from .error_codes import ERROR_CODES, get_error_message, get_module_name
except ImportError:
    # 如果新版本没有ERROR_CODES，使用ERR类
    from .error_codes import ERR, ERROR_MESSAGES
    
    # 创建兼容函数
    def get_error_message(code):
        """获取错误消息（兼容函数）"""
        if isinstance(code, int):
            return ERROR_MESSAGES.get(code, "未知错误")
        return str(code)
    
    def get_module_name(code):
        """获取模块名称（兼容函数）"""
        if isinstance(code, int):
            code_str = str(code)
            if code_str.startswith('1'):
                return '通用'
            elif code_str.startswith('2'):
                return '视觉'
            elif code_str.startswith('3'):
                return '音频'
            elif code_str.startswith('4'):
                return '导航'
            elif code_str.startswith('5'):
                return 'TTS'
            elif code_str.startswith('6'):
                return '场景记忆'
        return '未知'
    
    # 创建兼容的ERROR_CODES字典
    ERROR_CODES = {getattr(ERR, attr): ERROR_MESSAGES.get(getattr(ERR, attr), "未知错误") 
                   for attr in dir(ERR) if not attr.startswith('_') and isinstance(getattr(ERR, attr), int)}

__all__ = [
    'settings',
    'ERROR_CODES',
    'get_error_message',
    'get_module_name',
]

