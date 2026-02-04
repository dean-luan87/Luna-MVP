## OCR v0-real 验证记录

### PaddleOCR 本机崩溃（macOS / PaddleX）
- **现象**: 运行 `tools/demo_ocr_paddle_images.py` 或 `tools/demo_ocr_paddle_real_camera.py` 时进程退出码 139（segfault）。
- **复现**: 已在本机多次复现，模型加载完成后仍崩溃。
- **环境提示**:
  - `urllib3` LibreSSL 警告（macOS SSL 版本）
  - PaddleX pipeline 初始化后崩溃
- **已尝试**:
  - 限制线程（OMP/MKL/OPENBLAS/VECLIB/NUMEXPR）
  - `KMP_DUPLICATE_LIB_OK=True`
  - 不影响结果，仍崩溃
- **当前结论**: 本机环境不稳定，建议在 **conda / docker** 环境中重新验证。

### 计划（D0 后处理）
1. 在隔离环境（conda / docker）复跑 PaddleOCR
2. 若稳定，回接 `PaddleOcrRunner`
3. 若仍不稳，保留 YOLO11 作为 L0 信号，PaddleOCR 仅离线验证
