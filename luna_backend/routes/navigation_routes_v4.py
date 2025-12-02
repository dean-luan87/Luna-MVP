"""
导航路由 v4.0 (v1.2.0)
从web_test_server.py拆分导航相关API，使用services.runtime.rt
"""

from flask import Blueprint, request
from core.response import ok, error, api_success, api_error
from config.error_codes import ERR
from services.runtime import rt
import sys
import os

# 添加luna_backend到Python路径（确保可以导入modules）
_backend_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _backend_root not in sys.path:
    sys.path.insert(0, _backend_root)

try:
    from modules.scene_description.description_engine import SceneDescriptionEngine
except ImportError:
    # 如果modules目录不存在，尝试从services导入
    try:
        from services.scene.scene_description_engine import SceneDescriptionEngine
    except ImportError:
        SceneDescriptionEngine = None
from utils.image_utils import decode_base64_image
import logging
import time
import numpy as np
from PIL import Image
import io

logger = logging.getLogger(__name__)

nav_bp = Blueprint("navigation", __name__)

# 初始化场景描述引擎（延迟加载）
_scene_engine = None

def get_scene_engine():
    """获取场景描述引擎实例（延迟初始化）"""
    global _scene_engine
    if _scene_engine is None:
        if SceneDescriptionEngine is None:
            logger.error("SceneDescriptionEngine 模块未找到")
            return None
        _scene_engine = SceneDescriptionEngine()
        logger.info("✅ SceneDescriptionEngine 初始化完成")
    return _scene_engine

def _normalize_objects(detections: list) -> list:
    """
    把 YOLO/vision_engine 的输出整理成 SceneDescriptionEngine 预期结构：
    { label/class, bbox, distance, position }
    """
    normalized = []
    for d in detections or []:
        cls = d.get("class") or d.get("label")
        bbox = d.get("bbox") or _build_bbox_from_xywh(d)
        distance = d.get("distance")  # 如果前面已经算好了就直接用
        position = d.get("position")  # 如果前面已经算好了就直接用

        normalized.append({
            "label": d.get("label") or cls,
            "class": cls,
            "bbox": bbox,
            "distance": distance,
            "position": position,
        })
    return normalized

def _build_bbox_from_xywh(d: dict):
    """兼容你的 YOLO 输出结构"""
    if all(k in d for k in ("x1", "y1", "x2", "y2")):
        return (d["x1"], d["y1"], d["x2"], d["y2"])
    if all(k in d for k in ("x", "y", "w", "h")):
        x1 = d["x"]
        y1 = d["y"]
        return (x1, y1, x1 + d["w"], y1 + d["h"])
    return None

def _image_to_numpy(image_bytes):
    """将图像字节转换为numpy数组"""
    try:
        img = Image.open(io.BytesIO(image_bytes))
        img_np = np.array(img)
        if len(img_np.shape) == 3 and img_np.shape[2] == 4:
            # RGBA转RGB
            img_np = img_np[:, :, :3]
        return img_np
    except Exception as e:
        logger.error(f"[_image_to_numpy] 转换失败: {e}")
        return None


@nav_bp.route('/plan', methods=['POST'])
def plan_route():
    """
    路径规划API
    
    请求体:
    {
        "start": "当前位置",
        "destinations": ["711便利店", "新华医院"]
    }
    """
    try:
        if rt.path_planner is None:
            return error(ERR.NAV_NOT_READY, "路径规划器未初始化", http_status=500)
        
        data = request.get_json() or {}
        start = data.get('start', '')
        destinations = data.get('destinations', [])
        
        if not start or not destinations:
            return error(ERR.NAV_INVALID_INPUT, "缺少起点或目的地参数", http_status=400)
        
        if not isinstance(destinations, list):
            destinations = [destinations]
        
        result = rt.path_planner.plan_route(start, destinations)
        return ok({'route': result})
    
    except Exception as e:
        from utils.logger import logger
        logger.error(f"路径规划错误: {e}")
        return error(ERR.NAV_ROUTE_ERROR, f"路径规划失败: {str(e)}", http_status=500)


@nav_bp.route('/plan_multi', methods=['POST'])
def plan_multi_target():
    """
    多目标路径规划API
    
    请求体:
    {
        "start": "当前位置",
        "targets": [
            {"name": "711便利店", "type": "shop"},
            {"name": "新华医院", "type": "hospital"}
        ]
    }
    """
    try:
        if rt.path_planner is None:
            return error(ERR.NAV_NOT_READY, "路径规划器未初始化", http_status=500)
        
        from services.navigation.multi_target_planner import MultiTargetPlanner
        
        data = request.get_json() or {}
        start = data.get('start', '当前位置')
        targets = data.get('targets', [])
        
        if not targets:
            return error(ERR.NAV_INVALID_INPUT, "缺少目标列表", http_status=400)
        
        planner = MultiTargetPlanner(rt.path_planner)
        result = planner.plan_sequence(start, targets)
        
        # 更新导航上下文
        if rt.navigation_manager:
            ctx = rt.navigation_manager.context
            ctx.start_point = start
            ctx.multi_targets = targets
            ctx.planned_routes = result["routes"]
            ctx.multi_targets_ordered = result["ordered"]
        
        return ok(result)
    
    except Exception as e:
        from utils.logger import logger
        logger.error(f"多目标路径规划错误: {e}")
        return error(ERR.NAV_ROUTE_ERROR, f"多目标路径规划失败: {str(e)}", http_status=500)


@nav_bp.route('/start', methods=['POST'])
def start_navigation():
    """
    开始导航
    
    请求体:
    {
        "destination": "新华医院",
        "route_segments": [...]
    }
    """
    try:
        if rt.navigation_manager is None:
            return error(ERR.NAV_NOT_READY, "导航管理器未初始化", http_status=500)
        
        data = request.get_json() or {}
        destination = data.get('destination', '')
        route_segments = data.get('route_segments')
        
        if not destination:
            return error(ERR.NAV_INVALID_INPUT, "缺少目的地参数", http_status=400)
        
        # 使用新的NavigationManager接口
        if hasattr(rt.navigation_manager, 'start_navigation'):
            success = rt.navigation_manager.start_navigation(destination, route_segments)
        else:
            # 兼容旧接口
            success = rt.navigation_manager.start_navigation(destination, route_segments)
        
        if not success:
            return error(ERR.NAV_START_FAILED, "导航启动失败，可能已有导航在进行中", http_status=400)
        
        status = rt.navigation_manager.get_status()
        
        if rt.log_manager:
            try:
                rt.log_manager.log_navigation(
                    action="start_navigation",
                    destination=destination,
                    path_info=route_segments,
                    system_response=f"导航已启动到{destination}"
                )
            except:
                pass
        
        return ok({'status': status})
    
    except Exception as e:
        from utils.logger import logger
        logger.error(f"启动导航错误: {e}")
        return error(ERR.NAV_START_FAILED, f"启动导航失败: {str(e)}", http_status=500)


@nav_bp.route('/update', methods=['POST'])
def update_navigation():
    """
    更新导航状态（使用策略系统）
    
    请求体:
    {
        "position": {"lat": 31.23, "lng": 121.47},
        "vision": {...},
        "construction": false,
        "hazards": []
    }
    """
    try:
        if rt.navigation_manager is None:
            return error(ERR.NAV_NOT_READY, "导航管理器未初始化", http_status=500)
        
        data = request.get_json() or {}
        
        # 使用新的update_observation接口
        if hasattr(rt.navigation_manager, 'update_observation'):
            rt.navigation_manager.update_observation(data)
        else:
            # 兼容旧接口
            if 'lat' in data and 'lng' in data:
                rt.navigation_manager.update_position(
                    data['lat'],
                    data['lng'],
                    data.get('hazards')
                )
        
        # 执行策略
        result = rt.navigation_manager.run_step()
        
        return ok({
            'context': rt.navigation_manager.context.to_dict(),
            'strategy_result': result
        })
    
    except Exception as e:
        from utils.logger import logger
        logger.error(f"更新导航错误: {e}")
        return error(ERR.NAV_UPDATE_FAIL, f"更新导航失败: {str(e)}", http_status=500)


@nav_bp.route('/status', methods=['GET'])
def get_navigation_status():
    """获取导航状态"""
    try:
        if rt.navigation_manager is None:
            return error(ERR.NAV_NOT_READY, "导航管理器未初始化", http_status=500)
        
        status = rt.navigation_manager.get_status()
        return ok(status)
    
    except Exception as e:
        from utils.logger import logger
        logger.error(f"获取导航状态错误: {e}")
        return error(ERR.NAV_ENGINE_ERROR, f"获取状态失败: {str(e)}", http_status=500)


@nav_bp.route('/pause', methods=['POST'])
def pause_navigation():
    """暂停导航"""
    try:
        if rt.navigation_manager is None:
            return error(ERR.NAV_NOT_READY, "导航管理器未初始化", http_status=500)
        
        data = request.get_json() or {}
        reason = data.get('reason', '用户暂停')
        
        if hasattr(rt.navigation_manager, 'pause_navigation'):
            success = rt.navigation_manager.pause_navigation(reason)
        else:
            success = rt.navigation_manager.pause(reason)
        
        if not success:
            return error(ERR.NAV_ENGINE_ERROR, "暂停失败", http_status=400)
        
        status = rt.navigation_manager.get_status()
        return ok({'status': status})
    
    except Exception as e:
        return error(ERR.NAV_ENGINE_ERROR, f"暂停失败: {str(e)}", http_status=500)


@nav_bp.route('/resume', methods=['POST'])
def resume_navigation():
    """恢复导航"""
    try:
        if rt.navigation_manager is None:
            return error(ERR.NAV_NOT_READY, "导航管理器未初始化", http_status=500)
        
        if hasattr(rt.navigation_manager, 'resume_navigation'):
            success = rt.navigation_manager.resume_navigation()
        else:
            success = rt.navigation_manager.resume()
        
        if not success:
            return error(ERR.NAV_ENGINE_ERROR, "恢复失败", http_status=400)
        
        status = rt.navigation_manager.get_status()
        return ok({'status': status})
    
    except Exception as e:
        return error(ERR.NAV_ENGINE_ERROR, f"恢复失败: {str(e)}", http_status=500)


@nav_bp.route('/cancel', methods=['POST'])
def cancel_navigation():
    """取消导航"""
    try:
        if rt.navigation_manager is None:
            return error(ERR.NAV_NOT_READY, "导航管理器未初始化", http_status=500)
        
        data = request.get_json() or {}
        reason = data.get('reason', '用户取消')
        
        if hasattr(rt.navigation_manager, 'cancel_navigation'):
            success = rt.navigation_manager.cancel_navigation(reason)
        else:
            success = rt.navigation_manager.cancel(reason)
        
        if not success:
            return error(ERR.NAV_ENGINE_ERROR, "取消失败", http_status=400)
        
        status = rt.navigation_manager.get_status()
        return ok({'status': status})
    
    except Exception as e:
        return error(ERR.NAV_ENGINE_ERROR, f"取消失败: {str(e)}", http_status=500)


@nav_bp.route('/complete', methods=['POST'])
def complete_navigation():
    """完成导航"""
    try:
        if rt.navigation_manager is None:
            return error(ERR.NAV_NOT_READY, "导航管理器未初始化", http_status=500)
        
        if hasattr(rt.navigation_manager, 'complete_navigation'):
            success = rt.navigation_manager.complete_navigation()
        else:
            success = rt.navigation_manager.complete()
        
        if not success:
            return error(ERR.NAV_ENGINE_ERROR, "完成失败", http_status=400)
        
        status = rt.navigation_manager.get_status()
        return ok({'status': status})
    
    except Exception as e:
        return error(ERR.NAV_ENGINE_ERROR, f"完成失败: {str(e)}", http_status=500)


@nav_bp.route('/visual_guidance', methods=['POST'])
def visual_guidance():
    """
    实时视觉导航指引（整合 A-G 七个视觉子策略）。
    
    请求：
      - form-data: image: 文件
      - 可选：voice_command: 文本（你之前有的话可以保留）
    """
    try:
        nav_manager = rt.navigation_manager
        vision_engine = rt.vision_engine
        
        if vision_engine is None:
            return api_error("视觉引擎未初始化", status_code=500)
        
        if nav_manager is None:
            return api_error("导航管理器未初始化", status_code=500)
        
        # 支持multipart/form-data和base64两种方式
        file = request.files.get("image")
        if file:
            image_data = file.read()
            try:
                import numpy as np
                from PIL import Image
                import io
                img = Image.open(io.BytesIO(image_data))
                image_np = np.array(img)
                if len(image_np.shape) == 3 and image_np.shape[2] == 4:
                    # RGBA转RGB
                    image_np = image_np[:, :, :3]
            except Exception as e:
                return api_error(f"图片格式错误: {str(e)}", status_code=400)
        else:
            # 尝试base64
            data = request.get_json() or {}
            image_b64 = data.get("image")
            if not image_b64:
                return api_error("未上传图片", status_code=400)
            try:
                from utils.image_utils import decode_base64_image
                image_np = decode_base64_image(image_b64)
            except ImportError:
                import base64
                import numpy as np
                from PIL import Image
                import io
                try:
                    image_data = base64.b64decode(image_b64)
                    img = Image.open(io.BytesIO(image_data))
                    image_np = np.array(img)
                    if len(image_np.shape) == 3 and image_np.shape[2] == 4:
                        image_np = image_np[:, :, :3]
                except Exception as e:
                    return api_error(f"base64解码失败: {str(e)}", status_code=400)
            
            if image_np is None:
                return api_error("图片格式错误", status_code=400)
        
        # 1) 基础视觉识别（YOLO + OCR）
        try:
            vision_results = vision_engine.detect_and_recognize(image_np)
            detections = vision_results.get("detections", [])
            ocr_results = vision_results.get("ocr_results", [])
        except Exception as e:
            # 如果视觉引擎调用失败，使用空结果
            detections = []
            ocr_results = []
        
        # 2) 调用导航策略分析（A-G）
        guidance_list = nav_manager.analyze_frame_for_guidance(
            image_np=image_np,
            detections=detections,
            ocr_results=ocr_results,
            env_meta={},  # 后面可以加"室内/室外、时间段"等信息
        )
        
        # 3) 前端可以用 guidance_list 把提示播报出来
        return api_success({
            "vision": {
                "detections": detections,
                "ocr_results": ocr_results,
            },
            "guidance": guidance_list,
        })
    
    except Exception as e:
        from utils.logger import logger
        logger.error(f"视觉导航指引内部错误: {e}")
        return api_error(
            "视觉导航指引内部错误",
            details={"exception": str(e)},
            status_code=500,
        )


@nav_bp.route('/describe_scene', methods=['POST'])
def describe_scene():
    """场景描述接口（被动问询）"""
    try:
        # 获取图像
        image_bytes = None
        vision_result = None
        
        if 'image' in request.files:
            file = request.files['image']
            image_bytes = file.read()
        elif request.is_json:
            data = request.get_json() or {}
            image_b64 = data.get('image')
            if image_b64:
                image_bytes = decode_base64_image(image_b64)
                if image_bytes is None:
                    return error(ERR.NAV_IO_002, "图片解码失败")
            
            # 如果提供了vision_result，直接使用
            vision_result = data.get('vision_result')
        
        if image_bytes is None and vision_result is None:
            return error(ERR.NAV_IO_001, "缺少图片数据或视觉识别结果")

        # 如果有图像，先调用视觉识别
        if image_bytes and vision_result is None:
            try:
                if hasattr(rt, 'vision_engine') and rt.vision_engine:
                    vision_result = rt.vision_engine.detect_and_recognize(image_bytes)
            except Exception as e:
                logger.warn(f"[describe_scene] vision recognition failed: {e}")

        # 调用场景描述引擎
        scene_engine = get_scene_engine()
        description = scene_engine.describe(image_bytes, vision_result)

        return ok({
            "code": "NAV_SCENE_OK",
            "description": description.get("summary", ""),
            "scene": description.get("scene", "unknown"),
            "objects": description.get("objects", []),
            "environment": description.get("environment", {}),
            "hazards": description.get("hazards", [])
        })
    except Exception as e:
        logger.error(f"[navigation_routes_v4] describe_scene error: {e}", exc_info=True)
        return error(ERR.NAV_STRAT_001, f"场景描述失败: {str(e)}")


@nav_bp.route('/scene_query', methods=['POST'])
def scene_query():
    """场景问答接口"""
    try:
        data = request.get_json() or {}
        question = data.get('question')
        
        if not question:
            return error(ERR.NAV_GENERAL_001, "缺少question参数")

        # 获取图像（可选）
        image_bytes = None
        vision_result = None
        
        image_b64 = data.get('image')
        if image_b64:
            image_bytes = decode_base64_image(image_b64)
            if image_bytes is None:
                return error(ERR.NAV_IO_002, "图片解码失败")
        
        vision_result = data.get('vision_result')
        
        # 如果有图像，先调用视觉识别
        if image_bytes and vision_result is None:
            try:
                if hasattr(rt, 'vision_engine') and rt.vision_engine:
                    vision_result = rt.vision_engine.detect_and_recognize(image_bytes)
            except Exception as e:
                logger.warn(f"[scene_query] vision recognition failed: {e}")

        # 调用场景描述引擎的问答功能
        scene_engine = get_scene_engine()
        result = scene_engine.query(question, image_bytes, vision_result)

        return ok({
            "answer": result.get("answer", ""),
            "meta": result.get("meta", {})
        })
    except Exception as e:
        logger.error(f"[navigation_routes_v4] scene_query error: {e}", exc_info=True)
        return error(ERR.NAV_STRAT_001, f"场景问答失败: {str(e)}")


@nav_bp.route('/describe_scene', methods=['POST'])
def describe_scene():
    """
    场景描述 API
    支持两种调用方式：
    1）上传图片：multipart/form-data，字段 image
    2）上传已有检测结果：application/json，字段 detections / ocr_results / hazards / facilities / crowd / env
       （用于前端已有 YOLO/Bbox 的情况，比如 VisionBridge 已处理过）
    """
    try:
        scene_engine = get_scene_engine()
        if scene_engine is None:
            return error(ERR.NAV_STRAT_001, "场景描述引擎未初始化", http_status=500)

        # 优先看是否有图片
        if 'image' in request.files:
            file = request.files['image']
            if not file:
                return error(ERR.NAV_IO_001, "未上传图片", http_status=400)

            image_bytes = file.read()
            image_np = _image_to_numpy(image_bytes)
            if image_np is None:
                return error(ERR.NAV_IO_002, "图片格式错误", http_status=400)

            start = time.time()

            # 1) 基础视觉识别
            detections = []
            ocr_results = []
            if hasattr(rt, 'vision_engine') and rt.vision_engine:
                try:
                    v_res = rt.vision_engine.detect_and_recognize(image_np)
                    detections = v_res.get('detections', [])
                    ocr_results = v_res.get('ocr_results', [])
                except Exception as e:
                    logger.warning(f"视觉识别失败: {e}")

            # 2) 危险、设施、人群，可选
            hazards = []
            facilities = []
            crowd = None

            if hasattr(rt, 'hazard_detector') and rt.hazard_detector:
                try:
                    hazards_raw = rt.hazard_detector.detect_hazards(image_np, detected_objects=detections)
                    hazards = [h.to_dict() if hasattr(h, 'to_dict') else h for h in hazards_raw] if hazards_raw else []
                except Exception as e:
                    logger.warning(f"危险检测失败: {e}")

            if hasattr(rt, 'facility_detector') and rt.facility_detector:
                try:
                    fac_raw = rt.facility_detector.detect_facility(image_np)
                    facilities = [f.to_dict() if hasattr(f, 'to_dict') else f for f in fac_raw] if fac_raw else []
                except Exception as e:
                    logger.warning(f"设施检测失败: {e}")

            if hasattr(rt, 'crowd_density_detector') and rt.crowd_density_detector:
                try:
                    c_res = rt.crowd_density_detector.detect_density(image_np)
                    crowd = c_res.to_dict() if hasattr(c_res, 'to_dict') else c_res if c_res else None
                except Exception as e:
                    logger.warning(f"人群密度检测失败: {e}")

            # 3) 环境特征（可以用亮度/反光估计模块，如果暂时没有就传空）
            env_features = {}
            # TODO: 如果你有 brightness/反光估计模块，可以在这里填充 env_features

            desc = scene_engine.describe(
                objects=_normalize_objects(detections),
                texts=ocr_results,
                hazards=hazards,
                facilities=facilities,
                crowd_density=crowd,
                env_features=env_features,
            )

            latency = (time.time() - start) * 1000

            # 记录日志
            if hasattr(rt, 'log_manager') and rt.log_manager:
                try:
                    rt.log_manager.log_visual_event(
                        event_type="scene_description",
                        detection_result={
                            "objects_count": len(detections),
                            "hazards_count": len(hazards),
                            "facilities_count": len(facilities),
                            "crowd": crowd,
                        },
                        system_response=desc.get("summary", ""),
                    )
                except Exception as e:
                    logger.warning(f"记录场景描述日志失败: {e}")

            return ok({
                "code": "NAV_SCENE_OK",
                "latency_ms": round(latency, 2),
                "description": desc.get("summary"),
                "scene_type": desc.get("scene_type"),
                "environment": desc.get("environment"),
                "objects": desc.get("objects"),
                "hazards": desc.get("hazards"),
                "explanation": desc.get("explanation"),
            })

        else:
            # JSON 模式：前端已经有 YOLO 等结构化数据
            data = request.get_json(force=True, silent=True) or {}
            detections = data.get("detections") or data.get("yolo") or []
            ocr_results = data.get("ocr_results") or data.get("texts") or []
            hazards = data.get("hazards") or []
            facilities = data.get("facilities") or []
            crowd = data.get("crowd_density") or data.get("crowd") or None
            env_features = data.get("env") or {}

            if not detections and not ocr_results and not facilities and not hazards:
                return error(ERR.NAV_GENERAL_001, "缺少场景输入数据（image 或 detections）", http_status=400)

            desc = scene_engine.describe(
                objects=_normalize_objects(detections),
                texts=ocr_results,
                hazards=hazards,
                facilities=facilities,
                crowd_density=crowd,
                env_features=env_features,
            )

            return ok({
                "code": "NAV_SCENE_OK",
                "description": desc.get("summary"),
                "scene_type": desc.get("scene_type"),
                "environment": desc.get("environment"),
                "objects": desc.get("objects"),
                "hazards": desc.get("hazards"),
                "explanation": desc.get("explanation"),
            })

    except Exception as e:
        logger.exception(f"场景描述接口异常: {e}")
        return error(ERR.NAV_STRAT_001, f"场景描述失败: {str(e)}", http_status=500)


@nav_bp.route('/describe_scene_for_navigation', methods=['POST'])
def describe_scene_for_navigation():
    """
    结合导航情境的场景描述（语音问答版）
    支持两种输入方式：
    1. multipart/form-data: image文件
    2. application/json: {image: base64字符串}
    """
    try:
        data = request.get_json() or {}
        image = data.get("image")

        # 如果没有JSON，尝试从form-data获取
        if not image and 'image' in request.files:
            file = request.files['image']
            import base64
            image_bytes = file.read()
            image = base64.b64encode(image_bytes).decode('utf-8')

        if not image:
            return error(ERR.NAV_IO_001, "缺少 image 参数", http_status=400)

        # 加载图像
        try:
            from utils.image_utils import decode_base64_image
            frame = decode_base64_image(image)
        except Exception as e:
            return error(ERR.NAV_IO_002, f"图片解码失败: {str(e)}", http_status=400)

        if frame is None:
            return error(ERR.NAV_IO_002, "图片解码失败", http_status=400)

        # 调用场景描述引擎
        try:
            from backend.vision.scene_description_engine import SceneDescriptionEngine
            if rt.vision_engine:
                scene_engine = SceneDescriptionEngine(rt.vision_engine)
            else:
                scene_engine = SceneDescriptionEngine()
            
            result = scene_engine.describe(frame)
        except ImportError:
            # 如果backend版本不存在，使用modules版本
            try:
                from modules.scene_description.description_engine import SceneDescriptionEngine
                scene_engine = SceneDescriptionEngine()
                # 先获取检测结果
                if rt.vision_engine:
                    v_res = rt.vision_engine.detect_and_recognize(frame)
                    detections = v_res.get('detections', [])
                    ocr_results = v_res.get('ocr_results', [])
                    result = scene_engine.describe(
                        objects=detections,
                        texts=ocr_results,
                        hazards=[],
                        facilities=[],
                        env_features={}
                    )
                else:
                    return error(ERR.NAV_VIS_001, "视觉引擎未初始化", http_status=500)
            except Exception as e:
                return error(ERR.NAV_VIS_001, f"场景描述失败: {str(e)}", http_status=500)
        except Exception as e:
            return error(ERR.NAV_VIS_001, f"场景描述失败: {str(e)}", http_status=500)

        if not result.get("success"):
            return error(ERR.NAV_VIS_001, result.get("error", "场景描述失败"), http_status=500)

        # 生成TTS文本
        response_text = f"当前环境：{result.get('summary', '环境正常')}"

        return ok({
            "summary": result.get("summary", ""),
            "objects": result.get("objects", []),
            "scene_type": result.get("scene_type", "unknown"),
            "environment": result.get("environment", {}),
            "tts": response_text,
            "timestamp": result.get("timestamp")
        })
    except Exception as e:
        return error(ERR.NAV_VIS_001, f"场景描述失败: {str(e)}", http_status=500)

