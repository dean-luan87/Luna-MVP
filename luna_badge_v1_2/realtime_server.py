# realtime_server.py

import io
import time
from typing import Dict, Any

import cv2
import numpy as np
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse

# 1.4.1-core: 接入新基础设施
from core.config.config_center import ConfigCenter
from core.logging.log_manager import LogManager
from core.health.metrics_collector import MetricsCollector

from core.yolo_detector import YoloDetector

# 初始化基础设施（如果还未初始化）
try:
    ConfigCenter.init(env="dev")
    LogManager.init()
except RuntimeError:
    pass  # 已经初始化过了

# 使用新的日志系统
log = LogManager.get_logger("realtime_server")

app = FastAPI(title="Luna Badge Realtime Nav API")

# CORS（方便手机 / 本机访问）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 测试阶段放开
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局 detector（进程级单例）
detector = YoloDetector()


@app.get("/health")
async def health() -> Dict[str, Any]:
    return {"status": "ok", "model": "yolo11_nav_tiny"}


@app.post("/api/frame")
async def process_frame(frame: UploadFile = File(...)) -> JSONResponse:
    """
    接收 H5 上传的一帧 JPEG/PNG，做目标检测，返回 boxes 和耗时。
    1.4.1-core: 已接入 Metrics 和日志系统
    """
    # 1.4.1-core: 使用 Metrics 记录总耗时
    with MetricsCollector.timeit("api.frame.total"):
        t0 = time.perf_counter()
        
        # 1.4.1-core: 记录帧接收
        MetricsCollector.incr("api.frame.received")
        
        content = await frame.read()

        # 解析成 RGB
        image_array = np.frombuffer(content, dtype=np.uint8)
        
        # 1.4.1-core: 记录图像解码耗时
        with MetricsCollector.timeit("api.frame.decode"):
            img_bgr = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        
        if img_bgr is None:
            MetricsCollector.incr("api.frame.decode_error")
            log.warning("无法解码图像")
            return JSONResponse(
                status_code=400,
                content={"error": "invalid_image", "message": "cannot decode image"},
            )

        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

        # 1.4.1-speed.4: 优先使用 SpeedContext 中的新鲜推理结果（非阻塞）
        from core.speed.speed_context import SpeedContext
        
        det_result = None
        boxes = []
        model_name = None
        
        # 检查推理结果是否新鲜（1.4.1-speed.4）
        if SpeedContext.is_yolo_fresh(max_age_sec=0.3):
            # 使用新线程推理结果
            det_result = SpeedContext.current_yolo_result
            model_name = SpeedContext.current_model_name
            if det_result is not None:
                if hasattr(det_result, 'to_dict'):
                    boxes = det_result.to_dict().get("boxes", [])
                elif isinstance(det_result, dict):
                    boxes = det_result.get("boxes", [])
                MetricsCollector.incr("api.frame.processed_from_speed")
        else:
            # 结果不新鲜或不存在，使用 Fallback
            with MetricsCollector.timeit("yolo.inference"):
                det_result = detector.detect(img_rgb)
                boxes = det_result.to_dict()["boxes"]
            MetricsCollector.incr("yolo.calls")
            MetricsCollector.incr("api.frame.processed_fallback")
        
        MetricsCollector.incr("api.frame.processed")

        t1 = time.perf_counter()
        latency_ms = (t1 - t0) * 1000.0

        resp = {
            "latency_ms": latency_ms,
            "box_count": len(boxes),
            "boxes": boxes,
        }

        log.debug(
            f"[FRAME] size={img_rgb.shape} boxes={len(boxes)} latency={latency_ms:.2f} ms"
        )

    return JSONResponse(content=resp)


# 简单把 web/index.html 暴露出去，方便本机测试
@app.get("/", response_class=HTMLResponse)
async def index() -> HTMLResponse:
    from pathlib import Path
    html_path = Path("web/index.html")
    if html_path.exists():
        return FileResponse(html_path)
    else:
        return HTMLResponse(content="<h1>Web files not found</h1><p>Please ensure web/index.html exists</p>")


# 静态文件服务
@app.get("/{filename}")
async def serve_static(filename: str):
    from pathlib import Path
    file_path = Path("web") / filename
    if file_path.exists() and file_path.suffix in [".js", ".css"]:
        return FileResponse(file_path)
    return JSONResponse(status_code=404, content={"error": "not found"})


if __name__ == "__main__":
    import uvicorn
    import os
    from pathlib import Path

    # 1.4.1-core: 确保基础设施已初始化
    ConfigCenter.init(env=os.getenv("LUNA_ENV", "dev"))
    LogManager.init()
    
    log.info("=" * 60)
    log.info("Luna Badge Realtime Server v1.4.1-core 启动")
    log.info("=" * 60)
    log.info(f"环境: {ConfigCenter.get('env', 'dev')}")
    log.info(f"日志级别: {ConfigCenter.get('logging.level', 'INFO')}")

    # 检查是否有 SSL 证书
    cert_dir = Path("ssl_certs")
    key_file = cert_dir / "key.pem"
    cert_file = cert_dir / "cert.pem"

    if key_file.exists() and cert_file.exists():
        log.info("[SERVER] 使用 HTTPS (SSL 证书已找到)")
        uvicorn.run(
            "realtime_server:app",
            host="0.0.0.0",
            port=5001,
            reload=True,
            ssl_keyfile=str(key_file),
            ssl_certfile=str(cert_file),
        )
    else:
        log.warning("[SERVER] 使用 HTTP (未找到 SSL 证书)")
        log.info("[SERVER] 提示: 运行 'bash generate_ssl_cert.sh' 生成证书以支持 HTTPS")
        uvicorn.run("realtime_server:app", host="0.0.0.0", port=5001, reload=True)
