"""
健康检查和系统状态路由 (v1.2.0)
包含: /api/health, /api/system/status 等
"""

from flask import Blueprint
from core.response import api_success, api_error
from config.error_codes import ERR

health_bp = Blueprint("health", __name__)


@health_bp.route("/api/health", methods=["GET"])
def health_check():
    """健康检查"""
    return api_success({
        "status": "healthy",
        "version": "1.2.0"
    })


@health_bp.route("/api/system/status", methods=["GET"])
def system_status():
    """系统状态"""
    try:
        from flask import current_app
        
        # 检查各个模块是否初始化
        modules_status = {
            "vision_engine": current_app.extensions.get("vision_engine") is not None,
            "navigation_manager": current_app.extensions.get("navigation_manager") is not None,
            "tts_manager": current_app.extensions.get("tts_manager") is not None,
            "log_manager": current_app.extensions.get("log_manager") is not None,
        }
        
        return api_success({
            "modules": modules_status,
            "status": "running"
        })
    except Exception as e:
        return api_error(ERR.UNKNOWN_ERROR, {"exception": str(e)}, http_status=500)



