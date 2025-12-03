from core.logging import get_logger

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
log = get_logger("mobile_bridge_server")
"""
Luna Badge 手机桥接服务器

功能：
- 接收手机端上传的图片
- 执行 YOLO 检测、导航规划、TTS 播报
- 返回结果和音频数据

使用方法：
    python3 mobile_bridge_server.py

然后在手机浏览器打开：
    http://你的电脑IP:8899/mobile_client.html
"""

import os
import sys
import time
import base64
import io
import socket
from pathlib import Path
from typing import Dict, Any, Optional

import numpy as np
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# 设置静态文件目录
app = Flask(__name__, static_folder="static", static_url_path="/static")
CORS(app)  # 允许跨域请求

# 添加项目根目录到路径
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# 导入核心模块
try:
    from core.yolo_detector import YoloDetector
except ImportError as e:
    log.error(f"[ERROR] 无法导入 YoloDetector: {e}")
    YoloDetector = None

try:
    from core.navigation_logic_v1_3 import NavigationLogicV1_3 as NavigationLogic
except ImportError:
    try:
        from core.navigation_logic import NavigationLogic
    except ImportError:
        NavigationLogic = None

try:
    from core.tts_manager import TTSManager
except ImportError:
    TTSManager = None

try:
    import cv2
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    log.warning("[WARN] PIL 未安装，无法处理图片")

# Flask app 已在上面定义

# 全局实例
yolo_detector: Optional[YoloDetector] = None
nav_logic: Optional[Any] = None
tts_manager: Optional[Any] = None


def init_modules():
    """初始化所有模块"""
    global yolo_detector, nav_logic, tts_manager
    
    log.info("[INFO] 正在初始化模块...")
    
    # 初始化 YOLO
    if YoloDetector is not None:
        try:
            yolo_detector = YoloDetector()
            log.info("[INFO] ✅ YOLO11-tiny 检测器初始化成功")
        except Exception as e:
            log.warning(f"[WARN] YOLO 初始化失败: {e}")
            yolo_detector = None
    else:
        log.warning("[WARN] YoloDetector 不可用")
    
    # 初始化导航逻辑
    if NavigationLogic is not None:
        try:
            nav_logic = NavigationLogic()
            log.info("[INFO] ✅ 导航逻辑初始化成功")
        except Exception as e:
            log.warning(f"[WARN] 导航逻辑初始化失败: {e}")
            nav_logic = None
    else:
        log.warning("[WARN] NavigationLogic 不可用")
    
    # 初始化 TTS
    if TTSManager is not None:
        try:
            tts_manager = TTSManager(mode="normal")
            log.info("[INFO] ✅ TTS 管理器初始化成功")
        except Exception as e:
            log.warning(f"[WARN] TTS 初始化失败: {e}")
            tts_manager = None
    else:
        log.warning("[WARN] TTSManager 不可用")
    
    log.info("[INFO] 模块初始化完成")


def get_local_ip() -> str:
    """获取本机 IP 地址"""
    try:
        # 连接到一个远程地址（不实际发送数据）
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def base64_to_numpy(image_base64: str) -> np.ndarray:
    """将 base64 编码的图片转换为 numpy array"""
    if not PIL_AVAILABLE:
        raise RuntimeError("PIL 未安装，无法处理图片")
    
    # 移除 data:image/xxx;base64, 前缀（如果有）
    if "," in image_base64:
        image_base64 = image_base64.split(",")[1]
    
    # 解码 base64
    image_bytes = base64.b64decode(image_base64)
    
    # 转换为 PIL Image
    image = Image.open(io.BytesIO(image_bytes))
    
    # 转换为 RGB（如果需要）
    if image.mode != "RGB":
        image = image.convert("RGB")
    
    # 转换为 numpy array (BGR for OpenCV)
    img_array = np.array(image)
    if cv2 is not None:
        img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    
    return img_array


def generate_tts_audio(text: str) -> Optional[str]:
    """生成 TTS 音频（返回 base64 编码的音频数据）"""
    if not text or not text.strip():
        return None
    
    try:
        # 使用 edge-tts 生成音频
        import edge_tts
        import asyncio
        
        async def _generate():
            communicate = edge_tts.Communicate(
                text=text,
                voice="zh-CN-XiaoxiaoNeural"  # 中文语音
            )
            audio_data = b""
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_data += chunk["data"]
            return audio_data
        
        # 运行异步函数
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        audio_bytes = loop.run_until_complete(_generate())
        
        if audio_bytes:
            # 返回 base64 编码的音频数据
            return base64.b64encode(audio_bytes).decode("utf-8")
        else:
            return None
    except ImportError:
        # edge-tts 未安装，尝试使用系统 TTS
        log.warning("[WARN] edge-tts 未安装，TTS 功能受限")
        if tts_manager is not None and hasattr(tts_manager, "speak_sync"):
            tts_manager.speak_sync(text)
        return None
    except Exception as e:
        log.warning(f"[WARN] TTS 生成失败: {e}")
        return None


@app.route("/")
def index():
    """首页"""
    return """
    <html>
    <head><title>Luna Badge Mobile Bridge</title></head>
    <body>
        <h1>Luna Badge Mobile Bridge Server v1.3.1</h1>
        <p>服务器运行中...</p>
        <p><a href="/static/mobile_client.html">打开手机客户端</a></p>
        <p>API 端点：</p>
        <ul>
            <li><code>POST /api/detect</code> - YOLO 检测</li>
            <li><code>POST /api/nav</code> - 导航规划</li>
            <li><code>POST /api/full_pipeline</code> - 完整链路</li>
        </ul>
        <p>WebSocket 服务：<code>ws://你的IP:8898/ws</code></p>
    </body>
    </html>
    """


@app.route("/health")
def health():
    """健康检查"""
    return jsonify({"status": "ok"})

@app.route("/mobile_client.html")
def mobile_client():
    """返回手机客户端页面（兼容旧路径）"""
    return send_from_directory("static", "mobile_client.html")


@app.route("/api/detect", methods=["POST"])
def api_detect():
    """YOLO 检测 API"""
    if yolo_detector is None:
        return jsonify({"error": "YOLO 检测器未初始化"}), 500
    
    try:
        data = request.json
        if "image" not in data:
            return jsonify({"error": "缺少 image 参数"}), 400
        
        # 转换图片
        img_array = base64_to_numpy(data["image"])
        
        # 执行检测
        t0 = time.perf_counter()
        result = yolo_detector.detect(img_array)
        t1 = time.perf_counter()
        
        return jsonify({
            "success": True,
            "detections": result.get("detections", []),
            "meta": result.get("meta", {}),
            "detect_ms": round((t1 - t0) * 1000, 2),
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/nav", methods=["POST"])
def api_nav():
    """导航规划 API"""
    if nav_logic is None:
        return jsonify({"error": "导航逻辑未初始化"}), 500
    
    try:
        data = request.json
        detections = data.get("detections", [])
        
        # 构建视觉结果
        vision_result = {
            "detections": detections,
            "objects": detections,
        }
        
        # 执行导航规划
        t0 = time.perf_counter()
        if hasattr(nav_logic, "plan_route"):
            nav_result = nav_logic.plan_route(
                vision_result=vision_result,
                ground_state={"state": "safe"},
                dispatch_result={}
            )
        elif hasattr(nav_logic, "step"):
            nav_result = nav_logic.step(vision_result)
        else:
            nav_result = {"message": "前方环境正常，可以继续前进。"}
        t1 = time.perf_counter()
        
        return jsonify({
            "success": True,
            "nav_result": nav_result,
            "nav_ms": round((t1 - t0) * 1000, 2),
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/full_pipeline", methods=["POST"])
def api_full_pipeline():
    """完整链路 API：检测 + 导航 + TTS"""
    if yolo_detector is None:
        return jsonify({"error": "YOLO 检测器未初始化"}), 500
    
    try:
        data = request.json
        if "image" not in data:
            return jsonify({"error": "缺少 image 参数"}), 400
        
        total_t0 = time.perf_counter()
        
        # 1. 转换图片
        img_t0 = time.perf_counter()
        img_array = base64_to_numpy(data["image"])
        img_t1 = time.perf_counter()
        
        # 2. YOLO 检测
        det_t0 = time.perf_counter()
        det_result = yolo_detector.detect(img_array)
        det_t1 = time.perf_counter()
        
        detections = det_result.get("detections", [])
        vision_result = {
            "detections": detections,
            "objects": detections,
        }
        
        # 3. 导航规划
        nav_t0 = time.perf_counter()
        if nav_logic is not None:
            if hasattr(nav_logic, "plan_route"):
                nav_result = nav_logic.plan_route(
                    vision_result=vision_result,
                    ground_state={"state": "safe"},
                    dispatch_result={}
                )
            elif hasattr(nav_logic, "step"):
                nav_result = nav_logic.step(vision_result)
            else:
                nav_result = {"message": "前方环境正常，可以继续前进。"}
        else:
            nav_result = {"message": "前方环境正常，可以继续前进。"}
        nav_t1 = time.perf_counter()
        
        # 4. TTS 生成
        tts_t0 = time.perf_counter()
        instruction = nav_result.get("message") or nav_result.get("instruction", "前方环境正常")
        audio_base64 = generate_tts_audio(instruction)
        tts_t1 = time.perf_counter()
        
        total_t1 = time.perf_counter()
        
        return jsonify({
            "success": True,
            "detections": detections,
            "nav_result": nav_result,
            "audio": audio_base64,
            "timing": {
                "image_ms": round((img_t1 - img_t0) * 1000, 2),
                "detect_ms": round((det_t1 - det_t0) * 1000, 2),
                "nav_ms": round((nav_t1 - nav_t0) * 1000, 2),
                "tts_ms": round((tts_t1 - tts_t0) * 1000, 2),
                "total_ms": round((total_t1 - total_t0) * 1000, 2),
            },
        })
    except Exception as e:
        import traceback
        return jsonify({
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500


if __name__ == "__main__":
    log.info("\n" + "=" * 70")
    log.info("Luna Badge Mobile Bridge Server")
    log.info("=" * 70")
    
    # 初始化模块
    init_modules()
    
    # 获取本机 IP
    local_ip = get_local_ip()
    port = 8899
    
    log.info(f"\n[INFO] 服务器启动中...")
    log.info(f"[INFO] 本机 IP: {local_ip}")
    log.info(f"[INFO] 端口: {port}")
    log.info(f"\n[INFO] 手机端访问地址:")
    log.info(f"  http://{local_ip}:{port}/mobile_client.html")
    log.info(f"\n[INFO] 按 Ctrl+C 停止服务器")
    log.info("=" * 70 + "\n")
    
    # 启动服务器
    app.run(host="0.0.0.0", port=port, debug=False, threaded=True)

