"""
日志服务模块 (v1.2.0)
导出错误上报器
"""

from .error_reporter import ErrorReporter, report_error

__all__ = ['ErrorReporter', 'report_error']



