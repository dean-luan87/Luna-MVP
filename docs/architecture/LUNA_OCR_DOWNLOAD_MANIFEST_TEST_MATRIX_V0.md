## Phase-ModelOCR-003

OCR Download & Manifest Readiness Test Matrix v0

### 0. 本阶段边界（提醒）

本矩阵只验证“manifest/readiness 逻辑”，不下载、不跑 OCR、不接 runtime。

### 1. Verifier 覆盖项（A–J）

- **A**：PaddleOCR manifest 生成成功
- **B**：缺权重时不伪造 `pass`
- **C**：权重文件存在时记录 `sha256/size`
- **D**：macOS Vision system provider manifest 可生成
- **E**：PaddleOCR-VL candidate manifest 可 `pending`
- **F**：DeepSeek-OCR candidate manifest 可 `pending`
- **G**：`raw_text_only=true`
- **H**：`semantic_interpretation_enabled=false`
- **I**：`allows_execute_now=false`
- **J**：readiness 失败/partial 不进入 runtime（report 只给 `do_not_enter_runtime`）

### 2. 对应工具

- 生成 manifest：`tools/build_ocr_model_manifest_v0.py`
- readiness 检查：`tools/check_ocr_model_readiness_v0.py`
- verifier：`tools/verify_ocr_manifest_readiness_v0.py`

### 3. 建议执行命令（离线安全）

```bash
cd "/Users/luanlei/Desktop/Luna-Core"
python3 tools/verify_ocr_manifest_readiness_v0.py
```

