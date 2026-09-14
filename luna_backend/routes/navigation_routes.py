"""
后端导航 API 专用 (v1.2.0)
把 web_test_server 里的所有 /api/navigation/* 路由独立出来
统一使用 core.response + config.error_codes
"""

from flask import Blueprint, request, current_app
from core.response import ok, error
from core.logger import logger, log_error
from config.error_codes import ERR


navigation_bp = Blueprint("navigation", __name__, url_prefix="/api/navigation")


def _get_nav_manager():
    """
    获取导航管理器实例
    
    Returns:
        导航管理器实例，如果不存在则返回None
    """
    # 优先从current_app获取
    nav_manager = getattr(current_app, "navigation_manager", None)
    if nav_manager:
        return nav_manager
    
    # 尝试从全局获取（向后兼容）
    try:
        from core.runtime import navigation_manager
        return navigation_manager
    except:
        return None


@navigation_bp.route("/plan", methods=["POST"])
def plan_route():
    """路径规划API"""
    nav_manager = _get_nav_manager()
    
    if nav_manager is None or nav_manager.path_planner is None:
        return error(
            ERR.NAV_NOT_READY,
            "路径规划器未初始化",
            http_status=500
        )
    
    data = request.get_json() or {}
    start = data.get("start", "")
    destinations = data.get("destinations", [])
    
    if not start or not destinations:
        return error(
            ERR.NAV_INVALID_INPUT,
            "缺少起点或目的地参数",
            http_status=400
        )
    
    if not isinstance(destinations, list):
        destinations = [destinations]
    
    try:
        result = nav_manager.plan_route(start, destinations)
        return ok({"route": result})
    except RuntimeError as e:
        log_error(logger, ERR.NAV_NOT_READY, "路径规划器未初始化", {"exception": str(e)})
        return error(
            ERR.NAV_NOT_READY,
            str(e),
            http_status=500
        )
    except Exception as e:
        log_error(logger, ERR.NAV_ROUTE_ERROR, "路径规划失败", {"exception": str(e)})
        return error(
            ERR.NAV_ROUTE_ERROR,
            f"路径规划失败: {str(e)}",
            http_status=500
        )


@navigation_bp.route("/start", methods=["POST"])
def start_navigation():
    """开始导航"""
    nav_manager = _get_nav_manager()
    
    if nav_manager is None:
        return error(
            ERR.NAV_NOT_READY,
            "导航管理器未初始化",
            http_status=500
        )
    
    data = request.get_json() or {}
    destination = data.get("destination", "")
    route_segments = data.get("route_segments")
    
    if not destination:
        return error(
            ERR.NAV_INVALID_INPUT,
            "缺少目的地参数",
            http_status=400
        )
    
    try:
        success = nav_manager.start_navigation(destination, route_segments)
        
        if success:
            status = nav_manager.get_status()
            return ok({"status": status})
        else:
            return error(
                ERR.NAV_ENGINE_ERROR,
                "导航启动失败，可能已有导航在进行中",
                http_status=400
            )
    except RuntimeError as e:
        log_error(logger, ERR.NAV_NOT_READY, "导航启动失败", {"exception": str(e)})
        return error(
            ERR.NAV_NOT_READY,
            str(e),
            http_status=500
        )
    except Exception as e:
        log_error(logger, ERR.NAV_ENGINE_ERROR, "导航启动异常", {"exception": str(e)})
        return error(
            ERR.NAV_ENGINE_ERROR,
            f"导航启动异常: {str(e)}",
            http_status=500
        )


@navigation_bp.route("/update_position", methods=["POST"])
def update_position():
    """更新位置（支持障碍检测结果透传）"""
    nav_manager = _get_nav_manager()
    
    if nav_manager is None:
        return error(
            ERR.NAV_NOT_READY,
            "导航管理器未初始化",
            http_status=500
        )
    
    data = request.get_json() or {}
    lat = data.get("lat")
    lng = data.get("lng")
    hazards = data.get("detected_hazards")  # 这里允许前端直接传识别结果
    
    if lat is None or lng is None:
        return error(
            ERR.NAV_INVALID_INPUT,
            "缺少位置参数 lat/lng",
            http_status=400
        )
    
    try:
        nav_manager.update_position(lat, lng, hazards)
        status = nav_manager.get_status()
        is_idle = nav_manager.is_idle()
        
        return ok({
            "status": status,
            "is_idle": is_idle,
            "detected_hazards": hazards or [],
        })
    except Exception as e:
        log_error(logger, ERR.NAV_ENGINE_ERROR, "更新位置异常", {"exception": str(e)})
        return error(
            ERR.NAV_ENGINE_ERROR,
            f"更新位置异常: {str(e)}",
            http_status=500
        )


@navigation_bp.route("/status", methods=["GET"])
def get_navigation_status():
    """获取导航状态"""
    nav_manager = _get_nav_manager()
    
    if nav_manager is None:
        return error(
            ERR.NAV_NOT_READY,
            "导航管理器未初始化",
            http_status=500
        )
    
    try:
        status = nav_manager.get_status()
        is_idle = nav_manager.is_idle()
        
        return ok({
            "status": status,
            "is_idle": is_idle
        })
    except Exception as e:
        log_error(logger, ERR.NAV_ENGINE_ERROR, "获取导航状态异常", {"exception": str(e)})
        return error(
            ERR.NAV_ENGINE_ERROR,
            f"获取导航状态异常: {str(e)}",
            http_status=500
        )


@navigation_bp.route("/pause", methods=["POST"])
def pause_navigation():
    """暂停导航"""
    nav_manager = _get_nav_manager()
    
    if nav_manager is None:
        return error(
            ERR.NAV_NOT_READY,
            "导航管理器未初始化",
            http_status=500
        )
    
    data = request.get_json() or {}
    reason = data.get("reason", "用户暂停")
    
    try:
        success = nav_manager.pause(reason)
        
        if success:
            status = nav_manager.get_status()
            return ok({"status": status})
        else:
            return error(
                ERR.NAV_ENGINE_ERROR,
                "暂停失败，当前不是导航中状态",
                http_status=400
            )
    except Exception as e:
        log_error(logger, ERR.NAV_ENGINE_ERROR, "暂停导航异常", {"exception": str(e)})
        return error(
            ERR.NAV_ENGINE_ERROR,
            f"暂停导航异常: {str(e)}",
            http_status=500
        )


@navigation_bp.route("/resume", methods=["POST"])
def resume_navigation():
    """恢复导航"""
    nav_manager = _get_nav_manager()
    
    if nav_manager is None:
        return error(
            ERR.NAV_NOT_READY,
            "导航管理器未初始化",
            http_status=500
        )
    
    try:
        success = nav_manager.resume()
        
        if success:
            status = nav_manager.get_status()
            return ok({"status": status})
        else:
            return error(
                ERR.NAV_ENGINE_ERROR,
                "恢复失败，当前不是暂停状态",
                http_status=400
            )
    except Exception as e:
        log_error(logger, ERR.NAV_ENGINE_ERROR, "恢复导航异常", {"exception": str(e)})
        return error(
            ERR.NAV_ENGINE_ERROR,
            f"恢复导航异常: {str(e)}",
            http_status=500
        )


@navigation_bp.route("/cancel", methods=["POST"])
def cancel_navigation():
    """取消导航"""
    nav_manager = _get_nav_manager()
    
    if nav_manager is None:
        return error(
            ERR.NAV_NOT_READY,
            "导航管理器未初始化",
            http_status=500
        )
    
    data = request.get_json() or {}
    reason = data.get("reason", "用户取消")
    
    try:
        success = nav_manager.cancel(reason)
        
        if success:
            status = nav_manager.get_status()
            return ok({"status": status})
        else:
            return error(
                ERR.NAV_ENGINE_ERROR,
                "取消失败，当前不在导航流程中",
                http_status=400
            )
    except Exception as e:
        log_error(logger, ERR.NAV_ENGINE_ERROR, "取消导航异常", {"exception": str(e)})
        return error(
            ERR.NAV_ENGINE_ERROR,
            f"取消导航异常: {str(e)}",
            http_status=500
        )


@navigation_bp.route("/complete", methods=["POST"])
def complete_navigation():
    """完成导航"""
    nav_manager = _get_nav_manager()
    
    if nav_manager is None:
        return error(
            ERR.NAV_NOT_READY,
            "导航管理器未初始化",
            http_status=500
        )
    
    try:
        success = nav_manager.complete()
        
        if success:
            status = nav_manager.get_status()
            return ok({"status": status})
        else:
            return error(
                ERR.NAV_ENGINE_ERROR,
                "完成失败，当前不在导航流程中",
                http_status=400
            )
    except Exception as e:
        log_error(logger, ERR.NAV_ENGINE_ERROR, "完成导航异常", {"exception": str(e)})
        return error(
            ERR.NAV_ENGINE_ERROR,
            f"完成导航异常: {str(e)}",
            http_status=500
        )


# ==================== 向后兼容的路由 ====================

@navigation_bp.route("/api/navigation/plan", methods=["POST"])
def plan_route_legacy():
    """路径规划API（向后兼容）"""
    return plan_route()


@navigation_bp.route("/api/navigation/start", methods=["POST"])
def start_navigation_legacy():
    """开始导航（向后兼容）"""
    return start_navigation()


@navigation_bp.route("/api/navigation/update_position", methods=["POST"])
def update_position_legacy():
    """更新位置（向后兼容）"""
    return update_position()


@navigation_bp.route("/api/navigation/status", methods=["GET"])
def get_navigation_status_legacy():
    """获取导航状态（向后兼容）"""
    return get_navigation_status()
