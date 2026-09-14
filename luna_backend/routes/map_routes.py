"""
地图路由 (Map Routes) v1.2.0
本地地图/门牌号相关API
"""

from flask import Blueprint, request
from core.response import ok, error
from config.error_codes import ERR
from services.runtime import rt

map_bp = Blueprint("map", __name__)


@map_bp.route('/map/generate', methods=['POST'])
def generate_local_map():
    """
    生成/更新本地地图
    
    请求体:
    {
        "dx": 0.5,  # X方向移动距离（米）
        "dy": 0.3,  # Y方向移动距离（米）
        "angle_delta": 0.1  # 角度变化（弧度）
    }
    """
    if rt.local_map_service is None:
        return error(ERR.NAV_NOT_READY, "本地地图服务未初始化", http_status=500)
    
    try:
        data = request.get_json() or {}
        dx = float(data.get('dx', 0.0))
        dy = float(data.get('dy', 0.0))
        angle_delta = float(data.get('angle_delta', 0.0))
        
        rt.local_map_service.update_pose(dx, dy, angle_delta)
        
        # 可选：携带图片 + 设施检测器 → 添加地标
        if 'image' in request.files and rt.facility_detector:
            try:
                file = request.files['image']
                # TODO: 实现image_to_numpy函数
                # from utils.image import image_to_numpy
                # image_np = image_to_numpy(file.read())
                # if image_np is not None:
                #     facilities = rt.facility_detector.detect_facility(image_np)
                #     for f in facilities:
                #         rt.local_map_service.add_landmark(
                #             f.type.value, (0, 0), f.label, f.confidence
                #         )
                pass
            except Exception as e:
                # 地标添加失败不影响地图更新
                pass
        
        return ok({'map': rt.local_map_service.to_dict()})
    
    except Exception as e:
        from utils.logger import logger
        logger.error(f"本地地图生成错误: {e}")
        return error(ERR.NAV_ENGINE_ERROR, f"本地地图生成失败: {str(e)}", http_status=500)


@map_bp.route('/map/reset', methods=['POST'])
def reset_local_map():
    """重置本地地图"""
    if rt.local_map_service is None:
        return error(ERR.NAV_NOT_READY, "本地地图服务未初始化", http_status=500)
    
    try:
        rt.local_map_service.reset()
        return ok({'message': '本地地图已重置'})
    except Exception as e:
        return error(ERR.NAV_ENGINE_ERROR, f"重置失败: {str(e)}", http_status=500)


@map_bp.route('/map/status', methods=['GET'])
def get_map_status():
    """获取本地地图状态"""
    if rt.local_map_service is None:
        return error(ERR.NAV_NOT_READY, "本地地图服务未初始化", http_status=500)
    
    try:
        return ok({
            'map': rt.local_map_service.to_dict(),
            'landmark_count': len(rt.local_map_service.get_landmarks())
        })
    except Exception as e:
        return error(ERR.NAV_ENGINE_ERROR, f"获取状态失败: {str(e)}", http_status=500)



