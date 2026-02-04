"""
Luna Badge 统一日志系统 (v1.2.0)
日志格式: [LUNA][模块名][LEVEL] message { details }
增强版：支持文件路径、函数名、行号定位
"""

import logging
import sys
import inspect
from typing import Optional, Dict, Any
from config.error_codes import get_module_name

class LunaLogger:
    """Luna 统一日志记录器"""
    
    def __init__(self, name: str = "LUNA"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # 避免重复添加handler
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter(
                '[LUNA][%(name)s][%(levelname)s] %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def _get_caller_info(self, skip_frames: int = 2) -> Dict[str, str]:
        """获取调用者信息（文件路径、函数名、行号）"""
        try:
            frame = inspect.currentframe()
            for _ in range(skip_frames):
                frame = frame.f_back
                if frame is None:
                    break
            
            if frame:
                filename = frame.f_code.co_filename
                function = frame.f_code.co_name
                line_no = frame.f_lineno
                
                # 提取相对路径（相对于项目根目录）
                import os
                project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                if filename.startswith(project_root):
                    rel_path = os.path.relpath(filename, project_root)
                else:
                    rel_path = filename
                
                return {
                    "file": rel_path,
                    "function": function,
                    "line": str(line_no)
                }
        except:
            pass
        return {}
    
    def _format_message(self, message: str, details: Optional[Dict[str, Any]] = None, include_location: bool = True) -> str:
        """格式化日志消息"""
        if details is None:
            details = {}
        
        # 自动添加调用位置信息
        if include_location:
            caller_info = self._get_caller_info()
            details.update(caller_info)
        
        if details:
            import json
            details_str = json.dumps(details, ensure_ascii=False)
            return f"{message} {{ {details_str} }}"
        return message
    
    def info(self, message: str, details: Optional[Dict[str, Any]] = None, module: str = "System", include_location: bool = True):
        """信息日志"""
        formatted = self._format_message(message, details, include_location)
        self.logger.info(f"[{module}] {formatted}")
    
    def warn(self, message: str, details: Optional[Dict[str, Any]] = None, module: str = "System", include_location: bool = True):
        """警告日志"""
        formatted = self._format_message(message, details, include_location)
        self.logger.warning(f"[{module}] {formatted}")
    
    def error(self, message: str, details: Optional[Dict[str, Any]] = None, module: str = "System", include_location: bool = True):
        """错误日志"""
        formatted = self._format_message(message, details, include_location)
        self.logger.error(f"[{module}] {formatted}")
    
    def debug(self, message: str, details: Optional[Dict[str, Any]] = None, module: str = "System", include_location: bool = True):
        """调试日志"""
        formatted = self._format_message(message, details, include_location)
        self.logger.debug(f"[{module}] {formatted}")

def log_error(logger: LunaLogger, code: int, msg: str, extra: Optional[Dict[str, Any]] = None):
    """
    统一错误日志记录（带错误码和位置信息）
    
    Args:
        logger: 日志记录器实例
        code: 错误码
        msg: 错误消息
        extra: 额外信息
    """
    module = get_module_name(code)
    details = extra or {}
    details["error_code"] = code
    
    # 获取调用位置
    import inspect
    frame = inspect.currentframe()
    if frame and frame.f_back:
        caller_frame = frame.f_back
        filename = caller_frame.f_code.co_filename
        function = caller_frame.f_code.co_name
        line_no = caller_frame.f_lineno
        
        import os
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if filename.startswith(project_root):
            rel_path = os.path.relpath(filename, project_root)
        else:
            rel_path = filename
        
        details["file"] = rel_path
        details["function"] = function
        details["line"] = line_no
    
    logger.error(f"[ERR-{code}] {msg}", details=details, module=module, include_location=False)

# 全局日志实例
logger = LunaLogger()

def init_logger(name: str = "LUNA") -> LunaLogger:
    """初始化日志记录器"""
    return LunaLogger(name)
