# backend/api_gateway.py

from flask import Blueprint, request, jsonify
from typing import Any, Dict
from core.errors import LunaError, make_error_response, make_success_response

api_v1 = Blueprint("api_v1", __name__, url_prefix="/api/v1")


def _wrap_handler(handler):
    """统一错误包装器，用于所有 API 处理函数。"""
    def wrapper(*args, **kwargs):
        try:
            result = handler(*args, **kwargs)
            # 处理函数可以直接返回 dict / (dict, status)
            if isinstance(result, tuple):
                body, status = result
                return jsonify(body), status
            return jsonify(make_success_response(result)), 200
        except LunaError as e:
            return jsonify(make_error_response(e.code, e.details)), 400
        except Exception as e:
            # 兜底：系统未知错误
            return jsonify(make_error_response("SYS-0002", {"exception": str(e)})), 500
    wrapper.__name__ = handler.__name__
    return wrapper


# ========== 系统类 API ==========

@api_v1.route("/system/status", methods=["GET"])
@_wrap_handler
def system_status() -> Dict[str, Any]:
    # 简单示例：后续可读取真实 orchestrator 状态
    import time
    try:
        # 尝试获取系统编排器状态
        from core.system_orchestrator import SystemOrchestrator
        # 这里假设有一个全局实例或单例
        # 实际使用时需要根据项目结构调整
        uptime_sec = 0  # TODO: 接入真实数据
    except:
        uptime_sec = 0
    
    return {
        "status": "running",
        "version": "1.0.0",
        "uptime_sec": uptime_sec,
    }


@api_v1.route("/system/reboot", methods=["POST"])
@_wrap_handler
def system_reboot() -> Dict[str, Any]:
    # TODO: 接入真实重启逻辑（例如标记 flag 让 watchdog 执行重启）
    # 这里只返回 "accepted"
    return {"reboot": "accepted", "message": "Reboot request accepted, watchdog will handle restart"}


# ========== 配置类 API ==========

try:
    from core.unified_config_manager import (
        get_all_runtime_params,
        update_runtime_params,
    )
except ImportError:
    # 如果导入失败，提供stub函数
    def get_all_runtime_params():
        return {}
    
    def update_runtime_params(updates):
        return {}


@api_v1.route("/config/get", methods=["GET"])
@_wrap_handler
def config_get() -> Dict[str, Any]:
    """获取可调参数的当前值。"""
    return get_all_runtime_params()


@api_v1.route("/config/set", methods=["POST"])
@_wrap_handler
def config_set() -> Dict[str, Any]:
    """
    更新部分参数：
    body = { "navigation.max_deviation": 1.5, "vision.yolo_conf": 0.65 }
    """
    payload = request.get_json(silent=True) or {}
    if not isinstance(payload, dict):
        raise LunaError("API-8001", {"reason": "Payload must be JSON object"})

    updated = update_runtime_params(payload)
    return {"updated": updated}


# ========== 日志上传 API ==========

@api_v1.route("/log/client", methods=["POST"])
@_wrap_handler
def log_client() -> Dict[str, Any]:
    """
    前端日志上传入口，用于：
    - 任务链日志
    - 导航事件
    - 视觉事件
    - 错误码
    """
    payload = request.get_json(silent=True) or {}
    
    try:
        from core.log_manager import log_client_event
        log_client_event(payload)
    except ImportError:
        # 如果log_manager不存在，简单记录到文件
        import json
        import os
        from datetime import datetime
        
        log_dir = "logs/web_test"
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, "client_events.jsonl")
        with open(log_file, "a", encoding="utf-8") as f:
            entry = {
                "ts": datetime.now().isoformat(),
                **payload
            }
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    
    return {"stored": True}



