"""
导航路由 v2.0 (v1.2.0)
使用新的错误码规范和ResponseBuilder
"""

from flask import Blueprint, request
from config.error_codes_v2 import ErrorCode
from core.response_builder import ResponseBuilder

navigation_bp = Blueprint("navigation", __name__, url_prefix="/api/navigation")

# 这些实例从app.py里注入或全局引入
# 你可以按自己工程实际调整
navigation_manager = None
path_planner = None


def _get_nav_manager():
    """获取导航管理器实例"""
    global navigation_manager
    if navigation_manager:
        return navigation_manager
    
    # 尝试从current_app获取
    try:
        from flask import current_app
        return getattr(current_app, "navigation_manager", None)
    except:
        pass
    
    # 尝试从core.runtime获取
    try:
        from core.runtime import navigation_manager as runtime_nav
        return runtime_nav
    except:
        return None


def _get_path_planner():
    """获取路径规划器实例"""
    global path_planner
    if path_planner:
        return path_planner
    
    # 尝试从current_app获取
    try:
        from flask import current_app
        return getattr(current_app, "path_planner", None)
    except:
        pass
    
    # 尝试从core.runtime获取
    try:
        from core.runtime import path_planner as runtime_planner
        return runtime_planner
    except:
        return None


@navigation_bp.route("/plan", methods=["POST"])
def plan_route():
    """路径规划API"""
    rb = ResponseBuilder()
    planner = _get_path_planner()
    
    if planner is None:
        return rb.error(ErrorCode.NAV.PLANNER_NOT_INITIALIZED, status_code=500)
    
    data = request.get_json(force=True, silent=True) or {}
    start = data.get("start")
    destinations = data.get("destinations")
    
    if not start or not destinations:
        return rb.error(
            ErrorCode.COMMON.INVALID_PARAM,
            details={"missing": ["start", "destinations"]},
            status_code=400
        )
    
    if not isinstance(destinations, list):
        destinations = [destinations]
    
    try:
        result = planner.plan_route(start, destinations)
        return rb.success({"route": result})
    except Exception as e:
        return rb.error(
            ErrorCode.COMMON.INTERNAL,
            details={"exception": str(e)},
            status_code=500,
        )


@navigation_bp.route("/start", methods=["POST"])
def start_navigation():
    """开始导航"""
    rb = ResponseBuilder()
    nav_manager = _get_nav_manager()
    
    if nav_manager is None:
        return rb.error(ErrorCode.NAV.MANAGER_NOT_INITIALIZED, status_code=500)
    
    data = request.get_json(force=True, silent=True) or {}
    destination = data.get("destination")
    route_segments = data.get("route_segments")
    
    if not destination:
        return rb.error(ErrorCode.NAV.DESTINATION_MISSING, status_code=400)
    
    ok = nav_manager.start_navigation(destination, route_segments)
    
    if not ok:
        return rb.error(ErrorCode.NAV.START_FAILED, status_code=400)
    
    return rb.success({"status": nav_manager.get_status()})


@navigation_bp.route("/status", methods=["GET"])
def navigation_status():
    """获取导航状态"""
    rb = ResponseBuilder()
    nav_manager = _get_nav_manager()
    
    if nav_manager is None:
        return rb.error(ErrorCode.NAV.MANAGER_NOT_INITIALIZED, status_code=500)
    
    status = nav_manager.get_status()
    is_idle = nav_manager.check_idle()
    
    return rb.success({"status": status, "is_idle": is_idle})


@navigation_bp.route("/pause", methods=["POST"])
def pause_navigation():
    """暂停导航"""
    rb = ResponseBuilder()
    nav_manager = _get_nav_manager()
    
    if nav_manager is None:
        return rb.error(ErrorCode.NAV.MANAGER_NOT_INITIALIZED, status_code=500)
    
    data = request.get_json(force=True, silent=True) or {}
    reason = data.get("reason", "用户暂停")
    
    if not nav_manager.pause_navigation(reason):
        return rb.error(
            ErrorCode.NAV.STATE_INVALID,
            details={"state": nav_manager.get_status()["state"]},
            status_code=400
        )
    
    return rb.success({"status": nav_manager.get_status()})


@navigation_bp.route("/resume", methods=["POST"])
def resume_navigation():
    """恢复导航"""
    rb = ResponseBuilder()
    nav_manager = _get_nav_manager()
    
    if nav_manager is None:
        return rb.error(ErrorCode.NAV.MANAGER_NOT_INITIALIZED, status_code=500)
    
    if not nav_manager.resume_navigation():
        return rb.error(
            ErrorCode.NAV.STATE_INVALID,
            details={"state": nav_manager.get_status()["state"]},
            status_code=400
        )
    
    return rb.success({"status": nav_manager.get_status()})


@navigation_bp.route("/cancel", methods=["POST"])
def cancel_navigation():
    """取消导航"""
    rb = ResponseBuilder()
    nav_manager = _get_nav_manager()
    
    if nav_manager is None:
        return rb.error(ErrorCode.NAV.MANAGER_NOT_INITIALIZED, status_code=500)
    
    data = request.get_json(force=True, silent=True) or {}
    reason = data.get("reason", "用户取消")
    
    if not nav_manager.cancel_navigation(reason):
        return rb.error(
            ErrorCode.NAV.STATE_INVALID,
            details={"state": nav_manager.get_status()["state"]},
            status_code=400
        )
    
    return rb.success({"status": nav_manager.get_status()})


@navigation_bp.route("/complete", methods=["POST"])
def complete_navigation():
    """完成导航"""
    rb = ResponseBuilder()
    nav_manager = _get_nav_manager()
    
    if nav_manager is None:
        return rb.error(ErrorCode.NAV.MANAGER_NOT_INITIALIZED, status_code=500)
    
    if not nav_manager.complete_navigation():
        return rb.error(
            ErrorCode.NAV.STATE_INVALID,
            details={"state": nav_manager.get_status()["state"]},
            status_code=400
        )
    
    return rb.success({"status": nav_manager.get_status()})


@navigation_bp.route("/update_environment", methods=["POST"])
def update_environment():
    """
    更新导航环境（核心接口）
    接收GPS、视觉、危险等信息，返回nav_action
    """
    rb = ResponseBuilder()
    nav_manager = _get_nav_manager()
    
    if nav_manager is None:
        return rb.error(ErrorCode.NAV.MANAGER_NOT_INITIALIZED, status_code=500)
    
    data = request.get_json(force=True, silent=True) or {}
    
    # 组装环境信息
    env = {
        "gps": data.get("gps", {}),
        "vision": data.get("vision", {}),
        "hazards": data.get("hazards", []),
        "navigation_raw": data.get("navigation_raw", {}),
    }
    
    try:
        result = nav_manager.update_from_environment(env)
        return jsonify(result), 200
    except Exception as e:
        return rb.error(
            ErrorCode.NAV.UPDATE_ENV_INVALID,
            details={"exception": str(e)},
            status_code=500
        )



