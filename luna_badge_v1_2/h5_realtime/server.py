#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
H5 实时推理服务器（Flask + WebSocket）

支持 YOLOv11-tiny 实时推理
符合 Luna Badge 协议规范
"""

import base64
import time
import io
import json
from pathlib import Path

from flask import Flask, send_from_directory
from flask_sock import Sock

try:
    from PIL import Image
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False
    print("[WARN] ultralytics 未安装，使用 stub 推理")

# 导入协议库
try:
    from protocol.parser import parse_message, ProtocolError, create_error_response
    from protocol.builder import build_infer_result, build_heartbeat_ack, build_error
    PROTOCOL_AVAILABLE = True
except ImportError:
    PROTOCOL_AVAILABLE = False
    print("[WARN] 协议库未找到，使用旧版消息格式")

app = Flask(__name__, static_folder=".")
sock = Sock(app)

# 全局模型实例
model = None

def load_model(model_path="yolo11n.pt"):
    """加载 YOLO 模型"""
    global model
    
    if not YOLO_AVAILABLE:
        print("[WARN] ultralytics 未安装，使用 stub 推理")
        return None
    
    try:
        # 尝试多个可能的路径
        possible_paths = [
            model_path,
            f"weights/{model_path}",
            f"models/{model_path}",
            "yolo11n.pt",  # ultralytics 会自动下载
        ]
        
        for path in possible_paths:
            try:
                print(f"[MODEL] 尝试加载: {path}")
                model = YOLO(path)
                print(f"[MODEL] ✅ 模型加载成功: {path}")
                return model
            except Exception as e:
                continue
        
        print("[WARN] 模型加载失败，使用 stub 推理")
        return None
    except Exception as e:
        print(f"[ERROR] 模型加载异常: {e}")
        return None

def decode_image(b64_data):
    """解码 Base64 图像"""
    if b64_data.startswith("data:"):
        b64_data = b64_data.split(",", 1)[1]
    
    img_bytes = base64.b64decode(b64_data)
    return Image.open(io.BytesIO(img_bytes))

def run_detection(img):
    """运行 YOLO 检测"""
    if model is None:
        # Stub 检测结果
        return [
            {
                "cls": "person",
                "conf": 0.75,
                "bbox": [100, 100, 200, 300]
            }
        ], 5.0
    
    t0 = time.time()
    results = model(img)[0]
    det_ms = (time.time() - t0) * 1000.0
    
    detections = []
    for box in results.boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        detections.append({
            "cls": results.names[int(box.cls)],
            "conf": float(box.conf),
            "bbox": [int(x1), int(y1), int(x2), int(y2)]
        })
    
    return detections, det_ms

def run_navigation(detections):
    """运行导航决策（模拟）"""
    t0 = time.time()
    
    # 简单的导航逻辑
    nav_result = {
        "decision": "straight",
        "danger_level": 0,
        "text": "前方环境正常"
    }
    
    # 如果检测到人，建议减速
    if any(d.get("cls") == "person" for d in detections):
        nav_result = {
            "decision": "slow_down",
            "danger_level": 1,
            "text": "检测到行人，请减速"
        }
    
    nav_ms = (time.time() - t0) * 1000.0
    return nav_result, nav_ms

@app.route("/")
def index():
    """提供 index.html"""
    return send_from_directory(".", "index.html")

@app.route("/<path:filename>")
def static_files(filename):
    """提供静态文件"""
    return send_from_directory(".", filename)

@sock.route("/ws")
def ws_handler_legacy(ws):
    """WebSocket 处理函数（兼容路径）"""
    return ws_handler(ws)

@sock.route("/ws_json")
def ws_handler(ws):
    """WebSocket 处理函数"""
    client = f"{ws.remote_address[0]}:{ws.remote_address[1]}"
    print(f"[WS] 客户端连接: {client}")
    
    frame_count = 0
    
    try:
        while True:
            msg = ws.receive()
            if msg is None:
                break
            
            try:
                data = json.loads(msg)
            except json.JSONDecodeError as e:
                error_resp = build_error("PROTO-002", detail=f"JSON 解析失败: {e}") if PROTOCOL_AVAILABLE else {
                    "type": "error",
                    "message": f"JSON 解析失败: {e}"
                }
                ws.send(json.dumps(error_resp))
                continue
            
            # 使用协议库解析消息
            if PROTOCOL_AVAILABLE:
                try:
                    msg_type, parsed_data = parse_message(msg)
                    
                    if msg_type == "heartbeat":
                        # 心跳确认
                        ack = build_heartbeat_ack(
                            seq=parsed_data["seq"],
                            client_ts=parsed_data["client_ts"]
                        )
                        ws.send(json.dumps(ack))
                        continue
                    
                    elif msg_type == "frame":
                        data = parsed_data
                        msg_type = "frame"
                
                except ProtocolError as e:
                    error_resp = create_error_response("PROTO-002", detail=str(e))
                    ws.send(json.dumps(error_resp))
                    continue
            
            # 处理帧数据
            if data.get("type") == "frame":
                t0 = time.time()
                frame_id = data.get("frame_id", 0)
                client_ts = data.get("client_ts") or data.get("ts", time.time() * 1000)
                img_b64 = data.get("image_base64") or data.get("image") or data.get("data")
                
                if not img_b64:
                    error_resp = build_error("CAM-002", detail="缺少图像数据") if PROTOCOL_AVAILABLE else {
                        "type": "error",
                        "message": "缺少图像数据"
                    }
                    ws.send(json.dumps(error_resp))
                    continue
                
                try:
                    # 解码图像
                    img = decode_image(img_b64)
                    
                    # 运行检测
                    detections, infer_ms = run_detection(img)
                    
                    # 运行导航
                    nav_result, nav_ms = run_navigation(detections)
                    
                    frame_count += 1
                    
                    # 构建响应
                    if PROTOCOL_AVAILABLE:
                        result = build_infer_result(
                            frame_id=frame_id,
                            client_ts=client_ts,
                            infer_ms=infer_ms,
                            nav_ms=nav_ms,
                            objects=detections,
                            nav=nav_result
                        )
                        result["ts_server_send"] = int(time.time() * 1000)
                    else:
                        # 兼容旧版格式
                        result = {
                            "type": "result",
                            "frame_id": frame_id,
                            "latency": int((time.time() - t0) * 1000),
                            "det_ms": infer_ms,
                            "nav_ms": nav_ms,
                            "objects": detections,
                            "nav": nav_result
                        }
                    
                    ws.send(json.dumps(result, ensure_ascii=False))
                    
                    if frame_count % 10 == 0:
                        print(f"[WS] 已处理 {frame_count} 帧，平均推理: {infer_ms:.1f}ms")
                
                except Exception as e:
                    error_resp = build_error("INF-001", detail=str(e)) if PROTOCOL_AVAILABLE else {
                        "type": "error",
                        "message": f"推理失败: {e}"
                    }
                    ws.send(json.dumps(error_resp))
                    print(f"[ERROR] 推理异常: {e}")
    
    except Exception as e:
        print(f"[ERROR] WebSocket 异常: {e}")
    finally:
        print(f"[WS] 客户端断开: {client}")

if __name__ == "__main__":
    # 加载模型
    load_model()
    
    # 启动服务器
    print("[SERVER] 启动 Flask + WebSocket 服务器...")
    print("[SERVER] 访问地址: http://0.0.0.0:5000")
    print("[SERVER] WebSocket: ws://0.0.0.0:5000/ws")
    
    app.run(host="0.0.0.0", port=5000, debug=False)

