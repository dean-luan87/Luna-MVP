"""
错误上报器 (ErrorReporter) v1.2.0
将错误码和详细信息上报到后台，实现精准定位问题
"""

import requests
import logging
from typing import Dict, Any, Optional
import json

logger = logging.getLogger(__name__)

# 延迟导入以避免循环依赖
def _get_logger():
    try:
        from luna_backend.utils.logger import system_log
        return system_log
    except ImportError:
        try:
            from utils.logger import system_log
            return system_log
        except ImportError:
            def _dummy_log(tag, extra):
                pass
            return _dummy_log


class ErrorReporter:
    """
    错误上报器
    
    将错误码和详细信息上报到后台服务器
    支持异步上报，不阻塞主流程
    """
    
    # 后台错误上报端点（可配置）
    ENDPOINT = "https://your-backend.com/api/logs/errors"
    
    # 是否启用上报（可通过环境变量控制）
    ENABLED = True
    
    # 超时时间（秒）
    TIMEOUT = 1.2
    
    @classmethod
    def report(cls, error_code, detail: Dict[str, Any], module: Optional[str] = None):
        """
        上报错误
        
        Args:
            error_code: 错误码（可以是int或str）
            detail: 错误详情字典
            module: 模块名称（可选）
        """
        if not cls.ENABLED:
            return
        
        system_log = _get_logger()
        
        # 构建上报负载
        payload = {
            "error_code": str(error_code),
            "module": module or cls._get_module_from_code(error_code),
            "detail": detail,
            "timestamp": cls._get_timestamp(),
        }
        
        # 记录本地日志
        logger.error(f"[{error_code}] {detail.get('message', '')} meta={detail}")
        system_log("ERR_REPORT", payload)
        
        # 尝试通过log_manager记录
        try:
            from services.runtime import rt
            if rt.log_manager and hasattr(rt.log_manager, 'log_system_event'):
                rt.log_manager.log_system_event(
                    event=f"ERROR:{error_code}",
                    metadata={"message": detail.get("message", ""), "meta": detail}
                )
        except Exception as e:
            logger.exception("log_manager.log_system_event failed")
        
        # 异步上报（不阻塞主流程）
        try:
            import threading
            thread = threading.Thread(target=cls._send_report, args=(payload,))
            thread.daemon = True
            thread.start()
        except Exception as e:
            system_log("ERR_REPORT_THREAD_FAIL", {"error": str(e)})
    
    @classmethod
    def _send_report(cls, payload: Dict[str, Any]):
        """
        发送上报请求（内部方法）
        
        Args:
            payload: 上报负载
        """
        try:
            response = requests.post(
                cls.ENDPOINT,
                json=payload,
                timeout=cls.TIMEOUT,
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 200:
                system_log("ERR_REPORT_SUCCESS", {"error_code": payload.get("error_code")})
            else:
                system_log("ERR_REPORT_FAIL", {
                    "status_code": response.status_code,
                    "error_code": payload.get("error_code")
                })
        except requests.exceptions.Timeout:
            system_log("ERR_REPORT_TIMEOUT", {"error_code": payload.get("error_code")})
        except requests.exceptions.RequestException as e:
            system_log("ERR_REPORT_NETWORK_ERROR", {
                "error": str(e),
                "error_code": payload.get("error_code")
            })
        except Exception as e:
            system_log("ERR_REPORT_UNKNOWN_ERROR", {
                "error": str(e),
                "error_code": payload.get("error_code")
            })
    
    @classmethod
    def _get_module_from_code(cls, error_code) -> str:
        """
        从错误码推断模块名称
        
        Args:
            error_code: 错误码（可以是int或str）
        
        Returns:
            模块名称
        """
        # 如果是字符串错误码（如 "HOSPITAL_FLOW_NOT_INIT"）
        if isinstance(error_code, str):
            if error_code.startswith("NAV_"):
                return "NAVIGATION"
            elif error_code.startswith("VIS_") or error_code.startswith("VISION_"):
                return "VISION"
            elif error_code.startswith("TASK_") or error_code.startswith("HOSPITAL_"):
                return "TASKCHAIN"
            elif error_code.startswith("TTS_"):
                return "TTS"
            else:
                return "UNKNOWN"
        
        # 6位数字格式：MMSSEE
        if error_code >= 400000:
            return "NAVIGATION"
        elif error_code >= 200000:
            return "VISION"
        elif error_code >= 500000:
            return "TASKCHAIN"
        elif error_code >= 300000:
            return "AUDIO"
        elif error_code >= 100000:
            return "COMMON"
        else:
            # 4位数字格式
            if 3000 <= error_code < 4000:
                return "NAVIGATION"
            elif 4000 <= error_code < 5000:
                return "VISION"
            elif 5000 <= error_code < 6000:
                return "TASKCHAIN"
            else:
                return "UNKNOWN"
    
    @classmethod
    def _get_timestamp(cls) -> str:
        """
        获取时间戳
        
        Returns:
            时间戳字符串
        """
        import time
        return str(int(time.time() * 1000))
    
    @classmethod
    def set_endpoint(cls, endpoint: str):
        """
        设置上报端点
        
        Args:
            endpoint: 端点URL
        """
        cls.ENDPOINT = endpoint
    
    @classmethod
    def set_enabled(cls, enabled: bool):
        """
        设置是否启用上报
        
        Args:
            enabled: 是否启用
        """
        cls.ENABLED = enabled


# 便捷函数
def report_error(error_code: int, detail: Dict[str, Any], module: Optional[str] = None):
    """
    上报错误的便捷函数
    
    Args:
        error_code: 错误码
        detail: 错误详情
        module: 模块名称（可选）
    """
    ErrorReporter.report(error_code, detail, module)

