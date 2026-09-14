# LUNA — PaddleOCR Alternative Weight Source Matrix v0

## Phase

- **Phase-ModelOCR-003-Fix-003**

## 来源矩阵

| 来源 | 适用场景 | 优点 | 风险 / 依赖 |
|------|-----------|------|-------------|
| **official / 缓存** | 网络曾可达、已有 `.paddleocr` 等缓存 | 与 PaddleOCR 默认行为一致 | 托管不可达时无效；init-only 仍可能失败 |
| **Hugging Face 仓库** | 使用 `PaddlePaddle/*` 官方页模型 | 版本与页面可追溯 | 需 `huggingface_hub`；须确认 det/rec **配套** |
| **manual_url / Gitee 直链** | 有可信直链或国内镜像 | 灵活 | URL 必须可信；禁止混用不明版本 |
| **local_dir** | 已手动下载并解压 | 最稳、可完全离线 | 需人工确认目录与版本 |

## cls 策略

- **GO（完全 pinned）**：det + rec + cls 齐全。  
- **CONDITIONAL_GO**：`--cls-optional`，cls 缺失但 manifest 与 readiness 显式 `pinned_partial` / optional，且 hash 记录完整、不伪造 pass。

## 与运行时关系

| 禁止项 | 说明 |
|--------|------|
| 运行时临时下载 | Luna 主链不得依赖 PaddleOCR 自动拉权重 |
| 本阶段跑 OCR | 不允许 benchmark / 样本识别验收 |
