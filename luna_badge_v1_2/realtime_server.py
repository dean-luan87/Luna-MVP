# realtime_server.py

import io
import time
from typing import Dict, Any

import cv2
import numpy as np
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse

from core.yolo_detector import YoloDetector

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
    """
    t0 = time.perf_counter()
    content = await frame.read()

    # 解析成 RGB
    image_array = np.frombuffer(content, dtype=np.uint8)
    img_bgr = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    if img_bgr is None:
        return JSONResponse(
            status_code=400,
            content={"error": "invalid_image", "message": "cannot decode image"},
        )

    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    # 推理
    det_result = detector.detect(img_rgb)
    boxes = det_result.to_dict()["boxes"]

    t1 = time.perf_counter()
    latency_ms = (t1 - t0) * 1000.0

    resp = {
        "latency_ms": latency_ms,
        "box_count": len(boxes),
        "boxes": boxes,
    }

    print(
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

    # 检查是否有 SSL 证书
    cert_dir = Path("ssl_certs")
    key_file = cert_dir / "key.pem"
    cert_file = cert_dir / "cert.pem"

    if key_file.exists() and cert_file.exists():
        print("[SERVER] 使用 HTTPS (SSL 证书已找到)")
        uvicorn.run(
            "realtime_server:app",
            host="0.0.0.0",
            port=5001,
            reload=True,
            ssl_keyfile=str(key_file),
            ssl_certfile=str(cert_file),
        )
    else:
        print("[SERVER] 使用 HTTP (未找到 SSL 证书)")
        print("[SERVER] 提示: 运行 'bash generate_ssl_cert.sh' 生成证书以支持 HTTPS")
        uvicorn.run("realtime_server:app", host="0.0.0.0", port=5001, reload=True)
