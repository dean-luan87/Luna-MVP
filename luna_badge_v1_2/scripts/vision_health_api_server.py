"""
Vision Health API Server: 独立的视觉健康 API 服务

提供 HTTP API 接口用于查询模型健康状态。
可以独立运行，也可以集成到主服务器中。
"""

import sys
import os

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from flask import Flask, jsonify, Blueprint
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    print("警告: Flask 未安装，HTTP API 功能不可用。请运行: pip install flask")

from core.vision.vision_debug_service import VisionDebugService
from core.vision.multi_model_engine import MultiModelEngine

# 全局变量（在实际应用中，这些应该从应用初始化时注入）
_engine: MultiModelEngine = None
_debug_service: VisionDebugService = None


def init_vision_debug_service(engine: MultiModelEngine) -> None:
    """
    初始化视觉调试服务。

    Args:
        engine: MultiModelEngine 实例
    """
    global _engine, _debug_service
    _engine = engine
    _debug_service = VisionDebugService(engine)


def create_vision_debug_blueprint() -> Blueprint:
    """
    创建视觉调试 Blueprint（用于 Flask 应用）。

    Returns:
        Blueprint: Flask Blueprint 实例
    """
    if not FLASK_AVAILABLE:
        raise ImportError("Flask 未安装，无法创建 Blueprint")

    vision_debug_bp = Blueprint("vision_debug", __name__)

    @vision_debug_bp.route("/vision/health", methods=["GET"])
    def get_vision_health():
        """
        返回可直接在前端绘制模型健康图的 JSON。

        Returns:
            JSON 响应
        """
        if _debug_service is None:
            return jsonify({"ok": False, "error": "debug_service_not_initialized"}), 500

        snapshot = _debug_service.get_health().to_dict()
        return jsonify({"ok": True, "data": snapshot})

    @vision_debug_bp.route("/vision/health/<task_type>", methods=["GET"])
    def get_vision_health_by_type(task_type: str):
        """
        获取特定任务类型的模型健康。

        Args:
            task_type: 任务类型（如 'detect', 'ocr'）

        Returns:
            JSON 响应
        """
        if _debug_service is None:
            return jsonify({"ok": False, "error": "debug_service_not_initialized"}), 500

        model_block = _debug_service.get_model_block(task_type)
        if model_block is None:
            return jsonify({"ok": False, "error": f"task_type '{task_type}' not found"}), 404

        return jsonify({"ok": True, "data": model_block})

    return vision_debug_bp


def create_standalone_app(engine: MultiModelEngine) -> Flask:
    """
    创建独立的 Flask 应用（用于测试或独立运行）。

    Args:
        engine: MultiModelEngine 实例

    Returns:
        Flask: Flask 应用实例
    """
    if not FLASK_AVAILABLE:
        raise ImportError("Flask 未安装，无法创建 Flask 应用")

    app = Flask(__name__)

    # 初始化服务
    init_vision_debug_service(engine)

    # 注册路由
    blueprint = create_vision_debug_blueprint()
    app.register_blueprint(blueprint, url_prefix="/api/debug")

    return app


if __name__ == "__main__":
    """
    独立运行模式：创建一个简单的测试引擎并启动 HTTP 服务。
    """
    if not FLASK_AVAILABLE:
        print("错误: Flask 未安装。请运行: pip install flask")
        sys.exit(1)

    from core.vision.multi_model_engine import ModelSpec
    from core.vision.vision_task_orchestrator import VisionTask

    # 创建测试引擎
    engine = MultiModelEngine(max_workers=4)

    def fake_runner(task: VisionTask):
        return [{"label": "person", "score": 0.8}]

    engine.register_model("detect", ModelSpec(name="test_model", runner=fake_runner, weight=1.0))

    # 创建并启动应用
    app = create_standalone_app(engine)

    print("=== Vision Health API Server ===")
    print("访问地址:")
    print("  - GET http://localhost:8082/api/debug/vision/health")
    print("  - GET http://localhost:8082/api/debug/vision/health/detect")
    print("\n按 Ctrl+C 停止服务\n")

    app.run(host="0.0.0.0", port=8082, debug=False)

