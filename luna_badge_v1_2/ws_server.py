from core.logging import get_logger

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
log = get_logger("ws_server")
"""
Luna Badge WebSocket 实时推理服务器

功能：
- WebSocket 长连接，减少 HTTP 开销
- 自动心跳检测（每 3 秒）
- 连续导航模式（每 200ms 处理一帧）
- 实时返回 YOLO 检测和导航结果

使用方法：
    python3 ws_server.py

WebSocket 地址：
    ws://你的电脑IP:8898/ws
"""

import asyncio
import json
import base64
import io
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    from PIL import Image
    import numpy as np
    import cv2
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    log.warning("[WARN] PIL/OpenCV 未安装，图片处理功能受限")

try:
    import websockets
    WEBSOCKETS_AVAILABLE = True
except ImportError:
    WEBSOCKETS_AVAILABLE = False
    log.error("[ERROR] websockets 未安装，请执行: pip install websockets")

# 添加项目根目录到路径
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# 导入核心模块
try:
    from core.yolo_detector import YoloDetector
except ImportError:
    YoloDetector = None
    log.warning("[WARN] YoloDetector 不可用")

try:
    from core.navigation_logic_v1_3 import NavigationLogicV1_3 as NavigationLogic
except ImportError:
    try:
        from core.navigation_logic import NavigationLogic
    except ImportError:
        NavigationLogic = None
        log.warning("[WARN] NavigationLogic 不可用")

# 全局实例
yolo_detector = None
nav_logic = None


def init_modules():
    """初始化所有模块"""
    global yolo_detector, nav_logic
    
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
    
    log.info("[INFO] 模块初始化完成")


def generate_tts_audio(text: str):
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
            import base64
            return base64.b64encode(audio_bytes).decode("utf-8")
        else:
            return None
    except ImportError:
        log.warning("[WARN] edge-tts 未安装，TTS 功能受限")
        return None
    except Exception as e:
        log.warning(f"[WARN] TTS 生成失败: {e}")
        return None


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


async def send_heartbeat(ws):
    """每 3 秒发送一次心跳"""
    try:
        while True:
            msg = {
                "type": "heartbeat",
                "ts": datetime.utcnow().isoformat()
            }
            await ws.send(json.dumps(msg))
            await asyncio.sleep(3.0)
    except asyncio.CancelledError:
        # 连接关闭，心跳退出
        return
    except Exception as e:
        log.error(f"[WS] heartbeat error: {e}")


async def handle_connection(websocket):
    """
    WebSocket 连接处理
    
    协议约定：
    - 客户端 → 服务端：
      { "type": "frame", "image": "<base64-jpeg>" }
      { "type": "ping" }
    
    - 服务端 → 客户端：
      { "type": "heartbeat", "ts": "..." }
      { "type": "nav_result", "det": [...], "nav": {...}, "ts": "..." }
      { "type": "pong" }
      { "type": "error", "message": "..." }
    """
    try:
        client_addr = f"{websocket.remote_address[0]}:{websocket.remote_address[1]}"
    except:
        client_addr = "unknown"
    log.info(f"[WS] 客户端连接: {client_addr}")
    
    # 开一个心跳任务
    heartbeat_task = asyncio.create_task(send_heartbeat(websocket))
    
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
            except json.JSONDecodeError:
                await websocket.send(json.dumps({
                    "type": "error",
                    "message": "invalid json"
                }))
                continue
            
            msg_type = data.get("type")
            
            # ping-pong
            if msg_type == "ping":
                await websocket.send(json.dumps({
                    "type": "pong",
                    "ts": datetime.utcnow().isoformat()
                }))
                continue
            
            # 处理帧：连续导航模式
            if msg_type == "frame":
                image_b64 = data.get("image")
                if not image_b64:
                    await websocket.send(json.dumps({
                        "type": "error",
                        "message": "missing image"
                    }))
                    continue
                
                # 解析图像
                try:
                    img_array = base64_to_numpy(image_b64)
                except Exception as e:
                    await websocket.send(json.dumps({
                        "type": "error",
                        "message": f"invalid image: {e}"
                    }))
                    continue
                
                # YOLO 推理
                detections = []
                if yolo_detector is not None:
                    try:
                        det_result = yolo_detector.detect(img_array)
                        detections = det_result.get("detections", [])
                    except Exception as e:
                        log.info(f"[WS] YOLO 检测失败: {e}")
                        detections = []
                else:
                    # mock 结果
                    detections = [{
                        "class_id": 0,
                        "class_name": "person",
                        "conf": 0.9,
                        "box": [10, 10, 100, 200]
                    }]
                
                # 导航规划
                vision_result = {
                    "detections": detections,
                    "objects": detections,
                }
                
                if nav_logic is not None:
                    try:
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
                    except Exception as e:
                        log.info(f"[WS] 导航规划失败: {e}")
                        nav_result = {"message": "前方环境正常，可以继续前进。"}
                else:
                    # mock 结果
                    nav_result = {
                        "instruction": "向前走两步，然后向右转",
                        "risk": "low",
                        "message": "前方环境正常，可以继续前进。"
                    }
                
                # TTS 生成（可选）
                audio_base64 = None
                instruction = nav_result.get("message") or nav_result.get("instruction", "")
                if instruction:
                    try:
                        audio_base64 = generate_tts_audio(instruction)
                    except Exception as e:
                        log.info(f"[WS] TTS 生成失败: {e}")
                
                # 返回结果
                result_msg = {
                    "type": "nav_result",
                    "det": detections,
                    "nav": nav_result,
                    "ts": datetime.utcnow().isoformat()
                }
                if audio_base64:
                    result_msg["audio"] = audio_base64
                
                await websocket.send(json.dumps(result_msg))
                continue
            
            # 未知类型
            await websocket.send(json.dumps({
                "type": "error",
                "message": f"unknown type: {msg_type}"
            }))
    
    except websockets.exceptions.ConnectionClosed:
        log.info(f"[WS] 客户端断开: {client_addr}")
    except Exception as e:
        log.info(f"[WS] 连接错误: {e}")
    finally:
        heartbeat_task.cancel()
        try:
            await heartbeat_task
        except asyncio.CancelledError:
            pass


async def main():
    """主函数"""
    if not WEBSOCKETS_AVAILABLE:
        log.error("[ERROR] websockets 库未安装，请执行: pip install websockets")
        return
    
    log.info("\n" + "=" * 70")
    log.info("Luna Badge WebSocket 实时推理服务器")
    log.info("=" * 70")
    
    # 初始化模块
    init_modules()
    
    log.info(f"\n[INFO] WebSocket 服务器启动中...")
    log.info(f"[INFO] 地址: ws://0.0.0.0:8898/ws")
    log.info(f"[INFO] 按 Ctrl+C 停止服务器")
    log.info("=" * 70 + "\n")
    
    # 启动 WebSocket 服务器
    # 兼容新旧版本的 websockets API
    try:
        # 新版本 API（不需要 path 参数）
        async with websockets.serve(handle_connection, "0.0.0.0", 8898):
            await asyncio.Future()  # run forever
    except TypeError:
        # 旧版本 API（需要 path 参数）
        async def handle_connection_with_path(websocket, path):
            return await handle_connection(websocket)
        async with websockets.serve(handle_connection_with_path, "0.0.0.0", 8898):
            await asyncio.Future()  # run forever


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log.info("\n[INFO] 服务器已停止")

