# routes/visual_routes.py
# 视觉相关路由（识别 / 台阶 / 标识牌 / 危险 / 公共设施 / 综合检测 / 视觉导航）

from __future__ import annotations

import time
import base64
from typing import Any, Dict, List, Optional

from flask import Blueprint, jsonify, request

from core.response import api_success, api_error
from config.error_codes import (
    ErrorCodeSpec,
    get_error_spec,
)


def image_to_numpy(image_bytes: bytes):
    """
    将图片字节流转换为numpy数组
    
    兼容多种导入方式
    """
    try:
        from utils.image_utils import image_to_numpy as utils_image_to_numpy
        return utils_image_to_numpy(image_bytes)
    except ImportError:
        # 如果utils.image_utils不存在，使用本地实现
        try:
            import numpy as np
            from PIL import Image
            import io
            
            # 尝试解码为numpy数组
            img = Image.open(io.BytesIO(image_bytes))
            image_np = np.array(img)
            if len(image_np.shape) == 3 and image_np.shape[2] == 4:
                image_np = image_np[:, :, :3]
            return image_np
        except Exception as e:
            print(f"⚠️ 图片解码失败: {e}")
            return None


def create_visual_blueprint(
    *,
    vision_engine,
    step_detector,
    signboard_detector,
    hazard_detector,
    facility_detector,
    traffic_light_detector,
    crowd_density_detector,
    queue_detector,
    doorplate_reader,
    local_map_generator,
    # 视觉导航增强相关
    scene_memory_system=None,
    saliency_roi=None,
    temporal_fusion=None,
    visual_language_fusion=None,
    # 日志相关
    log_manager=None,
) -> Blueprint:
    """
    工厂方法：创建视觉相关 Blueprint。

    使用方式（web_test_server.py 中）：
        from routes.visual_routes import create_visual_blueprint
        visual_bp = create_visual_blueprint(
            vision_engine=vision_engine,
            step_detector=step_detector,
            ...
        )
        app.register_blueprint(visual_bp)
    """

    bp = Blueprint("visual", __name__)

    # ========== /api/recognize 基础视觉识别 ==========

    @bp.route("/api/recognize", methods=["POST"])
    def recognize():
        """基础视觉识别"""
        try:
            if vision_engine is None:
                return api_error("VISION_ENGINE_NOT_INITIALIZED")

            file = request.files.get("image")
            if not file:
                return api_error("VISION_IMAGE_MISSING")

            image_np = image_to_numpy(file.read())
            if image_np is None:
                return api_error("VISION_IMAGE_DECODE_FAILED")

            results = vision_engine.detect_and_recognize(image_np)

            # 记录日志
            if log_manager:
                try:
                    log_manager.log_visual_event(
                        event_type="vision_recognition",
                        detection_result={
                            "detections_count": len(results.get("detections", [])),
                            "ocr_results_count": len(results.get("ocr_results", [])),
                            "processing_time": results.get("processing_time", 0),
                        },
                        system_response="视觉识别完成",
                    )
                except Exception as e:
                    # 不阻断主流程
                    print(f"⚠️ 记录视觉日志失败: {e}")

            return api_success(
                {
                    "detections": results.get("detections", []),
                    "ocr_results": results.get("ocr_results", []),
                    "processing_time": results.get("processing_time", 0),
                }
            )
        except Exception as e:
            # 这里可以在日志模块中记录完整异常
            if log_manager:
                try:
                    log_manager.log_system_event(
                        event="vision_recognition_error",
                        metadata={
                            "exception_type": type(e).__name__,
                            "exception_message": str(e),
                        },
                    )
                except Exception:
                    pass
            return api_error(
                "VISION_PROCESSING_FAILED",
                details={"exception_type": type(e).__name__, "exception_message": str(e)},
            )

    # ========== /api/detect/step 台阶检测 ==========

    @bp.route("/api/detect/step", methods=["POST"])
    def detect_step():
        """台阶检测"""
        try:
            if step_detector is None:
                return api_error("STEP_DETECTOR_NOT_INITIALIZED")

            file = request.files.get("image")
            if not file:
                return api_error("STEP_IMAGE_MISSING")

            image_np = image_to_numpy(file.read())
            if image_np is None:
                return api_error("STEP_IMAGE_DECODE_FAILED")

            result = step_detector.detect_step(image_np)

            # 日志
            if log_manager:
                try:
                    log_manager.log_visual_event(
                        event_type="step_detection",
                        detection_result={
                            "detected": result is not None,
                            "result": result if result else None,
                        },
                        system_response="台阶检测完成" if result else "未检测到台阶",
                    )
                except Exception as e:
                    print(f"⚠️ 记录台阶检测日志失败: {e}")

            return api_success(
                {
                    "step_detection": result
                    if result
                    else {"detected": False, "message": "未检测到台阶"},
                }
            )
        except Exception as e:
            if log_manager:
                try:
                    log_manager.log_system_event(
                        event="step_detection_error",
                        metadata={
                            "exception_type": type(e).__name__,
                            "exception_message": str(e),
                        },
                    )
                except Exception:
                    pass
            return api_error(
                "STEP_DETECTION_FAILED",
                details={"exception_type": type(e).__name__, "exception_message": str(e)},
            )

    # ========== /api/detect/signboard 标识牌检测 ==========

    @bp.route("/api/detect/signboard", methods=["POST"])
    def detect_signboard():
        """标识牌检测"""
        try:
            if signboard_detector is None:
                return api_error("SIGNBOARD_DETECTOR_NOT_INITIALIZED")

            file = request.files.get("image")
            if not file:
                return api_error("SIGNBOARD_IMAGE_MISSING")

            image_np = image_to_numpy(file.read())
            if image_np is None:
                return api_error("SIGNBOARD_IMAGE_DECODE_FAILED")

            results = signboard_detector.detect_signboards(image_np)

            return api_success(
                {"signboards": [r.to_dict() for r in results] if results else []}
            )
        except Exception as e:
            if log_manager:
                try:
                    log_manager.log_system_event(
                        event="signboard_detection_error",
                        metadata={
                            "exception_type": type(e).__name__,
                            "exception_message": str(e),
                        },
                    )
                except Exception:
                    pass
            return api_error(
                "SIGNBOARD_DETECTION_FAILED",
                details={"exception_type": type(e).__name__, "exception_message": str(e)},
            )

    # ========== /api/detect/hazard 危险检测 ==========

    @bp.route("/api/detect/hazard", methods=["POST"])
    def detect_hazard():
        """危险检测"""
        try:
            if hazard_detector is None:
                return api_error("HAZARD_DETECTOR_NOT_INITIALIZED")

            file = request.files.get("image")
            if not file:
                return api_error("HAZARD_IMAGE_MISSING")

            image_np = image_to_numpy(file.read())
            if image_np is None:
                return api_error("HAZARD_IMAGE_DECODE_FAILED")

            # 如果可能，传递YOLO检测结果用于过滤误报
            detected_objects = []
            if vision_engine:
                try:
                    vision_results = vision_engine.detect_and_recognize(image_np)
                    detected_objects = vision_results.get("detections", [])
                except Exception:
                    pass

            results = hazard_detector.detect_hazards(
                image_np, detected_objects=detected_objects
            )

            # 记录日志
            if log_manager:
                try:
                    log_manager.log_visual_event(
                        event_type="hazard_detection",
                        detection_result={
                            "hazards_count": len(results),
                            "hazards": [r.to_dict() for r in results[:5]],
                        },
                        system_response=f"检测到{len(results)}个危险区域",
                    )
                except Exception as e:
                    print(f"⚠️ 记录危险检测日志失败: {e}")

            # 获取检测摘要（如果hazard_detector有这个方法）
            summary = {}
            if hasattr(hazard_detector, 'get_detection_summary'):
                try:
                    summary = hazard_detector.get_detection_summary(results)
                except Exception:
                    pass

            return api_success(
                {
                    "hazards": [r.to_dict() for r in results] if results else [],
                    "summary": summary,
                }
            )
        except Exception as e:
            if log_manager:
                try:
                    log_manager.log_system_event(
                        event="hazard_detection_error",
                        metadata={
                            "exception_type": type(e).__name__,
                            "exception_message": str(e),
                        },
                    )
                except Exception:
                    pass
            return api_error(
                "HAZARD_DETECTION_FAILED",
                details={"exception_type": type(e).__name__, "exception_message": str(e)},
            )

    # ========== /api/detect/facility 公共设施检测 ==========

    @bp.route("/api/detect/facility", methods=["POST"])
    def detect_facility():
        """公共设施检测"""
        try:
            if facility_detector is None:
                return api_error("FACILITY_DETECTOR_NOT_INITIALIZED")

            file = request.files.get("image")
            if not file:
                return api_error("FACILITY_IMAGE_MISSING")

            image_np = image_to_numpy(file.read())
            if image_np is None:
                return api_error("FACILITY_IMAGE_DECODE_FAILED")

            results = facility_detector.detect_facility(image_np)

            return api_success(
                {"facilities": [r.to_dict() for r in results] if results else []}
            )
        except Exception as e:
            if log_manager:
                try:
                    log_manager.log_system_event(
                        event="facility_detection_error",
                        metadata={
                            "exception_type": type(e).__name__,
                            "exception_message": str(e),
                        },
                    )
                except Exception:
                    pass
            return api_error(
                "FACILITY_DETECTION_FAILED",
                details={"exception_type": type(e).__name__, "exception_message": str(e)},
            )

    # ========== /api/detect/traffic_light 红绿灯检测 ==========

    @bp.route("/api/detect/traffic_light", methods=["POST"])
    def detect_traffic_light():
        """红绿灯检测"""
        try:
            if traffic_light_detector is None:
                return api_error("TRAFFIC_LIGHT_DETECTOR_NOT_INITIALIZED")

            file = request.files.get("image")
            if not file:
                return api_error("TRAFFIC_LIGHT_IMAGE_MISSING")

            image_np = image_to_numpy(file.read())
            if image_np is None:
                return api_error("TRAFFIC_LIGHT_IMAGE_DECODE_FAILED")

            result = traffic_light_detector.detect_traffic_light(image_np)

            broadcast_message = None
            if result and hasattr(result, 'get_broadcast_message'):
                try:
                    broadcast_message = result.get_broadcast_message()
                except Exception:
                    pass

            return api_success(
                {
                    "traffic_light": result.to_dict() if result else None,
                    "broadcast_message": broadcast_message,
                }
            )
        except Exception as e:
            if log_manager:
                try:
                    log_manager.log_system_event(
                        event="traffic_light_detection_error",
                        metadata={
                            "exception_type": type(e).__name__,
                            "exception_message": str(e),
                        },
                    )
                except Exception:
                    pass
            return api_error(
                "TRAFFIC_LIGHT_DETECTION_FAILED",
                details={"exception_type": type(e).__name__, "exception_message": str(e)},
            )

    # ========== /api/detect/crowd_density 人群密度检测 ==========

    @bp.route("/api/detect/crowd_density", methods=["POST"])
    def detect_crowd_density():
        """人群密度检测"""
        try:
            if crowd_density_detector is None:
                return api_error("CROWD_DENSITY_DETECTOR_NOT_INITIALIZED")

            file = request.files.get("image")
            if not file:
                return api_error("CROWD_DENSITY_IMAGE_MISSING")

            image_np = image_to_numpy(file.read())
            if image_np is None:
                return api_error("CROWD_DENSITY_IMAGE_DECODE_FAILED")

            result = crowd_density_detector.detect_density(image_np)

            return api_success({"density": result.to_dict() if result else None})
        except Exception as e:
            if log_manager:
                try:
                    log_manager.log_system_event(
                        event="crowd_density_detection_error",
                        metadata={
                            "exception_type": type(e).__name__,
                            "exception_message": str(e),
                        },
                    )
                except Exception:
                    pass
            return api_error(
                "CROWD_DENSITY_DETECTION_FAILED",
                details={"exception_type": type(e).__name__, "exception_message": str(e)},
            )

    # ========== /api/detect/queue 排队检测 ==========

    @bp.route("/api/detect/queue", methods=["POST"])
    def detect_queue():
        """排队检测"""
        try:
            if queue_detector is None:
                return api_error("QUEUE_DETECTOR_NOT_INITIALIZED")

            file = request.files.get("image")
            if not file:
                return api_error("QUEUE_IMAGE_MISSING")

            image_np = image_to_numpy(file.read())
            if image_np is None:
                return api_error("QUEUE_IMAGE_DECODE_FAILED")

            result = queue_detector.detect_queue(image_np)

            return api_success({"queue": result.to_dict() if result else None})
        except Exception as e:
            if log_manager:
                try:
                    log_manager.log_system_event(
                        event="queue_detection_error",
                        metadata={
                            "exception_type": type(e).__name__,
                            "exception_message": str(e),
                        },
                    )
                except Exception:
                    pass
            return api_error(
                "QUEUE_DETECTION_FAILED",
                details={"exception_type": type(e).__name__, "exception_message": str(e)},
            )

    # ========== /api/detect/doorplate 门牌号识别 ==========

    @bp.route("/api/detect/doorplate", methods=["POST"])
    def detect_doorplate():
        """门牌号识别"""
        try:
            if doorplate_reader is None:
                return api_error("DOORPLATE_READER_NOT_INITIALIZED")

            file = request.files.get("image")
            if not file:
                return api_error("DOORPLATE_IMAGE_MISSING")

            image_np = image_to_numpy(file.read())
            if image_np is None:
                return api_error("DOORPLATE_IMAGE_DECODE_FAILED")

            results = doorplate_reader.read_doorplate(image_np)

            return api_success(
                {"doorplates": [r.to_dict() for r in results] if results else []}
            )
        except Exception as e:
            if log_manager:
                try:
                    log_manager.log_system_event(
                        event="doorplate_recognition_error",
                        metadata={
                            "exception_type": type(e).__name__,
                            "exception_message": str(e),
                        },
                    )
                except Exception:
                    pass
            return api_error(
                "DOORPLATE_RECOGNITION_FAILED",
                details={"exception_type": type(e).__name__, "exception_message": str(e)},
            )

    # ========== /api/map/generate 本地地图生成 ==========

    @bp.route("/api/map/generate", methods=["POST"])
    def generate_local_map():
        """生成本地地图"""
        try:
            if local_map_generator is None:
                return api_error("LOCAL_MAP_GENERATOR_NOT_INITIALIZED")

            data = request.get_json() or {}
            dx = float(data.get("dx", 0.0))
            dy = float(data.get("dy", 0.0))
            angle_delta = float(data.get("angle_delta", 0.0))

            # 更新位置
            local_map_generator.update_position(dx, dy, angle_delta)

            # 如果有图片，添加地标
            if "image" in request.files:
                file = request.files["image"]
                image_np = image_to_numpy(file.read())
                if image_np is not None and facility_detector:
                    facilities = facility_detector.detect_facility(image_np)
                    for facility in facilities:
                        if hasattr(local_map_generator, 'add_landmark'):
                            local_map_generator.add_landmark(
                                facility.type.value if hasattr(facility.type, 'value') else str(facility.type),
                                (0, 0),  # TODO: 位置根据后续算法计算
                                facility.label if hasattr(facility, 'label') else "",
                                facility.confidence if hasattr(facility, 'confidence') else 0.0,
                            )

            local_map = None
            if hasattr(local_map_generator, 'get_map'):
                local_map = local_map_generator.get_map()

            return api_success({"map": local_map.to_dict() if local_map and hasattr(local_map, 'to_dict') else None})
        except Exception as e:
            if log_manager:
                try:
                    log_manager.log_system_event(
                        event="local_map_generation_error",
                        metadata={
                            "exception_type": type(e).__name__,
                            "exception_message": str(e),
                        },
                    )
                except Exception:
                    pass
            return api_error(
                "LOCAL_MAP_GENERATION_FAILED",
                details={"exception_type": type(e).__name__, "exception_message": str(e)},
            )

    # ========== /api/detect/comprehensive 综合检测 ==========

    @bp.route("/api/detect/comprehensive", methods=["POST"])
    def comprehensive_detection():
        """综合检测 - 同时运行所有视觉检测模块"""
        try:
            file = request.files.get("image")
            if not file:
                return api_error("VISION_IMAGE_MISSING")

            image_np = image_to_numpy(file.read())
            if image_np is None:
                return api_error("VISION_IMAGE_DECODE_FAILED")

            results: Dict[str, Any] = {}

            # 1. 基础视觉识别
            if vision_engine:
                try:
                    vision_results = vision_engine.detect_and_recognize(image_np)
                    results["vision"] = {
                        "detections": vision_results.get("detections", []),
                        "ocr_results": vision_results.get("ocr_results", []),
                    }
                except Exception as e:
                    results["vision"] = {"error": str(e)}

            # 2. 台阶检测
            if step_detector:
                try:
                    step_result = step_detector.detect_step(image_np)
                    results["step"] = (
                        step_result if step_result else {"detected": False}
                    )
                except Exception as e:
                    results["step"] = {"error": str(e)}

            # 3. 标识牌检测
            if signboard_detector:
                try:
                    signboards = signboard_detector.detect_signboards(image_np)
                    results["signboard"] = (
                        [r.to_dict() for r in signboards] if signboards else []
                    )
                except Exception as e:
                    results["signboard"] = {"error": str(e)}

            # 4. 危险检测
            if hazard_detector:
                try:
                    detected_objects = results.get("vision", {}).get(
                        "detections", []
                    )
                    hazards = hazard_detector.detect_hazards(
                        image_np, detected_objects=detected_objects
                    )
                    results["hazard"] = (
                        [r.to_dict() for r in hazards] if hazards else []
                    )
                except Exception as e:
                    results["hazard"] = {"error": str(e)}

            # 5. 公共设施检测
            if facility_detector:
                try:
                    facilities = facility_detector.detect_facility(image_np)
                    results["facility"] = (
                        [r.to_dict() for r in facilities] if facilities else []
                    )
                except Exception as e:
                    results["facility"] = {"error": str(e)}

            # 6. 红绿灯检测
            if traffic_light_detector:
                try:
                    traffic_light = traffic_light_detector.detect_traffic_light(
                        image_np
                    )
                    results["traffic_light"] = (
                        traffic_light.to_dict() if traffic_light else None
                    )
                except Exception as e:
                    results["traffic_light"] = {"error": str(e)}

            # 7. 人群密度检测
            if crowd_density_detector:
                try:
                    density = crowd_density_detector.detect_density(image_np)
                    results["crowd_density"] = (
                        density.to_dict() if density else None
                    )
                except Exception as e:
                    results["crowd_density"] = {"error": str(e)}

            # 8. 排队检测
            if queue_detector:
                try:
                    queue = queue_detector.detect_queue(image_np)
                    results["queue"] = queue.to_dict() if queue else None
                except Exception as e:
                    results["queue"] = {"error": str(e)}

            # 9. 门牌号识别
            if doorplate_reader:
                try:
                    doorplates = doorplate_reader.read_doorplate(image_np)
                    results["doorplate"] = (
                        [d.to_dict() for d in doorplates] if doorplates else []
                    )
                except Exception as e:
                    results["doorplate"] = {"error": str(e)}

            return jsonify(
                {
                    "success": True,
                    "results": results,
                    "timestamp": time.time(),
                }
            )
        except Exception as e:
            if log_manager:
                try:
                    log_manager.log_system_event(
                        event="comprehensive_detection_error",
                        metadata={
                            "exception_type": type(e).__name__,
                            "exception_message": str(e),
                        },
                    )
                except Exception:
                    pass
            # 综合检测出错，用通用视觉错误
            return api_error(
                "VISION_PROCESSING_FAILED",
                details={"exception_type": type(e).__name__, "exception_message": str(e)},
            )

    # ========== /api/navigation/visual_guidance 视觉导航指引 ==========

    @bp.route("/api/navigation/visual_guidance", methods=["POST"])
    def visual_guidance():
        """实时视觉导航指引（基于摄像头画面）"""
        try:
            if vision_engine is None:
                return api_error("NAV_VISUAL_GUIDANCE_NOT_AVAILABLE")

            file = request.files.get("image")
            if not file:
                return api_error("NAV_VISUAL_GUIDANCE_IMAGE_MISSING")

            image_np = image_to_numpy(file.read())
            if image_np is None:
                return api_error("NAV_VISUAL_GUIDANCE_IMAGE_DECODE_FAILED")

            start_time = time.time()

            # ===== 显著性 ROI 优化 =====
            use_roi_optimization = saliency_roi is not None
            vision_results: Dict[str, Any]

            if use_roi_optimization:
                try:
                    roi_regions = saliency_roi.extract_roi(image_np, top_k=5)
                    if roi_regions:
                        all_objects = []
                        all_texts = []
                        for roi in roi_regions:
                            x, y, w, h = roi["bbox"]
                            roi_img = image_np[y : y + h, x : x + w]
                            if roi_img.size == 0:
                                continue
                            roi_res = vision_engine.detect_and_recognize(roi_img)
                            for obj in roi_res.get("detections", []):
                                if "bbox" in obj:
                                    ox, oy, ow, oh = obj["bbox"]
                                    obj["bbox"] = (ox + x, oy + y, ow, oh)
                                all_objects.append(obj)
                            for text in roi_res.get("ocr_results", []):
                                if "bbox" in text:
                                    ox, oy, ow, oh = text["bbox"]
                                    text["bbox"] = (ox + x, oy + y, ow, oh)
                                all_texts.append(text)
                        vision_results = {
                            "detections": all_objects,
                            "ocr_results": all_texts,
                            "processing_time": time.time() - start_time,
                            "roi_optimized": True,
                        }
                    else:
                        vision_results = vision_engine.detect_and_recognize(image_np)
                        vision_results["roi_optimized"] = False
                except Exception:
                    # ROI 出错时退回全图
                    vision_results = vision_engine.detect_and_recognize(image_np)
                    vision_results["roi_optimized"] = False
            else:
                vision_results = vision_engine.detect_and_recognize(image_np)
                vision_results["roi_optimized"] = False

            # 2. 检测场景关键节点
            detected_nodes = []
            if scene_memory_system:
                node_detector = getattr(scene_memory_system, "node_detector", None)
                if node_detector and hasattr(node_detector, 'detect_nodes'):
                    try:
                        detected_nodes = node_detector.detect_nodes(image_np)
                    except Exception:
                        pass

            # 3. 标识牌
            signboard_results = []
            if signboard_detector:
                try:
                    signboard_results = signboard_detector.detect_signboards(image_np)
                except Exception:
                    pass

            # 4. 台阶 + 危险
            step_detected = False
            hazards_detected = []
            if step_detector:
                try:
                    step_result = step_detector.detect_step(image_np)
                    step_detected = step_result is not None
                except Exception:
                    pass
            if hazard_detector:
                try:
                    detected_objects = vision_results.get("detections", [])
                    hazards_detected = hazard_detector.detect_hazards(
                        image_np, detected_objects=detected_objects
                    )
                except Exception:
                    pass

            # ===== 时序融合 =====
            detection_data: Dict[str, Any] = {
                "objects": vision_results.get("detections", []),
                "texts": vision_results.get("ocr_results", []),
                "signboards": [
                    {
                        "type": r.type.value if hasattr(r.type, 'value') else str(r.type),
                        "bbox": r.bbox if hasattr(r, 'bbox') else [],
                        "confidence": r.confidence if hasattr(r, 'confidence') else 0.0,
                    }
                    for r in signboard_results
                ]
                if signboard_results
                else [],
                "step_detected": step_detected,
                "hazards": [
                    {
                        "type": h.type.value if hasattr(h.type, 'value') else str(h.type),
                        "bbox": h.bbox if hasattr(h, 'bbox') else [],
                        "severity": h.severity.value if hasattr(h.severity, 'value') else str(h.severity),
                        "confidence": h.confidence if hasattr(h, 'confidence') else 0.0,
                    }
                    for h in hazards_detected
                ]
                if hazards_detected
                else [],
            }

            stable_detection = detection_data
            if temporal_fusion:
                try:
                    if hasattr(temporal_fusion, 'fuse'):
                        stable_detection = temporal_fusion.fuse(detection_data)
                except Exception:
                    pass

            vision_results["detections"] = stable_detection.get("objects", [])
            vision_results["ocr_results"] = stable_detection.get("texts", [])
            signboard_results_stable = stable_detection.get("signboards", [])
            step_detected = stable_detection.get("step_detected", step_detected)
            hazards_detected_stable = stable_detection.get(
                "hazards", hazards_detected
            )

            # ===== 视觉-语言融合 =====
            voice_command = request.form.get("voice_command")
            fusion_decision = None
            if voice_command and visual_language_fusion:
                try:
                    fusion_input = {
                        "objects": [
                            {
                                "class": obj.get("class", ""),
                                "bbox": obj.get("bbox", (0, 0, 0, 0)),
                                "confidence": obj.get("confidence", 0.0),
                            }
                            for obj in stable_detection.get("objects", [])
                        ],
                        "texts": [
                            text.get("text", "")
                            for text in stable_detection.get("texts", [])
                        ],
                        "signboards": signboard_results_stable,
                    }
                    if hasattr(visual_language_fusion, 'fuse'):
                        fusion_decision = visual_language_fusion.fuse(
                            fusion_input, voice_command
                        )
                except Exception:
                    fusion_decision = None

            # ===== 生成导航指引 =====
            guidance_messages: List[str] = []
            guidance_direction = "forward"

            ocr_texts = [r.get("text", "") for r in vision_results.get("ocr_results", [])]
            all_text = " ".join(ocr_texts).lower()

            if fusion_decision:
                guidance_direction = fusion_decision.get("direction", "forward")
                msg = fusion_decision.get("message")
                if msg:
                    guidance_messages.append(msg)
            else:
                if any(k in all_text for k in ["左", "left", "←"]):
                    guidance_direction = "left"
                    guidance_messages.append("检测到左侧标识，请向左转。")
                elif any(k in all_text for k in ["右", "right", "→"]):
                    guidance_direction = "right"
                    guidance_messages.append("检测到右侧标识，请向右转。")
                elif any(k in all_text for k in ["直行", "straight", "forward", "↑"]):
                    guidance_direction = "forward"
                    guidance_messages.append("请直行。")

                # 台阶 / 危险补充
                if step_detected:
                    guidance_messages.append("前方有台阶，请注意脚下。")
                if hazards_detected_stable:
                    guidance_messages.append("前方存在潜在危险，请放慢速度。")

            # 回落：如果没有任何文案
            if not guidance_messages:
                guidance_messages.append("前方环境正常，请按当前方向继续行走。")

            latency_ms = (time.time() - start_time) * 1000.0

            return api_success(
                {
                    "direction": guidance_direction,
                    "messages": guidance_messages,
                    "vision": {
                        "detections": vision_results.get("detections", []),
                        "ocr_results": vision_results.get("ocr_results", []),
                        "roi_optimized": vision_results.get("roi_optimized", False),
                    },
                    "nodes": detected_nodes,
                    "latency_ms": latency_ms,
                }
            )
        except Exception as e:
            if log_manager:
                try:
                    log_manager.log_system_event(
                        event="visual_guidance_error",
                        metadata={
                            "exception_type": type(e).__name__,
                            "exception_message": str(e),
                        },
                    )
                except Exception:
                    pass
            return api_error(
                "NAV_VISUAL_GUIDANCE_FAILED",
                details={"exception_type": type(e).__name__, "exception_message": str(e)},
            )

    return bp
