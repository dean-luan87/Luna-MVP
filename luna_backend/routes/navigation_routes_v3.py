"""
导航路由 v3.0 (v1.2.0)
真正调用策略执行导航动作（API层）
"""

from flask import Blueprint, request
from core.response import ok, error
from config.error_codes import ERR

# 导入新的NavigationManager（策略引擎集成版）
try:
    from services.navigation.navigation_manager_v3 import NavigationManager
except ImportError:
    # 如果导入失败，尝试从旧版本导入
    try:
        from navigation_core.navigation_manager import NavigationManager
    except ImportError:
        NavigationManager = None

nav_bp = Blueprint("navigation", __name__, url_prefix="/nav")

# 单例导航管理器（可在任务链中保持状态）
nav_manager = None

def _get_nav_manager():
    """获取导航管理器实例"""
    global nav_manager
    if nav_manager is None:
        if NavigationManager is None:
            return None
        nav_manager = NavigationManager()
    return nav_manager


@nav_bp.route("/update", methods=["POST"])
def nav_update():
    """
    更新导航观察数据
    
    请求体示例:
    {
        "position": {"lat": 31.23, "lng": 121.47},
        "heading": 90.0,
        "hazards": [...],
        "construction": false,
        "people_density": 0.3,
        "traffic_light_state": "GREEN",
        "vision": {...},
        "navigation_raw": {...}
    }
    """
    nav_mgr = _get_nav_manager()
    
    if nav_mgr is None:
        return error(ERR.NAV_NOT_INITIALIZED, "导航管理器未初始化", http_status=500)
    
    data = request.get_json() or {}
    
    try:
        nav_mgr.update_observation(data)
        return ok({
            "message": "导航状态已更新",
            "context": nav_mgr.context.to_dict()
        })
    except Exception as e:
        return error(ERR.NAV_UPDATE_FAILED, f"更新导航状态失败: {str(e)}", http_status=500)


@nav_bp.route("/run", methods=["GET"])
def nav_run():
    """
    执行一次策略调度，获取导航动作
    
    每次调用由前端JS定时器触发（比如500ms）
    获取一次策略执行结果
    
    返回示例:
    {
        "success": true,
        "data": {
            "success": true,
            "action": "REROUTE",
            "text": "前方道路施工，我已为您规划绕行路线。",
            "strategy": "CONSTRUCTION_BYPASS"
        }
    }
    """
    nav_mgr = _get_nav_manager()
    
    if nav_mgr is None:
        return error(ERR.NAV_NOT_INITIALIZED, "导航管理器未初始化", http_status=500)
    
    try:
        result = nav_mgr.run_step()
        return ok(result)
    except Exception as e:
        return error(ERR.NAV_ENGINE_ERROR, f"策略执行失败: {str(e)}", http_status=500)


@nav_bp.route("/status", methods=["GET"])
def nav_status():
    """
    获取导航状态
    
    返回当前导航上下文和执行状态
    """
    nav_mgr = _get_nav_manager()
    
    if nav_mgr is None:
        return error(ERR.NAV_NOT_INITIALIZED, "导航管理器未初始化", http_status=500)
    
    try:
        status = nav_mgr.get_status()
        return ok(status)
    except Exception as e:
        return error(ERR.NAV_ENGINE_ERROR, f"获取状态失败: {str(e)}", http_status=500)


@nav_bp.route("/reset", methods=["POST"])
def nav_reset():
    """
    重置导航管理器
    
    清空上下文和策略状态
    """
    nav_mgr = _get_nav_manager()
    
    if nav_mgr is None:
        return error(ERR.NAV_NOT_INITIALIZED, "导航管理器未初始化", http_status=500)
    
    try:
        nav_mgr.reset()
        return ok({"message": "导航管理器已重置"})
    except Exception as e:
        return error(ERR.NAV_ENGINE_ERROR, f"重置失败: {str(e)}", http_status=500)


# ==================== 向后兼容的路由 ====================

@nav_bp.route("/api/navigation/update", methods=["POST"])
def nav_update_legacy():
    """向后兼容的路由"""
    return nav_update()


@nav_bp.route("/api/navigation/run", methods=["GET"])
def nav_run_legacy():
    """向后兼容的路由"""
    return nav_run()


@nav_bp.route("/api/navigation/status", methods=["GET"])
def nav_status_legacy():
    """向后兼容的路由"""
    return nav_status()



