import base64
import io
import json
import time
import threading
import sys
from pathlib import Path
from typing import List, Dict

from flask import Flask, jsonify
from flask_sock import Sock
from PIL import Image

# 添加项目根目录到路径（用于导入 core 模块）
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

# 使用新的统一 YOLO 加载器
try:
    from core.yolo_detector import YoloDetector
    print("[MODEL] 初始化 YOLO 检测器...")
    detector = YoloDetector()
    print("[MODEL] ✅ YOLO 检测器初始化成功")
    USE_NEW_MODEL_SYSTEM = True
    model = None  # 不再使用旧的 ultralytics 直接加载
except Exception as e:
    print(f"[MODEL] ⚠️ YOLO 检测器初始化失败: {e}")
    print("[MODEL] 回退到 stub 模式")
    USE_NEW_MODEL_SYSTEM = False
    detector = None
    model = None

app = Flask(__name__)
sock = Sock(app)

# 简单的运行状态
stats = {
    "total_frames": 0,
    "avg_latency_ms": 0.0,
    "last_latency_ms": 0.0,
    "last_error": None,
}

# -------------------------
# 工具函数
# -------------------------

def decode_image(b64_data: str) -> Image.Image:
    # dataURL: "data:image/jpeg;base64,...."
    if "," in b64_data:
        b64_data = b64_data.split(",", 1)[1]
    img_bytes = base64.b64decode(b64_data)
    return Image.open(io.BytesIO(img_bytes)).convert("RGB")


def run_yolo(img: Image.Image) -> List[Dict]:
    """运行 YOLO 检测，返回简化后的对象列表"""
    import numpy as np
    
    # 使用新的统一 YOLO 检测器
    if USE_NEW_MODEL_SYSTEM and detector is not None:
        try:
            # 转换为 numpy array（ultralytics 支持 PIL Image）
            img_array = np.array(img)
            result = detector.detect(img_array)
            
            # 转换格式（兼容前端期望的格式）
            objects = []
            for box in result.boxes:
                objects.append({
                    "cls": box.get("cls", "unknown"),
                    "conf": box.get("conf", 0.0),
                    "x1": int(box.get("x1", 0)),
                    "y1": int(box.get("y1", 0)),
                    "x2": int(box.get("x2", 0)),
                    "y2": int(box.get("y2", 0)),
                })
            return objects
        except Exception as e:
            print(f"[ERROR] YOLO 检测失败: {e}")
            import traceback
            traceback.print_exc()
            # 返回空列表而不是 stub，让前端知道检测失败
            return []
    
    # Stub 模式：返回模拟检测结果（仅当检测器未初始化时）
    print("[WARN] 使用 stub 模式（检测器未初始化）")
    return [
        {
            "cls": "person",
            "conf": 0.75,
            "x1": 100,
            "y1": 100,
            "x2": 200,
            "y2": 300,
        }
    ]


# -------------------------
# HTTP 健康检查
# -------------------------

@app.route("/health")
def health():
    model_info = {
        "model": "unknown",
        "model_system": "legacy"
    }
    
    if USE_NEW_MODEL_SYSTEM:
        try:
            from core.model_registry import ModelRegistry
            current_model = ModelRegistry.get_current_nav_model()
            model_info = {
                "model": current_model,
                "model_system": "registry",
                "model_path": str(ModelRegistry.get_model_path(current_model)),
                "model_exists": ModelRegistry.model_exists(current_model),
                "detector_loaded": detector is not None
            }
        except Exception as e:
            model_info["error"] = str(e)
    else:
        model_info["model"] = "unknown"
    
    return jsonify(
        {
            "status": "ok",
            **model_info,
            "total_frames": stats["total_frames"],
            "avg_latency_ms": stats["avg_latency_ms"],
            "last_latency_ms": stats["last_latency_ms"],
            "last_error": stats["last_error"],
        }
    )

@app.route("/api/model/info")
def get_model_info():
    """获取模型信息 API（供前端使用）"""
    try:
        from core.model_registry import ModelRegistry
        return jsonify({
            "current_nav_model": ModelRegistry.get_current_nav_model(),
            "current_fast_model": ModelRegistry.get_current_fast_model(),
            "models": ModelRegistry.list_models(),
            "detector_status": "loaded" if (USE_NEW_MODEL_SYSTEM and detector is not None) else "not_loaded"
        })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "current_nav_model": None,
            "current_fast_model": None,
            "models": {},
            "detector_status": "error"
        })


# -------------------------
# WebSocket 主通道
# -------------------------

@sock.route("/ws")
def ws_main(ws):
    """
    协议：
    前端 -> 后端：
      { "type": "frame", "data": "<dataurl>", "ts": <performance.now 毫秒> }

    后端 -> 前端：
      {
        "type": "result",
        "latency": <后端推理耗时ms>,
        "objects": [...],
        "server_ts": <服务器时间戳>,
        "frame_id": <累积帧编号>
      }

    心跳（可选）：
      浏览器 -> { "type": "ping" }
      服务器 -> { "type": "pong", "server_ts": ... }
    """
    import sys
    print("[WS] ========== WebSocket 客户端连接 ==========", flush=True)
    print(f"[WS] 客户端地址: {ws.remote_address if hasattr(ws, 'remote_address') else 'unknown'}", flush=True)
    sys.stdout.flush()

    try:
        while True:
            msg = ws.receive()
            if msg is None:
                print("[WS] client disconnected")
                break

            try:
                data = json.loads(msg)
            except Exception as e:
                print("[WS] invalid json:", e)
                continue

            msg_type = data.get("type")

            if msg_type == "ping":
                ws.send(
                    json.dumps(
                        {"type": "pong", "server_ts": time.time()}
                    )
                )
                continue

            if msg_type != "frame":
                # 无效类型，忽略
                continue

            # 处理图像帧
            print(f"[WS] 收到帧数据，开始处理...", flush=True)
            t0 = time.time()
            try:
                img = decode_image(data["data"])
                print(f"[WS] 图像解码成功，尺寸: {img.size}", flush=True)
                objects = run_yolo(img)
                print(f"[WS] YOLO 检测完成，发现 {len(objects)} 个对象", flush=True)
                t1 = time.time()
                latency_ms = (t1 - t0) * 1000.0

                # 更新统计
                stats["total_frames"] += 1
                stats["last_latency_ms"] = latency_ms
                # 指数滑动平均，避免抖动
                alpha = 0.1
                stats["avg_latency_ms"] = (
                    (1 - alpha) * stats["avg_latency_ms"] + alpha * latency_ms
                    if stats["total_frames"] > 1
                    else latency_ms
                )
                stats["last_error"] = None

                resp = {
                    "type": "result",
                    "latency": round(latency_ms, 2),
                    "objects": objects,
                    "server_ts": t1,
                    "frame_id": stats["total_frames"],
                }
                ws.send(json.dumps(resp))

            except Exception as e:
                print(f"[WS] ERROR: 处理帧时出错: {e}", flush=True)
                import traceback
                traceback.print_exc()
                stats["last_error"] = repr(e)
                try:
                    ws.send(
                        json.dumps(
                            {
                                "type": "error",
                                "error": str(e),
                                "server_ts": time.time(),
                            }
                        )
                    )
                except:
                    pass

    except Exception as e:
        print(f"[WS] ERROR: 连接错误: {e}", flush=True)
        import traceback
        traceback.print_exc()


# -------------------------
# 独立启动
# -------------------------

def run_server(host="0.0.0.0", port=5001, ssl_keyfile=None, ssl_certfile=None):
    protocol = "https" if ssl_keyfile and ssl_certfile else "http"
    print(f"[SERVER] starting at {protocol}://{host}:{port}")
    
    if ssl_keyfile and ssl_certfile:
        app.run(host=host, port=port, debug=False, ssl_context=(ssl_certfile, ssl_keyfile))
    else:
        app.run(host=host, port=port, debug=False)


if __name__ == "__main__":
    import sys
    import os
    from pathlib import Path
    
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5001
    
    # 检查是否有 SSL 证书
    script_dir = Path(__file__).parent
    ssl_dir = script_dir.parent / "ssl_certs"
    ssl_keyfile = ssl_dir / "key.pem"
    ssl_certfile = ssl_dir / "cert.pem"
    
    if ssl_keyfile.exists() and ssl_certfile.exists():
        print(f"[SERVER] 使用 HTTPS (SSL 证书已找到)")
        run_server(port=port, ssl_keyfile=str(ssl_keyfile), ssl_certfile=str(ssl_certfile))
    else:
        print(f"[SERVER] 使用 HTTP (未找到 SSL 证书)")
        print(f"[SERVER] 提示: 运行 'bash scripts/generate_ssl_cert.sh' 生成证书以支持 HTTPS")
        run_server(port=port)

