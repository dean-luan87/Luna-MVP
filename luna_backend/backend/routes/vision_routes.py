# backend/routes/vision_routes.py
from flask import Blueprint, request, jsonify
from core.response import api_success, api_error
from config.error_codes import get_error_spec

from backend.vision.scene_description_engine import SceneDescriptionEngine

bp_vision = Blueprint("vision", __name__, url_prefix="/api/vision")

# 全局实例（将在初始化时注入）
scene_engine = None
yolo_detector = None


def init_vision_routes(detector, engine=None):
    """初始化视觉路由（从web_test_server.py调用）"""
    global scene_engine, yolo_detector
    yolo_detector = detector
    if engine is None:
        scene_engine = SceneDescriptionEngine(detector)
    else:
        scene_engine = engine


@bp_vision.route("/describe_scene", methods=["POST"])
def describe_scene():
    """
    输入 base64 图片 → 输出场景描述
    """
    try:
        data = request.get_json() or {}
        image_b64 = data.get("image")

        if not image_b64:
            return api_error("VISION_IMAGE_MISSING")

        if not yolo_detector:
            return api_error("VISION_ENGINE_NOT_INITIALIZED")

        # 加载图像
        try:
            if hasattr(yolo_detector, 'load_image'):
                frame = yolo_detector.load_image(image_b64)
            else:
                # 使用utils.image_utils
                from utils.image_utils import decode_base64_image
                frame = decode_base64_image(image_b64)
        except Exception as e:
            return api_error("VISION_IMAGE_DECODE_FAILED", details={"error": str(e)})

        if frame is None:
            return api_error("VISION_IMAGE_DECODE_FAILED")

        # 生成场景描述
        result = scene_engine.describe(frame)

        if not result.get("success"):
            return api_error("VISION_PROCESSING_FAILED", details={"error": result.get("error")})

        return api_success({
            "objects": result.get("objects", []),
            "summary": result.get("summary", ""),
            "scene_type": result.get("scene_type", "unknown"),
            "environment": result.get("environment", {}),
            "timestamp": result.get("timestamp")
        })
    except Exception as e:
        return api_error("VISION_PROCESSING_FAILED", details={"exception": str(e)})



